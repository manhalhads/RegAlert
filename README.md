# RegAlert
 A notification script designed to monitor and log into the FAST-NUCES FLEX student portal, handle reCAPTCHA bypass, and alert you instantly when course registration opens.


## Prerequisites
* Python 3.8+ installed on your system.

## Installation

1. **Clone or Download this repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/your-repo-name.git](https://github.com/YOUR_USERNAME/your-repo-name.git)
   cd RegAlert

2. **Install the required dependencies:**
    ```bash
    pip install playwright playwright-stealth playwright-recaptcha python-dotenv playsound3
    playwright install chromium

3. **Configure your credentials:**

    Create a file named .env in the root folder.

    Add your credentials inside it like this:
    USERNAME=YourRollNumber
    PASSWORD=YourPassword

Usage

Run the script via your terminal:
python main.py

Potential issues:
Recaptcha v3 may not be bypassed in every scenario.
This script relies on Flex's UI and code of August 2026. It may fail for future versions.
