from flet import TextField, Dropdown,dropdown, Column,MainAxisAlignment, Text,ElevatedButton,icons,Row
from services.pacientes_servicio import Paciente_agente_servicio
from services.errors_show import mostrar_mensaje_error
from utils.sanitizacion import sanitizar_nombre,sanitizar_edad,sanitizar_sexo

class Inputs_data_paciente:
    def __init__(self,page,disabled_btn, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo = Paciente_agente_servicio()
        self.nombre = TextField(label="Nombre",hint_text="Introduzca el nombre")
        self.edad = TextField(label="Edad",hint_text="Introduzca la edad")
        self.subtitle = Text("Introduzca los datos del paciente",size=20,color="blue")
        self.pruebas = {}
        self.disabled_btn = disabled_btn
        self.page = page
        self.boton_borrar = ElevatedButton(text="Borrar",icon=icons.DELETE,on_click=lambda e:self.borrar_de_la_lista(e))
        self.fin_seleccion = ElevatedButton(text="Fin seleccion",icon=icons.CHECK,on_click=self.terminar_seleccion)
        self.listado_pruebas = Column()
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
                        
                    ],
                    width=350
                )
        self.id_to_nombre = {}
        self.btn_next = ElevatedButton(text="Siguiente",icon=icons.ARROW_FORWARD,on_click=self.manejador)
        self.btn_all = ElevatedButton(text="Todos",icon=icons.ALL_INBOX,on_click=self.btn_todos)
        self.content = Column(
            controls=[
                self.subtitle,
                self.nombre,
                self.edad,
                Text("Sexo"),
                self.sexo,
                Text("Servicio"),
                self.servicio,
                self.btn_next
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

    async def pruebas_disponibles(self):
        pruebas = await self.repo.listar_pruebas()
        self.id_to_nombre = {str(p.id): p.nombre for p in pruebas}
        return [dropdown.Option(prueba.id,prueba.nombre) for prueba in pruebas]
    
    async def manejador(self,e):
        """Manejador para el evento de cambio pantalla en el form"""
        
        try:
            
            botones = Row(controls=[self.btn_next,self.btn_all,self.boton_borrar,self.fin_seleccion])
            datos = self.obtener_datos()
            if 'error' in datos:
                self.content.controls = [
                    ctrl for ctrl in self.content.controls 
                    if not (isinstance(ctrl, Text) and ctrl.color == "red")
                ]
                texto_error = Text(value=datos.get("error"),color="red",size=18)
                self.content.controls.append(texto_error)
                self.content.update()
                return None
            else:
                self.content.controls.clear()
                self.btn_next.text = "Elegir"
                self.btn_next.icon = icons.CHECK
                self.btn_next.on_click = self.guardar_prueba
                texto = Text(value=f"Introdusca las pruebas para el usuario {datos.get("Nombre")}")
                self.content.controls.extend([self.subtitle,texto,self.prueba])
                self.prueba.options = await self.pruebas_disponibles()
                
                self.content.controls.extend([botones,self.listado_pruebas])
                self.content.update()

        except ValueError:
            print("dentra en el error del manejador")
            return None
        
        return True
    def _reset_form(self):
        """Restablecer el formulario a su estado inicial"""
        self.btn_next.text = "Siguiente"
        self.btn_next.icon = icons.ARROW_FORWARD
        self.btn_next.disabled = False
        self.subtitle.value = "Introduzca los datos del paciente"
        self.subtitle.color = "blue"
        self.listado_pruebas.controls.clear()
        self.boton_borrar.disabled = False
        self.fin_seleccion.disabled = False
        controles_iniciales = Column(
            controls=[
                self.subtitle,
                self.nombre,
                self.edad,
                Text("Sexo"),
                self.sexo,
                Text("Servicio"),
                self.servicio,
                self.btn_next
            ],
            alignment=MainAxisAlignment.CENTER,
            expand=True
        )
        self.content.controls.clear()
        self.content.controls.append(controles_iniciales)
        # Actualizar el contenido para que los cambios sean visibles
    async def terminar_seleccion(self,e):
        if len(self.pruebas) > 0:
            self.prueba.disabled = True
            self.btn_next.disabled = True
            self.boton_borrar.disabled = True
            self.btn_all.disabled = True
            self.subtitle.value = "Pruebas seleccionadas Correctamente las pruebas seleccionas \n abajo presiona aceptar para continuar"
            self.subtitle.color = "green"
            self.disabled_btn(e)
            self.fin_seleccion.disabled = True
            self.content.update()
        else:
            self.subtitle.value = "Debes agregar pruebas"
            self.subtitle.color = "red"
            self.content.update()
            return None

    def borrar_de_la_lista(self,e):
        if self.prueba.value != "...":
            self.subtitle.value = "Introduzca los datos del paciente"
            self.subtitle.color = "blue"
            prueba = self.prueba.value
            self.pruebas.pop(prueba, None)
            self.listado_pruebas.controls.clear()
            for prueba in self.pruebas.values():
                self.listado_pruebas.controls.append(Text(value=f"Prueba: {prueba}"))
            self.listado_pruebas.update()
            self.content.update()
        else:
            self.pruebas.clear()
            self.prueba.value = "..."
            self.listado_pruebas.controls.clear()
            self.content.update()
            return None
    
    def btn_todos(self,e):
        print(e)
        for prueba in self.prueba.options:
            if prueba.key != "...":
                self.pruebas[prueba.key] = prueba.text

        print(self.pruebas)
        self.prueba.disabled = True
        self.btn_next.disabled = True
        self.boton_borrar.disabled = True
        self.btn_all.disabled = True
        self.listado_pruebas.controls.append(Text(value="Todas las Pruebas seleccionadas Presiona el boton aceptar para guardar todas las pruebas",color="green",size=18))
        
        self.content.update()
    
    def guardar_prueba(self,e):
        """Guarda la prueba seleccionada en el dropdown"""
        prueba =str(self.prueba.value)
        if prueba != "..." and prueba != None:
            self.subtitle.value = "Introduzca los datos del paciente"
            self.subtitle.color = "blue"
            prueba_nombre = self.id_to_nombre.get(prueba, "Desconocido")
            if prueba not in self.pruebas:
                self.pruebas[prueba] = prueba_nombre
                self.listado_pruebas.controls.append(Text(value=f"Prueba: { prueba_nombre }"))
            self.prueba.value = "..."
            self.prueba.update()
            self.listado_pruebas.update()

            return None
        else:
            self.prueba.value = "..."
            self.subtitle.value = "Debes Elegir una prueba"
            self.subtitle.color = "red"

            self.prueba.update()
            self.listado_pruebas.update()


            return None
    
    async def guardar_Campos(self):
        
        try:
            datos = self.obtener_datos()
            pruebas = [int(prueba) for prueba in self.pruebas.keys()]
        except Exception as e:
            return None
        resultado = await self.repo.create_paciente(
                nombre=datos.get("Nombre"),
                Edad=datos.get("Edad"),
                sexo=datos.get("Sexo"),
                servicio_Remitente=datos.get("Servicio"),
                prueba=pruebas,
                resultado="Pendiente"
            )
        
        if 'error' not in  resultado:
            self.clean()
            self._reset_form()
        else:
            self.clean()
            return None
        self.content.update()
        self.pruebas.clear()
        return resultado
    
    def obtener_datos(self):
        """Obtiene los valores ingresados en los campos"""
        try:
            nombre = sanitizar_nombre(self.nombre.value)
            edad = sanitizar_edad(self.edad.value)
            sexo = sanitizar_sexo(self.sexo.value)
            if self.servicio.value == "..." or not self.servicio.value:
                raise ValueError("debes rellenar todos los campos")
            if not nombre or not edad or sexo == "...":
                raise ValueError("debes rellenar los campos")
            return {
                "Nombre": nombre,
                "Edad": edad,
                "Sexo": sexo,
                "Servicio": self.servicio.value,
            }
        except ValueError as e:
            return {"error": str(e)+ ' asegurate de llenar todos los campos y con los datos correctos'}