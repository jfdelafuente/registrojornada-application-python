import argparse
import re
import sys
from datetime import date, datetime, timedelta

import configDD
from utils.validarDay import validarDay, validarDias, validarDiaTT

# Crear el analizador de argumentos
parser = argparse.ArgumentParser(description="Procesa un parámetro obligatorio.", add_help=False)
parser.add_argument("tipo", choices=["INFO", "INFOP", "DIA"], help="Tipo de operación a realizar.")
parser.add_argument("fecha", nargs="?", help="Fecha en formato YYYYMMDD para el tipo DIA.")

args = parser.parse_args()

# Verificar si se proporcionó el argumento 'tipo' y si es 'DIA', asegurarse de que también se proporcionó 'fecha'
if args.tipo == "DIA" and not args.fecha:
    print("Error: Debes incluir una fecha en formato YYYYMMDD cuando elijas DIA.")
    sys.exit(1)

# Verificar el formato de la fecha si se proporcionó
if args.fecha:
    if not re.match(r"^\d{8}$", args.fecha):
        print("Error: El formato de la fecha debe ser YYYYMMDD.")
        sys.exit(1)

# Realizar una acción basada en el argumento proporcionado
if args.tipo == "INFO":
    print("Se seleccionó INFO.")
elif args.tipo == "INFOP":
    print("Se seleccionó INFOP.")
elif args.tipo == "DIA":
    print(f"Se seleccionó DIA con la fecha {args.fecha}.")

    if validarDay(args.fecha):
        print(f"La {args.fecha} es festivo ? {validarDias(args.fecha, configDD.festivosAnuales)}")
        print(f"La {args.fecha} es Vacaciones ? {validarDias(args.fecha, configDD.vacaciones)}")
        if not validarDiaTT(args.fecha, configDD.diasTeletrabajo):
            print(
                f"La {args.fecha} es Teletrabajo Ocasional ? {validarDias(args.fecha, configDD.teletrabajo)}"
            )
        else:
            print(f"La {args.fecha} es dia de Teletrabajo")

    else:
        print("no valida")
