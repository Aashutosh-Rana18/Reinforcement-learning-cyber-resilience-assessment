import json, csv
def load_vulnerability_data(path: str):
    with open(path, "r") as f: return json.load(f)
def save_results(results: list, path: str):
    with open(path, "w") as f: json.dump(results, f, indent=2)