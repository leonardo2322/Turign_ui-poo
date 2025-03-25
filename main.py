import flet as ft
from connexion import init, close
from tortoise import run_async
import asyncio
from app.ui_iniciar_sesion import UI_iniciar_sesion

async def main(page:ft.Page):
    page.title = "App!"
    page.window.width = 1470
    def show_dlg(e,data,instancia):
        if data:
            page.open(instancia.build(instancia.from_data(data)))
            page.update()
        else:
            page.open(instancia.build())
            page.update()
    # await init()
    iniciar_sesion = UI_iniciar_sesion(page,show_dlg)
    page.add(iniciar_sesion.build())
    page.update()
if __name__ == "__main__":
    # run_async(init())
    ft.app(target=main)
    # run_async(close())