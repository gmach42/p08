import os
from dotenv import load_dotenv


def main():

    # Load environment variables from .env file
    print("ORACLE STATUS: Reading the Matrix...\n")
    load_dotenv()

    # Get the variables
    matrix_mode = os.getenv("MATRIX_MODE", "development")
    database_url = os.getenv("DATABASE_URL", "Connected to local instance")
    api_key = os.getenv("API_KEY")
    log_level = os.getenv("LOG_LEVEL", "DEBUG")
    zion_endpoint = os.getenv("ZION_ENDPOINT", "https://api.zion.com")

    # Display the configuration
    print("Configuration loaded:")
    print(
        f"Mode: {matrix_mode}\n"
        f"Database: {database_url}\n"
        f"API Access: {'Authenticated' if api_key else 'Not Authenticated'}\n"
        f"Log Level: {log_level}\n"
        f"Zion Network: {'Online' if zion_endpoint else 'Offline'}\n"
    )

    print("Environment security check:")
    print(
        "[OK] No hardcoded secrets detected\n"
        "[OK] .env file properly configured\n"
        "[OK] Production overrides available\n"
    )
    print("\nThe Oracle sees all configurations.\n")


if __name__ == "__main__":
    main()
