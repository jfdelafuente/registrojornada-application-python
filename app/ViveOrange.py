from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import logging
import requests
import re
import json
import configD
from dotenv import load_dotenv
import os

class ViveOrange:
  pasada = False
  registrar = True
  USER = ''
  PASSW = ''
  COD_EMPLEADO = ''

  def __init__(self, registrar, pasada):
    load_dotenv()
    self.pasada = pasada
    self.registrar = registrar
    self.USER = os.environ['USUARIO']
    self.PASSW = os.environ['PASS']
    self.COD_EMPLEADO = os.environ['COD_EMPLEADO']

  def dummy(self, dia, msg):
    mensaje = "Dummy : %s  -  %s" % (str(dia), msg)
    logging.info("ViveOrange Dummy -->  '%s'" % mensaje)
    return mensaje

  def connectar(self, dia):
    hoy = dia.strftime("%d/%m/%Y")
    hinicio = configD.hinicio
    hfin = configD.hfin
    mensaje = ''

    # Construir JSON de forma segura para evitar inyección
    peticion_data = {
        "/vo_autologin.autologin/get-registra-tu-jornada": {
            "employeeNumber": int(self.COD_EMPLEADO)
        }
    }
    peticionCMD = json.dumps(peticion_data)
    
    #Nos tenemos que logar en Vive Orange para sacar la autorizacion del registro de jornada
    sHeaders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}
    s = requests.Session()
    s.headers.update(sHeaders)
    logging.info("Nos vamos a Vive Orange...")
    logging.debug("Cookies 1: " + str(s.cookies.get_dict()))
    logging.debug("Headers 1: " + str(s.headers))
    r = s.get(configD.urlVO)
    logging.debug(r.headers)
    logging.info(r.status_code)
    logging.debug(r.cookies)
    logging.debug(r.text)
    logging.debug("Cookies 2: " + str(s.cookies.get_dict()))
    logging.debug("Headers 2: " + str(s.headers))

    soup = BeautifulSoup(r.text, 'lxml')
    soup1 = soup.select('body form')

    urlOAM = ''
    cabecerasOAM = {}

    for f in soup1:
        logging.debug(f.get('action'))
        urlOAM = f.get('action')
        hidden_tags = f.find_all("input", type="hidden")
        for tag in hidden_tags:
            logging.debug(tag)
            cabecerasOAM[tag.get("name")] = tag.get("value")

    logging.info(urlOAM)
    logging.info(cabecerasOAM)
    logging.info("Nos vamos a OAM...")
    r = s.post(urlOAM, data=cabecerasOAM)
    logging.debug(r.headers)
    logging.info(r.status_code)
    logging.debug(r.cookies)
    logging.debug(r.text)
    logging.debug("Cookies 3: " + str(s.cookies.get_dict()))
    logging.debug("Headers 3: " + str(s.headers))

    soup = BeautifulSoup(r.text, 'lxml')
    soup1 = soup.select('form#loginData')

    urlOAM = configD.urlOAMBase
    cabecerasOAM = {}

    for f in soup1:
        logging.debug(f.get('action'))
        urlOAM = urlOAM + f.get('action')
        hidden_tags = f.find_all("input", type="hidden")
        for tag in hidden_tags:
            logging.debug(tag)
            if tag.get("name") == "username":
                cabecerasOAM["username"] = self.USER
            elif tag.get("name") == "password":
                cabecerasOAM["password"] = self.PASSW
            else:
                cabecerasOAM[tag.get("name")] = tag.get("value")
    cabecerasOAM["temp-username"] = self.USER
    cabecerasOAM["password"] = self.PASSW

    logging.info(urlOAM)
    logging.info(cabecerasOAM)
    logging.info("Nos logamos en OAM...")
    r = s.post(urlOAM, data=cabecerasOAM)
    logging.debug(r.headers)
    logging.info(r.status_code)
    logging.debug(r.cookies)
    logging.debug(r.text)
    logging.debug("Cookies 4: " + str(s.cookies.get_dict()))
    logging.debug("Headers 4: " + str(s.headers))

    # Volvemos a Vive Orange
    soup = BeautifulSoup(r.text, 'lxml')
    soup1 = soup.select('body form')

    urlOAM = ''
    cabecerasOAM = {}

    for f in soup1:
        logging.debug(f.get('action'))
        urlOAM = f.get('action')
        hidden_tags = f.find_all("input", type="hidden")
        for tag in hidden_tags:
            cabecerasOAM[tag.get("name")] = tag.get("value")

    logging.info(urlOAM)
    logging.info(cabecerasOAM)
    logging.info("Volvemos a Vive Orange...")
    r = s.post(urlOAM, data=cabecerasOAM)
    logging.debug(r.headers)
    logging.info(r.status_code)
    logging.debug(r.cookies)
    logging.debug(r.text)
    logging.debug("Cookies 5: " + str(s.cookies.get_dict()))
    logging.debug("Headers 5: " + str(s.headers))


    r = s.get(configD.urlRegistroJ)
    logging.debug(r.headers)
    logging.info(r.status_code)
    logging.debug(r.cookies)
    logging.debug(r.text)
    logging.debug("Cookies 6: " + str(s.cookies.get_dict()))
    logging.debug("Headers 6: " + str(s.headers))

    authToken = re.findall(r".*Liferay.authToken\s?\=\s?'(.*)';",r.text)
    logging.debug(authToken)

    peticion = {}
    peticion["cmd"] = peticionCMD
    peticion["p_auth"] = authToken[0]
    logging.debug(peticion)
    logging.info("Buscamos la autenticacion para el registro de jornada...")
    r = s.post(configD.urlRegistroJC, data=peticion)
    logging.debug(r.headers)
    logging.info(r.status_code)
    logging.debug(r.cookies)
    logging.info(r.text)
    logging.debug("Cookies 7: " + str(s.cookies.get_dict()))
    logging.debug("Headers 7: " + str(s.headers))

    # Nos logamos en la web del registro de jornada
    url = r.text.replace("\"","").replace("\\","")
    s = requests.Session()
    logging.info("Obtenemos jsessionid")
    r = s.get(url)
    logging.info(s.cookies.get("JSESSIONID"))
    logging.info(r.headers)
    logging.info(r.status_code)
    logging.info(r.cookies)

    if self.registrar == True:
        logging.info("Cargamos registro jornada (ko valor normal) para " + hoy + " de " + hinicio + " a " + hfin)
        r = s.post(configD.urlRJAccion, data = {"tipoAccion":"horaRegistroCargada","motivo":"1","fechaini":hoy+" "+hinicio,"fechafin":hoy+" "+hfin,"sede":"","horaEfectiva":""})
        html_text = r.text
        logging.info(html_text)
        logging.info(r.status_code)
        mensaje += f'\nCargado registro de jornada {hoy} de {hinicio} a {hfin}'


    finD = date.today()
    #hoy5d = date.today() - timedelta(days=5)
    #hoy5 = hoy5d.strftime("%d/%m/%Y")
    lunesD = datetime.today() - timedelta(days=datetime.today().weekday() % 7)

    if self.pasada:
        lunesD = lunesD - timedelta(days=7)
        finD = lunesD + timedelta(days=4)

    lunes = lunesD.strftime("%d/%m/%Y")
    fin = finD.strftime("%d/%m/%Y")

    logging.info("Consultamos registro jornada desde " + lunes + " hasta " + fin)
    # r = s.post(configD.urlRJInforme, data = {"tipoInforme":"1",
    #                                         "checkcodigo":"1", 
    #                                         "seleccionIdEmpleado":"", 
    #                                         "movil":"0",
    #                                         "seleccionFechaInicio":lunes+"", 
    #                                         "seleccionFechaFin":fin+""
    #                                        })
    
    
    r = s.post(configD.urlRJInforme, data = {"tipoInforme":"1",
                                             "movil":"0",
                                             "num":"0",
                                             "seleccionFechaInicio":lunes+"",
                                             "seleccionFechaFin":fin+""})
    html_text = r.text
    logging.info(html_text)
    logging.info(r.status_code)

    soup = BeautifulSoup(html_text, 'lxml')
    soup1 = soup.select('#tblEventos > tbody > tr')

    dias = 0    
    diasT = 0 
    diasF = 0 
    totalSegundos = 0 

    msg = ''
    for i in soup1:
        logging.info(i.select_one('td:nth-child(1)').text)
        logging.info(i.select_one('td:nth-child(2)').text)
        logging.info(i.select_one('td:nth-child(3)').text)
        logging.info(i.select_one('td:nth-child(4)').text)
        logging.info(i.select_one('td:nth-child(5)').text)
        logging.info(i.select_one('td:nth-child(6)').text)
        msg += "\n# %s : %s\n  %s : %s" % (i.select_one('td:nth-child(3)').text, \
            i.select_one('td:nth-child(4)').text, \
            i.select_one('td:nth-child(5)').text, \
            i.select_one('td:nth-child(6)').text)
        dInicio = datetime.strptime(i.select_one('td:nth-child(3)').text, '%d/%m/%Y %H:%M')
        dFin = datetime.strptime(i.select_one('td:nth-child(5)').text, '%d/%m/%Y %H:%M')
        totalSegundos += (dFin - dInicio).total_seconds()
        dias += 1
        if "TELETRABAJO" in i.select_one('td:nth-child(4)').text:
            diasT += 1
        if "FINCA" in i.select_one('td:nth-child(4)').text:
            diasF += 1

    totalHoras = totalSegundos/3600
    mensaje += f'\nInforme desde {lunes} hasta el {fin}:\n - {dias} dias trabajados ({diasT} teletrabajo, {diasF} La Finca)\n - Total horas: {totalHoras:.2f}'
    mensaje += msg
    logging.info(mensaje)
    return mensaje