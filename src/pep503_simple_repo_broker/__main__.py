"""PEP503 Simple Repo Broker."""

from .application import Application


def main() -> None:
    """Main function."""
    application = Application()
    application.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        pass
