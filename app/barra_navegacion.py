from flet import Text,Column, TextField,NavigationRail,NavigationRailLabelType,NavigationRailDestination,icons,Padding,Container,ButtonStyle,RoundedRectangleBorder,CrossAxisAlignment,MainAxisAlignment,Row, ElevatedButton,GridView
from config.variables import container_accion,head
from utils.functions import dlg_callback
from services.logica_form import Inputs_data_paciente,Paciente_agente_servicio
from utils.functions import Boton_P, DataTableManager,CustomCard

class Nav_Bar(Column):
    def __init__(self,destinations,bg,page,main,dlg,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.destinations = destinations if destinations else []
        self.page = page
        self.bg = bg
        self.main = main    
        self.data_Table = DataTableManager(main,listar=self.ejecucion_listar,dlg=dlg,page=page)
        self.busqueda = TextField(hint_text="Buscar....",width=270)
        self.contedor_tabla = Column(alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER,scroll='always')
        self.grid = GridView(expand=1, runs_count=3, spacing=15, run_spacing=10)
        self.boton_anterior = None
        self.boton_siguiente = None
        self.show_dlg = dlg
        self.form_pacientes = Inputs_data_paciente()
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
            if self.contedor_tabla.controls:
                self.contedor_tabla.clean()

            buscar_btn = Boton_P(text="Todos",
                    icon=icons.CHECK_CIRCLE,
                    color="white",
                    width=170,
                    on_click = self.cards_servicio,
                    style=ButtonStyle(
                                shape=RoundedRectangleBorder(radius=10),
                                shadow_color="black",
                                padding=Padding(20, 10, 20, 10)
                            ))
            
            self.window_selected([container_accion(botones=[buscar_btn]),self.grid,Container(width=200,height=80)])
            
        elif self.selected_index == 1:
            #boton para registrar guardado listado y buscar estos botones son de ejcucion de las funciones este a sido de ejemplo pero debo reescribir este codigo y hacerlo mas puro
            if self.grid.controls:
                self.grid.clean()
            btn_registrar = Boton_P(
                    text="Registrar",
                    icon=icons.NOTE_ADD,
                    color="white",
                    on_click= lambda e:dlg_callback(self,e,self.page,title="Registrar Pacientes",content=self.form_pacientes.build(),icon=icons.SAVE,color_icon="white",action_def=self.ejecucion,win_height=650),
                    width=170,
                    style=ButtonStyle(
                                shape=RoundedRectangleBorder(radius=10),
                                shadow_color="black",
                                padding=Padding(20, 10, 20, 10)
                            )
                    )
            btn_listar = Boton_P(
                    text="Listado pacientes",
                    icon=icons.LIST_ALT,
                    color="white",
                    on_click= self.ejecucion_listar,
                    width=200,
                    style=ButtonStyle(
                                shape=RoundedRectangleBorder(radius=10),
                                shadow_color="black",
                                padding=Padding(20, 10, 20, 10)
                            )
                    )
            btn_buscar = Boton_P(
                    text="Buscar",
                    icon=icons.SEARCH,
                    color="white",
                    on_click= self.buscar_paciente,
                    width=140,
                    style=ButtonStyle(
                                shape=RoundedRectangleBorder(radius=10),
                                shadow_color="black",
                                padding=Padding(20, 10, 20, 10)
                            )
                    )   
           #aqui inserto los controles de accion y los botones que estan en el archivo variables
            self.window_selected([container_accion(botones=[btn_registrar,btn_listar,self.busqueda,btn_buscar]),self.contedor_tabla,Container(
                        width=10,
                        height=200,
                    )])
        elif self.selected_index == 2:
            self.page.go("/listar")
        elif self.selected_index == 3:
            self.page.views.pop()
            self.page.go("/")

    async def cards_servicio(self,e):
        tarjetas = []
        async def wrapper():
            pruebas_count = await self.agent_paciente.pacientes_servicio()
            for servicio, pruebas in pruebas_count.items():
                contenido = "\n".join([f"{prueba}: {total}" for prueba, total in pruebas.items()])
                tarjeta = CustomCard(title=servicio, content=contenido)
                tarjetas.append(tarjeta)
        await wrapper()
        self.grid.controls.clear()
        self.grid.controls.extend(tarjetas)
        self.page.update()
        return wrapper
    async def ejecucion(self,e):
        #guarda los campos del paciente y los lista
        resultado = await self.form_pacientes.guardar_Campos()
        if resultado:
            await self.ejecucion_listar(e)
        self.page.update()
    
    async def buscar_paciente(self,e):
        resultado = await self.ejecucion_listar(e,filtrado=self.busqueda.value)
    
    def btn_siguiente(self,e,filtado,page):
        async def wrapper(e):
            await self.ejecucion_listar(e,filtado,page)
        return wrapper
    
    
    def window_selected(self,accion:list):
        self.main.clean()
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