from app.gemini_client import ask_gemini
from app.config import GEMINI_API_KEY
from app.utils import get_app_info


def main():
    info = get_app_info()

    print(f"{info['name']} v{info['version']}")
    print(f"Status: {info['status']}")

    if GEMINI_API_KEY:
        print("Gemini API key loaded successfully.")

        response = ask_gemini("Say hello to SmartDoc AI in one sentence.")
        print(f"Gemini: {response}")
    else:
        print("Gemini API key not found.")


if __name__ == "__main__":
    main()