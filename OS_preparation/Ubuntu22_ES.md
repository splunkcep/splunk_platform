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
