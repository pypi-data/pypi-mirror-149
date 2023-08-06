from pdfme import PDF
import json
from pathlib import Path

from .utils import gen_content

def run_test(index):
    pdf = PDF()
    pdf.add_page()
    name = 'test_content{}'.format(index)
    input_file = Path(name + '.json')
    if input_file.exists():
        with input_file.open(encoding='utf8') as f:
            content = json.load(f)
    else:
        content = gen_content(20)
        with input_file.open('w', encoding='utf8') as f:
            json.dump(content, f, ensure_ascii=False)

    pdf.content(content)
    with open('test_content{}.pdf'.format(index), 'wb') as f:
        pdf.output(f)

def test_content(index=None):
    if index is not None:
        run_test(index)
    else:
        for i in range(6):
            run_test(i)
