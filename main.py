import asyncio
import json
import websockets

# Lista para almacenar las conexiones de los jugadores
players = {}

async def handle_player(websocket):

    # Pide nombre para identificar al jugador
    # await websocket.send('¿Cuál es tu nombre?')
    name = await websocket.recv()
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

async def main():
    # Configurar el servidor WebSocket
    async with websockets.serve(handle_player, '0.0.0.0', 8765):
        # Obtener el bucle de eventos actual
        loop = asyncio.get_running_loop()

        try:
            # Ejecutar el bucle de eventos hasta que se cierre el servidor
            await asyncio.Future()
        except KeyboardInterrupt:
            pass
        finally:
            # Cerrar las conexiones del servidor
            for player in players:
                await player.close()

# Ejecutar el programa principal
asyncio.run(main())
