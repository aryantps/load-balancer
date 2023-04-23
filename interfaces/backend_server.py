class IBackendServer:
    """
    defines interface for backend server object.
    """
    def increment_request_count(self) -> None:
        """
        increments number of requests made to server.
        """
        pass
    
    def increment_success_count(self) -> None:
        """
        increments number of successful responses received from server.
        """
        pass
    
    def increment_error_count(self) -> None:
        """
        increments number of error responses received from server.
        """
        pass
    
    def add_latency(self, latency: float) -> None:
        """
        adds given latency to total latency for server.
        """
        pass
    
    def set_capacity(self, capacity: float) -> None:
        """
        sets maximum capacity for server.
        """
        pass
    
    def get_latency(self) -> float:
        """
        returns average latency for server
        """
        pass
    
    def get_capacity(self) -> float:
        """
        returns maximum capacity for server
        """
        pass

    def stop_health_check(self) -> None:
        """
        stops health check for server
        """
        pass
    
    def get_stats(self) -> dict:
        """
        returns statistics for server
        """
        pass

    def start_health_check(self) -> None:
        """
        starts health check for server
        """
        pass
