import socket
import threading
import time

# Configuración de red
HOST = '127.0.0.1'
PORT = 65432

#Se simularán los workers con hilos
def worker_task(client_socket, client_address, task_data):
    print(f"[WORKER] Empezando a procesar: '{task_data}' de {client_address}")
    
    # Simulación de trabajo de procesamiento
    time.sleep(2) 
    resultado = f"Resultado de procesar exitosamente: ({task_data})"
    
    try:
        client_socket.sendall(resultado.encode('utf-8'))
        print(f"[WORKER] Resultado enviado a {client_address}")
    except Exception as e:
        print(f"[ERROR WORKER] Error al enviar datos: {e}")
    finally:
        client_socket.close()

def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}... Esperando tareas.")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"\n[SERVIDOR] Conexión recibida de {client_address}")
            task_data = client_socket.recv(1024).decode('utf-8')
            
            if task_data:
                worker_thread = threading.Thread(
                    target=worker_task, 
                    args=(client_socket, client_address, task_data)
                )
                worker_thread.start()
                print(f"[SERVIDOR] Tarea distribuida a un Worker (Hilo: {worker_thread.name})")
                
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Apagando el servidor.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    iniciar_servidor()