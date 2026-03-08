import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Fix Modal Open Handler to read the sub_atributos discovered by the backend
new_open_handler = """  const handleOpenRowModal = (varName: string) => {
    setActiveTableVar(varName);
    
    // Attempt to load schema from backend sub_atributos or inherit from existing row
    const tableSchema = esquemaVariables.find((e: any) => e.nombre === varName);
    const currentList = Array.isArray(dinamicData[varName]) ? dinamicData[varName] : [];
    
    let template: any = {};
    if (tableSchema && tableSchema.sub_atributos && tableSchema.sub_atributos.length > 0) {
      tableSchema.sub_atributos.forEach((attr: string) => { template[attr] = ''; });
    } else if (currentList.length > 0) {
      template = { ...currentList[0] };
      for (let k in template) template[k] = '';
    } else {
      template = { nombre_atributo: "" }; // Fallback
    }
    
    setTempRowItem(template);
    setOpenRowModal(true);
  };"""
  
content = re.sub(r'  const handleOpenRowModal = \(varName: string\) => \{.*?\n  \};', new_open_handler, content, flags=re.DOTALL)

# Fix the Save Handler
new_save_handler = """  const handleSaveRow = () => {
    setDinamicData((prev: any) => ({
      ...prev,
      [activeTableVar]: [...(prev[activeTableVar] || []), tempRowItem]
    }));
    setTempRowItem({});
    setOpenRowModal(false);
  };"""

content = re.sub(r'  const handleSaveRow = \(\) => \{.*?\n  \};', new_save_handler, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
