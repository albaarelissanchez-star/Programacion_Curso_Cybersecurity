
/*
Control de Accesos a Red WiFi

Contiene:
 - Vectores / listas: dispositivos registrados
 - Matrices: historial de conexiones por usuario (lista de filas)
 - Condicionales y bucles: validación de límite y alertas
 - Funciones: RegistrarDispositivo, ValidarAcceso, GenerarAlertas

*/
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <tuple>
#include <algorithm>
#include <regex>
#include <mutex>
#include <chrono>
#include <iomanip>
#include <sstream>

using namespace std;

// ---------------------------- UTILIDADES ----------------------------

// Convierte un string a mayúsculas
static string ToUpper(string s) {
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c){ return (unsigned char)std::toupper(c); });
    return s;
}

// Quita espacios al inicio y al final
static string Trim(const string& s) {
    const auto start = s.find_first_not_of(" \t\r\n");
    if (start == string::npos) return "";
    const auto end = s.find_last_not_of(" \t\r\n");
    return s.substr(start, end - start + 1);
}

// Devuelve fecha/hora
string UtcIsoNow() {
    time_t t = time(nullptr);
    tm tm_utc;
    gmtime_s(&tm_utc, &t);
    ostringstream oss;
    oss << put_time(&tm_utc, "%Y-%m-%dT%H:%M:%SZ");
    return oss.str();
}

// Valida IPv4 de forma simple
static bool IsValidIPv4(const string& ip) {
    static const std::regex ipv4_regex(
        R"(^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$)"
    );
    return std::regex_match(ip, ipv4_regex);
}

// Valida IPv6 de forma “práctica”
static bool IsValidIPv6(const string& ip) {
    static const std::regex ipv6_regex(
        R"(^([0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}$|^(([0-9A-Fa-f]{1,4}:){1,7}:)$|^(:([0-9A-Fa-f]{1,4}:){1,7})$|^(([0-9A-Fa-f]{1,4}:){1,6}:[0-9A-Fa-f]{1,4})$|^(([0-9A-Fa-f]{1,4}:){1,5}(:[0-9A-Fa-f]{1,4}){1,2})$|^(([0-9A-Fa-f]{1,4}:){1,4}(:[0-9A-Fa-f]{1,4}){1,3})$|^(([0-9A-Fa-f]{1,4}:){1,3}(:[0-9A-Fa-f]{1,4}){1,4})$|^(([0-9A-Fa-f]{1,4}:){1,2}(:[0-9A-Fa-f]{1,4}){1,5})$|^([0-9A-Fa-f]{1,4}:)((:[0-9A-Fa-f]{1,4}){1,6})$|^(::)$|^(::([0-9A-Fa-f]{1,4}){1})$|^(::([0-9A-Fa-f]{1,4}:){1}([0-9A-Fa-f]{1,4}){1})$|^(::([0-9A-Fa-f]{1,4}:){2}([0-9A-Fa-f]{1,4}){1})$|^(::([0-9A-Fa-f]{1,4}:){3}([0-9A-Fa-f]{1,4}){1})$|^(::([0-9A-Fa-f]{1,4}:){4}([0-9A-Fa-f]{1,4}){1})$|^(::([0-9A-Fa-f]{1,4}:){5}([0-9A-Fa-f]{1,4}){1})$|^(::([0-9A-Fa-f]{1,4}:){6}([0-9A-Fa-f]{1,4}){1})$)"
    );
    return std::regex_match(ip, ipv6_regex);
}

static bool IsValidIP(const string& ip) {
    return IsValidIPv4(ip) || IsValidIPv6(ip);
}

// “Logger” sencillo por consola
static void LogInfo(const string& msg)    { std::cout << UtcIsoNow() << " - INFO - "    << msg << "\n"; }
static void LogWarn(const string& msg)    { std::cout << UtcIsoNow() << " - WARNING - " << msg << "\n"; }
static void LogError(const string& msg)   { std::cout << UtcIsoNow() << " - ERROR - "   << msg << "\n"; }

// ---------------------------- ESTRUCTURAS (VECTOR + MATRIZ) ----------------------------

// Dispositivo
struct Dispositivo {
    string mac;
    string ip;
    string nombre;
    string usuario;
    string ultimo_acceso;
};

// Matriz simplificada: filas (timestamp, mac, ip, evento)
using FilaHistorial = std::tuple<string, string, string, string>;

// Estructura: usuario -> lista de filas (matriz por usuario)
using ConexionesPorUsuario = std::unordered_map<string, std::vector<FilaHistorial>>;


// ---------------------------- CLASE PRINCIPAL ----------------------------

class ControlAccesos {
public:
    explicit ControlAccesos(int max_conexiones_simultaneas = 5)
        : max_conexiones_simultaneas_(max_conexiones_simultaneas) {}

    // -------- Funciones requeridas --------

    bool RegistrarDispositivo(string mac, string ip, string nombre, string usuario) {
        mac = ToUpper(Trim(mac));
        ip = Trim(ip);
        nombre = Trim(nombre);
        usuario = Trim(usuario);

        if (mac.empty() || usuario.empty()) {
            LogError("RegistrarDispositivo: MAC o usuario vacío.");
            return false;
        }

        // Validación de IP (si no es válida, no registra)
        if (!IsValidIP(ip)) {
            LogError("RegistrarDispositivo: IP inválida '" + ip + "' para MAC " + mac);
            return false;
        }

        std::lock_guard<std::mutex> guard(lock_);

        Dispositivo d;
        d.mac = mac;
        d.ip = ip;
        d.nombre = nombre.empty() ? "Sin nombre" : nombre;
        d.usuario = usuario;
        d.ultimo_acceso = UtcIsoNow();

        // Insertar o actualizar en el “vector” (map por MAC)
        dispositivos_[mac] = d;

        // Guardar evento 'registro' en la “matriz” (historial por usuario)
        AddConexionHistorial(usuario, mac, ip, "registro");

        LogInfo("Dispositivo registrado/actualizado: " + mac + " - " + d.nombre + " - " + usuario);
        return true;
    }

    bool ValidarAcceso(string mac, string ip) {
        mac = ToUpper(Trim(mac));
        ip = Trim(ip);

        if (mac.empty()) {
            LogWarn("ValidarAcceso: MAC vacía.");
            GenerarAlertas("MAC_VACIA", "Se intentó validar acceso con MAC vacía.");
            return false;
        }

        // Validar IP: si no sirve, alerta y se deniega
        if (!IsValidIP(ip)) {
            LogWarn("ValidarAcceso: IP inválida recibida: " + ip);
            GenerarAlertas("IP_INVALIDA", "IP inválida recibida: " + ip + " (MAC: " + mac + ")");
            return false;
        }

        std::lock_guard<std::mutex> guard(lock_);

        // 1) Debe existir la MAC en registros
        auto it = dispositivos_.find(mac);
        if (it == dispositivos_.end()) {
            LogWarn("ValidarAcceso: MAC no registrada: " + mac);
            GenerarAlertas("MAC_NO_REGISTRADA", "Intento de acceso de MAC no registrada: " + mac + " (IP: " + ip + ")");
            return false;
        }

        // 2) La IP debe coincidir con la registrada
        Dispositivo& registro = it->second;
        const string& ip_registrada = registro.ip;
        const string usuario = registro.usuario;

        if (ip_registrada != ip) {
            string mensaje = "Diferencia IP detectada para MAC " + mac +
                             ". IP registrada: " + ip_registrada +
                             ", IP actual: " + ip;
            LogWarn("ValidarAcceso: " + mensaje);
            GenerarAlertas("IP_DISCREPANTE", mensaje);
            return false;
        }

        // 3) Límite de conexiones por usuario
        int conexiones_activas = ContarConexionesActivas(usuario);
        if (conexiones_activas >= max_conexiones_simultaneas_) {
            string alerta = "Usuario '" + usuario + "' excede límite: " +
                            std::to_string(conexiones_activas) + " >= " +
                            std::to_string(max_conexiones_simultaneas_);
            LogWarn("ValidarAcceso: " + alerta);
            GenerarAlertas("LIMITE_EXCEDIDO", alerta);
            return false;
        }

        // Si pasa todo: registrar conexión
        registro.ultimo_acceso = UtcIsoNow();
        AddConexionHistorial(usuario, mac, ip, "conexion");
        LogInfo("Acceso permitido: " + mac + " (" + registro.nombre + ") para usuario " + usuario);
        return true;
    }

    void GenerarAlertas(const string& tipo, const string& mensaje) {
        const string prefijo = "ALERTA [" + tipo + "]";
        if (tipo == "IP_INVALIDA") {
            LogError(prefijo + " - " + mensaje);
        } else if (tipo == "MAC_NO_REGISTRADA" || tipo == "IP_DISCREPANTE" || tipo == "LIMITE_EXCEDIDO") {
            LogWarn(prefijo + " - " + mensaje);
        } else {
            LogInfo(prefijo + " - " + mensaje);
        }
    }

    // -------- Funciones de apoyo--------

    bool desconectar_dispositivo(string mac) {
        mac = ToUpper(Trim(mac));
        std::lock_guard<std::mutex> guard(lock_);

        auto it = dispositivos_.find(mac);
        if (it == dispositivos_.end()) {
            LogInfo("desconectar_dispositivo: MAC desconocida " + mac);
            return false;
        }
        const string usuario = it->second.usuario;
        const string ip = it->second.ip;

        AddConexionHistorial(usuario, mac, ip, "desconexion");
        LogInfo("Dispositivo " + mac + " desconectado (usuario: " + usuario + ")");
        return true;
    }

    std::vector<Dispositivo> listar_dispositivos() {
        std::lock_guard<std::mutex> guard(lock_);
        std::vector<Dispositivo> lista;
        lista.reserve(dispositivos_.size());
        for (const auto& par : dispositivos_) {
            lista.push_back(par.second);
        }
        return lista;
    }

    // Exponemos conexiones para el ejemplo
    const ConexionesPorUsuario& conexiones() const { return conexiones_; }

private:
    // Agrega una fila en el historial (matriz) del usuario
    void AddConexionHistorial(const string& usuario, const string& mac, const string& ip, const string& evento) {
        const string ahora = UtcIsoNow();
        conexiones_[usuario].push_back(std::make_tuple(ahora, mac, ip, evento));
    }

    // Cuenta cuántos eventos 'conexion' existen para un usuario
    int ContarConexionesActivas(const string& usuario) const {
        auto it = conexiones_.find(usuario);
        if (it == conexiones_.end()) return 0;

        int contador = 0;
        for (const auto& fila : it->second) {
            const string& evento = std::get<3>(fila);
            if (evento == "conexion") contador++;
        }
        return contador;
    }

private:
    std::unordered_map<string, Dispositivo> dispositivos_;
    ConexionesPorUsuario conexiones_;
    int max_conexiones_simultaneas_;
    mutable std::mutex lock_;
};


// ---------------------------- EJEMPLO DE USO ----------------------------

int main() {
    ControlAccesos controller(2);

    // Registrar algunos dispositivos
    controller.RegistrarDispositivo("aa:bb:cc:11:22:33", "192.168.1.10", "Telefono Alba", "alba");
    controller.RegistrarDispositivo("dd:ee:ff:44:55:66", "192.168.1.11", "Tablet Carlos", "carlos");

    // Intento de acceso valido
    std::cout << "\nIntento de acceso 1 (valido):\n";
    bool permitido = controller.ValidarAcceso("aa:bb:cc:11:22:33", "192.168.1.10");
    std::cout << "Acceso permitido? " << (permitido ? "True" : "False") << "\n";

    // Intento de acceso con MAC no registrada
    std::cout << "\nIntento de acceso 2 (MAC no registrada):\n";
    permitido = controller.ValidarAcceso("00:11:22:33:44:55", "192.168.1.50");
    std::cout << "Acceso permitido? " << (permitido ? "True" : "False") << "\n";

    // Intento con IP discrepante (posible suplantación)
    std::cout << "\nIntento de acceso 3 (IP discrepante):\n";
    permitido = controller.ValidarAcceso("dd:ee:ff:44:55:66", "10.0.0.5");
    std::cout << "Acceso permitido? " << (permitido ? "True" : "False") << "\n";

    // Probar límite de conexiones simultáneas
    std::cout << "\nProbar limite de conexiones:\n";
    controller.RegistrarDispositivo("11:22:33:44:55:66", "192.168.1.12", "PC Carlos 1", "carlos");

    controller.ValidarAcceso("dd:ee:ff:44:55:66", "192.168.1.11"); // 1er acceso de carlos
    controller.ValidarAcceso("11:22:33:44:55:66", "192.168.1.12"); // 2do acceso de carlos

    controller.RegistrarDispositivo("77:88:99:AA:BB:CC", "192.168.1.13", "PC Carlos 2", "carlos");
    permitido = controller.ValidarAcceso("77:88:99:AA:BB:CC", "192.168.1.13");
    std::cout << "Acceso permitido (debería ser False por limite): " << (permitido ? "True" : "False") << "\n";

    // Mostrar dispositivos registrados
    std::cout << "\nDispositivos registrados:\n";
    for (const auto& d : controller.listar_dispositivos()) {
        std::cout << "{mac: " << d.mac
                  << ", ip: " << d.ip
                  << ", nombre: " << d.nombre
                  << ", usuario: " << d.usuario
                  << ", ultimo_acceso: " << d.ultimo_acceso
                  << "}\n";
    }

    // Mostrar historial simplificado de conexiones por usuario
    std::cout << "\nHistorial de conexiones por usuario:\n";
    for (const auto& par : controller.conexiones()) {
        const string& usuario = par.first;
        const auto& historial = par.second;

        std::cout << "Usuario: " << usuario << "\n";
        for (const auto& fila : historial) {
            std::cout << "   (" << std::get<0>(fila) << ", "
                      << std::get<1>(fila) << ", "
                      << std::get<2>(fila) << ", "
                      << std::get<3>(fila) << ")\n";
        }
    }

    return 0;
}
