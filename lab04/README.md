# Lab 4: Användare och behörigheter

## Nyckelpar för devops_admin

```bash
ssh-keygen -t ed25519 -f ~/.ssh/devops_admin -C "devops_admin@controlnode"
```

## Playbook (users.yml)

```yaml
---
- name: Skapa användaren devops_admin
  hosts: all
  become: true

  tasks:
    - name: Skapa devops_admin och lägg till i gruppen sudo
      ansible.builtin.user:
        name: devops_admin
        state: present
        create_home: true
        shell: /bin/bash
        groups: sudo
        append: true

    - name: Lägg in publika nyckeln för devops_admin
      ansible.posix.authorized_key:
        user: devops_admin
        state: present
        key: "{{ lookup('file', '~/.ssh/devops_admin.pub') }}"
```

## Kommando

```bash
ansible-playbook -i inventory.ini users.yml -K
```

## Verifiering

```bash
ssh -i ~/.ssh/devops_admin devops_admin@ls-node1.local 'hostname; groups'
```

```
ls-node1
devops_admin sudo
```

```bash
ssh -i ~/.ssh/devops_admin devops_admin@ls-node2.local 'hostname; groups'
```

```
ls-node2
devops_admin sudo
```

Inloggningen fungerar utan lösenord på båda noderna, och devops_admin är med i gruppen sudo.
