import os
import json
import requests
import time

API_KEY = "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"
API_URL = "https://api.openai.com/v1/chat/completions"
MODEL_NAME = "gpt-4o-mini"  # Use "gpt-4o" or "gpt-3.5-turbo"

def read_prompts(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

def fetch_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    body = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=body, timeout=30)
        response.raise_for_status()
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            return data.get("error", {}).get("message", "Unknown error")
    except Exception as e:
        return f"Error: {str(e)}"

def save_results(data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    prompts = read_prompts("text.txt")
    results = {}
    for prompt in prompts:
        reply = fetch_response(prompt)
        results[prompt] = reply
        time.sleep(0.2)  # Polite delay
    save_results(results, "responses.json")

if __name__ == "__main__":
    main()
