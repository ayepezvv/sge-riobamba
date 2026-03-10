import re

path = "src/app/(dashboard)/contratacion/procesos/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Add dynamic inputs for montos comprometidos
dynamic_inputs = """
            {selectedPacItems.length > 0 && (
              <Grid item xs={12}>
                <Card variant="outlined" sx={{ bgcolor: 'background.default', p: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>Montos a Comprometer del Presupuesto Referencial</Typography>
                    {selectedPacItems.map(id => {
                        const item: any = pacItems.find((i: any) => i.id === id);
                        if (!item) return null;
                        return (
                            <Box key={id} display="flex" justifyContent="space-between" alignItems="center" mb={1} gap={2}>
                                <Typography variant="body2" sx={{ flex: 1 }}>{item.cpc} - {item.descripcion.substring(0, 40)}... (Disp: ${item.valor_total})</Typography>
                                <TextField 
                                    size="small" 
                                    type="number" 
                                    label="Monto ($)" 
                                    defaultValue={item.valor_total}
                                    sx={{ width: 150 }} 
                                />
                            </Box>
                        )
                    })}
                </Card>
              </Grid>
            )}
"""

content = content.replace("</FormControl>\n            </Grid>\n            <Grid item xs={12}>\n              <TextField fullWidth", "</FormControl>\n            </Grid>" + dynamic_inputs + "\n            <Grid item xs={12}>\n              <TextField fullWidth")

with open(path, "w") as f:
    f.write(content)
