from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import anthropic
import os
import fitz

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    job_description = request.form.get("job_description")
    resume_file = request.files.get("resume")
    if not resume_file:
        return jsonify({"error": "No resume uploaded"}), 400
    resume = ""
    with fitz.open(stream=resume_file.read(), filetype="pdf") as doc:
        for page in doc:
            resume += page.get_text()

    cover_letter_override = request.form.get("force_cover_letter")
    if cover_letter_override:
        override_text = "Always generate a cover letter regardless of fit score."   
    else:
        override_text = "Use your judgment on whether a cover letter is needed."


    prompt = f"""
    You are a senior hiring manager and recruiter with 15+ years of experience. You evaluate candidates ruthlessly but fairly. You do not sugarcoat, you do not try to be nice, and you do not give generic advice. You think in terms of hiring decisions, risk, and signal strength.
    Evaluate the candidate below against the job description as if you are deciding whether to interview them.
    Be direct. If something is weak, say it clearly. If something is strong, explain why it actually matters.
    Return your answer in this exact structure:
    1. Interview Likelihood (0–100%)
    * Give a realistic probability this candidate gets a first-round interview.
    * Justify it like a hiring manager defending a decision internally.
    * Call out any deal-breakers explicitly.
    2. Resume / Experience Strength
    * Strengths: Only include strengths that materially improve hiring chances.
    * Gaps: Be specific and critical. Focus on what is missing relative to THIS role, not in general.
    * Mismatches: Where the experience does not align with what the job actually needs.
    3. Cover Letter
    * ONLY generate this section if the candidate is borderline (roughly 40–70% likelihood) AND a strong, targeted cover letter could meaningfully improve their chances.
    * If not needed, write: "Not needed."
    * If generated, it must directly compensate for the candidate’s biggest weaknesses and align tightly with the role.
    Rules:
    * No generic advice.
    * No fluff.
    * No motivational tone.
    * Assume the reader is smart and wants truth, not encouragement.
    * If the candidate has no realistic chance, say so plainly and explain why in one sentence.
    *OVERRIDE: {override_text}
    JOB DESCRIPTION: {job_description}
    RESUME: {resume}
    """
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return jsonify({"result": response.content[0].text})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)

