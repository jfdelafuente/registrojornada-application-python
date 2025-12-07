# REGISTRO DE JORNADA

## Descripción de los directorios y archivos

- app/: Este directorio contendrá el código fuente de tu aplicación.
- init.py: Este archivo indica que la carpeta app es un paquete de Python.
- main.py: Este es el punto de entrada de tu aplicación.
- otros_módulos.py: Otros módulos necesarios para tu aplicación.
- tests/: Aquí se ubicarán los archivos de pruebas unitarias para tu aplicación.
- init.py: Indica que la carpeta tests es un paquete de Python.
- test_main.py: Archivo de pruebas para main.py.
- Dockerfile: Este archivo contendrá las instrucciones para crear la imagen Docker de tu aplicación.
- requirements.txt: Aquí se listarán todas las dependencias de tu aplicación.
- .gitignore: Archivo para especificar los archivos que Git debe ignorar.
- README.md: Documentación del proyecto.

## Ejecutar las pruebas

La forma más fácil de ejecutar pruebas de unittest es usar el descubrimiento automático disponible a través de la interfaz de línea de comandos.

Se utiliza el decorador @patch para simular las respuestas de las solicitudes HTTP y asegurar que las pruebas sean independientes de cualquier conexión externa. Asegúrate de que este archivo esté en el mismo directorio que tu clase BotTelegramRegistro.

- $ > C:\My Program Files\workspace-flask\registrojornada-application-python> python -m unittest -v
