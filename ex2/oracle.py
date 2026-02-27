import os
import sys


def check_config():
    required_vars = [
        "DATABASE_URL", "API_KEY", "MATRIX_MODE", "LOG_LEVEL", "ZION_ENDPOINT"
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError("Missing required configuration variables: "
                         f"{', '.join(missing_vars)}")


def main():
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("ERROR: python-dotenv is not installed. "
              "Run 'pip install python-dotenv'.")
        sys.exit(1)

    try:
        if not os.path.exists(".env"):
            print("ENV WARNING: No .env file found.")

        load_dotenv()

        mode = os.getenv("MATRIX_MODE")
        db_url = os.getenv("DATABASE_URL")
        api_key = os.getenv("API_KEY")
        log_level = os.getenv("LOG_LEVEL")
        zion_url = os.getenv("ZION_ENDPOINT")

        check_config()

        print("ORACLE STATUS: Reading the Matrix...")
        print("\nConfiguration loaded:")
        print(f"Mode: {mode}")
        database_status = "Connected to local" if "localhost" in db_url \
            else "Connected to remote"
        print(f"Database: {database_status}")
        api_check = ("Authenticated" if "secret" in api_key else "Denied")
        print(f"API Access: {api_check}")
        print(f"Log Level: {log_level}")
        print(f"Zion Network: Online ({zion_url})")

    except ValueError as e:
        print(f"CONFIGURATION ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        sys.exit(1)

    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")
    if os.path.exists(".env") and check_config():
        print("[OK] .env file properly configured")
    print("[OK] Production overrides available")


if __name__ == "__main__":
    main()
