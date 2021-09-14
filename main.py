from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

HOST_NAME = "localhost"
PORT = 4830

BASE_URL = "https://panel.example.com"
USERS_URL = BASE_URL + "/api/application/users"
NODES_URL = BASE_URL + "/api/application/nodes"
SERVERS_URL = BASE_URL + "/api/application/servers"
LOCATIONS_URL = BASE_URL + "/api/application/locations?include=nodes,servers"
PTERO_API_KEY = ""

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == "/favicon.ico":
            self.send_response(404)
            return
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


        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(exporter_text, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((HOST_NAME, PORT), MyServer)
    print("Server started http://%s:%s" % (HOST_NAME, PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
