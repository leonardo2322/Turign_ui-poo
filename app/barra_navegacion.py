from flet import Text,Column, TextField,NavigationRail,NavigationRailLabelType,NavigationRailDestination,icons,Padding,Container,ButtonStyle,RoundedRectangleBorder,CrossAxisAlignment,MainAxisAlignment,Row, ElevatedButton,GridView,TextAlign,colors,FontWeight,Colors
from config.variables import container_accion,head,turnos,head_prueba
from services.logica_form import Inputs_data_paciente,Paciente_agente_servicio
from services.forms.form_pruebas import Formulario_pruebas
from utils.functions import Boton_P, DataTableManager,CustomCard,dlg_callback
from services.estadistica import analizar_datos_describe,bar_chart,lines_chart,pie_chart

class Nav_Bar(Column):
    def __init__(self,destinations,bg,page,main,dlg,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.destinations = destinations if destinations else []
        self.page = page
        self.bg = bg
        self.main = main    
        self.data_Table = DataTableManager(main,listar=self.ejecucion_listar,dlg=dlg,page=page,listar_prueba=self.listado_pruebas)
        self.busqueda = TextField(hint_text="Buscar....",width=270)
        self.contedor_tabla = Column(alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER,scroll='always')
        self.grid = GridView(expand=1, runs_count=4, spacing=15, run_spacing=10)
        self.turno_name = Text("",text_align=TextAlign.CENTER,size=18,weight=FontWeight.BOLD,font_family="Montserrat",color=colors.AMBER_300)
        self.boton_anterior = None
        self.boton_siguiente = None
        self.show_dlg = dlg
        self.form_pacientes = Inputs_data_paciente(page,self.cambiar_estado)
        self.form_pruebas = Formulario_pruebas(page)
        self.agent_paciente = Paciente_agente_servicio()
        
    def build(self):
        return NavigationRail(
            selected_index=0,
            label_type = NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            group_alignment=0.0,
            bgcolor=self.bg,
            destinations=[
                NavigationRailDestination(
                    icon=item.get("icon",icons.HELP_OUTLINE),
                    selected_icon= item.get("selected_icon",icons.HELP),
                    label=item.get("label","--"),
                ) for item in self.destinations
            ],
            height=780,  # Ajusta la altura según tus necesidades
            width=100,   # Ajusta el ancho según tus necesidades
            on_change=self.change_window
        )
    
    def change_window(self, e):
        self.selected_index = e.control.selected_index  # Actualiza el índice seleccionado
        if self.selected_index == 0:
            self.busqueda.value = ""
            if self.contedor_tabla.controls:
                self.contedor_tabla.controls.clear()
            
          
       
            botones = [
                self._crear_boton(text="Dia",on_click=self.cards_servicio,data="Día",width=170,color="white"),
                self._crear_boton(text="Noche",on_click=self.cards_servicio, data="Noche",width=170,color="white"),
                self.busqueda,
                self._crear_boton(text="Buscar",data="Día",on_click=self.cards_servicio,icon=icons.SEARCH,width=170,color="blue"),

            ]
            self.window_selected([container_accion(botones=botones),turnos(self.turno_name,[]),self.grid,Container(width=200,height=80)])
            
        elif self.selected_index == 1:
            #boton para registrar guardado listado y buscar estos botones son de ejcucion de las funciones este a sido de ejemplo pero debo reescribir este codigo y hacerlo mas puro
            self.contedor_tabla.controls.clear()

            if self.grid.controls:
                self.grid.controls.clear()
            botones = [
                self._crear_boton(text="Registrar Paciente", on_click= lambda e:dlg_callback(self,e,self.page,title="Registrar Pacientes",content=self.form_pacientes.build(),icon=icons.SAVE,color_icon="white",action_def=self.ejecucion,win_height=650,disabled_btn=True),width=190,icon=icons.CHECK_CIRCLE_OUTLINE),

                self._crear_boton(text="agg prueba",on_click = lambda e:dlg_callback(self,e,self.page,title="Registrar Pruebas",content=self.form_pruebas.build(),icon=icons.SAVE,color_icon="white",action_def=self.creacion_pruebas,win_height=200),width=190,icon=icons.CHECK_CIRCLE_OUTLINE),
                self._crear_boton(text="Listar pruebas",on_click= self.listado_pruebas, icon=icons.LIST_ALT,width=200),
                self._crear_boton(text="Listado pacientes",
                    icon=icons.LIST_ALT,on_click=self.ejecucion_listar,width=200,),
                self.busqueda,
                self._crear_boton(text="Buscar",
                    icon=icons.SEARCH,on_click=self.buscar_paciente,width=140)
            ]

           #aqui inserto los controles de accion y los botones que estan en el archivo variables
            self.window_selected([container_accion(botones=botones),self.contedor_tabla,Container(
                        width=10,
                        height=200,
                    )])
        elif self.selected_index == 2:
            self.contedor_tabla.controls.clear()

            botones = [
                self._crear_boton(text="mostrar graficos",width=190,on_click = self.cargar_datos_Analizados)
            ]
            self.window_selected([container_accion(botones=botones),self.contedor_tabla])
        elif self.selected_index == 3:
            self.page.views.pop()
            
            self.page.go("/")


    def cambiar_estado(self,e):
        if self.page.dlg.boton_aceptar.disabled:
            self.page.dlg.boton_aceptar.disabled = False
            self.page.dlg.boton_aceptar.update()
            self.page.update()
    def _crear_boton(self, text, icon=None, data=None, on_click=None,bgcolor=None,width=None,color=None):
        return Boton_P(
            text=text,
            icon=icon,
            data=data,
            color=color,
            bgcolor=bgcolor,
            on_click=on_click,
            width=width,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
                shadow_color="black",
                padding=Padding(20, 10, 20, 10)
            )
        )
    # esta funcion se puede poner fuera pero la dejare aqui mientras
    async def cargar_datos_Analizados(self,e):
        async def wrapper():
            pruebas = await self.agent_paciente.all_pacientes()
            return pruebas
        cabecera = ["Id","fecha","Nombre","Edad","Sexo","Servicio Remitente","Prueba","Resultado","Turno"]
        pruebas = await wrapper()

        df = analizar_datos_describe(data=pruebas,columnas=cabecera)
        pacientes_x_fecha = df["fecha"].value_counts()
        pacientes_servicio = df["Servicio Remitente"].value_counts()
        barra_data = bar_chart(pacientes_x_fecha,"Pacientes asistidos en la fecha")
        pie_data = pie_chart(pacientes_servicio)
        self.contedor_tabla.controls.clear()

        self.contedor_tabla.controls.extend([barra_data,Container(width=200,height=80),Text("Sevicio Remitente Grafico de torta",size=22,color=Colors.YELLOW_200),Container(width=200,height=80),pie_data,Container(width=200,height=80)])
        self.page.update()
    
    async def cards_servicio(self,e):
        tarjetas = []
        turno = e.control.data #"Día"
        fecha_filtro = self.busqueda.value.strip()
        self.turno_name.value = f"Turno: {turno} Fecha: {fecha_filtro if fecha_filtro else 'Todos'}"

        async def wrapper():
        # Pasar la fecha si existe
            pruebas_count = await self.agent_paciente.pacientes_servicio(fecha=fecha_filtro or None)
            # print(pruebas_count)
            result_dia = {
                prueba: {
                    "servicios": [s for s in detalles["servicios"] if s["turno"] == turno],
                    "total_general": sum(s["total"] for s in detalles["servicios"] if s["turno"] == turno)
                }
                for prueba, detalles in pruebas_count.items()
                if any(s["turno"] == turno for s in detalles["servicios"])
            }
            if not result_dia:
                tarjeta = CustomCard(
                        title="Sin resultados",
                        content="No hay datos para la fecha y turno seleccionados."
                    )
                tarjetas.append(tarjeta)
                return
            for prueba, datos in result_dia.items():
                servicios = datos["servicios"]
                total_general = datos["total_general"]
                contenido_servicios = "\n".join([f"{s['servicio']}: {s['total']}" for s in servicios])
                contenido = f"{contenido_servicios}\n\nTotal: {total_general}"
                tarjeta = CustomCard(title=prueba, content=contenido)
                tarjetas.append(tarjeta)

        await wrapper()
        self.grid.controls.clear()
        self.grid.controls.extend(tarjetas)
        self.page.update()
    async def creacion_pruebas(self,e):
        resultado = await self.form_pruebas.guardar_datos()
        print(resultado)
        if resultado and not 'error' in resultado:
            self.form_pruebas.text_hide.value = "Se ha agregado de manera correcta la prueba"
            self.form_pruebas.text_hide.color = "green"
            await self.listado_pruebas(e)
        else:
            self.form_pruebas.text_hide.value = "A ocurrido un error  verifica lo que has introducido o ya existe la prueba"
            self.form_pruebas.text_hide.color = "red"

        self.page.update()

    async def listado_pruebas(self,e):
        self.contedor_tabla.controls.clear()
        pruebas = await self.agent_paciente.listar_pruebas()
        data = [(p.id, p.nombre, p.fecha.strftime("%d de %B de %Y - %I:%M %p")) for p in pruebas]

        if data:
            tabla = self.data_Table.create_data_table("Pruebas",head_prueba,data)
            self.contedor_tabla.controls.append(tabla)
        else:
            self.contedor_tabla.controls.append(Text("No se encontraron resultados", color="red"))
        self.page.update()

    async def ejecucion(self,e):
        #guarda los campos del paciente y los lista
        

        resultado = await self.form_pacientes.guardar_Campos()
        if resultado:
            await self.ejecucion_listar(e)
            dlg_callback(self,e,self.page,title="Paciente agregado",content=Text("El paciente ha sido agregado exitosamente"),icon=icons.CHECK_CIRCLE,color_icon="green",win_height=200),
        else:
            dlg_callback(self,e,self.page,title="Error de ingreso",content=Text("has cometido un error verifica y vuelve a intentarlo Debes relleanar todos los campos y la edad en numeros"),icon=icons.DANGEROUS,color_icon="red",win_height=200),
        self.page.update()
    
    async def buscar_paciente(self,e):
        resultado = await self.ejecucion_listar(e,filtrado=self.busqueda.value)
    
    
    def btn_siguiente(self,e,filtado,page):
        async def wrapper(e):
            await self.ejecucion_listar(e,filtado,page)
        return wrapper
    

    def window_selected(self,accion:list):
        self.main.controls.clear()
        self.main.controls.extend(accion)
        self.main.update()
    
    async def ejecucion_listar(self, e, filtrado:str="todos", page:int=1, page_size:int=10):
        try:
            cabecera = head  
            data = None
            total_pacientes = await self.agent_paciente.total_pacientes()

            num_pag = (total_pacientes + page_size - 1) // page_size

            desactivar_siguiente = (page >= num_pag)

            # Obtener datos con paginación
            if filtrado == "todos":
                data = await self.agent_paciente.get_pacientes(page=page, page_size=page_size)
                
            else:
                data = await self.agent_paciente.get_search(filtrado)
                desactivar_siguiente = True
            # Manejo de errores
            if not data or (isinstance(data, dict) and "error" in data):
                self.contedor_tabla.clean()
                self.contedor_tabla.controls.append(Text(f"No se encontraron resultados {data}", color="red"))
            else:

                tabla = self.data_Table.create_data_table("Pacientes", cabecera, data)
                self.contedor_tabla.controls.clear()
                self.contedor_tabla.controls.append(tabla)
                
                numero = Text(f"pagina{page} de {num_pag}")
                # Botones de paginación
                self.boton_anterior = ElevatedButton(
                    "Anterior", 
                    on_click= self.btn_siguiente(e, filtrado, page=max(1, page-1)),
                    disabled=(page <= 1)
                )
                self.boton_siguiente = ElevatedButton(
                    "Siguiente", on_click= self.btn_siguiente(e, filtrado, page=page+1),disabled=desactivar_siguiente
                )
                

                self.contedor_tabla.controls.append(Row(alignment=MainAxisAlignment.CENTER,controls=[self.boton_anterior,numero, self.boton_siguiente]))

            # Actualizar la interfaz
            self.main.update()
            return data

        except Exception as e:
            print(f"Error en ejecucion_listar: {e}")
            self.contedor_tabla.clean()
            self.contedor_tabla.controls.append(Text("Ocurrió un error al listar los datos", color="red"))
            self.main.update()
            return {"error": str(e)}