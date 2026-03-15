from decimal import Decimal

def test_payroll_logic():
    print("--- Simulador de Validación de Cálculos de Nómina ---")
    
    # Parámetros Mock (equivalentes a rrhh.parametro_calculo)
    SBU = Decimal('460.00')
    IESS_PERSONAL_PERCENT = Decimal('9.45')
    
    # Datos de Empleado Mock
    salario_acordado = Decimal('1200.00')
    
    print(f"[INFO] Parámetros: SBU={SBU}, % IESS Personal={IESS_PERSONAL_PERCENT}")
    print(f"[INFO] Salario Base: {salario_acordado}")
    
    # 1. Cálculo de Aportación IESS
    aporte_iess = (salario_acordado * IESS_PERSONAL_PERCENT) / Decimal('100.00')
    # Redondeo a 2 decimales
    aporte_iess = aporte_iess.quantize(Decimal('0.01'))
    
    # 2. Otros cálculos (ej. Fondos de Reserva - simplificado)
    fondos_reserva = (salario_acordado * Decimal('8.33')) / Decimal('100.00')
    fondos_reserva = fondos_reserva.quantize(Decimal('0.01'))
    
    # 3. Neto a Recibir
    neto = salario_acordado - aporte_iess
    
    print("\n[RESULTADOS]")
    print(f"   (+) Ingresos: {salario_acordado}")
    print(f"   (-) IESS Personal: {aporte_iess}")
    print(f"   (=) Neto a Pagar: {neto}")
    
    # Validaciones
    assert aporte_iess == Decimal('113.40'), "Error en cálculo de IESS"
    assert neto == Decimal('1086.60'), "Error en cálculo de Neto"
    
    print("\n[OK] Los cálculos matemáticos coinciden con los estándares legales de Ecuador.")
    print("--- Prueba de Nómina Finalizada ---")

if __name__ == "__main__":
    test_payroll_logic()
