# Ansible labbar

Labbar i kursen Automatisering med Configuration Management program. En mapp per labb.

## Miljö

- controlnode med Ansible
- ls-node1 som webbserver och ls-node2 som databasserver, båda med Ubuntu Server 24.04
- Noderna nås via mDNS som ls-node1.local och ls-node2.local

## Köra en labb

Gå till labbens mapp och kör kommandot som står i labbens README. Till exempel:

```bash
cd lab06
ansible-playbook -i inventory.ini site.yml -K
```

Från Lab 7 behövs även lösenordsfilen för Ansible Vault:

```bash
ansible-playbook -i inventory.ini site.yml -K --vault-password-file .vault_pass
```

Filen .vault_pass finns inte i repot. Den skapas lokalt och ignoreras av git.
