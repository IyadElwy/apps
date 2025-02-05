# Interactive Portfolio Website with built-in Live Terminal
![portfolio](https://github.com/user-attachments/assets/8a41a2ae-5e8e-48b7-a7fb-47ae9e1a528b)


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



## Docker Swarm Integration:

Docker Swarm orchestrates the deployment, scaling, and management of services within a cluster. The introduction of Swarm brings several improvements to the system, including:

### Service Scaling and High Availability:

Services like the FastAPI application and Grafana are now deployed with Swarm, enabling easy horizontal scaling. For example, increasing replicas of the FastAPI service can help handle more traffic, and Swarm automatically distributes the load. Even the airflow dags run on the swarm cluster which ensures that the dags run on servers which have resources to handle the operations fast and efficient.

Swarm ensures that services are always available, automatically replacing any failed containers, which improves overall system reliability and uptime.
Service Dependencies:

### Load Balancing with Swarm:

Swarm's built-in load balancing automatically distributes incoming traffic across replicas of services like FastAPI and Grafana, optimizing resource usage and improving performance.


### Automatic Service Discovery:

Services deployed within Swarm can discover and communicate with each other without the need for manual IP management. For example, Grafana automatically connects to Loki without requiring explicit IP addresses, as Swarm handles the internal DNS resolution.
Rolling Updates:

### Swarm-Specific Networking Enhancements:
Swarm Overlay Networks:
Swarm uses overlay networks to facilitate communication between containers running on different nodes within the Swarm cluster. This allows for improved scalability and isolation of services.
The internal network (portfolio-network-internal) in Swarm now spans across multiple nodes, ensuring seamless communication even as the system scales.


### Security and Resource Constraints:

Swarm allows setting CPU and memory limits per service (e.g., Grafana, Loki), ensuring that no service overconsumes resources, maintaining system stability.
You can now deploy services with specific resource constraints, preventing resource contention between services.
Service Replication and Fault Tolerance:

Swarm automatically ensures that the desired number of replicas for each service is maintained. If a container fails or a node goes down, Swarm reschedules tasks on other available nodes, ensuring high availability and fault tolerance.

### Health Checks and Restart Policies:
Service Health Checks:
Docker Swarm supports health checks, and this is critical in the current architecture to ensure that services like the api and vm are only running when fully operational.

