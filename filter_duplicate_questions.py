import json, pathlib, argparse, sys

def load_json(path: pathlib.Path):
    try:
        return json.load(path.open(encoding='utf-8'))
    except json.JSONDecodeError as e:
        sys.stderr.write(f'Error parsing {path}: {e}\n')
        sys.exit(1)

def save_json(data, path: pathlib.Path):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def filter_questions(data):
    # Expect a top‑level 'questions' list
    questions = data.get('questions', [])
    # Keep only items where question text != answer text
    cleaned = [q for q in questions if q.get('question') != q.get('answer')]
    # Re‑assign sequential IDs and numbers
    for idx, q in enumerate(cleaned, start=1):
        # Update a generic sequential field (questionNumber)
        q['questionNumber'] = idx
        # Overwrite or create a simple numeric ID
        q['questionId'] = f"q{idx:04d}"
    data['questions'] = cleaned
    data['totalQuestions'] = len(cleaned)
    return data

def main():
    parser = argparse.ArgumentParser(description='Filter out duplicate question/answer entries from exam JSON files.')
    parser.add_argument('input', type=pathlib.Path, help='Path to the source JSON file')
    parser.add_argument('output', type=pathlib.Path, help='Path where the cleaned JSON will be written')
    args = parser.parse_args()

    raw = load_json(args.input)
    cleaned = filter_questions(raw)
    save_json(cleaned, args.output)
    print(f"Processed {args.input.name}: {len(raw.get('questions', []))} → {len(cleaned.get('questions', []))} questions saved to {args.output}")

if __name__ == '__main__':
    main()

