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

Si ve "active (running)", vaya a la sección "[Open necessary ports](#open-necessary-ports)".

Si recibe el mensaje "Status: inactive" o "ufw: command not found", entonces instale y habilite el firewall.

```bash
# Update package lists
sudo apt update

# Firewall Installation (if not already installed)
sudo apt install ufw -y

# Enable firewall service (so it runs on boot)
sudo ufw enable

# Verify firewall is running
sudo ufw status
```

### 2. Abrir los puertos necesarios

Para aprovechar al máximo Splunk, necesitamos abrir los siguientes puertos. Hemos incluido los puertos comunes de Splunk listados en la documentación y en la preparación para otras distribuciones de Linux.

* 8000 TCP - Para permitir la interfaz web de Splunk
* 8089 TCP - Para permitir la interfaz de gestión de Splunk / API REST
* 8443 TCP - Para permitir la interfaz de gestión de Splunk (SSL)
* 9997 TCP - Para permitir la comunicación con Universal Forwarder (Recepción de datos del Indexador)
* 8088 TCP - Para permitir la comunicación con HTTP Event Collector (HEC)
* 8191 TCP - Para permitir KV Store (relevante para entornos en clúster)
* 443 TCP - Para permitir la interfaz web segura (HTTPS) si está configurada, o para conexiones salientes
* 22 TCP - Para permitir SSH (normalmente ya abierto, pero es bueno confirmarlo)

``` bash
# Abrir los puertos necesarios de forma permanente (ufw aplica los cambios inmediatamente)

# Permitir la interfaz web de Splunk (TCP 8000)
sudo ufw allow 8000/tcp

# Permitir la interfaz de gestión de Splunk / API REST (TCP 8089)
sudo ufw allow 8089/tcp

# Permitir la interfaz de gestión de Splunk (SSL) (TCP 8443)
sudo ufw allow 8443/tcp

# Permitir la recepción de datos del indexador (TCP 9997)
sudo ufw allow 9997/tcp

# Permitir la comunicación con HTTP Event Collector (HEC) (TCP 8088)
sudo ufw allow 8088/tcp

# Permitir KV Store (TCP 8191)
sudo ufw allow 8191/tcp

# Permitir la interfaz web segura (HTTPS) (TCP 443) - Opcional, solo necesario si configura Splunk para HTTPS en el puerto 443
sudo ufw allow 443/tcp

# Permitir SSH (TCP 22) - Normalmente ya abierto
sudo ufw allow 22/tcp

```

### 3. Aplicar cambios y verificar

ufw aplica los cambios inmediatamente al ejecutar los comandos ufw allow. Una recarga no es estrictamente necesaria, pero se puede utilizar.

``` bash
# Recargar el cortafuegos (opcional, ya que las reglas se aplican inmediatamente)
sudo ufw reload

# Verificar la configuración (listar puertos y reglas permitidos)
sudo ufw status verbose
```

## Próximos pasos

El siguiente paso recomendado para desplegar Splunk Enterprise es Deshabilitar las Páginas Grandes Transparentes (THP).
Nota: Aunque el documento enlazado es general, los pasos específicos para deshabilitar THP pueden variar ligeramente entre las distribuciones de Linux. Consulta siempre la documentación oficial de Splunk para obtener la guía más precisa para tu versión específica del sistema operativo.


## Referencias

* [Splunk Enterprise Network and Port Requirements](https://docs.splunk.com/Documentation/Splunk/9.4.1/InheritedDeployment/Ports)
