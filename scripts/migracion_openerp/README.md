# Estrategia de Migración OpenERP → SGE

## Arquitectura

- **Origen:** OpenERP 7, PostgreSQL 9.x, IP: 192.168.1.49, BD: siim_adm (solo lectura)
- **Destino:** SGE, PostgreSQL 15 en Docker, IP: 192.168.1.15, puerto: 5433
- **Credenciales origen:** usuario openerp / contraseña openerp (solo SELECT)

## Proceso ETL

```
[OpenERP 192.168.1.49]
        │
        ▼  (1_extraccion.py)
[CSV/JSON en /tmp/migracion/]
        │
        ▼  (2_transformacion.py)
[DataFrames limpios con nomenclatura SGE]
        │
        ▼  (3_carga.py)
[PostgreSQL SGE 192.168.1.15:5433]
        │
        ▼  (4_validacion.py)
[Reporte de conteos y checksums]
```

## Módulos a migrar (prioridad)

| Prioridad | Módulo SGE    | Tabla OpenERP fuente                   | Registros aprox |
|-----------|---------------|----------------------------------------|-----------------|
| 1         | presupuesto   | account_budget_post, budget_certificate| 30.898          |
| 2         | rrhh          | hr_employee, hr_contract               | 4.089 / 14.018  |
| 3         | contabilidad  | account_account, account_move          | 20.104 / 53.538 |
| 4         | tesoreria     | account_bank_statement                 | estimado 5.000+ |
| 5         | financiero    | account_voucher (pagos)                | estimado 28.000+|

## Rollback

Cada script de carga guarda checkpoint en /tmp/migracion/rollback_*.sql
Ejecutar: `psql -h 192.168.1.15 -p 5433 -U sge -f /tmp/migracion/rollback_presupuesto.sql`

## Validación

Post-migración ejecutar `4_validacion.py` que compara:
- Conteos de registros origen vs destino
- Checksums de montos totales
- Integridad referencial
