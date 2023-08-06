import signal
import sys

from tuixdate.common import process_arguments


def signal_handler(sig, frame):
    print("\n 👋 Bye!")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    process_arguments()


if __name__ == "__main__":
    main()
