from typing import List
from interfaces.backend_server import IBackendServer


class ILoadBalancerAlgorithm:
    """
    defines interface for load balancing algorithm.
    """
    def get_next_server(self, servers: List[IBackendServer]) -> IBackendServer:
        """
        given list of backend servers, returns next server to use according to algo.
        """
        pass