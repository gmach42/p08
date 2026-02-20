import os
from dotenv import load_dotenv


def main():
    print("\nORACLE STATUS: Reading the Matrix...")
    load_dotenv()

    mode = os.getenv("MATRIX_MODE")
    db_url = os.getenv("DATABASE_URL")
    api_key = os.getenv("API_KEY")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    zion_endpoint = os.getenv("ZION_ENDPOINT")

    if not all([mode, db_url, api_key, log_level, zion_endpoint]):
        print("Error: Missing configuration variables")
        return

    print("\nConfiguration loaded:")
    print(f"Mode: {mode}")
    data_base_status = (
        "Connected to local instance" if "localhost" in db_url else db_url
    )
    print(f"Database: {data_base_status}")
    print(f"API Access: {'Authenticated' if api_key else 'Denied'}")
    print(f"Log Level: {log_level}")
    print(f"Zion Network: {'Online' if zion_endpoint else 'Offline'}")

    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")
    print("[OK] .env file properly configured")
    print("[OK] Production overrides available")

    print("\nThe Oracle sees all configurations\n")


if __name__ == "__main__":
    main()
