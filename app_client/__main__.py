import argparse as ap
from client import main as client_main

def main(args):
    print(f"IP Address: {args.ipadd}")
    client_main(args)


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("ipadd", type=str, help="Ip address of the server")
    parser.add_argument("--debug","-d", action="store_true", help="Enable debug mode", default=False)
    args = parser.parse_args()
    main(args)
