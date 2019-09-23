from argparse import ArgumentParser
import json
import socket
import yaml
import logging
from protocol import validate_request, make_400, make_404, make_500, make_200
from resolvers import find_server_action

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


try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    logging.info(f'Server started with {host}:{port}')

    action_mapping = find_server_action()
    while True:

        client, (client_host, client_port) = sock.accept()
        logging.info(f'Client {client_host}:{client_port} was connected')

        bytes_request = client.recv(bufferSize)
        request = json.loads(bytes_request)
        if validate_request(request):
            action = request.get('action')
            controller = action_mapping.get(action)
            if controller:
                try:
                    response = controller(request)
                    logging.debug(f'Request: {bytes_request.decode()}')
                except Exception as err:
                    response = make_500(request)
                    logging.critical(err)
            else:
                response = make_404(request)
                logging.error(f'Action with name {action} not found')
        else:
            response = make_400(request, 'Request is not valid')
            logging.error(f'Wrong request: {request}')

        string_response = json.dumps(response)
        client.send(string_response.encode())
        client.close()
except KeyboardInterrupt:
    logging.info('Server shutdown')
