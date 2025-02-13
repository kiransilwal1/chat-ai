#!/bin/bash

# Change directory to chatai/
cd chatai/ || {
  echo "Directory chatai/ not found!"
  exit 1
}

# Run Alembic migration commands
alembic revision --autogenerate -m "initial migration"
alembic upgrade head

echo "Deployment completed successfully!"
