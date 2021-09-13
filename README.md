# PteroExporter
Prometheus exporter for Pterodactyl installs

## What it provides
PteroExporter will output metrics for your Pterodactyl install.

Four primary metrics are exposed:
```yml
total_users
total_nodes
total_servers
total_locations
```

Then for each location two additional metrics are exposed:
```yml
LOCATION_nodes
LOCATION_servers
```
`LOCATION` is replaced with the locations name with spaces replaced with _.

### Self hosting
Install requests:
`pip install requests`

Modify `PORT` on line 5 to the port you want to use.

Replace `BASE_URL` with the URL of your Pterodactyl install following the same format as what is there.

Replace `PTERO_API_KEY` with a application api key.

I recommend setting up a reverse proxy but it is not necessary.
