#!/usr/bin/python3

TELETRABAJO = "Es dia de teletrabajo ocasional"
FESTIVO = "Es día festivo."
VACACIONES = "Hoy estás de vacaciones. Disfruta del día."

# Dias teletrabajo (Lunes=1, Martes=2, Miercoles=3, Jueves=4, Viernes=5)
diasTeletrabajo = [1,2]

# Horas
hinicio = "8:00"
hfin = "18:00"
hinicioV = "7:30"
hfinV = "15:00"

# Programa
urlVO = 'https://newvo.orange.es'
urlOAMBase = 'https://applogin.orange.es'
urlRegistroJ = 'https://newvo.orange.es/group/viveorange/registro-de-jornada'
urlRegistroJC = 'https://newvo.orange.es/api/jsonws/invoke'
urlRJAccion = 'https://www.registratujornadaorange.com/RealizarAccion'
urlRJInforme = 'https://www.registratujornadaorange.com/ObtenerContenidoInformeGeneral'

# Festivos que se repiten todos los años
festivosAnuales = []
festivosAnuales.append("01/01")
festivosAnuales.append("06/01")
festivosAnuales.append("06/04")
festivosAnuales.append("07/04")
festivosAnuales.append("01/05")
festivosAnuales.append("02/05")
festivosAnuales.append("15/08")
festivosAnuales.append("12/10")
festivosAnuales.append("01/11")
festivosAnuales.append("06/12")
festivosAnuales.append("08/12")
festivosAnuales.append("25/12")
festivosAnuales.append("15/05") # San Isidro
festivosAnuales.append("09/11") # Almudena

# festivosOtros vacaciones (año completo)
vacaciones = []
vacaciones.append("17/04")
vacaciones.append("18/04")
vacaciones.append("19/04")
vacaciones.append("20/04")
vacaciones.append("21/04")
vacaciones.append("26/04")
vacaciones.append("27/04")
vacaciones.append("28/04")


# Dias que teletrabajo fuera de los planificados ( X,J,V )
teletrabajo = []
teletrabajo.append("05/04")
teletrabajo.append("10/05")
teletrabajo.append("11/08")
teletrabajo.append("16/08")