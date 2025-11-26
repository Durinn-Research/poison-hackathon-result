import json
import requests
import time

INPUT_FILE = "poisoned_snippets.json"
OUTPUT_FILE = "microsoft_promptshields_poison_detection.json"

API_URL = "https://promptshield-api.azurewebsites.net/prompt_shield/evaluate"

headers = {
    "Content-Type": "application/json"
}

def evaluate_snippet(snippet_id, snippet):
    payload = {
        "user_prompt": snippet  # EXACTLY like your curl command
    }

    resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)

    try:
        data = resp.json()
    except Exception:
        data = {"error": "Invalid JSON response", "raw": resp.text}

    return {
        "id": snippet_id,
        "input_snippet": snippet,
        "payload_sent": payload,
        "response": data,
        "status_code": resp.status_code
    }

def main():
    with open(INPUT_FILE, "r") as f:
        snippets = json.load(f)

    results = []

    for entry in snippets:
        print(f"Evaluating {entry['id']}...")
        result = evaluate_snippet(entry["id"], entry["snippet"])
        results.append(result)
        time.sleep(0.3)  # tiny throttle

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved results → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
