from typing import List
from interfaces.backend_server import IBackendServer
from interfaces.load_balancer_algorithm import ILoadBalancerAlgorithm


class WeightedResponseTimeAlgorithm(ILoadBalancerAlgorithm):
    """
    This class implements weighted response time load balancing algorithm.
    
    algorithm selects backend server with lowest weighted response time,
    where weighted response time is calculated as average latency divided
    by remaining capacity of server.
    
    :param self: instance of WeightedResponseTimeAlgorithm class.
    """
    
    def __init__(self):
        """
        Initialize WeightedResponseTimeAlgorithm instance.
        
        :param self: instance of WeightedResponseTimeAlgorithm class.
        """
        pass
        
    def get_next_server(self, servers: List[IBackendServer]) -> IBackendServer:
        """
        Select backend server with lowest weighted response time.
        
        :param self: instance of WeightedResponseTimeAlgorithm class.
        :param servers: list of available backend servers.
        :return: instance of IBackendServer interface.
        """
        if not servers:
            return None
        # Compute weighted response time for each server
        weighted_response_times = [] # each element corresponds to weighted response time of server in servers list
        for server in servers:
            capacity = server.get_capacity()
    
            # if capacity is 0, then corresponding server is considered "out of service"
            # and float('inf') value is added to weighted_response_times list. 
            if capacity == 0:
                weighted_response_times.append(float('inf'))
            else:
                weighted_response_times.append(server.get_latency() / server.get_capacity())

        try:
            # Select server with lowest weighted response time
            min_index = weighted_response_times.index(min(weighted_response_times))
            return servers[min_index]
        except ValueError:
            # If no server is found with lowest weighted response time, return None
            return None