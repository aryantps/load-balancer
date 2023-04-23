from typing import List
from interfaces.backend_server import IBackendServer
from interfaces.load_balancer_algorithm import ILoadBalancerAlgorithm


class RoundRobinAlgorithm(ILoadBalancerAlgorithm):
    """
    This class implements round-robin load balancing algorithm.
    
    algorithm selects next available backend server in rotating order.
    
    :param self: instance of RoundRobinAlgorithm class.
    """
    
    def __init__(self):
        """
        Initialize RoundRobinAlgorithm instance.
        
        :param self: instance of RoundRobinAlgorithm class.
        """
        self.current_server_index = 0
        
    def get_next_server(self, servers: List[IBackendServer]) -> IBackendServer:
        """
        Select next available backend server in rotating order.
        
        :param self: instance of RoundRobinAlgorithm class.
        :param servers: list of available backend servers.
        :return: instance of IBackendServer interface.
        """
        if not servers:
            return None
        
        # Get server at current index
        server = servers[self.current_server_index % len(servers)]

        #Increment current server index and wrap around to 0 if it goes past end of list
        # % returns remainder of division of self.current_server_index + 1 by length of servers list. 
        # This ensures that self.current_server_index value is always within range of valid indices for servers list, 
        # which enables algorithm to cycle through available servers in round-robin fashion.
        self.current_server_index = (self.current_server_index + 1) % len(servers)
        return server
