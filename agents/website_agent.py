from scanners.web_scanner import WebScanner


class WebsiteAgent:

    def __init__(self):

        self.scanner = WebScanner()

    def execute(self, url):

        return self.scanner.scan_website(
            url
        )