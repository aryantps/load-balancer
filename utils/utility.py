class Utils:

    @staticmethod
    def generate_response_string(response):
        """
        Generate response string from the given response object.

        :param response: The response object returned by the backend server.
        :return: string representing the response
        """
        response_str = f"HTTP/1.1 {response.status_code} {response.reason}\r\n"
        response_str += "\r\n".join([f"{k}: {v}" for k, v in response.headers.items()])
        response_str += "\r\n\r\n" + response.content.decode()
        return response_str