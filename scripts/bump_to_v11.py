from pathlib import Path

files = ['index.html', 'reader.html', 'assets/js/reader.js', 'assets/js/library.js']
for fp in files:
    p = Path(fp)
    content = p.read_text(encoding='utf-8')
    new_content = content.replace('20261126-v10', '20261126-v11')
    p.write_text(new_content, encoding='utf-8')
    print(f"Updated {fp} to 20261126-v11")
