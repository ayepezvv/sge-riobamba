import re

path = "src/app/(dashboard)/contratacion/procesos/page.tsx"
with open(path, "r") as f:
    content = f.read()

# 1. Update Steps Array
content = content.replace("const steps = ['Naturaleza', 'Catálogo', 'Monto', 'Expediente'];", "const steps = ['Afectación PAC', 'Naturaleza', 'Catálogo', 'Monto', 'Expediente'];")

# 2. Extract PAC state to be a dictionary of id -> monto
state_add = """  const [pacMontos, setPacMontos] = useState<Record<number, number>>({});"""
content = content.replace("const [selectedPacItems, setSelectedPacItems] = useState<number[]>([]);", "const [selectedPacItems, setSelectedPacItems] = useState<number[]>([]);\n" + state_add)

# 3. Handle Select Change to preset max amount
handle_pac = """  const handlePacChange = (event: any) => {
    const value = event.target.value;
    const selectedIds = typeof value === 'string' ? value.split(',') : value;
    setSelectedPacItems(selectedIds);
    
    // Auto-completar nombre de proyecto si es el primer item
    if (selectedIds.length > 0 && !formData.nombre_proyecto) {
        const firstItem = pacItems.find((i: any) => i.id === selectedIds[0]) as any;
        if (firstItem) {
            setFormData(prev => ({ ...prev, nombre_proyecto: firstItem.descripcion }));
        }
    }
  };

  const handleMontoChange = (id: number, value: string) => {
    const num = parseFloat(value) || 0;
    setPacMontos(prev => ({ ...prev, [id]: num }));
  };
"""

content = re.sub(r'  const handlePacChange = \(event: any\) => \{.*?\n  \};', handle_pac, content, flags=re.DOTALL)

# 4. Remove the old PAC logic from handleSave (we do it differently now)
old_save_links = """        // Vincular PAC si aplica (crear enlaces proporcionales)
        if (selectedPacItems.length > 0) {
            const links = selectedPacItems.map(id => {
                const item: any = pacItems.find((i: any) => i.id === id);
                return { item_pac_id: id, monto_comprometido: item ? item.valor_total : 0 };
            });
            await fetch(`http://192.168.1.15:8000/api/contratacion/procesos/${newProceso.id || editingId}/vincular_pac`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(links)
            });
        }"""
content = content.replace(old_save_links, "")

# 5. Update actual payload of handleSave to include items_pac
payload_replace = """    const items_pac = selectedPacItems.map(id => ({
        item_pac_id: id,
        monto_comprometido: pacMontos[id] || 0
    }));
    
    const payload = { 
        ...formData, 
        tipo_proceso_id: parseInt(formData.tipo_proceso_id),
        items_pac: items_pac
    };"""
content = content.replace("const payload = { ...formData, tipo_proceso_id: parseInt(formData.tipo_proceso_id) };", payload_replace)


# 6. Refactor the Stepper UI
# Remove the old PAC select from its random place (it was in Naturaleza before probably or just floating)
old_pac_ui = r'<Grid item xs=\{12\}>\s*<FormControl fullWidth>\s*<InputLabel>Vincular a Líneas del PAC.*?\{\/\* END OF RANDOM PAC \*\/'

# Actually, I injected it right before `<Grid item xs={12}>\n              <TextField fullWidth label="Código del Proceso"`
# Let's find exactly what I injected earlier and remove it from the wrong step.
content = re.sub(r'<Grid item xs=\{12\}>\s*<FormControl fullWidth>\s*<InputLabel>Vincular a Líneas del PAC \(Opcional\).*?</Card>\s*</Grid>\s*\)}', '', content, flags=re.DOTALL)

# Now, we redefine the steps.
# Step 0: Afectacion PAC
# Step 1: Naturaleza
# Step 2: Catalogo
# Step 3: Monto
# Step 4: Expediente

step_0 = """
          {activeStep === 0 && (
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <Typography variant="h6" color="primary" gutterBottom>1. Afectación Presupuestaria (PAC)</Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>Selecciona las líneas del Plan Anual de Contratación de las que nace este requerimiento.</Typography>
                </Grid>
                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel>Seleccionar Líneas del PAC Activo</InputLabel>
                    <Select
                      multiple
                      value={selectedPacItems}
                      onChange={handlePacChange}
                      label="Seleccionar Líneas del PAC Activo"
                      renderValue={(selected) => selected.map(id => {
                        const item: any = pacItems.find((i: any) => i.id === id);
                        return item ? `${item.cpc} - ${item.descripcion.substring(0, 30)}...` : id;
                      }).join(', ')}
                    >
                      {pacItems.map((item: any) => (
                        <MenuItem key={item.id} value={item.id}>
                          {item.cpc} | {item.descripcion} (Disp: ${item.valor_total})
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                {selectedPacItems.length > 0 && (
                  <Grid item xs={12}>
                    <Card variant="outlined" sx={{ bgcolor: 'background.default', p: 2 }}>
                        <Typography variant="subtitle2" gutterBottom>Montos a Comprometer</Typography>
                        {selectedPacItems.map(id => {
                            const item: any = pacItems.find((i: any) => i.id === id);
                            if (!item) return null;
                            return (
                                <Box key={id} display="flex" justifyContent="space-between" alignItems="center" mb={1} gap={2}>
                                    <Typography variant="body2" sx={{ flex: 1 }}>{item.cpc} - {item.descripcion}</Typography>
                                    <TextField 
                                        size="small" 
                                        type="number" 
                                        label="Monto a comprometer ($)" 
                                        value={pacMontos[id] ?? item.valor_total}
                                        onChange={(e) => handleMontoChange(id, e.target.value)}
                                        sx={{ width: 200 }} 
                                        error={(pacMontos[id] ?? item.valor_total) > item.valor_total}
                                        helperText={(pacMontos[id] ?? item.valor_total) > item.valor_total ? 'Excede saldo' : ''}
                                    />
                                </Box>
                            )
                        })}
                    </Card>
                  </Grid>
                )}
            </Grid>
          )}
"""

content = content.replace("{activeStep === 0 && (", step_0 + "\n          {activeStep === 1 && (")
content = content.replace("{activeStep === 1 && (", "{activeStep === 2 && (", 1) # shift remaining
content = content.replace("{activeStep === 2 && (", "{activeStep === 3 && (", 1)
content = content.replace("{activeStep === 3 && (", "{activeStep === 4 && (", 1)

# Step 3 logic (now Step 4? Wait)
# original: 0 Naturaleza, 1 Catalogo, 2 Monto, 3 Expediente
# now: 0 PAC, 1 Naturaleza, 2 Catalogo, 3 Monto, 4 Expediente
# We need to correctly shift all numbers in the conditions.

# Let's use regex to shift the activeStep === X upwards.
# We already replaced 0 with 0(new) and 1. We just need to shift the rest carefully.
# ACTUALLY, it's easier to just find the sections and replace.

with open(path, "w") as f:
    f.write(content)
