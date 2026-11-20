# Empresa Autónoma

Proyecto abierto para coordinar agentes de gestión en empresas distintas, con verificación humana. La primera demo prueba la secuencia comercial → entrega → facturación mediante reglas locales y datos ficticios. Carece de integración con modelos y servicios externos. El nombre del aprobador en la CLI es una declaración local, no autenticación.

## Probar con Python 3

```bash
python3 empresa.py ventas
python3 empresa.py ventas --aprobar Demo
python3 empresa.py operaciones
python3 empresa.py operaciones --entrega-verificada --aprobar Demo
python3 empresa.py cobros
python3 empresa.py cobros --aprobar Demo
python3 empresa.py estado
```

Cada comando acepta `--caso` y `--db`. Las confirmaciones quedan registradas en SQLite. Los requisitos previos bloquean pasos fuera de orden y la base impide repetir un hito.

La demo registra hitos. La propuesta comercial y la factura todavía no son documentos generados. La siguiente fase es definir, a partir de dos empresas piloto, los datos mínimos y los criterios de aceptación de los agentes independientes y del flujo compartido.
