
# Control de Accesos a Red WiFi - GUI - POO

"""Objetivo: Registrar dispositivos por MAC e IP, controlar límite de conexiones simultáneas y generar alertas por accesos no autorizados.

Componentes: 
- Vectores: lista de dispositivos - Matrices: conexiones por usuario 
- Condicionales y bucles: validación de límite y alertas 
- Funciones: RegistrarDispositivo,ValidarAcceso, GenerarAlertas Bibliotecas, incluye interfaz grafica y manual de uso."""


# ---------------------------- IMPORTACIONES ----------------------------
import ipaddress
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import threading

# Librerías para la interfaz gráfica
import tkinter as tk
from tkinter import ttk, messagebox


# ---------------------------- CONFIGURACIÓN DE LOGGING ----------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ControlAccesosWiFi')


# ---------------------------- ESTRUCTURAS DE DATOS ----------------------------
Dispositivo = Dict[str, Optional[str]]
ConexionesPorUsuario = Dict[str, List[Tuple[str, str, str, str]]]


class ControlAccesos:
    def __init__(self, max_conexiones_simultaneas: int = 5):
        # Lista (diccionario) de dispositivos registrados por MAC
        self.dispositivos: Dict[str, Dispositivo] = {}
        # Matriz de conexiones por usuario
        self.conexiones: ConexionesPorUsuario = {}
        # Límite de conexiones simultáneas permitidas por usuario
        self.max_conexiones_simultaneas = max_conexiones_simultaneas
        # Lock para evitar problemas si en el futuro se maneja en varios hilos
        self._lock = threading.Lock()

    # ---------------------------- FUNCIONES REQUERIDAS ----------------------------
    def RegistrarDispositivo(self, mac: str, ip: str, nombre: str, usuario: str) -> bool:

        mac = mac.strip().upper()

        # Validar datos muy básicos antes de continuar
        if not mac:
            logger.error("RegistrarDispositivo: MAC vacía")
            return False
        if not usuario.strip():
            logger.error("RegistrarDispositivo: usuario vacío")
            return False

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
                'nombre': nombre.strip() or 'Sin nombre',
                'usuario': usuario.strip(),
                'ultimo_acceso': ahora
            }
            # Insertar o actualizar
            self.dispositivos[mac] = entry
            # Añadir registro de conexión en la matriz (evento 'registro')
            self._add_conexion_historial(usuario.strip(), mac, str(ip_obj), 'registro')
            logger.info(f"Dispositivo registrado/actualizado: {mac} - {nombre} - {usuario}")
        return True

    def ValidarAcceso(self, mac: str, ip: str) -> bool:
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
                # Por seguridad, se deniega el acceso
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
        prefijo = f"ALERTA [{tipo}]"
        # Elegimos el nivel del log en función del tipo
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
        """Contar cuántas conexiones activas tiene un usuario."""

        historial = self.conexiones.get(usuario, [])
        contador = sum(1 for row in historial if row[3] == 'conexion')
        return contador

    def desconectar_dispositivo(self, mac: str) -> bool:
        """Marca un evento de desconexión para un dispositivo (no se usa en la GUI actual)."""
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

    def listar_dispositivos(self) -> List[Dispositivo]:
        """Devuelve una lista de todos los dispositivos registrados."""
        with self._lock:
            return list(self.dispositivos.values())


# ---------------------------- INTERFAZ GRÁFICA (TKINTER) ----------------------------

class AppControlAccesos(tk.Tk):

    def __init__(self, controlador: ControlAccesos):
        super().__init__()

        self.controlador = controlador

        # Configuración de la ventana
        self.title("Control de Accesos a Red WiFi")
        self.geometry("880x600")  # Ancho x alto en píxeles

        # Cuaderno de pestañas (notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Creamos los frames que serán las pestañas
        self.frame_registro = ttk.Frame(self.notebook)
        self.frame_validacion = ttk.Frame(self.notebook)
        self.frame_dispositivos = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_registro, text="Registrar dispositivo")
        self.notebook.add(self.frame_validacion, text="Validar acceso")
        self.notebook.add(self.frame_dispositivos, text="Dispositivos registrados")

        # Cuadro de mensajes en la parte inferior
        self.text_mensajes = tk.Text(self, height=7, state="disabled")
        self.text_mensajes.pack(fill="x", padx=10, pady=(0, 10))

        # Construimos el contenido de cada pestaña
        self._construir_pestana_registro()
        self._construir_pestana_validacion()
        self._construir_pestana_dispositivos()

        # Cargar la tabla al inicio
        self.actualizar_tabla_dispositivos()

    # ---------------------------- PESTAÑA: REGISTRAR ----------------------------
    def _construir_pestana_registro(self):
        """Crea los campos y botón para registrar dispositivos."""
        ttk.Label(self.frame_registro, text="Dirección MAC:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(self.frame_registro, text="Dirección IP:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(self.frame_registro, text="Nombre del dispositivo:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(self.frame_registro, text="Usuario propietario:").grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.entry_mac_reg = ttk.Entry(self.frame_registro, width=40)
        self.entry_ip_reg = ttk.Entry(self.frame_registro, width=40)
        self.entry_nombre_reg = ttk.Entry(self.frame_registro, width=40)
        self.entry_usuario_reg = ttk.Entry(self.frame_registro, width=40)

        self.entry_mac_reg.grid(row=0, column=1, padx=5, pady=5)
        self.entry_ip_reg.grid(row=1, column=1, padx=5, pady=5)
        self.entry_nombre_reg.grid(row=2, column=1, padx=5, pady=5)
        self.entry_usuario_reg.grid(row=3, column=1, padx=5, pady=5)

        btn_registrar = ttk.Button(
            self.frame_registro,
            text="Registrar dispositivo",
            command=self._accion_registrar_dispositivo
        )
        btn_registrar.grid(row=4, column=0, columnspan=2, pady=15)

    def _accion_registrar_dispositivo(self):
        """Obtiene datos de la interfaz y llama a RegistrarDispositivo."""
        mac = self.entry_mac_reg.get()
        ip = self.entry_ip_reg.get()
        nombre = self.entry_nombre_reg.get()
        usuario = self.entry_usuario_reg.get()

        # Validaciones sencillas a nivel de interfaz
        if not mac.strip() or not ip.strip() or not usuario.strip():
            mensaje = "Debe completar al menos MAC, IP y Usuario para registrar el dispositivo."
            messagebox.showwarning("Datos incompletos", mensaje)
            self._agregar_mensaje("ADVERTENCIA: " + mensaje)
            return

        ok = self.controlador.RegistrarDispositivo(mac, ip, nombre, usuario)

        if ok:
            mensaje = f"Dispositivo {mac.upper()} registrado correctamente para el usuario '{usuario}'."
            messagebox.showinfo("Registro exitoso", mensaje)
            self._agregar_mensaje(mensaje)
            # Limpiar campos
            self.entry_mac_reg.delete(0, tk.END)
            self.entry_ip_reg.delete(0, tk.END)
            self.entry_nombre_reg.delete(0, tk.END)
            self.entry_usuario_reg.delete(0, tk.END)
            # Actualizar tabla
            self.actualizar_tabla_dispositivos()
        else:
            mensaje = "No se pudo registrar el dispositivo. Revise la IP, la MAC y el usuario."
            messagebox.showerror("Error al registrar", mensaje)
            self._agregar_mensaje("ERROR: " + mensaje)

    # ---------------------------- PESTAÑA: VALIDAR ACCESO ----------------------------
    def _construir_pestana_validacion(self):
        """Crea los campos y el botón para validar accesos."""
        ttk.Label(self.frame_validacion, text="Dirección MAC:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(self.frame_validacion, text="Dirección IP:").grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.entry_mac_val = ttk.Entry(self.frame_validacion, width=40)
        self.entry_ip_val = ttk.Entry(self.frame_validacion, width=40)

        self.entry_mac_val.grid(row=0, column=1, padx=5, pady=5)
        self.entry_ip_val.grid(row=1, column=1, padx=5, pady=5)

        btn_validar = ttk.Button(
            self.frame_validacion,
            text="Validar acceso",
            command=self._accion_validar_acceso
        )
        btn_validar.grid(row=2, column=0, columnspan=2, pady=15)

    def _accion_validar_acceso(self):
        """Llama a ValidarAcceso y muestra el resultado."""
        mac = self.entry_mac_val.get()
        ip = self.entry_ip_val.get()

        if not mac.strip() or not ip.strip():
            mensaje = "Debe indicar tanto la MAC como la IP para validar el acceso."
            messagebox.showwarning("Datos incompletos", mensaje)
            self._agregar_mensaje("ADVERTENCIA: " + mensaje)
            return

        permitido = self.controlador.ValidarAcceso(mac, ip)

        if permitido:
            mensaje = f"Acceso PERMITIDO para el dispositivo {mac.upper()}"
            messagebox.showinfo("Acceso permitido", mensaje)
        else:
            mensaje = f"Acceso DENEGADO para el dispositivo {mac.upper()} (revisar alertas en la consola)."
            messagebox.showwarning("Acceso denegado", mensaje)

        self._agregar_mensaje(mensaje)

    # ---------------------------- PESTAÑA: DISPOSITIVOS ----------------------------
    def _construir_pestana_dispositivos(self):
        """Crea la tabla para ver los dispositivos registrados."""
        columnas = ("mac", "ip", "nombre", "usuario", "ultimo_acceso")
        self.tree_dispositivos = ttk.Treeview(
            self.frame_dispositivos,
            columns=columnas,
            show="headings",
            height=15
        )

        # Encabezados
        self.tree_dispositivos.heading("mac", text="MAC")
        self.tree_dispositivos.heading("ip", text="IP")
        self.tree_dispositivos.heading("nombre", text="Nombre")
        self.tree_dispositivos.heading("usuario", text="Usuario")
        self.tree_dispositivos.heading("ultimo_acceso", text="Último acceso")

        # Ancho aproximado de las columnas
        self.tree_dispositivos.column("mac", width=140)
        self.tree_dispositivos.column("ip", width=140)
        self.tree_dispositivos.column("nombre", width=180)
        self.tree_dispositivos.column("usuario", width=140)
        self.tree_dispositivos.column("ultimo_acceso", width=220)

        self.tree_dispositivos.pack(fill="both", expand=True, padx=5, pady=5)

        btn_actualizar = ttk.Button(
            self.frame_dispositivos,
            text="Actualizar lista",
            command=self.actualizar_tabla_dispositivos
        )
        btn_actualizar.pack(pady=5)

    def actualizar_tabla_dispositivos(self):
        """Recarga la tabla con la información más reciente."""
        # Eliminar filas actuales
        for item in self.tree_dispositivos.get_children():
            self.tree_dispositivos.delete(item)

        # Insertar dispositivos
        for d in self.controlador.listar_dispositivos():
            self.tree_dispositivos.insert(
                "", tk.END,
                values=(
                    d.get('mac', ''),
                    d.get('ip', ''),
                    d.get('nombre', ''),
                    d.get('usuario', ''),
                    d.get('ultimo_acceso', ''),
                )
            )

    # ---------------------------- ÁREA DE MENSAJES ----------------------------
    def _agregar_mensaje(self, texto: str):
        """Agrega una línea al cuadro de mensajes inferior."""
        self.text_mensajes.config(state="normal")
        self.text_mensajes.insert(tk.END, texto + "\n")
        self.text_mensajes.see(tk.END)
        self.text_mensajes.config(state="disabled")


# ---------------------------- FUNCIÓN PRINCIPAL ----------------------------

def main():
    # Creamos el controlador con un límite de 2 conexiones simultáneas por usuario
    controlador = ControlAccesos(max_conexiones_simultaneas=2)

    # Lanzamos la interfaz gráfica
    app = AppControlAccesos(controlador)
    app.mainloop()


if __name__ == '__main__':
    main()