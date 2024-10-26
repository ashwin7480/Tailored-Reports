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
    "injury_type": {
        "A physical injury": "Since you've suffered a physical rather than psychological injury, this may lead to less time off work. It's important to remember, though, that sometimes the physical pain, social isolation, ongoing stress, financial worries, and reduced opportunities can lead to psychological conditions emerging later. Seek support with this if you sense that you're struggling.",
        "A psychological injury": "You mentioned suffering a psychological injury. Workers can suffer psychological injuries such as anxiety, depression, and PTSD. These often require more recovery time. Compensation depends on whether the workplace was a significant contributor to the psychological injury.",
        "Both": "You said you'd suffered both a physical and psychological injury. Workers suffering from both physical and psychological injuries, such as anxiety or PTSD, may need longer recovery times. Compensation depends on the workplace being a significant contributor."
    },
    "pre_existing_condition": {
        "Yes": "You shared that you have a pre-existing condition relating to your injury. You may not be able to claim compensation if a pre-existing condition caused or significantly contributed to your injury. Your employer should have asked for pre-existing injury information, and you must not have provided false or misleading information.",
        "No": "You shared that you don't have a pre-existing condition relating to your injury. As you don't have a pre-existing condition, the organisation in question won't be able to avoid responsibility for your injury or illness by claiming that you do."
    },
    "training": {
        "No training": "You said that your workplace didn't offer any safety training. Workplaces are required to provide adequate safety training and ongoing instruction. You may be entitled to compensation if your injury resulted from inadequate training.",
        "Some training": "You said that your workplace offered some safety training. Workplaces must provide ongoing safety training. You may still be entitled to compensation if the training was insufficient. Ensure you document the level of training and how well you followed it.",
        "Extensive training": "You said that your workplace offered extensive safety training. Workplaces providing extensive safety training may argue that you failed to follow the guidelines, contributing to the injury. Ensure you're clear on what was offered and how you followed it."
    },
    "location": {
        "North Brisbane": "Since you live in the north of Brisbane, here are some local GPs and physiotherapists that have high Google Review scores and may be able to assist with your diagnosis and recovery: GPs: MyLocal Doc - Chermside, Petrie Medical Centre - Petrie. Physiotherapists: The Healthy Peach - Grange, Refine Physiotherapy and Pilates - Bowen Hills.",
        "South Brisbane": "Since you live in the south of Brisbane, here are some local GPs and physiotherapists that have high Google Review scores and may be able to assist with your diagnosis and recovery: GPs: Holland Park Medical Centre, Coorparoo Clinic. Physiotherapists: Restore Function - Greenslopes, Sunnybank Central - Sunnybank.",
        "West Brisbane": "Since you live in the west of Brisbane, here are some local GPs and physiotherapists that have high Google Review scores and may be able to assist with your diagnosis and recovery: GPs: Indooroopilly General Practice, Springfield Doctors. Physiotherapists: Hybrid Physio - Milton, Exercise Healthcare - Alderley.",
        "East Brisbane": "Since you live in the east of Brisbane, here are some local GPs and physiotherapists that have high Google Review scores and may be able to assist with your diagnosis and recovery: GPs: Bennetts Road Family Practice - Norman Park, Carina Medical Centre - Carina. Physiotherapists: Wynnum-Manly Physiotherapy, Peak Sports and Spine - Hawthorne.",
        "Moreton Bay": "Since you live in the Moreton Bay region, here are some local GPs and physiotherapists that have high Google Review scores and may be able to assist with your diagnosis and recovery: GPs: Redcliffe Family Parade Medical Practice, Medicross Medical. Physiotherapists: Moreton Bay All Body Care - Narangba, Redcliffe Physio - Redcliffe."
    },
    "insurance": {
        "Not sure": "You said that you're not sure if you currently have insurance. Many superannuation funds offer injury cover. Check with your provider to confirm if you qualify for total and permanent disability insurance.",
        "Yes": "You shared that you have your own insurance. You can speak to your insurer to find out their position on your injury, but it's also worth approaching them through a specialist such as a lawyer to ensure they fully meet their commitments laid out in your policy.",
        "No": "You shared that you don't have insurance. Be sure to check every superannuation fund that you're currently a client of, as in many cases, super funds include insurance cover for work-related injuries. In many cases though, it needs to be case of total and permanent disability."
    },
    "age_bracket": {
        "20 - 35": "You also mentioned being aged between 20 and 35. You may recover faster at your age, but injuries could affect your long-term well-being. Career disruptions and delayed life goals are also significant factors. This report aims to give you general information to help guide you, and help you to ask the right questions. Before making any decisions about a personal injury claim, we suggest talking to an experienced lawyer who can give your more specific advice. We'd love to offer you an obligation free consultation to help you better understand your options. If that's of interest, please click on the button below to book an appointment.",
        "35 - 45": "You also mentioned being aged between 35 and 45. Injuries at this age could affect your peak earning period and long-term financial stability. Consider the costs of managing dependants during your recovery. This report aims to give you general information to help guide you, and help you to ask the right questions. Before making any decisions about a personal injury claim, we suggest talking to an experienced lawyer who can give your more specific advice. We'd love to offer you an obligation free consultation to help you better understand your options. If that's of interest, please click on the button below to book an appointment.",
        "45 - 60": "You also mentioned being aged between 45 and 60. You may experience longer recovery times and higher risks of long-term health complications. Reduced mobility or chronic pain can interfere with your lifestyle and career. This report aims to give you general information to help guide you, and help you to ask the right questions. Before making any decisions about a personal injury claim, we suggest talking to an experienced lawyer who can give your more specific advice. We'd love to offer you an obligation free consultation to help you better understand your options. If that's of interest, please click on the button below to book an appointment.",
        "60+": "You also mentioned being over the age of 60. Injuries could severely impact your ability to maintain independence. Health complications and the potential need for long-term care should be considered when seeking compensation. This report aims to give you general information to help guide you, and help you to ask the right questions. Before making any decisions about a personal injury claim, we suggest talking to an experienced lawyer who can give your more specific advice. We'd love to offer you an obligation free consultation to help you better understand your options. If that's of interest, please click on the button below to book an appointment."
    }
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
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)