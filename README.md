# BrowserStack Demo – Python + Pytest Assignment

This is a small project where I wrote one UI test using Selenium + Pytest and ran it on multiple browsers/devices through BrowserStack.  
I also connected it to a Jenkins pipeline so the test can run automatically.

The purpose of the test is basically:
- log into bstackdemo.com  
- wait for the products to load  
- try to filter by Samsung (if available)  
- check that the Galaxy S20+ product is visible  
- and where possible, try to “favourite” it and confirm it appears in the Favourites page

Some parts of the UI change depending on device (especially on the real Android device), so I added some simple checks so the test doesn’t fully fail when the UI layout behaves differently.

---

browserstack-demo/
├── tests/
│ ├── conftest.py # Where BrowserStack capabilities + driver fixture live
│ └── test_favorite_samsung.py # The actual test file I wrote
├── browserstack.yml # Tells BrowserStack which environments to run
├── Jenkinsfile # Jenkins pipeline script
├── requirements.txt # Python packages used
└── README.md


---

## How the test works (in simple terms)

### 1. Login flow  
The script clicks “Sign In”, picks a username and password from the dropdowns, and logs in.

### 2. Waiting for the products  
I wrote a helper function that tries to wait until at least one product title appears.  
If product titles never show up:
- on desktop browsers → I fail the test  
- on mobile (real device) → I skip the rest because the UI behaves differently

### 3. Optional Samsung filter  
I tried two different locators (checkbox and label) because depending on the version of the UI it may not be displayed.  
If neither is found, I just move on without failing the test.

### 4. Locating Galaxy S20+  
Once the products are visible, the script looks for the Galaxy S20+ title and then finds its “product card” container.

### 5. Best-effort favourite  
This is optional because some layouts (especially mobile) don't show the favourite/heart button the same way.  
I search for several possible CSS selectors.  
If I find it, I click it and then open the Favourites page to verify the item is there.  
If not, the test simply stops after validating that Galaxy S20+ is present in the main list.

---

## Running the test locally (BrowserStack SDK)

### Requirements
- Python 3
- BrowserStack Automate credentials

### Install packages


python3 -m venv env
source env/bin/activate # (Windows: env\Scripts\activate)
pip install -r requirements.txt


### Set environment variables

export BROWSERSTACK_USERNAME="your-username"
export BROWSERSTACK_ACCESS_KEY="your-key"


### Run the tests

browserstack-sdk python -m pytest -q



This launches the test on:
- Windows 10 Chrome  
- macOS Firefox  
- Samsung Galaxy S22 real device

---

## Jenkins Pipeline (basic explanation)

I created a **Jenkinsfile** in the root of the repo so Jenkins can pull the project from GitHub and run the test automatically.

### Jenkins steps
1. Jenkins checks out the GitHub repository  
2. Jenkins creates a Python virtual environment  
3. Installs the requirements  
4. Runs the BrowserStack SDK command:


browserstack-sdk python -m pytest -q


### Credentials  
In Jenkins, I added two “Secret text” credentials:
- browserstack-username  
- browserstack-access-key  

The Jenkinsfile reads these and sets them as environment variables.

---

## What this project shows
- My ability to automate a UI test using Selenium + Pytest  
- Basic handling of cross-browser and mobile differences  
- Setting up BrowserStack execution  
- Setting up a working Jenkins pipeline  
- Structuring a small automation project in a clean way without over-complicating it
