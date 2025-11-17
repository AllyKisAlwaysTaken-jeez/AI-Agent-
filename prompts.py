def build_home_prompt(section: str, job_role: str, keywords: str, project_info: str) -> str:
    prompt = (
        f"Write SEO-optimized portfolio website text for the '{section}' section "
        f"for someone applying as a {job_role}. Use these keywords: {keywords}. "
        f"Include these project details if relevant: {project_info}. "
        f"Tone: professional and engaging. Keep it concise (about 150-250 words)."
    )
    return prompt
