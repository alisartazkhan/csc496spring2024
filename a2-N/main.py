from common.shared_main import shared_main

from borda import scheme
from copeland import scheme
from irv import scheme
from black import scheme
from river import scheme

def main() -> None:
    # shared_main("copeland", scheme)
    shared_main("irv", scheme)
    # shared_main("black", scheme)
    # shared_main("river", scheme)




if __name__ == "__main__":
    main()
# python3 a2-N/main.py --elections tests/elections.json
# python3 a2-N/main.py --elections tests/elections.json --check