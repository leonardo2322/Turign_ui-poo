from utils.dialog import Dialog
from flet import ElevatedButton,DataTable,border,BorderSide,DataColumn,colors,Text,Row,DataCell,IconButton,icons,DataRow,Column,Margin,Card,Container,BoxShadow,FontWeight,LinearGradient,alignment,Offset
# funcion para llamar al dialog y se abre
from services.pacientes_servicio import Paciente_agente_servicio
from tortoise.expressions import Q

def dlg_callback(
          self,e,page,title,content,icon=None,color_icon=None,
          action_def=None,btn_ok=None,btn_cancel=None,icon_btn=None,
          win_height=None,btn_data=None,disabled_btn=None):
        # esta es la instancia del dialogo la clase como tal es como decir un base y todo se construye en el momento de ejecucion
        instance_dlg = Dialog
        try:
            #esta es la informacion que necesita el dialogo para mostrarse los iconos y todo lo demas
            data =(
                page,
                title,
                content,
                icon,
                color_icon,
                action_def,
                btn_ok,
                btn_cancel,
                icon_btn,
                win_height,
                btn_data,
                disabled_btn
            )
            # esta funcion viene desde la plantilla main.py y es la que va a mostrar el dialogo
            self.show_dlg(e,data,instance_dlg)
        except Exception as e:
            print("el error es: ",str(e))

class Boton_P(ElevatedButton):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.text = kwargs.get("text","Boton")
        self.icon = kwargs.get("icon",None)
        self.icon_color = kwargs.get("icon_color","white")
        self.bgcolor = kwargs.get("icon_color","#2c3e50")
        self.color = kwargs.get("color","white")
        self.width = kwargs.get("width",100)
        self.height = kwargs.get("height", 40)
        self.on_click = kwargs.get("on_click",None)     
        self.style = kwargs.get("style",None)
        self.data = kwargs.get("data",None)
class CustomCard(Card):
    def __init__(self, title: str, content: str, color: str = "#6b6ecc"):
        super().__init__()
        self.content = Container(
            content=Column([
                Text(title, size=22, weight=FontWeight.BOLD, color="white"),
                Text(content, size=16, color="black"),
            ], spacing=10),
            padding=15,
            bgcolor=color,
            width=220,
            border_radius=10,
            gradient=LinearGradient(
                begin=alignment.top_left,
                end=alignment.bottom_right,
                colors=["#04051dea", "#2b566e"]
            ),
            shadow=BoxShadow(
                blur_radius=7,
                spread_radius=-7,
                offset=Offset(0, 10),
                color=colors.BLUE_400,
            ),
        )

class DataTableManager(Column):
    def __init__(self, main,listar,dlg,page,listar_prueba,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main
        self.listar = listar
        self.show_dlg = dlg
        self.listar_prueba = listar_prueba
        self.page = page
        self.head_table = None
        self.margin = Margin(left=10, top=10, right=10, bottom=20)
    def create_data_table(self, head_table, table_items, data=None):
        """
        Genera una tabla con los datos proporcionados.
        
        Parámetros:
            head_table (str): Nombre de la tabla.
            table_items (list): Lista de encabezados.
            data (list, opcional): Lista de tuplas con los datos.

        Retorna:
            ft.DataTable: Una instancia de DataTable con los datos cargados.
        """
        self.head_table = head_table
        # Mapeo de clases según el tipo de tabla
        clases = {
            "Pacientes": Paciente_agente_servicio,
            "Pruebas": Paciente_agente_servicio,
            # "ingredientes": Ingredientes,
            # "receta": Receta,
            # "cantidad_ingredientes": Cant_ing_x_receta
        }
        clase = clases.get(head_table, None)

        table = DataTable(
            expand=True,
            border=border.all(0.7, "black"),
            border_radius=10,
            vertical_lines=BorderSide(0.7, "black"),
            horizontal_lines=BorderSide(0.7, "black"),
            bgcolor="#F5EDED",
            data_row_color="#CAF4FF",
            heading_row_color="#E2DAD6",
            columns=[
                DataColumn(
                    label=Text(
                        "Fecha " if item == "fecha" else item,
                        color=colors.BLACK
                    )
                ) for item in table_items
            ] + [
                DataColumn(label=Text("Opciones", color=colors.BLACK))
            ]
        )

        # Si hay datos, crea las filas
        if data:
            table.rows = [
            DataRow(
                cells=[
                    DataCell(
                        Text(f"{cell:.4f}" if isinstance(cell, float) and i in [5, 8] else cell,
                             size=12, color=colors.BLACK)
                    ) for i, cell in enumerate(row)
                ] + [
                    DataCell(Row(controls=[
                        # IconButton(icon="create", on_click=lambda e, r=row: self.edit_row(r, e, clase)),
                        IconButton(icon=icons.DELETE, icon_color="red", data={"row":row,"row_id":row[0],"nombre":row[2]if self.head_table =="Pacientes" else row[1]}, on_click=lambda e:self.permiso_eliminar(e, clase)),
                    ], spacing=12))
                ]
            ) for row in data
        ]
        return table

    

    def edit_row(self,e, clase):
        """Método para editar una fila"""
        print(f"Editando:  en la clase {clase}")
        # Aquí podrías abrir un modal o actualizar datos en la base
    def permiso_eliminar(self,e,clase):
        data = e.control.data
        row_id = data.get("row_id")
        nombre = data.get("nombre")
        dlg_callback(self,e=e,page=self.page,content=Text("Presiona aceptar para eliminar si estas seguro"),title=f"Estas seguro de querer Eliminar a {nombre}",icon=icons.WARNING,color_icon="red",action_def=self.delete_row(row_id,clase,nombre),win_height=200,icon_btn=icons.DELETE)
        
    def delete_row(self, row_id, clase,nombre):
        """Método para eliminar una fila"""
        # Aquí podrías ejecutar la lógica de eliminación de la base de d
        
        
        async def on_delete_click(e):

            instancia = clase()
            if self.head_table == "Pacientes":
                resultado = await instancia.delete_paciente(id=row_id)
                await self.listar(e)

            elif self.head_table == "Pruebas":
                resultado = await instancia.delete_prueba(id=row_id)
                await self.listar_prueba(e)
            if 'success' in resultado:
                dlg_callback(self,e=e,page=self.page,content=Text("El usuario ha sido eliminado exitosamente"),title=f"eliminaste a {nombre}",icon=icons.CHECK,color_icon="green",win_height=200,icon_btn=icons.CHECK)
            self.main.update()
            
        return on_delete_click



    
# async def actualizar_turnos():
#     pacientes = await Paciente.all()

#     for paciente in pacientes:
#         if paciente.fecha:  # Verifica que la fecha existe
#             hora = paciente.fecha.time()
#             paciente.turno = "Día" if time(7, 0) <= hora < time(19, 0) else "Noche"
#             await paciente.save()

# async def actualizar(self,e):

#     async def wrapper(e):
#         result = await actualizar_turnos()
#         print(result,"en resultado")
#     await wrapper(e) 
#     return wrapper