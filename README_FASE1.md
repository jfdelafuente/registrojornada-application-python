# Registro de Jornada - Guía de Inicio Rápido (Post Fase 1)

Bot de Telegram para registro automático de jornadas laborales en ViveOrange con **mejoras de seguridad implementadas**.

---

## 🔐 Cambios de Seguridad (Fase 1)

Esta versión incluye mejoras críticas de seguridad:

- ✅ **Credenciales encriptadas** con Fernet
- ✅ **Logs sanitizados** automáticamente
- ✅ **Validación de entradas** robusta
- ✅ **Dependencias actualizadas** sin vulnerabilidades
- ✅ **Prevención de inyección** de código

---

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
cd "c:\My Program Files\workspace-flask\registrojornada-application-python"
pip install -r requirements.txt
```

### 2. Configurar Credenciales (IMPORTANTE)

**⚠️ Las credenciales ahora deben estar encriptadas**

```bash
# Ejecutar script de encriptación
python scripts/encrypt_secrets.py
```

El script le pedirá:
1. Token del bot de Telegram
2. Chat ID
3. Usuario de ViveOrange
4. Contraseña de ViveOrange
5. Código de empleado

**Salida del script:**
```env
ENCRYPTION_KEY=...
BOT_TOKEN_ENCRYPTED=...
CHAT_ID_ENCRYPTED=...
HR_USERNAME_ENCRYPTED=...
HR_PASSWORD_ENCRYPTED=...
EMPLOYEE_CODE_ENCRYPTED=...
```

### 3. Actualizar archivo .env

Copie TODO el contenido generado al archivo `.env`:

```bash
# En Windows
notepad .env

# En Linux/Mac
nano .env
```

**IMPORTANTE:** Elimine las variables antiguas sin encriptar:
- ~~USUARIO~~
- ~~PASS~~
- ~~COD_EMPLEADO~~
- ~~BOT_TOKEN~~ (sin _ENCRYPTED)
- ~~CHAT_ID~~ (sin _ENCRYPTED)

### 4. Ejecutar el Bot

```bash
python app/bot.py
```

---

## 📁 Estructura del Proyecto

```
registrojornada-application-python/
├── app/
│   ├── security/              ✨ NUEVO
│   │   ├── __init__.py
│   │   └── secrets_manager.py
│   ├── utils/                 ✨ NUEVO
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── validators/            ✨ NUEVO
│   │   ├── __init__.py
│   │   └── input_validator.py
│   ├── bot.py                 ⚡ MEJORADO
│   ├── ViveOrange.py          ⚡ MEJORADO
│   ├── DiaValidator.py
│   ├── configD.py
│   └── BotTelegramRegistro.py
├── scripts/                   ✨ NUEVO
│   └── encrypt_secrets.py
├── logs/                      ✨ NUEVO
│   ├── registrojornada.log
│   └── vive_orange.log
├── tests/
├── .env                       🔒 ENCRIPTADO
├── .env.example              ✨ NUEVO
├── requirements.txt          ⚡ ACTUALIZADO
├── ANALISIS_PROYECTO.md      📋 ANÁLISIS
├── FASE1_SEGURIDAD.md        📋 DOCUMENTACIÓN
└── README.md
```

---

## 🤖 Comandos del Bot

| Comando | Descripción |
|---------|-------------|
| `/start` | Iniciar bot y ver bienvenida |
| `/help` | Mostrar comandos disponibles |
| `/dia` | Registrar jornada (HOY/AYER/YYYYMMDD) |
| `/info` | Ver registro de la semana actual |
| `/infop` | Ver registro de la semana anterior |
| `/version` | Información de versión |

---

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)

```env
# Clave de encriptación (generada por el script)
ENCRYPTION_KEY=your_key_here

# Bot de Telegram (encriptado)
BOT_TOKEN_ENCRYPTED=...
CHAT_ID_ENCRYPTED=...

# Sistema ViveOrange (encriptado)
HR_USERNAME_ENCRYPTED=...
HR_PASSWORD_ENCRYPTED=...
EMPLOYEE_CODE_ENCRYPTED=...
```

### Rotación de Logs

Los logs se rotan automáticamente:
- **Tamaño máximo:** 10MB por archivo
- **Archivos de backup:** 5
- **Ubicación:** `logs/`

Para cambiar la configuración, edite `app/bot.py`:

```python
logger = setup_logger(
    name='registrojornada',
    log_file=str(log_dir / 'registrojornada.log'),
    level=logging.INFO,
    max_bytes=5*1024*1024,  # 5MB
    backup_count=3          # 3 backups
)
```

---

## 🧪 Testing

```bash
# Ejecutar tests
python -m unittest discover -s tests -v

# Con coverage (instalar pytest-cov)
pip install pytest pytest-cov
pytest tests/ --cov=app --cov-report=html
```

---

## 🐳 Docker

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

**Nota:** Asegúrese de que el archivo `.env` está configurado antes de ejecutar Docker.

---

## 🔒 Seguridad

### Mejores Prácticas

1. ✅ **Nunca compartir el archivo .env**
2. ✅ **Guardar ENCRYPTION_KEY en gestor de contraseñas**
3. ✅ **Verificar que .env está en .gitignore**
4. ✅ **Cambiar credenciales si se comprometen**
5. ✅ **Revisar logs periódicamente**

### Rotación de Credenciales

Si necesita cambiar credenciales:

```bash
# 1. Cambiar contraseña en ViveOrange
# 2. Generar nuevos valores encriptados
python scripts/encrypt_secrets.py

# 3. Actualizar .env
# 4. Reiniciar bot
```

### Verificar Seguridad

```bash
# Ver que logs están sanitizados
grep "password" logs/registrojornada.log
# Debería mostrar: password=***

# Verificar encriptación
python -c "from app.security.secrets_manager import SecretsManager; print('OK')"
```

---

## 📊 Logs

### Ubicación

- **Principal:** `logs/registrojornada.log`
- **ViveOrange:** `logs/vive_orange.log`

### Visualizar Logs

```bash
# Ver últimas líneas
tail -n 50 logs/registrojornada.log

# Seguir en tiempo real
tail -f logs/registrojornada.log

# Buscar errores
grep "ERROR" logs/registrojornada.log
```

### Información Sanitizada

Los logs automáticamente ocultan:
- Contraseñas
- Tokens
- Session IDs
- Cookies
- Códigos de empleado

**Ejemplo:**
```
2024-06-15 10:30:00 - registrojornada - INFO - User login successful
2024-06-15 10:30:01 - registrojornada - DEBUG - password=*** (sanitizado)
```

---

## ⚠️ Troubleshooting

### Error: "ENCRYPTION_KEY not found"

**Solución:**
```bash
python scripts/encrypt_secrets.py
# Copiar ENCRYPTION_KEY al .env
```

### Error: "Invalid ENCRYPTION_KEY"

**Causa:** La clave no es válida o está corrupta

**Solución:**
```bash
# Generar nueva clave y re-encriptar todo
python scripts/encrypt_secrets.py
```

### Error: "Secret not found in environment variables"

**Causa:** Falta variable en .env

**Solución:**
Verificar que .env contiene todas las variables:
```bash
# Verificar
cat .env | grep ENCRYPTED

# Debería mostrar:
# BOT_TOKEN_ENCRYPTED=...
# CHAT_ID_ENCRYPTED=...
# HR_USERNAME_ENCRYPTED=...
# HR_PASSWORD_ENCRYPTED=...
# EMPLOYEE_CODE_ENCRYPTED=...
```

### Bot no responde

**Checklist:**
1. ✅ Token de Telegram válido
2. ✅ Chat ID correcto
3. ✅ Credenciales ViveOrange correctas
4. ✅ Internet conectado
5. ✅ No hay errores en logs

```bash
# Ver últimos errores
tail -n 100 logs/registrojornada.log | grep ERROR
```

---

## 📝 Desarrollo

### Agregar Nuevos Secretos

1. Agregar variable al script de encriptación
2. Encriptar valor
3. Actualizar .env.example
4. Documentar en README

### Agregar Nuevos Validadores

```python
# En app/validators/input_validator.py

@staticmethod
def validate_my_input(value: str) -> bool:
    """Validar mi entrada."""
    # Lógica de validación
    return True
```

### Personalizar Sanitización de Logs

```python
# En app/utils/logger.py

class SanitizedFormatter(logging.Formatter):
    PATTERNS = [
        # Agregar nuevo patrón
        (r'(mi_secreto)["\']?\s*[:=]\s*["\']?([^"\'}\s]+)', r'\1=***'),
        # ... patrones existentes
    ]
```

---

## 📚 Documentación Adicional

- **[ANALISIS_PROYECTO.md](ANALISIS_PROYECTO.md)** - Análisis completo del proyecto
- **[FASE1_SEGURIDAD.md](FASE1_SEGURIDAD.md)** - Detalles de mejoras de seguridad
- **[.env.example](.env.example)** - Template de configuración

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

---

## 📄 Licencia

Este proyecto es de uso interno para empleados de Orange.

---

## 👥 Soporte

Para issues y preguntas:
1. Revisar [FASE1_SEGURIDAD.md](FASE1_SEGURIDAD.md)
2. Verificar logs en `logs/`
3. Contactar al equipo de desarrollo

---

## ✅ Checklist Pre-Producción

Antes de desplegar en producción:

- [ ] Ejecutar `python scripts/encrypt_secrets.py`
- [ ] Copiar valores encriptados a .env
- [ ] Eliminar variables sin encriptar del .env
- [ ] Verificar .env está en .gitignore
- [ ] Ejecutar tests: `python -m unittest discover -s tests`
- [ ] Probar bot localmente
- [ ] Verificar logs se sanitizan correctamente
- [ ] Documentar ENCRYPTION_KEY en gestor de contraseñas
- [ ] Configurar monitoreo de logs
- [ ] Establecer proceso de rotación de credenciales

---

**Versión:** 2.0 (Post Fase 1)
**Última actualización:** 2025-12-07

🔒 **Sistema seguro y production-ready**
