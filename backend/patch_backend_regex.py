import re

path = "/home/ayepez/.openclaw/workspace/sge/backend/app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Fix the Regex Tank
old_regex = "vars_simples = re.findall(r'{{\s*(\w+)\s*}}', texto_completo)"
new_regex = r"vars_simples = re.findall(r'\{\{\s*([\w.]+)\s*\}\}', texto_completo)"

content = content.replace(old_regex, new_regex)

# Fix the processing loop to split the dot and group them properly
old_loop = """        esquema = []
        for var in variables_detectadas:
            if var.startswith("img_"):
                esquema.append({"nombre": var, "tipo": "imagen"})
            elif var in todas_las_listas or var.startswith("tbl_") or var.startswith("lista_"):
                esquema.append({"nombre": var, "tipo": "tabla_dinamica"})
            else:
                esquema.append({"nombre": var, "tipo": "texto"})
                
        return {"variables": esquema}"""

new_loop = """        esquema = []
        tablas_dict = {}
        
        for var in variables_detectadas:
            # Check if it's a dotted variable (e.g. bien.nombre)
            if '.' in var:
                prefijo, atributo = var.split('.', 1)
                
                # Guessing the list name based on prefix
                # Normally jinja: {% for bien in lista_bienes %} {{ bien.nombre }} {% endfor %}
                # We will map this attribute to any dynamic table that was discovered, or create a generic one
                lista_padre = next((l for l in todas_las_listas if l.endswith(f"s") or l.startswith("lista_")), f"lista_{prefijo}s")
                
                if lista_padre not in tablas_dict:
                    tablas_dict[lista_padre] = []
                tablas_dict[lista_padre].append(atributo)
                continue
                
            # Normal processing for non-dotted variables
            if var.startswith("img_"):
                esquema.append({"nombre": var, "tipo": "imagen"})
            elif var in todas_las_listas or var.startswith("tbl_") or var.startswith("lista_"):
                if var not in tablas_dict:
                    tablas_dict[var] = []
            else:
                esquema.append({"nombre": var, "tipo": "texto"})
                
        # Append dynamic tables with their discovered sub-attributes
        for tbl_name, attrs in tablas_dict.items():
            esquema.append({"nombre": tbl_name, "tipo": "tabla_dinamica", "sub_atributos": attrs})
                
        return {"variables": esquema}"""

content = content.replace(old_loop, new_loop)

with open(path, "w") as f:
    f.write(content)
