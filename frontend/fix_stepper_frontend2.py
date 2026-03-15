import re

path = "src/app/(dashboard)/contratacion/procesos/page.tsx"
with open(path, "r") as f:
    content = f.read()

# We need to make sure the indices match the new 5 step array:
# 0 Afectacion PAC
# 1 Naturaleza (was 0)
# 2 Catalogo (was 1)
# 3 Monto (was 2)
# 4 Expediente (was 3)

# Let's fix the step numbers
content = content.replace("activeStep === 1 && (\n            <Grid container spacing={3}>\n              <Grid item xs={12}>\n                <Typography variant=\"h6\" color=\"primary\" gutterBottom>2. ¿El bien o servicio consta", "activeStep === 2 && (\n            <Grid container spacing={3}>\n              <Grid item xs={12}>\n                <Typography variant=\"h6\" color=\"primary\" gutterBottom>3. ¿El bien o servicio consta")
content = content.replace("activeStep === 2 && (\n            <Grid container spacing={3}>\n              <Grid item xs={12}>\n                <Typography variant=\"h6\" color=\"primary\" gutterBottom>3. Presupuesto", "activeStep === 3 && (\n            <Grid container spacing={3}>\n              <Grid item xs={12}>\n                <Typography variant=\"h6\" color=\"primary\" gutterBottom>4. Presupuesto")
content = content.replace("activeStep === 3 && (\n            <Grid container spacing={3}>\n              <Grid item xs={12}>\n                <Typography variant=\"h6\" color=\"primary\" gutterBottom>4. Generación", "activeStep === 4 && (\n            <Grid container spacing={3}>\n              <Grid item xs={12}>\n                <Typography variant=\"h6\" color=\"primary\" gutterBottom>5. Generación")

# Calculate automatic referential budget from PAC
auto_monto = """
  const presupuestoReferencial = selectedPacItems.reduce((acc, id) => {
    const item = pacItems.find((i: any) => i.id === id) as any;
    const monto = pacMontos[id] ?? (item ? item.valor_total : 0);
    return acc + monto;
  }, 0);
"""
content = content.replace("const [pacMontos, setPacMontos] = useState<Record<number, number>>({});", "const [pacMontos, setPacMontos] = useState<Record<number, number>>({});\n" + auto_monto)

# Pre-fill Monto step
monto_step_search = """<TextField 
                  fullWidth 
                  label="Presupuesto Referencial ($)" 
                  type="number"
                  value={formData.presupuesto_referencial || ''} 
                  onChange={(e) => setFormData({ ...formData, presupuesto_referencial: parseFloat(e.target.value) })}
                />"""
monto_step_replace = """<TextField 
                  fullWidth 
                  label="Presupuesto Referencial (Autocalculado del PAC)" 
                  type="number"
                  disabled
                  value={presupuestoReferencial}
                />"""
content = content.replace(monto_step_search, monto_step_replace)

# Ensure next button goes up to 4
content = content.replace("activeStep === 3 ? 'Guardar Expediente' : 'Siguiente'", "activeStep === 4 ? 'Guardar Expediente' : 'Siguiente'")

# Also update the save payload to use the auto calculated budget
content = content.replace("...formData,", "...formData,\n        presupuesto_referencial: presupuestoReferencial,")

with open(path, "w") as f:
    f.write(content)
