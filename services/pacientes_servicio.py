from repositories.Pacientes import Paciente_agente_repo
from tortoise.expressions import Q
from datetime import datetime
class Paciente_agente_servicio:
    def __init__(self):
        self.paciente_agente_repo = Paciente_agente_repo()


    def validar_paciente(self, nombre, Edad, sexo,servicio_Remitente, prueba):
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

    async def create_paciente(self, nombre, Edad, sexo, servicio_Remitente, prueba, resultado):
        error = self.validar_paciente(nombre, Edad, sexo,servicio_Remitente, prueba)
        if error:
            return error
        
        try:
            paciente = await self.paciente_agente_repo.create_paciente(nombre.strip(), Edad, sexo, servicio_Remitente, prueba, resultado)
            return paciente if paciente else {"error": "No se pudo crear el paciente."}
        except Exception as e:
            return {"error": str(e)}

    def order_pacientes(self, pacientes):
       
        return [
                    (
                        paciente.id,
                        paciente.fecha.strftime("%d-%m-%Y"),
                        paciente.nombre,
                        paciente.Edad,
                        paciente.sexo,
                        paciente.servicio_Remitente,
                        paciente.prueba,
                        paciente.resultado,
                        paciente.turno
                    ) for paciente in pacientes
                ]
    
    async def get_pacientes(self, page=1, page_size=10):
        try:
            offset = (page - 1) * page_size  # Calcula el inicio de la paginación
            pacientes = await self.paciente_agente_repo.get_all_pacientes(limit=page_size, offset=offset)
            if not pacientes:
                return []
            return self.order_pacientes(pacientes)
        except Exception as e:
            return {"error": str(e)}
        
    async def get_search(self,busqueda):
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
                "F": Q(fecha__icontains=valor),      # Busca por fecha (puedes ajustar el formato)
                "E": Q(Edad=valor) if valor.isdigit() else None,  # Busca por edad exacta (solo números)
                "T": Q(turno__icontains=valor)
                }
            filtro = filtros.get(prefijo.upper())
            

            if filtro is None:
                return {"error": "Prefijo no reconocido. Usa N, S, P, F o E."}
            pacientes = await self.paciente_agente_repo.get_pacientes_filtered(filtro)
        
            if not pacientes:
                return []
            return self.order_pacientes(pacientes)
        except Exception as e:
            return {"error": str(e)}
    
    async def total_pacientes(self):
        return await self.paciente_agente_repo.get_total_pacientes()   
    async def all_pacientes(self):
        results = await self.paciente_agente_repo.get_all()
        data = self.order_pacientes(results)
        return data
    
    async def pacientes_servicio(self,servicio=None):
        pruebas_count = await self.paciente_agente_repo.get_pacientes_serivicio(servicio=servicio)
        dict_pruebas = [dict(item) for item in pruebas_count]
        conteo_dict = {}

        for item in dict_pruebas:
            servicio = item["servicio_Remitente"]
            prueba = item["prueba"]
            total = item["total"]
            turno_creado = item['turno']
            # Ajustar el total según el tipo de prueba
            if prueba == "Hematologia":
                total *= 5
            elif prueba == "Orina":
                total *= 6
            elif prueba == "Heces":
                total *= 2

            # Si la prueba no está en el diccionario, la inicializamos con lista de servicios y total general
            if prueba not in conteo_dict:
                conteo_dict[prueba] = {"servicios": [], "total_general": 0}

            # Buscar si el servicio ya existe en la lista de servicios
            servicio_existente = next((s for s in conteo_dict[prueba]["servicios"] if s["servicio"] == servicio), None)

            if servicio_existente:
                # Si el servicio ya existe, sumamos el total
                servicio_existente["total"] += int(total)
            else:
                # Si el servicio no existe, lo agregamos a la lista
                conteo_dict[prueba]["servicios"].append({"servicio": servicio, "total": total,"turno":turno_creado})

            # Sumar al total general de la prueba
            conteo_dict[prueba]["total_general"] += int(total)
        return conteo_dict
 
    async def paciente_por_fecha(self,busqueda):
        query = busqueda.strip()
       
        try:
            if not query:
                return []
            fecha = datetime.strptime(query, "%d/%m/%Y")
            if fecha:
                filtro = Q(fecha__iconstain=fecha)
                self.paciente_agente_repo.get_pacientes_filtered(filtro)
            else:
                return {"error":"la fecha es incorrecta introduce una valida"}
        except Exception as e:
            return f"error {str(e)}"
    async def delete_pacientes(self, id):
        try:
            if id.is_integer():
                id = int(id)
            else:
                return {"error": "El ID debe ser un número entero."}
            
            paciente = await self.paciente_agente_repo.delete_paciente(id)
            return paciente if paciente else {"error": "No se pudo eliminar el paciente."}
        except Exception as e:
            return {"error": str(e)}