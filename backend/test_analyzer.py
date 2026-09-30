from analyzer import analyze_log_file

file_path = "../logs/sample.log"

results = analyze_log_file(file_path)

for result in results:
    print(result)