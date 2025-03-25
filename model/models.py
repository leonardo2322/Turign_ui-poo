from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    password = fields.CharField(max_length=255)
    fecha = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)



    def __str__(self):
        return self.name
    
class Paciente(Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=50)
    fecha = fields.DatetimeField(auto_now_add=True)
    Edad = fields.IntField()
    sexo = fields.CharField( max_length=1,choices=[("M","Masculino"),("F","Femenino")])
    servicio_Remitente = fields.CharField(
        max_length=120,
        choices=[
            ("Emergencia pediatrica", "Emergencia pediatrica"),
            ("Emergencia adulto", "Emergencia adulto"),
            ("Consulta externa", "Consulta externa"),
            ("Hospitalizacion", "Hospitalizacion"),
            ("Consulta especial", "Consulta especial")
        ]
    )
    prueba = fields.CharField(
        max_length=120,
        choices=[
            ("orina", "orina"), ("Hematologia", "Hematologia"), ("heces", "heces"),
            ("hiv", "hiv"), ("vdrl", "vdrl"), ("prueba de embarazo", "prueba de embarazo"),
            ("serologia dengue", "serologia dengue"), ("proteina c reactiva", "proteina c reactiva"),
            ("serologia H. pilori", "serologia H. pilori"), ("factor Reumatoide", "factor Reumatoide"),
            ("antigeno Prostatico", "antigeno Prostatico")
        ]
    )
    resultado = fields.CharField(
        max_length=120,
        choices=[("Positivo", "Positivo"), ("Negativo", "Negativo"), ("Pendiente", "Pendiente")],
        default="Pendiente"
    )

    def __str__(self):
        return self.nombre