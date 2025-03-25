from flet import Text, ElevatedButton,Column, Row,Page,icons,Icons, Row, Container,CrossAxisAlignment,MainAxisAlignment, Margin
from app.barra_navegacion import Nav_Bar
from utils.functions import dlg_callback
from config.variables import botones_navegacion, background_app

class UI_Principal(Column):
    def __init__(self,page:Page,dlg,**kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.show_dlg = dlg
        self.func_dlg = dlg_callback
        
        self.main = Column(
            scroll='always',
            width=1400,
            height=800,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
        self.nav = Nav_Bar(destinations=botones_navegacion, bg=background_app,page=self.page,main=self.main,dlg=self.show_dlg)
        
        
        self.controls.append(
            Row(
                controls=[
                    self.nav.build(),
                    self.main
                ],
                scroll="always",
            )
        )

    def cerrar_sesion(self, e):
        self.page.views.pop()  # Elimina la el el inicio y vuelve login
        self.page.go("/")
    