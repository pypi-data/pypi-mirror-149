import asyncio, websockets, threading

async def client(*args):
    # interface cus you cant make async __init__
    websocket_client = Client(*args)
    await websocket_client.connect()
    return websocket_client

class Client:
    def __init__(self, ip, version="2.0", client_id="PythonUser", auto_reconnect=False): 
        self.version = version
        self.client_id = client_id
        self.ip = ip
        self.auto_reconnect = auto_reconnect
        self.info = []
        self.closed = False

    async def connect(self):
        self.webs = await websockets.connect(self.ip)
        await self.webs.send('token {"version":"' + self.version + '","clientID":"' + self.client_id + '"}')
        thread = threading.Thread(target=self.listen).start()

    def listen(self):
        while not self.closed:
            try:
                message = asyncio.run(self.get(self.webs))
                if message: 
                    self.info.append(message)
            except asyncio.TimeoutError:
                pass
            except asyncio.CancelledError:
                pass

    async def get(self, webs):
        try:
            return await asyncio.wait_for(webs.recv(), 0.1)
        except:
            return None

    async def send_packet(self, data):
        try:
            await asyncio.wait_for(self.webs.send(data), 1)
        except:
            if auto_reconnect:
                await self.connect()
                await self.webs.send(data)
            else:
                self.closed = True
                raise ConnectionError

    async def close(self):
        self.closed = True
        await self.webs.close()

    def get_packets(self, **kwargs):
        to_return = self.info
        self.info = []
        if to_return:
            return to_return
        try:
            while kwargs["wait_until_packet"]:
                to_return = self.info
                self.info = []
                if to_return:
                    return to_return
        except:
            pass
        return []

    def get_packet(self, *args, **kwargs): # alias
        return self.get_packets(args, kwargs)

    # alias functions start

    async def place(self, **kwargs):
        # place <x> <y> <id> <rot> <heat> - Places cell
        
        x, y, id = kwargs["x"], kwargs["y"], kwargs["id"]
        try:
            rot = kwargs["rot"]
        except:
            rot = 0
        try:
            heat = kwargs["heat"]
        except:
            heat = 0
        await self.send_packet(f"place {x} {y} {id} {rot} {heat}")

    async def bg(self, **kwargs):
        # bg <x> <y> <bg> - Sets background (placeables)

        x, y = kwargs["x"], kwargs["y"]
        try:
            bg = kwargs["bg"]
        except:
            bg = "placeable"
        await self.send_packet(f"bg {x} {y} {bg}")

    async def wrap(self):
        # wrap - Toggles wrap mode
        await self.send_packet("wrap")

    async def setinit(self, code):
        # setinit <code> - Sets initial state on the server
        await self.send_packet(f"setinit {code}")

    async def new_hover(self, **kwargs):
        # new-hover <uuid> <x> <y> <id> <rot> - Creates new hover
        x, y, id = kwargs["x"], kwargs["y"], kwargs["id"]
        try:
            uuid = kwargs["uuid"]
        except:
            uuid = self.client_id
        try:
            rot = kwargs["rot"]
        except:
            rot = 0
        await self.send_packet(f"new-hover {uuid} {x} {y} {id} {rot}")

    async def set_hover(self, **kwargs):
        # set-hover <uuid> <x> <y> - Sets the new hover position
        x, y = kwargs["x"], kwargs["y"]
        try:
            uuid = kwargs["uuid"]
        except:
            uuid = self.client_id
        await self.send_packet(f"set-hover {uuid} {x} {y}")

    async def drop_hover(self, *args):
        # drop-hover <uuid> - Removes the hover
        try:
            uuid = args[0]
        except:
            uuid = self.client_id
        await self.send_packet(f"drop-hover {uuid}")

    async def set_cursor(self, **kwargs):
        # set-cursor <uuid> <x> <y> - Sets cursor state
        x, y = kwargs["x"], kwargs["y"]
        try:
            uuid = kwargs["uuid"]
        except:
            uuid = self.client_id
        await self.send_packet(f"set-cursor {uuid} {x} {y}")

    # alias functions end