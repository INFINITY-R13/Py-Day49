# Py-Day49

# LinkedIn Easy Apply Bot 🤖

A Python script that automates the process of applying for jobs on LinkedIn using Selenium. This bot is designed to handle the "Easy Apply" feature, intelligently filling in basic information and skipping more complex, multi-page applications.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📝 Description

This project uses the **Selenium** framework and **webdriver-manager** to control a Chrome browser. It navigates to a specified LinkedIn jobs search page, logs into your account, iterates through the job listings, and attempts to submit "Easy Apply" applications.

### Key Features

-   **Secure Credential Handling**: Loads your LinkedIn email, password, and phone number from environment variables instead of hardcoding them in the script.
-   **Robust Automation**: Uses Selenium's `WebDriverWait` for explicit waits, making the script more reliable than using fixed `time.sleep()` delays.
-   **Smart Application Filtering**: Detects and skips multi-step applications to only focus on the simple, single-click "Easy Apply" jobs.
-   **Automatic Driver Management**: `webdriver-manager` automatically downloads and manages the correct ChromeDriver for your browser version.
-   **Error Handling**: Includes `try...except` blocks to gracefully handle missing elements or timeouts, preventing the script from crashing unexpectedly.

---

## 🏗️ Project Structure

The project has a simple and flat file structure:

```
/LinkedIn-Job-Bot
|
├── main.py        # The main Python script with all the automation logic.
└── README.md      # This documentation file.
```

---

## 🚀 Getting Started

Follow these steps to get the bot up and running on your local machine.

### Prerequisites

-   Python 3.8 or higher
-   Google Chrome browser

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/LinkedIn-Job-Bot.git](https://github.com/your-username/LinkedIn-Job-Bot.git)
    cd LinkedIn-Job-Bot
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required Python packages:**
    ```sh
    pip install selenium webdriver-manager
    ```

4.  **Configure Environment Variables:**
    To keep your login credentials secure, you must set them as environment variables. The script will not work without them.

    * **On Windows (Command Prompt):**
        ```sh
        setx LINKEDIN_EMAIL "your_email@example.com"
        setx LINKEDIN_PASSWORD "your_super_secret_password"
        setx PHONE_NUMBER "your_phone_number"
        ```
        *(Note: You may need to restart your terminal for these changes to take effect.)*

    * **On macOS/Linux (Terminal):**
        ```sh
        export LINKEDIN_EMAIL="your_email@example.com"
        export LINKEDIN_PASSWORD="your_super_secret_password"
        export PHONE_NUMBER="your_phone_number"
        ```
        *(To make these permanent, add the `export` commands to your shell profile, like `~/.bashrc` or `~/.zshrc`, and then run `source ~/.bashrc`.)*

---

## ⚙️ Usage

1.  **Customize the Job Search (Optional):**
    Open the `main.py` file and modify the `LINKEDIN_JOBS_URL` constant to match your desired search query (e.g., job title, location).

    ```python
    # In main.py
    LINKEDIN_JOBS_URL = "[https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=your_job_title&location=Your_Location](https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=your_job_title&location=Your_Location)"
    ```

2.  **Run the script:**
    Make sure your virtual environment is activated, and then run:
    ```sh
    python main.py
    ```

3.  **Handle CAPTCHA:**
    The script will open a Chrome window and navigate to LinkedIn. It will then pause and prompt you in the terminal to solve any CAPTCHA puzzle manually.
    ```
    Press Enter when you have solved the Captcha...
    ```
    After you solve it and press **Enter** in the terminal, the bot will resume and start applying.

4.  **Enable Job Submission:**
    For safety, the final submission click is commented out by default. To enable the bot to actually submit applications, you need to uncomment the following line in `main.py`:

    ```python
    # Find this line in the main loop:
    # submit_button.click() # Uncomment this line to actually submit the application
    ```

---

## ⚠️ Disclaimer

-   This script is intended for **educational purposes only**.
-   Automating user interactions can be against the **Terms of Service** of websites like LinkedIn. Use this bot responsibly and at your own risk.
-   The bot will perform actions on your behalf on your LinkedIn profile. Ensure you understand what the code does before running it with job submission enabled. The creators of this script are not responsible for any actions taken by the bot.

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.