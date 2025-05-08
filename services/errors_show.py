
from flet import SnackBar, Text

def mostrar_mensaje_error(page, mensaje):
    snack = SnackBar(
        content=Text(mensaje),
        open=True,
        show_close_icon=True,
        duration=5000  # En milisegundos
    )
    page.snack_bar = snack
    print(page.snack_bar)
    page.update()