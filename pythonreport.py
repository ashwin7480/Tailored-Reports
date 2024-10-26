from flask import Flask, render_template, request

app = Flask(__name__)

# Conditionals for tailored report
conditionals = {
    "injury_time": {
        "Less than 3 months": "<br>Since your injury happened less than three months ago, you should still have ample time to gather evidence and seek medical treatment, which can strengthen your case. Take photos of your injury and document your medical visits and related expenses. Speak to witnesses if possible.",
        "3 - 6 months": "<br>Since your injury happened 3-6 months ago, you may still have time to gather evidence and seek medical treatment. Document your medical visits, related expenses, and actions you've taken for recovery. Make sure your actions haven’t worsened the injury, and document the pain you're experiencing and how the injury has impacted your life. Given that some time has passed, find out what the long-term (chronic) prognosis is for your condition.",
        "12 months – 3 years": "<br>Since your injury occurred 12 months to 3 years ago, you'll need to explain why you’ve waited to take action and what steps you've taken for recovery. In Queensland, you generally have three years from the injury date to lodge a Notice of Claim for Damages (NOCD)."
    },
    "employment_status": {
        "Employee": "As an employee at the time of your injury in Queensland, you'll be covered by WorkCover or another insurer. Employers must provide insurance through WorkCover or self-insurance for work injuries. You may be eligible for both statutory compensation and a common law claim, depending on your case.",
        "Contractor": "As a contractor at the time of your injury, you may need your own insurance for injuries. However, if the nature of your work resembled that of an employee, you might be entitled to WorkCover compensation from the company on whose location you were injured."
    },
    # Additional conditionals for "injury_type", "pre_existing_condition", etc.
    # ...
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user responses
        responses = {
            "injury_time": request.form["injury_time"],
            "employment_status": request.form["employment_status"],
            "injury_type": request.form["injury_type"],
            "pre_existing_condition": request.form["pre_existing_condition"],
            "training": request.form["training"],
            "location": request.form["location"],
            "insurance": request.form["insurance"],
            "age_bracket": request.form["age_bracket"]
        }

        # Build report based on user responses
        report = []
        for question, answer in responses.items():
            if answer in conditionals.get(question, {}):
                report.append(conditionals[question][answer] + "<p>")  # Add a paragraph break

        # Format the report with paragraphs
        formatted_report = "".join(report)
        return render_template("report.html", report=formatted_report)

    # Add the missing line to handle the GET request
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)