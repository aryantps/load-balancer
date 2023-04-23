import socket


class ILoadBalancer:
    """
    defines interface for a load balancer object.
    """
    def handle_request(self, client_sock: socket.socket) -> None:
        """
        handles a client request by forwarding it to appropriate backend server 
        and sending response back to client.
        """
        pass
    
    def start(self) -> None:
        """
        starts load balancer, listening for incoming requests and handling them.
        """
        pass