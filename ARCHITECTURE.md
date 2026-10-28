# Arkitekturmotivering och systemdokumentation

**Författare:** Love Silventoinen
**Datum:** 2026-10-28
**Kurs:** Automation med Ansible

---

## 1. Systemöversikt och verktygsval

Miljön består av tre servrar med Ubuntu Server 24.04. ls-controlnode kör Ansible, ls-node1 är webbserver och ls-node2 är databasserver.

**Val av verktyg:** Jag valde Ansible eftersom det är agentlöst. För tre servrar behövs ingen Puppetserver och inga agenter att installera och sköta. Det räcker med en controlnode.

**Agentlöst och agentbaserat:** Ansible använder en pushmodell över SSH. SSH och Python finns redan på Ubuntu Server, så det finns inget extra program att installera, uppdatera eller skydda på noderna. Ändringar sker när jag kör playbooken, inte när en agent själv hämtar dem.

**Mapp och rollstruktur:** Projektet är uppdelat i tre roller: common för användare och grundpaket, database för MariaDB och webapp för Flask, Gunicorn och Nginx. site.yml säger bara vilken roll som körs på vilken grupp. Med roller finns varje del bara på ett ställe, så en ändring görs i en fil, och en ny server läggs till med en rad i inventoryn. Krypterade variabler ligger i group_vars/all och rapporten till CMDB i playbooks.

## 2. Säkerhet och hemligheter

**Ansible Vault:** Databaslösenordet ligger krypterat med AES256 i group_vars/all/vault.yml. Playbooks och mallar använder variabeln vault_db_password, så lösenordet står aldrig i klartext i koden. Uppgiften som skapar databasanvändaren har no_log: true, så lösenordet syns inte heller i utskriften. Filen .vault_pass låser upp valvet. Den finns bara lokalt på controlnode med rättigheterna 600, och den står i .gitignore tillsammans med loggar och filer som slutar på .retry.

**Behörighetshöjning:** become: true används bara i de delar som behöver sudo. Lösenordet för sudo skrivs in med -K varje gång, så det sparas aldrig i någon fil. Rapporten till CMDB körs helt utan sudo.

**SSH:** Ansible loggar in med SSH nycklar av typen ed25519 i stället för lösenord. Den privata nyckeln lämnar aldrig controlnode, och den publika ligger i authorized_keys på noderna. Användaren devops_admin har ett eget nyckelpar. Den publika nyckeln får ligga i repot eftersom den inte är hemlig. Controlnode når GitHub med en deploy key som bara har åtkomst till det här repot.

## 3. Skalbarhet och dynamik

**Statiska och dynamiska inventories:** Projektet använder inventory.ini, en statisk fil. Den passar bra för tre servrar som sällan ändras. I Lab 9 byggde jag ett dynamiskt inventory, ett skript som tar fram servrarna från en lista. I verkligheten skulle listan komma från ett API, till exempel en molntjänst eller en CMDB, och då passar det bättre när servrar ofta skapas och tas bort. Eftersom site.yml kör på grupper som webservers och dbservers, får en ny server samma roller bara genom att hamna i rätt grupp. Koden behöver inte ändras.

**Jinja2 och variabler:** Koden och inställningarna är separerade. Mallen app.py.j2 innehåller inga fasta värden. Databasens IP adress hämtas från facts och lösenordet från valvet när playbooken körs. För utveckling, test och produktion kan varje miljö få en egen inventory med egna variabler, medan rollerna och site.yml är samma kod.

## 4. Drift, optimering och återhämtning

**Idempotens:** Idempotens betyder att samma playbook ger samma resultat varje gång. Modulerna kollar först hur det ser ut på noden och ändrar bara det som behövs. I Lab 3 blev det changed=1 första gången och changed=0 andra gången. Det gör det säkert att köra playbooken igen. Om någon har ändrat något för hand rättar Ansible bara det som avviker, utan att förstöra resten. Uppgiften som skapar tabellen i databasen säger changed varje gång, eftersom modulen inte kan se att tabellen redan finns, men ingenting ändras på riktigt.

**Felsökning och verifiering:** Innan en ändring körs jag en torrkörning med --check. Den visar vad som skulle ändras utan att ändra något. Den kan inte testa allt, till exempel hoppades uppgiften med tabellen över eftersom modulen inte klarar torrkörning. Handlers startar bara om en tjänst när något har ändrats, så tjänsterna inte startas om i onödan. Efter en körning kontrollerar jag att allt fungerar med curl http://ls-node1.local och med systemctl is-active för labbapp, nginx och mariadb. Om något går fel läser jag felmeddelandet. I Lab 11 visade det till exempel att en mapp inte fanns än, eftersom uppgifterna körde i fel ordning.
