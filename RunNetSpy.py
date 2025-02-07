from classes.NetSentinel import NetSentinel
import argparse


def main():
    """
    Entry point for the NetSentinel Command Line Interface.
    This function parses command line arguments to determine the method of
    sending the report (either via email or Telegram), performs validation
    checks on the provided arguments, and then executes the domain checking
    and report sending processes.
    Command Line Arguments:
    --email (str): Email address to send the report to.
    --telegram (tuple): A tuple containing the Telegram chat ID and API token
                        to send the report to.
    Raises:
    argparse.ArgumentError: If the provided email address or Telegram
                            credentials are invalid, or if the required
                            utilities are not installed.
    Example:
    python RunNetSentinel.py --email example@example.com
    python RunNetSentinel.py --telegram CHAT_ID API_TOKEN
    python RunNetSentinel.py --email example@example.com --telegram CHAT_ID API_TOKEN
    """
    parser = argparse.ArgumentParser(description="NetSentinel Command Line Interface")
    parser.add_argument("--email", type=str, help="Email address to send the report to")
    parser.add_argument(
        "--telegram",
        nargs=2,
        metavar=("CHAT_ID", "API_TOKEN"),
        help="Telegram chat ID and API token to send the report to",
    )
    args = parser.parse_args()

    # Validation checks
    if args.email:
        if NetSentinel.is_mail_utility_installed() is False:
            parser.error(
                "The 'mail' utility is not installed, please install and configure a mail client"
            )

        # Not exactly RFC 5322 compliant, but a simple check
        if "@" not in args.email or "." not in args.email:
            parser.error("Invalid email address format")

    if args.telegram:
        chat_id, api_token = args.telegram
        if not chat_id.isdigit():
            parser.error("Invalid Telegram chat ID format")
        if not api_token:
            parser.error("Invalid Telegram API token format")

    net_sentinel = NetSentinel()

    # Check domains in live
    net_sentinel.check_domains()

    # Sent report by selected method
    if args.email:
        net_sentinel.send_report_email(args.email)

    if args.telegram:
        chat_id, api_token = args.telegram
        net_sentinel.send_report_telegram(chat_id, api_token)


if __name__ == "__main__":
    main()
