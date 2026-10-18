# Lab 5: Strukturering med Ansible Roles

Två roller:

- common körs på alla noder: grundpaket och användaren devops_admin från Lab 4
- webserver körs på node1: nginx, en startsida och en handler som startar om nginx

## site.yml

```yaml
---
- name: Gemensam grund på alla noder
  hosts: all
  become: true
  roles:
    - common

- name: Webbserver
  hosts: webservers
  become: true
  roles:
    - webserver
```

## Rollstruktur

```bash
tree roles/
```

```
roles/
├── common
│   ├── defaults
│   │   └── main.yml
│   ├── files
│   ├── handlers
│   │   └── main.yml
│   ├── meta
│   │   └── main.yml
│   ├── README.md
│   ├── tasks
│   │   └── main.yml
│   ├── templates
│   ├── tests
│   │   ├── inventory
│   │   └── test.yml
│   └── vars
│       └── main.yml
└── webserver
    ├── defaults
    │   └── main.yml
    ├── files
    ├── handlers
    │   └── main.yml
    ├── meta
    │   └── main.yml
    ├── README.md
    ├── tasks
    │   └── main.yml
    ├── templates
    ├── tests
    │   ├── inventory
    │   └── test.yml
    └── vars
        └── main.yml

19 directories, 16 files
```

## Körning

```bash
ansible-playbook -i inventory.ini site.yml -K
```

```
PLAY [Gemensam grund på alla noder] ************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]
ok: [node2]

TASK [common : Installera grundpaket] **********************************************************************************
changed: [node2]
changed: [node1]

TASK [common : Skapa devops_admin och lägg till i gruppen sudo] ********************************************************
ok: [node1]
ok: [node2]

TASK [common : Lägg in publika nyckeln för devops_admin] ***************************************************************
ok: [node1]
ok: [node2]

PLAY [Webbserver] ******************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [webserver : Installera nginx] ************************************************************************************
ok: [node1]

TASK [webserver : Lägg in en enkel startsida] **************************************************************************
changed: [node1]

TASK [webserver : Se till att nginx är igång och startar vid boot] *****************************************************
ok: [node1]

RUNNING HANDLER [webserver : Starta om nginx] **************************************************************************
changed: [node1]

PLAY RECAP *************************************************************************************************************
node1                      : ok=9    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Kontroll

```bash
curl http://ls-node1.local
```

```
Webbservern installerad med en roll i Ansible
```
