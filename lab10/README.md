# Lab 10: Driftsättning av Flerskiktsapplikation (VG)

## Så hänger det ihop

```
Besökare → Nginx (node1, port 80) → Gunicorn (node1, 127.0.0.1:8000) → Flask app → MariaDB (node2, port 3306)
```

- Nginx tar emot besökare och skickar vidare till Gunicorn. Det kallas reverse proxy.
- Gunicorn kör Flask appen som systemd tjänsten labbapp.
- Appen hämtar ett meddelande från databasen labbdb på node2.
- Ansible fyller i node2:s IP adress i appen med facts, och lösenordet kommer från valvet.

## Kommando

```bash
ansible-playbook -i inventory.ini site.yml -K --vault-password-file .vault_pass
```

Filen .vault_pass finns inte i repot.

## Roller

- database: installerar MariaDB, öppnar för anslutningar från andra servrar och skapar databasen labbdb, användaren appuser och tabellen meddelanden.
- webapp: installerar Flask, Gunicorn, PyMySQL och Nginx, lägger in appen, gör den till en systemd tjänst och sätter upp Nginx som reverse proxy.

## Verifiering

```bash
curl http://ls-node1.local
```

```
<h1>VG: node1 hämtade data från databasen på 10.6.69.109</h1><p>Hej från databasen på node2!</p>
```

```bash
ansible webservers -i inventory.ini --vault-password-file .vault_pass -a "systemctl is-active labbapp nginx"
```

```
node1 | CHANGED | rc=0 >>
active
active
```

```bash
ansible dbservers -i inventory.ini --vault-password-file .vault_pass -a "systemctl is-active mariadb"
```

```
node2 | CHANGED | rc=0 >>
active
```
