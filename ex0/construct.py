import sys
import os
import site


def main() -> None:
    # Check if we're outside the Matrix or not
    matrix_status = (
        "You're still in the real world..."
        if sys.prefix == sys.base_prefix
        else "Welcome to the Matrix"
    )
    print(f"\nMATRIX STATUS: {matrix_status}\n")
    print(f"Current Python: {sys.executable}")

    # get virtual environment name and path
    virtual_env_path = os.getenv("VIRTUAL_ENV") or "None"
    virtual_env_name = (
        "None detected"
        if sys.prefix == sys.base_prefix
        else os.path.basename(virtual_env_path)
    )
    print(f"Virtual Environment: {virtual_env_name}")

    # You entered the Matrix
    if sys.prefix != sys.base_prefix:
        print(f"Environment path: {virtual_env_path}")
        print("\nSUCCESS: You're in an isolated environment!")
        print(
            "Safe to install packages without affecting the global system.\n"
        )
        print("Package installation path: ")
        try:
            print(site.getsitepackages()[0], "\n")
        except (AttributeError, IndexError) as e:
            print(f"Error detecting package installation path: {e}\n")

    # You are still in the real world
    else:
        print("\nWARNING: You're in the global environment!")
        print("The machines can see everything you install.\n")
        print(
            "To enter the construct, run:\n"
            "  python3 -m venv matrix_env\n"
            "  source matrix_env/bin/activate # On Unix\n"
            "  matrix_env\n"
            "  Scripts\n"
            "  activate # On Windows\n"
        )
        print("Then run this program again\n")


if __name__ == "__main__":
    main()
