class SecurityGradeAgent:

    def calculate(self, website_result):

        score = 100

        missing = website_result.get(
            "missing_headers",
            []
        )

        score -= len(missing) * 15

        if score >= 90:
            grade = "A+"

        elif score >= 80:
            grade = "A"

        elif score >= 70:
            grade = "B"

        elif score >= 60:
            grade = "C"

        elif score >= 40:
            grade = "D"

        else:
            grade = "F"

        return {
            "grade": grade,
            "score": score,
            "missing_headers": missing
        }