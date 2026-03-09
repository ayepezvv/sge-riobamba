path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Looks like it's missing the closing quote
content = content.replace('texto_completo += cell.text + "\\n\n', 'texto_completo += cell.text + "\\n"\n')
content = content.replace('texto_completo += p.text + "\\n\n', 'texto_completo += p.text + "\\n"\n')

with open(path, "w") as f:
    f.write(content)
