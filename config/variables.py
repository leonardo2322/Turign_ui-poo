from flet import icons,Icons, Container, MainAxisAlignment, Text, Row, ButtonStyle, CrossAxisAlignment, Padding,Column,colors,Colors

botones_navegacion = [
    {"icon": icons.HOME, "selected_icon": icons.HOME_WORK_OUTLINED, "label": "Servicios"},
    {"icon": icons.NOTE_ADD, "selected_icon": icons.NOTE_ADD_OUTLINED, "label": "Registros"},
    {"icon":icons.STACKED_BAR_CHART, "selected_icon": icons.STACKED_BAR_CHART_OUTLINED, "label": "Estadistica"},

    {"icon":Icons.SUBDIRECTORY_ARROW_LEFT, "selected_icon": Icons.SUBDIRECTORY_ARROW_LEFT_OUTLINED, "label": "Cerrar sesion"},
]

colors_for_charts = {
      "0":Colors.PINK,
      "1":Colors.LIGHT_GREEN,
      "2":Colors.CYAN,
      "3":Colors.RED_200,
      "4":Colors.GREEN_ACCENT_700,

      "other":Colors.WHITE
}
head = ["Id","fecha","Nombre","Edad","Sexo","Servicio Remitente","Prueba","Resultado","Turno"]
head_prueba = ["Id","Nombre","Fecha Creado"]
background_app = '#2c3e50'

def turnos(title,data):
    return Container(
          width=1450,
          height=80,
          bgcolor=colors.BLACK38,
          content=Column(alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER,
                         controls=[title]+[item for item in data ])
    )

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