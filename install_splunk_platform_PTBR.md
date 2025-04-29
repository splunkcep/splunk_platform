# Splunk Enterprise Security 8.0.2 Setup Guide

Este projeto documenta o passo a passo do procedimento realizado originalmente em um ambiente Google Colab, adaptado agora em formato Markdown para projetos profissionais.

O objetivo é tornar o conteúdo claro, organizado e reutilizável por qualquer analista ou arquiteto Splunk que deseje instalar ou configurar o **Splunk ES 8.0.2**.

---

## Índice

- [Introdução](#introdução)
- [Pré-requisitos](#pré-requisitos)
- [Procedimento Detalhado](#procedimento-detalhado)
- [Conclusão](#conclusão)
- [Notas Finais](#notas-finais)

---

## Introdução

Este documento foi baseado em um notebook prático criado para facilitar a instalação e configuração do Splunk Enterprise Security 8.0.2 em ambientes controlados.

## Pré-requisitos

Antes de começar, verifique se você possui:

- Acesso a um ambiente Splunk Enterprise instalado (versão compatível com o ES 8.0.2).
- Licença válida do Splunk ES.
- Permissões administrativas no Splunk.
- Conectividade adequada entre os componentes Splunk.
- Google Colab (originalmente utilizado) ou ambiente equivalente para execuções Python (opcional).

## Procedimento Detalhado

# Regras de Firewall

---

## Prerequisites

Ensure `iptables` is installed and you have **root privileges** to run the commands below.

---

## 1. Add Firewall Rules

```bash
# Allow Splunk Web Interface
sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT

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

## Integração de Logs do Cisco ASA e Carbon Black EDR no Splunk ES 8

💾 2. Salvar as regras para persistência após reboot

Para sistemas baseados em Debian/Ubuntu:


```python
sudo iptables-save | sudo tee /etc/iptables.rules
```

🔄 3. Aplicar as regras após reinicialização

Para garantir que as regras sejam aplicadas no boot:


```python
sudo bash -c "echo -e '#!/bin/sh\n/sbin/iptables-restore < /etc/iptables.rules' > /etc/network/if-pre-up.d/iptables"
```


```python
sudo chmod +x /etc/network/if-pre-up.d/iptables
```

✅ 4. Verificar se as regras foram aplicadas


```python
sudo iptables -L -n
```

Isso listará todas as regras configuradas no iptables, incluindo as portas recém-adicionadas.

# Desativando Transparent Huge Pages (THP) antes de instalar o Splunk Enterprise Trial

O Transparent Huge Pages (THP) pode impactar negativamente o desempenho do Splunk. Portanto, a Splunk recomenda que essa configuração seja desativada antes da instalação.

1️⃣ Verificar o status atual do THP

Antes de fazer qualquer alteração, verifique se o THP está ativado no sistema:


```python
cat /sys/kernel/mm/transparent_hugepage/enabled
```

Se a saída indicar [always] ou [madvise], significa que o THP está ativado e precisa ser desativado.

2️⃣ Editar o arquivo de configuração do GRUB

Abra o arquivo de configuração do GRUB com o editor vi (ou outro de sua preferência):


```python
sudo vi /etc/default/grub
```

Localize a linha que começa com GRUB_CMDLINE_LINUX e adicione transparent_hugepage=never no final da linha, dentro das aspas.

Exemplo:


```python
GRUB_CMDLINE_LINUX="rhgb quiet transparent_hugepage=never"
```

Salve e saia do editor (ESC → :wq → Enter).

3️⃣ Atualizar o GRUB

Após editar o arquivo, gere uma nova configuração do GRUB com o seguinte comando:


```python
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

4️⃣ Reiniciar o sistema

Agora, reinicie o servidor para aplicar as alterações:


```python
sudo reboot
```

5️⃣ Verificar se o THP foi desativado

Após o reboot, confirme se o THP está desativado:


```python
cat /sys/kernel/mm/transparent_hugepage/enabled
```

A saída deve mostrar ”[never]”, indicando que o THP foi desativado com sucesso.

🔗 Documentação Oficial

Para mais informações, consulte a documentação oficial da Splunk:
🔗 Splunk and THP - Transparent Huge Pages

# 📌 Passo a Passo: Instalação do Splunk Enterprise Trial no Linux

🔹 1️⃣ Acessando o Servidor via SSH

Abra um terminal e conecte-se ao servidor via SSH:

`ssh Nome_Do_Usuario@<IP_DO_SERVIDOR>`

🔹 Substitua:
	•	Nome_Do_Usuario pelo usuário do sistema operacional ou domínio.
	•	<IP_DO_SERVIDOR> pelo IP real do host onde deseja instalar o Splunk.

🔹 2️⃣ Criando um Usuário para o Splunk

Para garantir uma instalação segura, criaremos um usuário dedicado para rodar o Splunk:

🔹 Esse comando:
	•	Cria um usuário chamado splunkuser.


```python
sudo useradd -m -r splunkuser
```

🔹 Esse comando:
	•	Solicita a definição de uma senha para ele.


```python
sudo passwd splunkuser
```

🔑 *Credenciais:
	•	Usuário do SO: splunkuser
	•	Senha do SO: Definida no comando acima*

 🔹 3️⃣ Adicionando o Usuário Splunk ao Grupo Sudo

1️Adicione o splunkuser ao grupo sudo:


```python
sudo usermod -aG sudo splunkuser
```

Verifique se a adição foi bem-sucedida:


```python
groups splunkuser
```

Para mudar para o bash, execute:


```python
sudo chsh -s /bin/bash splunkuser
```

Aplique as mudanças saindo e entrando novamente como splunkuser:


```python
su - splunkuser
```

Onde Estou?


```python
pwd
```

Quem eu sou?


```python
whoami
```

O que tenho?


```python
ls
```

Quais as permissões associadas ao que tenho?


```python
ls -lha
```

🔹 4️⃣ Baixando o Instalador do Splunk

🔹 Esse comando:
	•	Faz o download do Splunk Enterprise versão 9.4.1.
	•	Se quiser outra versão, ajuste o link no wget.


```python
sudo wget -O splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz "https://download.splunk.com/products/splunk/releases/9.4.1/linux/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz"
```

Agora, vá para o diretório de downloads:


```python
cd /home/splunkuser/
```

🔹 5️⃣ Ajustando Permissões no Arquivo de Instalação

Antes de instalar, confira as permissões do arquivo:


```python
ls -lha /home/splunkuser
```

Dê permissão de execução ao arquivo:


```python
sudo chmod +x /home/splunkuser/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz
```

Verifique novamente as permissões:


```python
ls -lha /home/splunkuser
```

🔹 6️⃣ Criando o Diretório de Instalação do Splunk


```python
sudo mkdir /opt/splunk
```

Agora, altere o dono da pasta para o usuário splunkuser:

sudo chown -R splunkuser:splunkuser /opt/splunk


```python
sudo chown -R splunkuser:splunkuser /opt/splunk
```

Verifique se as permissões estão corretas:


```python
ls -lha /opt/splunk
```

🔹 7️⃣ Instalando o Splunk

Extraia o arquivo baixado para /opt
(📌 Isso instalará o Splunk na pasta /opt/splunk.):


```python
tar -xzvf splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz -C /opt
```

🔹 8️⃣ Iniciando o Splunk

Agora, inicie o Splunk e aceite a licença:


```python
/opt/splunk/bin/splunk start --accept-license
```

🔑
* Credenciais Padrão do Splunk:
*	Usuário do SO: splunkuser
*	Senha do SO: (definida anteriormente)
*	Usuário do Splunk: admin
*	Senha do Splunk: splunkuser

🔹 9️⃣ Configurando o Splunk para Iniciar Automaticamente

Para garantir que o Splunk inicie automaticamente ao reiniciar o servidor:


```python
sudo /opt/splunk/bin/splunk enable boot-start -user splunkuser --accept-license --answer-yes --no-prompt
```

Isso configura o serviço do Splunk para iniciar automaticamente com o sistema.

Verifique o arquivo de inicialização:


```python
sudo vi /etc/init.d/splunk
```

Adicione as seguintes linhas (se necessário):


```python
RETVAL=0
USER=splunkuser
. /etc/init.d/functions
```

🔹 🔄 Comandos Básicos para Gerenciar o Splunk

Verificar status


```python
/opt/splunk/bin/splunk status
```

Iniciar o Splunk


```python
/opt/splunk/bin/splunk start
```

Parar o Splunk


```python
/opt/splunk/bin/splunk stop
```

Reiniciar o Splunk


```python
/opt/splunk/bin/splunk restart
```

Agora o Splunk está instalado e configurado no seu servidor Linux. Para acessá-lo via navegador, abra:


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




## Conclusão

O procedimento descrito aqui permite a instalação e configuração eficiente do **Splunk Enterprise Security 8.0.2** seguindo boas práticas estruturadas.

Adapte o processo conforme necessidades específicas do seu ambiente ou versões futuras do Splunk.

## Notas Finais

- Este procedimento foi inicialmente elaborado em **Google Colab** para facilitar execuções rápidas e testes controlados.
- Recomenda-se sempre consultar as **Release Notes** oficiais da Splunk para ajustes e atualizações futuras.
- Para contribuições ou melhorias, utilize Pull Requests neste repositório.

---

**Autor:**  
Levi Lima Greter

**Contribuidores**


**Licença:**  
MIT License

