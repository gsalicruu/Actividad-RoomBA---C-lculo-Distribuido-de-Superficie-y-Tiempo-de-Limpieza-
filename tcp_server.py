import socket
import logging
import threading
import random
import json
from config import WIDTH, HEIGHT, GRID_SIZE, NUM_PELUSAS

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Estado compartido del mundo
pelusas = []

def generar_pelusas():
    global pelusas
    pelusas = [
        (random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE,
         random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
        for _ in range(NUM_PELUSAS)
    ]
    print("[Servidor] Pelusas generadas:", pelusas)

def manejar_cliente(conn, addr):
    global pelusas
    print(f"[Servidor] Conexión desde {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            mensaje = data.decode('utf-8').strip()

            if mensaje == "get_pelusas":
                response = json.dumps(pelusas)
                conn.sendall(response.encode('utf-8'))

            elif mensaje.startswith("limpiar"):
                try:
                    _, x_str, y_str = mensaje.split(",")
                    x, y = int(x_str), int(y_str)
                    if (x, y) in pelusas:
                        pelusas.remove((x, y))
                        conn.sendall(b"ok")
                        print(f"[Servidor] Pelusa eliminada en ({x},{y})")
                    else:
                        conn.sendall(b"not_found")
                except:
                    conn.sendall(b"error")

            else:
                conn.sendall(b"comando_desconocido")

    except Exception as e:
        print(f"[Servidor] Error con {addr}: {e}")
    finally:
        conn.close()
        print(f"[Servidor] Conexión cerrada con {addr}")

def start_server(host='127.0.0.1', port=8809):
    generar_pelusas()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[Servidor] Escuchando en {host}:{port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=manejar_cliente, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
