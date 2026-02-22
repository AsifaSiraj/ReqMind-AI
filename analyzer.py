import os, json
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert software requirements analyst. 
Analyze the provided software requirements document and return ONLY valid JSON with this exact structure:

{
  "project_info": {
    "detected_type": "E-commerce / Hospital System / LMS / FinTech / ERP / Social Media / Other",
    "complexity": "Small / Medium / Large",
    "complexity_reason": "brief reason",
    "total_requirements_count": 0
  },
  "quality_score": {
    "overall": 0,
    "clarity": 0,
    "completeness": 0,
    "consistency": 0,
    "testability": 0,
    "breakdown": "brief explanation of score"
  },
  "functional_requirements": [
    {"id": "FR1", "description": "...", "priority": "High/Medium/Low", "category": "Core/Secondary/Optional"}
  ],
  "non_functional_requirements": [
    {"id": "NFR1", "category": "Performance/Security/Usability/Scalability/Reliability", "description": "..."}
  ],
  "constraints": [
    {"id": "CON1", "description": "..."}
  ],
  "risks": [
    {"id": "RSK1", "type": "Security/Scalability/Performance/Privacy/Compliance", "description": "...", "severity": "High/Medium/Low"}
  ],
  "ambiguities": [
    {"id": "AMB1", "text": "...", "issue": "why it is ambiguous", "suggestion": "how to fix it"}
  ],
  "missing_information": [
    {"id": "MI1", "area": "...", "description": "what is missing", "impact": "High/Medium/Low"}
  ],
  "scope_creep": [
    {"id": "SC1", "statement": "exact text from document", "reason": "why this is scope creep"}
  ],
  "clarification_questions": {
    "client": [{"id": "CQ1", "question": "..."}],
    "developer": [{"id": "DQ1", "question": "..."}],
    "tester": [{"id": "TQ1", "question": "..."}],
    "project_manager": [{"id": "PQ1", "question": "..."}]
  },
  "summary": {
    "total_fr": 0,
    "total_nfr": 0,
    "total_ambiguities": 0,
    "total_risks": 0,
    "total_scope_creep": 0,
    "overall_quality": "Good/Fair/Poor",
    "recommendation": "..."
  }
}

Return ONLY the JSON. No extra text. No markdown."""


def analyze_requirements(text: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Analyze this software requirements document:\n\n{text}"}
        ],
        temperature=0.3,
        max_tokens=6000
    )
    raw = response.choices[0].message.content
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)


COMPARE_PROMPT = """You are a software requirements analyst.
Compare the OLD and NEW requirement documents and return ONLY valid JSON:
{
  "added": [{"id": "A1", "description": "new requirement added"}],
  "removed": [{"id": "R1", "description": "requirement removed"}],
  "modified": [{"id": "M1", "old": "old text", "new": "new text"}],
  "scope_changes": ["description of scope change"],
  "quality_change": {"old_score": 0, "new_score": 0, "verdict": "Improved/Degraded/Same"},
  "summary": "overall summary of changes"
}
Return ONLY the JSON."""


def compare_documents(old_text: str, new_text: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": COMPARE_PROMPT},
            {"role": "user", "content": f"OLD DOCUMENT:\n{old_text}\n\nNEW DOCUMENT:\n{new_text}"}
        ],
        temperature=0.3,
        max_tokens=4000
    )
    raw = response.choices[0].message.content
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)