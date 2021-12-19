const express = require('express');
const JSONdb = require('simple-json-db');
const axios = require('axios');
const config = require('./config.json');
const app = express();
const port = config.port;

const db = new JSONdb('storage.json');

let axiosConfig = {
    headers: {
        Authorization: 'Bearer ' + config.api_key
    }
}

let locations = [];

fetchAPIData = (async () => {
    const userData = await axios.get(config.ptero_url + '/api/application/users', axiosConfig);
    db.set('total_users', userData.data.meta.pagination.total);

    const nodeData = await axios.get(config.ptero_url + '/api/application/nodes', axiosConfig);
    db.set('total_nodes', nodeData.data.meta.pagination.total);

    const serverData = await axios.get(config.ptero_url + '/api/application/servers', axiosConfig);
    db.set('total_servers', serverData.data.meta.pagination.total);

    const locationData = await axios.get(config.ptero_url + '/api/application/locations?include=nodes,servers', axiosConfig);
    db.set('total_locations', locationData.data.meta.pagination.total);

    locations = [];

    locationData.data.data.forEach(location => {
        let name = location.attributes.short.replaceAll(' ', '_').replaceAll('-', '_');
        let nodes = location.attributes.relationships.nodes.data.length;
        let servers = location.attributes.relationships.servers.data.length;
        let locationMin = { name: name, nodes: nodes, servers: servers };
        locations.push(locationMin);
    });

    db.set('locations', locations);
    console.log('Updated data');
});

fetchAPIData();

setInterval(async () => {
    fetchAPIData();
}, config.interval * 1000);


app.get('/', (req, res) => {
    res.send('Metrics are on /metrics');
});

app.get('/metrics', (req, res) => {
    res.set('Content-Type', 'text/plain');
    let responseString = '';
    responseString += `# HELP pterodactyl_total_users The total number of users registered in pterodactyl.\n# TYPE pterodactyl_total_users gauge\npterodactyl_total_users ${db.get('total_users')}\n\n`;
    responseString += `# HELP pterodactyl_total_nodes The total number of nodes registered in pterodactyl.\n# TYPE pterodactyl_total_nodes gauge\npterodactyl_total_nodes ${db.get('total_nodes')}\n\n`;
    responseString += `# HELP pterodactyl_total_servers The total number of servers registered in pterodactyl.\n# TYPE pterodactyl_total_servers gauge\npterodactyl_total_servers ${db.get('total_servers')}\n\n`;
    responseString += `# HELP pterodactyl_total_locations The total number of locations registered in pterodactyl.\n# TYPE pterodactyl_total_locations gauge\npterodactyl_total_locations ${db.get('total_locations')}\n\n`;
    locations.forEach(location => {
        responseString += `# HELP pterodactyl_${location.name}_nodes The total number of nodes for this location.\n# TYPE pterodactyl_${location.name}_nodes gauge\npterodactyl_${location.name}_nodes ${location.nodes}\n\n`;
        responseString += `# HELP pterodactyl_${location.name}_servers The total number of servers for this location.\n# TYPE pterodactyl_${location.name}_servers gauge\npterodactyl_${location.name}_servers ${location.servers}\n\n`;
    });
    res.send(responseString);
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
})