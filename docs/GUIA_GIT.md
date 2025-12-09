# Guía de Git - RegistroJornada Bot

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Configuración Inicial](#configuración-inicial)
3. [Comandos Básicos](#comandos-básicos)
4. [Flujos de Trabajo Comunes](#flujos-de-trabajo-comunes)
5. [Trabajo con Ramas](#trabajo-con-ramas)
6. [Trabajo con Remoto](#trabajo-con-remoto)
7. [Resolución de Conflictos](#resolución-de-conflictos)
8. [Comandos Avanzados](#comandos-avanzados)
9. [Buenas Prácticas](#buenas-prácticas)
10. [Troubleshooting](#troubleshooting)

---

## Introducción

Esta guía proporciona los comandos Git más comunes y los flujos de trabajo utilizados en el proyecto RegistroJornada Bot.

### ¿Por qué Git?

- **Control de versiones**: Historial completo de cambios
- **Colaboración**: Trabajo en equipo sin conflictos
- **Branches**: Desarrollo paralelo de features
- **Seguridad**: Backup distribuido del código

### Estructura de Branches

```
main/master    ← Producción (estable)
    ↑
develop        ← Desarrollo (integración)
    ↑
feature/*      ← Nuevas características
hotfix/*       ← Correcciones urgentes
```

---

## Configuración Inicial

### Primera Vez con Git

**Configurar identidad**:
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```

**Verificar configuración**:
```bash
git config --list
```

**Configuración recomendada**:
```bash
# Editor por defecto
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "vim"          # Vim

# Colores en terminal
git config --global color.ui auto

# Configurar line endings (Windows)
git config --global core.autocrlf true

# Configurar line endings (Linux/Mac)
git config --global core.autocrlf input

# Alias útiles
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
```

### Clonar el Repositorio

**Clonar proyecto**:
```bash
git clone <repository-url>
cd registrojornada-application-python
```

**Verificar estado**:
```bash
git status
git branch -a
```

---

## Comandos Básicos

### Ver Estado del Repositorio

**Estado actual**:
```bash
git status
```

**Salida típica**:
```
On branch develop
Your branch is up to date with 'origin/develop'.

Changes not staged for commit:
  modified:   app/config.py

Untracked files:
  new_file.py
```

**Estado resumido**:
```bash
git status -s
```

### Ver Historial de Commits

**Historial completo**:
```bash
git log
```

**Historial compacto**:
```bash
git log --oneline
```

**Últimos N commits**:
```bash
git log -n 5
git log --oneline -10
```

**Historial con gráfico**:
```bash
git log --graph --oneline --all
```

**Historial de un archivo**:
```bash
git log -- app/config.py
git log -p app/config.py  # Con diferencias
```

### Ver Diferencias

**Cambios no staged**:
```bash
git diff
```

**Cambios staged**:
```bash
git diff --staged
```

**Diferencias entre commits**:
```bash
git diff HEAD~1 HEAD
git diff abc1234 def5678
```

**Diferencias de un archivo específico**:
```bash
git diff app/config.py
git diff HEAD~1 app/config.py
```

---

## Flujos de Trabajo Comunes

### Flujo 1: Desarrollo de Feature Nueva

**Paso a paso**:

```bash
# 1. Asegurarse de estar en develop actualizado
git checkout develop
git pull origin develop

# 2. Crear rama para la feature
git checkout -b feature/nueva-funcionalidad

# 3. Hacer cambios en el código
# ... editar archivos ...

# 4. Ver qué cambió
git status
git diff

# 5. Agregar cambios al staging
git add app/new_file.py
git add app/modified_file.py
# O agregar todo:
git add .

# 6. Verificar qué se va a commitear
git status

# 7. Hacer commit
git commit -m "feat: add new functionality for user management"

# 8. Push de la rama
git push -u origin feature/nueva-funcionalidad

# 9. Crear Pull Request en GitHub
# (Ir a GitHub y crear PR)

# 10. Una vez aprobado y mergeado, actualizar develop
git checkout develop
git pull origin develop

# 11. Eliminar rama local (opcional)
git branch -d feature/nueva-funcionalidad
```

### Flujo 2: Corrección de Bug

```bash
# 1. Desde develop, crear rama de bugfix
git checkout develop
git pull origin develop
git checkout -b fix/corregir-error-autenticacion

# 2. Hacer correcciones
# ... editar archivos ...

# 3. Agregar y commitear
git add app/services/auth_service.py
git commit -m "fix: resolve authentication timeout issue"

# 4. Push y crear PR
git push -u origin fix/corregir-error-autenticacion
```

### Flujo 3: Trabajo Diario

```bash
# Al iniciar el día
git checkout develop
git pull origin develop
git checkout feature/mi-rama
git merge develop  # Actualizar con últimos cambios

# Durante el día (commits frecuentes)
git add archivo1.py archivo2.py
git commit -m "feat: implement validation logic"

# ... más trabajo ...

git add tests/test_validation.py
git commit -m "test: add validation tests"

# Al final del día
git push origin feature/mi-rama
```

### Flujo 4: Actualizar Rama con Cambios de Develop

```bash
# Estando en tu rama feature
git checkout feature/mi-rama

# Opción A: Merge (preserva historial completo)
git fetch origin
git merge origin/develop

# Opción B: Rebase (historial lineal)
git fetch origin
git rebase origin/develop

# Si hay conflictos, resolverlos y continuar
git add archivo_resuelto.py
git rebase --continue
# o para merge:
git commit
```

### Flujo 5: Hotfix Urgente

```bash
# 1. Crear rama desde main
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-fix

# 2. Hacer fix
# ... editar archivos ...

# 3. Commit
git add app/security/
git commit -m "fix: critical security vulnerability in authentication"

# 4. Push y crear PR urgente
git push -u origin hotfix/critical-security-fix

# 5. Mergear a main Y develop
# (Después de PR aprobado)
git checkout main
git merge hotfix/critical-security-fix
git push origin main

git checkout develop
git merge hotfix/critical-security-fix
git push origin develop
```

---

## Trabajo con Ramas

### Crear y Cambiar de Rama

**Ver ramas**:
```bash
git branch              # Locales
git branch -a           # Todas (locales + remotas)
git branch -r           # Solo remotas
```

**Crear rama**:
```bash
git branch feature/nueva-rama
```

**Cambiar a rama**:
```bash
git checkout feature/nueva-rama
```

**Crear y cambiar en un comando**:
```bash
git checkout -b feature/nueva-rama
```

**Crear rama desde commit específico**:
```bash
git checkout -b feature/nueva-rama abc1234
```

### Renombrar y Eliminar Ramas

**Renombrar rama actual**:
```bash
git branch -m nuevo-nombre
```

**Renombrar otra rama**:
```bash
git branch -m viejo-nombre nuevo-nombre
```

**Eliminar rama local**:
```bash
git branch -d feature/completada      # Safe delete
git branch -D feature/abandonada      # Force delete
```

**Eliminar rama remota**:
```bash
git push origin --delete feature/completada
```

### Mergear Ramas

**Merge simple**:
```bash
git checkout develop
git merge feature/mi-feature
```

**Merge con commit de merge (no fast-forward)**:
```bash
git merge --no-ff feature/mi-feature
```

**Merge con squash (un solo commit)**:
```bash
git merge --squash feature/mi-feature
git commit -m "feat: implement complete feature X"
```

### Comparar Ramas

**Ver diferencias entre ramas**:
```bash
git diff develop..feature/mi-rama
```

**Ver commits únicos en rama**:
```bash
git log develop..feature/mi-rama
```

**Ver archivos diferentes**:
```bash
git diff --name-only develop..feature/mi-rama
```

---

## Trabajo con Remoto

### Ver Remotos

**Lista de remotos**:
```bash
git remote -v
```

**Salida típica**:
```
origin  https://github.com/user/repo.git (fetch)
origin  https://github.com/user/repo.git (push)
```

### Sincronizar con Remoto

**Fetch (traer cambios sin aplicar)**:
```bash
git fetch origin
```

**Pull (fetch + merge)**:
```bash
git pull origin develop
```

**Pull con rebase**:
```bash
git pull --rebase origin develop
```

**Push (enviar cambios)**:
```bash
git push origin feature/mi-rama
```

**Push con tracking**:
```bash
git push -u origin feature/mi-rama
# Después solo:
git push
```

**Forzar push (¡CUIDADO!)**:
```bash
git push --force origin feature/mi-rama
# Más seguro:
git push --force-with-lease origin feature/mi-rama
```

### Trabajar con Tags

**Crear tag**:
```bash
git tag v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
```

**Ver tags**:
```bash
git tag
git tag -l "v1.*"
```

**Push tags**:
```bash
git push origin v1.0.0
git push origin --tags  # Todos los tags
```

**Eliminar tag**:
```bash
git tag -d v1.0.0                    # Local
git push origin --delete v1.0.0     # Remoto
```

---

## Resolución de Conflictos

### Detectar Conflictos

**Durante merge/rebase**:
```
Auto-merging app/config.py
CONFLICT (content): Merge conflict in app/config.py
Automatic merge failed; fix conflicts and then commit the result.
```

### Resolver Conflictos

**Ver archivos con conflictos**:
```bash
git status
```

**Formato de conflicto en archivo**:
```python
<<<<<<< HEAD
# Tu código actual
def authenticate(username, password):
    return validate_credentials(username, password)
=======
# Código entrante
def authenticate(user, pwd):
    return check_credentials(user, pwd)
>>>>>>> feature/new-auth
```

**Pasos para resolver**:

```bash
# 1. Abrir archivo con conflicto
code app/config.py

# 2. Editar manualmente, elegir o combinar código
# Eliminar marcadores <<<<<<< ======= >>>>>>>

# 3. Agregar archivo resuelto
git add app/config.py

# 4. Continuar merge/rebase
git commit  # Para merge
git rebase --continue  # Para rebase
```

### Herramientas de Merge

**Usar merge tool**:
```bash
git mergetool
```

**Configurar VS Code como merge tool**:
```bash
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```

### Abortar Merge/Rebase

**Abortar merge**:
```bash
git merge --abort
```

**Abortar rebase**:
```bash
git rebase --abort
```

---

## Comandos Avanzados

### Stash (Guardar Trabajo Temporal)

**Guardar cambios**:
```bash
git stash
git stash save "WIP: working on authentication"
```

**Ver stashes**:
```bash
git stash list
```

**Aplicar stash**:
```bash
git stash apply           # Último stash
git stash apply stash@{1} # Stash específico
```

**Aplicar y eliminar**:
```bash
git stash pop
```

**Eliminar stash**:
```bash
git stash drop stash@{0}
git stash clear  # Todos
```

### Reset (Deshacer Cambios)

**Reset soft (mantiene cambios staged)**:
```bash
git reset --soft HEAD~1
```

**Reset mixed (mantiene cambios unstaged)**:
```bash
git reset HEAD~1
git reset --mixed HEAD~1  # Mismo efecto
```

**Reset hard (¡ELIMINA cambios!)**:
```bash
git reset --hard HEAD~1
```

**Deshacer staging de archivo**:
```bash
git reset HEAD archivo.py
```

### Revert (Deshacer Commit)

**Revertir último commit**:
```bash
git revert HEAD
```

**Revertir commit específico**:
```bash
git revert abc1234
```

**Revertir sin crear commit**:
```bash
git revert --no-commit abc1234
```

### Cherry-pick (Copiar Commit)

**Copiar commit a rama actual**:
```bash
git cherry-pick abc1234
```

**Copiar múltiples commits**:
```bash
git cherry-pick abc1234 def5678
```

### Reflog (Recuperar Commits)

**Ver historial de operaciones**:
```bash
git reflog
```

**Recuperar commit perdido**:
```bash
git reflog
# Encontrar commit: abc1234
git checkout abc1234
git checkout -b recovery-branch
```

### Bisect (Encontrar Bug)

**Iniciar bisect**:
```bash
git bisect start
git bisect bad           # Commit actual tiene bug
git bisect good abc1234  # Commit que funcionaba
```

**Git probará commits automáticamente**:
```bash
# Probar código
# Si funciona:
git bisect good
# Si tiene bug:
git bisect bad
```

**Terminar bisect**:
```bash
git bisect reset
```

### Clean (Limpiar Archivos)

**Ver qué se eliminará**:
```bash
git clean -n
```

**Eliminar archivos no rastreados**:
```bash
git clean -f
```

**Eliminar directorios también**:
```bash
git clean -fd
```

**Incluir archivos ignorados**:
```bash
git clean -fdx
```

---

## Buenas Prácticas

### Commits

**Mensajes de commit claros**:

```bash
# ❌ Mal
git commit -m "fix"
git commit -m "cambios"
git commit -m "update files"

# ✅ Bien
git commit -m "feat: add user authentication service"
git commit -m "fix: resolve timeout in HTTP client"
git commit -m "docs: update API documentation"
```

**Formato recomendado (Conventional Commits)**:

```
<tipo>: <descripción corta>

<descripción larga opcional>

<footer opcional>
```

**Tipos comunes**:
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formateo, espacios, etc.
- `refactor`: Refactorización de código
- `test`: Añadir/modificar tests
- `chore`: Tareas de mantenimiento

**Ejemplo completo**:
```bash
git commit -m "$(cat <<'EOF'
feat: implement user authentication with JWT

Add complete authentication flow using JWT tokens:
- Login endpoint with credential validation
- Token generation with expiration
- Token refresh mechanism
- Logout with token invalidation

Closes #123
EOF
)"
```

### Commits Frecuentes

```bash
# ✅ Commits pequeños y frecuentes
git commit -m "feat: add User model"
git commit -m "feat: add authentication logic"
git commit -m "test: add authentication tests"

# ❌ Un commit gigante
git commit -m "feat: complete authentication system"
```

### Branches

**Nomenclatura clara**:
```bash
# ✅ Bien
feature/user-authentication
feature/export-reports
fix/login-timeout
hotfix/security-vulnerability

# ❌ Mal
nueva-rama
mis-cambios
test
```

**Una feature por rama**:
```bash
# ✅ Bien
feature/add-user-auth
feature/add-export-pdf

# ❌ Mal
feature/multiple-features  # Muchas cosas juntas
```

### Pull/Push

**Pull antes de push**:
```bash
# Siempre actualizar antes de subir
git pull origin develop
git push origin feature/mi-rama
```

**No hacer force push en ramas compartidas**:
```bash
# ❌ NUNCA en main/develop
git push --force origin develop

# ✅ OK en tu rama personal
git push --force-with-lease origin feature/mi-rama
```

### Code Review

**Antes de crear PR**:
```bash
# 1. Actualizar con develop
git fetch origin
git rebase origin/develop

# 2. Ejecutar tests
pytest

# 3. Verificar calidad
scripts/run_quality_checks.bat full

# 4. Review propio
git diff origin/develop..HEAD

# 5. Push y crear PR
git push origin feature/mi-rama
```

---

## Troubleshooting

### Problema 1: "Your branch has diverged"

**Síntoma**:
```
Your branch and 'origin/develop' have diverged,
and have 3 and 2 different commits each, respectively.
```

**Solución**:
```bash
# Opción A: Merge
git pull origin develop

# Opción B: Rebase (historial limpio)
git pull --rebase origin develop
```

### Problema 2: "Permission denied (publickey)"

**Causa**: SSH keys no configuradas.

**Solución**:
```bash
# Generar SSH key
ssh-keygen -t ed25519 -C "tu.email@ejemplo.com"

# Agregar a ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copiar clave pública y agregar a GitHub
cat ~/.ssh/id_ed25519.pub
# Settings → SSH and GPG keys → New SSH key
```

### Problema 3: "fatal: not a git repository"

**Causa**: No estás en un directorio Git.

**Solución**:
```bash
# Verificar dónde estás
pwd

# Ir al directorio correcto
cd c:\My Program Files\workspace-flask\registrojornada-application-python

# O inicializar nuevo repo
git init
```

### Problema 4: Commit al Branch Equivocado

**Solución**:
```bash
# 1. Guardar commit hash
git log -1
# Commit: abc1234

# 2. Deshacer commit (mantener cambios)
git reset --soft HEAD~1

# 3. Cambiar a rama correcta
git checkout rama-correcta

# 4. Commitear ahí
git commit -m "mensaje"

# O usar cherry-pick:
git checkout rama-correcta
git cherry-pick abc1234
```

### Problema 5: Eliminar Archivo del Historial

**Eliminar archivo sensible del historial**:
```bash
# ⚠️ Reescribe historial - coordinar con equipo
git filter-branch --tree-filter 'rm -f secrets.txt' HEAD

# Más moderno (requiere instalación):
git filter-repo --path secrets.txt --invert-paths
```

### Problema 6: "merge conflict in ..."

**Ver archivos en conflicto**:
```bash
git status
```

**Resolver**:
```bash
# 1. Abrir archivo
code app/config.py

# 2. Resolver conflictos manualmente

# 3. Marcar como resuelto
git add app/config.py

# 4. Completar merge
git commit
```

### Problema 7: Deshacer Push

**Si no lo han pulled otros**:
```bash
git reset --hard HEAD~1
git push --force-with-lease origin feature/mi-rama
```

**Si ya lo pulled alguien**:
```bash
# Crear commit que revierta
git revert HEAD
git push origin feature/mi-rama
```

### Problema 8: .gitignore No Funciona

**Causa**: Archivos ya tracked.

**Solución**:
```bash
# Eliminar de tracking (mantener archivo)
git rm --cached archivo.txt
git rm --cached -r directorio/

# Commit cambios
git commit -m "chore: update .gitignore"
```

### Problema 9: Line Endings (CRLF vs LF)

**Síntoma**:
```
warning: LF will be replaced by CRLF
```

**Solución**:
```bash
# Windows
git config --global core.autocrlf true

# Linux/Mac
git config --global core.autocrlf input

# Normalizar repo
git add --renormalize .
git commit -m "chore: normalize line endings"
```

### Problema 10: Recuperar Archivo Eliminado

**Recuperar archivo eliminado en último commit**:
```bash
git checkout HEAD~1 -- archivo_eliminado.py
```

**Buscar en historial**:
```bash
git log --all -- archivo_eliminado.py
# Ver hash del commit
git checkout abc1234 -- archivo_eliminado.py
```

---

## Comandos de Inspección

### Blame (Quién Cambió Qué)

**Ver autor de cada línea**:
```bash
git blame app/config.py
```

**Con rango de líneas**:
```bash
git blame -L 10,20 app/config.py
```

### Show (Ver Commit)

**Ver detalles de commit**:
```bash
git show abc1234
```

**Ver archivo en commit específico**:
```bash
git show abc1234:app/config.py
```

### Grep (Buscar en Historial)

**Buscar en archivos**:
```bash
git grep "authenticate"
```

**Buscar en historial**:
```bash
git log -S "authenticate" --all
```

---

## Workflows Específicos del Proyecto

### Workflow: Nueva Feature

```bash
# 1. Actualizar develop
git checkout develop
git pull origin develop

# 2. Crear rama
git checkout -b feature/implement-export-pdf

# 3. Desarrollo iterativo
# ... código ...
git add app/services/export_service.py
git commit -m "feat: add PDF export service"

# ... más código ...
git add tests/unit/test_export_service.py
git commit -m "test: add export service tests"

# ... documentación ...
git add docs/API.md
git commit -m "docs: document export API endpoints"

# 4. Actualizar con develop (antes de PR)
git fetch origin
git rebase origin/develop

# 5. Verificar calidad
pytest
scripts/run_quality_checks.bat full

# 6. Push
git push -u origin feature/implement-export-pdf

# 7. Crear PR en GitHub
# 8. Review y merge
# 9. Actualizar local
git checkout develop
git pull origin develop
git branch -d feature/implement-export-pdf
```

### Workflow: Code Review

**Como reviewer**:
```bash
# 1. Fetch rama
git fetch origin feature/nueva-feature

# 2. Checkout para probar
git checkout feature/nueva-feature

# 3. Ver cambios
git diff origin/develop..HEAD

# 4. Probar localmente
pytest
python app/main.py

# 5. Comentar en GitHub PR
# 6. Volver a develop
git checkout develop
```

### Workflow: Hotfix Producción

```bash
# 1. Desde main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug-fix

# 2. Fix
git add app/services/auth_service.py
git commit -m "fix: resolve critical authentication bug"

# 3. Tests
pytest -v

# 4. Push y PR urgente
git push -u origin hotfix/critical-bug-fix

# 5. Merge a main (después de aprobación)
git checkout main
git merge hotfix/critical-bug-fix
git tag v1.0.1
git push origin main --tags

# 6. Merge a develop también
git checkout develop
git merge hotfix/critical-bug-fix
git push origin develop

# 7. Limpiar
git branch -d hotfix/critical-bug-fix
```

---

## Configuración del Proyecto

### .gitignore

**Archivos ignorados comunes**:
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Project specific
.env
secrets.json
logs/
*.log
```

### Pre-commit Hooks

**Instalar hooks**:
```bash
pip install pre-commit
pre-commit install
```

**Archivo [.pre-commit-config.yaml](../.pre-commit-config.yaml)**:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
```

---

## Resumen de Comandos

### Comandos Esenciales Diarios

```bash
# Ver estado
git status

# Actualizar rama
git pull origin develop

# Crear rama
git checkout -b feature/nueva-rama

# Agregar cambios
git add archivo.py
git add .

# Commitear
git commit -m "feat: add new feature"

# Push
git push origin feature/nueva-rama

# Ver historial
git log --oneline
```

### Comandos por Frecuencia

**Diariamente**:
```bash
git status
git pull
git add
git commit
git push
git log
```

**Semanalmente**:
```bash
git branch
git merge
git rebase
git stash
git diff
```

**Ocasionalmente**:
```bash
git tag
git cherry-pick
git revert
git reset
git clean
```

**Raramente**:
```bash
git reflog
git bisect
git filter-branch
```

---

## Atajos y Alias Útiles

### Alias Recomendados

```bash
# Agregar a ~/.gitconfig o ejecutar:
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --graph --oneline --all'
git config --global alias.amend 'commit --amend --no-edit'
```

**Uso**:
```bash
git st              # = git status
git co develop      # = git checkout develop
git br              # = git branch
git ci -m "msg"     # = git commit -m "msg"
git unstage file    # = git reset HEAD file
git last            # = git log -1 HEAD
git visual          # = git log --graph --oneline --all
git amend           # = git commit --amend --no-edit
```

---

## Referencias

### Documentación Oficial

- **Git**: https://git-scm.com/doc
- **GitHub**: https://docs.github.com/
- **Conventional Commits**: https://www.conventionalcommits.org/

### Recursos del Proyecto

- **Guía de Testing**: [GUIA_TESTING.md](GUIA_TESTING.md)
- **Guía de Calidad**: [GUIA_CALIDAD_CODIGO.md](GUIA_CALIDAD_CODIGO.md)
- **Roadmap**: [NEXT_STEPS.md](NEXT_STEPS.md)

### Cheat Sheets

- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Interactive Git Cheat Sheet**: https://ndpsoftware.com/git-cheatsheet.html

---

**Última actualización**: 2025-12-09
**Versión**: 1.0
**Mantenedor**: Equipo de Desarrollo RegistroJornada Bot
