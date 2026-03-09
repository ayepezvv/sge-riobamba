import re
path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# 1. Fix Modal Render schema mapping
old_modal_start = """             {(() => {
                const tableSchema = esquemaVariables.find((e: any) => e.nombre === activeTableVar);
                const columnsToRender = (tableSchema && (tableSchema.columnas || tableSchema.sub_atributos)) 
                  ? (tableSchema.columnas || tableSchema.sub_atributos)
                  : Object.keys(tempRowItem);

                return columnsToRender.map((colKey: string) => {"""

new_modal_start = """             {(() => {
                const tableSchema = esquemaVariables.find((e: any) => e.nombre === activeTableVar);
                const columnasFila = tableSchema?.sub_atributos || tableSchema?.columnas || Object.keys(tempRowItem);

                return columnasFila.map((colKey: string) => {"""

content = content.replace(old_modal_start, new_modal_start)


# 2. Fix the Download Blob logic to use native fetch for robustness
old_submit_block = """      if (editingDocId) {
        const response = await axios.put(`/api/contratacion/documento/${editingDocId}/regenerar`, { datos: dinamicData }, {
            responseType: 'blob'
        });
        
        if (response.data instanceof Blob || response.headers['content-type']?.includes('wordprocessingml') || response.headers['content-type']?.includes('octet-stream')) {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          // El backend envia el filename en Content-Disposition si esta disponible
          let fileName = `Proceso_${procesoId}_Regenerado.docx`;
          const disposition = response.headers['content-disposition'];
          if (disposition && disposition.includes('filename=')) {
              fileName = disposition.split('filename=')[1].replace(/['"]/g, '').split(';')[0];
          }
          link.setAttribute('download', fileName);
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
          let fileName = `Proceso_${procesoId}_Generado.docx`;
          const disposition = response.headers['content-disposition'];
          if (disposition && disposition.includes('filename=')) {
              fileName = disposition.split('filename=')[1].replace(/['"]/g, '').split(';')[0];
          }
          link.setAttribute('download', fileName);
          document.body.appendChild(link);
          link.click();
          link.parentNode?.removeChild(link);
          window.URL.revokeObjectURL(url);
          setToast({ open: true, message: 'Documento generado exitosamente', severity: 'success' });
        } else {
          setToast({ open: true, message: 'El servidor no devolvió un archivo válido.', severity: 'error' });
        }
      }"""

new_submit_block = """      const serviceToken = window.localStorage.getItem('serviceToken');
      const authHeader = serviceToken ? { 'Authorization': `Bearer ${serviceToken}` } : {};
      
      if (editingDocId) {
        const response = await fetch(`/api/contratacion/documento/${editingDocId}/regenerar`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json', ...authHeader },
          body: JSON.stringify({ datos: dinamicData })
        });
        
        if (!response.ok) throw new Error("Error en el servidor al regenerar");
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `Documento_${procesoId}_Regenerado.docx`);
        document.body.appendChild(link);
        link.click();
        link.parentNode?.removeChild(link);
        window.URL.revokeObjectURL(url);
        
        setToast({ open: true, message: 'Documento regenerado exitosamente', severity: 'success' });
      } else {
        const payload = {
          proceso_contratacion_id: parseInt(procesoId as string),
          plantilla_id: parseInt(selectedPlantillaId),
          datos: dinamicData
        };
        
        const response = await fetch('/api/contratacion/documento', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', ...authHeader },
          body: JSON.stringify(payload)
        });
        
        if (!response.ok) throw new Error("Error en el servidor al generar");
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `Documento_${procesoId}_Generado.docx`);
        document.body.appendChild(link);
        link.click();
        link.parentNode?.removeChild(link);
        window.URL.revokeObjectURL(url);

        setToast({ open: true, message: 'Documento generado exitosamente', severity: 'success' });
      }"""

content = content.replace(old_submit_block, new_submit_block)

# 3. Patch the download icon button just in case
old_download_btn = """      const response = await axios.get(`/api/contratacion/documento/${docId}/descargar`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Documento_v${version}.docx`);
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url);"""

new_download_btn = """      const serviceToken = window.localStorage.getItem('serviceToken');
      const authHeader = serviceToken ? { 'Authorization': `Bearer ${serviceToken}` } : {};
      const response = await fetch(`/api/contratacion/documento/${docId}/descargar`, {
        method: 'GET',
        headers: { ...authHeader }
      });
      
      if (!response.ok) throw new Error("Archivo no disponible");
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Documento_v${version}.docx`);
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url);"""

content = content.replace(old_download_btn, new_download_btn)

with open(path, "w") as f:
    f.write(content)
