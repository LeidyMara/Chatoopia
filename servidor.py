from concurrent.futures import thread
from http import server
import threading
import socket


host = '10.253.56.45'
port = 10000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clientes = []
usuarios = []
salas = []


def comunicacion(mensaje):
    for cliente in clientes:
        cliente.send(mensaje)

def comunicacion1(mensaje, usuario_des):
    for cliente in clientes:
        indice = clientes.index(cliente)
        usuario = usuarios[indice]
        if usuario[1] == usuario_des:
            cliente.send(mensaje.encode('ascii'))

def comunicacion2(mensaje):
    for cliente in clientes:
        indice = clientes.index(cliente)
        usuario = usuarios[indice]
        if usuario[1] == mensaje:
            for u in usuarios:
                user = "#"+u[1]
                cliente.send(user.encode('ascii'))


def Control(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            mensaje_deco = mensaje.decode('ascii')
            if mensaje_deco[0:2] == "#/":
                comunicacion2(mensaje_deco[2:])
            elif mensaje_deco[0:1] == "#":
                cont_usuario = mensaje_deco.find(" ")
                comunicacion1(mensaje_deco[cont_usuario+1:], mensaje_deco[1:cont_usuario])
            else:
                comunicacion(mensaje)
        except:
            indice = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            usuario = usuarios[indice]
            comunicacion(f'{usuario[0]} ha abandonado el chat'.encode('ascii'))
            usuarios.remove(usuario)
            break


def recibir():
    while True:
        cliente, direccion = server.accept()
        print(f"Se ha conectado a través de {str(direccion)}")

        cliente.send('Nombre'.encode('ascii'))
        nombre = cliente.recv(1024).decode('ascii')
        usuarios.append([cliente,nombre])
        clientes.append(cliente)

        print(f'Nombre de usuario es {nombre}')
        comunicacion(f'{nombre} se ha unido al chat\n'.encode('ascii'))
        cliente.send('Conectado al servidor'.encode('ascii'))

        hilo = threading.Thread(target=Control, args=(cliente,))
        hilo.start()


print('El servidor se está ejecutando...')
recibir()