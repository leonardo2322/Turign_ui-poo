from model.models import Paciente,Prueba
from tortoise.exceptions import DoesNotExist
from collections import Counter
from pprint import pprint

class Paciente_agente_repo:
    async def get_all_pruebas(self):
        try:
            pruebas = await Prueba.all().order_by("id")
            return pruebas
        except Exception as e:
            return {"error": str(e)}
        
    async def create_prueba(self,nombre):
        prueba = await Prueba.create(nombre=nombre)
        if prueba:
            return prueba
        else:
            return None
   
    async def create_paciente(self, nombre, Edad, sexo, servicio_Remitente, pruebas, resultado):
        # Aseguramos que pruebas sea una lista, incluso si es una sola prueba.
        
        paciente = Paciente(nombre=nombre, Edad=Edad, sexo=sexo, servicio_Remitente=servicio_Remitente, resultado=resultado)
        await paciente.save()
        
        # Ahora asociamos las pruebas con el paciente (ManyToMany)
        prueba_objects = await Prueba.filter(id__in=pruebas)  # Obtener los objetos Prueba por id
        await paciente.pruebas.add(*prueba_objects)  # Asociamos las pruebas al paciente
        
        return paciente

    async def get_paciente(self, id):
        try:
            paciente = await Paciente.filter(id=id).prefetch_related("pruebas").first()
            return paciente
        except DoesNotExist:
            return None
    
    async def get_total_pacientes(self):
        return await Paciente.all().count()  
    
    async def get_total_pruebas(self):
        return await Prueba.all().values_list("nombre", flat=True)
    async def get_all_pacientes(self, limit=10, offset=0):
        pacientes = await Paciente.all().offset(offset).limit(limit).prefetch_related("pruebas")
        pruebas_dict = {}

        for paciente in pacientes:
            pruebas = await paciente.pruebas.all()
            pruebas_dict[str(paciente.id)] = [prueba.nombre for prueba in pruebas]
        return pacientes, pruebas_dict

    async def get_pacientes_serivicio(self, servicio, fecha=None):
        try:
            consulta = Paciente.all().prefetch_related("pruebas")

            # 👇 Filtrar por servicio si se proporciona
            if servicio:
                consulta = consulta.filter(servicio_Remitente=servicio)

            # 👇 Filtrar por fecha si se proporciona como Q()
            if fecha:
                consulta = consulta.filter(fecha)

            pacientes = await consulta
            resultado = []
            for paciente in pacientes:
                for prueba in paciente.pruebas:
                    resultado.append({
                        "fecha": paciente.fecha,
                        "prueba": prueba.nombre,
                        "servicio_Remitente": paciente.servicio_Remitente,
                        "turno": paciente.turno,
                    })
            pprint(resultado)
            
            # 👇 Contar el total por combinación única
            conteo = Counter(
                (item["fecha"], item["prueba"], item["servicio_Remitente"], item["turno"])
                for item in resultado
            )

            resultado_final = [
                {
                    "fecha": k[0],
                    "prueba": k[1],
                    "servicio_Remitente": k[2],
                    "turno": k[3],
                    "total": v
                }
                for k, v in conteo.items()
            ]
            return resultado_final

        except Exception as e:
            return {"error": str(e)}

        
    async def get_pacientes_filtered(self, filtro):
        try:
            pacientes = await Paciente.filter(filtro).prefetch_related("pruebas")
            pruebas_dict = {}
        
            for paciente in pacientes:
                pruebas = await paciente.pruebas.all()
                pruebas_dict[str(paciente.id)] = [prueba.nombre for prueba in pruebas]
            return pacientes,pruebas_dict
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
    async def delete_prueba(self, id):
        try:
            prueba = await Prueba.get_or_none(id=id)
            if not prueba:
                return {"error": "La prueba no existe."}
            await prueba.delete()
            return {"success": "Prueba eliminada correctamente."}
        except Exception as e:
            return {"error": f"Error al eliminar prueba: {str(e)}"}