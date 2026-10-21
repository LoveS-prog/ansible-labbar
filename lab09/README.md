# Lab 9: Dynamiska Inventories

Ett dynamiskt inventory är ett skript som tar fram listan över servrar när Ansible frågar. Här ligger listan i skriptet, men i verkligheten skulle skriptet hämta den från ett API, till exempel en molntjänst eller en CMDB.

## Kommandon

```bash
./inventory.py --list
ansible-inventory -i inventory.py --list
ansible all -i inventory.py -m ping
```

## Källkod (inventory.py)

```python
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
```

## ansible-inventory --list

```
{
    "_meta": {
        "hostvars": {
            "node1": {
                "ansible_host": "ls-node1.local",
                "ansible_user": "node1"
            },
            "node2": {
                "ansible_host": "ls-node2.local",
                "ansible_user": "node2"
            }
        }
    },
    "all": {
        "children": [
            "ungrouped",
            "webservers",
            "dbservers"
        ]
    },
    "dbservers": {
        "hosts": [
            "node2"
        ]
    },
    "webservers": {
        "hosts": [
            "node1"
        ]
    }
}
```

## Ping via det dynamiska inventoryt

```
node1 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
node2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```
