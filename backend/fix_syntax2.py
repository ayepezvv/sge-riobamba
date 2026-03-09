path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    lines = f.readlines()

with open(path, "w") as f:
    for i, line in enumerate(lines):
        if "texto_completo += cell.text +" in line or "texto_completo += p.text +" in line:
            # We enforce exactly the correct format with a newline string literal
            indent = line[:len(line) - len(line.lstrip())]
            if "cell" in line:
                f.write(indent + 'texto_completo += cell.text + "\\n"\n')
            else:
                f.write(indent + 'texto_completo += p.text + "\\n"\n')
            
            # Skip the next line if it's the broken continuation of the string literal
            if i + 1 < len(lines) and lines[i+1].strip() == '"':
                lines[i+1] = "" 
        else:
            f.write(line)
