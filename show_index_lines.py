from pathlib import Path

path = Path('index.html')
lines = path.read_text('utf-8').splitlines()
for i in range(820, 881):
    print(f'{i+1}: {lines[i][:120]}')
