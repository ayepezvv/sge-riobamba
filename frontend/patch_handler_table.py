import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Make sure handleRowImageUpload is properly defined
new_handler = """  const handleRowImageUpload = (varName: string, rowIndex: number, key: string, e: any) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
            handleRowPropChange(varName, rowIndex, key, reader.result as string);
        };
        reader.readAsDataURL(file);
    }
  };"""

if "handleRowImageUpload" not in content:
    content = content.replace("const handleAddRow", new_handler + "\n\n  const handleAddRow")

with open(path, "w") as f:
    f.write(content)
