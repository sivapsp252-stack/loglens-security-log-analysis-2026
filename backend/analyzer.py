from parser import parse_log_line
from detector import detect_attack
from bruteforce import detect_brute_force
from geoip import get_location


def analyze_log_file(file_path):
    results = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parsed = parse_log_line(line)

            if parsed:
                attacks = detect_attack(line)
                parsed["attacks"] = attacks

                # GeoIP lookup
                location = get_location(parsed["ip"])
                parsed.update(location)

                results.append(parsed)

    # Brute-force detection
    brute_force_attacks = detect_brute_force(results)

    for attack in brute_force_attacks:
        for result in results:
            if (
                result["ip"] == attack["ip"]
                and result["status"] == 401
            ):
                brute_force_attack = {
                    "type": "brute_force",
                    "severity": attack["severity"]
                }

                # Avoid duplicate brute-force tags
                already_detected = any(
                    existing_attack.get("type") == "brute_force"
                    for existing_attack in result["attacks"]
                    if isinstance(existing_attack, dict)
                )

                if not already_detected:
                    result["attacks"].append(brute_force_attack)

    return results