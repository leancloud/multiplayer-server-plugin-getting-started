"""
Process starts here
"""
import atexit
import os
import traceback
import argparse
import colorama
# to support editing of the current input line. do not delete it even you think we don't use it
import readline

from tools.base import router
from tools.base import lobby_shortcuts
from tools.base import client
from tools.base import config
from tools.base import input_parser


def start_process():
    """Driver function to run this script"""
    parser = argparse.ArgumentParser(
        description="Command line client to comunicate with LeanCloud game service")
    parser.add_argument('--peerid', default='2a',
                        dest="peerid", help="Client peerId, default is \"2a\"")
    parser.add_argument('--env', default='q0', dest="config_env",
                        help="Which env in config.ini to use, default is \"qcloud\"")
    parser.add_argument('--protocol', default='json.1', dest="protocol",
                        help="Serialization protocol, default is \"json.1\"")
    parser.add_argument('--addr', default=None, dest="server_addr",
                        help="Server address connecting to directly, default is \"None\"")
    parser.add_argument('--roomid', default=None,
                        dest="roomid",
                        help="Room id to join or create, default is \"None\"")
    parser.add_argument('--create', action="store_true", default=False,
                        dest="is_create_room",
                        help="Create room when joined failed, default is \"False\"")
    parser.add_argument('--insecure', action="store_true", default=False,
                        dest="is_insecure",
                        help="Connect to game lobby and game server with insecure websocket, default is \"False\"")

    args = parser.parse_args()

    config.init_config(args.config_env)

    resp = None
    room_id = args.roomid
    server_addr = args.server_addr

    if args.is_create_room:
        resp = lobby_shortcuts.create_room(
            args.peerid, room_id=room_id, insecure=args.is_insecure)
    else:
        if room_id is not None:
            resp = lobby_shortcuts.join_room(
                args.peerid, room_id, insecure=args.is_insecure)
            if resp.get('error') and resp.get('error').get('reasonCode'):
                resp = None

        if server_addr is None and resp is None:
            server_addr = router.get_lobby_route(
                insecure=args.is_insecure).get('server')

    if server_addr is None:
        if args.is_insecure:
            server_addr = resp.get('addr')
        else:
            server_addr = resp.get('secure_addr')

    print(colorama.Fore.YELLOW + "Connecting to %s" % server_addr)

    clt = client.client_builder() \
        .with_addr(server_addr) \
        .with_appid(config.APP_ID) \
        .with_protocol(args.protocol) \
        .with_peerid(args.peerid) \
        .build()
    clt.connect()

    while True:
        try:
            raw_str = input()
            if len(raw_str) != 0:
                cmd_msg_args = input_parser.parse_input_cmd_args(raw_str)
                clt.send_msg(cmd_msg_args)
            else:
                print(raw_str)
        except KeyboardInterrupt:
            break
        except Exception:
            print(colorama.Fore.RED + "Got exception: %s" %
                  traceback.print_exc())

    clt.close()
    client.close_all_opened_clients()
    print(colorama.Fore.GREEN + "Client closed")


# copied from https://docs.python.org/3/library/readline.html
def prepare_history_file():
    histfile = os.path.join(
        os.path.expanduser("~"), ".game_command_line_testing_tool_history")
    try:
        readline.read_history_file(histfile)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, histfile)


if __name__ == "__main__":
    prepare_history_file()
    colorama.init(autoreset=True)
    start_process()
