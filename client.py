import socket
import time
import random
import threading

HOST = '127.0.0.1'
PORT = 65432

cant_peticiones = int(input("Ingrese la cantidad de peticiones que desea realizar: "))

def simular_cliente_individual(id_cliente, tarea):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        time.sleep(random.uniform(0.1, 0.5)) 
        
        client_socket.connect((HOST, PORT))
        print(f"[CLIENTE {id_cliente}] Conectado. Enviando: '{tarea}'")
        client_socket.sendall(tarea.encode('utf-8'))
        
        respuesta = client_socket.recv(1024).decode('utf-8')
        print(f"[CLIENTE {id_cliente}] ¡Respuesta recibida!: {respuesta}")
        
    except Exception as e:
        print(f"[CLIENTE {id_cliente} ERROR] Error de conexión: {e}")
    finally:
        client_socket.close()

def lanzar_carga_simulada(cantidad_peticiones):
    print(f"=== INICIANDO SIMULACIÓN DE {cantidad_peticiones} PETICIONES CONCURRENTES ===")
    
    hilos_clientes = []
    
    for i in range(cantidad_peticiones):
        tarea = f"Nueva tarea (ID: {i+1})"
        
        hilo = threading.Thread(target=simular_cliente_individual, args=(i+1, tarea))
        hilos_clientes.append(hilo)
        hilo.start()
        
    for hilo in hilos_clientes:
        hilo.join()
        
    print("=== SIMULACIÓN FINALIZADA ===")

if __name__ == "__main__":
    lanzar_carga_simulada(cant_peticiones)