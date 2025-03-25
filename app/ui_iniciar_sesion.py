from flet import Text, Column, Row, TextField,ElevatedButton,MainAxisAlignment, CrossAxisAlignment,Container,Image,ImageFit,Icons,Page,View,icons
from connexion import init, close
from model.models import User
from tortoise import Tortoise
from app.ui_principal import UI_Principal
from utils.functions import dlg_callback

class UI_iniciar_sesion(Row):
    def __init__(self,page:Page,dlg,**kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.show_dlg = dlg
        self.func_dlg = dlg_callback
        self.content = Column()
        self.nombre = TextField(label="nombre", hint_text="Introduzca el nombre")
        self.contraseña = TextField(label="contraseña", hint_text="Introduzca la contraseña",password=True,can_reveal_password=True)
        self.logo = Image(src='../statics/img/remove_paper.png',width=200,height=200,fit=ImageFit.CONTAIN,)
        self.submit = ElevatedButton(text="Iniciar sesion",on_click=self.iniciar_sesion)
        self.content.controls.append(
            Column(
                controls=[
                    self.logo,   
                    self.nombre,
                    self.contraseña,
                    self.submit
                ],
                scroll="always",
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER
            )
        )
    def build(self):
        return self.content

    async def iniciar_sesion(self,e):

        # import bcrypt
        connexion = await init()
        self.page.views.clear()
        self.page.views.append(View("/Inicio", controls=[UI_Principal(self.page,self.show_dlg)]))
        self.page.go("/Inicio")
        # user = await User.filter(name=self.nombre.value).first()
        # if user:
        #     if bcrypt.checkpw(self.contraseña.value.encode(), user.password.encode()):
        #         self.nombre.value = ''
        #         self.contraseña.value = ''
        #         self.page.views.append(View("/Inicio", controls=[UI_Principal(self.page,self.show_dlg)]))
        #         self.page.go("/Inicio") 
        #     else:
        #         self.func_dlg(self,
        #                     e=e, 
        #                     page=self.page, 
        #                     title="Error", 
        #                     content=Text("contraseña invalida verifica e intenta de nuevo"),
        #                     icon=icons.DANGEROUS,
        #                     color_icon="red",
        #                     icon_btn=Icons.BLOCK,
        #                     win_height=200
        #                 )
        # else:
        #     self.func_dlg(self,
        #                     e=e, 
        #                     page=self.page, 
        #                     title="Error", 
        #                     content=Text("Usuario no encontrado"),
        #                     icon=icons.DANGEROUS,
        #                     color_icon="red",
        #                     icon_btn=Icons.BLOCK,
        #                     win_height=200
        #                 )
        await Tortoise.close_connections()