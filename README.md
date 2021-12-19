# PteroExporter
Prometheus exporter for Pterodactyl installs

## What it provides
PteroExporter will output metrics for your Pterodactyl install.

Four primary metrics are exposed:
```yml
pterodactyl_total_users
pterodactyl_total_nodes
pterodactyl_total_servers
pterodactyl_total_locations
```

Then for each location two additional metrics are exposed:
```yml
pterodactyl_LOCATION_nodes
pterodactyl_LOCATION_servers
```
`LOCATION` is replaced with the locations name with spaces replaced with _.

### Self hosting
`npm install`

`npm start`

#### config.json
`port` to the port you want to use.

`ptero_url` with the URL of your Pterodactyl panel (https://panel.website.com)

`api_key` with an admin API key with all read permissions

I recommend setting up a reverse proxy but it is not necessary.
