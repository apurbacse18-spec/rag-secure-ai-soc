from typing import List, Dict
import re


def clean_text(text: str) -> str:
    text = re.sub(r"#+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_sentences(text: str):
    sentences = re.split(r"\.\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 25]


def build_topic_answer(topic: Dict) -> str:
    if not topic:
        return "No relevant banking topic found."

    title = topic.get("title", "Banking Support")
    short_answer = topic.get("short_answer", "No answer available.")
    detailed_answer = topic.get("detailed_answer", "")
    steps = topic.get("steps", [])
    escalation_conditions = topic.get("escalation_condition", [])
    escalation_target = topic.get("escalation_target", "")
    related_topics = topic.get("related_topics", [])
    risk_level = topic.get("risk_level", "").lower()

    sections = []

    sections.append(f"🏦 {title}")
    sections.append(f"**Answer:** {short_answer}")

    if detailed_answer:
        sections.append(f"**Details:** {detailed_answer}")

    if steps:
        step_lines = ["**What to do:**"]
        for idx, step in enumerate(steps, start=1):
            step_lines.append(f"{idx}. {step}")
        sections.append("\n".join(step_lines))

    if escalation_conditions:
        esc_lines = ["**Escalate if:**"]
        for condition in escalation_conditions:
            esc_lines.append(f"- {condition}")
        sections.append("\n".join(esc_lines))

    if escalation_target:
        sections.append(f"**Support team:** {escalation_target}")

    if related_topics:
        sections.append(f"**Related topics:** {', '.join(related_topics)}")

    if risk_level in {"high", "critical"}:
        sections.append("🚨 **This issue may require urgent attention.**")

    return "\n\n".join(sections)


def build_answer(query: str, matches: List[Dict]) -> str:
    if not matches:
        return "No relevant information found."

    findings = []
    steps = []
    sources = set()

    for match in matches[:3]:
        content = clean_text(match.get("content", ""))
        sources.add(match.get("source", ""))

        sentences = extract_sentences(content)

        for sentence in sentences:
            s_lower = sentence.lower()

            if any(k in s_lower for k in ["failed", "attempt", "unusual", "login", "attack", "suspicious"]):
                findings.append(sentence)
            elif any(k in s_lower for k in ["check", "review", "identify", "correlate", "verify", "investigate"]):
                steps.append(sentence)

    findings = list(dict.fromkeys(findings))[:3]
    steps = list(dict.fromkeys(steps))[:4]

    if not findings and not steps:
        summary = extract_sentences(clean_text(matches[0].get("content", "")))[:3]
        answer = ["📄 Retrieved Guidance"]

        if summary:
            answer.append("")
            answer.append("**Summary:**")
            for item in summary:
                answer.append(f"- {item}")

        if sources:
            answer.append("")
            answer.append(f"**Sources:** {', '.join(sorted(sources))}")

        return "\n".join(answer)

    answer = ["📄 Retrieved Guidance"]

    if findings:
        answer.append("")
        answer.append("**Key findings:**")
        for item in findings:
            answer.append(f"- {item}")

    if steps:
        answer.append("")
        answer.append("**Suggested steps:**")
        for item in steps:
            answer.append(f"- {item}")

    if sources:
        answer.append("")
        answer.append(f"**Sources:** {', '.join(sorted(sources))}")

    return "\n".join(answer)