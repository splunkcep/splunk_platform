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
