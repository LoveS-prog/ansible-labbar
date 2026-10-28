# Lab 11: Ansible jämfört med Puppet

## 1. Push och pull

I Ansible är det jag som startar körningen. Jag kör ansible-playbook på controlnode, och Ansible skickar ändringarna till noderna via SSH. Det kallas push.

I Puppet startar noden själv körningen. En agent på varje nod hämtar konfigurationen från en Puppetserver, var 30:e minut som standard. Det kallas pull.

## 2. Ordningen

I Ansible körs uppgifterna i den ordning de står. Jag testade att flytta uppgiften som skapar konfigurationsfilen före installationen av nginx (ordning.yml). Då blev det fel, eftersom mappen inte fanns än:

```
Destination directory /etc/nginx/sites-available does not exist
```

I Puppet hade det inte hänt, eftersom filen har require => Package['nginx']. Då vet Puppet att nginx måste installeras först, oavsett i vilken ordning raderna står.

## 3. Jämförelse

| | Ansible | Puppet |
|---|---|---|
| Arkitektur | Push. Ingen agent, controlnode ansluter till noderna via SSH. | Pull. En agent på varje nod hämtar konfigurationen från en Puppetserver. |
| Språk och syntax | YAML. Uppgifter i en playbook som körs i ordning. | Puppets eget språk. Resurser som beskriver hur det ska vara, med beroenden som require. |
| Fördelar | Inget behöver installeras på noderna. Lätt att komma igång och lätt att läsa. | Noderna rättar sig själva. Ändrar någon något för hand ändras det tillbaka. Fungerar bra med väldigt många servrar. |
| Nackdelar | Ändringar sker bara när någon kör playbooken. Ordningen måste vara rätt. | Kräver en agent på varje nod och en server att sköta. Ett eget språk att lära sig. |
