# Lab 2: Ad-hoc-kommandon

Ad-hoc-kommandon är enstaka kommandon som körs direkt från terminalen mot noderna i inventoryn, utan playbook.

## Uppgift 1: Diskutrymme med `df -h /`

```bash
ansible all -i inventory.ini -m command -a "df -h /"
```

```
node1 | CHANGED | rc=0 >>
Filesystem                         Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-ubuntu--lv   61G  5.1G   53G   9% /
node2 | CHANGED | rc=0 >>
Filesystem                         Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-ubuntu--lv   61G  5.8G   52G  11% /
```


## Uppgift 2: Linux-distribution via facts

Ansible samlar in information om varje maskin, så kallade facts, med modulen `setup`. Med `filter` plockar man ut bara de fält man vill ha, här Linux-distributionen.

```bash
ansible all -i inventory.ini -m setup -a "filter=ansible_distribution*"
```

```
node1 | SUCCESS => {
    "ansible_facts": {
        "ansible_distribution": "Ubuntu",
        "ansible_distribution_file_parsed": true,
        "ansible_distribution_file_path": "/etc/os-release",
        "ansible_distribution_file_variety": "Debian",
        "ansible_distribution_major_version": "24",
        "ansible_distribution_release": "noble",
        "ansible_distribution_version": "24.04",
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false
}
node2 | SUCCESS => {
    "ansible_facts": {
        "ansible_distribution": "Ubuntu",
        "ansible_distribution_file_parsed": true,
        "ansible_distribution_file_path": "/etc/os-release",
        "ansible_distribution_file_variety": "Debian",
        "ansible_distribution_major_version": "24",
        "ansible_distribution_release": "noble",
        "ansible_distribution_version": "24.04",
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false
}
```

