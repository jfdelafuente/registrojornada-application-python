#!/usr/bin/env python
"""
Script para encriptar secretos de forma segura.

Este script genera una clave de encriptación y encripta las credenciales
para almacenarlas de forma segura en el archivo .env

Uso:
    python scripts/encrypt_secrets.py

El script generará la salida que debe copiarse al archivo .env
"""

import sys
from pathlib import Path

# Añadir app al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))

from security.secrets_manager import SecretsManager


def print_separator():
    """Imprime separador visual."""
    print("=" * 70)


def main():
    """Función principal del script de encriptación."""
    print_separator()
    print("🔐 GENERADOR DE SECRETOS ENCRIPTADOS")
    print_separator()
    print()

    # Generar clave de encriptación
    print("Generando clave de encriptación...")
    encryption_key = SecretsManager.generate_key()
    print("✓ Clave generada exitosamente")
    print()

    print_separator()
    print("PASO 1: Copie esta clave al archivo .env")
    print_separator()
    print(f"\nENCRYPTION_KEY={encryption_key}\n")
    print("IMPORTANTE: Guarde esta clave de forma segura.")
    print("Si la pierde, deberá volver a encriptar todos los secretos.")
    print()

    # Solicitar credenciales
    print_separator()
    print("PASO 2: Ingrese las credenciales a encriptar")
    print_separator()
    print()

    try:
        # Bot Token
        print("1. Token del Bot de Telegram")
        bot_token = input("   BOT_TOKEN: ").strip()
        if not bot_token:
            print("❌ Error: El token del bot no puede estar vacío")
            return 1

        # Chat ID
        print("\n2. Chat ID de Telegram")
        chat_id = input("   CHAT_ID: ").strip()
        if not chat_id:
            print("❌ Error: El chat ID no puede estar vacío")
            return 1

        # Usuario ViveOrange
        print("\n3. Usuario de ViveOrange")
        username = input("   USUARIO: ").strip()
        if not username:
            print("❌ Error: El usuario no puede estar vacío")
            return 1

        # Contraseña
        print("\n4. Contraseña de ViveOrange")
        password = input("   PASS: ").strip()
        if not password:
            print("❌ Error: La contraseña no puede estar vacía")
            return 1

        # Código de empleado
        print("\n5. Código de empleado")
        employee_code = input("   COD_EMPLEADO: ").strip()
        if not employee_code:
            print("❌ Error: El código de empleado no puede estar vacío")
            return 1

        print()

        # Encriptar secretos
        print_separator()
        print("PASO 3: Encriptando secretos...")
        print_separator()

        encrypted_bot_token = SecretsManager.encrypt_secret(bot_token, encryption_key)
        encrypted_chat_id = SecretsManager.encrypt_secret(chat_id, encryption_key)
        encrypted_username = SecretsManager.encrypt_secret(username, encryption_key)
        encrypted_password = SecretsManager.encrypt_secret(password, encryption_key)
        encrypted_employee_code = SecretsManager.encrypt_secret(employee_code, encryption_key)

        print("✓ Todos los secretos encriptados exitosamente")
        print()

        # Mostrar resultado
        print_separator()
        print("PASO 4: Copie estas líneas a su archivo .env")
        print_separator()
        print()
        print("# Encryption Key (generada automáticamente)")
        print(f"ENCRYPTION_KEY={encryption_key}")
        print()
        print("# Bot Configuration (encriptado)")
        print(f"BOT_TOKEN_ENCRYPTED={encrypted_bot_token}")
        print(f"CHAT_ID_ENCRYPTED={encrypted_chat_id}")
        print()
        print("# HR System Credentials (encriptado)")
        print(f"HR_USERNAME_ENCRYPTED={encrypted_username}")
        print(f"HR_PASSWORD_ENCRYPTED={encrypted_password}")
        print(f"EMPLOYEE_CODE_ENCRYPTED={encrypted_employee_code}")
        print()

        # Instrucciones adicionales
        print_separator()
        print("INSTRUCCIONES FINALES")
        print_separator()
        print()
        print("1. Copie TODO el contenido anterior a su archivo .env")
        print("2. ELIMINE las variables antiguas sin encriptar:")
        print("   - BOT_TOKEN (sin _ENCRYPTED)")
        print("   - CHAT_ID (sin _ENCRYPTED)")
        print("   - USUARIO")
        print("   - PASS")
        print("   - COD_EMPLEADO")
        print()
        print("3. NUNCA comparta el archivo .env ni la ENCRYPTION_KEY")
        print("4. Asegúrese de que .env está en .gitignore")
        print()
        print("✓ Proceso completado exitosamente")
        print_separator()

        return 0

    except KeyboardInterrupt:
        print("\n\n❌ Proceso cancelado por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
