#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import smtplib
from email.mime.text import MIMEText
import os

# ==== Config from Environment Variables ====
PINCODE = os.getenv("PINCODE", "560037")  # Real PIN comes from GitHub Secrets
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def send_email_report(results):
    """Send product availability results via Gmail SMTP"""
    report_text = "\n".join(results)
    msg = MIMEText(report_text)
    msg['Subject'] = f'Amul Products Availability Report for {PINCODE}'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print("📧 Email sent successfully!")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

def set_location_by_pincode(driver):
    """Enter pincode and apply it on the page"""
    wait = WebDriverWait(driver, 15)
    try:
        pincode_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Enter Your Pincode']"))
        )
        pincode_input.clear()
        pincode_input.send_keys(PINCODE)
        print("📍 Entered pincode (hidden in logs).")

        pincode_suggestion = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@role='button']//p[text()='{PINCODE}']"))
        )
        pincode_suggestion.click()
        print("📌 Clicked pincode suggestion.")

        apply_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply')]"))
        )
        apply_button.click()
        print("✅ Applied pincode successfully.")

        time.sleep(4)
    except Exception as e:
        print(f"⚠️ Could not set pincode: {e}")

def check_product_availability(driver, url, product_name):
    """Check if a given Amul product is available for the set pincode"""
    driver.get(url)
    set_location_by_pincode(driver)

    try:
        driver.find_element(By.XPATH, "//div[@class='alert alert-danger mt-3' and contains(text(),'Sold Out')]")
        return f"{product_name} -> Out of Stock"
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.CSS_SELECTOR, "div.price-wrap.product-prices.text-left.pt-3")
        return f"{product_name} -> Available"
    except NoSuchElementException:
        pass

    return f"{product_name} -> Unknown"

def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    products = {
        "protein_milk_32": "https://shop.amul.com/en/product/amul-high-protein-milk-250-ml-or-pack-of-32",
        "rose_lassi": "https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30",
        "buttermilk": "https://shop.amul.com/en/product/amul-high-protein-buttermilk-200-ml-or-pack-of-30",
        "plain_lassi": "https://shop.amul.com/en/product/amul-high-protein-plain-lassi-200-ml-or-pack-of-30",
        "protein_milk_8": "https://shop.amul.com/en/product/amul-high-protein-milk-250-ml-or-pack-of-8"
    }

    results = []
    for name, url in products.items():
        print(f"🔍 Checking {name} ...")
        status_line = check_product_availability(driver, url, name)
        results.append(status_line)
        print(status_line)
        print("-" * 40)

    print("\n✅ Final Availability Status:")
    for line in results:
        print(line)

    # Send email only if at least one product is available
    if any("Available" in r for r in results):
        print("📧 At least one product available — sending email...")
        send_email_report(results)
    else:
        print("📭 No products available — email not sent.")

    driver.quit()

if __name__ == "__main__":
    main()
