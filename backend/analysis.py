from collections import Counter


def attacks_per_hour(results):
    hourly_attacks = Counter()

    for result in results:
        if result.get("attacks"):
            hour = result["timestamp"][12:14]
            hourly_attacks[hour] += len(result["attacks"])

    return dict(sorted(hourly_attacks.items()))


def get_geo_locations(results):
    locations = []
    seen = set()

    for result in results:
        latitude = result.get("latitude")
        longitude = result.get("longitude")

        # Ignore IPs that cannot be geolocated
        if latitude is None or longitude is None:
            continue

        key = (
            result["ip"],
            latitude,
            longitude
        )

        if key in seen:
            continue

        seen.add(key)

        locations.append({
            "ip": result["ip"],
            "country": result.get("country"),
            "city": result.get("city"),
            "latitude": latitude,
            "longitude": longitude
        })

    return locations


def create_summary(results):
    total_requests = len(results)

    attack_counts = Counter()
    severity_counts = Counter()
    attacker_ips = Counter()

    for result in results:
        attacks = result.get("attacks", [])

        for attack in attacks:

            # New severity-aware format
            if isinstance(attack, dict):
                attack_type = attack.get("type", "unknown")
                severity = attack.get("severity", "unknown")
            else:
                # Backward compatibility
                attack_type = attack
                severity = "unknown"

            attack_counts[attack_type] += 1
            severity_counts[severity] += 1
            attacker_ips[result["ip"]] += 1

    total_attacks = sum(attack_counts.values())

    return {
        "total_requests": total_requests,
        "total_attacks": total_attacks,
        "attack_types": dict(attack_counts),
        "severity_counts": dict(severity_counts),
        "top_attackers": attacker_ips.most_common(10),
        "geo_locations": get_geo_locations(results)
    }