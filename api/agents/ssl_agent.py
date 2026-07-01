import ssl
import socket
from datetime import datetime


class SSLAgent:

    def scan(self, domain):

        try:

            context = ssl.create_default_context()

            with socket.create_connection(
                (domain, 443)
            ) as sock:

                with context.wrap_socket(
                    sock,
                    server_hostname=domain
                ) as secure_sock:

                    cert = secure_sock.getpeercert()

                    expiry = datetime.strptime(
                        cert["notAfter"],
                        "%b %d %H:%M:%S %Y %Z"
                    )

                    days_left = (
                        expiry - datetime.now()
                    ).days

                    return {
                        "ssl_enabled": True,
                        "issuer": dict(
                            cert["issuer"]
                        ),
                        "expiry_date": str(expiry),
                        "days_remaining": days_left,
                        "tls_version":
                            secure_sock.version(),
                    }

        except Exception as e:

            return {
                "ssl_enabled": False,
                "error": str(e)
            }