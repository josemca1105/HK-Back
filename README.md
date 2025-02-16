## HK-Back

# API REST con Django

Descripción breve del proyecto.

## Requisitos

Antes de comenzar, asegúrate de tener instaladas las siguientes herramientas:

- Python 3.8+ (recomendado)
- pip
- virtualenv

## Instalación

Sigue estos pasos para instalar y configurar el proyecto en tu máquina local.

### 1. Clonar el Repositorio

Clona el repositorio desde GitHub a tu máquina local.

### 2. Crear un Entorno Virtual

Crea un entorno virtual para aislar las dependencias del proyecto:

```bash
python -m venv venv
```

Activa el entorno virtual:

```bash
.\venv\Scripts\activate
```

### 3. Instalar Dependencias

Instala todas las dependencias necesarias desde `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar el Proyecto

Copia el archivo de ejemplo de configuración y ajusta los valores según tus necesidades:

```bash
copy .env.example .env
```

Edita el archivo `.env` para configurar las variables de entorno necesarias.

### 5. Aplicar Migraciones

Aplica las migraciones de la base de datos para configurar las tablas iniciales:

```bash
python manage.py migrate
```

### 6. Crear un Superusuario

Crea un superusuario para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

Sigue las instrucciones en pantalla para configurar el superusuario.

### 7. Ejecutar el Servidor de Desarrollo

Finalmente, ejecuta el servidor de desarrollo de Django:

```bash
python manage.py runserver
```

### 8. Acceder al Proyecto

Abre tu navegador web y ve a `http://127.0.0.1:8000`.
