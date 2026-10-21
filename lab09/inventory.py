#!/usr/bin/env python3
"""Enkelt dynamiskt inventory för labbmiljön."""

import json
import sys

# Listan över servrar. I verkligheten skulle den komma från ett API.
SERVERS = [
    {"name": "node1", "address": "ls-node1.local", "user": "node1", "group": "webservers"},
    {"name": "node2", "address": "ls-node2.local", "user": "node2", "group": "dbservers"},
]


def build_inventory():
    inventory = {"_meta": {"hostvars": {}}}
    for server in SERVERS:
        group = server["group"]
        inventory.setdefault(group, {"hosts": []})
        inventory[group]["hosts"].append(server["name"])
        inventory["_meta"]["hostvars"][server["name"]] = {
            "ansible_host": server["address"],
            "ansible_user": server["user"],
        }
    return inventory


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        print(json.dumps(build_inventory(), indent=2))
    else:
        print(json.dumps({}))
