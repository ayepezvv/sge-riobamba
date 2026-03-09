import re

path = "src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# 1. Fix Modal Render (Columns)
old_modal_content = """        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 1 }}>
             {Object.keys(tempRowItem).map((colKey) => {"""

new_modal_content = """        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 1 }}>
             {(() => {
                const tableSchema = esquemaVariables.find((e: any) => e.nombre === activeTableVar);
                const columnsToRender = (tableSchema && tableSchema.sub_atributos && tableSchema.sub_atributos.length > 0) 
                  ? tableSchema.sub_atributos 
                  : Object.keys(tempRowItem);

                return columnsToRender.map((colKey: string) => {"""

content = content.replace(old_modal_content, new_modal_content)
content = content.replace("                return (\n                  <TextField ", "                return (\n                  <TextField ")

# Also close the IIFE in the JSX
content = content.replace("""                );
             })}
             <Button""", """                );
             });
             })()}
             <Button""")


# 2. Fix the Blob Download logic
old_submit = """      if (editingDocId) {
        const response = await axios.put(`/api/contratacion/documento/${editingDocId}/regenerar`, { datos: dinamicData }, {
            responseType: 'blob'
        });
        
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `Proceso_${procesoId}_Regenerado.docx`);
        document.body.appendChild(link);
        link.click();
        link.parentNode?.removeChild(link);
        window.URL.revokeObjectURL(url);
        
        setToast({ open: true, message: 'Documento regenerado exitosamente', severity: 'success' });
      } else {
        const response = await axios.post('/api/contratacion/documento', {
          proceso_contratacion_id: parseInt(procesoId as string),
          plantilla_id: parseInt(selectedPlantillaId),
          datos: dinamicData
        }, {
            responseType: 'blob'
        });
        
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `Proceso_${procesoId}_Generado.docx`);
        document.body.appendChild(link);
        link.click();
        link.parentNode?.removeChild(link);
        window.URL.revokeObjectURL(url);

        setToast({ open: true, message: 'Documento generado exitosamente', severity: 'success' });
      }"""

new_submit = """      if (editingDocId) {
        const response = await axios.put(`/api/contratacion/documento/${editingDocId}/regenerar`, { datos: dinamicData }, {
            responseType: 'blob'
        });
        
        if (response.data instanceof Blob || response.headers['content-type']?.includes('wordprocessingml') || response.headers['content-type']?.includes('octet-stream')) {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', `Proceso_${procesoId}_Regenerado.docx`);
          document.body.appendChild(link);
          link.click();
          link.parentNode?.removeChild(link);
          window.URL.revokeObjectURL(url);
          setToast({ open: true, message: 'Documento regenerado exitosamente', severity: 'success' });
        } else {
          setToast({ open: true, message: 'El servidor no devolvió un archivo válido.', severity: 'error' });
        }
      } else {
        const response = await axios.post('/api/contratacion/documento', {
          proceso_contratacion_id: parseInt(procesoId as string),
          plantilla_id: parseInt(selectedPlantillaId),
          datos: dinamicData
        }, {
            responseType: 'blob'
        });
        
        if (response.data instanceof Blob || response.headers['content-type']?.includes('wordprocessingml') || response.headers['content-type']?.includes('octet-stream')) {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', `Proceso_${procesoId}_Generado.docx`);
          document.body.appendChild(link);
          link.click();
          link.parentNode?.removeChild(link);
          window.URL.revokeObjectURL(url);
          setToast({ open: true, message: 'Documento generado exitosamente', severity: 'success' });
        } else {
          setToast({ open: true, message: 'El servidor no devolvió un archivo válido.', severity: 'error' });
        }
      }"""

content = content.replace(old_submit, new_submit)

with open(path, "w") as f:
    f.write(content)
