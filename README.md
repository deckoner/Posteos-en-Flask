# Posteos En Flask
Bienvenido al proyecto **Flask Pruebas**. Esta es una aplicación web construida con Flask que use para aprender a usar las diferentes tecnologias de Flask y pydoc para la documentacion.

## Características Principales
*   **Autenticación de Usuarios**: Segura y completa usando `Flask-Login` (Registro, Login, Logout).
*   **Gestión de Base de Datos**: Uso de `Flask-SQLAlchemy` para el ORM.
*   **Formularios Seguros**: Implementación con `Flask-WTF` y protección CSRF.
*   **Generación de Documentación**: Script personalizado para generar documentación técnica automátiacmente.

## Requisitos Previos
Asegúrate de tener instalado Python 3.8 o superior

## Instalación y Configuración
Sigue estos pasos para configurar el proyecto en tu máquina local:
1.  **Crear y activar el entorno virtual**:
    *   Windows:
        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```
    *   macOS/Linux:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

2.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar variables de entorno** (Opcional):
    El proyecto usa una configuración por defecto en `config.py`.

## Ejecución de la Aplicación
Para iniciar el servidor de desarrollo:

```bash
python manage.py
```

La aplicación estará disponible en: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Documentación
El proyecto incluye un script para generar documentación técnica en formato HTML usando `pdoc`.

Para generar la documentación:

```bash
python build_docs.py
```

Los archivos generados se guardarán en la carpeta `docs/`.

## Estructura del Proyecto
```
FlaskPruebas/
├── app/                 # Paquete principal de la aplicación
│   ├── auth/            # Blueprint de autenticación
│   ├── main/            # Blueprint principal (vistas generales)
│   ├── static/          # Archivos estáticos (CSS, JS, imágenes)
│   ├── templates/       # Plantillas HTML (Jinja2)
│   ├── __init__.py      # Inicialización y App Factory
│   └── models.py        # Modelos de base de datos
├── docs/                # Documentación generada
├── uploads/             # Carpeta para subida de archivos
├── build_docs.py        # Script para generar documentación
├── config.py            # Configuraciones de la app
├── manage.py            # Script de entrada y gestión
└── requirements.txt     # Dependencias del proyecto
```
