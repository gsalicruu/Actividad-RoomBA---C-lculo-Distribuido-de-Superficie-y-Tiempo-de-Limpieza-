import socket
import json

def pedir_pelusas(host='127.0.0.1', port=8809):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(b"get_pelusas")
            data = s.recv(4096).decode('utf-8')
            return json.loads(data)
    except Exception as e:
        print(f"[Cliente] Error al pedir pelusas: {e}")
        return []

def notificar_limpieza(x, y, host='127.0.0.1', port=8809):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            mensaje = f"limpiar,{x},{y}"
            s.sendall(mensaje.encode('utf-8'))
            respuesta = s.recv(1024).decode('utf-8')
            return respuesta == "ok"
    except Exception as e:
        print(f"[Cliente] Error al notificar limpieza: {e}")
        return False
