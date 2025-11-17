def build_home_prompt(section, job_role, keywords, project_info):
prompt = (
f"Write SEO-optimized portfolio website text for the '{section}' section "
f"for someone applying as a {job_role}. Use the following keywords: {keywords}. "
f"Include these project details if relevant: {project_info}. The tone should be professional and engaging."
)
return prompt
