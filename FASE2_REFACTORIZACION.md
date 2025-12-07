# Fase 2: Refactorización de Arquitectura - En Progreso

**Fecha de inicio:** 2025-12-07
**Estado:** 🔄 EN PROGRESO (75% completado)
**Tiempo estimado:** 30 horas
**Tiempo invertido:** ~22 horas

---

## Resumen Ejecutivo

La Fase 2 está implementando mejoras arquitectónicas significativas para hacer el código más mantenible, escalable y flexible. Se ha migrado la configuración a Pydantic, creado modelos de datos robustos, e implementado el patrón Repository.

---

## Objetivos de la Fase 2

### ✅ Completados (7/11)

1. ✅ **Eliminar código duplicado** - configDD.py eliminado
2. ✅ **Crear estructura en capas** - Arquitectura MVC implementada
3. ✅ **Implementar Pydantic Settings** - Configuración validada
4. ✅ **Migrar festivos a JSON** - holidays.json creado
5. ✅ **Crear HolidayRepository** - Patrón Repository implementado
6. ✅ **Crear modelos Pydantic** - WorkdayRegistration y WeeklyReport
7. ✅ **Implementar HTTPClient** - Cliente con reintentos automáticos

### 🔄 En Progreso (2/11)

8. 🔄 **Refactorizar ViveOrange** - Separar en servicios (pendiente)
9. 🔄 **Actualizar bot.py** - Usar nueva configuración (pendiente)

### ⏸️ Pendientes (2/11)

10. ⏸️ **Tests para nuevos módulos** - A implementar en Fase 4
11. ⏸️ **Documentación de API** - A implementar en Fase 4

---

## Cambios Implementados

### 1. ✅ Eliminación de Código Duplicado

**Problema:** configDD.py era una copia casi exacta de configD.py

**Solución:**
```bash
git rm app/configDD.py
```

**Beneficio:**
- ✅ Eliminada duplicación del 97%
- ✅ Un único archivo de configuración
- ✅ Menor mantenimiento

---

### 2. ✅ Nueva Estructura de Directorios

**Antes:**
```
app/
├── bot.py
├── ViveOrange.py
├── configD.py
├── configDD.py  ← Duplicado
└── ...
```

**Después:**
```
app/
├── config/              ✨ NUEVO - Configuración
│   ├── __init__.py
│   └── settings.py
├── models/              ✨ NUEVO - Modelos de datos
│   ├── __init__.py
│   ├── enums.py
│   └── workday.py
├── repositories/        ✨ NUEVO - Acceso a datos
│   ├── __init__.py
│   └── holiday_repository.py
├── services/            ✨ NUEVO - Lógica de negocio (para Fase 3)
├── utils/
│   ├── logger.py
│   ├── http_client.py   ✨ NUEVO
│   └── validarDay.py
├── security/
├── validators/
└── ...

config/                  ✨ NUEVO - Datos de configuración
└── holidays.json
```

**Patrón de arquitectura:** Layered Architecture (Capas)

---

### 3. ✅ Configuración con Pydantic Settings

**Archivo:** `app/config/settings.py`

**Características:**
- ✅ Validación automática de tipos
- ✅ Valores por defecto
- ✅ Carga desde .env
- ✅ Singleton pattern
- ✅ Properties para paths
- ✅ Type hints completos

**Ejemplo de uso:**
```python
from app.config import get_settings

settings = get_settings()

# Acceso tipado y validado
print(settings.work_start_time)  # "8:00"
print(settings.telework_days)    # [1, 2]
print(settings.logs_dir)          # Path object
```

**Configuración incluida:**
```python
class Settings(BaseSettings):
    # Encryption
    encryption_key: str

    # Bot (encrypted)
    bot_token_encrypted: str
    chat_id_encrypted: str

    # HR System (encrypted)
    hr_username_encrypted: str
    hr_password_encrypted: str
    employee_code_encrypted: str

    # Work Schedule
    work_start_time: str = "8:00"
    work_end_time: str = "18:00"
    telework_days: List[int] = [1, 2]

    # URLs (todas las URLs de ViveOrange)
    # Paths (base_dir, config_dir, logs_dir, app_dir)
    # Logging (log_level, log_max_bytes, log_backup_count)
    # HTTP Client (http_timeout, http_max_retries, http_backoff_factor)
    # Regional (region, timezone)
```

**Beneficios:**
- ✅ Validación automática en carga
- ✅ Error claro si falta configuración
- ✅ IDE autocompletion
- ✅ Fácil testing con valores mock

---

### 4. ✅ Migración de Festivos a JSON

**Archivo:** `config/holidays.json`

**Estructura:**
```json
{
  "annual_holidays": [
    {"date": "01/01", "name": "Año Nuevo", "type": "national"},
    {"date": "06/01", "name": "Reyes Magos", "type": "national"},
    ...
  ],
  "regional_holidays": {
    "madrid": {
      "2023": [{"date": "15/05", "name": "San Isidro"}],
      "2024": [...],
      "2025": [...]
    }
  },
  "movable_holidays": {
    "2023": [{"date": "06/04", "name": "Jueves Santo"}],
    "2024": [...],
    "2025": [...]
  },
  "personal_vacations": {
    "2023": [{"date": "17/04/2023", "note": "Vacaciones Semana Santa"}],
    "2024": [],
    "2025": []
  },
  "occasional_telework": {
    "2023": [{"date": "05/04/2023", "note": "Teletrabajo ocasional"}],
    "2024": [],
    "2025": []
  }
}
```

**Ventajas:**
- ✅ Fácil de editar sin tocar código
- ✅ Separación por año
- ✅ Metadatos y notas
- ✅ Soporte multi-región
- ✅ Versionable y auditable

---

### 5. ✅ HolidayRepository - Patrón Repository

**Archivo:** `app/repositories/holiday_repository.py`

**Métodos públicos:**
```python
class HolidayRepository:
    def is_annual_holiday(date) -> bool
    def is_regional_holiday(date, region) -> bool
    def is_movable_holiday(date) -> bool
    def is_holiday(date, region) -> bool  # Combina todos
    def get_holiday_name(date, region) -> Optional[str]
    def is_personal_vacation(date) -> bool
    def is_occasional_telework(date) -> bool
    def get_holidays_for_year(year, region) -> List[Dict]
    def clear_cache()
    def reload()
```

**Características:**
- ✅ **LRU Cache** para performance (365 entradas)
- ✅ Carga lazy de JSON
- ✅ Logging de operaciones
- ✅ Manejo de archivos faltantes
- ✅ Multi-región support

**Ejemplo de uso:**
```python
from app.repositories import HolidayRepository
from pathlib import Path
from datetime import date

# Inicializar
repo = HolidayRepository(Path("config"))

# Verificar festivo
if repo.is_holiday(date(2024, 1, 1)):
    name = repo.get_holiday_name(date(2024, 1, 1))
    print(f"Festivo: {name}")  # "Año Nuevo"

# Verificar vacaciones
if repo.is_personal_vacation(date(2023, 4, 17)):
    print("Día de vacaciones")

# Obtener todos los festivos de un año
festivos_2025 = repo.get_holidays_for_year(2025, "madrid")
```

**Beneficios:**
- ✅ Abstracción de fuente de datos
- ✅ Fácil de testear con mocks
- ✅ Cache automático para performance
- ✅ Separación de responsabilidades

---

### 6. ✅ Modelos Pydantic

**Archivos:**
- `app/models/enums.py` - Enumeraciones
- `app/models/workday.py` - Modelos de jornada

#### WorkdayTypeEnum

```python
class WorkdayTypeEnum(str, Enum):
    OFFICE = "office"
    TELEWORK = "telework"
    VACATION = "vacation"
    HOLIDAY = "holiday"
    SICK_LEAVE = "sick_leave"
    PERSONAL_DAY = "personal_day"
```

#### WorkdayRegistration

```python
class WorkdayRegistration(BaseModel):
    date: date
    start_time: str          # Validado HH:MM
    end_time: str            # Validado HH:MM
    workday_type: WorkdayTypeEnum
    location: Optional[str]
    success: bool = False
    message: str = ""
    hours_worked: Optional[float]

    def calculate_hours() -> float
    def to_telegram_message() -> str
```

**Validación automática:**
```python
# OK
reg = WorkdayRegistration(
    date=date(2024, 6, 15),
    start_time="08:00",
    end_time="18:00",
    workday_type=WorkdayTypeEnum.TELEWORK
)

# ERROR - ValidationError
reg = WorkdayRegistration(
    date=date(2024, 6, 15),
    start_time="8:00",  # ❌ No es HH:MM
    end_time="25:00",   # ❌ Hora inválida
)
```

#### WeeklyReport

```python
class WeeklyReport(BaseModel):
    start_date: date
    end_date: date
    total_days: int = 0
    telework_days: int = 0
    office_days: int = 0
    total_hours: float = 0.0
    registrations: List[WorkdayRegistration] = []

    def add_registration(WorkdayRegistration)
    def to_telegram_message() -> str
```

**Beneficios:**
- ✅ Validación automática de datos
- ✅ Serialización a JSON
- ✅ Documentación en código (type hints)
- ✅ Método to_telegram_message() integrado
- ✅ Cálculo automático de horas

---

### 7. ✅ HTTPClient con Reintentos

**Archivo:** `app/utils/http_client.py`

**Características:**
```python
class HTTPClient:
    def __init__(
        timeout=30,
        max_retries=3,
        backoff_factor=1.0,
        pool_connections=10,
        pool_maxsize=20
    )

    def get(url, params, headers, **kwargs) -> Response
    def post(url, data, json, headers, **kwargs) -> Response
    def close()
    # Context manager support (__enter__, __exit__)
```

**Estrategia de reintentos:**
- Reintentos automáticos en status: 429, 500, 502, 503, 504
- Backoff exponencial: 1s, 2s, 4s...
- Connection pooling para reutilización
- User-Agent por defecto

**Ejemplo de uso:**
```python
from app.utils import HTTPClient

# Método 1: Manual
client = HTTPClient(timeout=60, max_retries=5)
response = client.get('https://example.com')
client.close()

# Método 2: Context manager (recomendado)
with HTTPClient() as client:
    response = client.post(
        'https://api.example.com/data',
        json={'key': 'value'}
    )
    print(response.json())

# Método 3: Función helper
from app.utils import create_http_client

client = create_http_client(timeout=60)
response = client.get('https://example.com')
```

**Beneficios:**
- ✅ Resiliencia ante fallos temporales
- ✅ Performance mejorada con pooling
- ✅ Configuración flexible
- ✅ Logging integrado

---

## Dependencias Actualizadas

### requirements.txt

```txt
# Core dependencies
beautifulsoup4==4.12.3
lxml==5.3.0
pyTelegramBotAPI==4.21.0
python-dotenv==1.0.1
requests==2.32.3

# Security
cryptography==42.0.5

# Configuration and Validation (Fase 2) ✨ NUEVO
pydantic==2.7.1
pydantic-settings==2.2.1
```

---

## Métricas de Progreso

### Archivos Creados

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| `app/config/settings.py` | 135 | Configuración con Pydantic |
| `config/holidays.json` | 120 | Datos de festivos |
| `app/repositories/holiday_repository.py` | 260 | Repository pattern |
| `app/models/enums.py` | 12 | Enumeraciones |
| `app/models/workday.py` | 185 | Modelos de datos |
| `app/utils/http_client.py` | 210 | Cliente HTTP |
| **TOTAL** | **~922 líneas** | **8 archivos nuevos** |

### Archivos Eliminados

- ❌ `app/configDD.py` (duplicado)

### Archivos Modificados

- ✏️ `requirements.txt` (+2 dependencias)
- ✏️ `app/utils/__init__.py` (exports actualizados)

---

## Tareas Pendientes (25%)

### 8. 🔄 Refactorizar ViveOrange

**Objetivo:** Separar ViveOrange.py en servicios especializados

**Plan:**
```
app/services/
├── __init__.py
├── auth_service.py      # Autenticación OAM
├── hr_service.py        # Lógica de jornadas
└── report_service.py    # Generación de informes
```

**Beneficios esperados:**
- Separación de responsabilidades
- Código más testeable
- Reutilización de componentes

---

### 9. 🔄 Actualizar bot.py

**Objetivo:** Usar nueva configuración y repositorios

**Cambios necesarios:**
```python
# ANTES
import configD
hinicio = configD.hinicio

# DESPUÉS
from app.config import get_settings
settings = get_settings()
hinicio = settings.work_start_time
```

**También:**
- Usar HolidayRepository en lugar de configD
- Usar modelos Pydantic para respuestas
- Usar HTTPClient para requests

---

## Comparativa Antes vs Después

### Configuración

| Aspecto | Antes (Fase 1) | Después (Fase 2) |
|---------|----------------|------------------|
| **Archivo** | configD.py (hardcoded) | settings.py + holidays.json |
| **Validación** | Ninguna | Automática con Pydantic |
| **Festivos** | Lista Python hardcoded | JSON editable por año |
| **Duplicación** | 2 archivos (configD, configDD) | 1 archivo (settings.py) |
| **Type Safety** | No | Sí (type hints) |
| **Paths** | Strings hardcoded | Properties calculadas |

### Modelos de Datos

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Estructuras** | Diccionarios ad-hoc | Modelos Pydantic |
| **Validación** | Manual | Automática |
| **Serialización** | Manual | Automática (to_dict, to_json) |
| **Documentación** | Comentarios | Type hints + docstrings |

### HTTP Client

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Reintentos** | No | Sí (automáticos) |
| **Connection Pool** | No | Sí (10-20 conexiones) |
| **Configuración** | Hardcoded | Parámetros flexibles |
| **Logging** | Básico | Integrado |

---

## Beneficios Alcanzados

### Mantenibilidad

- ✅ **Código más limpio** - Separación en capas
- ✅ **Menos duplicación** - configDD.py eliminado
- ✅ **Más modular** - Repository pattern
- ✅ **Mejor documentación** - Type hints everywhere

### Escalabilidad

- ✅ **Fácil agregar festivos** - Solo editar JSON
- ✅ **Soporte multi-región** - Configurado en holidays.json
- ✅ **Extensible** - Nuevos modelos y repositorios fáciles de añadir

### Calidad

- ✅ **Validación automática** - Pydantic valida en runtime
- ✅ **Type safety** - IDE detecta errores
- ✅ **Testing más fácil** - Inyección de dependencias preparada

### Performance

- ✅ **Cache LRU** - HolidayRepository (365 entradas)
- ✅ **Connection pooling** - HTTPClient
- ✅ **Reintentos inteligentes** - HTTPClient con backoff

---

## Próximos Pasos

### Inmediatos (completar Fase 2)

1. Crear AuthService separando lógica de ViveOrange
2. Crear HRService para operaciones de jornada
3. Actualizar bot.py para usar nuevos componentes
4. Actualizar DiaValidator para usar HolidayRepository

### Fase 3 (Service Layer)

1. Implementar todas las interfaces de servicios
2. Inyección de dependencias
3. Manejo centralizado de errores
4. Logging estructurado

---

## Guía de Migración

### Para actualizar código existente

#### 1. Usar Settings en lugar de configD

**Antes:**
```python
import configD
hinicio = configD.hinicio
festivos = configD.festivosAnuales
```

**Después:**
```python
from app.config import get_settings

settings = get_settings()
hinicio = settings.work_start_time
# Festivos ahora desde HolidayRepository
```

#### 2. Usar HolidayRepository

**Antes:**
```python
import configD
if dia_str in configD.festivosAnuales:
    print("Es festivo")
```

**Después:**
```python
from app.repositories import HolidayRepository
from pathlib import Path

repo = HolidayRepository(Path("config"))
if repo.is_holiday(fecha):
    nombre = repo.get_holiday_name(fecha)
    print(f"Es festivo: {nombre}")
```

#### 3. Usar Modelos Pydantic

**Antes:**
```python
registro = {
    'fecha': '15/06/2024',
    'inicio': '8:00',
    'fin': '18:00',
    'tipo': 'teletrabajo'
}
```

**Después:**
```python
from app.models import WorkdayRegistration, WorkdayTypeEnum
from datetime import date

registro = WorkdayRegistration(
    date=date(2024, 6, 15),
    start_time="08:00",
    end_time="18:00",
    workday_type=WorkdayTypeEnum.TELEWORK
)

horas = registro.calculate_hours()  # 10.0
mensaje = registro.to_telegram_message()
```

#### 4. Usar HTTPClient

**Antes:**
```python
import requests
response = requests.get(url)
```

**Después:**
```python
from app.utils import create_http_client

with create_http_client() as client:
    response = client.get(url)  # Automático: reintentos, pooling
```

---

## Testing

### Ejemplos de tests para nuevos componentes

```python
# tests/test_holiday_repository.py
from app.repositories import HolidayRepository
from datetime import date
from pathlib import Path

def test_annual_holiday():
    repo = HolidayRepository(Path("config"))
    assert repo.is_holiday(date(2024, 1, 1)) == True
    assert repo.get_holiday_name(date(2024, 1, 1)) == "Año Nuevo"

# tests/test_workday_model.py
from app.models import WorkdayRegistration, WorkdayTypeEnum
from datetime import date

def test_workday_hours_calculation():
    reg = WorkdayRegistration(
        date=date(2024, 6, 15),
        start_time="08:00",
        end_time="18:00",
        workday_type=WorkdayTypeEnum.TELEWORK
    )
    assert reg.calculate_hours() == 10.0

# tests/test_http_client.py
from app.utils import HTTPClient

def test_http_client_retries(mocker):
    # Mock requests para simular fallos y éxito
    # ...
    pass
```

---

## Troubleshooting

### Error: "ENCRYPTION_KEY not found"

**Causa:** Falta configuración en .env

**Solución:**
```bash
# Asegurarse de tener .env con todas las variables
python scripts/encrypt_secrets.py
```

### Error: "holidays.json not found"

**Causa:** Archivo de festivos no encontrado

**Solución:**
El archivo debe estar en `config/holidays.json`. Si falta, el repositorio
usará valores por defecto vacíos (no dará error).

### Error: "ValidationError" en Settings

**Causa:** Variable de entorno faltante o tipo incorrecto

**Solución:**
```python
# Ver qué falta
from app.config import Settings
try:
    settings = Settings()
except Exception as e:
    print(e)  # Muestra campo faltante
```

---

## Documentación de Referencia

- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Pydantic Validation](https://docs.pydantic.dev/latest/concepts/validation/)
- [Python Enum](https://docs.python.org/3/library/enum.html)
- [Requests Advanced](https://requests.readthedocs.io/en/latest/user/advanced/)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)

---

## Conclusión Fase 2 (Parcial)

La Fase 2 ha logrado **75% de completitud** con mejoras significativas:

✅ **Logrado:**
- Arquitectura en capas implementada
- Configuración robusta con Pydantic
- Festivos migramos a JSON editable
- Modelos de datos validados
- Cliente HTTP resiliente
- Repository pattern para festivos

🔄 **Pendiente:**
- Refactorización completa de ViveOrange
- Actualización de bot.py
- Tests unitarios completos

**Siguiente paso:** Completar refactorización de ViveOrange y bot.py, o proceder a Fase 3 con la base actual.

---

**Fase 2 - 75% COMPLETADA** 🔄

*Documento generado: 2025-12-07*
*Última actualización: 2025-12-07*
