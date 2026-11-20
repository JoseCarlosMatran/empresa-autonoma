"""Demo local de coordinación empresarial con datos ficticios."""
import argparse
import sqlite3

AGENTES = {
    "ventas": (None, "propuesta", "Preparar propuesta comercial"),
    "operaciones": ("propuesta", "entrega", "Registrar entrega verificada"),
    "cobros": ("entrega", "factura", "Preparar borrador de factura"),
}

def abrir(ruta):
    db = sqlite3.connect(ruta)
    db.execute("""CREATE TABLE IF NOT EXISTS historial (
        caso TEXT, hito TEXT, aprobador TEXT NOT NULL,
        PRIMARY KEY (caso, hito))""")
    return db

def proponer(db, caso, agente):
    previo, hito, tarea = AGENTES[agente]
    hechos = dict(db.execute(
        "SELECT hito, aprobador FROM historial WHERE caso = ?", (caso,)))
    if hito in hechos or (previo and previo not in hechos):
        return None
    return hito, tarea

def confirmar(db, caso, agente, aprobador, entrega_verificada=False):
    if not aprobador.strip():
        raise ValueError("Se requiere identificar a la persona que confirma.")
    if agente == "operaciones" and not entrega_verificada:
        raise ValueError("Se requiere confirmar la entrega.")
    propuesta = proponer(db, caso, agente)
    if not propuesta:
        raise ValueError("Acción ya registrada o requisito previo pendiente.")
    with db:
        db.execute("INSERT INTO historial VALUES (?, ?, ?)",
                   (caso, propuesta[0], aprobador))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agente", choices=[*AGENTES, "estado"])
    parser.add_argument("--db", default="demo.sqlite")
    parser.add_argument("--caso", default="DEMO-001")
    parser.add_argument("--aprobar", metavar="NOMBRE")
    parser.add_argument("--entrega-verificada", action="store_true")
    args = parser.parse_args()
    db = abrir(args.db)
    if args.agente == "estado":
        for hito, persona in db.execute(
            "SELECT hito, aprobador FROM historial WHERE caso = ? ORDER BY rowid",
            (args.caso,)):
            print(f"{hito}: confirmado por {persona}")
        return
    try:
        if args.aprobar is not None:
            confirmar(db, args.caso, args.agente, args.aprobar, args.entrega_verificada)
            print("Confirmación registrada.")
        else:
            propuesta = proponer(db, args.caso, args.agente)
            print(propuesta[1] if propuesta else "Acción completada o bloqueada.")
    except (ValueError, sqlite3.IntegrityError) as error:
        parser.exit(1, f"{error}\n")

if __name__ == "__main__":
    main()
