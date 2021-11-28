from aiohttp import web
import requests
import asyncio

HOST_NAME = "localhost"
PORT = 4830

BASE_URL = "https://panel.dedicatedmc.io"
USERS_URL = BASE_URL + "/api/application/users"
NODES_URL = BASE_URL + "/api/application/nodes"
SERVERS_URL = BASE_URL + "/api/application/servers"
LOCATIONS_URL = BASE_URL + "/api/application/locations?include=nodes,servers"
PTERO_API_KEY = ""
exporter_text = ""

async def update_text():
    headers = {'Authorization': 'Bearer ' + PTERO_API_KEY}
    r = requests.get(USERS_URL, headers=headers)
    response = r.json()
    total_users = response["meta"]["pagination"]["total"]

    r = requests.get(NODES_URL, headers=headers)
    response = r.json()
    total_nodes = response["meta"]["pagination"]["total"]

    r = requests.get(SERVERS_URL, headers=headers)
    response = r.json()
    total_servers = response["meta"]["pagination"]["total"]

    r = requests.get(LOCATIONS_URL, headers=headers)
    response = r.json()
    total_locations = response["meta"]["pagination"]["total"]

    global exporter_text
    exporter_text = ""
    exporter_text += f"# HELP total_users The total number of users registered in pterodactyl.\n# TYPE total_users gauge\ntotal_users {total_users}\n\n"
    exporter_text += f"# HELP total_nodes The total number of nodes registered in pterodactyl.\n# TYPE total_nodes gauge\ntotal_nodes {total_nodes}\n\n"
    exporter_text += f"# HELP total_servers The total number of servers registered in pterodactyl.\n# TYPE total_servers gauge\ntotal_servers {total_servers}\n\n"
    exporter_text += f"# HELP total_locations The total number of locations registered in pterodactyl.\n# TYPE total_locations gauge\ntotal_locations {total_locations}\n\n"

    for location in response["data"]:
        name = location["attributes"]["short"].replace(" ", "_").replace("-", "_")
        node_count = len(location["attributes"]["relationships"]["nodes"]["data"])
        server_count = len(location["attributes"]["relationships"]["servers"]["data"])
        exporter_text += f"# HELP {name}_nodes The total number of nodes at {name}.\n# TYPE {name}_nodes gauge\n{name}_nodes {node_count}\n\n"
        exporter_text += f"# HELP {name}_servers The total number of servers at {name}.\n# TYPE {name}_servers gauge\n{name}_servers {server_count}\n\n"

async def fetch_data():
    while True:
        await update_text()
        print("Updated exporter")
        await asyncio.sleep(300)


async def print_test():
    while True:
        print('Test')
        await asyncio.sleep(5)


async def handle(request):
    text = exporter_text
    return web.Response(text=text)


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/metrics', handle)])

runners = []

async def start_site(app, address='localhost', port=8080):
    runner = web.AppRunner(app)
    runners.append(runner)
    await runner.setup()
    site = web.TCPSite(runner, address, port)
    await site.start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(update_text())
    loop.create_task(start_site(app, address=HOST_NAME, port=PORT))
    loop.create_task(fetch_data())
    try:
        loop.run_forever()
    except:
        pass
