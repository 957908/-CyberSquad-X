import ollama



class OllamaAgent:

    def analyze(
        self,
        target,
        risk_score,
        vulnerabilities

    ):

        prompt = f"""
You are a cybersecurity expert.

Target: {target}

Risk Score: {risk_score}/100

Vulnerabilities:
{vulnerabilities}

Provide output in this format:

### Security Risks
- bullet points

### Impact
- bullet points

### Recommendations
- bullet points

Keep response under 250 words.
"""
        response = ollama.chat(
            model="mistral",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]