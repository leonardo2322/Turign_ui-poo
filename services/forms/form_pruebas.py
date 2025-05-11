from flet import TextField, Dropdown,dropdown, Column,MainAxisAlignment, Text,ElevatedButton,icons,Row
from services.pacientes_servicio import Paciente_agente_servicio
from utils.sanitizacion import sanitizar_nombre


class Formulario_pruebas:
    def __init__(self,page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.repo = Paciente_agente_servicio()
        self.label = Text(value="Escriba el nombre de la prueba por favor")
        self.nombre = TextField(label="Nombre",hint_text="Introduzca el nombre")
        self.text_hide = Text(value="")
        self.content = Column(
            controls=[
                self.label,
                self.nombre,
                self.text_hide
            ],
            alignment=MainAxisAlignment.CENTER,
            )
    def build(self):
        return self.content 
    def obtener_datos(self):
        """Obtiene los valores ingresados en los campos"""
        try:
            nombre = sanitizar_nombre(self.nombre.value)
            if len(nombre) > 0:
                return {
                    "Nombre": nombre.capitalize(),
                }
            return None
        except ValueError as e:
            return {"error": str(e)+ ' asegurate de llenar todos los campos y con los datos correctos'}
        
    async def guardar_datos(self):
        try:
            datos = self.obtener_datos()
        except Exception as e:
            return None
        resultado = await self.repo.create_prueba(nombre=datos.get("Nombre"))
        if resultado:
            self.clean()
            return resultado

        else:
            self.clean()
            return None
    def clean(self):
        self.nombre.value = ""
