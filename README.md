````markdown
# 🥛 Amul Stock Availability Checker

A Python + Selenium script that automatically checks the stock status of selected Amul products for a given pincode, and optionally sends an email report when any item is available.  
Can run **locally** or on **GitHub Actions** (for scheduled automated checks every 10 minutes).

---

## 📦 Features
- ✅ Checks stock for multiple Amul high-protein products.
- 📍 Sets location using your pincode before checking.
- 📧 Sends availability results via Gmail SMTP (only if something is available).
- ☁️ Runs on GitHub Actions for **automation**.
- 🖥 Can also be run **manually** from your local machine.

---

## 🚀 1. Running Locally

### 1.1. Install Python
Make sure Python 3.8+ is installed:

```bash
python3 --version
````

If you don’t have Python, [download it here](https://www.python.org/downloads/).

---

### 1.2. Install Google Chrome

This script uses Selenium with Chrome.
[Download Chrome](https://www.google.com/chrome/) if not already installed.

---

### 1.3. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

---

### 1.4. Install dependencies

```bash
pip install --upgrade pip
pip install selenium webdriver-manager
```

---

### 1.5. Set up environment variables

Create a `.env` file or export variables in your shell.

Example `.env`:

```env
PINCODE=123456
SENDER_EMAIL=youremail@gmail.com
RECEIVER_EMAIL=receiveremail@gmail.com
APP_PASSWORD=your_gmail_app_password
```

**Note:** Gmail requires an **App Password** for SMTP.
How to create one:

1. Enable 2-Step Verification in your Google Account.
2. Go to **Google Account > Security > App passwords**.
3. Generate an app password and paste it here.

---

### 1.6. Run the script

```bash
python final_amul_check.py
```

You should see logs like:

```
🔍 Checking protein_milk_32 ...
📍 Entered pincode
📌 Clicked pincode suggestion.
✅ Applied pincode successfully.
PINCODE - protein_milk_32 -> Available
...
📧 Email sent successfully!
```

---

## ☁️ 2. Running with GitHub Actions (Automation)

This repo includes `.github/workflows/amul_stock_check.yml` to run every 10 minutes.

---

### 2.1. Add GitHub Secrets

In your GitHub repo:

1. Go to **Settings > Secrets and variables > Actions**.
2. Add these secrets:

   * `PINCODE`
   * `SENDER_EMAIL`
   * `RECEIVER_EMAIL`
   * `APP_PASSWORD`

---

### 2.2. Push the workflow file

Make sure `.github/workflows/amul_stock_check.yml` is in your repo.

Example schedule:

```yaml
on:
  schedule:
    - cron: "*/10 * * * *"  # Every 10 minutes
  workflow_dispatch:        # Manual trigger
```

---

### 2.3. Workflow Run

* Action runs every 10 minutes.
* If a product is available, you’ll get an email report.
* You can also trigger it manually from the **Actions** tab.

---

## 🛠 Troubleshooting

* **`selenium.common.exceptions.SessionNotCreatedException`**: Update Chrome & ChromeDriver.
* **Email not sending**: Check Gmail App Password and that "Less secure apps" is not required (App Password bypasses this).
* **Timeouts**: Your internet might be slow — increase wait times in `WebDriverWait`.

---

## 📜 License

MIT License — free to use & modify.
