# Arkitekturmotivering och systemdokumentation

**Författare:** Love Silventoinen
**Datum:** 2026-10-28
**Kurs:** Automation med Ansible

---

## 1. Systemöversikt och verktygsval

Jag har tre servrar med Ubuntu Server 24.04. ls-controlnode kör Ansible, ls-node1 är webbserver och ls-node2 är databasserver.

**Varför Ansible:** Jag valde Ansible för att det är agentlöst. Med bara tre servrar vore det onödigt att sätta upp en Puppetserver och installera agenter på alla noder. Det räcker med en controlnode.

**Agentlöst:** Ansible pushar ändringar över SSH. Alla mina servrar har redan SSH och Python, så jag behöver inte installera något extra på noderna. Det blir färre program att uppdatera och hålla säkra. Ändringar händer när jag kör playbooken, inte när en agent bestämmer det.

**Roller och mappar:** Jag har delat upp koden i tre roller. common skapar användare och installerar grundpaket, database sätter upp MariaDB och webapp sätter upp Flask, Gunicorn och Nginx. site.yml säger bara vilken roll som ska köras på vilken grupp. Det gör det lätt att förvalta. Vill jag ändra något i databasen ändrar jag bara i roles/database. Vill jag ha en till webbserver lägger jag bara till den i inventoryn. Hemligheter ligger i group_vars/all och rapporten till CMDB ligger i playbooks.

## 2. Säkerhet och hemligheter

**Ansible Vault:** Databaslösenordet ligger krypterat i group_vars/all/vault.yml. Koden använder bara variabeln vault_db_password, så lösenordet syns aldrig i klartext i repot. Uppgiften som skapar databasanvändaren har no_log: true så att lösenordet inte heller syns när playbooken körs. Lösenordet som låser upp valvet ligger i .vault_pass. Den filen finns bara på controlnode, bara jag kan läsa den, och den står i .gitignore så att den aldrig hamnar på GitHub. Loggar och .retry filer står också i .gitignore.

**Sudo:** Jag använder become: true bara där det behövs. Sudolösenordet skriver jag in med -K varje gång, så det sparas aldrig i någon fil. Rapporten till CMDB behöver inte sudo alls.

**SSH:** Ansible loggar in med SSH nycklar, inte lösenord. Den privata nyckeln stannar på controlnode och den publika ligger på noderna. devops_admin har ett eget nyckelpar. Den publika nyckeln ligger i repot, men det gör inget eftersom den inte är hemlig. GitHub når jag med en deploy key som bara funkar för det här repot.

## 3. Skalbarhet och dynamik

**Statiskt och dynamiskt inventory:** Jag använder inventory.ini, som är en vanlig fil. Det funkar bra för tre servrar som inte ändras så ofta. I Lab 9 gjorde jag ett dynamiskt inventory med ett Pythonskript. På riktigt skulle skriptet hämta servrarna från ett API, till exempel från molnet, och det är bättre när servrar läggs till och tas bort hela tiden. Eftersom site.yml kör på grupper får en ny server samma roller direkt när den hamnar i rätt grupp. Jag behöver inte ändra koden.

**Jinja2 och variabler:** Jag har inga fasta värden i koden. I mallen app.py.j2 fyller Ansible i databasens IP adress från facts och lösenordet från valvet. Därför kan samma roller användas för utveckling, test och produktion. Varje miljö får en egen inventory med egna variabler, men koden är samma.

## 4. Drift, optimering och återhämtning

**Idempotens:** Idempotens betyder att man kan köra samma playbook många gånger och få samma resultat. Ansible kollar först hur det ser ut och ändrar bara det som behövs. I Lab 3 blev det changed=1 första gången och changed=0 andra gången. Det gör att jag kan köra playbooken igen utan att vara rädd att förstöra något. Om någon har ändrat något för hand fixar Ansible bara det som är fel. En sak jag märkte är att uppgiften som skapar tabellen alltid säger changed, fast inget ändras, eftersom modulen inte kan se att tabellen redan finns.

**Felsökning och verifiering:** Innan jag ändrar något kan jag köra med --check. Då ser jag vad som skulle ändras utan att något händer. Det funkar inte för allt, uppgiften med tabellen hoppades över eftersom modulen inte stödjer det. Handlers startar bara om en tjänst om något faktiskt ändrats, så tjänster startas inte om i onödan. Efter en körning kollar jag att allt funkar med curl http://ls-node1.local och med systemctl is-active för labbapp, nginx och mariadb. Om något går fel läser jag felmeddelandet. I Lab 11 såg jag till exempel att en mapp saknades, eftersom uppgifterna körde i fel ordning.


