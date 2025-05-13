import flet as ft
from connexion import init, close
from tortoise import run_async
from app.ui_iniciar_sesion import UI_iniciar_sesion
from app.ui_principal import UI_Principal
async def main(page:ft.Page):
    page.title = "App!"
    page.window.width = 1470
    def show_dlg(e,data,instancia):
        if data:
            dlg = instancia.from_data(data)
            page.dlg = dlg
            page.open(dlg.build())
            page.update()
        else:
            page.open(instancia.build())
            page.update()
    # await init()
    def route_change(route):
        print(f"📌 Cambiando a la ruta: {page.route}")
        page.views.clear()  # Limpiar las vistas al cambiar de ruta

        if page.route == "/":
            iniciar_sesion = UI_iniciar_sesion(page, show_dlg)
            page.views.append(ft.View("/", [iniciar_sesion.build()]))
        elif page.route == "/Inicio":
            page.views.append(ft.View("/Inicio", controls=[UI_Principal(page,show_dlg)]))
        page.update()


    page.on_route_change = route_change
    page.go(page.route)

    
if __name__ == "__main__":
    # run_async(init())
    ft.app(target=main)
    # run_async(close())