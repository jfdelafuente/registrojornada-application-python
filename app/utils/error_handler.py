"""Centralized error handling for the application."""

import logging
from typing import Dict, Optional, Any
from datetime import datetime

from exceptions import (
    RegistroJornadaException,
    AuthenticationError,
    InvalidCredentialsError,
    SessionExpiredError,
    OAMRedirectError,
    HRServiceError,
    RegistrationError,
    ReportGenerationError,
    HTMLParsingError,
    ValidationError,
    InvalidDateError,
    InvalidTimeFormatError,
    HolidayValidationError,
    NetworkError,
    ConnectionTimeoutError,
    ServiceUnavailableError,
    HTTPError,
    ConfigurationError,
    NotificationError,
    TelegramSendError,
)

logger = logging.getLogger(__name__)


class ErrorHandler:
    """
    Centralized error handler for consistent error management.

    Features:
    - Converts exceptions to user-friendly messages
    - Logs errors with context
    - Determines error severity
    - Provides recovery suggestions
    """

    def __init__(self, notification_service=None):
        """
        Initialize error handler.

        Args:
            notification_service: Optional NotificationService for critical errors
        """
        self.notification_service = notification_service

    def handle_exception(
        self,
        exc: Exception,
        context: Dict[str, Any] = None
    ) -> str:
        """
        Handle any exception and return user-friendly message.

        Args:
            exc: Exception that occurred
            context: Additional context (user, date, operation, etc.)

        Returns:
            User-friendly error message
        """
        context = context or {}

        # Log the error with full context
        self._log_error(exc, context)

        # Handle specific exception types
        if isinstance(exc, AuthenticationError):
            return self.handle_authentication_error(exc)
        elif isinstance(exc, ValidationError):
            return self.handle_validation_error(exc)
        elif isinstance(exc, NetworkError):
            return self.handle_network_error(exc)
        elif isinstance(exc, HRServiceError):
            return self.handle_hr_service_error(exc)
        elif isinstance(exc, ConfigurationError):
            return self.handle_configuration_error(exc)
        elif isinstance(exc, NotificationError):
            return self.handle_notification_error(exc)
        elif isinstance(exc, RegistroJornadaException):
            # Generic application error
            return self._format_generic_error(exc)
        else:
            # Unexpected error
            return self._format_unexpected_error(exc)

    def _log_error(
        self,
        exc: Exception,
        context: Dict[str, Any]
    ):
        """
        Log error with context information.

        Args:
            exc: Exception to log
            context: Context dictionary
        """
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(exc).__name__,
            'error_message': str(exc),
            'context': context
        }

        if isinstance(exc, RegistroJornadaException) and exc.details:
            error_info['details'] = exc.details

        # Determine log level based on error type
        if isinstance(exc, (ValidationError, NotificationError)):
            logger.warning(f"Error: {error_info}")
        elif isinstance(exc, NetworkError):
            logger.error(f"Network error: {error_info}")
        elif isinstance(exc, AuthenticationError):
            logger.error(f"Authentication error: {error_info}")
        else:
            logger.error(f"Unexpected error: {error_info}", exc_info=True)

    def handle_authentication_error(self, exc: AuthenticationError) -> str:
        """
        Handle authentication errors.

        Args:
            exc: AuthenticationError exception

        Returns:
            User-friendly message
        """
        if isinstance(exc, InvalidCredentialsError):
            return (
                "❌ *Error de Autenticación*\n\n"
                "Las credenciales son inválidas. Por favor, verifica:\n"
                "• Que el usuario y contraseña en .env sean correctos\n"
                "• Que las credenciales estén correctamente encriptadas\n\n"
                "💡 _Usa el script encrypt_secrets.py para re-encriptar credenciales_"
            )
        elif isinstance(exc, SessionExpiredError):
            return (
                "❌ *Sesión Expirada*\n\n"
                "Tu sesión ha expirado. Por favor, intenta de nuevo.\n\n"
                "🔄 _El sistema se autenticará automáticamente_"
            )
        elif isinstance(exc, OAMRedirectError):
            step = exc.details.get('step', 'desconocido')
            return (
                f"❌ *Error de Autenticación OAM*\n\n"
                f"Falló el paso: {step}\n\n"
                "Posibles causas:\n"
                "• Cambios en el sistema OAM de Orange\n"
                "• Problemas de conectividad\n\n"
                "💡 _Contacta con soporte si el error persiste_"
            )
        else:
            return (
                "❌ *Error de Autenticación*\n\n"
                f"{exc.message}\n\n"
                "🔄 _Intenta de nuevo en unos minutos_"
            )

    def handle_validation_error(self, exc: ValidationError) -> str:
        """
        Handle validation errors.

        Args:
            exc: ValidationError exception

        Returns:
            User-friendly message
        """
        if isinstance(exc, InvalidDateError):
            format_exp = exc.details.get('expected_format', 'YYYYMMDD')
            date_str = exc.details.get('date', '')
            return (
                "⚠️ *Fecha Inválida*\n\n"
                f"La fecha '{date_str}' no es válida.\n\n"
                f"Formato esperado: *{format_exp}*\n\n"
                "Ejemplos:\n"
                "• HOY\n"
                "• AYER\n"
                "• 20251207 (7 de diciembre de 2025)"
            )
        elif isinstance(exc, InvalidTimeFormatError):
            time_str = exc.details.get('time', '')
            return (
                "⚠️ *Hora Inválida*\n\n"
                f"La hora '{time_str}' no es válida.\n\n"
                "Formato esperado: *HH:MM*\n\n"
                "Ejemplo: 08:00"
            )
        elif isinstance(exc, HolidayValidationError):
            date_str = exc.details.get('date', '')
            holiday = exc.details.get('holiday', 'festivo')
            return (
                "🎉 *Día Festivo*\n\n"
                f"El día {date_str} es *{holiday}*.\n\n"
                "No es necesario registrar jornada.\n\n"
                "💡 _Si quieres registrarlo de todas formas, responde 'Y'_"
            )
        else:
            return (
                "⚠️ *Error de Validación*\n\n"
                f"{exc.message}\n\n"
                "Por favor, verifica los datos e intenta de nuevo."
            )

    def handle_network_error(self, exc: NetworkError) -> str:
        """
        Handle network errors.

        Args:
            exc: NetworkError exception

        Returns:
            User-friendly message
        """
        if isinstance(exc, ConnectionTimeoutError):
            timeout = exc.details.get('timeout_seconds', 30)
            return (
                "⏱️ *Timeout de Conexión*\n\n"
                f"La conexión tardó más de {timeout} segundos.\n\n"
                "Posibles causas:\n"
                "• Conexión a internet lenta\n"
                "• Servidor sobrecargado\n\n"
                "🔄 _Intenta de nuevo en unos minutos_"
            )
        elif isinstance(exc, ServiceUnavailableError):
            service = exc.details.get('service', 'servicio')
            status_code = exc.details.get('status_code', '')
            msg = (
                "🚫 *Servicio No Disponible*\n\n"
                f"El servicio de {service} no está disponible."
            )
            if status_code:
                msg += f"\nCódigo: {status_code}"
            msg += "\n\n🔄 _Intenta de nuevo más tarde_"
            return msg
        elif isinstance(exc, HTTPError):
            status_code = exc.details.get('status_code', '')
            return (
                "🌐 *Error HTTP*\n\n"
                f"Error en la petición HTTP (código: {status_code}).\n\n"
                "🔄 _Intenta de nuevo_"
            )
        else:
            return (
                "🌐 *Error de Red*\n\n"
                f"{exc.message}\n\n"
                "Verifica tu conexión a internet."
            )

    def handle_hr_service_error(self, exc: HRServiceError) -> str:
        """
        Handle HR service errors.

        Args:
            exc: HRServiceError exception

        Returns:
            User-friendly message
        """
        if isinstance(exc, RegistrationError):
            date_str = exc.details.get('date', '')
            reason = exc.details.get('reason', '')
            msg = "❌ *Error al Registrar Jornada*\n\n"
            if date_str:
                msg += f"Fecha: {date_str}\n"
            if reason:
                msg += f"Razón: {reason}\n"
            msg += "\n🔄 _Intenta de nuevo_"
            return msg
        elif isinstance(exc, ReportGenerationError):
            report_type = exc.details.get('report_type', 'informe')
            return (
                f"📊 *Error al Generar {report_type.title()}*\n\n"
                f"{exc.message}\n\n"
                "🔄 _Intenta de nuevo_"
            )
        elif isinstance(exc, HTMLParsingError):
            element = exc.details.get('element', '')
            msg = "⚠️ *Error al Procesar Respuesta*\n\n"
            if element:
                msg += f"No se encontró el elemento: {element}\n\n"
            msg += (
                "Posibles causas:\n"
                "• Cambios en la web de ViveOrange\n"
                "• Respuesta inesperada del servidor\n\n"
                "💡 _Contacta con soporte si el error persiste_"
            )
            return msg
        else:
            return (
                "❌ *Error en Servicio de RRHH*\n\n"
                f"{exc.message}\n\n"
                "🔄 _Intenta de nuevo_"
            )

    def handle_configuration_error(self, exc: ConfigurationError) -> str:
        """
        Handle configuration errors.

        Args:
            exc: ConfigurationError exception

        Returns:
            User-friendly message
        """
        config_key = exc.details.get('config_key', '')
        return (
            "⚙️ *Error de Configuración*\n\n"
            f"{exc.message}\n"
            f"Clave: {config_key}\n\n"
            "Verifica tu archivo .env"
        )

    def handle_notification_error(self, exc: NotificationError) -> str:
        """
        Handle notification errors.

        Args:
            exc: NotificationError exception

        Returns:
            User-friendly message
        """
        if isinstance(exc, TelegramSendError):
            return (
                "📱 *Error al Enviar Mensaje*\n\n"
                "No se pudo enviar el mensaje por Telegram.\n"
                "El mensaje ha sido registrado en los logs.\n\n"
                "⚠️ _Verifica el token del bot y el chat ID_"
            )
        else:
            return f"📱 *Error de Notificación*\n\n{exc.message}"

    def _format_generic_error(self, exc: RegistroJornadaException) -> str:
        """Format generic application error."""
        msg = f"❌ *Error*\n\n{exc.message}"
        if exc.details:
            details_str = "\n".join(f"• {k}: {v}" for k, v in exc.details.items())
            msg += f"\n\n*Detalles:*\n{details_str}"
        return msg

    def _format_unexpected_error(self, exc: Exception) -> str:
        """Format unexpected error."""
        return (
            "❌ *Error Inesperado*\n\n"
            f"{type(exc).__name__}: {str(exc)}\n\n"
            "Este error no era esperado.\n"
            "Por favor, revisa los logs para más información.\n\n"
            "💡 _Contacta con soporte si el error persiste_"
        )
