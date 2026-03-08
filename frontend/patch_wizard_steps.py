import re
path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Fix Step 1 (Separation of options)
old_step1 = """<MenuItem value="Bienes y Servicios">Bienes y Servicios Normalizados / No Normalizados</MenuItem>
                  <MenuItem value="Obras">Ejecución de Obras</MenuItem>
                  <MenuItem value="Consultoria">Consultoría</MenuItem>"""

new_step1 = """<MenuItem value="Bienes">Adquisición de Bienes</MenuItem>
                  <MenuItem value="Servicios">Prestación de Servicios</MenuItem>
                  <MenuItem value="Obras">Ejecución de Obras</MenuItem>
                  <MenuItem value="Consultoria">Consultoría</MenuItem>"""

content = content.replace(old_step1, new_step1)

# Fix Step 3 (Dynamic loading)
old_step3 = """            {activeStep === 2 && wizardData.catalogo_electronico === 'No' && (
              <FormControl fullWidth>
                <InputLabel>Monto Referencial Aproximado</InputLabel>
                <Select value={wizardData.monto} label="Monto Referencial Aproximado" onChange={(e) => setWizardData({...wizardData, monto: e.target.value})}>
                  <MenuItem value="infima">Menor a $ 7,495.00 (Ínfima Cuantía)</MenuItem>
                  <MenuItem value="menor">Entre $ 7,495.00 y $ 64,554.00 (Menor Cuantía / Cotización)</MenuItem>
                  <MenuItem value="subasta">Mayor a $ 64,554.00 (Subasta Inversa Electrónica)</MenuItem>
                  <MenuItem value="licitacion">Mayor a $ 490,000.00 (Licitación)</MenuItem>
                </Select>
              </FormControl>
            )}"""

new_step3 = """            {activeStep === 2 && wizardData.catalogo_electronico === 'No' && (
              <FormControl fullWidth>
                <InputLabel>Monto Referencial / Condición</InputLabel>
                <Select value={wizardData.monto} label="Monto Referencial / Condición" onChange={(e) => setWizardData({...wizardData, monto: e.target.value})}>
                  {tiposProceso.filter(t => t.is_activo && (t.categoria.includes(wizardData.categoria) || wizardData.categoria.includes(t.categoria.split(' ')[0])) && !t.nombre.includes('Catálogo')).map((t: any) => (
                    <MenuItem key={t.id} value={t.id}>{t.condicion_monto || 'Sin límite específico'} ({t.nombre})</MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}"""
            
content = content.replace(old_step3, new_step3)

# Fix the next logic to catch the dynamic ID instead of text mapping
old_next = """    if (activeStep === 2) {
      // Determinar el tipo de proceso según respuestas
      let recomendado = null;
      if (wizardData.catalogo_electronico === 'Si') {
        recomendado = tiposProceso.find(t => t.nombre.includes('Catálogo'));
      } else {
        // Logica simplificada del SERCOP
        if (wizardData.monto === 'infima') recomendado = tiposProceso.find(t => t.nombre.includes('Ínfima') || t.nombre.includes('Infima'));
        else if (wizardData.monto === 'menor') recomendado = tiposProceso.find(t => t.nombre.includes('Menor'));
        else if (wizardData.monto === 'subasta') recomendado = tiposProceso.find(t => t.nombre.includes('Subasta'));
        else if (wizardData.monto === 'licitacion') recomendado = tiposProceso.find(t => t.nombre.includes('Licitación') && t.categoria === wizardData.categoria);
      }
      
      // Fallback
      if (!recomendado) recomendado = tiposProceso.find(t => t.categoria === wizardData.categoria) || tiposProceso[0];
      
      setTipoRecomendado(recomendado);
    }"""

new_next = """    if (activeStep === 2) {
      let recomendado = null;
      if (wizardData.catalogo_electronico === 'Si') {
        recomendado = tiposProceso.find(t => t.nombre.includes('Catálogo'));
      } else if (wizardData.monto) {
        recomendado = tiposProceso.find(t => t.id === parseInt(wizardData.monto));
      }
      setTipoRecomendado(recomendado);
    }"""
    
content = content.replace(old_next, new_next)

with open(path, "w") as f:
    f.write(content)
