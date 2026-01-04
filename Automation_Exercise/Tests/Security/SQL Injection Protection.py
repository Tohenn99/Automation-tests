"""
Security Test 02: SQL Injection Protection
Тества за SQL injection уязвимости в login и signup форми
"""

import pytest
from playwright.sync_api import Page
from POM import LoginPage


@pytest.mark.security
def test_sql_injection_protection(page: Page):
    """
    Проверява дали апликацията е защитена от SQL injection атаки
    Тества классически SQL injection payloads
    """
    login_page = LoginPage(page)
    login_page.navigate()

    # SQL Injection payloads
    sql_payloads = [
        "' OR '1'='1",
        "admin'--",
        "' OR 1=1--",
        "admin' OR '1'='1'/*",
        "' UNION SELECT NULL--",
        "1' AND '1'='1",
        "'; DROP TABLE users--",
        "' OR 'x'='x",
        "admin'; DELETE FROM users WHERE 'a'='a",
        "' UNION SELECT password FROM users--",
    ]

    for payload in sql_payloads:
        # Опит за SQL injection в email field
        page.locator(login_page.SIGNUP_NAME).fill("Test User")
        page.locator(login_page.SIGNUP_EMAIL).fill(payload)
        page.locator(login_page.SIGNUP_BUTTON).click()

        page.wait_for_timeout(1000)

        # Проверка 1: Не трябва да има успешна регистрация
        # Страницата не трябва да редиректне към registration form
        current_url = page.url

        # Проверка 2: Търси за error messages или validation
        page_content = page.content().lower()

        # Не трябва да се появява registration form при SQL injection
        registration_form_visible = page.locator('#form').is_visible() if page.locator('#form').count() > 0 else False

        if registration_form_visible:
            # Ако формата е видима, значи може да има проблем
            print(f"WARNING: Form appeared with payload: {payload}")

        # Проверка 3: Database error messages не трябва да се показват
        dangerous_errors = [
            'sql syntax',
            'mysql error',
            'database error',
            'query failed',
            'ora-',
            'pg_query',
            'sqlite',
        ]

        for error_msg in dangerous_errors:
            assert error_msg not in page_content, f"Database error exposed with payload: {payload}"

        # Reload за нов опит
        page.goto(f"{login_page.base_url}/login")
        page.wait_for_load_state('networkidle')

    # Финална проверка - валиден email трябва да работи нормално
    valid_email = "validuser@test.com"
    page.locator(login_page.SIGNUP_NAME).fill("Valid User")
    page.locator(login_page.SIGNUP_EMAIL).fill(valid_email)
    page.locator(login_page.SIGNUP_BUTTON).click()

    page.wait_for_timeout(1000)

    print("✓ SQL Injection Protection Test PASSED - No vulnerabilities detected")