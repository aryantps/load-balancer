import random
import logging
import unittest
from implementations.backend_server import BackendServer
from implementations.lb_algorithms.weighted_round_robin_algorithm import WeightedRoundRobinAlgorithm

logging.basicConfig(level=logging.INFO)

class TestWeightedRoundRobinAlgorithm(unittest.TestCase):
    def setUp(self):
        # Creating some backend servers with different capacities
        self.servers = []
        for i in range(random.randint(5, 10)):
            server = BackendServer(f"http://localhost:800{i+1}", health_check_url=None, capacity=random.randint(1, 100))
            self.servers.append(server)

        self.algorithm = WeightedRoundRobinAlgorithm()

    def test_get_next_server(self):

        expected_index = 0
        weights = {}
        total_capacity = sum(server.get_capacity() for server in self.servers)

        # Calculating expected weight for each server based on its capacity
        for server in self.servers:
            weight = server.get_capacity() / total_capacity
            weights[server.url] = weight
            logging.info(f"Weight for server {server.url}: {weight}")

        # Calling get_next_server for each server and verify expected index
        for server in self.servers:
            selected_server = self.algorithm.get_next_server(self.servers)
            logging.info(f"Expected server {self.servers[expected_index].url} | Selected server - {selected_server.url}")
            self.assertEqual(selected_server.url, self.servers[expected_index].url)

            # Getting number of servers with non-zero weight
            num_nonzero_weights = len(self.servers) - list(weights.values()).count(0)

            # Incrementing expected_index by 1, and wrapping around to 0 if it exceeds num_nonzero_weights
            expected_index = (expected_index + 1) % num_nonzero_weights

        # Verifying that weights for each server match expected weights
        for server in self.servers:
            self.assertAlmostEqual(weights[server.url], server.get_capacity() / total_capacity, delta=0.001)
