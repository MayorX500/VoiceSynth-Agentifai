import argparse as ap
from client import main as client_main

def main(args):
    print(f"IP Address: {args.proxy_add}")
    client_main(args)


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("proxy_add", nargs='?', type=str, help="IP address of the server", default=None)
    parser.add_argument("user_token", nargs='?', type=str, help="User token", default="1")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode", default=False)
    args = parser.parse_args()
    main(args)
