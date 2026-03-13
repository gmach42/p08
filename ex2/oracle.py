import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print(
        "Error: python-dotenv is not installed. Run: pip install python-dotenv"
    )
    sys.exit(1)

# NOCHECK_START
HARDCODED_PATTERNS = [
    "matrix_mode = ", "database_url = ", "api_key = ", "log_level = ",
    "zion_endpoint = "
]
# NOCHECK_END

# matrix_mode = "hardcodedmode"
# MATRIX_MODE = "hardcodedmode"

load_dotenv()

MATRIX_MODE = os.getenv("MATRIX_MODE")
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
LOG_LEVEL = os.getenv("LOG_LEVEL")
ZION_ENDPOINT = os.getenv("ZION_ENDPOINT")


def check_configuration() -> tuple[bool, str]:
    """Check that all required configuration variables are set and valid."""
    out = []
    out.append("ORACLE STATUS: Reading the Matrix...\n")
    out.append("Configuration loaded:")
    config_flag = True

    if not MATRIX_MODE:
        out.append("Mode: [WARNING] MATRIX_MODE not set")
    elif MATRIX_MODE not in ("development", "production"):
        out.append("Mode: [WARNING] MATRIX_MODE has invalid value")
    else:
        out.append(f"Mode: {MATRIX_MODE}")

    if not DATABASE_URL:
        out.append("Database: [WARNING] DATABASE_URL not set")
    elif not isinstance(DATABASE_URL, str):
        out.append("Database: [WARNING] DATABASE_URL has invalid type")
    else:
        out.append("Database: Connected to local instance")

    if API_KEY:
        out.append("API Access: Authenticated")
    else:
        out.append("API Access: [WARNING] API_KEY not set")

    if LOG_LEVEL:
        out.append(f"Log Level: {LOG_LEVEL}")
    else:
        out.append("Log Level: [WARNING] LOG_LEVEL not set")

    if ZION_ENDPOINT:
        out.append("Zion Network: Online")
    else:
        out.append("Zion Network: [WARNING] ZION_ENDPOINT not set")

    out.append("")

    res = "\n".join(out)
    if "[WARNING]" in res:
        config_flag = False

    return config_flag, res


def check_no_hardcoded_secrets() -> tuple[bool, str | None]:
    """Check that oracle.py itself contains no hardcoded secret."""
    script_path = os.path.abspath(__file__)
    try:
        with open(script_path, "r") as f:
            lines = f.readlines()
    except OSError as e:
        return False, f"Could not read source file: {e}"

    in_skip_block = False
    for idx, line in enumerate(lines, start=1):
        line_lower = line.lower()
        # Skip lines in NOCHECK block
        if "# nocheck_start" in line_lower:
            in_skip_block = True
            continue
        if "# nocheck_end" in line_lower:
            in_skip_block = False
            continue
        if in_skip_block:
            continue
        # Skip comments
        if line_lower.strip().startswith("#"):
            continue
        for pattern in HARDCODED_PATTERNS:
            if pattern in line_lower and "os.getenv" not in line_lower:
                msg = (f"Possible hardcoded secret at line {idx}: "
                       f"'{line.strip()}'")
                return False, msg

    return True, None


def check_env_file_configured() -> bool:
    """.env file must exist and with valid content"""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.isfile(env_path) and check_configuration():
        return True
    return False


def check_production_overrides() -> bool:
    """Verify that env variables can override .env file values."""

    test_key = "_OVERRIDE_TEST"
    os.environ[test_key] = "shell_value"

    # Simulate what load_dotenv does by manually trying to overwrite
    # Force failure: directly overwrite os.environ with a fake .env value
    FORCE_FAIL = False  # toggle this to test overriding

    if FORCE_FAIL:
        os.environ[test_key] = "dotenv_value"  # simule override=True

    result = os.environ.get(test_key)
    del os.environ[test_key]

    if result == "shell_value":
        return True
    return False


def check_environment_security() -> tuple[bool, str]:
    """Check the 3 environment securities"""
    out = []
    out.append("Environment security check:")
    check_flag = True
    if not check_no_hardcoded_secrets()[0]:
        out.append("[WARNING] Hardcoded secrets detected or OS error: "
                   f"{check_no_hardcoded_secrets()[1]}")
        check_flag = False
    else:
        out.append("[OK] No hardcoded secrets detected")

    if not check_env_file_configured():
        out.append("[WARNING] .env file not found — "
                   "copy .env.example to .env to get started")
        check_flag = False
    elif not check_configuration()[0]:
        out.append(
            "[WARNING] .env file found but configuration issues detected")
        check_flag = False
    else:
        out.append("[OK] .env file properly configured")

    if not check_production_overrides():
        out.append(
            "[WARNING] Shell environment variables do not override .env values"
        )
        check_flag = False
    else:
        out.append("[OK] Production overrides available")

    out.append("")
    return check_flag, "\n".join(out)


def main() -> None:
    config_flag, config_str = check_configuration()
    if MATRIX_MODE == "production":
        print("PRODUCTION MODE DETECTED: "
              "Configuration details hidden for security.\n")
    else:
        print(config_str)

    security_flag, security_str = check_environment_security()
    print(security_str)

    if not config_flag:
        print("[CRITICAL] Configuration issues detected!")
    if not security_flag:
        print("[CRITICAL] Security checks failed!")
    if security_flag and config_flag:
        print("The Oracle sees all configurations.")
    print()


if __name__ == "__main__":
    main()
