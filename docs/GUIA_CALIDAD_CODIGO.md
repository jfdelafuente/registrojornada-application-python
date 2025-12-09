# Guía de Calidad de Código - RegistroJornada Bot

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Prerequisitos](#prerequisitos)
3. [Herramientas de Calidad de Código](#herramientas-de-calidad-de-código)
4. [Configuración del Entorno](#configuración-del-entorno)
5. [Validación Automática del Entorno](#validación-automática-del-entorno)
6. [Ejecución de Herramientas](#ejecución-de-herramientas)
7. [Interpretación de Resultados](#interpretación-de-resultados)
8. [Pre-commit Hooks](#pre-commit-hooks)
9. [Flujo de Trabajo Diario](#flujo-de-trabajo-diario)
10. [Troubleshooting](#troubleshooting)

---

## Introducción

Esta guía proporciona instrucciones paso a paso para configurar y ejecutar las herramientas de calidad de código en el proyecto RegistroJornada Bot.

### ¿Por qué calidad de código?

- **Consistencia**: Código uniforme y fácil de leer
- **Mantenibilidad**: Reducción de bugs y code smells
- **Type Safety**: Detección temprana de errores de tipo
- **Best Practices**: Adherencia a estándares de Python

### Herramientas incluidas

| Herramienta | Propósito | Documentación |
|-------------|-----------|---------------|
| **Black** | Formateo automático de código | [docs.black](https://black.readthedocs.io/) |
| **isort** | Ordenamiento de imports | [pycqa.github.io/isort](https://pycqa.github.io/isort/) |
| **Flake8** | Linting y detección de errores | [flake8.pycqa.org](https://flake8.pycqa.org/) |
| **Mypy** | Type checking estático | [mypy-lang.org](https://mypy-lang.org/) |

---

## Prerequisitos

### 1. Python 3.10+

Verificar versión de Python:

```bash
python --version
```

**Salida esperada**: `Python 3.10.x` o superior

### 2. Virtual Environment Activo

**Windows**:
```bash
venv\Scripts\activate
```

**Linux/Mac**:
```bash
source venv/bin/activate
```

**Verificación**: El prompt debe mostrar `(venv)` al inicio

### 3. Dependencias Instaladas

```bash
pip install -r requirements-dev.txt
```

---

## Herramientas de Calidad de Código

### Black - Code Formatter

**Qué hace**: Formatea automáticamente el código Python según un estilo consistente.

**Características**:
- Formateo determinístico (mismo código → mismo resultado)
- Line length: 100 caracteres
- Compatibilidad con Python 3.10+
- No requiere configuración (opinionated)

**Configuración** (pyproject.toml):
```toml
[tool.black]
line-length = 100
target-version = ['py310']
exclude = '''
/(
    \.git
  | \.venv
  | venv
  | build
  | dist
)/
'''
```

### isort - Import Sorter

**Qué hace**: Ordena y agrupa imports según convenciones de Python.

**Características**:
- Separa imports de stdlib, third-party y locales
- Alfabetización automática
- Compatible con Black
- Detección automática de imports

**Configuración** (pyproject.toml):
```toml
[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
```

### Flake8 - Linter

**Qué hace**: Verifica el código contra PEP 8 y detecta errores comunes.

**Características**:
- Detección de errores de sintaxis
- Verificación de PEP 8
- Detección de complejidad ciclomática
- Variables no usadas, imports sin usar

**Configuración** (.flake8):
```ini
[flake8]
max-line-length = 100
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    build,
    dist
ignore =
    E203,  # whitespace before ':' (conflicto con black)
    E501,  # line too long (manejado por black)
    W503   # line break before binary operator
```

### Mypy - Type Checker

**Qué hace**: Verifica tipos estáticos en Python para detectar errores de tipo.

**Características**:
- Type checking estático
- Detección de errores antes de runtime
- Compatibilidad con type hints de Python
- Gradual typing (puede usarse parcialmente)

**Configuración** (pyproject.toml):
```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
ignore_missing_imports = true
no_implicit_optional = true
show_error_codes = true
```

---

## Configuración del Entorno

### Paso 1: Clonar el Repositorio (si no está hecho)

```bash
git clone <repository-url>
cd registrojornada-application-python
```

### Paso 2: Crear Virtual Environment

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac**:
```bash
python -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias de Desarrollo

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**Verificar instalación**:
```bash
black --version
isort --version
flake8 --version
mypy --version
```

### Paso 4: Verificar Archivos de Configuración

**Archivos necesarios**:
- ✅ `pyproject.toml` - Configuración de Black, isort, mypy
- ✅ `.flake8` - Configuración de Flake8
- ✅ `.pre-commit-config.yaml` - Hooks de pre-commit

**Verificar existencia**:
```bash
# Windows
dir pyproject.toml .flake8 .pre-commit-config.yaml

# Linux/Mac
ls -la pyproject.toml .flake8 .pre-commit-config.yaml
```

---

## Validación Automática del Entorno

### Script de Validación

Ejecutar el script de validación automática:

**Windows**:
```bash
python scripts\validate_quality_tools.py
```

**Linux/Mac**:
```bash
python scripts/validate_quality_tools.py
```

### Qué Valida el Script

El script verifica **25+ checks** incluyendo:

1. **Entorno Python**:
   - ✅ Versión de Python (3.10+)
   - ✅ Virtual environment activo
   - ✅ Pip actualizado

2. **Herramientas Instaladas**:
   - ✅ Black (versión)
   - ✅ isort (versión)
   - ✅ Flake8 (versión)
   - ✅ Mypy (versión)
   - ✅ Pre-commit (versión)

3. **Archivos de Configuración**:
   - ✅ pyproject.toml existe
   - ✅ .flake8 existe
   - ✅ .pre-commit-config.yaml existe
   - ✅ Configuraciones válidas

4. **Estructura del Proyecto**:
   - ✅ Directorio app/ existe
   - ✅ Directorio tests/ existe
   - ✅ Archivos Python detectados

5. **Verificación Funcional**:
   - ✅ Black puede ejecutarse
   - ✅ isort puede ejecutarse
   - ✅ Flake8 puede ejecutarse
   - ✅ Mypy puede ejecutarse

### Salida Esperada

```
==============================================================================
                        Code Quality Tools Validation
==============================================================================

1. Python Environment
[OK] Python version: 3.10.11
[OK] Virtual environment: Active

2. Code Quality Tools
[OK] black: 24.10.0
[OK] isort: 5.13.2
[OK] flake8: 7.1.1
[OK] mypy: 1.13.0
[OK] pre-commit: 4.0.1

3. Configuration Files
[OK] pyproject.toml: exists
[OK] .flake8: exists
[OK] .pre-commit-config.yaml: exists

4. Project Structure
[OK] app directory: exists
[OK] tests directory: exists
[OK] Python files: 45 files found

5. Tool Execution Tests
[OK] Black can format code
[OK] isort can sort imports
[OK] Flake8 can lint code
[OK] Mypy can type check

==============================================================================
                                   Summary
==============================================================================

Total checks: 25
Passed: 25
Success rate: 100.0%

Environment is ready for code quality checks!

Next steps:
  black app/ tests/          # Format code
  isort app/ tests/          # Sort imports
  flake8 app/ tests/         # Lint code
  mypy app/                  # Type check

See docs/GUIA_CALIDAD_CODIGO.md for complete guide
```

### Si Hay Errores

El script mostrará recomendaciones específicas:

```
Failed checks:
  - black: NOT installed

Recommendations:
1. Activate virtual environment: venv\Scripts\activate
2. Install dev dependencies: pip install -r requirements-dev.txt
3. Verify Python version: python --version (need 3.10+)
```

---

## Ejecución de Herramientas

### Black - Formateo de Código

#### Verificar Qué Cambiaría (Dry Run)

**Check mode** (no modifica archivos):
```bash
black --check app/ tests/
```

**Salida si hay cambios necesarios**:
```
would reformat app/services/auth_service.py
would reformat tests/unit/test_config.py
Oh no! 💥 💔 💥
2 files would be reformatted, 43 files would be left unchanged.
```

**Salida si todo está formateado**:
```
All done! ✨ 🍰 ✨
45 files would be left unchanged.
```

#### Formatear Código

**Formatear todo el proyecto**:
```bash
black app/ tests/
```

**Formatear archivo específico**:
```bash
black app/services/auth_service.py
```

**Formatear con verbose output**:
```bash
black -v app/ tests/
```

#### Opciones Útiles

```bash
# Ver diferencias sin aplicar cambios
black --diff app/

# Formatear solo archivos modificados (git)
black $(git diff --name-only --diff-filter=d | grep '\.py$')

# Excluir directorios específicos
black app/ --exclude 'legacy/'
```

### isort - Ordenamiento de Imports

#### Verificar Imports (Dry Run)

```bash
isort --check-only app/ tests/
```

**Salida si hay cambios necesarios**:
```
ERROR: app/services/auth_service.py Imports are incorrectly sorted and/or formatted.
Skipped 1 files
```

**Salida si todo está ordenado**:
```
Skipped 0 files
```

#### Ordenar Imports

**Ordenar todos los imports**:
```bash
isort app/ tests/
```

**Ordenar archivo específico**:
```bash
isort app/services/auth_service.py
```

**Ver diferencias sin aplicar cambios**:
```bash
isort --diff app/ tests/
```

#### Opciones Útiles

```bash
# Mostrar archivos procesados
isort -v app/ tests/

# Verificar compatibilidad con black
isort --check-only --profile black app/

# Ordenar solo archivos modificados
isort $(git diff --name-only --diff-filter=d | grep '\.py$')
```

### Flake8 - Linting

#### Ejecutar Linting

**Lint completo del proyecto**:
```bash
flake8 app/ tests/
```

**Lint con configuración específica**:
```bash
flake8 app/ tests/ --max-line-length=100
```

**Lint archivo específico**:
```bash
flake8 app/services/auth_service.py
```

#### Salida de Errores

```
app/services/auth_service.py:45:1: E302 expected 2 blank lines, found 1
app/services/auth_service.py:67:80: E501 line too long (105 > 100 characters)
tests/unit/test_config.py:23:1: F401 'os' imported but unused
```

**Formato**: `archivo:línea:columna: código mensaje`

#### Opciones Útiles

```bash
# Mostrar estadísticas
flake8 app/ --statistics

# Mostrar solo errores específicos
flake8 app/ --select=E302,E501

# Ignorar errores específicos
flake8 app/ --ignore=E501

# Generar reporte HTML
flake8 app/ --format=html --htmldir=flake8-report

# Contar errores por tipo
flake8 app/ --count
```

### Mypy - Type Checking

#### Ejecutar Type Checking

**Type check del módulo app**:
```bash
mypy app/
```

**Type check con configuración específica**:
```bash
mypy app/ --ignore-missing-imports --no-strict-optional
```

**Type check archivo específico**:
```bash
mypy app/services/auth_service.py
```

#### Salida de Errores

```
app/services/auth_service.py:45: error: Argument 1 to "login" has incompatible type "str"; expected "int"  [arg-type]
app/config.py:23: error: Need type annotation for "settings"  [var-annotated]
Found 2 errors in 2 files (checked 25 source files)
```

**Formato**: `archivo:línea: error: mensaje [código]`

#### Opciones Útiles

```bash
# Mostrar información detallada
mypy app/ --show-error-codes --pretty

# Verificar solo tipos públicos
mypy app/ --disallow-untyped-defs

# Generar reporte HTML
mypy app/ --html-report mypy-report/

# Type check incremental (más rápido)
mypy app/ --incremental

# Ignorar errores en módulos específicos
mypy app/ --exclude 'app/legacy/'
```

---

## Interpretación de Resultados

### Black - Sin Errores

✅ **Salida esperada**:
```
All done! ✨ 🍰 ✨
45 files would be left unchanged.
```

❌ **Necesita formateo**:
```
would reformat app/services/auth_service.py
Oh no! 💥 💔 💥
1 file would be reformatted, 44 files would be left unchanged.
```

**Acción**: Ejecutar `black app/ tests/` para formatear.

### isort - Sin Errores

✅ **Salida esperada**:
```
Skipped 0 files
```

❌ **Necesita ordenamiento**:
```
ERROR: app/services/auth_service.py Imports are incorrectly sorted
Skipped 1 files
```

**Acción**: Ejecutar `isort app/ tests/` para ordenar imports.

### Flake8 - Sin Errores

✅ **Salida esperada**: (sin output)

❌ **Errores encontrados**:
```
app/services/auth_service.py:45:1: E302 expected 2 blank lines, found 1
app/services/auth_service.py:67:80: E501 line too long (105 > 100 characters)
```

**Códigos de error comunes**:

| Código | Descripción | Solución |
|--------|-------------|----------|
| **E302** | Esperadas 2 líneas en blanco | Agregar línea en blanco |
| **E501** | Línea demasiado larga | Reformatear con Black |
| **F401** | Import no usado | Eliminar import |
| **F841** | Variable no usada | Usar o eliminar variable |
| **E711** | Comparación con None | Usar `is None` |
| **E722** | Bare except | Especificar excepción |

**Acción**: Corregir manualmente o usar herramientas automáticas (Black, isort).

### Mypy - Sin Errores

✅ **Salida esperada**:
```
Success: no issues found in 25 source files
```

❌ **Errores de tipo**:
```
app/services/auth_service.py:45: error: Argument 1 to "login" has incompatible type "str"; expected "int"  [arg-type]
Found 1 error in 1 file (checked 25 source files)
```

**Códigos de error comunes**:

| Código | Descripción | Solución |
|--------|-------------|----------|
| **[arg-type]** | Tipo de argumento incorrecto | Corregir tipo del argumento |
| **[var-annotated]** | Falta anotación de tipo | Agregar type hint |
| **[return-value]** | Tipo de retorno incorrecto | Corregir tipo de retorno |
| **[assignment]** | Asignación incompatible | Verificar tipos |
| **[attr-defined]** | Atributo no definido | Verificar nombre/existencia |

**Acción**: Agregar/corregir type hints en el código.

---

## Pre-commit Hooks

### ¿Qué son Pre-commit Hooks?

Los pre-commit hooks ejecutan automáticamente las herramientas de calidad **antes de cada commit**, asegurando que solo código de calidad llegue al repositorio.

### Instalación

**1. Instalar pre-commit**:
```bash
pip install pre-commit
```

**2. Instalar los hooks**:
```bash
pre-commit install
```

**Verificación**:
```bash
pre-commit --version
```

### Configuración (.pre-commit-config.yaml)

El proyecto ya incluye configuración pre-commit:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
        args: ['--max-line-length=100']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, types-requests]
```

### Uso Diario

#### Commit Normal

Cuando haces commit, los hooks se ejecutan automáticamente:

```bash
git add app/services/auth_service.py
git commit -m "feat: add new authentication method"
```

**Salida**:
```
black....................................................................Passed
isort....................................................................Passed
flake8...................................................................Passed
mypy.....................................................................Passed
[develop abc1234] feat: add new authentication method
 1 file changed, 25 insertions(+), 10 deletions(-)
```

#### Si Fallan los Hooks

```
black....................................................................Failed
- hook id: black
- files were modified by this hook

reformatted app/services/auth_service.py
```

**Acción**:
1. Los archivos fueron modificados automáticamente (Black, isort)
2. Revisar cambios: `git diff`
3. Agregar cambios: `git add app/services/auth_service.py`
4. Reintentar commit: `git commit -m "..."`

#### Saltar Hooks (No Recomendado)

Solo en casos excepcionales:
```bash
git commit -m "WIP: work in progress" --no-verify
```

⚠️ **Advertencia**: Esto omite todas las verificaciones de calidad.

### Ejecutar Pre-commit Manualmente

#### En Todos los Archivos

```bash
pre-commit run --all-files
```

#### En Archivos Staged

```bash
pre-commit run
```

#### Hook Específico

```bash
pre-commit run black --all-files
pre-commit run mypy --all-files
```

### Actualizar Hooks

```bash
pre-commit autoupdate
```

---

## Flujo de Trabajo Diario

### Opción 1: Workflow Automático (Recomendado)

**Con pre-commit hooks instalados**, el flujo es automático:

```bash
# 1. Modificar código
# 2. Agregar cambios
git add .

# 3. Commit (hooks se ejecutan automáticamente)
git commit -m "feat: add new feature"

# 4. Push si todo pasa
git push
```

### Opción 2: Workflow Manual

**Sin pre-commit hooks**, ejecutar manualmente antes de commit:

```bash
# 1. Modificar código

# 2. Formatear código
black app/ tests/
isort app/ tests/

# 3. Verificar calidad
flake8 app/ tests/
mypy app/

# 4. Si todo pasa, hacer commit
git add .
git commit -m "feat: add new feature"
git push
```

### Opción 3: Script Automatizado

Usar el script de calidad completo:

**Windows**:
```bash
scripts\run_quality_checks.bat
```

**Linux/Mac**:
```bash
./scripts/run_quality_checks.sh
```

**Este script ejecuta**:
1. ✅ Black (formateo)
2. ✅ isort (imports)
3. ✅ Flake8 (linting)
4. ✅ Mypy (type checking)
5. ✅ Pytest (tests)

### Workflow Antes de Pull Request

```bash
# 1. Ejecutar calidad completa
scripts\run_quality_checks.bat  # Windows
./scripts/run_quality_checks.sh  # Linux/Mac

# 2. Ejecutar tests
pytest

# 3. Verificar coverage
pytest --cov=app --cov-report=term-missing

# 4. Si todo pasa, crear PR
git push origin feature-branch
```

### Integración con CI/CD

El pipeline de GitHub Actions ejecuta automáticamente:

```yaml
- name: Code Quality Checks
  run: |
    black --check app/ tests/
    isort --check-only app/ tests/
    flake8 app/ tests/ --max-line-length=100
    mypy app/ --ignore-missing-imports

- name: Run Tests
  run: |
    pytest --cov=app --cov-report=xml
```

**Esto asegura que**:
- ✅ Solo código formateado llega a main
- ✅ No hay errores de linting
- ✅ Type hints son correctos
- ✅ Tests pasan

---

## Troubleshooting

### Problema 1: "black: command not found"

**Causa**: Black no está instalado o el venv no está activo.

**Solución**:
```bash
# Activar venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Verificar instalación
pip show black

# Si no está instalado
pip install black
```

### Problema 2: "flake8: Module not found"

**Causa**: Flake8 no está en el path del virtual environment.

**Solución**:
```bash
# Reinstalar flake8
pip uninstall flake8
pip install flake8

# Verificar
flake8 --version
```

### Problema 3: Black y Flake8 Conflictos

**Síntoma**: Flake8 reporta errores E203, W503 que Black ignora.

**Solución**: Configurar `.flake8` para ignorar estos códigos:
```ini
[flake8]
ignore =
    E203,  # whitespace before ':'
    W503   # line break before binary operator
```

### Problema 4: Mypy "No module named 'app'"

**Causa**: Mypy no encuentra el módulo app.

**Solución**:
```bash
# Ejecutar desde el directorio raíz
cd c:\My Program Files\workspace-flask\registrojornada-application-python

# Verificar estructura
dir app  # Windows
ls -la app/  # Linux/Mac

# Ejecutar mypy
mypy app/
```

### Problema 5: isort y Black Conflictos

**Síntoma**: isort formatea imports de manera diferente a Black.

**Solución**: Configurar isort para ser compatible con Black:
```toml
[tool.isort]
profile = "black"
```

**O usar directamente**:
```bash
isort --profile black app/ tests/
```

### Problema 6: Pre-commit Hooks No Se Ejecutan

**Causa**: Hooks no están instalados.

**Solución**:
```bash
# Instalar hooks
pre-commit install

# Verificar instalación
ls -la .git/hooks/pre-commit  # Linux/Mac
dir .git\hooks\pre-commit  # Windows

# Ejecutar manualmente
pre-commit run --all-files
```

### Problema 7: Mypy Errores en Third-Party Libraries

**Síntoma**:
```
app/services/notification_service.py:5: error: Cannot find implementation or library stub for module named 'telebot'
```

**Solución**:
```bash
# Opción 1: Ignorar imports faltantes
mypy app/ --ignore-missing-imports

# Opción 2: Instalar stubs (si existen)
pip install types-requests types-beautifulsoup4

# Opción 3: Configurar en pyproject.toml
[tool.mypy]
ignore_missing_imports = true
```

### Problema 8: "Line too long" después de Black

**Causa**: Black tiene límite de 100 pero a veces no puede acortar líneas (strings, comentarios).

**Solución**:
```python
# Antes:
very_long_string = "This is a very long string that cannot be automatically shortened by Black"

# Después:
very_long_string = (
    "This is a very long string that cannot be "
    "automatically shortened by Black"
)
```

### Problema 9: Hooks Muy Lentos

**Causa**: Mypy type checking puede ser lento en proyectos grandes.

**Solución**:
```bash
# Usar caché incremental
mypy app/ --incremental

# O deshabilitar mypy en pre-commit (ejecutar manualmente)
# Comentar mypy en .pre-commit-config.yaml
```

### Problema 10: "ImportError" en Validation Script

**Causa**: Script no encuentra módulos del proyecto.

**Solución**:
```bash
# Ejecutar desde directorio raíz
cd c:\My Program Files\workspace-flask\registrojornada-application-python

# Verificar PYTHONPATH
echo %PYTHONPATH%  # Windows
echo $PYTHONPATH  # Linux/Mac

# Ejecutar script
python scripts\validate_quality_tools.py
```

---

## Scripts de Automatización

### validate_quality_tools.py

**Ubicación**: `scripts/validate_quality_tools.py`

**Qué hace**:
- Verifica instalación de herramientas
- Valida archivos de configuración
- Ejecuta tests funcionales de cada herramienta
- Genera reporte de estado

**Uso**:
```bash
python scripts\validate_quality_tools.py
```

### run_quality_checks.bat / .sh

**Ubicación**:
- Windows: `scripts/run_quality_checks.bat`
- Linux/Mac: `scripts/run_quality_checks.sh`

**Qué hace**:
- Ejecuta todas las herramientas en orden
- Reporta éxitos/fallos
- Detiene en primer error (fail-fast)

**Uso**:
```bash
# Windows
scripts\run_quality_checks.bat

# Linux/Mac
./scripts/run_quality_checks.sh

# Con opciones
scripts\run_quality_checks.bat --fix  # Auto-fix con Black/isort
scripts\run_quality_checks.bat --skip-mypy  # Saltar mypy
```

### quick_fix_quality.bat / .sh

**Ubicación**:
- Windows: `scripts/quick_fix_quality.bat`
- Linux/Mac: `scripts/quick_fix_quality.sh`

**Qué hace**:
- Ejecuta Black y isort para auto-fix
- No ejecuta verificaciones (solo fixes)

**Uso**:
```bash
# Windows
scripts\quick_fix_quality.bat

# Linux/Mac
./scripts/quick_fix_quality.sh
```

---

## Resumen de Comandos

### Comandos Esenciales

```bash
# Validar entorno
python scripts\validate_quality_tools.py

# Formatear código (auto-fix)
black app/ tests/
isort app/ tests/

# Verificar calidad (check only)
black --check app/ tests/
isort --check-only app/ tests/
flake8 app/ tests/
mypy app/

# Ejecutar todo (script automatizado)
scripts\run_quality_checks.bat  # Windows
./scripts/run_quality_checks.sh  # Linux/Mac

# Pre-commit hooks
pre-commit install               # Instalar
pre-commit run --all-files       # Ejecutar manualmente
```

### Comandos por Frecuencia

**Diariamente** (antes de cada commit):
```bash
black app/ tests/
isort app/ tests/
flake8 app/ tests/
```

**Antes de PR**:
```bash
scripts\run_quality_checks.bat
pytest
```

**Semanalmente** (mantenimiento):
```bash
pre-commit autoupdate
pip list --outdated
```

---

## Métricas de Calidad

### Objetivos del Proyecto

| Métrica | Objetivo | Estado Actual |
|---------|----------|---------------|
| **Black Coverage** | 100% | 🎯 100% |
| **isort Coverage** | 100% | 🎯 100% |
| **Flake8 Score** | 0 errores | ✅ 0 errores |
| **Mypy Coverage** | >80% typed | ⚠️ ~60% |
| **Pre-commit** | Instalado | ✅ Activo |

### Mejoras Futuras (Phase 7-8)

- [ ] Aumentar type hints a >90%
- [ ] Configurar pylint adicional
- [ ] Añadir bandit (security linting)
- [ ] Configurar radon (complexity metrics)
- [ ] Dashboard de métricas de calidad

---

## Referencias

### Documentación Oficial

- **Black**: https://black.readthedocs.io/
- **isort**: https://pycqa.github.io/isort/
- **Flake8**: https://flake8.pycqa.org/
- **Mypy**: https://mypy-lang.org/
- **Pre-commit**: https://pre-commit.com/

### PEPs Relevantes

- **PEP 8**: Style Guide for Python Code
- **PEP 484**: Type Hints
- **PEP 526**: Syntax for Variable Annotations
- **PEP 3107**: Function Annotations

### Recursos del Proyecto

- **Guía de Testing**: [docs/GUIA_TESTING.md](GUIA_TESTING.md)
- **Roadmap**: [docs/NEXT_STEPS.md](NEXT_STEPS.md)
- **Fase 4 Docs**: [docs/fases/FASE4_TESTING.md](fases/FASE4_TESTING.md)

---

**Última actualización**: 2025-12-09
**Versión**: 1.0
**Mantenedor**: Equipo de Desarrollo RegistroJornada Bot
