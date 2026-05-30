from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

mapping = {
    'Urive ALLBAMY QF100': 'qhd/allbamy_QF100.jpg',
    'Urive Albatross Q9000': 'qhd/2ch_albaq9000.jpg',
    'Urive Albatross TQ7000': 'qhd/2ch_albatq7000.jpg',
    'Urive Albatross Q7000': 'qhd/2ch_q7000.jpg',
    'Urive Q2': 'qhd/2ch_q2.jpg',
    'Urive Albatross Platinum T': 'qhd/2ch_albapt.jpg',
    'Urive Albatross5/Platinum': 'qhd/2ch_alba5.jpg',
    'Urive Albatross Q': 'qhd/2ch_albaq.jpg',
    'Urive ALLBAMY': 'full_hd/allbamy.jpg',
    'Urive Albatross Quad 7000': 'full_hd/quad7000.jpg',
    'Urive U9': 'full_hd/2ch_u9.jpg',
    'Urive Albatross NEXT': 'full_hd/2ch_next.jpg',
    'Urive S8': 'full_hd/2ch_s8.jpg',
    'Urive S700': 'full_hd/2ch_s700.jpg',
    'Urive S7': 'full_hd/2ch_s7.jpg',
    'Urive G700': 'full_hd/2ch_g700.jpg',
    'Urive Albatross Quad 5000': 'full_hd/2ch_quad5000.jpg',
    'Urive Albatross S7000': 'full_hd/2ch_s7000.jpg',
    'Urive Albatross S3000': 'full_hd/2ch_s3000.jpg',
    'Urive G600': 'full_hd/2ch_g600.jpg',
    'Urive G500': 'full_hd/2ch_g500.jpg',
    'Urive S500': 'full_hd/2ch_s500.jpg',
    'Urive S2': 'full_hd/2ch_s2.jpg',
    'Urive Albatross Quad 500': 'full_hd/2ch_quad500.jpg',
    'Urive Albatross TIO 450': 'full_hd/2ch_tio450.jpg',
    'Urive HIT2': 'hd/2ch_hit2.jpg',
    'Urive A5': 'hd/2ch_a5.jpg',
    'Urive HIT': 'hd/2ch_hit.jpg',
    'Urive Albatross A3': 'hd/2ch_a3.jpg',
    'Urive Albatross A2': 'hd/2ch_a2.jpg',
    'Urive Zest': 'hd/2ch_zest.jpg',
    'Urive Albatross+A': 'hd/2ch_alba_plus_a.jpg',
    'Urive Retro': 'hd/2ch_retro.jpg',
    'Urive Albatross+': 'hd/2ch_alba_plus.jpg',
    'Urive Albatross mini': 'hd/2ch_alba_mini.jpg',
    'Urive Albatross': 'hd/2ch_alba.jpg',
    'Urive Green HD': 'hd/2ch_greenhd.jpg',
    'Urive Single+': 'hd/1ch_singleplus.jpg',
    'Urive Ace': 'hd/1ch_ace.jpg',
    'Urive N200': 'navi/navi_n200.jpg',
    'Urive N400': 'navi/navi_n400.jpg',
    'Urive N100': 'navi/navi_n100.jpg',
    'Urive N8': 'navi/navi_n8.jpg',
}

lines = text.splitlines(True)
changed = 0

for i, line in enumerate(lines):
    if '<div class="product-card-name">' in line:
        m = re.search(r'<div class="product-card-name">(.*?)</div>', line)
        if not m:
            continue
        name = m.group(1)
        if name not in mapping:
            continue

        j = i - 1
        while j >= 0 and '<img class="product-card-img"' not in lines[j]:
            j -= 1
        if j < 0:
            continue

        k = j
        while k < i:
            if 'src="data:image/jpeg;base64,' in lines[k]:
                lines[k] = re.sub(r'src="[^"]*"', f'src="{mapping[name]}"', lines[k])
                changed += 1
                break
            k += 1
# Replace remaining A/S center base64 images inside the same item block.
as_mapping = {
    '블랙박스': 'imgs/as_blackbox.jpg',
    '네비게이션': 'imgs/as_navigation.jpg',
}
text = ''.join(lines)
for title, replacement in as_mapping.items():
    pattern = re.compile(
        rf'(<div class="item">.*?<h3>{re.escape(title)}</h3>.*?)(<img\s+src=")data:image/jpeg;base64,[^"]*("[^>]*>)',
        re.S,
    )
    def repl(match):
        prefix = match.group(1)
        img_start = match.group(2)
        img_end = match.group(3).replace('>', f' alt="{title} 서비스">', 1)
        return prefix + img_start + replacement + img_end
    text, n = pattern.subn(repl, text)
    changed += n
path.write_text(text, encoding='utf-8')
print(f'updated={changed}')
