from tortoise import fields
from tortoise.models import Model
from datetime import time, datetime
from tortoise.contrib.pydantic import pydantic_model_creator

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    password = fields.CharField(max_length=255)
    fecha = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)



    def __str__(self):
        return self.name
    
class Prueba(Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=120, unique=True)
    fecha = fields.DatetimeField(auto_now_add=True)
    def __str__(self):
        return self.nombre


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
    pruebas: fields.ManyToManyRelation["Prueba"] = fields.ManyToManyField(
        "models.Prueba", related_name="pruebas", through="paciente_pruebas"
    )
    resultado = fields.CharField(
        max_length=120,
        choices=[("Positivo", "Positivo"), ("Negativo", "Negativo"), ("Pendiente", "Pendiente"),("Reactivo","Reactivo"),("NO Reactivo","NO Reactivo")],
        default="Pendiente"
    )
    turno = fields.CharField(max_length=10,null=True)
    def __str__(self):
        return self.nombre

    async def save(self, *args, **kwargs):
        if self.fecha:
            hora = self.fecha.time()
        else:
            # Si no hay fecha, usa la hora actual del sistema
            hora = datetime.now().time() # O asigna un valor predeterminado
        if time(7, 0) <= hora < time(19, 0):
            self.turno = "Día"
        else:
            self.turno = "Noche"
        await super().save(*args, **kwargs)

