import json, pathlib, re, sys

def fix_json_text(text: str) -> str:
    # Insert missing commas between objects in the 'questions' array.
    # This looks for a closing brace followed by optional whitespace/newlines and an opening brace,
    # not preceded by a comma.
    # We assume objects are at same indentation level (4 spaces).
    pattern = re.compile(r'\}\s*\n\s*\{')
    return pattern.sub('},\n    {', text)

def clean_file(path: pathlib.Path):
    raw = path.read_text(encoding='utf-8')
    raw_fixed = fix_json_text(raw)
    try:
        data = json.loads(raw_fixed)
    except json.JSONDecodeError as e:
        print(f"Failed to parse {path}: {e}")
        return False
    questions = data.get('questions', [])
    cleaned = [q for q in questions if q.get('question') != q.get('answer')]
    # Reassign ordering if needed (optional: add an explicit index field)
    for idx, q in enumerate(cleaned, start=1):
        q['questionNumber'] = idx
    data['questions'] = cleaned
    data['totalQuestions'] = len(cleaned)
    # Write back with pretty indentation, preserving UTF-8.
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Cleaned {path}: {len(questions)} -> {len(cleaned)} questions")
    return True

def main():
    root = pathlib.Path('.')
    for json_path in root.rglob('*.json'):
        # Skip non-exam files if needed (e.g., package.json). Here we process all JSON files.
        clean_file(json_path)

if __name__ == '__main__':
    main()

