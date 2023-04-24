import socket
from typing import Optional
import time
import socket
import logging
import requests
from typing import Dict, Union,Tuple, Any

from constants.app_constants import REQUEST_TIMEOUT
from interfaces.backend_server import IBackendServer
from interfaces.communicator import ICommunicator


class BackendServerCommunicator(ICommunicator):
    
    def send_request_to_backend_server(self, client_sock: socket.socket, backend_server: IBackendServer) -> Tuple[bool, Optional[str]]:
        incoming_req_details = self._extract_incoming_req_details(client_sock)
        logging.debug(f"Data received from client: data - {incoming_req_details}")
        start_time = time.monotonic()
        try:
            response = self.make_request(backend_server.url, incoming_req_details)
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Failed to connect to backend server: {e}")
            return True, None
        end_time = time.monotonic()
        backend_server.add_latency(end_time - start_time)
        return False, response
    
    
    def send_success_response(self, client_sock: socket.socket, response_str: str) -> None:
        client_sock.sendall(response_str.encode())
        # Check if socket is still connected before shutting down and closing
        if client_sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE) == 0:
            return
        client_sock.shutdown(socket.SHUT_RDWR)
        client_sock.close()

    def send_error_response(self, client_sock: socket.socket, reason: str, message: str) -> None:
        """
        Sends  error HTTP response to client socket.

        Parameters:
        :param client_sock (socket.socket): socket object representing client connection.
        :param reason (str): reason for error.
        :param message (str): message explaining error.

        :return : None
        """
        response_str = f"HTTP/1.1 400 {reason}\r\n\r\n{message}"
        client_sock.sendall(response_str.encode())
        # Check if socket is still connected before shutting down and closing
        if client_sock.fileno() != -1:
            client_sock.shutdown(socket.SHUT_RDWR)
            client_sock.close()

    def make_request(self, host_url: str, incoming_req_details: Dict[str, Any]) -> Union[requests.Response, None]:
        method = incoming_req_details['method']
        if method in ["GET", "POST", "PUT", "DELETE"]:
            data = incoming_req_details['request_data']
            headers = incoming_req_details['headers']
            url_path = incoming_req_details['path']
            url = host_url + url_path
            return requests.request(method, url, data=data, timeout=REQUEST_TIMEOUT, headers=headers)
        else:
            return None


    def _extract_incoming_req_details(self, client_sock: socket.socket) -> Dict[str, Any]:
        """
        Extract details of incoming HTTP request from client socket.

        :param client_sock: socket object representing client connection.
        :type client_sock: socket.socket
        :return: tuple containing raw request data, HTTP method, protocol, URL path, request headers, and request data of incoming request.
        :return: dictionary containing raw request data, HTTP method, protocol, URL path, request headers, and request data of incoming request.
        :rtype: dict[str, Any]
        """
        # Check if socket is still connected before shutting down and closing
        data = client_sock.recv(1024)
        request_lines = data.split(b"\r\n")
        request_line = request_lines[0].decode("utf-8")
        method, path, protocol = request_line.split()
        headers = {}
        for line in request_lines[1:]:
            if not line:
                break
            key, value = line.split(b': ', 1)
            headers[key.decode()] = value.decode()
        headers_end = request_lines.index(b'')
        request_data = b'\r\n'.join(request_lines[headers_end+1:])
        return {
            'raw_request_data': data,
            'method': method,
            'protocol': protocol,
            'path' : path,
            'headers' : headers,
            'request_data' : request_data
        }
        

    

