from model.models import Paciente
from tortoise.exceptions import DoesNotExist
from tortoise.functions import Count

class Paciente_agente_repo:

    async def create_paciente(self, nombre, Edad, sexo, servicio_Remitente, prueba, resultado):
        paciente = Paciente(nombre=nombre, Edad=Edad, sexo=sexo, servicio_Remitente=servicio_Remitente, prueba=prueba, resultado=resultado)
        await paciente.save()
        return paciente

    async def get_paciente(self, id):
        try:
            paciente = await Paciente.get(id=id)
            return paciente
        except DoesNotExist:
            return None
    async def get_total_pacientes(self):
        return await Paciente.all().count()  
    async def get_all_pacientes(self, limit=10, offset=0):
        pacientes = await Paciente.all().order_by("id").offset(offset).limit(limit)
        return pacientes
    async def get_pacientes_serivico(self,servicio):
        try:
            pruebas_count = (
                await Paciente.filter(servicio_Remitente=servicio)
                .group_by("prueba")
                .annotate(total=Count("prueba"))
                .values("prueba", "total")
            )
            return pruebas_count
        except DoesNotExist:
            return None
        except Exception as e:
            return {"error": str(e)}
        

    async def get_pacientes_filtered(self,filtro):
        try:
            pruebas_count = (
                await Paciente.filter(filtro)
            )
            return pruebas_count
        except DoesNotExist:
            return None
        except Exception as e:
            return {"error": str(e)}
        
    async def delete_paciente(self, id):
        try:
            paciente = await Paciente.get_or_none(id=id)
            if not paciente:
                return {"error": "El paciente no existe."}
            await paciente.delete()
            return {"success": "Paciente eliminado correctamente."}

        except Exception as e:
            return {"error": f"Error al eliminar paciente: {str(e)}"}
        
    async def update_paciente(self, id, nombre, Edad, sexo, servicio_Remitente, prueba, resultado):
        try:
            # Verificar si el paciente existe
            paciente = await Paciente.filter(id=id).first()
            if not paciente:
                return {"error": "Paciente no encontrado."}
            # Actualizar datos
            paciente.nombre = nombre
            paciente.Edad = Edad
            paciente.sexo = sexo
            paciente.servicio_Remitente = servicio_Remitente
            paciente.prueba = prueba
            paciente.resultado = resultado
            await paciente.save()

            return {"success": True, "message": "Paciente actualizado correctamente."}

        except DoesNotExist:
            return {"error": "Paciente no encontrado."}
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}