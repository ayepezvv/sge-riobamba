import re
path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

old_download = """  const handleDownload = (path: string) => {
    setToast({ open: true, message: `El archivo físico está en el backend en: ${path}`, severity: 'info' });
  };"""
  
new_download = """  const handleDownload = async (docId: number, version: number) => {
    try {
      const response = await axios.get(`/api/contratacion/documento/${docId}/descargar`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Documento_v${version}.docx`);
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      setToast({ open: true, message: 'Error al descargar el archivo', severity: 'error' });
    }
  };"""

content = content.replace(old_download, new_download)
content = content.replace("onClick={() => handleDownload(params.row.ruta_archivo_generado)}", "onClick={() => handleDownload(params.row.id, params.row.version)}")

with open(path, "w") as f:
    f.write(content)
