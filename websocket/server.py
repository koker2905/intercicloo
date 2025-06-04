import asyncio
import websockets
import nest_asyncio
import datetime

nest_asyncio.apply()

connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    print(f"Cliente conectado. Total: {len(connected_clients)}")
    try:
        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=30)
                print(f"Mensaje recibido: {message}")
                for client in connected_clients:
                    if client != websocket:
                        await client.send(f"Maya: {message}")
            except asyncio.TimeoutError:
                # No recibimos mensajes en 30s, seguimos esperando
                pass
    except websockets.exceptions.ConnectionClosed:
        print("Un cliente se desconectó.")
    finally:
        connected_clients.remove(websocket)
        print(f"Cliente desconectado. Total: {len(connected_clients)}")

async def enviar_mensajes_periodicos():
    while True:
        if connected_clients:
            now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            mensaje = f"Mensaje automático del servidor: {now} UTC"
            tasks = [asyncio.create_task(client.send(mensaje)) for client in connected_clients]
            await asyncio.wait(tasks)
            print(f"Mensaje enviado: {mensaje}")
        else:
            print("No hay clientes conectados.")
        await asyncio.sleep(5)

async def iniciar_servidor():
    print("Iniciando servidor WebSocket...")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Servidor WebSocket ejecutándose en ws://0.0.0.0:8765")
        await enviar_mensajes_periodicos()

asyncio.run(iniciar_servidor())
