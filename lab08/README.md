# Lab 8: Hantering av CMDB och Configuration Items (CIs)

## Kommando

```bash
ansible-playbook -i inventory.ini report.yml
```

Playbooken samlar in facts och installerade paket från alla noder. Sedan skriver den rapporten [inventory_report.md](inventory_report.md) med mallen templates/inventory_report.md.j2.

## Koppling till CMDB

Varje server i labbmiljön är en CI: ls-node1, ls-node2 och ls-controlnode. Hostname, OS, CPU, RAM, IP och upptid är egenskaper som beskriver varje CI. I en CMDB sparas varje CI med sina egenskaper och relationer, och rapporten från Ansible ger just den informationen. Det tar mindre tid än att skriva för hand, och det blir rätt, eftersom en person kan göra fel. Relationerna visar vad som påverkas om en server går ner, så att man snabbare hittar var felet är och kan lösa det.
