import re

path = "src/app/(dashboard)/contratacion/procesos/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Fix invalid dates in frontend columns
content = content.replace("valueGetter: (params) => new Date(params.value).toLocaleString()", "valueGetter: (params) => params.value ? new Date(params.value).toLocaleString() : 'N/A'")

with open(path, "w") as f:
    f.write(content)
