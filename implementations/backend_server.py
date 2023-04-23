import time
import logging
import requests
import threading
from typing import Optional
from constants.app_constants import HEALTH_CHECK_PERIOD, SERVER_CAPACITY, UNHEALTHY_RECHECK_INTERVAL
from interfaces.backend_server import IBackendServer


class BackendServer(IBackendServer):
    def __init__(self, url: str, health_check_url: Optional[str], capacity: float = SERVER_CAPACITY,health_check_period: float = HEALTH_CHECK_PERIOD) -> None:
        self.url = url
        self.capacity = capacity #maximum number of concurrent requests that server can handle at given time.
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        self.total_latency = 0

        self.stop_health_check_flag = False
        self.health_check_url = health_check_url
        self.health_check_period = health_check_period
        self.is_healthy = True

        #ensures that only one thread can modify is_healthy attribute at time, preventing race conditions and other synchronization issues.
        self.lock = threading.Lock()

        if self.health_check_url is not None:
            self.start_health_check()

    def increment_request_count(self) -> None:
        self.request_count += 1

    def increment_success_count(self) -> None:
        self.success_count += 1

    def increment_error_count(self) -> None:
        self.error_count += 1

    def add_latency(self, latency: float) -> None:
        self.total_latency += latency

    def get_capacity(self) -> int:
        return self.capacity
    
    def get_latency(self) -> float:
        return self.total_latency / self.success_count if self.success_count > 0 else 0
    
    def set_capacity(self, capacity: int) -> None:
        self.capacity = capacity

    def stop_health_check(self) -> None:
        self.stop_health_check_flag = True

    def get_stats(self) -> dict:
        return {
            "server_url" : self.url,
            "server_capacity" : self.capacity,
            "request_count": self.request_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "avg_latency": self.get_latency(),
        }
    
    def start_health_check(self) -> None:
        """
        Starts new thread to execute health check function
        """
        thread = threading.Thread(target=self._health_check, daemon=True)
        thread.start()


    # Private methods from here

    def _health_check(self) -> None:
        """
        Checks health of server by sending GET request to health check URL at regular intervals
        """
        last_health_check_time = time.time()
        
        while not self.stop_health_check_flag:
            self._check_server_health()
            last_health_check_time = self._wait_for_health_check_period(last_health_check_time)
            
    def _check_server_health(self) -> None:
        """
        Checks health of server by making GET request to health check URL.

        If server responds with status code of 200, it is considered healthy and the
        _set_server_healthy() method is called. Otherwise, _set_server_unhealthy() method
        is called, followed by _try_to_recover_server_health() method.
        """
        try:
            response = requests.get(self.health_check_url)
            if response.status_code == 200:
                self._set_server_healthy()
            else:
                self._set_server_unhealthy()
                self._try_to_recover_server_health()
        except requests.exceptions.RequestException as e:
            self._set_server_unhealthy()

    def _set_server_healthy(self) -> None:
        """
        Sets is_healthy attribute to True and logs message indicating that server
        is healthy.
        """
        self.is_healthy = True
        logging.info(f"Server {self.url} is healthy. Current thread: {threading.current_thread().name}")
        
    def _set_server_unhealthy(self) -> None:
        """
        Sets is_healthy attribute to False and logs message indicating that server
        is now unhealthy.
        """
        self.is_healthy = False
        logging.debug(f"Server {self.url} is now unhealthy. Current thread: {threading.current_thread().name}")
        
    def _try_to_recover_server_health(self) -> None:
        """
        Attempts to recover health of server by checking its health periodically.

        If server is still unhealthy after certain number of checks, it is assumed to be
        permanently down and no further recovery attempts are made.
        """
        last_health_check_time = time.time()
        if (time.time() - last_health_check_time) > UNHEALTHY_RECHECK_INTERVAL:
            logging.info(f"Checking health of unhealthy server {self.url}")
            try:
                response = requests.get(self.health_check_url)
                if response.status_code == 200:
                    self._set_server_healthy()
                    logging.info(f"Server {self.url} is healthy again. Current thread: {threading.current_thread().name}")
                else:
                    logging.debug(f"Server {self.url} is still unhealthy. Current thread: {threading.current_thread().name}")
            except requests.exceptions.RequestException as e:
                logging.debug(f"Unable to check health of server {self.url} due to error: {e}. Current thread: {threading.current_thread().name}")
        
    def _wait_for_health_check_period(self, last_health_check_time) -> float:
        """
        Sleeps for period of time equal to difference between current time and last health check time
        plus configured health check period. 
        If time since last health check is greater than or equal
        to health check period, function immediately returns current time.
        """
        time_since_last_health_check = time.time() - last_health_check_time
        time_to_sleep = max(0, self.health_check_period - time_since_last_health_check)
        time.sleep(time_to_sleep)
        return time.time()