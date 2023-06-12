### Rooms server ###

import asyncio
import websockets
import string
import random

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

async def create_room(websocket, name):
    room = Room(name)
    ROOMS[room.code] = room
    await websocket.send(f"Sala creada. Código de invitación: {room.code}")

    # Ingresa directamente a la sala pedir el nombre porque el nombre ya se lo pasamos al crear la sala
    room.add_user(websocket)
    await websocket.send(f"Te has unido a la sala {room.code}.")

async def join_room(websocket, room_code):
    # Verificar si el código de invitación es válido y si la sala existe
    if room_code in ROOMS:
        room = ROOMS[room_code]
        # Solicitar al usuario que ingrese su nombre de usuario
        await websocket.send("Ingresa tu nombre de usuario:")
        username = await websocket.recv()
        room.add_user(username)
        await websocket.send(f"Te has unido a la sala {room_code}.")
        # Envia un mensaje de bienvenida a todos los usuarios de la sala
        for user in room.users:
            if user != username:
                await websocket.send(f"{username} se ha unido a la sala.")
    else:
        await websocket.send("Código de invitación inválido.")

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

async def handler(websocket, path):
    try:
        async for message in websocket:
            if message.startswith("create"):
                _, name = message.split(",")
                await create_room(websocket, name)
            elif message.startswith("join"):
                _, room_code = message.split(",")
                await join_room(websocket, room_code)
            else:
                room_code = None
                for code, room in ROOMS.items():
                    if websocket in room.users:
                        room_code = code
                        break
                if room_code:
                    await broadcast(room_code, message)
                else:
                    await websocket.send("No estás en ninguna sala.")

    finally:
        await unregister(websocket)

async def main():
    start_server = websockets.serve(handler, "0.0.0.0", 8000)
    server = await start_server
    await server.wait_closed()

asyncio.run(main())
