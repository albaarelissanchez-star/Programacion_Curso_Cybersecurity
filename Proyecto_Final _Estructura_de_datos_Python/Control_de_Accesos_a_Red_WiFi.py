"""
Control de Accesos a Red WiFi

Contiene:
 - Vectores: lista de dispositivos registrados
 - Matrices: conexiones por usuario (registro histórico simplificado)
 - Condicionales y bucles: validación de límites y generación de alertas
 - Funciones: RegistrarDispositivo, ValidarAcceso, GenerarAlertas
"""

import ipaddress
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import threading

# Configuración básica del logger para generar alertas y registros.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ControlAccesosWiFi')


# ---------------------------- ESTRUCTURAS DE DATOS ----------------------------
# Vector: lista de dispositivos registrados (clave: MAC en mayúsculas)
# Cada entrada almacena: MAC, IP, nombre de dispositivo, propietario (usuario), ultimo_acceso

Dispositivo = Dict[str, Optional[str]]

# Matriz simplificada: conexiones por usuario.
# Estructura: { usuario: [ (timestamp, mac, ip, evento) ] }
ConexionesPorUsuario = Dict[str, List[Tuple[str, str, str, str]]]


class ControlAccesos:
    """Clase que encapsula la lógica de control de accesos de la red WiFi."""

    def __init__(self, max_conexiones_simultaneas: int = 5):
        # Lista (diccionario) de dispositivos registrados por MAC
        self.dispositivos: Dict[str, Dispositivo] = {}
        # Matriz de conexiones por usuario
        self.conexiones: ConexionesPorUsuario = {}
        # Límite de conexiones simultáneas permitidas por usuario
        self.max_conexiones_simultaneas = max_conexiones_simultaneas
        # Registramos un objeto lock para evitar condiciones de carrera si el
        # sistema se usa en hilos/threads (p. ej. eventos simultáneos)
        self._lock = threading.Lock()

    # ---------------------------- FUNCIONES REQUERIDAS ----------------------------
    def RegistrarDispositivo(self, mac: str, ip: str, nombre: str, usuario: str) -> bool:
        """
        RegistrarDispositivo:
        Registra (o actualiza) un dispositivo en el vector de dispositivos.

        Parámetros:
          - mac: dirección MAC del dispositivo (se normaliza a mayúsculas).
          - ip: dirección IP asignada al dispositivo (valida formato IPv4/IPv6).
          - nombre: nombre humano del dispositivo (ej. 'Teléfono Alba').
          - usuario: nombre del usuario/propietario del dispositivo.

        Retorna:
          - True si el registro/actualización fue exitoso; False si hay error.

        Nota:
          - La función valida la IP; si la IP no es válida, no registra el dispositivo.
        """

        mac = mac.strip().upper()
        try:
            # Validación de la IP usando el módulo ipaddress
            ip_obj = ipaddress.ip_address(ip)
        except Exception as e:
            logger.error(f"RegistrarDispositivo: IP inválida '{ip}' para MAC {mac}: {e}")
            return False

        with self._lock:
            ahora = datetime.utcnow().isoformat()
            entry: Dispositivo = {
                'mac': mac,
                'ip': str(ip_obj),
                'nombre': nombre,
                'usuario': usuario,
                'ultimo_acceso': ahora
            }
            # Insertar o actualizar
            self.dispositivos[mac] = entry

            # Añadir registro de conexión en la matriz
            self._add_conexion_historial(usuario, mac, str(ip_obj), 'registro')
            logger.info(f"Dispositivo registrado/actualizado: {mac} - {nombre} - {usuario}")
        return True

    def ValidarAcceso(self, mac: str, ip: str) -> bool:

        """
        ValidarAcceso:
        Comprueba si un dispositivo con MAC e IP dadas está autorizado y si el
        usuario supera el límite de conexiones simultáneas.

        Comportamiento:
          - Si el dispositivo no está registrado -> acceso denegado (alerta).
          - Si la IP no coincide con la registrada -> alerta de posible spoofing.
          - Si el usuario supera su límite de conexiones simultáneas -> acceso denegado.

        Retorna:
          - True si el acceso es permitido; False en caso contrario.
        """


        mac = mac.strip().upper()
        try:
            ip_obj = ipaddress.ip_address(ip)
        except Exception:
            logger.warning(f"ValidarAcceso: IP inválida recibida: {ip}")
            self.GenerarAlertas('IP_INVALIDA', f"IP inválida recibida: {ip} (MAC: {mac})")
            return False

        with self._lock:
            if mac not in self.dispositivos:
                # Dispositivo no registrado
                logger.warning(f"ValidarAcceso: MAC no registrada: {mac}")
                self.GenerarAlertas('MAC_NO_REGISTRADA', f"Intento de acceso de MAC no registrada: {mac} (IP: {ip})")
                return False

            registro = self.dispositivos[mac]
            registrado_ip = registro.get('ip')
            usuario = registro.get('usuario', 'desconocido')

            # Detectar discrepancia de IP -> posible suplantación
            if registrado_ip != str(ip_obj):
                mensaje = (f"Diferencia IP detectada para MAC {mac}. IP registrada: {registrado_ip}, "
                           f"IP actual: {ip}")
                logger.warning("ValidarAcceso: " + mensaje)
                self.GenerarAlertas('IP_DISCREPANTE', mensaje)
                # Aún así se podría permitir el acceso si se desea; aquí lo denegamos por seguridad
                return False

            # Validar límite de conexiones simultáneas para el usuario
            conexiones_activas = self._contar_conexiones_activas(usuario)
            if conexiones_activas >= self.max_conexiones_simultaneas:
                alerta_msg = (f"Usuario '{usuario}' excede límite: {conexiones_activas} >= {self.max_conexiones_simultaneas}")
                logger.warning("ValidarAcceso: " + alerta_msg)
                self.GenerarAlertas('LIMITE_EXCEDIDO', alerta_msg)
                return False

            # Si pasó todas las validaciones, registramos la conexión
            ahora = datetime.utcnow().isoformat()
            registro['ultimo_acceso'] = ahora
            self._add_conexion_historial(usuario, mac, str(ip_obj), 'conexion')
            logger.info(f"Acceso permitido: {mac} ({registro.get('nombre')}) para usuario {usuario}")
            return True

    def GenerarAlertas(self, tipo: str, mensaje: str) -> None:
        """
        GenerarAlertas:
        Produce alertas en el sistema; actualmente envía mensajes al logger.
        En una implementación real se podrían enviar correos, SMS, notificaciones a
        un dashboard, o almacenar las alertas en una base de datos.

        Parámetros:
          - tipo: código corto del tipo de alerta (ej. 'MAC_NO_REGISTRADA').
          - mensaje: texto descriptivo de la alerta.
        """

        # Aquí usamos logging con nivel WARNING/ERROR dependiendo del tipo
        prefijo = f"ALERTA [{tipo}]"

        # Para eventos críticos podría usarse logger.error
        if tipo in ('MAC_NO_REGISTRADA', 'IP_DISCREPANTE', 'LIMITE_EXCEDIDO'):
            logger.warning(f"{prefijo} - {mensaje}")
        elif tipo == 'IP_INVALIDA':
            logger.error(f"{prefijo} - {mensaje}")
        else:
            logger.info(f"{prefijo} - {mensaje}")

    # ---------------------------- MÉTODOS AUXILIARES ----------------------------
    def _add_conexion_historial(self, usuario: str, mac: str, ip: str, evento: str) -> None:
        """Agregar una fila en la 'matriz' de conexiones por usuario."""
        ahora = datetime.utcnow().isoformat()
        entry = (ahora, mac, ip, evento)
        if usuario not in self.conexiones:
            self.conexiones[usuario] = []
        self.conexiones[usuario].append(entry)

    def _contar_conexiones_activas(self, usuario: str) -> int:
        """Contar cuántas conexiones activas tiene un usuario."
        """

        historial = self.conexiones.get(usuario, [])
        # Contar entradas cuyo evento sea 'conexion'
        contador = sum(1 for row in historial if row[3] == 'conexion')
        return contador

    # Función para desconectar un dispositivo (marcar evento de desconexión en la matriz)
    def desconectar_dispositivo(self, mac: str) -> bool:
        mac = mac.strip().upper()
        with self._lock:
            if mac not in self.dispositivos:
                logger.info(f"desconectar_dispositivo: MAC desconocida {mac}")
                return False
            usuario = self.dispositivos[mac].get('usuario', 'desconocido')
            ip = self.dispositivos[mac].get('ip', '')
            self._add_conexion_historial(usuario, mac, ip, 'desconexion')
            logger.info(f"Dispositivo {mac} desconectado (usuario: {usuario})")
            return True

    # Método para listar dispositivos (útil para administración)
    def listar_dispositivos(self) -> List[Dispositivo]:
        with self._lock:
            return list(self.dispositivos.values())


# ---------------------------- EJEMPLO DE USO ----------------------------
def main():
    controller = ControlAccesos(max_conexiones_simultaneas=2)

    # Registrar algunos dispositivos
    controller.RegistrarDispositivo('aa:bb:cc:11:22:33', '192.168.1.10', 'Teléfono Alba', 'alba')
    controller.RegistrarDispositivo('dd:ee:ff:44:55:66', '192.168.1.11', 'Tablet Carlos', 'carlos')

    # Intento de acceso válido
    print('\nIntento de acceso 1 (válido):')
    permitido = controller.ValidarAcceso('aa:bb:cc:11:22:33', '192.168.1.10')
    print('Acceso permitido?' , permitido)

    # Intento de acceso con MAC no registrada
    print('\nIntento de acceso 2 (MAC no registrada):')
    permitido = controller.ValidarAcceso('00:11:22:33:44:55', '192.168.1.50')
    print('Acceso permitido?' , permitido)

    # Intento con IP discrepante (posible spoofing)
    print('\nIntento de acceso 3 (IP discrepante):')
    permitido = controller.ValidarAcceso('dd:ee:ff:44:55:66', '10.0.0.5')
    print('Acceso permitido?' , permitido)

    # Probar límite de conexiones simultáneas
    print('\nProbar límite de conexiones:')
    # Registrar dos conexiones válidas para 'carlos'
    controller.RegistrarDispositivo('11:22:33:44:55:66', '192.168.1.12', 'PC Carlos 1', 'carlos')
    controller.ValidarAcceso('dd:ee:ff:44:55:66', '192.168.1.11')  # 1er acceso de carlos
    controller.ValidarAcceso('11:22:33:44:55:66', '192.168.1.12')  # 2do acceso de carlos

    # Ahora carlos tiene 2 conexiones activas (límite = 2)
    # Un tercer intento (mismo usuario con otro dispositivo) debe ser denegado
    
    controller.RegistrarDispositivo('77:88:99:AA:BB:CC', '192.168.1.13', 'PC Carlos 2', 'carlos')
    permitido = controller.ValidarAcceso('77:88:99:AA:BB:CC', '192.168.1.13')
    print('Acceso permitido (debería ser False por límite):', permitido)

    # Mostrar dispositivos registrados
    print('\nDispositivos registrados:')
    for d in controller.listar_dispositivos():
        print(d)

    # Mostrar historial simplificado de conexiones por usuario
    print('\nHistorial de conexiones por usuario:')
    for usuario, historial in controller.conexiones.items():
        print(f"Usuario: {usuario}")
        for row in historial:
            print('  ', row)


if __name__ == '__main__':
    main()
