import unittest
from datetime import datetime
from app.DiaValidator import dia_validate
from app.configD import configD

class DiasTestCase(unittest.TestCase):
    
    def setUp(self):
        print("\n--------------------------------")
        
    def test_dia_actual_laboral_oficina(self):
        print("Running test_dia_actual_laboral_oficina")
        dia = datetime.strptime("20230503", "%Y%m%d").date()
        mensaje, registar = dia_validate(dia)
        print("mensaje : %s" % mensaje)
        self.assertEqual(registar, False)
        self.assertEqual(mensaje, "\n" + configD.TELETRABAJO+ " : " +str(registar))
    
    def test_dia_actual_laboral_teletrabajo(self):
        print("Running test_dia_actual_laboral_teletrabajo")
        dia = datetime.strptime("20230508", "%Y%m%d").date()
        mensaje, registar = dia_validate(dia)
        print("mensaje : %s" % mensaje)
        self.assertEqual(registar, True)
        self.assertEqual(mensaje, "")
        
    def test_dia_actual_laboral_teletrabajo_ocasional(self):
        print("Running test_dia_actual_laboral_teletrabajo_ocasional")
        dia = datetime.strptime("20230811", "%Y%m%d").date()
        mensaje, registar = dia_validate(dia)
        print("mensaje : %s" % mensaje)
        self.assertEqual(registar, True)
        self.assertEqual(mensaje, "\n" +configD.TELETRABAJO+ " : " +str(registar))
        
    def test_dia_actual_festivo(self):
        print("Running test_dia_actual_festivo")
        dia = datetime.strptime("20230502", "%Y%m%d").date()
        mensaje, registar = dia_validate(dia)
        print("mensaje : %s" % mensaje)
        self.assertEqual(registar, False)
        self.assertEqual(mensaje, "\n" +configD.FESTIVO)
        
    def test_dia_actual_vacaciones(self):
        print("Running test_dia_actual_vacaciones")
        dia = datetime.strptime("20230428", "%Y%m%d").date()
        mensaje, registar = dia_validate(dia)
        print("mensaje : %s" % mensaje)
        self.assertEqual(registar, False)
        self.assertEqual(mensaje, "\n" +configD.VACACIONES)
        
    def test_dia_actual_finde_semana(self):
        print("Running test_dia_actual_finde_semana")
        dia = datetime.strptime("20230506", "%Y%m%d").date()
        mensaje, registar = dia_validate(dia)
        print("mensaje : %s" % mensaje)
        self.assertEqual(registar, False)
        self.assertEqual(mensaje, "\n" +configD.TELETRABAJO+ " : " +str(registar))
        
    def test_dia_actual_domingo(self):
        print("Running test_dia_actual_domingo")
        dia = datetime.strptime("20230507", "%Y%m%d").date()
        mensaje, registar = dia_validate(dia)
        print("mensaje : %s" % mensaje)
        self.assertEqual(registar, False)
        self.assertEqual(mensaje, "\n" +configD.TELETRABAJO+ " : " +str(registar))
    
    def test_san_isidro(self):
        print("Running test_san_isidro")
        dia = datetime.strptime("20230515", "%Y%m%d").date()
        mensaje, registar = dia_validate(dia)
        print("mensaje : %s" % mensaje)
        self.assertEqual(registar, False)
        self.assertEqual(mensaje, "\n" +configD.FESTIVO)
    
        
if __name__ == '__main__':
    unittest.main()