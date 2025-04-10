import pandas as pd
from flet import BarChart,BarChartGroup,BarChartRod, Column,Text,Colors,border,ChartAxis,ChartAxisLabel,MainAxisAlignment,LineChartData,CrossAxisAlignment,LineChartDataPoint,LineChart,Border,BorderSide,FontWeight,Container,TextStyle,BoxShadow,PieChart,PieChartEvent,PieChartSection
from config.variables import colors_for_charts
import numpy as np
def bar_chart(data:dict,Name):
    

    df = data.reset_index()  # Convierte la Serie en un DataFrame con índices correctos
    df.columns = ["Fecha", "Cantidad"]   
    bar_groups = [
        BarChartGroup(
            x=index,
            bar_rods=[
                BarChartRod(
                    from_y=0,
                    to_y=row["Cantidad"],  # Asegúrate que tengas esta columna
                    tooltip=str(row["Fecha"]),
                    width=40,
                    border_radius=0,
                )
            ]
        )
        for index, row in df.iterrows()
    ]

    bottom_labels = [
        ChartAxisLabel(
            value=index,
            label=Text(f"{row['Fecha']}", size=10, weight=FontWeight.BOLD)
        )
        for index, row in df.iterrows()
    ]

    area_chart = Column(
        controls=[
            Text(f"{Name}"),
            BarChart(
                bar_groups=bar_groups,
                border=border.all(1, Colors.GREY_400),
                tooltip_bgcolor=Colors.with_opacity(0.5, Colors.GREY_300),
                left_axis=ChartAxis(labels_size=40, title=Text(f"{Name}"), title_size=40),
                bottom_axis=ChartAxis(labels=bottom_labels),
                interactive=True
            )
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )
    return area_chart

def lines_chart(data: dict):
    
    # Crear los puntos de datos correctamente
    lins_data_charts = [
        LineChartData(
            data_points=[
                LineChartDataPoint(index, value),
                # LineChartDataPoint(index*2, value*0.3), son varios campos de manera que las lineas en el grafico se muestran largas y muestran todo
                # LineChartDataPoint(index*2.5, value*0.2)     # Ahora bien estructurado
            ],
            stroke_width=8,
            color=colors_for_charts.get(str(index), Colors.GREY),
            curved=True,
            stroke_cap_round=True,
        )
        for index, (titulo, value) in enumerate(data.items())  # Agregar el título
    ]

    # Configurar el eje izquierdo (valores numéricos)
    left_axis = ChartAxis(
        labels=[
            ChartAxisLabel(
                value=value,
                label=Text(f"{value}", size=8, weight=FontWeight.BOLD)
            )
            for _, value in data.items()  # Usamos los valores reales
        ]
    )

    # Configurar el eje inferior (títulos de las categorías)
    bottom_axis = ChartAxis(
        labels=[
            ChartAxisLabel(
                value=index,  # Aquí sí usamos el índice
                label=Container(
                    content=Text(titulo, size=12, weight=FontWeight.BOLD, color=colors_for_charts.get(str(index), Colors.GREY)),
                ),
            )
            for index, (titulo, _) in enumerate(data.items())  # Títulos bien posicionados
        ]
    )

    chart = Column(
        controls=[
            LineChart(
                data_series=lins_data_charts,
                border=Border(bottom=BorderSide(4, Colors.with_opacity(1, Colors.ON_SURFACE))),
                left_axis=left_axis,
                bottom_axis=bottom_axis,
                tooltip_bgcolor=Colors.with_opacity(0.8, Colors.BLUE_GREY),
            ),
            Container(height=80,width=10)
        ],
        wrap=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

    return chart

def pie_chart(data:dict):
    def on_chart_event(e: PieChartEvent):
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        chart.update()
    total =  np.sum(data)
    normal_radius = 50
    hover_radius = 60
    normal_title_style = TextStyle(
        size=8, color=Colors.WHITE, weight=FontWeight.BOLD
    )
    hover_title_style = TextStyle(
        size=20,
        color=Colors.WHITE,
        weight=FontWeight.BOLD,
        shadow=BoxShadow(blur_radius=2, color=Colors.BLACK54),
    )
    chart = PieChart(
        width=300,
        height=300,
        sections=[
            PieChartSection(
                value=val,
                color=colors_for_charts.get(str(index),"other"),
                title=Text(f"{titulo} {(val / total)*100:.2f}%").value,
                title_style=normal_title_style,
                radius=normal_radius
            )    
            for index, (titulo,val) in enumerate(data.items())
        ],
        sections_space=0,
        center_space_radius=40,
        on_chart_event=on_chart_event,
        scale=2,
        expand=True,
    )
    return chart
def analizar_datos_describe(data,columnas):
    df = pd.DataFrame(data, columns=columnas)

    return df
