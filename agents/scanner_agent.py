from scanners.network_scanner import NetworkScanner

class ScannerAgent:

    def __init__(self):
        self.scanner = NetworkScanner()

    def execute(self, target):

        print("\n[Scanner Agent Started]\n")

        result = self.scanner.scan_target(target)

        return result