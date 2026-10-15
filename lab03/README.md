# Lab 3: Min första Playbook & Idempotens

## Playbook (web.yml)

```yaml
---
- name: Installera och starta nginx
  hosts: webservers
  become: true

  tasks:
    - name: Installera nginx
      apt:
        name: nginx
        state: present
        update_cache: true

    - name: Se till att nginx är igång och startar vid boot
      service:
        name: nginx
        state: started
        enabled: true
```

## Kommando

```bash
ansible-playbook -i inventory.ini web.yml -K
```

## Resultat

Första körningen:

```
node1 : ok=3    changed=1    unreachable=0    failed=0
```

Andra körningen:

```
node1 : ok=3    changed=0    unreachable=0    failed=0
```

## Varför changed=0?

Första gången fanns inte nginx på node1, så Ansible installerade den. Därför blev det changed=1.

Andra gången fanns nginx redan, så Ansible gjorde inget. Därför blev det changed=0.

Det kallas idempotens. Samma playbook ger samma resultat, hur många gånger man än kör den.
