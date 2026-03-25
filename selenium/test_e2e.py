import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv("APP_URL", "http://localhost:3000")
UNIQUE = str(int(time.time()))


# ── Helpers ──────────────────────────────────────────────

def _wait(driver, timeout=10):
    return WebDriverWait(driver, timeout)


# ── 1. Registration & Login ─────────────────────────────

def test_register_new_user(driver, test_user):
    driver.get(f"{BASE_URL}/login")

    # Switch to Register mode
    _wait(driver).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Register']"))).click()

    driver.find_element(By.ID, "username").send_keys(test_user["username"])
    driver.find_element(By.ID, "password").send_keys(test_user["password"])
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Should redirect to /students after registration
    _wait(driver).until(EC.url_contains("/students"))
    assert "/students" in driver.current_url


def test_logout(driver):
    _wait(driver).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Logout']"))).click()
    _wait(driver).until(EC.url_contains("/login"))
    assert "/login" in driver.current_url


def test_login_existing_user(driver, test_user):
    driver.get(f"{BASE_URL}/login")
    _wait(driver).until(EC.presence_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys(test_user["username"])
    driver.find_element(By.ID, "password").send_keys(test_user["password"])
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    _wait(driver).until(EC.url_contains("/students"))
    assert "/students" in driver.current_url


def test_login_invalid_credentials(driver):
    driver.get(f"{BASE_URL}/login")
    _wait(driver).until(EC.presence_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys("nonexistent")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    error = _wait(driver).until(EC.presence_of_element_located((By.CLASS_NAME, "error")))
    assert error.text != ""


# ── 2. Add Student ──────────────────────────────────────

def test_add_student(driver, test_user):
    # Ensure logged in
    driver.get(f"{BASE_URL}/login")
    _wait(driver).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(test_user["username"])
    driver.find_element(By.ID, "password").send_keys(test_user["password"])
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    _wait(driver).until(EC.url_contains("/students"))

    # Navigate to Add Student
    driver.get(f"{BASE_URL}/add-student")
    _wait(driver).until(EC.presence_of_element_located((By.ID, "name")))

    driver.find_element(By.ID, "name").send_keys(f"Selenium Student {UNIQUE}")
    driver.find_element(By.ID, "age").send_keys("21")
    driver.find_element(By.ID, "email").send_keys(f"sel_{UNIQUE}@test.com")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    success = _wait(driver).until(EC.presence_of_element_located((By.CLASS_NAME, "success")))
    assert "successfully" in success.text.lower()


# ── 3. Student List Validation ──────────────────────────

def test_student_list_shows_added_student(driver):
    driver.get(f"{BASE_URL}/students")
    _wait(driver).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    page_text = driver.find_element(By.TAG_NAME, "table").text
    assert f"Selenium Student {UNIQUE}" in page_text
    assert f"sel_{UNIQUE}@test.com" in page_text
