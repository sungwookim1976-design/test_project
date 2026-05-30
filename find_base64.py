from pathlib import Path
import re

path = Path('index.html')
text = path.read_text('utf-8')
lines = text.splitlines()
pattern = re.compile(r'src="data:image/jpeg;base64,')
count = 0
for i, line in enumerate(lines, 1):
    if pattern.search(line):
        count += 1
        print(i, line.strip()[:200])
print('TOTAL', count)
