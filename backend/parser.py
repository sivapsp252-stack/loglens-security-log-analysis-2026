import re

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) '
    r'\S+ \S+ '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>.*?) (?P<protocol>HTTP/\S+)" '
    r'(?P<status>\d+) '
    r'\S+ '
    r'"(?P<user_agent>[^"]*)"'
)


def parse_log_line(line):
    match = LOG_PATTERN.match(line)

    if not match:
        return None

    data = match.groupdict()
    data["status"] = int(data["status"])

    return data