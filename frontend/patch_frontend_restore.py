import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# I need to ensure the renderContexto function exists and is used
# I also need to ensure the columns logic uses 'columnas' properly inside the Dialog for rows

# 1. Dialog rendering fix for the Row Modal (Adding back the 'disponibilidad' check based on schema 'columnas')
old_dialog_content = """        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 1 }}>
             {(() => {
                const tableSchema = esquemaVariables.find((e: any) => e.nombre === activeTableVar);
                const columnsToRender = (tableSchema && tableSchema.sub_atributos && tableSchema.sub_atributos.length > 0) 
                  ? tableSchema.sub_atributos 
                  : Object.keys(tempRowItem);

                return columnsToRender.map((colKey: string) => {"""

new_dialog_content = """        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 1 }}>
             {(() => {
                const tableSchema = esquemaVariables.find((e: any) => e.nombre === activeTableVar);
                // El backend ahora devuelve 'columnas'
                const columnsToRender = (tableSchema && tableSchema.columnas && tableSchema.columnas.length > 0) 
                  ? tableSchema.columnas 
                  : Object.keys(tempRowItem);

                return columnsToRender.map((colKey: string) => {"""

if old_dialog_content in content:
    content = content.replace(old_dialog_content, new_dialog_content)
else:
    # Use regex if exact match fails
    content = re.sub(r'const columnsToRender = \(tableSchema && tableSchema\.sub_atributos && tableSchema\.sub_atributos\.length > 0\)\s*\?\s*tableSchema\.sub_atributos', 'const columnsToRender = (tableSchema && tableSchema.columnas && tableSchema.columnas.length > 0)\n                  ? tableSchema.columnas', content)

# 2. Add Context renderer
context_renderer = """  const renderContexto = (contextoStr: string, variableNombre: string) => {
    if (!contextoStr) return null;
    const parts = contextoStr.split(`[ ${variableNombre} ]`);
    if (parts.length === 1) return <Typography variant="caption" color="textSecondary">{contextoStr}</Typography>;
    return (
      <Typography variant="caption" color="textSecondary" component="span" sx={{ display: 'block', mt: 0.5, lineHeight: 1.2 }}>
        {parts[0]}
        <Typography component="span" fontWeight="bold" color="primary.main" sx={{ bgcolor: 'primary.light', px: 0.5, borderRadius: 1 }}>
          {variableNombre}
        </Typography>
        {parts[1]}
      </Typography>
    );
  };"""

if "const renderContexto" not in content:
    content = content.replace("  const [toast, setToast] = useState", context_renderer + "\n\n  const [toast, setToast] = useState")

# 3. Use renderContexto in the main form builder
old_main_render = """{v.tipo === 'texto' && (
                        <TextField 
                          label={v.nombre.replace(/_/g, ' ').toUpperCase()} 
                          value={dinamicData[v.nombre] || ''} 
                          onChange={(e) => handleDynamicChange(v.nombre, e.target.value)} 
                          fullWidth 
                          multiline={!v.nombre.includes('fecha') && !v.nombre.includes('codigo')}
                          rows={v.nombre.includes('descripcion') || v.nombre.includes('objeto') ? 3 : 1}
                        />
                      )}"""

new_main_render = """{v.tipo === 'texto' && (
                        <TextField 
                          label={v.nombre.replace(/_/g, ' ').toUpperCase()} 
                          value={dinamicData[v.nombre] || ''} 
                          onChange={(e) => handleDynamicChange(v.nombre, e.target.value)} 
                          fullWidth 
                          helperText={renderContexto(v.contexto, v.nombre)}
                          multiline={!v.nombre.includes('fecha') && !v.nombre.includes('codigo')}
                          rows={v.nombre.includes('descripcion') || v.nombre.includes('objeto') ? 3 : 1}
                        />
                      )}"""

content = content.replace(old_main_render, new_main_render)

with open(path, "w") as f:
    f.write(content)
