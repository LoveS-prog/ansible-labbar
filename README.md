# Ansible labbar

Automationsprojekt i kursen Automatisering med Configuration Management program. Projektet sätter upp en webbapp på ls-node1 som hämtar data från en databas på ls-node2.

## Miljö

- ls-controlnode med Ansible
- ls-node1: webbserver med Nginx, Gunicorn och Flask
- ls-node2: databasserver med MariaDB
- Ubuntu Server 24.04 på alla, och noderna nås via mDNS som ls-node1.local och ls-node2.local

## Köra projektet

Skapa först lösenordsfilen för Ansible Vault. Den finns inte i repot.

```bash
echo "DITT_VAULT_LOSENORD" > .vault_pass
chmod 600 .vault_pass
```

Sätt upp hela miljön:

```bash
ansible-playbook -i inventory.ini site.yml -K --vault-password-file .vault_pass
```

Skapa rapporten till CMDB:

```bash
ansible-playbook -i inventory.ini playbooks/report.yml --vault-password-file .vault_pass
```

Testa appen:

```bash
curl http://ls-node1.local
```

## Struktur

```
inventory.ini        noderna och grupperna
site.yml             huvudplaybook som kör alla roller
group_vars/all/      vault.yml med krypterade lösenord
roles/common/        användaren devops_admin och grundpaket
roles/database/      MariaDB med databas, användare och tabell
roles/webapp/        Flask, Gunicorn och Nginx
playbooks/           report.yml för rapporten till CMDB
lab01 till lab11/    varje labb med egen README
```

Varje labb kan också köras i sin egen mapp, se labbens README. ARCHITECTURE.md förklarar varför projektet är byggt så här.
