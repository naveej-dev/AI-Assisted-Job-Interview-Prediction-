import ollama
import markdown
import bleach

ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + [
    "h2", "h3", "p", "ul", "ol", "li", "strong", "em"
]


def render_feedback(feedback_text):
    html = markdown.markdown(feedback_text)
    clean_html = bleach.clean(html, tags=ALLOWED_TAGS, strip=True)
    return clean_html

def generate_feedback(final_score, label, traits):
    prompt = f"""
    You are an AI interview performance coach.

    Generate feedback in **clear Markdown format** using the structure below.
    Do NOT use HTML. Keep the tone professional, constructive, and encouraging.

    ## Overall Assessment
    - Interpret the Final Average Score and Overall Label.
    - Briefly explain what this means for the candidate’s confidence and communication.

    ## Trait Averages
    Explain each trait in 1–2 short lines:
    - **Openness**: {traits.get('openness_level')}
    - **Conscientiousness**: {traits.get('conscientiousness_level')}
    - **Extraversion**: {traits.get('extraversion_level')}
    - **Agreeableness**: {traits.get('agreeableness_level')}
    - **Neuroticism**: {traits.get('neuroticism_level')}

    ## Improvement Tips
    Provide 2–3 actionable, practical tips to improve interview performance.

    ## Closing Note
    End with a short, motivating and positive closing sentence.

    ### Metrics Reference
    Final Average Score: {final_score}
    Overall Label: {label}
    """


    try:
        response = ollama.chat(
            model="gemma:2b",  # ✅ Lightweight model for CPU-only systems
            messages=[{"role": "user", "content": prompt}]
        )
        # return response["message"]["content"]
        raw_feedback = response["message"]["content"]
        styled_feedback = render_feedback(raw_feedback)
        return styled_feedback
    except Exception as e:
        return f"⚠️ LLM feedback error: {e}"
