# BrowserStack demo – Python + pytest

This is a small UI test suite I wrote for the BrowserStack Customer Engineer exercise.

The goal of the test is to:

- open https://bstackdemo.com
- log in with `demouser / testingisfun99`
- (if possible) filter products by **Samsung**
- find the **Galaxy S20+** product
- where the UI allows it, try to “favourite” the item and check it on the Favourites page

The same test is run on three environments through BrowserStack:

- Windows 10 / Chrome (latest)
- macOS Ventura / Firefox (latest)
- Samsung Galaxy S22 / Android 12 (Chrome)

---

## Project layout

- `tests/conftest.py` – BrowserStack capabilities and the `driver` fixture  
- `tests/test_favorite_samsung.py` – main UI test for the Galaxy S20+ flow  
- `browserstack.yml` – tells BrowserStack SDK which environments to run  
- `requirements.txt` – Python dependencies  
- `Jenkinsfile` – Jenkins pipeline script

---

## How the test behaves

### Login

The test clicks **Sign In**, chooses `demouser` and `testingisfun99` from the dropdowns, and logs in.

### Waiting for products

After login, I wait until at least one product title (`p.shelf-item__title`) is visible.

- On desktop browsers: if no products appear, the test fails.
- On the real Android device: if titles never appear (because the layout behaves differently), the test stops early and doesn’t fail the whole suite.

### Samsung filter

I try to apply the Samsung brand filter in a “best effort” way:

1. First I look for a checkbox with `value="Samsung"`.
2. If that isn’t found, I look for a `<label>` that contains the text “Samsung”.

If neither is found (for example on a different mobile layout), the test just continues without filtering.

### Galaxy S20+ and favourites

Once products are visible, the test:

1. Finds the **Galaxy S20+** title.
2. Locates its parent product card.
3. Tries a small set of CSS selectors to find a “favourite/heart” button inside the card.
4. If a favourite button exists:
   - clicks it,
   - opens the **Favourites** page,
   - checks that **Galaxy S20+** appears there.
5. If no favourite button is found, the test still passes as long as Galaxy S20+ is visible in the main list.

This makes the test a bit more tolerant across desktop vs real mobile devices.

---

## Running the tests locally

Prerequisites:

- Python 3.9+
- A BrowserStack Automate account

Set your credentials as environment variables (no hard-coding in the code):

**bash**
export BROWSERSTACK_USERNAME=your_username
export BROWSERSTACK_ACCESS_KEY=your_access_key
