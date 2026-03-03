import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/catastro/ciudadanos/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Replace the lower section of the details panel
old_details = """                  <Box sx={{ mt: 3, display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <EmailTwoToneIcon color="secondary" />
                      <Typography variant="body2">{selectedUser.correo_principal || 'No registrado'}</Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <PhoneTwoToneIcon color="secondary" />
                      <Typography variant="body2">{selectedUser.celular || selectedUser.telefono_fijo || 'No registrado'}</Typography>
                    </Box>
                    
                    {selectedUser.tipo_persona === 'Natural' && selectedUser.fecha_nacimiento && (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <CakeIcon color="secondary" />
                        <Typography variant="body2">{selectedUser.fecha_nacimiento}</Typography>
                      </Box>
                    )}
                    
                    {selectedUser.tipo_persona === 'Natural' && selectedUser.genero && (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <WcIcon color="secondary" />
                        <Typography variant="body2">{selectedUser.genero}</Typography>
                      </Box>
                    )}

                    {selectedUser.tipo_persona === 'Juridica' && selectedUser.tipo_empresa && (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <BusinessIcon color="secondary" />
                        <Typography variant="body2">{selectedUser.tipo_empresa} - {selectedUser.naturaleza_juridica}</Typography>
                      </Box>
                    )}

                    {/* Beneficios (Si aplican) */}
                    {(selectedUser.tiene_discapacidad || selectedUser.aplica_tercera_edad) && (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mt: 1 }}>
                        <AssignmentIndIcon color="secondary" />
                        <Box>
                          {selectedUser.aplica_tercera_edad && <Chip label="Tercera Edad" size="small" color="info" sx={{ mr: 1 }} />}
                          {selectedUser.tiene_discapacidad && <Chip label={`Discapacidad (${selectedUser.porcentaje_discapacidad}%)`} size="small" color="warning" />}
                        </Box>
                      </Box>
                    )}
                  </Box>"""

new_details = """                  <Box sx={{ mt: 3, display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <Typography variant="subtitle1" color="primary">Información de Contacto</Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <EmailTwoToneIcon color="secondary" fontSize="small" />
                          <Box>
                            <Typography variant="caption" color="textSecondary" display="block">Correo</Typography>
                            <Typography variant="body2">{selectedUser.correo_principal || 'No registrado'}</Typography>
                          </Box>
                        </Box>
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <PhoneTwoToneIcon color="secondary" fontSize="small" />
                          <Box>
                            <Typography variant="caption" color="textSecondary" display="block">Teléfonos</Typography>
                            <Typography variant="body2">{selectedUser.celular} / {selectedUser.telefono_fijo || 'N/A'}</Typography>
                          </Box>
                        </Box>
                      </Grid>
                    </Grid>

                    <Divider sx={{ my: 1 }} />
                    <Typography variant="subtitle1" color="primary">Datos Demográficos / Comerciales</Typography>
                    
                    <Grid container spacing={2}>
                      {selectedUser.tipo_persona === 'Natural' && selectedUser.fecha_nacimiento && (
                        <Grid item xs={12} sm={6}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <CakeIcon color="secondary" fontSize="small" />
                            <Box>
                              <Typography variant="caption" color="textSecondary" display="block">Nacimiento</Typography>
                              <Typography variant="body2">{selectedUser.fecha_nacimiento}</Typography>
                            </Box>
                          </Box>
                        </Grid>
                      )}
                      {selectedUser.tipo_persona === 'Natural' && selectedUser.genero && (
                        <Grid item xs={12} sm={6}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <WcIcon color="secondary" fontSize="small" />
                            <Box>
                              <Typography variant="caption" color="textSecondary" display="block">Género</Typography>
                              <Typography variant="body2">{selectedUser.genero}</Typography>
                            </Box>
                          </Box>
                        </Grid>
                      )}
                      {selectedUser.tipo_persona === 'Juridica' && selectedUser.tipo_empresa && (
                        <Grid item xs={12}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <BusinessIcon color="secondary" fontSize="small" />
                            <Box>
                              <Typography variant="caption" color="textSecondary" display="block">Estructura</Typography>
                              <Typography variant="body2">{selectedUser.tipo_empresa} - {selectedUser.naturaleza_juridica}</Typography>
                            </Box>
                          </Box>
                        </Grid>
                      )}
                    </Grid>

                    {/* Beneficios (Si aplican) */}
                    {(selectedUser.tiene_discapacidad || selectedUser.aplica_tercera_edad) && (
                      <>
                        <Divider sx={{ my: 1 }} />
                        <Typography variant="subtitle1" color="primary">Beneficios de Ley</Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mt: 1 }}>
                          <AssignmentIndIcon color="secondary" />
                          <Box>
                            {selectedUser.aplica_tercera_edad && <Chip label="Tercera Edad" size="small" color="info" sx={{ mr: 1 }} />}
                            {selectedUser.tiene_discapacidad && <Chip label={`Discapacidad (${selectedUser.porcentaje_discapacidad}%)`} size="small" color="warning" />}
                          </Box>
                        </Box>
                      </>
                    )}
                    
                    {/* Referencias Anidadas */}
                    {selectedUser.referencias && selectedUser.referencias.length > 0 && (
                      <>
                        <Divider sx={{ my: 1 }} />
                        <Typography variant="subtitle1" color="primary">Referencias Registradas</Typography>
                        {selectedUser.referencias.map((ref: any, idx: number) => (
                           <Box key={idx} sx={{ p: 1.5, bgcolor: 'background.default', borderRadius: 1, border: '1px dashed', borderColor: 'divider' }}>
                             <Typography variant="body2" fontWeight="bold">{ref.tipo_referencia}</Typography>
                             <Typography variant="body2">{ref.nombres} {ref.apellidos}</Typography>
                             <Typography variant="caption" color="textSecondary">CI: {ref.identificacion || 'N/A'}</Typography>
                           </Box>
                        ))}
                      </>
                    )}
                  </Box>"""

content = content.replace(old_details, new_details)

with open(path, "w") as f:
    f.write(content)
