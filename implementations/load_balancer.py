import socket
import logging
import threading
from typing import List,Dict

from utils.utility import Utils
from interfaces.load_balancer import ILoadBalancer
from implementations.backend_server import BackendServer
from constants.app_constants import LOAD_BALANCER_ADDRESS
from interfaces.load_balancer_algorithm import ILoadBalancerAlgorithm
from implementations.backend_communicator import BackendServerCommunicator

class LoadBalancer(ILoadBalancer):
    
    def __init__(self, backend_servers_config: List[Dict[str, str]], algorithm: ILoadBalancerAlgorithm):
        self.backend_servers = [BackendServer(url=server.get("url"),health_check_url=server.get("health_check_url")) for server in backend_servers_config]
        self.algorithm = algorithm
        self.backend_server_communicator = BackendServerCommunicator()
        self.server_sock = None

    def start(self) -> None:
        # created new socket object with IPv4 addressing and TCP protocol
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            self.server_sock = server_sock
            server_sock.bind(LOAD_BALANCER_ADDRESS)

            # listening for incoming connections on bound address and port
            server_sock.listen()

            logging.info(f"Load balancer listening on {LOAD_BALANCER_ADDRESS[0]}:{LOAD_BALANCER_ADDRESS[1]}")
            try:

                # continuously accept incoming connections and spawn new threads to handle them
                while True:

                    # accept incoming connection and return new socket object representing connection, along with address of client
                    client_sock, client_addr = server_sock.accept()

                    logging.info(f"Received request on LB from client {client_addr[0]}:{client_addr[1]} using thread {threading.current_thread().name}")

                    # spawn new thread to handle request
                    threading.Thread(target=self.handle_request, args=(client_sock,)).start()
            except KeyboardInterrupt:
                # if Ctrl+C is received then stop 
                self.stop()
    
    def stop(self) -> None:
        if self.server_sock:
            logging.info(f"......Shutting down load balancer listening on {LOAD_BALANCER_ADDRESS[0]}:{LOAD_BALANCER_ADDRESS[1]}")
            self.server_sock.close()

            # stopping health check of each backend server
            for server in self.backend_servers:
                server.stop_health_check()


    def handle_request(self, client_sock: socket.socket) -> None:
        # Removed unhealthy servers from list of available servers
        healthy_servers = [server for server in self.backend_servers if server.is_healthy]

        # getting next server according to lb algo to handle request 
        backend_server = self.algorithm.get_next_server(healthy_servers)

        # no healthy backend server is available
        if backend_server is None:
            logging.info("No healthy backend servers available")
            self.backend_server_communicator.send_error_response(client_sock, "Service Unavailable", "No healthy backend servers available")
            return

        error_occurred, response = self.backend_server_communicator.send_request_to_backend_server(client_sock, backend_server)

        if error_occurred:
            self.backend_server_communicator.send_error_response(client_sock,"Service Unavailable", "Failed to connect to backend server")
            backend_server.increment_error_count()
            backend_server.increment_request_count()
            logging.info(backend_server.get_stats())
            return

        if response.status_code >= 400:
            error_message = f"Request failed with status code {response.status_code}"
            self.backend_server_communicator.send_error_response(client_sock, "Bad Request", error_message)
            backend_server.increment_error_count()
        else:
            response_str = Utils.generate_response_string(response)
            self.backend_server_communicator.send_success_response(client_sock, response_str)
            backend_server.increment_success_count()

        backend_server.increment_request_count()
        logging.info(backend_server.get_stats())
