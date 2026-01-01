import json
from workflow import run_and_save

if __name__ == "__main__":
    user_input = input("Enter PDF/DOCX path, URL, or search query: ").strip()
    slides_count = input("Number of slides (default 5): ").strip()
    slides_count = int(slides_count) if slides_count.isdigit() else 5
    json_name = input("JSON filename (e.g., slides.json): ").strip() or "output.json"

    result = run_and_save(user_input, slides_count, json_name)
    print("\n--- JSON OUTPUT ---\n")
    print(json.dumps(result, indent=2))
