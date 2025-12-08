# 🧪 Guía Rápida de Testing

Guía paso a paso para configurar el entorno de testing y ejecutar la suite de tests.

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración del Entorno](#configuración-del-entorno)
3. [Validación del Entorno](#validación-del-entorno)
4. [Ejecutar Tests](#ejecutar-tests)
5. [Interpretar Resultados](#interpretar-resultados)
6. [Troubleshooting](#troubleshooting)
7. [Scripts de Automatización](#scripts-de-automatización)

---

## ✅ Requisitos Previos

### Software Necesario

- **Python 3.10 o 3.11** (recomendado 3.11)
- **Git** para clonar el repositorio
- **pip** actualizado (versión 23.0+)

### Verificar Python

```bash
python --version
# Esperado: Python 3.11.x o 3.10.x

pip --version
# Esperado: pip 23.0 o superior
```

### Verificar Git

```bash
git --version
# Esperado: git version 2.x
```

---

## 🔧 Configuración del Entorno

### Paso 1: Clonar el Repositorio

```bash
# Clonar repositorio
git clone <repository-url>
cd registrojornada-application-python

# Cambiar a rama develop
git checkout develop
```

### Paso 2: Crear Entorno Virtual

**Windows:**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Verificar activación (debe mostrar (venv) en el prompt)
```

**Linux/Mac:**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Verificar activación (debe mostrar (venv) en el prompt)
```

### Paso 3: Actualizar pip

```bash
# Actualizar pip a última versión
python -m pip install --upgrade pip

# Verificar
pip --version
```

### Paso 4: Instalar Dependencias

```bash
# Instalar dependencias de producción
pip install -r requirements.txt

# Instalar dependencias de desarrollo (NECESARIO para tests)
pip install -r requirements-dev.txt

# Verificar instalación
pip list | grep pytest
# Debe mostrar: pytest, pytest-cov, pytest-mock, pytest-asyncio
```

---

## 🔍 Validación del Entorno

### Script de Validación Automática

Hemos creado un script que valida automáticamente tu entorno de testing.

#### Ejecutar Validación

```bash
python scripts/validate_test_environment.py
```

#### Salida Esperada

```
[OK] Python version: 3.11.2
[OK] Virtual environment: Active
[OK] pytest: 8.0.0
[OK] pytest-cov: 4.1.0
[OK] pytest-mock: 3.12.0
[OK] black: 24.2.0
[OK] All test dependencies installed
[OK] Test directory exists
[OK] 88 test files found
[OK] Environment ready for testing!

Summary: 10/10 checks passed
```

### Validación Manual

Si prefieres validar manualmente:

```bash
# 1. Verificar Python
python --version

# 2. Verificar pytest
pytest --version

# 3. Verificar dependencias clave
python -c "import pytest, pytest_cov, pytest_mock, black, flake8, mypy; print('All imports OK')"

# 4. Verificar tests existen
ls tests/unit/*.py
# Debe mostrar: test_config.py, test_models.py, test_exceptions.py, etc.

# 5. Verificar pytest config
cat pytest.ini
# Debe existir y tener configuración
```

---

## 🚀 Ejecutar Tests

### Tests Rápidos (Sin Coverage)

Ideal para desarrollo rápido:

```bash
# Ejecutar todos los tests sin coverage
pytest --no-cov

# Salida esperada:
# ======================== 88 passed in 5.08s =========================
```

### Tests Completos (Con Coverage)

Ejecución completa con reporte de cobertura:

```bash
# Ejecutar todos los tests con coverage
pytest

# O explícitamente:
pytest --cov=app --cov-report=term-missing
```

### Tests por Categoría

```bash
# Solo tests unitarios
pytest tests/unit/

# Solo un módulo específico
pytest tests/unit/test_models.py

# Solo una clase de tests
pytest tests/unit/test_models.py::TestWorkdayRegistration

# Solo un test específico
pytest tests/unit/test_models.py::TestWorkdayRegistration::test_create_valid_workday
```

### Tests con Verbosidad

```bash
# Modo verbose (más detalles)
pytest -v

# Modo muy verbose (máximo detalle)
pytest -vv

# Mostrar print statements
pytest -s

# Combinado
pytest -vv -s tests/unit/test_config.py
```

### Tests por Marcadores

```bash
# Solo tests unitarios (marcados con @pytest.mark.unit)
pytest -m unit

# Excluir tests lentos
pytest -m "not slow"
```

---

## 📊 Interpretar Resultados

### Salida Exitosa

```
============================= test session starts =============================
platform win32 -- Python 3.11.2, pytest-8.0.0, pluggy-1.6.0
rootdir: c:\...\registrojornada-application-python
configfile: pytest.ini
plugins: anyio-4.3.0, asyncio-0.23.5, cov-4.1.0, mock-3.12.0
collected 88 items

tests/unit/test_config.py ...........                                   [ 12%]
tests/unit/test_exceptions.py .............                             [ 27%]
tests/unit/test_models.py ..................................            [ 66%]
tests/unit/test_notification_service.py ..............                  [ 82%]
tests/unit/test_secrets_manager.py ................                     [100%]

======================== 88 passed in 5.08s ================================
```

**Indicadores de éxito:**
- ✅ Todos los tests muestran `.` (punto verde)
- ✅ Mensaje final: `88 passed`
- ✅ No hay `FAILED` o `ERROR`

### Salida con Fallos

```
tests/unit/test_models.py::TestWorkdayRegistration::test_invalid_time F [50%]

================================== FAILURES ====================================
_____________________ TestWorkdayRegistration.test_invalid_time _______________

    def test_invalid_time(self):
>       assert False
E       AssertionError

tests/unit/test_models.py:75: AssertionError
====================== 1 failed, 87 passed in 5.2s =========================
```

**Indicadores de fallo:**
- ❌ `F` indica fallo
- ❌ Mensaje final: `1 failed, 87 passed`
- ❌ Sección `FAILURES` muestra detalles

### Reporte de Coverage

```
---------- coverage: platform win32, python 3.11.2 -----------
Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
app/__init__.py                             0      0   100%
app/config.py                              45      2    96%   78-79
app/models/workday.py                      67      3    95%   45, 89-90
app/services/notification_service.py      112     15    87%   67-72, 145-150
---------------------------------------------------------------------
TOTAL                                     856     98    89%

================== 88 passed, 3 warnings in 6.45s ====================
```

**Indicadores:**
- ✅ `Cover` >85% es objetivo mínimo
- ✅ `Missing` muestra líneas sin cubrir
- ⚠️ `warnings` son normales (deprecations de Pydantic)

---

## 🐛 Troubleshooting

### Error: "No module named 'pytest'"

**Causa:** pytest no instalado

**Solución:**
```bash
pip install -r requirements-dev.txt
```

### Error: "No tests collected"

**Causa:** pytest no encuentra los tests

**Solución:**
```bash
# Verificar que estás en el directorio raíz del proyecto
pwd  # o cd en Windows

# Verificar que tests/ existe
ls tests/

# Ejecutar desde raíz con path explícito
pytest tests/
```

### Error: "ModuleNotFoundError: No module named 'app'"

**Causa:** PYTHONPATH no configurado o no estás en directorio raíz

**Solución:**
```bash
# Asegurarte de estar en raíz
cd registrojornada-application-python

# Ejecutar tests
pytest
```

### Error: "ImportError: cannot import name 'X'"

**Causa:** Dependencias de producción no instaladas

**Solución:**
```bash
# Instalar todas las dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Tests muy lentos

**Causa:** Coverage toma tiempo

**Solución:**
```bash
# Ejecutar sin coverage
pytest --no-cov

# O solo tests específicos
pytest tests/unit/test_config.py --no-cov
```

### Error: "Failed: DID NOT RAISE <exception>"

**Causa:** Test espera una excepción que no se lanzó

**Solución:** Este es un fallo real en el código, revisar el test y la implementación.

---

## 🤖 Scripts de Automatización

### Script: validate_test_environment.py

Ubicación: `scripts/validate_test_environment.py`

Valida que el entorno esté correctamente configurado para testing.

**Uso:**
```bash
python scripts/validate_test_environment.py
```

**Qué valida:**
- ✅ Versión de Python
- ✅ Entorno virtual activo
- ✅ Dependencias de testing instaladas
- ✅ Estructura de directorios correcta
- ✅ Tests descubribles

### Script: run_tests.sh / run_tests.bat

Scripts convenientes para ejecutar tests comunes.

**Linux/Mac (run_tests.sh):**
```bash
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

**Windows (run_tests.bat):**
```bash
scripts\run_tests.bat
```

**Opciones:**
```bash
# Tests rápidos
./scripts/run_tests.sh fast

# Tests con coverage
./scripts/run_tests.sh coverage

# Tests con HTML report
./scripts/run_tests.sh html

# Todos los checks de calidad
./scripts/run_tests.sh full
```

### Script: check_quality.sh / check_quality.bat

Ejecuta todos los checks de calidad de código.

**Uso:**
```bash
# Linux/Mac
./scripts/check_quality.sh

# Windows
scripts\check_quality.bat
```

**Qué ejecuta:**
1. Black (formateo)
2. isort (imports)
3. flake8 (linting)
4. mypy (type checking)
5. pytest (tests)

---

## 📈 Flujo de Trabajo Recomendado

### Desarrollo Diario

```bash
# 1. Activar entorno
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Actualizar código
git pull origin develop

# 3. Tests rápidos
pytest --no-cov -x

# 4. Si todo OK, hacer cambios
# ... editar código ...

# 5. Tests del módulo modificado
pytest tests/unit/test_mi_modulo.py

# 6. Tests completos antes de commit
pytest

# 7. Checks de calidad
black app/ tests/
flake8 app/ tests/

# 8. Commit
git add .
git commit -m "feat: mi cambio"
```

### Pre-commit

```bash
# Instalar pre-commit hooks (solo una vez)
pre-commit install

# Los hooks se ejecutarán automáticamente en cada commit
git commit -m "feat: mi cambio"

# Ejecutar manualmente si necesario
pre-commit run --all-files
```

### Antes de Pull Request

```bash
# 1. Ejecutar suite completa
pytest

# 2. Verificar coverage
pytest --cov=app --cov-report=html
open htmlcov/index.html

# 3. Checks de calidad
./scripts/check_quality.sh

# 4. Verificar que todo está limpio
git status

# 5. Push
git push origin mi-feature-branch
```

---

## 📊 Métricas de Éxito

### Estado Actual (Post Fase 4)

| Métrica | Objetivo | Actual | Estado |
|---------|----------|--------|--------|
| Tests Unitarios | >80 | 88 | ✅ |
| Coverage | >80% | >85% | ✅ |
| Tests Passing | 100% | 100% | ✅ |
| Tiempo Ejecución | <10s | ~5s | ✅ |
| CI/CD | Automatizado | ✅ | ✅ |

### Objetivos Próximos (Fase 5)

| Métrica | Objetivo | Estimado |
|---------|----------|----------|
| Tests Totales | >200 | 225+ |
| Coverage | >90% | 90-95% |
| Tests Integración | >20 | 23 |
| Tests E2E | >10 | 12 |

---

## 🔗 Referencias Rápidas

### Comandos Esenciales

```bash
# Setup inicial
pip install -r requirements.txt requirements-dev.txt

# Validar entorno
python scripts/validate_test_environment.py

# Tests rápidos
pytest --no-cov

# Tests completos
pytest

# Coverage HTML
pytest --cov=app --cov-report=html

# Calidad de código
black app/ tests/
flake8 app/ tests/
mypy app/
```

### Archivos Importantes

- `pytest.ini` - Configuración de pytest
- `pyproject.toml` - Configuración de herramientas
- `.pre-commit-config.yaml` - Pre-commit hooks
- `requirements-dev.txt` - Dependencias de desarrollo
- `tests/conftest.py` - Fixtures compartidas

### Documentación

- [Documentación completa de testing](FASE4_TESTING.md)
- [Índice de documentación](README.md)
- [Próximos pasos](NEXT_STEPS.md)

---

## 💡 Tips y Mejores Prácticas

### Performance

```bash
# Ejecutar tests en paralelo (requiere pytest-xdist)
pip install pytest-xdist
pytest -n auto

# Solo tests que fallaron en última ejecución
pytest --lf

# Solo tests que fallaron, luego el resto
pytest --ff
```

### Debugging

```bash
# Entrar en debugger en fallos
pytest --pdb

# Mostrar variables locales en fallos
pytest -l

# Capturar solo errores (no stdout)
pytest --capture=no
```

### Coverage Detallado

```bash
# Coverage de un módulo específico
pytest --cov=app.services.notification_service

# Coverage con líneas faltantes
pytest --cov=app --cov-report=term-missing

# Fallar si coverage < 80%
pytest --cov=app --cov-fail-under=80
```

---

## ✅ Checklist de Validación

Antes de considerar el entorno listo:

- [ ] Python 3.10+ instalado y verificado
- [ ] Entorno virtual creado y activado
- [ ] `requirements.txt` instalado
- [ ] `requirements-dev.txt` instalado
- [ ] `python scripts/validate_test_environment.py` pasa todos los checks
- [ ] `pytest --no-cov` ejecuta 88 tests exitosamente
- [ ] `pytest` genera reporte de coverage >85%
- [ ] `black --check app/ tests/` no muestra errores
- [ ] `flake8 app/ tests/` no muestra errores críticos
- [ ] Pre-commit hooks instalados: `pre-commit install`

---

**Última actualización:** 2025-12-08
**Versión:** 1.0
**Tests actuales:** 88 unitarios
**Coverage:** >85%
