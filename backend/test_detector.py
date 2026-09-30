from detector import detect_attack

tests = [
    "/search?q=' OR 1=1",
    "/<script>alert(1)</script>",
    "/../../etc/passwd",
    "/login"
]

for test in tests:
    result = detect_attack(test)
    print(test, "=>", result)