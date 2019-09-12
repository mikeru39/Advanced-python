import json
from argparse import ArgumentParser
import socket
import yaml

if __name__ == '__main__':
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

    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    while True:
        client, (client_host, client_port) = sock.accept()
        print(f'Client {client_host}:{client_port} was connected')

        bytes_request = client.recv(bufferSize)
        response = json.loads(bytes_request)
        print(response['data'])
        print(f'Request: {response["data"]}')
        client.send(bytes_request)
        client.close()