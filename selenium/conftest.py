import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

BASE_URL = os.getenv("APP_URL", "http://localhost:3000")
UNIQUE = str(int(time.time()))


@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")

    drv = webdriver.Chrome(options=opts)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()


@pytest.fixture(scope="module")
def test_user():
    return {
        "username": f"seluser_{UNIQUE}",
        "password": "Sel3niumP@ss",
    }
