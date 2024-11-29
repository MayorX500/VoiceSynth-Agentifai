import argparse as ap
from normalizer import serve as normalizer_main

def main(args):
    normalizer_main(args)

if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("rules", type=str, help="Path to the configuration file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode", default=False)
    args = parser.parse_args()
    main(args)