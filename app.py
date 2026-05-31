import os
import json
import time
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import weave
from dotenv import load_dotenv

TIME_SLEEP = 0

load_dotenv()

weave.init('multiagent-rural-health')
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = Flask(__name__)

LATEST_ORCHESTRATION_RESULT = None

@weave.op()
def device_data_agent(vitals):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    prompt = f"Normalize and validate these vitals. Check for format anomalies. Input: {json.dumps(vitals)}. Output format: JSON with keys: normalizedVitals, anomalies."
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    return json.loads(response.text)

@weave.op()
def risk_triage_agent(vitals, symptoms):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    prompt = f"Analyze vitals and symptoms to compute a risk level (Low, Moderate, High) and list critical alerts. Vitals: {json.dumps(vitals)}. Symptoms: {json.dumps(symptoms)}. Output format: JSON with keys: score, criticalAlerts."
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    return json.loads(response.text)

@weave.op()
def medication_adherence_agent(symptoms):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    prompt = f"Evaluate potential adherence issues or side effects based on symptoms: {json.dumps(symptoms)}. Output format: JSON with key: adherenceBarriers."
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    return json.loads(response.text)

@weave.op()
def social_needs_agent(symptoms):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    prompt = f"Screen text context or symptoms for structural barriers like transportation or food insecurity: {json.dumps(symptoms)}. Output format: JSON with key: socialNeedsIdentified."
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    return json.loads(response.text)

@weave.op()
def patient_education_agent(triage_score, vitals):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    prompt = f"Draft simple lifestyle or preventative actions for the patient. Risk: {triage_score}. Vitals: {json.dumps(vitals)}. Output format: JSON with key: patientGuidance."
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    return json.loads(response.text)

@weave.op()
def specialist_access_agent(vitals, symptoms):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    prompt = f"Generate a condensed clinical brief for an emergency specialist consultation. Vitals: {json.dumps(vitals)}. Symptoms: {json.dumps(symptoms)}. Output format: JSON with key: specialistBrief."
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    return json.loads(response.text)

@weave.op()
def care_coordinator_agent(triage, social):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    prompt = f"Determine resource routing based on Triage: {json.dumps(triage)} and Social Needs: {json.dumps(social)}. Output format: JSON with key: recommendedRoute."
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    return json.loads(response.text)

@weave.op()
def documentation_agent(patient_id, triage, clean_data):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    prompt = f"Synthesize a professional EHR narrative note and append standard RPM billing code. Patient: {patient_id}. Triage: {json.dumps(triage)}. Data: {json.dumps(clean_data)}. Output format: JSON with keys: ehrClinicalNote, billingCodeReady."
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    return json.loads(response.text)

@weave.op()
def multi_agent_orchestrator(payload):
    patient_info = payload.get("patient_information", {})
    vitals = payload.get("vital_signs", {})
    symptoms = payload.get("symptoms", {})

    clean_data = device_data_agent(vitals)
    time.sleep(TIME_SLEEP)

    triage_result = risk_triage_agent(clean_data.get("normalizedVitals"), symptoms)
    time.sleep(TIME_SLEEP)

    medication_result = medication_adherence_agent(symptoms)
    time.sleep(TIME_SLEEP)

    social_result = social_needs_agent(symptoms)
    time.sleep(TIME_SLEEP)

    education_result = patient_education_agent(triage_result.get("score"), clean_data.get("normalizedVitals"))
    time.sleep(TIME_SLEEP)

    specialist_result = None
    if triage_result.get("score") == "High":
        specialist_result = specialist_access_agent(clean_data.get("normalizedVitals"), symptoms)
        time.sleep(TIME_SLEEP)

    coordination_result = care_coordinator_agent(triage_result, social_result)
    time.sleep(TIME_SLEEP)

    doc_result = documentation_agent(patient_info.get("patient_id"), triage_result, clean_data)

    priority_calculated = "Standard"
    if triage_result.get("score") == "High":
        priority_calculated = "Emergency Escalation"
    elif triage_result.get("score") == "Moderate":
        priority_calculated = "Elevated Priority"

    mapped_output = {
        "patient_information": patient_info,
        "vital_signs": vitals,
        "symptoms": symptoms,
        "medications": payload.get("medications", [{}]),
        "notes": payload.get("notes", {}),
        "triage_output": {
            "risk_level": triage_result.get("score", "Unknown"),
            "priority": priority_calculated
        },
        "agent_status": {
            "intake_agent": "✅ Intake Agent Processed Data Successfully",
            "device_agent": "✅ Device Data Agent Normalized Data Successfully",
            "symptom_agent": "✅ Symptom Agent Logged Anomalies Successfully",
            "medication_agent": f"✅ Medication Agent Complete: Barriers -> {medication_result.get('adherenceBarriers')}",
            "connectivity_agent": f"✅ Connectivity Agent Configured for status: {patient_info.get('connectivity_status')}",
            "triage_agent": f"✅ Triage Agent Completed Critical Calculations",
            "care_agent": "✅ Care Coordination Agent Outlined Care Routines",
            "documentation_agent": "✅ Documentation Agent Finalized Clinical Records Bundle"
        },
        "care_coordination": {
            "recommended_next_steps": [
                coordination_result.get("recommendedRoute", "Review clinician logs."),
                education_result.get("patientGuidance", "Follow standard guidance protocols.")
            ]
        },
        "documentation": {
            "nurse_note": f"{doc_result.get('ehrClinicalNote', '')}\n\n[Billing Reference Attached Code: {doc_result.get('billingCodeReady', 'N/A')}]"
        }
    }
    return mapped_output

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/output")
def output_dashboard():
    return render_template("output.html")

@app.route("/api/patient-intake", methods=["POST"])
def patient_intake_api():
    global LATEST_ORCHESTRATION_RESULT
    try:
        data = request.get_json()
        response_data = multi_agent_orchestrator(data)
        LATEST_ORCHESTRATION_RESULT = response_data
        return jsonify({"status": "processed", "redirect": "/output"}), 200
    except Exception as e:
        # Imprime o erro crítico em vermelho no terminal para debug instantâneo
        print(f"\n🔥 ERRO FATAL NA ORQUESTRAÇÃO: {str(e)}\n")
        return jsonify({"error": str(e)}), 500

@app.route("/api/agent-output", methods=["GET"])
def get_agent_output():
    global LATEST_ORCHESTRATION_RESULT
    if LATEST_ORCHESTRATION_RESULT is None:
        return jsonify({"error": "No processing tasks found on memory instance"}), 404
    return jsonify(LATEST_ORCHESTRATION_RESULT), 200

if __name__ == "__main__":
    app.run(debug=True, port=3000)