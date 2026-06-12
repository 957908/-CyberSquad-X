from scanners.apk_scanner import APKScanner


class APKAgent:

    def __init__(self):

        self.scanner = APKScanner()

    def execute(self, apk_path):

        return self.scanner.scan(
            apk_path
        )