from repositories.Pacientes import Paciente_agente_repo
from tortoise.expressions import Q
from datetime import datetime,timedelta
#F:21-03-2025
def parse_fecha(valor):
    try:
        fecha_obj = datetime.strptime(valor, "%d-%m-%Y")
        fecha_siguiente = fecha_obj + timedelta(days=1)
        return Q(fecha__gte=fecha_obj, fecha__lt=fecha_siguiente)
    except ValueError:
        return None


class Paciente_agente_servicio:
    def __init__(self):
        self.paciente_agente_repo = Paciente_agente_repo()

    def validar_paciente(self, nombre, Edad, sexo, servicio_Remitente, prueba):
        if not isinstance(nombre, str) or not nombre.strip():
            return {"error": "El nombre debe ser una cadena no vacía."}
        if not isinstance(Edad, int) or Edad < 0:
            return {"error": "La edad debe ser un número entero positivo."}
        if sexo not in ["M", "F"]:
            return {"error": "Sexo inválido. Usa 'M' o 'F'."}
        if servicio_Remitente == "...":
            return {"error": "Seleccione un servicio"}
        if prueba == "...":
            return {"error": "Seleccione una prueba"}

        return None
    async def listar_pruebas(self):
        try:
            pruebas = await self.paciente_agente_repo.get_all_pruebas()
            if not pruebas:
                return []
            return pruebas
        except Exception as e:
            return {"error": str(e)}
    async def create_prueba(self,nombre):
        if not isinstance(nombre,str) or not nombre.strip():
            return {"error":"el nombre no debe ser una cadena vacia introduzca un campo valido"}
        try:
            resultado = await self.paciente_agente_repo.create_prueba(nombre=nombre)
            return resultado if resultado else {"error no se pudo crea el paciente."}
        except Exception as e:
            return {"error":str(e)}
    async def create_paciente(self, nombre, Edad, sexo, servicio_Remitente, prueba, resultado):
        error = self.validar_paciente(nombre, Edad, sexo, servicio_Remitente, prueba)
        if error:
            return error

        # Convertir la prueba a una lista si es solo una
        if isinstance(prueba, str):
            prueba = [prueba]
        print(prueba)
        try:
            paciente = await self.paciente_agente_repo.create_paciente(nombre=nombre,Edad=Edad,sexo=sexo, servicio_Remitente=servicio_Remitente,pruebas= prueba, resultado=resultado)
            return paciente if paciente else {"error": "No se pudo crear el paciente."}
        except Exception as e:
            return {"error": str(e)}
    def order_pacientes_pruebas(self,pacientes):
        data = [
            (
                paciente.id,
                paciente.fecha.strftime("%d-%m-%Y"),
                paciente.nombre,
                paciente.Edad,
                paciente.sexo,
                paciente.servicio_Remitente,
                ", ".join(pacientes[1].get(str(paciente.id), [])),
                paciente.resultado,
                paciente.turno
            ) for paciente in pacientes[0]
            
        ]
        return data

    
    async def get_pacientes(self, page=1, page_size=10):
        try:
            offset = (page - 1) * page_size  # Calcula el inicio de la paginación
            pacientes = await self.paciente_agente_repo.get_all_pacientes(limit=page_size, offset=offset)
           
            if not pacientes:
                return []
            return self.order_pacientes_pruebas(pacientes)
        except Exception as e:
            return {"error": str(e)}

    async def get_search(self, busqueda):
        query = busqueda.strip()

        try:
            if not query:
                return []
            partes = busqueda.split(":", 1)
            if len(partes) != 2:
                return {"error": "Formato incorrecto. Usa prefijos como N:Juan, o S:Emergencia pediatrica, o E:30, etc."}
            prefijo, valor = partes
            valor = valor.strip()
            filtros = {
                "N": Q(nombre__icontains=valor),     # Busca por nombre
                "S": Q(servicio_Remitente__icontains=valor),  # Busca por servicio remitente
                "P": Q(prueba__icontains=valor),     # Busca por prueba
                "F": parse_fecha(valor),      # Busca por fecha (puedes ajustar el formato)
                "E": Q(Edad=valor) if valor.isdigit() else None,  # Busca por edad exacta (solo números)
                "T": Q(turno__icontains=valor)
            }
            filtro = filtros.get(prefijo.upper())
            if filtro is None:
                return {"error": "Prefijo no reconocido. Usa N, S, P, F o E."}
            pacientes = await self.paciente_agente_repo.get_pacientes_filtered(filtro)

            if not pacientes:

                return []

            return self.order_pacientes_pruebas(pacientes)
        except Exception as e:
            return {"error": str(e)}

    async def total_pacientes(self):
        return await self.paciente_agente_repo.get_total_pacientes()

    async def all_pacientes(self):
        results = await self.paciente_agente_repo.get_all_pacientes()
        data = self.order_pacientes_pruebas(results)
        return data
    
    async def pacientes_servicio(self, servicio=None,fecha=None):
        pruebas_count = await self.paciente_agente_repo.get_pacientes_serivicio(servicio=servicio, fecha=fecha)
        dict_pruebas = [dict(item) for item in pruebas_count]
        conteo_dict = {}

        for item in dict_pruebas:
            if fecha and item["fecha"] != fecha:
                continue  # Filtrar por fecha si fue proporcionada

            servicio = item["servicio_Remitente"]
            prueba = item["prueba"]
            total = item["total"]
            turno_creado = item['turno']

            if prueba == "Hematologia":
                total *= 5
            elif prueba == "Orina":
                total *= 6
            elif prueba == "Heces":
                total *= 2

            if prueba not in conteo_dict:
                conteo_dict[prueba] = {"servicios": [], "total_general": 0}

            servicio_existente = next((s for s in conteo_dict[prueba]["servicios"] if s["servicio"] == servicio), None)

            if servicio_existente:
                servicio_existente["total"] += int(total)
            else:
                conteo_dict[prueba]["servicios"].append({"servicio": servicio, "total": total, "turno": turno_creado})

            conteo_dict[prueba]["total_general"] += int(total)

        return conteo_dict
    
    async def delete_prueba(self, id):
        try:
            resultado = await self.paciente_agente_repo.delete_prueba(id=id)
            if 'success' in resultado:
                return {"success": "Prueba eliminada correctamente."}
            else:
                return {"error": "La prueba no existe."}
        except Exception as e:
            return {"error": str(e)}
        
    async def delete_paciente(self, id):
        try:
            resultado = await self.paciente_agente_repo.delete_paciente(id=id)
            if 'success' in resultado:
                return {"success": "Paciente eliminado correctamente."}
            else:
                return {"error": "El paciente no existe."}
        except Exception as e:
            return {"error": str(e)}