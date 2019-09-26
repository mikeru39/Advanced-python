from argparse import ArgumentParser

import socket
import yaml
import logging
import select
from resolvers import find_server_action
from handlers import handle_tcp_request

config = {
    'host': 'localhost',
    'port': 8000,
    'bufferSize': 1024
}

parser = ArgumentParser()

parser.add_argument('-c', '--config', type=str, required=False,
                    help='Sets config path')
parser.add_argument('-ht', '--host', type=str, required=False,
                    help='Sets server host')
parser.add_argument('-p', '--port', type=str, required=False,
                    help='Sets server port')

args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        file_config = yaml.safe_load(file)
        config.update(file_config or {})

host = args.host if args.config else config.get('host')
port = args.port if args.config else config.get('port')
bufferSize = config.get('bufferSize')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=(
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    )
)
requests = []
connections = []
try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.setblocking()
    sock.listen(5)

    logging.info(f'Server started with {host}:{port}')

    action_mapping = find_server_action()
    while True:
        try:
            client, (client_host, client_port) = sock.accept()
            logging.info(f'Client {client_host}:{client_port} was connected')
            connections.append(client)
        except:
            pass

        rlist, wlist, xlist = select.select(connections, connections, connections, 0)

        for read_client in rlist:
            bytes_request = read_client.recv(bufferSize)
            requests.append(bytes_request)
        if requests:
            bytes_request = requests.pop()
            bytes_response = handle_tcp_request(bytes_request, action_mapping)

            for write_client in wlist:
                write_client.send(bytes_response)

except KeyboardInterrupt:
    logging.info('Server shutdown')
