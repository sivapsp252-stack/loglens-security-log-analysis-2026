from bruteforce import detect_brute_force

logs = [
    {"ip": "192.168.1.50", "status": 401},
    {"ip": "192.168.1.50", "status": 401},
    {"ip": "192.168.1.50", "status": 401},
    {"ip": "192.168.1.10", "status": 200},
]

result = detect_brute_force(logs)

print(result)