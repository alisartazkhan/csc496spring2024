from common.shared_main import shared_main

from borda import scheme
from copeland import scheme


def main() -> None:
    shared_main("copeland", scheme)


if __name__ == "__main__":
    main()
# python3 a2-N/main.py --elections tests/elections.json