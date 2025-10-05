import pdfplumber
import re
from autogen import AssistantAgent, UserProxyAgent

llm_config = {
    "config_list": [
        {
            "model": "mistral",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
        }
    ]
}

def extract_resume_sections(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    full_text = re.sub(r'\s+', ' ', full_text).strip()

    headers = [
        "EDUCATION",
        "WORK EXPERIENCE",
        "PROJECTS",
        "TECHNICAL SKILLS",
        "PUBLICATIONS",
        "CERTIFICATIONS",
        "ACHIEVEMENTS",
    ]

    pattern = r"(?=(" + "|".join(headers) + r"))"
    parts = re.split(pattern, full_text)

    sections = {}
    current_header = "GENERAL"
    sections[current_header] = ""

    for part in parts:
        upper = part.strip().upper()
        if upper in headers:
            current_header = upper
            sections[current_header] = ""
        else:
            sections[current_header] += part.strip() + " "

    for header, content in sections.items():
        print(f"\n{'='*40}\n{header}\n{'='*40}")
        print(content.strip())

    return sections


sections = extract_resume_sections("Siddhesh_Resume.pdf")

assistant = AssistantAgent(name="assistant", llm_config=llm_config)
user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config={"work_dir": "coding", "use_docker": False}
)

user_proxy.initiate_chat(
    assistant,
    message=f"Summarize the WORK EXPERIENCE section: {sections.get('WORK EXPERIENCE', '')}"
)
