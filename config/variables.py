from flet import icons,Icons, Container, MainAxisAlignment, Text, Row, ButtonStyle, RoundedRectangleBorder, Padding

botones_navegacion = [
    {"icon": icons.HOME, "selected_icon": icons.HOME_WORK_OUTLINED, "label": "Inicio"},
    {"icon": icons.NOTE_ADD, "selected_icon": icons.NOTE_ADD_OUTLINED, "label": "Registros"},
    {"icon":icons.LIST_ALT, "selected_icon": icons.FORMAT_LIST_BULLETED, "label": "Listado"},
    {"icon":Icons.SUBDIRECTORY_ARROW_LEFT, "selected_icon": Icons.SUBDIRECTORY_ARROW_LEFT_OUTLINED, "label": "Cerrar sesion"},


]
head = ["Id","fecha","Nombre","Edad","Sexo","Servicio Remitente","Prueba","Resultado"]
background_app = '#2c3e50'

def container_accion(h=100,botones=[]):
        container_acciones = Container(
            bgcolor=background_app,
            height=h,
            border_radius=10,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                
                controls=[Text("Acciones",color="white",size=20)]+[
                        boton for boton in botones
                ]
            ))

        return container_acciones

# funcion para llamar a eliminar desde el boton a una funcion async

# def create_delete_button_click(self, row, clase):
#     """ Crear un manejador síncrono para el botón de eliminar """
#     async def on_delete_click(e):
#                 # Asegúrate de pasar todos los parámetros a la función asincrónica
#                 await self.delete(r=row, e=e, Instance=clase)
#             return on_delete_click