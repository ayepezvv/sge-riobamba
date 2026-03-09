import re
path = "src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# We need to make sure the replacement hits the right spot. I'll just write a cleaner regex.
new_modal = """             {(() => {
                const tableSchema = esquemaVariables.find((e: any) => e.nombre === activeTableVar);
                const columnsToRender = (tableSchema && (tableSchema.columnas || tableSchema.sub_atributos)) 
                  ? (tableSchema.columnas || tableSchema.sub_atributos)
                  : Object.keys(tempRowItem);

                return columnsToRender.map((colKey: string) => {
                  const lowerKey = colKey.toLowerCase();
                  
                  // REGLA A: Selectores Booleanos
                  if (lowerKey.includes('disponibilidad') || lowerKey.includes('aplica') || lowerKey.includes('estado')) {
                    return (
                      <FormControl fullWidth key={colKey} size="small" sx={{ mb: 2 }}>
                        <InputLabel>{colKey.replace(/_/g, ' ').toUpperCase()}</InputLabel>
                        <Select
                          value={tempRowItem[colKey] || 'SÍ'}
                          label={colKey.replace(/_/g, ' ').toUpperCase()}
                          onChange={(e) => handleTempRowPropChange(colKey, e.target.value)}
                        >
                          <MenuItem value="SÍ">SÍ</MenuItem>
                          <MenuItem value="NO">NO</MenuItem>
                        </Select>
                      </FormControl>
                    );
                  }
                  
                  // REGLA B: Imágenes Base64
                  if (lowerKey.includes('img_')) {
                    return (
                      <Box key={colKey} sx={{ mb: 2 }}>
                        <Button variant={tempRowItem[colKey] ? "contained" : "outlined"} color={tempRowItem[colKey] ? "success" : "primary"} component="label" fullWidth size="small">
                          {tempRowItem[colKey] ? `✅ Imagen Cargada (${colKey})` : `📸 Subir Imagen (${colKey})`}
                          <input 
                            type="file" 
                            hidden 
                            accept="image/*" 
                            onChange={(e) => handleTempRowImageUpload(colKey, e)} 
                          />
                        </Button>
                        {tempRowItem[colKey] && <img src={tempRowItem[colKey]} alt="preview" style={{maxHeight: 60, marginTop: 4, display: 'block', margin: '4px auto'}} />}
                      </Box>
                    );
                  }
                  
                  // REGLA C: Campos de texto normales
                  return (
                    <TextField 
                      key={colKey} 
                      label={colKey.replace(/_/g, ' ').toUpperCase()} 
                      fullWidth 
                      sx={{ mb: 2 }}
                      size="small"
                      value={tempRowItem[colKey] || ''} 
                      onChange={(e) => handleTempRowPropChange(colKey, e.target.value)} 
                    />
                  );
                });
             })()}"""

# Attempting to replace the whole block mapping tempRowItem inside DialogContent
content = re.sub(r'\{\(\(\) => \{.*?const tableSchema =.*?\);\n\s+\}\);\n\s+\}\)\(\)\}', new_modal, content, flags=re.DOTALL)
content = re.sub(r'\{Object\.keys\(tempRowItem\)\.map\(\(colKey\) => \{.*?\n\s+return \(\n\s+<TextField.*?\);\n\s+\}\)\}', new_modal, content, flags=re.DOTALL)


# 2. Fix Initial State for default 'SÍ'
new_open_modal = """  const handleOpenRowModal = (varName: string) => {
    setActiveTableVar(varName);
    
    const tableSchema = esquemaVariables.find((e: any) => e.nombre === varName);
    const currentList = Array.isArray(dinamicData[varName]) ? dinamicData[varName] : [];
    
    let template: any = {};
    const cols = tableSchema?.columnas || tableSchema?.sub_atributos;
    if (cols && cols.length > 0) {
      cols.forEach((attr: string) => { 
        const lower = attr.toLowerCase();
        if (lower.includes('disponibilidad') || lower.includes('aplica') || lower.includes('estado')) {
            template[attr] = 'SÍ'; // Default state to prevent nulls
        } else {
            template[attr] = ''; 
        }
      });
    } else if (currentList.length > 0) {
      template = { ...currentList[0] };
      for (let k in template) {
        const lower = k.toLowerCase();
        template[k] = (lower.includes('disponibilidad') || lower.includes('aplica') || lower.includes('estado')) ? 'SÍ' : '';
      }
    } else {
      template = { nombre_atributo: "" };
    }
    
    setTempRowItem(template);
    setOpenRowModal(true);
  };"""

content = re.sub(r'  const handleOpenRowModal = \(varName: string\) => \{.*?\n  \};', new_open_modal, content, flags=re.DOTALL)


# 3. Fix Frontend Blob logic to prevent crash on download naming 
new_blob_logic = """        if (response.data instanceof Blob || response.headers['content-type']?.includes('wordprocessingml') || response.headers['content-type']?.includes('octet-stream')) {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          // El backend envia el filename en Content-Disposition si esta disponible
          let fileName = `Proceso_${procesoId}_Generado.docx`;
          const disposition = response.headers['content-disposition'];
          if (disposition && disposition.indexOf('filename=') !== -1) {
              const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
              const matches = filenameRegex.exec(disposition);
              if (matches != null && matches[1]) { 
                fileName = matches[1].replace(/['"]/g, '');
              }
          }
          link.setAttribute('download', fileName);
          document.body.appendChild(link);
          link.click();
          link.parentNode?.removeChild(link);
          window.URL.revokeObjectURL(url);
          setToast({ open: true, message: 'Documento procesado exitosamente', severity: 'success' });
        }"""

# Replace the inner try block of handlesubmit blob logic (both create and regenerate)
content = re.sub(r"        if \(response\.data instanceof Blob.*?setToast\(\{ open: true, message: 'Documento (?:re)?generado exitosamente', severity: 'success' \}\);\n        \}", new_blob_logic, content, flags=re.DOTALL)


with open(path, "w") as f:
    f.write(content)
