# 📱 Registro de Jornada - Bot de Telegram

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-88%20passing-success.svg)](docs/fases/docs/fases/FASE4_TESTING.md)
[![Coverage](https://img.shields.io/badge/coverage->85%25-success.svg)](docs/fases/docs/fases/FASE4_TESTING.md)
[![Phase](https://img.shields.io/badge/phase-4%20completed-blue.svg)](docs/fases/)
[![License](https://img.shields.io/badge/license-Internal-orange.svg)]()

> **Fase 4 completada** ✅ - 88 tests, >85% coverage, CI/CD automatizado
> Ver [📚 Documentación completa](docs/) y [🗺️ Roadmap](docs/NEXT_STEPS.md)

Bot de Telegram para automatizar el registro de jornadas laborales en el sistema ViveOrange de empleados de Orange España.

---

## 🎯 Características Principales

### Funcionalidad Core
- ✅ **Registro automático de jornadas** laborales
- ✅ **Consulta de registros** semanales (actual y anterior)
- ✅ **Validación inteligente** de días festivos y vacaciones
- ✅ **Gestión de teletrabajo** con confirmación opcional
- ✅ **Informes estadísticos avanzados** con análisis de patrones
- ✅ **Exportación a JSON** de registros y estadísticas

### Seguridad (Fase 1)
- ✅ **Credenciales encriptadas** con Fernet
- ✅ **Logs sanitizados** sin información sensible
- ✅ **Validación de entradas** robusta contra XSS e inyección
- ✅ **Prevención de vulnerabilidades** CVE resueltas

### Arquitectura (Fase 2 & 3)
- ✅ **Arquitectura en capas** (Models, Services, Repositories)
- ✅ **Dependency Injection** con ServiceContainer
- ✅ **Pydantic Settings** para configuración type-safe
- ✅ **Jerarquía de excepciones** personalizada (22 tipos)
- ✅ **Manejo centralizado de errores** con mensajes user-friendly
- ✅ **Notificaciones inteligentes** con rate limiting y retry
- ✅ **Repositorio de festivos** con caché LRU
- ✅ **Containerización** con Docker

---

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.11+
- Token de bot de Telegram (obtener de [@BotFather](https://t.me/botfather))
- Credenciales de ViveOrange
- Código de empleado

### Instalación

1. **Clonar el repositorio**
   ```bash
   cd registrojornada-application-python
   git clone https://github.com/jfdelafuente/registrojornada-application-python.git
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar credenciales** 🔐

   **IMPORTANTE:** Las credenciales deben estar encriptadas (novedad Fase 1)

   ```bash
   # Ejecutar script de encriptación
   python scripts/encrypt_secrets.py
   ```

   El script solicitará:
   - Token del bot de Telegram
   - Chat ID de Telegram
   - Usuario de ViveOrange
   - Contraseña de ViveOrange
   - Código de empleado

   Copie el output generado al archivo `.env`

5. **Validar el entorno** ✅ (Recomendado)

   **NUEVO:** Antes de ejecutar el bot, valida que todo esté correctamente configurado:

   ```bash
   # Validación completa del entorno
   python scripts/validate_environment.py

   # Validación con detalles
   python scripts/validate_environment.py --verbose
   ```

   El script verificará:
   - ✅ Versión de Python (3.11+)
   - ✅ Dependencias instaladas y versiones
   - ✅ Variables de entorno encriptadas
   - ✅ Archivos de configuración
   - ✅ Estructura de directorios
   - ✅ Permisos de escritura en logs/
   - ✅ Módulos del proyecto importables
   - ✅ Conectividad básica (Telegram API)

6. **Ejecutar el bot**
   ```bash
   python app/bot.py
   ```

---

## 📁 Estructura del Proyecto

```
registrojornada-application-python/
├── app/                          # Código fuente de la aplicación
│   ├── core/                     # 🆕 Dependency Injection (Fase 3)
│   │   ├── __init__.py
│   │   └── container.py         # ServiceContainer (Singleton)
│   ├── models/                   # 🆕 Modelos de datos (Fase 2)
│   │   ├── __init__.py
│   │   └── workday.py           # WorkdayRegistration, WeeklyReport (Pydantic)
│   ├── services/                 # 🆕 Capa de servicios (Fases 2 & 3)
│   │   ├── __init__.py
│   │   ├── auth_service.py      # Autenticación ViveOrange
│   │   ├── hr_service.py        # Registro de jornadas e informes
│   │   ├── notification_service.py  # Notificaciones Telegram (rate limit)
│   │   └── report_service.py    # Informes avanzados y estadísticas
│   ├── repositories/             # 🆕 Repositorios de datos (Fase 2)
│   │   ├── __init__.py
│   │   └── holiday_repository.py  # Gestión de festivos (LRU cache)
│   ├── security/                 # 🆕 Módulos de seguridad (Fase 1)
│   │   ├── __init__.py
│   │   └── secrets_manager.py   # Gestión de credenciales encriptadas
│   ├── utils/                    # 🆕 Utilidades (Fases 1 & 3)
│   │   ├── __init__.py
│   │   ├── logger.py            # Logging con sanitización
│   │   ├── error_handler.py     # 🆕 Manejo centralizado de errores
│   │   └── validarDay.py        # Validación de fechas
│   ├── validators/               # 🆕 Validadores (Fase 1)
│   │   ├── __init__.py
│   │   └── input_validator.py   # Validación de entradas (XSS, injection)
│   ├── exceptions/               # 🆕 Excepciones personalizadas (Fase 3)
│   │   └── __init__.py          # Jerarquía de 22 excepciones
│   ├── bot.py                    # 🔄 Punto de entrada principal (refactorizado)
│   ├── config.py                 # 🆕 Pydantic Settings (Fase 2)
│   ├── ViveOrange.py            # ⚠️ Legacy (se mantiene por compatibilidad)
│   ├── DiaValidator.py          # Validación de días laborales
│   ├── BotTelegramRegistro.py   # ⚠️ Legacy wrapper Telegram
│   ├── configD.py               # ⚠️ Legacy configuración (deprecado)
│   └── main2.py                 # CLI alternativo
├── data/                         # 🆕 Datos de configuración (Fase 2)
│   └── holidays.json            # Festivos nacionales y regionales
├── scripts/                      # 🆕 Scripts de utilidad (Fases 1-3)
│   ├── encrypt_secrets.py       # Script de encriptación de credenciales
│   └── validate_environment.py  # 🆕 Validador de entorno (Fase 3)
├── tests/                        # Tests unitarios
│   ├── test_bot_telegram_registro.py
│   ├── test_dias_validator.py
│   └── test_main.py
├── logs/                         # 🆕 Logs (generados automáticamente)
│   ├── registrojornada.log
│   └── vive_orange.log
├── .env                          # Variables de entorno encriptadas 🔒
├── .env.example                  # 🆕 Template de configuración
├── .gitignore                    # Archivos ignorados por Git
├── Dockerfile                    # Configuración Docker
├── docker-compose.yml            # Orquestación Docker
├── requirements.txt              # Dependencias actualizadas
├── README.md                     # Este archivo
├── ANALISIS_PROYECTO.md          # 🆕 Análisis completo del proyecto
├── docs/fases/FASE1_SEGURIDAD.md           # 🆕 Documentación Fase 1 (Seguridad)
├── docs/fases/FASE2_REFACTORIZACION.md     # 🆕 Documentación Fase 2 (Arquitectura)
└── docs/fases/FASE3_SERVICIOS.md           # 🆕 Documentación Fase 3 (Servicios)
```

### Arquitectura en Capas

```
┌─────────────────────────────────────────┐
│         bot.py (Handlers)              │  ← Telegram Bot Handlers
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      ServiceContainer (DI)             │  ← Dependency Injection
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Services Layer (Business Logic)       │
│  • AuthService                          │
│  • HRService                            │
│  • NotificationService                  │
│  • ReportService                        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Repositories (Data Access)            │
│  • HolidayRepository                    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Models (Pydantic)                     │
│  • WorkdayRegistration                  │
│  • WeeklyReport                         │
│  • Settings                             │
└─────────────────────────────────────────┘
```

---

## 🤖 Comandos del Bot

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/start` | Inicializar el bot y mostrar bienvenida | `/start` |
| `/help` | Mostrar lista de comandos disponibles | `/help` |
| `/dia` | Registrar jornada para un día específico | `/dia` → `HOY` / `AYER` / `20241207` |
| `/info` | Ver registro de la semana actual | `/info` |
| `/infop` | Ver registro de la semana pasada | `/infop` |
| `/version` | Mostrar información de versión | `/version` |

### Flujo de Registro de Jornada

```
Usuario: /dia
Bot: ¿Qué día quieres registrar? HOY, AYER o YYYYMMDD

Usuario: HOY
Bot: [Valida si es festivo/vacación/teletrabajo]

Si requiere confirmación:
Bot: ¿Es día de teletrabajo ocasional? Y/N
Usuario: Y
Bot: ✅ Jornada registrada de 8:00 a 18:00
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)

**🔐 IMPORTANTE:** Todas las credenciales deben estar encriptadas

```env
# Clave de encriptación (generada por scripts/encrypt_secrets.py)
ENCRYPTION_KEY=gAAAAABl...

# Configuración del Bot de Telegram (encriptado)
BOT_TOKEN_ENCRYPTED=gAAAAABl...
CHAT_ID_ENCRYPTED=gAAAAABl...

# Credenciales del Sistema ViveOrange (encriptado)
HR_USERNAME_ENCRYPTED=gAAAAABl...
HR_PASSWORD_ENCRYPTED=gAAAAABl...
EMPLOYEE_CODE_ENCRYPTED=gAAAAABl...
```

Ver [.env.example](.env.example) para más detalles.

### Festivos y Días No Laborables (data/holidays.json)

**🆕 Fase 2:** Los festivos ahora se gestionan mediante un archivo JSON estructurado.

El archivo `data/holidays.json` contiene:
- **Festivos nacionales** de España (2024-2025)
- **Festivos regionales** por comunidad autónoma:
  - Madrid
  - Valencia
  - Cataluña
  - Andalucía
  - País Vasco
  - Galicia
- **Metadatos** (última actualización, notas)

**Estructura del archivo:**
```json
{
  "national": [
    {
      "date": "2025-01-01",
      "name": "Año Nuevo",
      "description": "Primer día del año"
    }
  ],
  "regional": {
    "madrid": [
      {
        "date": "2025-05-02",
        "name": "Fiesta de la Comunidad de Madrid",
        "description": "Dos de Mayo"
      }
    ]
  }
}
```

**Ventajas de este approach:**
- ✅ Fácil actualización anual sin modificar código
- ✅ Soporte multi-regional
- ✅ Versionable en Git
- ✅ Lectura eficiente con LRU cache (HolidayRepository)

**Actualizar festivos:**
1. Editar `data/holidays.json` con los nuevos festivos del año
2. Mantener formato JSON válido
3. Actualizar campo `last_updated`
4. El bot recargará automáticamente los cambios

### Configuración de Horarios (configD.py) ⚠️ Legacy

```python
# Horarios de trabajo
hinicio = "8:00"
hfin = "18:00"

# Días de teletrabajo (1=Lunes, 2=Martes, etc.)
diasTeletrabajo = [1, 2]  # Lunes y Martes

# Festivos nacionales
festivosAnuales = ["01/01", "06/01", "01/05", ...]

# Vacaciones personales
festivosOtros = ["17/04/2023", "18/04/2023", ...]
```

---

## 🔒 Seguridad (Fase 1 Completada)

### Mejoras Implementadas

✅ **Credenciales Encriptadas**
- Encriptación Fernet (cryptography)
- Script interactivo de encriptación
- Gestión segura con `SecretsManager`

✅ **Logs Sanitizados**
- Redacción automática de información sensible
- Rotación de archivos (10MB, 5 backups)
- `SanitizedFormatter` personalizado

✅ **Validación de Entradas**
- 7 métodos de validación implementados
- Protección contra inyección XSS
- Sanitización de strings

✅ **Prevención de Inyección**
- Eliminada concatenación de JSON
- Serialización segura con `json.dumps()`
- Validación de tipos de datos

✅ **Dependencias Actualizadas**
- CVE-2023-32681 eliminado (requests 2.32.3)
- Todas las dependencias en últimas versiones

### Generar Credenciales Encriptadas

```bash
# Ejecutar script interactivo
python scripts/encrypt_secrets.py

# Seguir instrucciones en pantalla
# Copiar output al archivo .env
```

Ver [docs/fases/FASE1_SEGURIDAD.md](docs/fases/FASE1_SEGURIDAD.md) para más detalles.

---

## 🏗️ Arquitectura de Servicios (Fases 2 & 3 Completadas)

### Dependency Injection Container

El proyecto utiliza un **ServiceContainer** singleton para gestión centralizada de servicios:

```python
from core import get_container

# Obtener container (singleton global)
container = get_container()

# Acceder a servicios (lazy initialization)
notification = container.notification_service
auth = container.auth_service
hr = container.hr_service
report = container.report_service
error_handler = container.error_handler
```

### Servicios Implementados

#### 1. NotificationService

**Propósito:** Gestión centralizada de notificaciones Telegram con rate limiting y retry logic

**Características:**
- ✅ Rate limiting (20 mensajes/minuto)
- ✅ Retry automático con backoff exponencial (3 intentos)
- ✅ Plantillas de mensajes (success, error, warning, info)
- ✅ Fallback a logging si Telegram falla
- ✅ Mensajes especializados (confirmación de jornada, informes)

**Uso:**
```python
# Enviar mensaje básico
container.notification_service.send_message("Hola", chat_id=123456)

# Mensajes templados
container.notification_service.send_success("Operación completada", chat_id=123456)
container.notification_service.send_error(exception, chat_id=123456)
container.notification_service.send_warning("Advertencia", chat_id=123456)

# Mensajes especializados
container.notification_service.send_workday_confirmation(registration)
container.notification_service.send_weekly_report(report)
```

#### 2. ErrorHandler

**Propósito:** Manejo centralizado de errores con mensajes user-friendly en español

**Características:**
- ✅ Convierte excepciones técnicas a mensajes comprensibles
- ✅ Logging automático con contexto
- ✅ Mapeo específico por tipo de excepción
- ✅ Emojis descriptivos (❌ error, ⚠️ warning, 🔐 auth)

**Uso:**
```python
try:
    # Operación que puede fallar
    hr_service.register_workday(date)
except RegistroJornadaException as e:
    # Convertir excepción técnica a mensaje user-friendly
    user_msg = container.error_handler.handle_exception(e, {
        'user': username,
        'command': '/dia',
        'date': date
    })
    container.notification_service.send_message(user_msg, chat_id=chat_id)
```

#### 3. ReportService

**Propósito:** Generación de informes avanzados y análisis estadístico

**Características:**
- ✅ Informes semanales y mensuales
- ✅ Estadísticas por tipo de jornada, ubicación, día de semana
- ✅ Análisis de patrones temporales (hora inicio/fin promedio)
- ✅ Exportación a JSON con estadísticas
- ✅ Formateo mejorado para Telegram

**Uso:**
```python
# Generar resumen semanal
summary = container.report_service.generate_weekly_summary(report)

# Calcular estadísticas
stats = container.report_service.calculate_statistics(registrations)
# stats contiene:
# - total_hours, total_days
# - by_type (presencial, teletrabajo, etc.)
# - by_location
# - by_day_of_week
# - time_patterns (earliest_start, latest_end, avg hours/day)

# Exportar a JSON
json_report = container.report_service.export_to_json(report, include_statistics=True)

# Formatear para Telegram
telegram_msg = container.report_service.format_for_telegram(report, include_details=True)
```

#### 4. AuthService

**Propósito:** Autenticación en sistema ViveOrange con manejo de sesión

**Características:**
- ✅ Login multi-paso con OAM
- ✅ Gestión de cookies y sesión
- ✅ Excepciones específicas (InvalidCredentialsError, OAMRedirectError, SessionExpiredError)
- ✅ Logging detallado de cada paso

#### 5. HRService

**Propósito:** Registro de jornadas y generación de informes desde ViveOrange

**Características:**
- ✅ Registro de jornada con validación Pydantic
- ✅ Generación de informes semanales (actual y anterior)
- ✅ Parsing robusto de HTML
- ✅ Excepciones específicas (RegistrationError, HTMLParsingError, ReportGenerationError)

### Jerarquía de Excepciones

El proyecto define **22 excepciones personalizadas** organizadas por categoría:

**Base:**
- `RegistroJornadaException` - Excepción base con message y details

**Autenticación:**
- `AuthenticationError`, `InvalidCredentialsError`, `OAMRedirectError`, `SessionExpiredError`

**Servicios HR:**
- `HRServiceError`, `RegistrationError`, `ReportGenerationError`, `HTMLParsingError`

**Validación:**
- `ValidationError`, `InvalidDateError`, `InvalidTimeFormatError`, `HolidayValidationError`, `WeekendValidationError`

**Red:**
- `NetworkError`, `ConnectionTimeoutError`, `ServiceUnavailableError`, `HTTPError`

**Configuración:**
- `ConfigurationError`, `MissingConfigurationError`, `InvalidConfigurationError`

**Notificaciones:**
- `NotificationError`, `TelegramSendError`

Ver [docs/fases/FASE3_SERVICIOS.md](docs/fases/FASE3_SERVICIOS.md) para documentación completa.

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Descubrimiento automático de tests
python -m unittest discover -s tests -v

# Test específico
python -m unittest tests.test_dias_validator -v
```

### Con Coverage (opcional)

```bash
# Instalar pytest y coverage
pip install pytest pytest-cov

# Ejecutar con coverage
pytest tests/ --cov=app --cov-report=html

# Ver reporte
open htmlcov/index.html  # Linux/Mac
start htmlcov/index.html  # Windows
```

**Nota:** Se utiliza el decorador `@patch` para simular respuestas HTTP y asegurar independencia de conexiones externas.

---

## 🐳 Docker

### Build y Run

```bash
# Build
docker-compose build

# Run en background
docker-compose up -d

# Ver logs
docker-compose logs -f bot

# Stop
docker-compose down
```

### Configuración Docker

El contenedor usa:
- **Imagen base:** Python 3.10-slim
- **Usuario:** appuser (no-root)
- **Directorio de trabajo:** /app
- **Variables de entorno:** Desde .env
- **Volúmenes:** ./logs:/app/logs

Ver [Dockerfile](Dockerfile) y [docker-compose.yml](docker-compose.yml) para detalles.

---

## 📊 Dependencias

### Core Dependencies

```txt
beautifulsoup4==4.12.3      # Parsing HTML
lxml==5.3.0                 # Procesamiento XML/HTML
pyTelegramBotAPI==4.21.0    # API de Telegram
python-dotenv==1.0.1        # Variables de entorno
requests==2.32.3            # Cliente HTTP (sin CVE)
pydantic==2.10.3            # 🆕 Validación de datos y settings (Fase 2)
pydantic-settings==2.6.1    # 🆕 Gestión de configuración type-safe (Fase 2)
```

### Security Dependencies

```txt
cryptography==42.0.5        # Encriptación Fernet (Fase 1)
```

### Development Dependencies (opcional)

```bash
pip install pytest pytest-cov pytest-mock
pip install flake8 black mypy
```

---

## 📝 Logs

### Ubicación

- **Principal:** `logs/registrojornada.log`
- **ViveOrange:** `logs/vive_orange.log`

### Características

- ✅ **Sanitización automática** de información sensible
- ✅ **Rotación automática** (10MB por archivo, 5 backups)
- ✅ **Formato estructurado** con timestamp
- ✅ **Encoding UTF-8**

### Ver Logs

```bash
# Ver últimas 50 líneas
tail -n 50 logs/registrojornada.log

# Seguir en tiempo real
tail -f logs/registrojornada.log

# Buscar errores
grep "ERROR" logs/registrojornada.log
```

### Ejemplo de Log Sanitizado

```
2024-12-07 10:30:00 - registrojornada - INFO - User login successful
2024-12-07 10:30:01 - registrojornada - DEBUG - password=*** (redactado)
2024-12-07 10:30:02 - registrojornada - DEBUG - JSESSIONID=*** (redactado)
```

---

## 🔧 Troubleshooting

### Problema: "ENCRYPTION_KEY not found"

**Solución:**
```bash
python scripts/encrypt_secrets.py
# Copiar ENCRYPTION_KEY generada al .env
```

### Problema: "Invalid ENCRYPTION_KEY"

**Causa:** Clave corrupta o valores encriptados con otra clave

**Solución:**
```bash
# Re-encriptar todos los secretos
python scripts/encrypt_secrets.py
```

### Problema: Bot no responde

**Checklist:**
1. ✅ Verificar token de Telegram válido
2. ✅ Verificar chat_id correcto
3. ✅ Comprobar credenciales ViveOrange
4. ✅ Revisar conexión a internet
5. ✅ Consultar logs: `tail -f logs/registrojornada.log`

### Problema: Error de autenticación en ViveOrange

**Solución:**
1. Verificar credenciales correctas
2. Cambiar contraseña en portal ViveOrange si es necesario
3. Re-encriptar credenciales
4. Reiniciar bot

---

## 📚 Documentación Adicional

### Documentos del Proyecto

- **[ANALISIS_PROYECTO.md](ANALISIS_PROYECTO.md)** (54KB)
  - Análisis completo del proyecto
  - Problemas identificados
  - Roadmap de 4 fases
  - Propuestas de mejora detalladas

- **[docs/fases/FASE1_SEGURIDAD.md](docs/fases/FASE1_SEGURIDAD.md)** ✅ Completada
  - Implementación técnica de seguridad
  - Uso de SecretsManager y encriptación Fernet
  - Uso de SanitizedFormatter para logs
  - Validación de entradas con InputValidator
  - Guías de troubleshooting

- **[docs/fases/FASE2_REFACTORIZACION.md](docs/fases/FASE2_REFACTORIZACION.md)** ✅ Completada
  - Arquitectura en capas (Models, Services, Repositories)
  - Implementación de Pydantic Settings
  - AuthService y HRService detallados
  - HolidayRepository con LRU cache
  - Modelos de datos Pydantic

- **[docs/fases/FASE3_SERVICIOS.md](docs/fases/FASE3_SERVICIOS.md)** ✅ Completada
  - ServiceContainer y Dependency Injection
  - NotificationService con rate limiting y retry
  - ReportService con análisis estadístico
  - ErrorHandler centralizado
  - Jerarquía de 22 excepciones personalizadas
  - Ejemplos de uso de cada servicio

- **[.env.example](.env.example)**
  - Template de configuración
  - Instrucciones de uso
  - Notas de seguridad

### Recursos Externos

- [Python Telegram Bot API](https://github.com/eternnoir/pyTelegramBotAPI)
- [Cryptography (Fernet)](https://cryptography.io/en/latest/fernet/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Docker Documentation](https://docs.docker.com/)

---

## 🗺️ Roadmap

### ✅ Fase 1: Seguridad (Completada)
- [x] Gestión segura de credenciales con Fernet
- [x] Sanitización de logs
- [x] Validación de entradas contra XSS e inyección
- [x] Actualización de dependencias (CVE resueltos)
- [x] Prevención de inyección

**Documentación:** [docs/fases/FASE1_SEGURIDAD.md](docs/fases/FASE1_SEGURIDAD.md)

### ✅ Fase 2: Refactorización Arquitectónica (Completada)
- [x] Eliminar código duplicado
- [x] Reestructurar en capas (Models, Services, Repositories)
- [x] Implementar Pydantic Settings para configuración type-safe
- [x] Migrar festivos a JSON con HolidayRepository
- [x] Separar ViveOrange en AuthService y HRService
- [x] Crear modelos Pydantic (WorkdayRegistration, WeeklyReport)
- [x] Implementar Repository pattern con LRU cache

**Documentación:** [docs/fases/FASE2_REFACTORIZACION.md](docs/fases/FASE2_REFACTORIZACION.md)

### ✅ Fase 3: Service Layer Completa (Completada)
- [x] Crear ServiceContainer para Dependency Injection
- [x] Implementar NotificationService con rate limiting
- [x] Implementar ReportService con análisis estadístico
- [x] Implementar ErrorHandler centralizado
- [x] Crear jerarquía de 22 excepciones personalizadas
- [x] Refactorizar AuthService con excepciones
- [x] Refactorizar HRService con validación Pydantic
- [x] Refactorizar bot.py con ServiceContainer

**Documentación:** [docs/fases/FASE3_SERVICIOS.md](docs/fases/FASE3_SERVICIOS.md)

### 🎯 Fase 4: Testing y CI/CD (Próxima)
- [ ] Tests unitarios completos (>80% coverage)
- [ ] Tests de integración para servicios
- [ ] GitHub Actions CI/CD pipeline
- [ ] Dockerfile multi-stage para optimización
- [ ] Automatización de deployment
- [ ] Pre-commit hooks
- [ ] Code coverage reports

Ver [ANALISIS_PROYECTO.md](ANALISIS_PROYECTO.md) para detalles completos.

---

## 🤝 Contribuir

### Flujo de Trabajo

1. Fork del proyecto
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abrir Pull Request

### Estándares de Código

- Seguir PEP 8
- Documentar funciones con docstrings
- Añadir tests para nuevas funcionalidades
- Mantener cobertura >80%

### Seguridad

- ❌ NUNCA commitear archivo `.env`
- ✅ Usar siempre credenciales encriptadas
- ✅ Validar todas las entradas de usuario
- ✅ Sanitizar logs con información sensible

---

## ⚠️ Notas Importantes

### Seguridad

1. **El archivo .env NO debe versionarse** - Verificar que está en .gitignore
2. **Guardar ENCRYPTION_KEY en gestor de contraseñas** - Si se pierde, hay que re-encriptar todo
3. **Rotar credenciales periódicamente** - Usar `scripts/encrypt_secrets.py`
4. **Revisar logs periódicamente** - Buscar comportamientos anómalos

### Mantenimiento

1. **Actualizar festivos anualmente** - Editar `configD.py`
2. **Actualizar vacaciones personales** - Editar `festivosOtros` en `configD.py`
3. **Revisar logs rotados** - Limpiar archivos antiguos si es necesario
4. **Actualizar dependencias** - Ejecutar `pip list --outdated`

### Limitaciones Conocidas

- Fechas de vacaciones hardcodeadas en código (se resolverá en Fase 2)
- Configuración duplicada en `configDD.py` (se eliminará en Fase 2)
- Tests con cobertura ~30% (se mejorará en Fase 4)

---

## 📄 Licencia

Este proyecto es de **uso interno** para empleados de Orange España.

Todos los derechos reservados © 2023-2024 Orange España

---

## 👥 Autores y Contacto

- **Desarrollador:** Equipo de Desarrollo Interno
- **Mantenedor:** [Contacto interno]
- **Issues:** Reportar en repositorio interno

### Soporte

Para obtener ayuda:
1. Consultar documentación en este README
2. Revisar [docs/fases/FASE1_SEGURIDAD.md](docs/fases/FASE1_SEGURIDAD.md)
3. Verificar logs en `logs/`
4. Contactar al equipo de desarrollo

---

## 📈 Estado del Proyecto

```
Version: 4.0 (Post Fase 4)
Estado: 🟢 PRODUCTION-READY (Testing & CI/CD Completo)
Última actualización: 2025-12-08

Fases completadas: 4/4 (100%)
Tests: 88 unitarios (100% passing)
Cobertura: >85%
CI/CD: ✅ GitHub Actions
Vulnerabilidades: 0
Nivel de seguridad: ALTO
Arquitectura: Enterprise-grade
```

### Métricas

| Métrica | Valor |
|---------|-------|
| Líneas de código | ~8,500 |
| Archivos Python | 35+ |
| Servicios | 5 (Auth, HR, Notification, Report, Error) |
| Modelos Pydantic | 3 (Settings, WorkdayRegistration, WeeklyReport) |
| Excepciones personalizadas | 22 |
| Repositorios | 1 (HolidayRepository) |
| Tests | 88 unitarios (100% passing) |
| Coverage | >85% |
| Documentación | ~250KB (4 fases + roadmap) |
| Dependencias | 7 core + 10 dev |

---

## 📚 Documentación Completa

Este README proporciona una visión general. Para documentación detallada, ver:

### 📖 Índice de Documentación

**Directorio principal**: [`docs/`](docs/)

**Documentos de Fases**:
- 📄 [Fase 1: Seguridad y Logging](docs/fases/FASE1_SEGURIDAD.md) - SecretsManager, logging sanitizado
- 📄 [Fase 2: Refactorización Arquitectónica](docs/fases/FASE2_REFACTORIZACION.md) - Servicios, modelos, repositorios
- 📄 [Fase 3: Capa de Servicios Completa](docs/fases/FASE3_SERVICIOS.md) - NotificationService, excepciones
- 📄 [Fase 4: Testing y CI/CD](docs/fases/FASE4_TESTING.md) - 88 tests, GitHub Actions, coverage

**Documentos de Planificación**:
- 🔍 [Análisis del Proyecto](docs/ANALISIS_PROYECTO.md) - Análisis técnico completo del código legacy
- 🗺️ [Próximos Pasos](docs/NEXT_STEPS.md) - Roadmap de Fases 5-8 con estimaciones

**Guías por Perfil**:

<details>
<summary><b>👨‍💻 Para Desarrolladores</b></summary>

1. Leer [Inicio Rápido](#-inicio-rápido) en este README
2. Revisar [Fase 4: Testing](docs/fases/FASE4_TESTING.md) para setup de desarrollo
3. Ver [Próximos Pasos](docs/NEXT_STEPS.md) para tareas disponibles
4. Ejecutar tests: `pytest`
5. Instalar pre-commit hooks: `pre-commit install`

**Tiempo: 15-20 minutos**
</details>

<details>
<summary><b>🏗️ Para Arquitectos</b></summary>

1. Leer [Análisis del Proyecto](docs/ANALISIS_PROYECTO.md)
2. Revisar [Fase 2: Arquitectura](docs/fases/FASE2_REFACTORIZACION.md)
3. Estudiar [Fase 3: Servicios](docs/fases/FASE3_SERVICIOS.md)
4. Evaluar [Próximos Pasos](docs/NEXT_STEPS.md) para decisiones arquitectónicas

**Tiempo: 45-60 minutos**
</details>

<details>
<summary><b>📊 Para Product Owners</b></summary>

1. Ver [Estado del Proyecto](#-estado-del-proyecto)
2. Revisar [Próximos Pasos](docs/NEXT_STEPS.md) - Fases 5-8
3. Evaluar roadmap y prioridades
4. Revisar métricas de calidad

**Tiempo: 20-30 minutos**
</details>

---

## ✅ Checklist Pre-Producción

Antes de desplegar:

- [ ] Ejecutar `python scripts/encrypt_secrets.py`
- [ ] Verificar `.env` con credenciales encriptadas
- [ ] Eliminar variables sin encriptar del `.env`
- [ ] Verificar `.env` en `.gitignore`
- [ ] Ejecutar tests: `python -m unittest discover -s tests -v`
- [ ] Probar bot en local
- [ ] Verificar logs se sanitizan
- [ ] Guardar `ENCRYPTION_KEY` en gestor de contraseñas
- [ ] Configurar monitoreo de logs
- [ ] Establecer proceso de rotación de credenciales
- [ ] Revisar configuración de festivos
- [ ] Actualizar vacaciones personales

---

## 🎓 Aprendizajes y Mejores Prácticas

### Fase 1: Seguridad

- ✅ **Principio de mínimo privilegio** - Credenciales encriptadas
- ✅ **Defense in depth** - Múltiples capas de seguridad
- ✅ **Secure by default** - Sanitización automática
- ✅ **Fail securely** - Validación con excepciones claras
- ✅ **Don't trust input** - Validación exhaustiva

### Fase 2: Arquitectura

- ✅ **Separation of Concerns** - Capas bien definidas (Models, Services, Repos)
- ✅ **Single Responsibility** - Cada servicio con una responsabilidad clara
- ✅ **Type Safety** - Pydantic para validación en tiempo de ejecución
- ✅ **DRY (Don't Repeat Yourself)** - Código reutilizable en servicios
- ✅ **Repository Pattern** - Abstracción de acceso a datos

### Fase 3: Servicios

- ✅ **Dependency Injection** - ServiceContainer para gestión centralizada
- ✅ **Error Handling** - Excepciones personalizadas y mensajes user-friendly
- ✅ **Rate Limiting** - Prevención de abuse en NotificationService
- ✅ **Retry Logic** - Resiliencia con backoff exponencial
- ✅ **Observability** - Logging estructurado con contexto
- ✅ **Graceful Degradation** - Fallbacks cuando servicios externos fallan

### Recomendaciones

1. Revisar logs diariamente
2. Actualizar dependencias mensualmente
3. Rotar credenciales trimestralmente
4. Hacer backup de `ENCRYPTION_KEY`
5. Mantener documentación actualizada
6. Usar ServiceContainer en toda la aplicación
7. Capturar excepciones específicas, no genéricas
8. Validar datos con Pydantic antes de procesarlos

---

**Última actualización:** 2025-12-08
**Versión:** 4.0 (Post Fase 3)
**Estado:** 🟢 Enterprise-grade Architecture - Production-Ready
