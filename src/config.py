GROQ_MODELS = {
    "openai/gpt-oss-safeguard-20b" : "Recommended for Guardrails",
    "openai/gpt-oss-20b" : "Recommended for general chat",
    "meta-llama/llama-prompt-guard-2-22m" : "Recommended for Guardrails",
    "qwen/qwen3.8-27b" : "Recommended for Chat"
}



GUARD_MODEL_DEFAULT = "openai/gpt-oss-safeguard-20b"
CHAT_MODEL_DEFAULT = "openai/gpt-oss-20b"

HR_SYSTEM_PROMPT = """
You are a professional HR Assistant. Answer employee questions using the
retrieved HR policy excerpts below. The excerpts are the authoritative company
knowledge base for this conversation.

Retrieved HR policy excerpts:
{context}
"""

sensitive_output_patterns = {
    "password": r"(?i)\b(password|passwd|pwd)\b\s*[:=]\s*\S+",
    "api_key": r"(?i)\b(api[_-]?key)\b\s*[:=]\s*\S+",
    "secret_key": r"(?i)\b(secret[_-]?key)\b\s*[:=]\s*\S+",
    "access_token": r"(?i)\b(access[_-]?token|auth[_-]?token)\b\s*[:=]\s*\S+",
    "bearer_token": r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]+",
    "private_key": r"-----BEGIN\s+(RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "phone": r"\b(?:\+91[-.\s]?)?[6-9]\d{9}\b",
}




