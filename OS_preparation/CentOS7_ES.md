# Preparación de CentOS7 para la Instalación de Splunk Enterprise

Este proyecto documenta el procedimiento paso a paso para preparar un sistema operativo CentOS7 para la instalación de Splunk Enterprise.

## Tabla de Contenido

* [Introducción](#introduccion)

* [Prerequisitos](#prerequisitos)

* [Preparación del Firewall](#preparacion-del-firewall)

* [Próximos Pasos](#proximos-pasos)

---

## Introducción

Este proyecto documenta el procedimiento paso a paso para preparar un sistema operativo CentOS7 para instalar Splunk Enterprise.

## Prerequisitos

Antes de comenzar, asegúrate de que:

* Ya tienes instalado el sistema operativo CentOS7.

* El servidor tiene conectividad a internet.

* Tienes privilegios de Root para ejecutar los comandos.

## Preparación del Firewall

CentOS 7 típicamente usa `iptables` para la gestión del firewall. Nos aseguraremos de que el paquete `iptables-services` esté instalado y configuraremos los puertos necesarios.

### 1. Validación / Instalación del Firewall

Primero, verifica el estado del servicio `iptables`.

```bash
# Verificar estado del servicio iptables
sudo systemctl status iptables
```

Si ves "active (exited)" o "active (running)", es probable que el servicio esté instalado. Si recibes un mensaje indicando que el servicio no se encuentra o está inactivo, puede que necesites instalar y habilitar el paquete `iptables-services`.

```bash
# Instalar iptables-services (si no está instalado)
sudo yum install -y iptables-services

# Habilitar el servicio iptables para iniciar en el arranque
sudo systemctl enable iptables

# Iniciar el servicio iptables ahora
sudo systemctl start iptables

# Verificar que el servicio iptables está corriendo
sudo systemctl status iptables
```

### 2. Abrir los puertos necesarios

Añadiremos reglas de `iptables` para abrir los puertos necesarios para Splunk. Estas reglas se insertarán al principio de la cadena `INPUT`.

Basado en los puertos comunes de Splunk (como se ve en el documento "Puertos por Defecto Comunes de Splunk Enterprise"):

* 8000 TCP - Para permitir la Interfaz Web de Splunk

* 8089 TCP - Para permitir la Interfaz de Gestión de Splunk / API REST

* 8443 TCP - Para permitir la Interfaz de Gestión de Splunk (SSL)

* 9997 TCP - Para permitir la comunicación con Universal Forwarder

* 8088 TCP - Para permitir la comunicación con HTTP Event Collector (HEC)

* 8191 TCP - Para permitir KV Store (relevante para entornos clusterizados)

* 443 TCP - Para permitir la Interfaz Web Segura (HTTPS) si está configurada, o para conexiones de salida

* 22 TCP - Para permitir SSH (usualmente ya abierto, pero bueno confirmarlo)

```bash
# Abrir los puertos necesarios usando iptables

# Permitir Interfaz Web de Splunk (TCP 8000)
sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT

# Permitir Interfaz de Gestión / API REST de Splunk (TCP 8089)
sudo iptables -I INPUT -p tcp --dport 8089 -j ACCEPT

# Permitir Interfaz de Gestión de Splunk (SSL) (TCP 8443)
sudo iptables -I INPUT -p tcp --dport 8443 -j ACCEPT

# Permitir Recepción de Datos del Indexer (TCP 9997)
sudo iptables -I INPUT -p tcp --dport 9997 -j ACCEPT

# Permitir HTTP Event Collector (HEC) (TCP 8088)
sudo iptables -I INPUT -p tcp --dport 8088 -j ACCEPT

# Permitir KV Store (TCP 8191)
sudo iptables -I INPUT -p tcp --dport 8191 -j ACCEPT

# Permitir Interfaz Web Segura (HTTPS) (TCP 443)
sudo iptables -I INPUT -p tcp --dport 443 -j ACCEPT

# Permitir SSH (TCP 22) - Usualmente ya abierto
sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT
```

### 3. Guardar las reglas para persistencia y verificar

Para asegurar que estas reglas de `iptables` persistan después de un reinicio, necesitas guardar las reglas actuales. El paquete `iptables-services` se encarga de cargar estas reglas guardadas automáticamente en el arranque si el servicio está habilitado.

```bash
# Guardar las reglas actuales de iptables en el archivo por defecto
sudo service iptables save

# Verificar que las reglas fueron guardadas (opcional)
# cat /etc/sysconfig/iptables

# Verificar que las reglas están activas actualmente
sudo iptables -nvL
```

## Próximos Pasos

El siguiente paso recomendado para instalar Splunk Enterprise es [Deshabilitar Transparent Huge Pages (THP)](https://github.com/splunkcep/splunk_platform/blob/main/OS_preparation/Disable_THP_ES.md)

## Referencias

- [Splunk Enterprise Network and Port Requirements](https://docs.splunk.com/Documentation/Splunk/9.4.1/InheritedDeployment/Ports)
- [iptables Documentation](https://linux.die.net/man/8/iptables)
