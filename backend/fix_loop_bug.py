import re

path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

old_block = """        for match in matches:
            var_raw = match.group(1)
            
            # Extraer contexto (40 chars)"""

new_block = """        for match in matches:
            var_raw = match.group(1)
            
            # Omitir variables internas de jinja2 (ej: loop.index)
            if 'loop' in var_raw.lower():
                continue
                
            # Extraer contexto (40 chars)"""

content = content.replace(old_block, new_block)

with open(path, "w") as f:
    f.write(content)
