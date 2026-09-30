from collections import Counter


def detect_brute_force(logs, threshold=3):
    failed_logins = Counter()

    for log in logs:
        if log["status"] == 401:
            failed_logins[log["ip"]] += 1

    attackers = []

    for ip, count in failed_logins.items():
        if count >= threshold:
            attackers.append({
                "ip": ip,
                "failed_attempts": count,
                "type": "brute_force",
                "severity": "high"
            })

    return attackers