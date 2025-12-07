import re
from datetime import datetime


def validarDay(fecha: str) -> bool:
    """
    Valida si la variable fechas está en formato YYYYMMDD

    Args:
        fecha (str): Fecha a validar su formato

    Returns:
        bool: True si el formato es correcto
    """
    return bool(re.match(r'^\d{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])$', fecha))
    
def validarDias(fecha: str, lista_fechas: list) -> bool:
    """
    Comprueba si 'fecha' está incluido en la 'lista_fechas'

    Args:
        fecha (str): fecha en formato YYYYMMDD
        lista_fechas (list): lista de string en formato YYYYMMDD

    Returns:
        bool: True si 'fecha' está incluíodo en 'lista_fecha'
    """
    fecha_real = datetime.strptime(fecha, "%Y%m%d")
    return fecha_real.strftime("%d/%m") in lista_fechas

def validarDiaTT(fecha:str, lista_fechas: list) -> bool:
    """
    Comprueba si el dia de la semana a la que pertenence 'fecha' 
    está incluido en la 'lista_fechas'. Los valores válidos son:
    1:Lunes,2:Martes,3:Miercóles ...6:Sabado y 7:Domingo

    Args:
        fecha (str): fecha en formato YYYYMMDD
        lista_fechas (list): lista de valores. ejemplo [1,2,3]

    Returns:
        bool: True si 'fecha' está incluíodo en 'lista_fecha'
    """
    fecha_real = datetime.strptime(fecha, "%Y%m%d")
    if fecha_real.isoweekday() in lista_fechas:
        return True
    return False