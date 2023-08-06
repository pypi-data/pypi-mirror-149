import asyncio

async def handle_echo(reader, writer):
    data = await reader.read(-1)
    message = data#.decode()
    addr = writer.get_extra_info('peername')
    print(addr)

    print(f"Received {message!r} from {addr!r}")

    #print(f"Send: {"Got it"!r}")
    writer.write(data)
    await writer.drain()

    #print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 9999)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())