import logging
from typing import List
from interfaces.backend_server import IBackendServer
from interfaces.load_balancer_algorithm import ILoadBalancerAlgorithm

class WeightedRoundRobinAlgorithm(ILoadBalancerAlgorithm):
    """
    Implements weighted round robin load balancing algorithm.

    Algorithm selects backend server using weighted round robin method,
    where weight of each server is calculated as ratio of its remaining
    capacity to maximum capacity among all servers.

    :param self: instance of WeightedRoundRobinAlgorithm class.
    """

    def __init__(self):
        """
        Initialize WeightedRoundRobinAlgorithm instance.

        :param self: instance of WeightedRoundRobinAlgorithm class.
        """
        self.index = -1 #index of last server used

    def get_next_server(self, servers: List[IBackendServer]) -> IBackendServer:
        """
        Select next backend server using weighted round robin method.

        :param self: instance of WeightedRoundRobinAlgorithm class.
        :param servers: list of available backend servers.
        :return: instance of IBackendServer interface.
        """
        if not servers:
            return None

        # weights calculated every time func is called because it depends on 
        # current status of each server's capacity which can changes between calls
        weights = []

        # total capacity of all available backend servers
        total_capacity = sum(server.get_capacity() for server in servers)
        for server in servers:

            # Calculating weight as ratio of server capacity to total capacity
            weight = server.get_capacity() / total_capacity
            weights.append(weight)
            logging.info(f"Weight for server {server.url}: {weight}")

        # selects next server to use
        # algo cycles through server list in circular fashion, selecting each server in turn
        # modulo ensures that index value wraps around to 0 when reaching end of servers ist, allowing algo to keep cycling through list indefinitely.
        self.index = (self.index + 1) % len(servers)

        # If server weight is very small, skippiing it and moving to next server
        while weights and self.index < len(servers) and weights[self.index] < 1e-6:
            self.index = (self.index + 1) % len(servers)
        return servers[self.index]