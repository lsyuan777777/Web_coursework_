#!/usr/bin/env python
"""CosmicLens API Management Script"""
import sys
import subprocess


def run_command(cmd):
    """Run a shell command"""
    subprocess.run(cmd, shell=True, check=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage.py <command>")
        print("\nCommands:")
        print("  server      - Start the API server")
        print("  init        - Initialize the database")
        print("  import <file> - Import data from CSV file")
        print("  test        - Test API endpoints")
        sys.exit(1)

    command = sys.argv[1]

    if command == "server":
        run_command("uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    elif command == "init":
        run_command("python -m app.scripts.init_db")
    elif command == "import":
        if len(sys.argv) < 3:
            print("Error: Please specify CSV file path")
            sys.exit(1)
        run_command(f"python -m app.scripts.init_db import {sys.argv[2]}")
    elif command == "test":
        print("Testing API...")
        run_command('curl -s http://localhost:8000/api/v1/pictures?page=1 | python3 -m json.tool')
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
