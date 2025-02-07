<br />
<div align="center">
  <a >
    <img src="git/logo.webp" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">🔎 NetSpy 🔎</h3>

  <p align="center">
    🕵️ Keep an eye on those domains
    <br />
    <a href="https://github.com//Samuel-Hinchliffe/NetSpy"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com//Samuel-Hinchliffe/NetSpy/issues">Report Bug</a>
    ·
    <a href="https://github.com//Samuel-Hinchliffe/NetSpy/issues">Request Feature</a>
  </p>
</div>

# About

This project is a free and open-source OSINT / OpSec tool designed to enhance web domain monitoring and threat detection.
Stay alert to changes in domain behavior by tracking HTTP response codes.

For example, you've got an important domain that you need to keep an eye on. You can use NetSpy to monitor the domain and receive alerts when the domain is down or when the HTTP response code changes.

Another example, you've got a list of hostile domains that you want to keep an eye on. NetSpy will monitor these domains and alert you when the response code changes.

## 💻 Features

1. Set up a list of domains to monitor.
2. Be alerted when a domain is down or when the HTTP response code changes.
3. Be alerted on Email / Telegram

## Usage Instructions

To use this application, follow the steps below:

### 1. Clone the repository to your local machine.

### 2. Create a virtual environment:

```bash
python -m venv venv
```

### 3. Activate the virtual environment:

- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 5 Fill out the domain list in the **data/DomainsToWatch.txt** file. Each domain should be on a new line.

```bash
example.com
example2.com
```

### 6. Run the script

#### Email Only

To run the script and receive alerts via email, use the following command:

```bash
python RunNetSpy.py --email example@example.com
```

#### Telegram Only

To run the script and receive alerts via Telegram.
If you don't have a Telegram bot set up, you can follow the instructions [here](https://www.directual.com/lesson-library/how-to-create-a-telegram-botr) to create one.

use the following command:

```bash
python RunNetSpy.py --telegram CHAT_ID API_TOKEN
```

#### Both Email and Telegram

To run the script and receive alerts via both email and Telegram, use the following command:

```bash
python RunNetSpy.py --email example@example.com --telegram CHAT_ID API_TOKEN
```

1. You'll want to run this script regularly to monitor the domains. See the section below for instructions on how to automate this process via a cron job.

### Automate with a Cron Job

To automate the script execution, you can set up a cron job. Here's an example of how to run the script every hour:

1. Open your crontab file:

```bash
crontab -e
```

2. Add the following line to schedule the script to run every hour:

```bash
0 * * * * /path/to/your/venv/bin/python /path/to/your/RunNetSpy.py --email example@example.com --telegram CHAT_ID API_TOKEN
```

Make sure to replace `/path/to/your/venv/bin/python` with the path to your Python interpreter in the virtual environment and `/path/to/your/RunNetSpy.py` with the path to your script.

Save and close the crontab file. Your script will now run every hour, and you will receive alerts as configured.

## Limitations

This isn't designed to be a full-fledged monitoring solution. It's a simple tool to help you keep an eye on a small number of domains. If you need more advanced monitoring capabilities, you should consider using a dedicated monitoring service.

It uses a json file to store the last known response code for each domain. So it will be able to handle a limited number of domains before running into performance issues.

Of course, a SQL database would be a better choice for a production environment. But for a small number of domains, a json file should be sufficient.

Want to contribute? Great! Feel free to fork the repository and submit a pull request.

## Author

Samuel Hinchliffe

- [Linkedin](https://www.linkedin.com/feed/)
