import random
import logging
import unittest
from implementations.backend_server import BackendServer
from implementations.lb_algorithms.weighted_response_time_algorithm import WeightedResponseTimeAlgorithm

logging.basicConfig(level=logging.INFO)

class TestWeightedResponseTimeAlgorithm(unittest.TestCase):
    def setUp(self):
        # Creating some backend servers with different capacities and latencies
        self.servers = []
        for i in range(random.randint(5, 10)):
            server = BackendServer(f"http://localhost:800{i+1}", health_check_url=None, capacity=random.randint(1, 100))
            server.total_latency = random.uniform(0.1, 0.9)
            server.success_count = random.randint(0, 10)
            self.servers.append(server)

        # Created instance of the WeightedResponseTimeAlgorithm
        self.algorithm = WeightedResponseTimeAlgorithm()

    def test_get_next_server(self):
        # Using the algo to select the server with the lowest weighted response time
        selected_server = self.algorithm.get_next_server(self.servers)

        weighted_response_time_list = []
        #Calculating and printing the weighted response time for the server
        for server in self.servers:
            weighted_response_time = server.get_latency() / server.get_capacity()
            logging.info(f"{server.url} - Weighted response time: {weighted_response_time}")
            weighted_response_time_list.append(weighted_response_time)


        #Finding the server with the minimum weighted response time
        min_weighted_response_time = min(weighted_response_time_list)
        min_weighted_response_time_index = weighted_response_time_list.index(min_weighted_response_time)
        expected_server = BackendServer(self.servers[min_weighted_response_time_index].url, capacity=self.servers[min_weighted_response_time_index].get_capacity(), health_check_url=None)

        # Asserting that the url attribute of the selected server is the same as that of the expected server
        self.assertEqual(selected_server.url, expected_server.url)


if __name__ == '__main__':
    unittest.main()
