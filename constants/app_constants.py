LOAD_BALANCER_ADDRESS = ("localhost", 8080)
REQUEST_TIMEOUT = 5
SERVER_CAPACITY = 5

BACKEND_SERVERS_CONFIG = [
                            {
                                "url" : "http://localhost:8003",
                                "health_check_url" : "http://localhost:8003/health"
                            },
                            {
                                "url" : "http://localhost:8002",
                                "health_check_url" : "http://localhost:8002/health"
                            }
                        ]

HEALTH_CHECK_PERIOD = 10
UNHEALTHY_RECHECK_INTERVAL = 15 # interval (in seconds) for checking unhealthy servers