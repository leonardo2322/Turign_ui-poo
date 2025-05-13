

TORTOISE_ORM = {
    "connections": {
        "default": "postgres://postgres:leo.2322@localhost:5432/turing"  # Reemplaza con tu conexión de base de datos
    },
    "apps": {
        "models": {
            "models": ["model.models","aerich.models"],  # Ruta correcta a tus modelos
            "default_connection": "default",  # Asegúrate de que esta línea esté presente
        }
    }
}