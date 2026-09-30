from analyzer import analyze_log_file
from analysis import create_summary

file_path = "../logs/sample.log"

results = analyze_log_file(file_path)

summary = create_summary(results)

print("Total Requests:", summary["total_requests"])
print("Total Attacks:", summary["total_attacks"])
print("Attack Types:", summary["attack_types"])
print("Top Attackers:", summary["top_attackers"])
from analysis import attacks_per_hour

print("Attacks Per Hour:", attacks_per_hour(results))