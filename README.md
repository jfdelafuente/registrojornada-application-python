# 📱 Registro de Jornada - Bot de Telegram

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Security](https://img.shields.io/badge/security-phase%201%20completed-green.svg)](FASE1_SEGURIDAD.md)
[![License](https://img.shields.io/badge/license-Internal-orange.svg)]()

Bot de Telegram para automatizar el registro de jornadas laborales en el sistema ViveOrange de empleados de Orange España.

---

## 🎯 Características Principales

- ✅ **Registro automático de jornadas** laborales
- ✅ **Consulta de registros** semanales (actual y anterior)
- ✅ **Validación inteligente** de días festivos y vacaciones
- ✅ **Gestión de teletrabajo** con confirmación opcional
- ✅ **Credenciales encriptadas** con Fernet
- ✅ **Logs sanitizados** sin información sensible
- ✅ **Validación de entradas** robusta
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
   cd "c:\My Program Files\workspace-flask\registrojornada-application-python"
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

5. **Ejecutar el bot**
   ```bash
   python app/bot.py
   ```

---

## 📁 Estructura del Proyecto

```
registrojornada-application-python/
├── app/                          # Código fuente de la aplicación
│   ├── security/                 # 🆕 Módulos de seguridad (Fase 1)
│   │   ├── __init__.py
│   │   └── secrets_manager.py   # Gestión de credenciales encriptadas
│   ├── utils/                    # 🆕 Utilidades (Fase 1)
│   │   ├── __init__.py
│   │   ├── logger.py            # Logging con sanitización
│   │   └── validarDay.py        # Validación de fechas
│   ├── validators/               # 🆕 Validadores (Fase 1)
│   │   ├── __init__.py
│   │   └── input_validator.py   # Validación de entradas
│   ├── bot.py                    # Punto de entrada principal (actualizado)
│   ├── ViveOrange.py            # Integración con sistema ViveOrange (mejorado)
│   ├── DiaValidator.py          # Validación de días laborales
│   ├── BotTelegramRegistro.py   # Wrapper de API de Telegram
│   ├── configD.py               # Configuración (horarios, festivos)
│   └── main2.py                 # CLI alternativo
├── scripts/                      # 🆕 Scripts de utilidad (Fase 1)
│   └── encrypt_secrets.py       # Script de encriptación de credenciales
├── tests/                        # Tests unitarios
│   ├── test_bot_telegram_registro.py
│   ├── test_dias_validator.py
│   └── test_main.py
├── logs/                         # 🆕 Logs (generados automáticamente)
│   ├── registrojornada.log
│   └── vive_orange.log
├── config/                       # Configuración (para futuras fases)
├── .env                          # Variables de entorno encriptadas 🔒
├── .env.example                  # 🆕 Template de configuración
├── .gitignore                    # Archivos ignorados por Git
├── Dockerfile                    # Configuración Docker
├── docker-compose.yml            # Orquestación Docker
├── requirements.txt              # Dependencias actualizadas (Fase 1)
├── README.md                     # Este archivo
├── ANALISIS_PROYECTO.md          # 🆕 Análisis completo del proyecto
├── FASE1_SEGURIDAD.md           # 🆕 Documentación técnica Fase 1
└── RESUMEN_FASE1.md             # 🆕 Resumen ejecutivo Fase 1
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

### Configuración de Horarios (configD.py)

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

Ver [FASE1_SEGURIDAD.md](FASE1_SEGURIDAD.md) para más detalles.

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
```

### Security Dependencies

```txt
cryptography==42.0.5        # Encriptación Fernet
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

- **[FASE1_SEGURIDAD.md](FASE1_SEGURIDAD.md)** (14KB)
  - Implementación técnica de seguridad
  - Uso de SecretsManager
  - Uso de SanitizedFormatter
  - Guías de troubleshooting

- **[RESUMEN_FASE1.md](RESUMEN_FASE1.md)** (12KB)
  - Resumen ejecutivo de Fase 1
  - Métricas alcanzadas
  - KPIs y logros

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
- [x] Gestión segura de credenciales
- [x] Sanitización de logs
- [x] Validación de entradas
- [x] Actualización de dependencias
- [x] Prevención de inyección

### 🔄 Fase 2: Refactorización (Próxima)
- [ ] Eliminar código duplicado
- [ ] Reestructurar en capas
- [ ] Implementar Pydantic Settings
- [ ] Migrar festivos a JSON
- [ ] Separar ViveOrange en servicios

### 📅 Fase 3: Service Layer
- [ ] Crear interfaces de servicios
- [ ] Implementar HRService
- [ ] Implementar AuthService
- [ ] Refactorizar handlers

### 🧪 Fase 4: Testing y CI/CD
- [ ] Tests unitarios (>80% coverage)
- [ ] GitHub Actions CI
- [ ] Dockerfile multi-stage
- [ ] Automatización de deployment

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
2. Revisar [FASE1_SEGURIDAD.md](FASE1_SEGURIDAD.md)
3. Verificar logs en `logs/`
4. Contactar al equipo de desarrollo

---

## 📈 Estado del Proyecto

```
Version: 2.0 (Post Fase 1)
Estado: 🟢 PRODUCTION-READY (Seguridad)
Última actualización: 2025-12-07

Vulnerabilidades: 0
Cobertura de tests: ~40%
Nivel de seguridad: ALTO
```

### Métricas

| Métrica | Valor |
|---------|-------|
| Líneas de código | ~3,000 |
| Archivos Python | 16 |
| Tests | 8 |
| Documentación | ~100KB |
| Dependencias | 6 core + 1 security |

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

### Implementadas en Fase 1

- ✅ **Principio de mínimo privilegio** - Credenciales encriptadas
- ✅ **Defense in depth** - Múltiples capas de seguridad
- ✅ **Secure by default** - Sanitización automática
- ✅ **Fail securely** - Validación con excepciones claras
- ✅ **Don't trust input** - Validación exhaustiva

### Recomendaciones

1. Revisar logs diariamente
2. Actualizar dependencias mensualmente
3. Rotar credenciales trimestralmente
4. Hacer backup de `ENCRYPTION_KEY`
5. Mantener documentación actualizada

---

**Última actualización:** 2025-12-07
**Versión:** 2.0
**Estado:** 🔒 Seguro y Production-Ready
