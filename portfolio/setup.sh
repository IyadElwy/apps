#!/bin/bash

touch /mnt/storage-server0/sda3/portfolio/data/db.sqlite

sqlite3 /mnt/storage-server0/sda3/portfolio/data/db.sqlite < ./db-init.sql

chmod 660 /var/run/docker.sock