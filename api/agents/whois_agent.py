import whois

class WhoisAgent:

    def lookup(self, domain):

        try:
            data = whois.whois(domain)

            return {
                "domain": str(data.domain_name),
                "registrar": str(data.registrar),
                "creation_date": str(data.creation_date),
                "expiration_date": str(data.expiration_date),
            }

        except Exception as e:
            return {
                "error": str(e)
            }