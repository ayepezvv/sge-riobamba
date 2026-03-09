import re
path = "/home/ayepez/.openclaw/workspace/sge/backend/app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# I need to inject the headers and footers reading logic
old_extraction = """        for table in doc_docx.tables:
            for row in table.rows:
                for cell in row.cells:
                    texto_completo += cell.text + "\\n"
        
        # 1. Buscar todos los bucles y sus iteradores"""

new_extraction = """        for table in doc_docx.tables:
            for row in table.rows:
                for cell in row.cells:
                    texto_completo += cell.text + "\\n"
                    
        # Extraer texto de encabezados y pies de pagina
        for section in doc_docx.sections:
            for header_footer in [section.header, section.footer]:
                if header_footer:
                    for p in header_footer.paragraphs:
                        texto_completo += p.text + "\\n"
                    for table in header_footer.tables:
                        for row in table.rows:
                            for cell in row.cells:
                                texto_completo += cell.text + "\\n"
        
        # 1. Buscar todos los bucles y sus iteradores"""

content = content.replace(old_extraction, new_extraction)

with open(path, "w") as f:
    f.write(content)
