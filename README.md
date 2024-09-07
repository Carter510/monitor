# Monitor

Monitor is a simple tool designed to check if your servers and services are UP or DOWN by monitoring specific ports. This project helps you keep track of the availability of your infrastructure, and let you see if something is wrong

## Features

- **Server Monitoring:** Continuously checks if your servers are reachable.
- **Port Monitoring:** Ensures that specific ports on your servers are open and services are running.
- **Simple Setup:** Easy to install and use, with minimal configuration required.

# Installation

To install and start using Monitor with Docker, use the following command:

```bash
docker run --name monitor -d -p 5000:5000 carter510/monitor
