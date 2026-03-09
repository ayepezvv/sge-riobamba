import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Replace the submission logic to handle the blob correctly
old_submit = """  const handleDocSubmit = async () => {
    try {
      if (editingDocId) {
        await axios.put(`/api/contratacion/documento/${editingDocId}/regenerar`, { datos: dinamicData });
        setToast({ open: true, message: 'Documento regenerado exitosamente', severity: 'success' });
      } else {
        await axios.post('/api/contratacion/documento', {
          proceso_contratacion_id: parseInt(procesoId as string),
          plantilla_id: parseInt(selectedPlantillaId),
          datos: dinamicData
        });
        setToast({ open: true, message: 'Documento generado exitosamente', severity: 'success' });
      }
      setOpenDoc(false);
      fetchData(); // Refresh list
    } catch (error: any) {
      setToast({ open: true, message: error.response?.data?.detail || 'Error al generar', severity: 'error' });
    }
  };"""

new_submit = """  const handleDocSubmit = async () => {
    try {
      if (editingDocId) {
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
      }
      setOpenDoc(false);
      fetchData(); // Refresh list
    } catch (error: any) {
      // Axios con blob devuelve el error como FileReader
      if (error.response && error.response.data instanceof Blob) {
          const reader = new FileReader();
          reader.onload = () => {
              try {
                  const errorData = JSON.parse(reader.result as string);
                  setToast({ open: true, message: errorData.detail || 'Error al generar', severity: 'error' });
              } catch (e) {
                  setToast({ open: true, message: 'Error de validación en la generación', severity: 'error' });
              }
          };
          reader.readAsText(error.response.data);
      } else {
          setToast({ open: true, message: error.response?.data?.detail || 'Error al generar', severity: 'error' });
      }
    }
  };"""

content = content.replace(old_submit, new_submit)

with open(path, "w") as f:
    f.write(content)
