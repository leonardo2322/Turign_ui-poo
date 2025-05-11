import flet as ft


class Dialog:
    def __init__(self,page:ft.Page, title:str="titulo", content_text:list=[],icon:ft.icons=ft.icons.INFO,color_icon:str="#80DAEB",action_def=None,btn_icon:ft.icons=None,btn_ok:str= None,btn_cancel:str = None,win_height= None,btn_data = None,*args, **kwargs):
        self.page = page
        self.title = title
        self.content_text = content_text
        self.dialog = None
        self.icon = icon
        self.color= color_icon
        self.action_def = action_def
        self.name_btn_ok = btn_ok
        self.btn_name_cancel = btn_cancel
        self.btn_icon = btn_icon
        self.win_height = win_height
        self.btn_data = btn_data
    @classmethod    
    def from_data(cls,data):
        
        (page,title, content, icon,color, action_def,btn_ok,btn_cancel,btn_icon, win_height,btn_data) = data

        return cls(
            page = page,
            title = title,
            content_text = content,
            icon = icon,
            color_icon= color,
            action_def = action_def,
            btn_ok = btn_ok,
            btn_cancel = btn_cancel,
            btn_icon = btn_icon,
            win_height = win_height,
            btn_data = btn_data
        )
 
    def handle_close(self, e):
        if self.dialog:
            self.content_text = None
            self.page.close(self.dialog)
    def build(self):
        # Crear el diálogo
        if self.dialog:
            self.page.close(self.dialog)
        self.dialog = ft.AlertDialog(
            modal=True,
            adaptive=True,
            icon=ft.Icon(self.icon, size=28,color=self.color),
            bgcolor="#2c3e50",
            title=ft.Text(self.title),
            content=ft.Column(
                width=400,
                height=self.win_height if self.win_height is not None else 0,
                controls=[
                    self.content_text if self.content_text is not None else ft.Text("")
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        
                ),
            actions=[
                    ft.ElevatedButton("Aceptar" if self.name_btn_ok is None else self.name_btn_ok,data=self.btn_data, on_click=self.set_handle_yes_async if  self.action_def is not None else self.handle_close, icon=ft.icons.SAVE if self.btn_icon is None else self.btn_icon),
                    ft.ElevatedButton("Cancelar" if self.btn_name_cancel is None else self.btn_name_cancel, on_click=self.handle_close), 
                ],
            
            
        
        )
        return self.dialog
    
    def set_handle_yes(self,e):
        if self.action_def:
            self.action_def(e)
            self.page.update()
    async def set_handle_yes_async(self,e):
        if self.action_def:
            await self.action_def(e)
            self.page.update()