# 🏥 RuralCare AI

**Multi-Agent Remote Patient Monitoring (RPM) for Rural Healthcare**
*Built for the Multi-Agent Orchestration Hackathon with Weights & Biases at MIT (Cambridge, MA - May 31, 2026)*

RuralCare AI bridges the gap between patients in low-connectivity rural areas and urban healthcare providers. By utilizing an asynchronous, 5-layer multi-agent architecture, the system securely processes delayed patient vitals, calculates clinical risk, screens for social barriers, and drafts comprehensive EHR notes—all fully observable via Weights & Biases.

## ✨ Key Features

* **Dual-Portal Architecture:**
  * **Patient Connect Portal:** A lightweight, mobile-first interface for patients and caregivers to securely submit offline/delayed vitals and symptoms.
  * **Clinical Provider Hub:** A desktop dashboard for nurses to review pending intakes and trigger the multi-agent orchestration on demand.
* **8-Node Multi-Agent Orchestration:** Powered by Google's Gemini 2.5 Flash Lite, the system splits complex clinical reasoning into specialized, deterministic agents working in parallel.
* **Full Clinical Observability:** 100% of agent calls, prompts, latency, and reasoning are traced and logged using **Weights & Biases (Weave)**, ensuring AI safety and governance in a healthcare setting.

## 🧠 The Multi-Agent Ecosystem

Our backend orchestration acts as a virtual medical team, processing data through 5 distinct layers:

1. **Ingestion Layer:** `Device Data Agent` normalizes raw vitals and checks for hardware anomalies.
2. **Evaluation Layer:** `Risk Triage Agent` analyzes the normalized data against reported symptoms to calculate a definitive Risk Score (Low, Moderate, High).
3. **Parallel Review Network:** * `Medication Adherence Agent` flags missed doses and side effects.
   * `Social Needs Agent` screens for structural barriers (transportation, food insecurity).
   * `Patient Education Agent` drafts personalized lifestyle guidance.
4. **Synthesis & Routing:** `Care Coordinator Agent` determines the safest clinical route based on risk and social barriers, escalating to the `Specialist Access Agent` if critical.
5. **Clinical Narrative:** `Documentation Agent` compiles all agent outputs into a standardized EHR note with preliminary billing codes.

## 🛠️ Tech Stack

* **Frontend:** HTML5, Tailwind CSS, JavaScript (Vanilla)
* **Backend:** Python, Flask
* **Database:** MongoDB (Local persistence for async workflow)
* **AI / LLM:** Google Generative AI (`gemini-2.5-flash-lite`)
* **Observability & Tracing:** Weights & Biases (`weave`)
