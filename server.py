import logging
from constants.app_constants import BACKEND_SERVERS_CONFIG
from implementations.load_balancer import LoadBalancer
from implementations.lb_algorithms.round_robin_algorithm import RoundRobinAlgorithm
from implementations.lb_algorithms.weighted_response_time_algorithm import WeightedResponseTimeAlgorithm


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    algorithm = WeightedResponseTimeAlgorithm()
    lb = LoadBalancer(
        backend_servers_config = BACKEND_SERVERS_CONFIG,
        algorithm=algorithm)
    lb.start()