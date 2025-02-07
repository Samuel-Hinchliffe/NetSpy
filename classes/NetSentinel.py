import requests
import os
import json
from datetime import datetime
import subprocess


class NetSentinel:
    """
    NetSentinel is a class that monitors the status of specified domains and reports any changes.
    Attributes:
        domainsToCheckPath (str): Path to the file containing domains to check.
        historicalDataPath (str): Path to the file containing historical data.
        domainsToCheck (list): List of domains to check.
        historicalData (dict): Dictionary containing historical data of domains.
        report (list): List of domains with status changes.
        headers (dict): HTTP headers for making requests.
    Methods:
        __init__():
            Initializes the NetSentinel instance, loads domains and historical data.
        load_domains():
            Loads the list of domains to check from the specified file.
        load_historical_data():
            Loads historical data from the specified file. Creates the file if it does not exist.
        save_historical_data():
            Saves the current historical data to the specified file.
        check_domains():
            Checks the status of each domain and updates the historical data. Generates a report for any status changes.
        is_mail_utility_installed() -> bool:
            Checks if the 'mail' utility is installed on the system.
        send_report_telegram(chatId: str, apiToken: str):
            Sends the report of status changes to a specified Telegram chat.
        send_report_email(email: str):
            Sends the report of status changes to a specified email address.
    """

    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.domainsToCheckPath = os.path.join(base_path, "data", "DomainsToWatch.txt")
        self.historicalDataPath = os.path.join(base_path, "data", "history.json")
        self.domainsToCheck = []
        self.historicalData = {}
        self.report = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }

        self.load_domains()
        self.load_historical_data()

    def load_domains(self):
        """
        Loads domains from a file and extends the domainsToCheck list with the contents.

        This method reads the file specified by the attribute `domainsToCheckPath` and
        appends each line from the file to the `domainsToCheck` list.

        Raises:
            FileNotFoundError: If the file specified by `domainsToCheckPath` does not exist.
            IOError: If there is an error reading the file.
        """
        with open(self.domainsToCheckPath, "r") as w:
            self.domainsToCheck.extend(w.readlines())

    def load_historical_data(self):
        """
        Loads historical data from a JSON file specified by `self.historicalDataPath`.

        If the file does not exist, it creates an empty JSON file at the specified path.
        The loaded data is stored in the `self.historicalData` attribute.

        Raises:
            JSONDecodeError: If the file contains invalid JSON.
            IOError: If there is an issue reading from or writing to the file.
        """
        if not os.path.exists(self.historicalDataPath):
            with open(self.historicalDataPath, "w") as file:
                json.dump({}, file)
        with open(self.historicalDataPath, "r") as file:
            self.historicalData = json.load(file)

    def save_historical_data(self):
        """
        Save the historical data to a JSON file.

        This method writes the historical data stored in the `historicalData` attribute
        to a file specified by the `historicalDataPath` attribute in JSON format.

        Raises:
            IOError: If there is an error opening or writing to the file.
        """
        with open(self.historicalDataPath, "w") as json_file:
            json.dump(self.historicalData, json_file, indent=4)

    def check_domains(self):
        """
        Checks the status of each domain in the domainsToCheck list and updates the historical data.
        This method iterates over the domainsToCheck list, sends an HTTP GET request to each domain,
        and updates the historical data with the status code of the response. If the status code has
        changed since the last check, it marks the status as recently changed and appends the domain's
        data to the report list.
        Attributes:
            domainsToCheck (list): A list of domains to check.
            headers (dict): HTTP headers to include in the request.
            historicalData (dict): A dictionary storing historical data of domain statuses.
            report (list): A list to store domains with recently changed statuses.
        Raises:
            Exception: If there is an error while making the HTTP request, it is caught and the domain is skipped.
        Returns:
            None
        """
        for domain in self.domainsToCheck:
            domain = domain.strip()
            lastStatus = self.historicalData.get(domain, {}).get("status", None)
            newStatus = None
            try:
                response = requests.get(
                    domain, headers=self.headers, allow_redirects=True
                )
                newStatus = response.status_code
            except Exception as e:
                continue

            statusChangedRecently = newStatus != lastStatus

            self.historicalData[domain] = {
                "name": domain,
                "status": newStatus,
                "statusChangedRecently": statusChangedRecently,
                "last_checked": datetime.now().strftime("%Y-%m-%d"),
            }

            if statusChangedRecently:
                self.report.append(self.historicalData[domain])

        self.save_historical_data()

    @staticmethod
    def is_mail_utility_installed():
        return subprocess.run(["which", "mail"], stdout=subprocess.PIPE).returncode == 0

    def send_report_telegram(self, chatId: str, apiToken: str):
        """
        Sends a report to a specified Telegram chat using the provided API token.

        Parameters:
        chatId (str): The ID of the Telegram chat where the report will be sent.
        apiToken (str): The API token for the Telegram bot.

        Returns:
        None

        Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.

        Notes:
        - The report is sent only if there are changes reported.
        - The report is formatted as a JSON string with an indentation of 4 spaces.
        - The method prints a success message if the report is sent successfully.
        - The method prints an error message if the report fails to send.
        """
        if len(self.report) > 0:
            message = "🛡️👺 NetSentinel - Reported Changes\n\n" + json.dumps(
                self.report, indent=4
            )
            url = f"https://api.telegram.org/bot{apiToken}/sendMessage"
            payload = {
                "chat_id": chatId,
                "text": message,
            }
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                print("Report sent to Telegram channel")
            except requests.exceptions.RequestException as e:
                print(f"Failed to send Telegram message: {e}")

    def send_report_email(self, email: str):
        """
        Sends a report email with the changes detected by NetSentinel.

        Args:
            email (str): The recipient's email address.

        Raises:
            subprocess.CalledProcessError: If the email sending process fails.

        Returns:
            None
        """
        if len(self.report) > 0:
            subject = "🛡️👺 NetSentinel - Reported Changes"
            recipient = email
            body = json.dumps(self.report, indent=4)
            try:
                subprocess.run(
                    ["mail", "-s", subject, recipient],
                    input=body,
                    text=True,
                    check=True,
                )
                print(f"Report emailed to {recipient}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to send email: {e}")
