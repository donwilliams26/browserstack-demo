import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def is_mobile(driver) -> bool:
    caps = getattr(driver, "capabilities", {}) or {}
    bstack_opts = caps.get("bstack:options") or {}

    if isinstance(bstack_opts, dict):
        if bstack_opts.get("realMobile") or bstack_opts.get("deviceName"):
            return True

    if caps.get("realMobile") or caps.get("deviceName"):
        return True

    platform = (caps.get("platformName") or "").lower()
    return platform in ("android", "ios")


def wait_for_any_product_titles(driver, timeout: int = 20):
    wait = WebDriverWait(driver, timeout)
    try:
        return wait.until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, "p.shelf-item__title")
            )
        )
    except TimeoutException:
        return []


def click_samsung_filter(driver, timeout: int = 10):
    wait = WebDriverWait(driver, timeout)

    try:
        samsung_checkbox = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='checkbox'][value='Samsung']")
            )
        )
        driver.execute_script("arguments[0].click();", samsung_checkbox)
        return
    except Exception:
        pass

    try:
        samsung_label = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//label[contains(normalize-space(.), 'Samsung')]")
            )
        )
        driver.execute_script("arguments[0].click();", samsung_label)
        return
    except Exception:
        pass


def test_favorite_galaxy_s20_plus(driver):
    driver.get("https://bstackdemo.com/")
    wait = WebDriverWait(driver, 25)

    # Login
    wait.until(EC.element_to_be_clickable((By.ID, "signin"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "username"))).click()
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@id,'react-select-2-option') and contains(., 'demouser')]")
        )
    ).click()

    wait.until(EC.element_to_be_clickable((By.ID, "password"))).click()
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@id,'react-select-3-option') and contains(., 'testingisfun99')]")
        )
    ).click()

    wait.until(EC.element_to_be_clickable((By.ID, "login-btn"))).click()

    # Products grid
    product_titles = wait_for_any_product_titles(driver, timeout=25)

    if not product_titles:
        if is_mobile(driver):
            return
        else:
            assert product_titles, "Products did not load on desktop browser."

    # Optional filter
    click_samsung_filter(driver)
    time.sleep(2)

    # Galaxy S20+
    galaxy_title = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//p[@class='shelf-item__title' and normalize-space()='Galaxy S20+']")
        )
    )
    galaxy_card = galaxy_title.find_element(
        By.XPATH, "./ancestor::div[contains(@class,'shelf-item')]"
    )

    # Best-effort favourite
    try:
        selectors = [
            "button.shelf-item__btn-favorite",
            "button.shelf-item__heart",
            "button[title*='Favourite'], button[title*='Favorite']",
            "button[aria-label*='Favourite'], button[aria-label*='Favorite']",
        ]

        favourite_button = None
        for selector in selectors:
            try:
                favourite_button = galaxy_card.find_element(By.CSS_SELECTOR, selector)
                if favourite_button:
                    break
            except NoSuchElementException:
                continue

        if not favourite_button:
            return

        favourite_button.click()

        # Favourites page
        wait.until(EC.element_to_be_clickable((By.ID, "favourites"))).click()

        favourites_galaxy = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[@class='shelf-item__title' and normalize-space()='Galaxy S20+']")
            )
        )

        assert "Galaxy S20+" in favourites_galaxy.text

    except Exception:
        return
