### Create/join room + multiplayer positions ###


import asyncio
import websockets
import string
import random
import json

# Clase para representar una sala y su código de invitación
class Room:
    def __init__(self, creator):
        self.code = self.generate_code()
        self.creator = creator
        self.users = set()

    def generate_code(self):
        # Generar un código de invitación aleatorio de 6 caracteres
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def add_user(self, user):
        self.users.add(user)

    def remove_user(self, user):
        self.users.remove(user)

    def is_empty(self):
        return len(self.users) == 0

# Diccionario para almacenar las salas y sus códigos de invitación
ROOMS = {}

# Lista para almacenar las conexiones de los jugadores
players = {}

async def create_room(websocket, name):

    room = Room(name)
    ROOMS[room.code] = room
    await websocket.send(f"create:{room.code}")

    # Ingresa directamente a la sala con el nombre de ususario que ingresó sin pedir el nombre porque el nombre ya se lo pasamos al crear la sala
    room.add_user(websocket)

    await websocket.send(f"join:{room.code}.")

    await handle_player(websocket, name)

async def join_room(websocket, room_code):

    # Verificar si el código de invitación es válido y si la sala existe
    if room_code in ROOMS:
        room = ROOMS[room_code]

        # Solicitar al usuario que ingrese su nombre de usuario
        await websocket.send("Ingresa tu nombre de usuario:")
        username = await websocket.recv()

        # Agregar el objeto WebSocket a la sala en lugar del nombre de usuario
        room.add_user(websocket)
        await websocket.send(f"join:{room_code}.")

        # Enviar un mensaje de bienvenida a todos los usuarios de la sala
        for user in room.users:
            if user != websocket:
                await user.send(f"{username} se ha unido a la sala.")

        await handle_player(websocket, username)

    else:
        await websocket.send("error:Código de invitación inválido.")
        room_code = await websocket.recv()


async def unregister(websocket):
    for room_code, room in list(ROOMS.items()):
        if websocket in room.users:
            room.remove_user(websocket)
            if room.is_empty():
                del ROOMS[room_code]

async def broadcast(room_code, message):
    if room_code in ROOMS:
        room = ROOMS[room_code]
        for user in room.users:
            await user.send(message)

async def handle_player(websocket, name):

    # Pide nombre para identificar al jugador
    # await websocket.send('¿Cuál es tu nombre?')
    # name = await websocket.recv()
    players[name] = { 'x': 0, 'y': 0}

    try:
        while True:
            # Esperar mensajes del jugador 
            message = await websocket.recv()
            
            # Procesar el mensaje recibido del jugador
            player_position = json.loads(message)
            # Actualizar las posiciones de los jugadores
            players[name]['x'] = player_position['x']
            players[name]['y'] = player_position['y']

            # Enviar las nuevas posiciones
            await websocket.send(json.dumps(players))
            # imprime en consola las posiciones de los jugadores con el nombre
            print(players)

    except websockets.exceptions.ConnectionClosedOK:
        print('Conexión cerrada')
        pass
    finally:
        # Eliminar la conexión del jugador cuando se desconecta
        print('Desconectado')
        del players[name]

async def handler(websocket, path):
    try:
        async for message in websocket:
            if message.startswith("create"):
                _, name = message.split(",")
                await create_room(websocket, name)
            elif message.startswith("join"):
                _, room_code = message.split(",")
                await join_room(websocket, room_code)
            # else:
            #     await handle_player(websocket)

    finally:
        await unregister(websocket)

async def main():
    start_server = websockets.serve(handler, "0.0.0.0", 8765)
    server = await start_server
    await server.wait_closed()

# Ejecutar el programa principal
asyncio.run(main())