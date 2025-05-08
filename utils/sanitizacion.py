import re

def sanitizar_nombre(nombre: str) -> str:
    nombre = nombre.strip()                      # Quita espacios al inicio y final
    nombre = re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]", "", nombre)  # Elimina caracteres raros
    if not nombre:
        raise ValueError("Nombre inválido")
    return nombre.title()[:50] 

def sanitizar_edad(edad_str: str) -> int:
    try:
        edad = int(edad_str)
        if 0 <= edad <= 120:
            return edad
    except ValueError:
        return None
    raise ValueError("Edad inválida")

def sanitizar_sexo(sexo: str) -> str:
    sexo = sexo.strip().upper()
    if sexo in ['M', 'F', 'O']:
        return sexo
    raise ValueError("Sexo inválido (usa M, F u O)")