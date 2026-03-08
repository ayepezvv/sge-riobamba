import re

path = "src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Fix the JSX {{ campos }} bug
content = content.replace("Esta plantilla no tiene variables ({{ campos }}) configuradas en su archivo DOCX.", "Esta plantilla no tiene variables {'{{ campos }}'} configuradas en su archivo DOCX.")

# Fix invalid dates in frontend columns
content = content.replace("valueGetter: (params) => new Date(params.value).toLocaleString()", "valueGetter: (params) => params.value ? new Date(params.value).toLocaleString() : 'N/A'")

with open(path, "w") as f:
    f.write(content)
