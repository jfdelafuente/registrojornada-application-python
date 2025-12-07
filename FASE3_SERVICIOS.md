# Fase 3: Capa de Servicios Completa - En Progreso

**Fecha de inicio:** 2025-12-07
**Estado:** 🔄 EN PROGRESO (0% completado)
**Tiempo estimado:** 20 horas
**Tiempo invertido:** ~0 horas

---

## Resumen Ejecutivo

La Fase 3 completa la capa de servicios iniciada en Fase 2, agregando servicios especializados para notificaciones, reportes avanzados, y manejo centralizado de errores. También implementa inyección de dependencias y mejora la separación de responsabilidades.

---

## Objetivos de la Fase 3

### ✅ Completados (2/8)

1. ✅ **AuthService** - Ya implementado en Fase 2
2. ✅ **HRService** - Ya implementado en Fase 2

### 🔄 En Progreso (0/8)

3. ⏸️ **NotificationService** - Abstracción de notificaciones Telegram/Email
4. ⏸️ **ReportService** - Generación avanzada de informes
5. ⏸️ **Exception Hierarchy** - Jerarquía de excepciones personalizadas
6. ⏸️ **Error Handling** - Manejo centralizado de errores
7. ⏸️ **Dependency Injection** - Inyección de dependencias en servicios
8. ⏸️ **Service Integration** - Integración completa en bot.py

---

## Arquitectura de Servicios

### Diagrama de Capas

```
┌─────────────────────────────────────────────┐
│          Telegram Bot Interface             │
│              (bot.py)                       │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│         Service Layer (Business Logic)      │
├─────────────────────────────────────────────┤
│  • AuthService                              │
│  • HRService                                │
│  • NotificationService     ◄── NEW          │
│  • ReportService          ◄── NEW          │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│      Repository Layer (Data Access)         │
├─────────────────────────────────────────────┤
│  • HolidayRepository                        │
│  • ConfigRepository       ◄── NEW          │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│         Models & Validators                 │
├─────────────────────────────────────────────┤
│  • WorkdayRegistration                      │
│  • WeeklyReport                             │
│  • Custom Exceptions      ◄── NEW          │
└─────────────────────────────────────────────┘
```

---

## Servicios a Implementar

### 1. NotificationService

**Propósito:** Centralizar todas las notificaciones (Telegram, email, logs).

**Características:**
- Envío de mensajes Telegram con formato markdown
- Soporte para diferentes tipos de notificaciones (info, success, error, warning)
- Rate limiting para evitar spam
- Plantillas de mensajes reutilizables
- Fallback a logging si Telegram falla

**Archivo:** `app/services/notification_service.py`

**Interfaz propuesta:**
```python
class NotificationService:
    def send_telegram_message(message: str, parse_mode: str = "Markdown")
    def send_success_notification(title: str, details: str)
    def send_error_notification(error: Exception, context: dict)
    def send_workday_confirmation(registration: WorkdayRegistration)
    def send_weekly_report(report: WeeklyReport)
```

---

### 2. ReportService

**Propósito:** Generación avanzada de informes y estadísticas.

**Características:**
- Informes semanales/mensuales/anuales
- Estadísticas de horas trabajadas
- Análisis de patrones (teletrabajo vs oficina)
- Exportación a diferentes formatos (texto, JSON)
- Cálculo de métricas (promedio horas/día, días trabajados, etc.)

**Archivo:** `app/services/report_service.py`

**Interfaz propuesta:**
```python
class ReportService:
    def generate_weekly_report(start_date: date, end_date: date) -> WeeklyReport
    def generate_monthly_summary(year: int, month: int) -> MonthlySummary
    def calculate_statistics(registrations: List[WorkdayRegistration]) -> Statistics
    def export_to_json(report: WeeklyReport) -> str
    def format_for_telegram(report: WeeklyReport) -> str
```

---

### 3. Exception Hierarchy

**Propósito:** Jerarquía de excepciones personalizadas para manejo de errores específicos.

**Archivo:** `app/exceptions/__init__.py`

**Jerarquía propuesta:**
```python
# Base exception
class RegistroJornadaException(Exception):
    """Base exception for all application errors"""

# Authentication errors
class AuthenticationError(RegistroJornadaException):
    """Authentication failed"""

class InvalidCredentialsError(AuthenticationError):
    """Invalid username or password"""

class SessionExpiredError(AuthenticationError):
    """Session has expired"""

# HR Service errors
class HRServiceError(RegistroJornadaException):
    """HR service operation failed"""

class RegistrationError(HRServiceError):
    """Workday registration failed"""

class ReportGenerationError(HRServiceError):
    """Report generation failed"""

# Validation errors
class ValidationError(RegistroJornadaException):
    """Data validation failed"""

class InvalidDateError(ValidationError):
    """Invalid date provided"""

class InvalidTimeFormatError(ValidationError):
    """Invalid time format"""

# Network errors
class NetworkError(RegistroJornadaException):
    """Network operation failed"""

class ConnectionTimeoutError(NetworkError):
    """Connection timed out"""

class ServiceUnavailableError(NetworkError):
    """External service is unavailable"""
```

---

### 4. Error Handler

**Propósito:** Manejo centralizado de errores con logging y notificaciones.

**Archivo:** `app/utils/error_handler.py`

**Características:**
```python
class ErrorHandler:
    def __init__(notification_service: NotificationService):
        self.notification_service = notification_service

    def handle_exception(exc: Exception, context: dict) -> str:
        """
        Handle exception with logging and user notification.

        Returns user-friendly message.
        """
        # Log the error with context
        # Send notification if critical
        # Return user-friendly message

    def handle_network_error(exc: NetworkError) -> str:
        """Handle network-related errors"""

    def handle_authentication_error(exc: AuthenticationError) -> str:
        """Handle authentication errors"""

    def handle_validation_error(exc: ValidationError) -> str:
        """Handle validation errors"""
```

---

## Dependency Injection

### Service Container

**Archivo:** `app/core/container.py`

```python
class ServiceContainer:
    """Dependency injection container for services"""

    def __init__(self):
        self._settings = None
        self._secrets_manager = None
        self._notification_service = None
        self._auth_service = None
        self._hr_service = None
        self._report_service = None
        self._error_handler = None

    @property
    def settings(self) -> Settings:
        if self._settings is None:
            self._settings = get_settings()
        return self._settings

    @property
    def notification_service(self) -> NotificationService:
        if self._notification_service is None:
            self._notification_service = NotificationService(
                bot_token=self.secrets_manager.get_secret('BOT_TOKEN_ENCRYPTED'),
                settings=self.settings
            )
        return self._notification_service

    # ... other services
```

---

## Mejoras en Servicios Existentes

### AuthService

**Mejoras:**
- Agregar manejo de errores específico
- Implementar retry logic para pasos de autenticación
- Agregar validación de sesión
- Logging más detallado

### HRService

**Mejoras:**
- Agregar validación de datos antes de enviar
- Implementar caché de informes recientes
- Mejorar parsing HTML con manejo de errores
- Agregar timeout configurable

---

## Integración con Bot

### Antes (Fase 2)

```python
# bot.py
def dia_handler(message):
    vive_orange = viveOrange.ViveOrange(True, False)
    msg = vive_orange.connectar(dia_registro)
    bot.send_message(message.chat.id, msg)
```

### Después (Fase 3)

```python
# bot.py
def dia_handler(message):
    try:
        # Use dependency injection
        container = get_container()

        # Validate date
        dia_registro = validar_dia(day.upper())
        mensaje, registrar = dia_validate(dia_registro)

        if registrar:
            # Use services
            session = create_session()
            container.auth_service.authenticate(session)
            registration = container.hr_service.register_workday(
                session, dia_registro, "8:00", "18:00"
            )

            # Send notification
            container.notification_service.send_workday_confirmation(registration)
        else:
            container.notification_service.send_telegram_message(mensaje)

    except RegistroJornadaException as e:
        error_msg = container.error_handler.handle_exception(e, {
            'user': message.chat.username,
            'date': dia_registro
        })
        container.notification_service.send_error_notification(e, error_msg)
```

---

## Métricas de Progreso

### Archivos a Crear

| Archivo | Líneas Est. | Estado | Descripción |
|---------|-------------|---------|-------------|
| `app/services/notification_service.py` | ~200 | ⏸️ Pendiente | Servicio de notificaciones |
| `app/services/report_service.py` | ~250 | ⏸️ Pendiente | Generación de informes |
| `app/exceptions/__init__.py` | ~100 | ⏸️ Pendiente | Jerarquía de excepciones |
| `app/utils/error_handler.py` | ~150 | ⏸️ Pendiente | Manejo centralizado de errores |
| `app/core/container.py` | ~120 | ⏸️ Pendiente | Contenedor de dependencias |
| **TOTAL** | **~820 líneas** | **0%** | **5 archivos nuevos** |

### Archivos a Modificar

- `app/services/auth_service.py` - Agregar manejo de errores
- `app/services/hr_service.py` - Agregar validaciones
- `app/bot.py` - Integrar nuevos servicios
- `requirements.txt` - (sin cambios necesarios)

---

## Beneficios Esperados

### Mantenibilidad

- ✅ Separación clara de responsabilidades
- ✅ Código más testeable (cada servicio independiente)
- ✅ Menor acoplamiento entre componentes
- ✅ Reutilización de código

### Robustez

- ✅ Manejo de errores centralizado y consistente
- ✅ Validación en múltiples capas
- ✅ Logging detallado para debugging
- ✅ Recuperación automática de errores transitorios

### Escalabilidad

- ✅ Fácil agregar nuevos servicios
- ✅ Servicios intercambiables (interfaces)
- ✅ Inyección de dependencias facilita testing
- ✅ Preparado para agregar nuevas funcionalidades

---

## Próximos Pasos

### Inmediatos

1. Crear NotificationService
2. Crear ReportService
3. Crear jerarquía de excepciones
4. Crear ErrorHandler
5. Implementar ServiceContainer

### Post-Fase 3

**Fase 4: Testing y CI/CD**
- Tests unitarios para todos los servicios
- Tests de integración
- GitHub Actions
- Optimización Docker

---

## Notas de Implementación

### Prioridad de Implementación

1. **Alta**: NotificationService (mejora UX inmediatamente)
2. **Alta**: Exception hierarchy (base para error handling)
3. **Media**: ErrorHandler (mejora robustez)
4. **Media**: ReportService (mejora funcionalidad)
5. **Baja**: ServiceContainer (mejora arquitectura, pero no funcionalidad)

### Compatibilidad

- Mantener retrocompatibilidad con ViveOrange.py actual
- Deprecar gradualmente métodos antiguos
- Agregar warnings para código deprecated
