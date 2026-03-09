import re
path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# I will just write a regex sub to catch the block since formatting might differ
new_hf = """        # Extraer texto de encabezados y pies de pagina en todas sus variantes
        for section in doc_docx.sections:
            elementos_hf = [
                section.header, section.first_page_header, section.even_page_header,
                section.footer, section.first_page_footer, section.even_page_footer
            ]
            for hf in elementos_hf:
                if hf:
                    for p in hf.paragraphs:
                        texto_completo += p.text + "\\n"
                    for table in hf.tables:
                        for row in table.rows:
                            for cell in row.cells:
                                texto_completo += cell.text + "\\n"
"""

content = re.sub(r'        # Extraer texto de encabezados y pies de pagina.*?texto_completo \+= cell\.text \+ "\\n"', new_hf, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
