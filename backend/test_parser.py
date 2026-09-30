from parser import parse_log_line

log = '192.168.1.10 - - [19/Sep/2026:10:30:15 +0530] "GET /login HTTP/1.1" 200 1234 "Mozilla/5.0"'

result = parse_log_line(log)

print(result)