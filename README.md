# RegAlert
A notification script designed to monitor and log into the FAST-NUCES FLEX student portal, handle reCAPTCHA bypass, and alert you instantly when course registration opens.
Auto relogs in when faced with Server or Runtime Error. A notification sound will continue playing when Registration opens until the script execution is forcefully stopped.


## Prerequisites
* Python 3.8+ installed on your system.

## Installation

1. **Clone or Download this repository:**
   ```bash
   git clone https://github.com/manhalhads/RegAlert
   cd RegAlert

2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    playwright install chromium

3. **Configure your credentials:**
   * Create a file named `.env` in the root folder.
   * Add your credentials inside it like this:
     ```bash
     USERNAME=YourRollNumber # e.g.22L8976
     PASSWORD=YourPassword # e.g 012356789
     

**Usage**

Run the script via your terminal:
```bash
python main.py
```


**Potential issues:**<br>
Recaptcha v3 may not be bypassed in every scenario.
This script relies on Flex's UI and code of August 2026. It may fail for future versions.

## Issues & Troubleshooting

If you encounter unexpected behavior or errors while using RegAlert, check the common issues below before opening a new issue.

| Issue | Possible Cause | Solution |
| :--- | :--- | :--- |
| **reCAPTCHA Bypass Fails** | Google or Flex updated their reCAPTCHA scoring mechanism or Playwright's automation flags were detected. | Try running in non-headless mode (if applicable) or update your browser binaries via `playwright install --force chromium`. |
| **`Server or Runtime Error` Loop** | The FLEX portal is experiencing heavy traffic or temporary downtime. | The script is designed to auto-relog. If it loops indefinitely, check your internet connection or log into the portal manually via a browser to verify server status. |
| **Element Not Found / Script Crashes** | FAST-NUCES updated the FLEX portal UI, breaking the HTML selectors. | Open an issue on GitHub with the traceback error so selectors can be updated. |
| **Missing Dependencies / Playwright Errors** | Chromium drivers are missing or outdated. | Run `pip install --upgrade -r requirements.txt` followed by `playwright install chromium`. |


**Notes** <br>
The file has comments so you may customize the script according to your requirement (Change the refresh frequency, look for a specific text on the registration page or a button.) For details on how to do the former and more using playwright, check out playwright's documentation on https://playwright.dev/python/docs/api/class-playwright and for any questions, contact at https://fajar-shakeel.vercel.app/
