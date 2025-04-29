#!/usr/bin/env python3

import os
import subprocess

def check_and_install_firewalld():
    """Verifica se o firewalld está instalado e instala se necessário no Debian."""
    print("Verificando a presença do firewalld...")
    firewalld_check = subprocess.run(["dpkg", "-s", "firewalld"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    if "Status: install ok installed" not in firewalld_check.stdout:
        print("firewalld não encontrado. Instalando via apt...")
        os.system("sudo apt update && sudo apt install -y firewalld")
        os.system("sudo systemctl enable firewalld --now")
        print("firewalld instalado e ativado com sucesso!")
    else:
        print("firewalld já está instalado.")

def configure_firewall():
    """Abre a porta 8000 no firewalld."""
    print("Configurando firewall para abrir a porta 8000...")
    os.system("sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent")
    os.system("sudo firewall-cmd --reload")
    print("Porta 8000 adicionada com sucesso!")

def create_splunk_user():
    """Cria o usuário splunkuser com privilégios de sudo."""
    print("Criando usuário splunkuser...")
    os.system("sudo useradd -m -r splunkuser")
    os.system("echo 'splunkuser:splunkuser' | sudo chpasswd")
    os.system("sudo usermod -aG sudo splunkuser")
    print("Usuário splunkuser criado e adicionado ao grupo sudo.")

def download_splunk():
    """Baixa o pacote do Splunk."""
    print("Baixando Splunk Enterprise...")
    os.system("mkdir -p /home/splunker")
    os.system("wget -O /home/splunker/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz 'https://download.splunk.com/products/splunk/releases/9.4.1/linux/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz'")
    print("Download finalizado!")

def prepare_installation():
    """Cria /opt/splunk com permissões corretas."""
    print("Preparando diretório /opt/splunk...")
    os.system("sudo rm -rf /opt/splunk")
    os.system("sudo mkdir -p /opt/splunk")
    os.system("sudo chown -R splunkuser:splunkuser /opt/splunk")
    os.system("sudo chmod -R 755 /opt/splunk")
    print("Diretório /opt/splunk pronto.")

def install_splunk():
    """Extrai o Splunk no destino correto."""
    print("Extraindo pacote do Splunk...")
    os.system("sudo -u splunkuser tar -xzvf /home/splunker/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz -C /opt")
    print("Splunk instalado em /opt.")

def create_admin_user():
    """Cria o usuário admin via user-seed.conf."""
    print("Criando usuário admin no Splunk...")
    user_seed_path = "/opt/splunk/etc/system/local/user-seed.conf"
    os.system("sudo mkdir -p /opt/splunk/etc/system/local")
    os.system(f"echo '[user_info]' | sudo tee {user_seed_path} > /dev/null")
    os.system(f"echo 'USERNAME = admin' | sudo tee -a {user_seed_path} > /dev/null")
    os.system(f"echo 'PASSWORD = splunkuser' | sudo tee -a {user_seed_path} > /dev/null")
    os.system(f"sudo chown splunkuser:splunkuser {user_seed_path}")
    os.system(f"sudo chmod 600 {user_seed_path}")
    print("Usuário admin configurado com sucesso.")

def start_splunk():
    """Inicia o Splunk e ativa inicialização automática."""
    print("Iniciando Splunk Enterprise...")
    create_admin_user()
    os.system("sudo -u splunkuser /opt/splunk/bin/splunk start --accept-license --answer-yes --no-prompt")
    os.system("sudo /opt/splunk/bin/splunk enable boot-start -user splunkuser --accept-license --answer-yes --no-prompt")
    print("Splunk iniciado e ativado no boot.")

def get_splunk_web_url():
    """Exibe o IP local para acesso via Web."""
    result = subprocess.run(["hostname", "-I"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    ip_address = result.stdout.split()[0] if result.stdout else "[IP_NAO_ENCONTRADO]"
    print("\n\n=== SPLUNK WEB INTERFACE ===")
    print(f"Acesse o Splunk Web copiando e colando:\nhttp://{ip_address}:8000\n")

def main():
    check_and_install_firewalld()
    configure_firewall()
    create_splunk_user()
    download_splunk()
    prepare_installation()
    install_splunk()
    start_splunk()
    get_splunk_web_url()
    print("Instalação do Splunk Enterprise finalizada com sucesso!")

if __name__ == "__main__":
    main()
