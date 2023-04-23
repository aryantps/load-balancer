import socket
import requests
from typing import Optional, Dict, Union,Tuple, Any
from interfaces.backend_server import IBackendServer

class ICommunicator:
    """
    Defines interface for communicator that handles communication with backend servers and LB app.
    """
    def send_request_to_backend_server(self, client_sock: socket.socket, backend_server: IBackendServer) -> Tuple[bool, Optional[str]]:
        """
        Sends HTTP request to backend server, 
        using provided client socket to extract request details.

        :param client_sock (socket.socket): socket object representing connection to client.
        :param backend_server: IBackendServer object representing backend server to send request to.
        :return: tuple containing flag indicating whether error occurred, and response received from backend server, or None if error occurred
        """
        pass
    
    def send_success_response(self, client_sock: socket.socket, response_str: str) -> None:
        """
        Sends HTTP response to client socket.

        :param client_sock (socket.socket): socket object representing client connection.
        :param response_str (str): HTTP response to send to client socket.

        :return: None
        """
        pass
    
    def send_error_response(self, client_sock: socket.socket, reason: str, message: str) -> None:
        """
        Sends error HTTP response to client socket.

        Parameters:
        :param client_sock (socket.socket): socket object representing client connection.
        :param reason (str): reason for error.
        :param message (str): message explaining error.

        :return : None
        """
        pass

    def make_request(self, host_url: str, incoming_req_details: Dict[str, Any]) -> Union[requests.Response, None]:
        """
        Sends HTTP request to specified backend server using provided details.

        :param host_url: base URL of backend server.
        :param incoming_req_details: dict containing details of incoming HTTP request.
            It contains following keys: method (str), data (bytes), url_path (str), and headers (Dict[str, str]).
        :return: response object returned by backend server, or None if HTTP method is unsupported.
        """
        pass
