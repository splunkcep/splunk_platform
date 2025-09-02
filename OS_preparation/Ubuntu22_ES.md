# Preparación de Ubuntu 22 para la instalación de Splunk Enterprise

Este documento describe el procedimiento paso a paso para preparar un sistema operativo Ubuntu 22 para alojar Splunk Enterprise.

## Tabla de Contenido
- [Introducción](#introducción)
- [Requisitos Previos](#requisitos-previos)
- [Preparación del Firewall](#preparación-del-firewall)
- [Próximos Pasos](#próximos-pasos)

---

## Introducción
Este documento describe el procedimiento paso a paso para preparar un sistema operativo **Ubuntu 22** para alojar **Splunk Enterprise**.

---

## Requisitos Previos
Antes de comenzar, asegúrate de que:

* El sistema operativo **Ubuntu 22** ya está instalado.
* El servidor tiene conectividad a internet. 🌐
* Tienes privilegios de `sudo` para ejecutar los comandos. 🔑

---

## Preparación del Firewall
Ubuntu 22 utiliza comúnmente **Uncomplicated Firewall (ufw)** para la gestión del firewall. Nos aseguraremos de que el servicio esté instalado y configuraremos los puertos necesarios.

### 1. Validación / Instalación del Firewall
Primero, verifica el estado del servicio `ufw`.

```bash
# Verificar el estado del servicio del firewall
sudo ufw status
```

If you see "Status: active", go to the section "Open necessary ports".

If you receive the message "Status: inactive" or "ufw: command not found", then install and enable the firewall.

```bash
Copy Code
# Update package lists
sudo apt update

# Firewall Installation (if not already installed)
sudo apt install ufw -y

# Enable firewall service (so it runs on boot)
sudo ufw enable

# Verify firewall is running
sudo ufw status
```

### 2. Open necessary ports

To make the most of Splunk, we need to open the following ports. We have included common Splunk ports listed in the documentation and in the preparation for other Linux distributions.

* 8000 TCP - To allow Splunk Web Interface
* 8089 TCP - To allow Splunk Management Interface / REST API
* 8443 TCP - To allow Splunk Management Interface (SSL)
* 9997 TCP - To allow communication to Universal Forwarder (Indexer Data Receiving)
* 8088 TCP - To allow communication to HTTP Event Collector (HEC)
* 8191 TCP - To allow KV Store (relevant for clustered environments)
* 443 TCP - To allow Secure Web Interface (HTTPS) if configured, or for outbound connections
* 22 TCP - To allow SSH (usually already open, but good to confirm)

``` bash
# Open necessary ports permanently (ufw applies changes immediately)

# Allow Splunk Web Interface (TCP 8000)
sudo ufw allow 8000/tcp

# Allow Splunk Management Interface / REST API (TCP 8089)
sudo ufw allow 8089/tcp

# Allow Splunk Management Interface (SSL) (TCP 8443)
sudo ufw allow 8443/tcp

# Allow Indexer Data Receiving (TCP 9997)
sudo ufw allow 9997/tcp

# Allow HTTP Event Collector (HEC) (TCP 8088)
sudo ufw allow 8088/tcp

# Allow KV Store (TCP 8191)
sudo ufw allow 8191/tcp

# Allow Secure Web Interface (HTTPS) (TCP 443) - Optional, only needed if you configure Splunk for HTTPS on 443
sudo ufw allow 443/tcp

# Allow SSH (TCP 22) - Usually already open
sudo ufw allow 22/tcp

```

### 3. Apply changes and verify

ufw applies changes immediately upon running the ufw allow commands. A reload is not strictly necessary but can be used.

``` bash
# Reload firewall (optional, as rules are applied immediately)
sudo ufw reload

# Verify configuration (list allowed ports and rules)
sudo ufw status verbose
```
