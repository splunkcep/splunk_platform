# Splunk Enterprise Security 8.0.2 Setup Guide

This project documents the step-by-step procedure originally executed in a Google Colab environment, now adapted into Markdown format for professional GitHub repositories.

The goal is to make the content clear, organized, and reusable by any Splunk analyst or architect aiming to install and configure **Splunk ES 8.0.2**.

---

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Detailed Procedure](#detailed-procedure)
- [Conclusion](#conclusion)
- [Final Notes](#final-notes)

---

## Introduction

This document was originally based on a practical notebook created to facilitate the installation and configuration of Splunk Enterprise Security 8.0.2 in controlled environments.

## Prerequisites

Before starting, make sure you have:

- Access to a Splunk Enterprise environment installed (compatible with ES 8.0.2).
- A valid Splunk ES license.
- Administrative permissions on the Splunk instance.
- Proper connectivity between Splunk components.
- Google Colab (originally used) or an equivalent Python execution environment (optional).

# Regras de Firewall

## Prerequisites

Ensure `iptables` is installed and you have **root privileges** to run the commands below.

## 1. Add Firewall Rules

# Allow Splunk Web Interface
```bash
sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
```
```bash
# Allow Splunk Management Interface (SSL)
sudo iptables -I INPUT -p tcp --dport 8443 -j ACCEPT

# Allow Secure Web Interface (HTTPS)
sudo iptables -I INPUT -p tcp --dport 443 -j ACCEPT

# Allow HTTP Event Collector (HEC)
sudo iptables -I INPUT -p tcp --dport 8088 -j ACCEPT

# Allow Universal Forwarder Port
sudo iptables -I INPUT -p tcp --dport 9997 -j ACCEPT
```

---

## 2. Save Rules (Persistent on Reboot)

### For CentOS / RHEL

```bash
sudo yum install -y iptables-services
sudo service iptables save
sudo systemctl enable iptables
```

### For Ubuntu / Debian

```bash
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
sudo netfilter-persistent reload
```
---

## 3. Verify Open Ports

```bash
sudo iptables -L -n -v | grep tcp
```

You should see the ports **8000, 8443, 443, 8088, and 9997** listed with ACCEPT rules.

---

## Notes

- These rules apply to **IPv4**. For **IPv6**, use `ip6tables`.
- Consider securing your server with `fail2ban` or `ufw` if running in production.
- Use `iptables-save` to export your current configuration at any time.

---

## References

- [Splunk Enterprise Network and Port Requirements](https://docs.splunk.com/Documentation/Splunk/latest/Admin/Ports)
- [iptables Documentation](https://linux.die.net/man/8/iptables)

______


## Cisco ASA and Carbon Black EDR Log Integration in Splunk ES 8

💾 2. Save rules for persistence after reboot

For Debian/Ubuntu based systems:


```python
sudo iptables-save | sudo tee /etc/iptables.rules
```

🔄 3. Apply rules after reboot

To ensure that the rules are applied at boot:


```python
sudo bash -c "echo -e '#!/bin/sh\n/sbin/iptables-restore < /etc/iptables.rules' > /etc/network/if-pre-up.d/iptables"
```


```python
sudo chmod +x /etc/network/if-pre-up.d/iptables
```

✅ 4. Check if the rules were applied


```python
sudo iptables -L -n
```

This will list all the rules configured in iptables, including the newly added ports.

# Disabling Transparent Huge Pages (THP) before installing the Splunk Enterprise Trial

Transparent Huge Pages (THP) can negatively impact Splunk performance. Therefore, Splunk recommends that this setting be disabled before installation.

1️⃣ Check current THP status

Before making any changes, make sure THP is enabled on your system:


```python
cat /sys/kernel/mm/transparent_hugepage/enabled
```

If the output says [always] or [madvise], it means that THP is enabled and needs to be disabled.

2️⃣ Edit the GRUB configuration file

Open the GRUB configuration file with vi (or another editor of your choice):


```python
sudo vi /etc/default/grub
```

Locate the line that begins with GRUB_CMDLINE_LINUX and add transparent_hugepage=never to the end of the line, inside the quotes.

Example:


```python
GRUB_CMDLINE_LINUX="rhgb quiet transparent_hugepage=never"
```

Save and exit the editor (ESC → :wq → Enter).

3️⃣ Update GRUB

After editing the file, generate a new GRUB configuration with the following command:


```python
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

4️⃣ Restart the system

Now, restart the server to apply the changes:


```python
sudo reboot
```

5️⃣ Check if THP has been disabled

After reboot, confirm that THP is disabled:


```python
cat /sys/kernel/mm/transparent_hugepage/enabled
```

The output should show ”[never]”, indicating that THP was successfully disabled.

🔗 Official Documentation

For more information, see the official Splunk documentation:
🔗 Splunk and THP - Transparent Huge Pages

# 📌 Step by Step: Installing Splunk Enterprise Trial on Linux

🔹 1️⃣ Accessing the Server via SSH

Open a terminal and connect to the server via SSH:

`ssh Nome_Do_Usuario@<IP_DO_SERVIDOR>`

🔹 Replace:
	•	User_Name by the operating system or domain user.
	•	<SERVER_IP> with the actual IP of the host where you want to install Splunk.

🔹 2️⃣ Creating a User for Splunk

To ensure a secure installation, we will create a dedicated user to run Splunk:

🔹 This command:
	•	Creates a user called splunkuser.


```python
sudo useradd -m -r splunkuser
```

🔹 This command:
	•	It asks you to set a password for it.


```python
sudo passwd splunkuser
```

🔑 *Credentials:
	•	OS User: splunkuser
	•	OS Password: Set in the above command*

 🔹 3️⃣ Adding the Splunk User to the Sudo Group

1️Add splunkuser to the sudo group:


```python
sudo usermod -aG sudo splunkuser
```

Verify that the addition was successful:


```python
groups splunkuser
```

To switch to bash, run:


```python
sudo chsh -s /bin/bash splunkuser
```

Apply the changes by logging out and logging back in as splunkuser:


```python
su - splunkuser
```

Where am I?


```python
pwd
```

Who am I?


```python
whoami
```

What do I have?


```python
ls
```

What permissions are associated with what I have?


```python
ls -lha
```

🔹 4️⃣ Downloading the Splunk Installer

🔹 This command:
	•	Download Splunk Enterprise version 9.4.1.
	•	If you want another version, adjust the link in wget.


```python
sudo wget -O splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz "https://download.splunk.com/products/splunk/releases/9.4.1/linux/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz"
```

Now, go to your downloads directory:


```python
cd /home/splunkuser/
```

🔹 5️⃣ Adjusting Permissions on the Installation File

Before installing, check the file permissions:


```python
ls -lha /home/splunkuser
```

Give execute permission to the file:


```python
sudo chmod +x /home/splunkuser/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz
```

Double check the permissions:


```python
ls -lha /home/splunkuser
```

🔹 6️⃣ Creating the Splunk Installation Directory


```python
sudo mkdir /opt/splunk
```

Now, change the owner of the folder to the splunkuser user:


```python
sudo chown -R splunkuser:splunkuser /opt/splunk
```

```python
sudo chown -R splunkuser:splunkuser /opt/splunk
```

Check if the permissions are correct:


```python
ls -lha /opt/splunk
```

🔹 7️⃣ Installing Splunk

Extract the downloaded file to /opt
(📌 This will install Splunk in the folder /opt/splunk):


```python
tar -xzvf splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz -C /opt
```

🔹 8️⃣ Starting Splunk

Now, launch Splunk and accept the license:


```python
/opt/splunk/bin/splunk start --accept-license
```

🔑
* Splunk Default Credentials:
*	OS User: splunkuser
*	OS Password: (definida anteriormente)
*	Splunk User: admin
*	Splunk Password: splunkuser

🔹 9️⃣ Setting Splunk to Start Automatically

To ensure that Splunk starts automatically when you restart the server:


```python
sudo /opt/splunk/bin/splunk enable boot-start -user splunkuser --accept-license --answer-yes --no-prompt
```

This configures the Splunk service to start automatically when the system starts.

Check the startup file:


```python
sudo vi /etc/init.d/splunk
```

Add the following lines (if necessary):


```python
RETVAL=0
USER=splunkuser
. /etc/init.d/functions
```

🔹 🔄 Basic Commands to Manage Splunk

Check status


```python
/opt/splunk/bin/splunk status
```

Launch Splunk


```python
/opt/splunk/bin/splunk start
```

Stop Splunk


```python
/opt/splunk/bin/splunk stop
```

Restart Splunk


```python
/opt/splunk/bin/splunk restart
```

Splunk is now installed and configured on your Linux server. To access it via a web browser, open:


```python
http://<IP_DO_SERVIDOR>:8000
```

# Integrar logs de Cisco ASA Firewall e Carbon Black EDR ao Splunk Enterprise Security (ES) 8, garantindo conformidade com o Common Information Model (CIM).

📌 1. Criar os Indexes no Splunk

O Splunk ES usa indexes específicos para cada tipo de dado. Vamos criar os indexes corretos:

Criar index para logs do Cisco ASA Firewall


```python
/opt/splunk/bin/splunk add index network -datatype event -maxTotalDataSizeMB 50000 -homePath.maxDataSizeMB 10000
```

Usuário Admin

Criar index para logs do Carbon Black EDR


```python
/opt/splunk/bin/splunk  add index edr -datatype event -maxTotalDataSizeMB 50000 -homePath.maxDataSizeMB 10000
```

🔹 network → Para logs de firewall e segurança de rede.
🔹 edr → Para logs de detecção e resposta de endpoint (EDR).

🚀 Reinicie o Splunk para aplicar as mudanças:


```python
splunk /opt/splunk/bin/splunk restart
```

📌 2. Criar as Stanzas de Entrada (inputs.conf)

Agora vamos configurar o Splunk Add-on correspondente para que ele colete os logs.

➡️ Cisco ASA Firewall

Verificando se existe pasta local no add on Cisco Asa:


```python
ls /opt/splunk/etc/apps/Splunk_TA_cisco-asa/
```

Caso não tenha crie a pasta:


```python
mkdir /opt/splunk/etc/apps/Splunk_TA_cisco-asa/local
```

📌 Arquivo: /opt/splunk/etc/apps/Splunk_TA_cisco-asa/local/inputs.conf


```python
vi /opt/splunk/etc/apps/Splunk_TA_cisco-asa/local/inputs.conf
```

Use "i" para inserir


```python
i
```

Cole a stanza abaixo:


```python
[monitor:///var/log/splunk_real_env/cisco_firewall.log]
index = network
sourcetype = cisco:asa
disabled = false
```

➡️ Carbon Black EDR

📌 Arquivo: /opt/splunk/etc/apps/Splunk_TA_carbonblack/local/inputs.conf

Caso não tenha crie a pasta:


```python
vi /opt/splunk/etc/apps/Splunk_TA_carbonblack/local/inputs.conf
```


```python
[monitor:///var/log/splunk_real_env/carbon_black_edr.log]
index = edr
sourcetype = carbonblack:edr
disabled = false
```

🚀 Reinicie o Splunk para aplicar as mudanças:


```python
/opt/splunk/bin/splunk restart
```

📌 3. Criar Scripts para Gerar Eventos de Teste

Criando pasta local:


```python
sudo mkdir /var/log/splunk_real_env/
```

Verificando pasta local:


```python
ls -lha /var/log/
```

Agora criamos dois scripts para simular eventos reais.

➡️ Script para Gerar Logs de Cisco ASA

📌 Arquivo: /var/log/splunk_real_env/generate_cisco_asa_logs.py


```python
sudo vi /var/log/splunk_real_env/generate_cisco_asa_logs.py
```


```python
import time
import random

log_path = "/var/log/splunk_real_env/cisco_firewall.log"

sample_logs = [
    "Mar 12 12:34:56 hostname %ASA-6-106100: access-list inside_access_in permitted tcp inside/192.168.1.10(12345) -> outside/8.8.8.8(443) hit-cnt 1 first hit",
    "Mar 12 12:35:10 hostname %ASA-6-302015: Built outbound UDP connection 1234 for outside:8.8.8.8/53 to inside:192.168.1.20/54231",
]

while True:
    with open(log_path, "a") as log_file:
        log_file.write(random.choice(sample_logs) + "\n")
    time.sleep(3)  # Envia logs a cada 3 segundos
```

🔹 Gera eventos aleatórios de firewall e escreve no arquivo de logs.



➡️ Script para Gerar Logs de Carbon Black EDR

📌 Arquivo: /var/log/splunk_real_env/generate_carbon_black_edr_logs.py


```python
import time
import random

log_path = "/var/log/splunk_real_env/carbon_black_edr.log"

sample_logs = [
    'Timestamp: 2025-03-12 12:10:26, Sensor ID: 12345, Event Type: Process Creation, Process Name: "cmd.exe", Process Path: "C:\\Windows\\System32\\cmd.exe", Arguments: "/c powershell.exe -noprofile -executionpolicy bypass"',
    'Timestamp: 2025-03-12 12:15:10, Sensor ID: 54321, Event Type: File Modification, File Name: "malicious.exe", File Path: "C:\\Users\\Public\\Downloads\\malware.exe"',
]

while True:
    with open(log_path, "a") as log_file:
        log_file.write(random.choice(sample_logs) + "\n")
    time.sleep(30)  # Envia logs a cada 30 segundos
```

🔹 Simula processos suspeitos detectados pelo Carbon Black EDR.

🚀 Tornar os scripts executáveis e rodá-los em segundo plano:


```python
sudo chmod +x /var/log/splunk_real_env/generate_cisco_asa_logs.py
```

Veja se o processo está ativo:


```python
ps aux | grep generate_cisco_asa_logs.py
```

Se aparecer algo como:


```python
username  35943  0.0  0.1  12345  6789 pts/0    S    14:30   0:00 python3 /var/log/splunk_real_env/generate_cisco_asa_logs.py
```

Isso significa que o script está rodando.


```python
sudo chmod +x /var/log/splunk_real_env/generate_carbon_black_edr_logs.py
```


```python
sudo nohup python3 /var/log/splunk_real_env/generate_cisco_asa_logs.py > /dev/null 2>&1 &
```


```python
sudo nohup python3 /var/log/splunk_real_env/generate_carbon_black_edr_logs.py > /dev/null 2>&1 &
```

📌 4. Mapear os Indexes no ES (macros.conf)

Agora precisamos configurar o Splunk Enterprise Security (ES) para reconhecer os logs no CIM (Common Information Model).

📌 Arquivo: /opt/splunk/etc/apps/SplunkEnterpriseSecuritySuite/local/macros.conf

➡️ Cisco ASA (Network_Traffic)


```python
[Network_Traffic_Indexes]
definition = (index=network OR index=main)
iseval = 0
```

➡️ Carbon Black EDR (Endpoint)


```python
[Endpoint_Indexes]
definition = (index=edr OR index=main)
iseval = 0
```

🚀 Após editar, aplique as mudanças:


```python
splunk /opt/splunk/bin/splunk restart
```

📌 5. Testar os Logs no Splunk

Agora vamos testar se os eventos estão aparecendo corretamente nos Dashboards do ES.

➡️ Teste para Cisco ASA


```python
| tstats count FROM datamodel=Network_Traffic.All_Traffic WHERE index=network BY _time, All_Traffic.src, All_Traffic.dest
```

➡️ Teste para Carbon Black EDR


```python
| tstats count FROM datamodel=Endpoint.Processes WHERE index=edr BY _time, Processes.process_name
```

Se os eventos aparecerem, significa que os logs estão sendo normalizados corretamente no ES. 🚀

Resumo Final



* ✅ Criamos os indexes (network e edr) para garantir que os logs sejam armazenados corretamente.
* ✅ Configuramos as entradas (inputs.conf) para monitorar os arquivos de log.
* ✅ Criamos scripts Python para gerar eventos reais de Cisco ASA e Carbon Black EDR.
* ✅ Adicionamos os indexes nas Search Macros (macros.conf) para que o Splunk ES os reconheça.
* ✅ Testamos os logs no Splunk ES e confirmamos que os dashboards estão funcionando corretamente.

# Transferindo o Splunk ES 8 para o splunk via SCP

Acesse o diretorio onde você fez o donwload do arquivo. Por exemplo:


```python
cd /Users/Levi/Downloads/splunk-enterprise-security_802.spl
```

Abra o terminal e faça a transferência:


```python
scp splunk-enterprise-security_802.spl splunkuser@SEU_IP:/home/splunkuser
```

Confira se o arquivo chegou corretamente:


```python
ls -lha /home/splunkuser/splunk-enterprise-security_802.spl
```

Adicione permissão de execução no arquivo:


```python
sudo chmod +x /home/splunkuser/splunk-enterprise-security_802.spl
```

Confirme que existe agora permissão de execução "x":


```python
ls -lha /home/splunkuser/splunk-enterprise-security_802.spl
```

# Instalando o ES 8

Acesse o diretorio com o arquivo spl:


```python
cd /home/splunkuser/
```

Comando para instalar o Enterprise Security 8:


```python
sudo /opt/splunk/bin/splunk install app /home/splunkuser/splunk-enterprise-security_802.spl -auth admin:splunkuser
```

🕒 Aumentar o Timeout do Splunk Web

Verifique se existe a pasta local:


```python
ls /opt/splunk/etc/system/
```

Caso a pasta não exista crie:


```python
sudo mkdir /opt/splunk/etc/system/local
```

Reforce as permissões para nosso usuário:


```python
sudo chown -R splunkuser:splunkuser /opt/splunk
```

Edite oe / ou arquivo web.conf:


```python
sudo vi /opt/splunk/etc/system/local/web.conf
```

Adicione (ou edite) a seção abaixo para aumentar o tempo limite:


```python
[settings]
startwebserver = true
splunkdConnectionTimeout = 300
```

Isso aumentará o tempo limite para 300 segundos (5 minutos).

Salve e saia do editor (ESC → :wq → Enter).

⚙️ Ajustar Timeout no splunk-launch.conf

Edite o arquivo:


```python
sudo vi /opt/splunk/etc/splunk-launch.conf
```

Adicione a linha abaixo no final do arquivo:


```python
SPLUNKD_CONNECTION_TIMEOUT=300
```

Salve e saia (ESC → :wq → Enter).

Reinicie o Splunk:


```python
sudo /opt/splunk/bin/splunk restart
```

# Simulando um SQL Inject

Script Python para simular SQL Injection:


```python
sudo vi /var/log/splunk_real_env/sql_injection_simulation.py
```


```python
import time
import random
import logging
from datetime import datetime

# Configuração do logger para gravar em um arquivo de log
log_file = '/var/log/splunk_real_env/cisco_ips.log'  # Defina o caminho para o arquivo de log
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] [%(message)s]')

# Função para gerar SQL Injection (simulado)
def generate_sql_injection():
    # SQL Injection simples simulando um ataque
    injection_attempts = [
        "OR 1=1 --",
        "' OR 'a'='a",
        "' UNION SELECT NULL, username, password FROM users --",
        "'; DROP TABLE users --",
        "' OR 'x'='x",
        "admin' --",
        "' OR 1=1#",
        "admin' OR '1'='1' --",
        "' OR '' = '",
        "'; EXEC xp_cmdshell('dir') --"
    ]

    # Escolha uma tentativa aleatória de injeção SQL
    return random.choice(injection_attempts)

# Função para gerar um log de SQL Injection simulado
def log_sql_injection():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    source_ip = "192.168.1." + str(random.randint(1, 255))  # IP de origem aleatório
    destination_ip = "10.0.0." + str(random.randint(1, 255))  # IP de destino aleatório
    sql_injection = generate_sql_injection()

    # Log formatado
    log_message = f"[INFO] {timestamp} src_ip={source_ip} dest_ip={destination_ip} sql_injection={sql_injection} eventtype=cisco-security-events"

    # Grava no arquivo de log
    logging.info(log_message)
    print(log_message)

# Loop para gerar uma tentativa de SQL Injection a cada 30 segundos
try:
    while True:
        log_sql_injection()
        time.sleep(30)  # Espera 30 segundos antes da próxima tentativa
except KeyboardInterrupt:
    print("Script interrompido pelo usuário.")
```


```python
sudo chmod +x sql_injection_simulation.py
```


```python
ls -lha
```

Configurando o CIM compliance search macro:


```python
vi /opt/splunk/etc/apps/SplunkEnterpriseSecuritySuite/local/macros.conf
```


```python
[monitor:///var/log/splunk_real_env/cisco_ips.log]
disabled = false
sourcetype = cisco:firewall
index = network
```

Rodar em background:


```python
nohup python3 /var/log/splunk_real_env/sql_injection_simulation.py > /dev/null 2>&1 &
```

Depois de rodar o script com nohup, você pode verificar se o script está sendo executado em segundo plano com o comando:


```python
ps aux | grep sql_injection_simulation.py
```

# Troubleshooting

Verificar o processo exato:


```python
pgrep -fl sql_injection_simulation.py
```

Se não houver saída, o script não está rodando.


```python
Caso o script tenha parado e você queira rodá-lo novamente:
```


```python
sudo nohup python3 /var/log/splunk_real_env/sql_injection_simulation.py > /dev/null 2>&1 &
```

Para confirmar que ele está rodando, use:


```python
sudo pgrep -fl sql_injection_simulation.py
```

# Lista Monitor


```python
/opt/splunk/bin/splunk list monitor
```

# 🛠 1️⃣ Verifique permissões da pasta

O Splunk pode não ter permissão para escrever na pasta /var/log/splunk_real_env. Verifique com:


```python
ls -ld /var/log/splunk_real_env
```

Se a saída for algo como:


```python
drwxr-xr-x 2 root root 4096 Mar 13 13:10 /var/log/splunk_real_env
```

Isso significa que somente o root pode escrever. Para corrigir, execute:


```python
sudo chmod 777 /var/log/splunk_real_env
```

Isso dará permissão total (teste isso, depois podemos ajustar as permissões corretamente).

Recursivo:


```python
sudo chmod -R 777 /var/log/splunk_real_env
```

Rodar o script novamente:


```python
nohup python3 /var/log/splunk_real_env/sql_injection_simulation.py > /dev/null 2>&1 &
```

Verificar se foi criado:


```python
ls -l /var/log/splunk_real_env/cisco_ips.log
```

📁 2️⃣ Veja se o arquivo está sendo criado


```python
ls -l /var/log/splunk_real_env/cisco_ips.log
```

Verificar se o script sql esta rodando:


```python
pgrep -fl sql_injection_simulation.py
```

Verificar se o script firewall esta rodando:


```python
pgrep -fl generate_cisco_asa_logs.py
```

Rodar os dois scripts novamente:


```python
sudo nohup python3 /var/log/splunk_real_env/generate_cisco_asa_logs.py > /dev/null 2>&1 &
sudo nohup python3 /var/log/splunk_real_env/sql_injection_simulation.py > /dev/null 2>&1 &
```

# Como ativar uma regra de correlação?




## Conclusion

The procedure described here enables efficient installation and configuration of **Splunk Enterprise Security 8.0.2**, following structured best practices.

Feel free to adapt the process according to your specific environment needs or future Splunk versions.

## Final Notes

- This procedure was initially designed on **Google Colab** to facilitate quick executions and controlled testing.
- It is highly recommended to always check the official **Splunk Release Notes** for updates and adjustments.
- For contributions or improvements, feel free to submit Pull Requests to this repository.

---

**License:**  
MIT License

