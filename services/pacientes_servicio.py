from repositories.Pacientes import Paciente_agente_repo
from tortoise.expressions import Q
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
                }
            filtro = filtros.get(prefijo.upper())
            

            if filtro is None:
                return {"error": "Prefijo no reconocido. Usa N, S, P, F o E."}
            pacientes = await self.paciente_agente_repo.get_pacientes_filtered(filtro)
        
            if not pacientes:
                return []
            print(pacientes)
            return self.order_pacientes(pacientes)
        except Exception as e:
            return {"error": str(e)}
    
    async def total_pacientes(self):
        return await self.paciente_agente_repo.get_total_pacientes()   
    
    async def pacientes_servicio(self,servicio=None):
        pruebas_count = await self.paciente_agente_repo.get_pacientes_serivicio(servicio=servicio)
        dict_pruebas = [dict(item) for item in pruebas_count]
        conteo_dict = {}

        for item in dict_pruebas:
                servicio = item["servicio_Remitente"]
                prueba = item["prueba"]
                total = item["total"]

                if servicio not in conteo_dict:
                    conteo_dict[servicio] = {}

                conteo_dict[servicio][prueba] = total
        return conteo_dict

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