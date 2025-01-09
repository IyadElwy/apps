# Interactive Portfolio Website with built-in Live Terminal

![portfolio](https://github.com/user-attachments/assets/a49ffb6e-d2b9-4dec-9e4e-7c1084ede3aa)


# Architecture


## Components


### Cloudflare Integration:

A Cloudflare Tunnel is used to securely expose the platform to the internet, ensuring robust security and reliability.
Cloudflare CDN optimizes performance and protects the platform from threats like DDoS attacks.


### FastAPI Application:

Serves as the central API layer for handling user requests.
Allows interaction with movie data via predefined endpoints.
Connects to an SQLite database hosted on a mounted volume.


### Apache Airflow:

Runs a Directed Acyclic Graph (DAG) pipeline for ETL (Extract, Transform, Load) processes.
Retrieves, processes, and stores movie-related data.
DAGs are triggered manually through the Airflow API or CLI for controlled operation.


### VM Container:

A sandboxed environment designed to execute user commands interactively.
Implements a restricted command-line interface to ensure security and isolate operations.
Enables controlled interaction with the data for analysis or retrieval.



## Networking
### Container Networks:
portfolio-network-external: A bridged Docker network enabling communication with external systems (e.g., Cloudflare Tunnel).
portfolio-network-internal: A bridged internal network isolating system components to enhance security.


## Storage
Docker Bind Mounts:
Shared storage between containers, ensuring persistent data access across the system.
Key paths:
/app/appdata/db.sqlite (airflow)
/app/temp_data (airflow)
/appdata/db.sqlite (app)
/etc/loki

## Security
Restricted User Environment:

The "narrator user" is created as a limited shell (rbash) within the VM container, allowing only predefined commands.
This approach ensures the integrity of the system by blocking unauthorized or unsafe operations.

Cloudflare Tunnel:
Adds an additional layer of security by exposing services via a trusted intermediary.


## Logging

### Loki Logging Integration
Loki, a log aggregation system, is integrated into this architecture to streamline and improve the monitoring and troubleshooting of the system's components. It adds the following key features and benefits:

Centralized Logging for Airflow DAGs and FastAPI Server

Airflow Logs: Loki collects and stores logs from the Apache Airflow DAGs, providing insights into the status of data processing 
tasks. It allows real-time tracking of task execution and failures, making it easier to debug any issues.


FastAPI Logs: Loki also captures logs from the FastAPI server, allowing you to monitor requests, errors, and API interactions. This ensures that any issues with the API layer are tracked efficiently.



At the moment the project runs on one machine with the potential for horizontal scaling using container orchestrators like docker swarm or K8s and reverse proxies like ngnix for load balancing.
