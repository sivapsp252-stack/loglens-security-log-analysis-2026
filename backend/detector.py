import re


SIGNATURES = {
    "sql_injection": {
        "patterns": [
            r"'\s*OR\s+1\s*=\s*1",
            r"UNION\s+SELECT"
        ],
        "severity": "high"
    },

    "xss": {
        "patterns": [
            r"<script>",
            r"javascript:"
        ],
        "severity": "high"
    },

    "directory_traversal": {
        "patterns": [
            r"\.\./\.\./",
            r"/etc/passwd"
        ],
        "severity": "high"
    }
}


def detect_attack(text):
    detected = []

    for attack_type, rule in SIGNATURES.items():

        for pattern in rule["patterns"]:

            if re.search(pattern, text, re.IGNORECASE):
                detected.append({
                    "type": attack_type,
                    "severity": rule["severity"]
                })
                break

    return detected