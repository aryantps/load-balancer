import unittest
from typing import List
from implementations.backend_server import BackendServer
from implementations.lb_algorithms.round_robin_algorithm import RoundRobinAlgorithm

class TestRoundRobinAlgorithm(unittest.TestCase):
    def setUp(self):
        self.algorithm = RoundRobinAlgorithm()

    def test_empty_server_list(self):
        servers = []
        next_server = self.algorithm.get_next_server(servers)
        self.assertIsNone(next_server)

    def test_single_server(self):
        servers = [BackendServer("http://localhost:8000", health_check_url=None)]
        next_server = self.algorithm.get_next_server(servers)
        self.assertEqual(next_server.url, "http://localhost:8000")

    def test_multiple_servers(self):
        servers = [
            BackendServer("http://localhost:8000", health_check_url=None),
            BackendServer("http://localhost:8001", health_check_url=None),
            BackendServer("http://localhost:8002", health_check_url=None)
        ]
        next_server = self.algorithm.get_next_server(servers)
        self.assertEqual(next_server.url, "http://localhost:8000")

        next_server = self.algorithm.get_next_server(servers)
        self.assertEqual(next_server.url, "http://localhost:8001")

        next_server = self.algorithm.get_next_server(servers)
        self.assertEqual(next_server.url, "http://localhost:8002")

        next_server = self.algorithm.get_next_server(servers)
        self.assertEqual(next_server.url, "http://localhost:8000")

if __name__ == '__main__':
    unittest.main()