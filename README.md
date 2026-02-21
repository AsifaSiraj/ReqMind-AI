# 🚀 ReqMind AI
## Intelligent AI-Powered Requirement Analysis System  
**HEC Generative AI Hackathon – Cohort 02 | Group 26**

---

## 📌 Overview

ReqMind AI is an AI-powered Requirement Engineering Assistant designed to transform unstructured software requirements into structured, analyzable, and actionable outputs.

The system leverages Large Language Models (LLMs) to automatically:

- Extract Functional Requirements  
- Identify Non-Functional Requirements (NFRs)  
- Detect Ambiguities  
- Highlight Missing Information  
- Generate Clarification Questions  
- Produce Structured JSON Output  
- Export Detailed PDF Reports  

ReqMind AI demonstrates the practical application of Generative AI in improving requirement engineering workflows.

---

## 🌐 Live Deployment (Hugging Face Space)

The application is deployed and publicly accessible via Hugging Face Spaces:

🔗 **Live Demo:**  
https://huggingface.co/spaces/MahzaibDhillo/ReqMind_AI  

This deployment enables real-time interaction with the AI-powered requirement analysis system without local setup.

---

## 🏛 Developed Under

This project was developed as part of:

**HEC Generative AI Training – Cohort 2**  
📅 January 18 – February 27, 2026  
🖥 Six Weeks Live Online Program  

Organized and supported by:

- Higher Education Commission (HEC) Pakistan  
- National Computing Education Accreditation Council (NCEAC)  
- Pak Angels  
- iCodeGuru  
- Aspire Pakistan  
- UET Lahore Endowment Fund (ULEF US/PAK)

---

## 🎯 Problem Statement

Poorly defined requirements remain one of the primary causes of software project failure.

Common issues include:

- Ambiguous terminology  
- Incomplete specifications  
- Lack of measurable constraints  
- Time-consuming manual analysis  
- Inconsistent documentation  

Example:

> "The app should be fast and user-friendly."

This statement is vague and not technically measurable.

ReqMind AI addresses these challenges through AI-driven semantic analysis.

---

## 🧠 Core Features

✔ Functional Requirement Extraction  
✔ Non-Functional Requirement Classification  
✔ Ambiguity Detection  
✔ Missing Constraint Identification  
✔ Automated Clarification Questions  
✔ Structured JSON Output Schema  
✔ PDF Report Generation  
✔ REST-based AI Integration  

---

## ⚙️ System Architecture

### 🔹 Workflow

User Input  
→ Input Validation  
→ Prompt Engineering  
→ LLM Inference (Hugging Face)  
→ Structured JSON Parsing  
→ Categorization  
→ PDF Generation  
→ Final Report Output  

### 🔹 Components

- **Frontend:** Gradio(Python) 
- **Backend:** Python  
- **AI Hosting:** Hugging Face Inference API  
- **Model Type:** Large Language Model (Llama-based)  
- **PDF Engine:** ReportLab / FPDF  

---

## 📂 Project Structure

```
ReqMind-AI/
│
├── app.py
├── backend/
│   ├── prompt_engineering.py
│   ├── parser.py
│   ├── pdf_generator.py
│
├── diagrams/
│   ├── architecture_diagram.png
│   ├── component_diagram.png
│   ├── sequence_diagram.png
│   └── activity_diagram.png
│
├── requirements.txt
└── README.md
```

---

## 📑 AI Output Schema

```json
{
  "functional": [
    {"id": 1, "actor": "User", "action": "login"}
  ],
  "non_functional": [
    {"category": "performance", "metric": "load_time < 3s"}
  ],
  "ambiguities": [
    "'fast' requires measurable definition"
  ],
  "missing": [
    "User roles specification"
  ],
  "questions": [
    "What authentication method should be used?"
  ]
}
```

---

## 🧪 Testing Coverage

| Scenario | Description | Status |
|----------|------------|--------|
| Empty Input | Input validation handling | ✅ Completed |
| Basic Requirement | Simple extraction | ✅ Completed |
| Complex SRS | Long-form structured analysis | 🔄 In Progress |
| Multilingual Input | Urdu text parsing | 🔄 In Progress |
| Edge Case Handling | Symbols/emojis cleanup | ✅ Completed |

---

## 🚀 Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/ReqMind-AI.git
cd ReqMind-AI
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Hugging Face Token
Set your environment variable:

```bash
export HF_TOKEN=your_token_here
```

### 4️⃣ Run Application
```bash
streamlit run app.py
```

---

## 📊 Expected Impact

- Reduced requirement analysis time  
- Improved documentation clarity  
- Reduced ambiguity-driven rework  
- Enhanced project planning accuracy  
- Standardized structured outputs  
- Improved stakeholder communication  

---

## 🔮 Future Enhancements

- Requirement Traceability Matrix (RTM) Generation  
- Jira / Trello Integration  
- Version Comparison & Change Impact Analysis  
- Agile User Story Conversion  
- Risk Scoring & Requirement Quality Index  
- Multi-language Semantic Support  
- Cloud-Based SaaS Deployment  

---

## 👩‍💻 Team – Group 26

- Asifa Siraj  
- Warisha Danin Bilal  
- Iman Ayaz  
- Zobia Hassan  
- Mahzaib Iqbal  
- Mansoor Ahmed  

---

## 📜 License

This project was developed for academic and hackathon purposes under the HEC Generative AI Training Program.

---

## 🇵🇰 Vision

ReqMind AI aligns with Pakistan’s national mission to advance Generative AI capabilities and empower engineers with intelligent automation tools that enhance productivity, precision, and innovation.

---
