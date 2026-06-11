from scanners.api_scanner import APIScanner


class APIAgent:

    def __init__(self):

        self.scanner = APIScanner()

    def execute(self, api_url):

        return self.scanner.scan(
            api_url
        )