from flet import TextField, Dropdown, dropdown, Column, MainAxisAlignment, Text, ElevatedButton, icons, Row
from services.pacientes_servicio import Paciente_agente_servicio
from utils.sanitizacion import sanitizar_nombre, sanitizar_edad, sanitizar_sexo


class Inputs_data_paciente:
    def __init__(self, page, disabled_btn, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.repo = Paciente_agente_servicio()
        self.disabled_btn = disabled_btn
        self.pruebas = {}
        self.id_to_nombre = {}

        # Inputs
        self.nombre = TextField(label="Nombre", hint_text="Introduzca el nombre")
        self.edad = TextField(label="Edad", hint_text="Introduzca la edad")
        self.sexo = Dropdown(
            label="Sexo",
            hint_text="Elige una...",
            options=[
                dropdown.Option("...", "elige una opción ..."),
                dropdown.Option("M", "Masculino"),
                dropdown.Option("F", "Femenino"),
            ],
            width=350
        )
        self.servicio = Dropdown(
            label="Servicio",
            hint_text="Elige una...",
            options=[
                dropdown.Option("...", "elige una opción ..."),
                dropdown.Option("Emergencia pediatrica", "Emergencia pediatrica"),
                dropdown.Option("Emergencia adulto", "Emergencia adulto"),
                dropdown.Option("Consulta externa", "Consulta externa"),
                dropdown.Option("Hospitalizacion", "Hospitalizacion"),
                dropdown.Option("Consulta especial", "Consulta especial"),
            ],
            width=350
        )
        self.prueba = Dropdown(
            label="Prueba",
            hint_text="Elige una...",
            options=[dropdown.Option("...", "elige una opción ...")],
            width=350
        )

        # Botones
        self.btn_back = ElevatedButton(text="volver",icon=icons.ARROW_BACK,on_click=self.volver)
        self.btn_next = ElevatedButton(text="Siguiente", icon=icons.ARROW_FORWARD, on_click=self.manejador)
        self.btn_all = ElevatedButton(text="Todas", icon=icons.ALL_INBOX, on_click=self.btn_todos)
        self.boton_borrar = ElevatedButton(text="Borrar", icon=icons.DELETE, on_click=self.borrar_de_la_lista)
        self.fin_seleccion = ElevatedButton(text="Fin selección", icon=icons.CHECK, on_click=self.terminar_seleccion)

        # Estructura
        self.listado_pruebas = Column()
        self.subtitle = Text("Introduzca los datos del paciente", size=20, color="blue")

        self.seccion_datos = Column(controls=[
            self.subtitle,
            self.nombre,
            self.edad,
            Text("Sexo"),
            self.sexo,
            Text("Servicio"),
            self.servicio,
            self.btn_next
        ])

        self.botones_pruebas = Row(controls=[
            self.btn_next,
            self.btn_all,
            self.boton_borrar,
            self.fin_seleccion
        ])

        self.seccion_pruebas = Column(controls=[
            self.prueba,
            self.botones_pruebas,
            self.btn_back,
            self.listado_pruebas
        ], visible=False)

        self.content = Column(
            controls=[self.seccion_datos, self.seccion_pruebas],
            alignment=MainAxisAlignment.CENTER,
            expand=True
        )

    def build(self):
        return self.content

    def mostrar_error(self, mensaje):
        self.subtitle.value = mensaje
        self.subtitle.color = "red"
        self.content.update()

    def limpiar_campos(self):
        self.nombre.value = ""
        self.edad.value = ""
        self.sexo.value = "..."
        self.servicio.value = "..."
        self.prueba.value = "..."

    async def pruebas_disponibles(self):
        pruebas = await self.repo.listar_pruebas()
        self.id_to_nombre = {str(p.id): p.nombre for p in pruebas}
        return [dropdown.Option(str(p.id), p.nombre) for p in pruebas]
    def volver(self,e):
        self.seccion_datos.visible = True
        self.seccion_pruebas.visible = False
        self._reset_form()
        self.content.update()
    async def manejador(self, e):
        datos = self.obtener_datos()
        if 'error' in datos:
            self.mostrar_error(datos['error'])
            return

        self.prueba.options = await self.pruebas_disponibles()
        self.btn_next.text = "Elegir"
        self.btn_next.icon = icons.CHECK
        self.btn_next.on_click = self.guardar_prueba

        self.seccion_datos.visible = False
        self.seccion_pruebas.visible = True
        
        self.subtitle.value = f"Introduce las pruebas para {datos['Nombre']}"
        self.subtitle.color = "blue"
        self.content.update()

    def obtener_datos(self):
        try:
            nombre = sanitizar_nombre(self.nombre.value)
            edad = sanitizar_edad(self.edad.value)
            sexo = sanitizar_sexo(self.sexo.value)
            if not nombre or not edad or sexo == "..." or self.servicio.value == "...":
                raise ValueError("Debes rellenar todos los campos correctamente")
            return {"Nombre": nombre, "Edad": edad, "Sexo": sexo, "Servicio": self.servicio.value}
        except ValueError as e:
            return {"error": str(e)}

    def guardar_prueba(self, e):
        if self.prueba.value not in ("...", None):
            nombre = self.id_to_nombre.get(self.prueba.value, "Desconocido")
            if self.prueba.value not in self.pruebas:
                self.pruebas[self.prueba.value] = nombre
                self.listado_pruebas.controls.append(Text(value=f"Prueba: {nombre}"))
                self.listado_pruebas.update()
            self.prueba.value = "..."
        else:
            self.mostrar_error("Debes seleccionar una prueba")

    def borrar_de_la_lista(self, e):
        if self.prueba.value != "...":
            self.pruebas.pop(self.prueba.value, None)
        else:
            self.pruebas.clear()
        self.actualizar_lista_pruebas()

    def actualizar_lista_pruebas(self):
        self.listado_pruebas.controls.clear()
        for nombre in self.pruebas.values():
            self.listado_pruebas.controls.append(Text(value=f"Prueba: {nombre}"))
        self.listado_pruebas.update()

    def btn_todos(self, e):
        for prueba in self.prueba.options:
            if prueba.key != "...":
                self.pruebas[prueba.key] = prueba.text
        self.listado_pruebas.controls.append(Text(value="Todas las pruebas seleccionadas", color="green", size=18))
        self.prueba.disabled = self.btn_next.disabled = self.boton_borrar.disabled = self.btn_all.disabled = True
        self.content.update()

    async def terminar_seleccion(self, e):
        if not self.pruebas:
            self.mostrar_error("Debes agregar pruebas")
            return
        self.prueba.disabled = self.btn_next.disabled = self.boton_borrar.disabled = self.btn_all.disabled = True
        self.fin_seleccion.disabled = True
        self.subtitle.value = "Pruebas seleccionadas correctamente. Presiona aceptar para continuar."
        self.subtitle.color = "green"
        self.disabled_btn(e)
        self.content.update()

    async def guardar_Campos(self):
        datos = self.obtener_datos()
        if 'error' in datos:
            self.mostrar_error(datos['error'])
            return None

        pruebas = [int(p) for p in self.pruebas]
        resultado = await self.repo.create_paciente(
            nombre=datos["Nombre"],
            Edad=datos["Edad"],
            sexo=datos["Sexo"],
            servicio_Remitente=datos["Servicio"],
            prueba=pruebas,
            resultado="Pendiente"
        )
        if 'error' not in resultado:
            self.limpiar_campos()
            self._reset_form()
        return resultado

    def _reset_form(self):
        self.pruebas.clear()
        self.limpiar_campos()
        self.listado_pruebas.controls.clear()
        self.seccion_pruebas.visible = False
        self.seccion_datos.visible = True

        # Restaurar botones y dropdowns
        self.btn_next.text = "Siguiente"
        self.btn_next.icon = icons.ARROW_FORWARD
        self.btn_next.on_click = self.manejador

        self.prueba.disabled = False
        self.btn_next.disabled = False
        self.boton_borrar.disabled = False
        self.btn_all.disabled = False
        self.fin_seleccion.disabled = False

        self.subtitle.value = "Introduzca los datos del paciente"
        self.subtitle.color = "blue"
        self.content.update()