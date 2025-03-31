from datetime import datetime
from flet import TextField, Dropdown,dropdown, Column,MainAxisAlignment, Text
from services.pacientes_servicio import Paciente_agente_servicio

class Inputs_data_paciente:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo = Paciente_agente_servicio()
        self.nombre = TextField(label="Nombre",hint_text="Introduzca el nombre")
        self.edad = TextField(label="Edad",hint_text="Introduzca la edad")
        
        self.sexo = Dropdown(
                    label="Selecciona una opción",
                    hint_text="Elige una...",
                    label_content="Sexo",
                    options=[
                        dropdown.Option("...","eliga una opción ..."),
                        dropdown.Option("M","Masculino"),
                        dropdown.Option("F","Femenino"),
                    ],
                    width=350

                )
        self.servicio = Dropdown(
                    label="Selecciona una opción",
                    hint_text="Elige una...",
                    label_content="Servicio",
                    options=[
                        dropdown.Option("...","eliga una opción ..."),
                        dropdown.Option("Emergencia pediatrica", "Emergencia pediatrica"),
                        dropdown.Option("Emergencia adulto", "Emergencia adulto"),
                        dropdown.Option("Consulta externa", "Consulta externa"),
                        dropdown.Option("Hospitalizacion", "Hospitalizacion"),
                        dropdown.Option("Consulta especial", "Consulta especial"),
                    ],
                    width=350

                )
        self.prueba = Dropdown(
                    label="Selecciona una opción",
                    hint_text="Elige una...",
                    label_content="Prueba",
                    options=[
                        dropdown.Option("...","eliga una opción ..."),
                        dropdown.Option("Orina", "orina"),
                        dropdown.Option("Heces", "heces"),
                        dropdown.Option("Hematologia", "Hematologia"),
                        dropdown.Option("HIV", "hiv"),
                        dropdown.Option("VDRL", "vdrl"),
                        dropdown.Option("Prueba de embarazo", "prueba de embarazo"),
                        dropdown.Option("Serologia dengue", "serologia dengue"),
                        dropdown.Option("Proteina c reactiva", "proteina c reactiva"),
                        dropdown.Option("Serologia H. pilori", "serologia H. pilori"),
                        dropdown.Option("Factor Reumatoide", "factor Reumatoide"),
                        dropdown.Option("Antigeno Prostatico", "antigeno Prostatico"),
                    ],
                    width=350
                )
        self.content = Column(
            controls=[
                self.nombre,
                self.edad,
                Text("Sexo"),
                self.sexo,
                Text("Servicio"),

                self.servicio,
                Text("Prueba"),

                self.prueba
            ],
            alignment=MainAxisAlignment.CENTER,
            expand=True
        )
    def build(self):
        return self.content
    def clean(self):
        self.nombre.value = ""
        self.edad.value = ""
        self.servicio.value = ""
        self.prueba.value = ""
        self.sexo.value = "..."
        self.servicio.value = "..."
        self.prueba.value = "..."
        
        
    async def guardar_Campos(self):
        
        try:
            datos = self.obtener_datos()
        except Exception as e:
            return None
        resultado = await self.repo.create_paciente(
                nombre=datos.get("Nombre"),
                Edad=datos.get("Edad"),
                sexo=datos.get("Sexo"),
                servicio_Remitente=datos.get("Servicio"),
                prueba=datos.get("Prueba"),
                resultado="Pendiente"
            )
        if resultado:
            self.clean()
        else:
            self.clean()
            return None

        return resultado
    def obtener_datos(self):
        """Obtiene los valores ingresados en los campos"""

        return {
            "Nombre": self.nombre.value,
            "Edad": int(self.edad.value),
            "Sexo": self.sexo.value,
            "Servicio": self.servicio.value,
            "Prueba": self.prueba.value
        }