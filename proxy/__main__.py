# __main__.py for the proxy module:
# proxy works as a bridge between the client and the server to provide a seamless experience for the user. It is responsible for handling the communication between the client and the server allowing for redundancy.

import argparse as ap
from proxy import serve as proxy_main

def main(args):
    proxy_main(args)

if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("config_file",nargs='?', type=str, help="Path to the configuration file", default="config/proxy_config.json")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode", default=False)
    args = parser.parse_args()
    main(args)
