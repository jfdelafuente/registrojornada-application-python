#!/usr/bin/env python3
"""
Script de validación del entorno para Registro de Jornada Bot.

Verifica que el entorno esté correctamente configurado antes de ejecutar el bot:
- Versión de Python
- Dependencias instaladas
- Variables de entorno encriptadas
- Archivos de configuración
- Permisos de directorios
- Conectividad básica

Uso:
    python scripts/validate_environment.py
    python scripts/validate_environment.py --verbose
"""

import sys
import os
from pathlib import Path
import importlib
from typing import List, Tuple, Dict
import argparse


# Colores para terminal (compatibles con Windows y Unix)
class Colors:
    """ANSI color codes para output en terminal."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def disable():
        """Deshabilitar colores (para Windows sin soporte ANSI)."""
        Colors.HEADER = ''
        Colors.OKBLUE = ''
        Colors.OKCYAN = ''
        Colors.OKGREEN = ''
        Colors.WARNING = ''
        Colors.FAIL = ''
        Colors.ENDC = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''


# Deshabilitar colores en Windows si no hay soporte
if sys.platform == 'win32':
    try:
        import colorama
        colorama.init()
    except ImportError:
        Colors.disable()


class EnvironmentValidator:
    """Validador de entorno para el bot de Registro de Jornada."""

    def __init__(self, verbose: bool = False):
        """
        Inicializar validador.

        Args:
            verbose: Mostrar información detallada
        """
        self.verbose = verbose
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.checks_passed = 0
        self.checks_total = 0

        # Detectar directorio raíz del proyecto
        self.project_root = Path(__file__).parent.parent
        self.app_dir = self.project_root / 'app'
        self.data_dir = self.project_root / 'data'
        self.logs_dir = self.project_root / 'logs'

    def print_header(self, text: str):
        """Imprimir encabezado."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

    def print_check(self, name: str, passed: bool, message: str = ""):
        """
        Imprimir resultado de un check.

        Args:
            name: Nombre del check
            passed: Si pasó o no
            message: Mensaje adicional
        """
        self.checks_total += 1
        if passed:
            self.checks_passed += 1
            status = f"{Colors.OKGREEN}✓ PASS{Colors.ENDC}"
        else:
            status = f"{Colors.FAIL}✗ FAIL{Colors.ENDC}"

        print(f"{status} {name}")
        if message and self.verbose:
            print(f"      {Colors.OKCYAN}→{Colors.ENDC} {message}")

    def check_python_version(self) -> bool:
        """Verificar versión de Python."""
        print(f"{Colors.BOLD}1. Verificando versión de Python...{Colors.ENDC}")

        required_major = 3
        required_minor = 11

        current_version = sys.version_info
        version_str = f"{current_version.major}.{current_version.minor}.{current_version.micro}"

        if current_version.major >= required_major and current_version.minor >= required_minor:
            self.print_check(
                f"Python {required_major}.{required_minor}+",
                True,
                f"Versión actual: {version_str}"
            )
            return True
        else:
            self.print_check(
                f"Python {required_major}.{required_minor}+",
                False,
                f"Versión actual: {version_str} (se requiere {required_major}.{required_minor}+)"
            )
            self.errors.append(
                f"Python {required_major}.{required_minor}+ requerido, encontrado {version_str}"
            )
            return False

    def check_dependencies(self) -> bool:
        """Verificar dependencias instaladas."""
        print(f"\n{Colors.BOLD}2. Verificando dependencias...{Colors.ENDC}")

        # Dependencias core
        core_dependencies = [
            ('beautifulsoup4', 'bs4', '4.12.3'),
            ('lxml', 'lxml', '5.3.0'),
            ('pyTelegramBotAPI', 'telebot', '4.21.0'),
            ('python-dotenv', 'dotenv', '1.0.1'),
            ('requests', 'requests', '2.32.3'),
            ('pydantic', 'pydantic', '2.10.3'),
            ('pydantic-settings', 'pydantic_settings', '2.6.1'),
            ('cryptography', 'cryptography', '42.0.5'),
        ]

        all_installed = True

        for package_name, import_name, expected_version in core_dependencies:
            try:
                module = importlib.import_module(import_name)
                version = getattr(module, '__version__', 'unknown')

                self.print_check(
                    f"{package_name}",
                    True,
                    f"v{version} (esperada: {expected_version})"
                )
            except ImportError:
                self.print_check(f"{package_name}", False, f"No instalado")
                self.errors.append(f"Dependencia faltante: {package_name}")
                all_installed = False

        return all_installed

    def check_environment_variables(self) -> bool:
        """Verificar variables de entorno."""
        print(f"\n{Colors.BOLD}3. Verificando variables de entorno...{Colors.ENDC}")

        env_file = self.project_root / '.env'

        # Verificar que existe .env
        if not env_file.exists():
            self.print_check(".env file", False, "Archivo no encontrado")
            self.errors.append("Archivo .env no encontrado. Ejecuta scripts/encrypt_secrets.py")
            return False

        self.print_check(".env file", True, f"Encontrado en {env_file}")

        # Cargar y verificar variables
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)

            required_vars = [
                'ENCRYPTION_KEY',
                'BOT_TOKEN_ENCRYPTED',
                'HR_USERNAME_ENCRYPTED',
                'HR_PASSWORD_ENCRYPTED',
                'EMPLOYEE_CODE_ENCRYPTED',
            ]

            all_present = True
            for var in required_vars:
                value = os.getenv(var)
                if value:
                    # Mostrar primeros caracteres para verificar formato
                    preview = value[:20] + '...' if len(value) > 20 else value
                    self.print_check(
                        var,
                        True,
                        f"Presente ({preview})"
                    )
                else:
                    self.print_check(var, False, "No encontrada")
                    self.errors.append(f"Variable de entorno faltante: {var}")
                    all_present = False

            return all_present

        except Exception as e:
            self.print_check("Cargar .env", False, str(e))
            self.errors.append(f"Error cargando .env: {e}")
            return False

    def check_encryption_key(self) -> bool:
        """Verificar que ENCRYPTION_KEY es válida."""
        print(f"\n{Colors.BOLD}4. Verificando clave de encriptación...{Colors.ENDC}")

        try:
            from dotenv import load_dotenv
            load_dotenv(self.project_root / '.env')

            encryption_key = os.getenv('ENCRYPTION_KEY')
            if not encryption_key:
                self.print_check("ENCRYPTION_KEY", False, "No encontrada")
                self.errors.append("ENCRYPTION_KEY no configurada")
                return False

            # Verificar formato Fernet
            from cryptography.fernet import Fernet
            try:
                Fernet(encryption_key.encode())
                self.print_check(
                    "Formato ENCRYPTION_KEY",
                    True,
                    "Formato Fernet válido"
                )
                return True
            except Exception as e:
                self.print_check("Formato ENCRYPTION_KEY", False, str(e))
                self.errors.append(f"ENCRYPTION_KEY inválida: {e}")
                return False

        except Exception as e:
            self.print_check("Validar ENCRYPTION_KEY", False, str(e))
            self.errors.append(f"Error validando ENCRYPTION_KEY: {e}")
            return False

    def check_config_files(self) -> bool:
        """Verificar archivos de configuración."""
        print(f"\n{Colors.BOLD}5. Verificando archivos de configuración...{Colors.ENDC}")

        required_files = [
            (self.app_dir / 'config.py', 'Pydantic Settings'),
            (self.app_dir / 'configD.py', 'Configuración legacy'),
            (self.data_dir / 'holidays.json', 'Festivos nacionales'),
        ]

        all_present = True
        for file_path, description in required_files:
            if file_path.exists():
                size = file_path.stat().st_size
                self.print_check(
                    description,
                    True,
                    f"{file_path.name} ({size} bytes)"
                )
            else:
                self.print_check(description, False, f"{file_path} no encontrado")
                if 'holidays.json' in str(file_path):
                    self.warnings.append(f"Archivo opcional faltante: {file_path}")
                else:
                    self.errors.append(f"Archivo requerido faltante: {file_path}")
                    all_present = False

        return all_present

    def check_directory_structure(self) -> bool:
        """Verificar estructura de directorios."""
        print(f"\n{Colors.BOLD}6. Verificando estructura de directorios...{Colors.ENDC}")

        required_dirs = [
            (self.app_dir, 'app/'),
            (self.app_dir / 'core', 'app/core/'),
            (self.app_dir / 'models', 'app/models/'),
            (self.app_dir / 'services', 'app/services/'),
            (self.app_dir / 'repositories', 'app/repositories/'),
            (self.app_dir / 'security', 'app/security/'),
            (self.app_dir / 'utils', 'app/utils/'),
            (self.app_dir / 'validators', 'app/validators/'),
            (self.app_dir / 'exceptions', 'app/exceptions/'),
            (self.data_dir, 'data/'),
        ]

        all_present = True
        for dir_path, name in required_dirs:
            if dir_path.exists() and dir_path.is_dir():
                file_count = len(list(dir_path.glob('*.py')))
                self.print_check(
                    name,
                    True,
                    f"{file_count} archivos .py"
                )
            else:
                self.print_check(name, False, "Directorio no encontrado")
                self.errors.append(f"Directorio faltante: {dir_path}")
                all_present = False

        return all_present

    def check_logs_directory(self) -> bool:
        """Verificar directorio de logs y permisos."""
        print(f"\n{Colors.BOLD}7. Verificando directorio de logs...{Colors.ENDC}")

        # Crear directorio si no existe
        if not self.logs_dir.exists():
            try:
                self.logs_dir.mkdir(parents=True, exist_ok=True)
                self.print_check(
                    "Crear logs/",
                    True,
                    "Directorio creado automáticamente"
                )
            except Exception as e:
                self.print_check("Crear logs/", False, str(e))
                self.errors.append(f"No se pudo crear directorio logs/: {e}")
                return False
        else:
            self.print_check("logs/", True, "Directorio existe")

        # Verificar permisos de escritura
        test_file = self.logs_dir / '.write_test'
        try:
            test_file.write_text('test')
            test_file.unlink()
            self.print_check("Permisos escritura logs/", True, "OK")
            return True
        except Exception as e:
            self.print_check("Permisos escritura logs/", False, str(e))
            self.errors.append(f"Sin permisos de escritura en logs/: {e}")
            return False

    def check_imports(self) -> bool:
        """Verificar que los módulos del proyecto se pueden importar."""
        print(f"\n{Colors.BOLD}8. Verificando módulos del proyecto...{Colors.ENDC}")

        # Agregar app/ al path
        sys.path.insert(0, str(self.app_dir))

        modules_to_check = [
            'config',
            'core.container',
            'services.auth_service',
            'services.hr_service',
            'services.notification_service',
            'services.report_service',
            'utils.error_handler',
            'security.secrets_manager',
            'exceptions',
        ]

        all_imported = True
        for module_name in modules_to_check:
            try:
                importlib.import_module(module_name)
                self.print_check(f"Importar {module_name}", True, "OK")
            except Exception as e:
                self.print_check(f"Importar {module_name}", False, str(e))
                self.errors.append(f"Error importando {module_name}: {e}")
                all_imported = False

        return all_imported

    def check_connectivity(self) -> bool:
        """Verificar conectividad básica (opcional)."""
        print(f"\n{Colors.BOLD}9. Verificando conectividad (opcional)...{Colors.ENDC}")

        try:
            import requests
            from dotenv import load_dotenv

            load_dotenv(self.project_root / '.env')

            # Test conectividad a Telegram (sin autenticación completa)
            try:
                response = requests.get('https://api.telegram.org', timeout=5)
                if response.status_code == 200 or response.status_code == 404:
                    self.print_check(
                        "Telegram API",
                        True,
                        "Servidor accesible"
                    )
                else:
                    self.print_check(
                        "Telegram API",
                        False,
                        f"Status code: {response.status_code}"
                    )
                    self.warnings.append("No se pudo conectar a Telegram API")
            except Exception as e:
                self.print_check("Telegram API", False, str(e))
                self.warnings.append(f"No se pudo conectar a Telegram API: {e}")

            return True  # No es crítico, solo warning

        except Exception as e:
            self.print_check("Test conectividad", False, str(e))
            self.warnings.append(f"Error en test de conectividad: {e}")
            return True  # No es crítico

    def print_summary(self):
        """Imprimir resumen final."""
        self.print_header("RESUMEN DE VALIDACIÓN")

        print(f"{Colors.BOLD}Checks ejecutados:{Colors.ENDC} {self.checks_total}")
        print(f"{Colors.OKGREEN}Checks pasados:{Colors.ENDC} {self.checks_passed}")
        print(f"{Colors.FAIL}Checks fallados:{Colors.ENDC} {self.checks_total - self.checks_passed}")

        if self.warnings:
            print(f"\n{Colors.WARNING}{Colors.BOLD}⚠ ADVERTENCIAS ({len(self.warnings)}):{Colors.ENDC}")
            for warning in self.warnings:
                print(f"  {Colors.WARNING}•{Colors.ENDC} {warning}")

        if self.errors:
            print(f"\n{Colors.FAIL}{Colors.BOLD}✗ ERRORES ({len(self.errors)}):{Colors.ENDC}")
            for error in self.errors:
                print(f"  {Colors.FAIL}•{Colors.ENDC} {error}")

            print(f"\n{Colors.FAIL}{Colors.BOLD}El entorno NO está listo para ejecutar el bot.{Colors.ENDC}")
            print(f"\n{Colors.BOLD}Acciones sugeridas:{Colors.ENDC}")
            print(f"  1. Instalar dependencias: {Colors.OKCYAN}pip install -r requirements.txt{Colors.ENDC}")
            print(f"  2. Configurar credenciales: {Colors.OKCYAN}python scripts/encrypt_secrets.py{Colors.ENDC}")
            print(f"  3. Verificar archivos de configuración en app/")
            print(f"  4. Re-ejecutar validación: {Colors.OKCYAN}python scripts/validate_environment.py{Colors.ENDC}")

            return False
        else:
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ El entorno está correctamente configurado!{Colors.ENDC}")
            print(f"\n{Colors.BOLD}Puedes ejecutar el bot:{Colors.ENDC}")
            print(f"  {Colors.OKCYAN}python app/bot.py{Colors.ENDC}")

            return True

    def validate(self) -> bool:
        """
        Ejecutar todas las validaciones.

        Returns:
            True si todas las validaciones pasaron, False en caso contrario
        """
        self.print_header("VALIDACIÓN DE ENTORNO")
        print(f"{Colors.OKCYAN}Proyecto:{Colors.ENDC} {self.project_root}")
        print(f"{Colors.OKCYAN}Python:{Colors.ENDC} {sys.version.split()[0]}")

        # Ejecutar checks
        self.check_python_version()
        self.check_dependencies()
        self.check_environment_variables()
        self.check_encryption_key()
        self.check_config_files()
        self.check_directory_structure()
        self.check_logs_directory()
        self.check_imports()
        self.check_connectivity()

        # Resumen
        return self.print_summary()


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Validar entorno para Registro de Jornada Bot'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mostrar información detallada'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Deshabilitar colores en output'
    )

    args = parser.parse_args()

    if args.no_color:
        Colors.disable()

    validator = EnvironmentValidator(verbose=args.verbose)
    success = validator.validate()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
