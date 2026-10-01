from app.utils import get_app_info


def main():
    info = get_app_info()

    print(f"{info['name']} v{info['version']}")
    print(f"Status: {info['status']}")


if __name__ == "__main__":
    main()