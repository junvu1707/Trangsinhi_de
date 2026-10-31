import json, pathlib, sys
p = pathlib.Path(r'e:\Junvu\AI\Project\Siêu trạng\De_github\grade 2_round 2.json')
with p.open(encoding='utf-8') as f:
    data = json.load(f)
matches = [(i, q.get('question')) for i, q in enumerate(data.get('questions', []), start=1) if q.get('question') == q.get('answer')]
print('Matches:', len(matches))
for idx, txt in matches[:10]:
    print(idx, txt)

