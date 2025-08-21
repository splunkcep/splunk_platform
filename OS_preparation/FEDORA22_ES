Preparando Fedora 22 para la Instalación de Splunk Enterprise
Este proyecto documenta el procedimiento paso a paso para preparar un sistema operativo Fedora 22 para alojar Splunk Enterprise.

Tabla de Contenido
Introducción

Requisitos Previos

Preparación del Firewall

Próximos Pasos

Introducción
Este proyecto documenta el procedimiento paso a paso para preparar un sistema operativo Fedora 22 para alojar Splunk Enterprise.

Requisitos Previos
Antes de comenzar, asegúrate de que:

Ya tienes instalado el sistema operativo Fedora 22.

El servidor tiene conectividad a internet.

Tienes privilegios de Root para ejecutar los comandos.

Preparación del Firewall
Fedora típicamente usa firewalld para la gestión del firewall. Nos aseguraremos de que el servicio esté instalado y configuraremos los puertos necesarios.

1. Validación / Instalación del Firewall
Primero, verifica el estado del servicio firewalld.

# Verificar estado del servicio firewalld
sudo systemctl status firewalld



Si ves "active (running)", ve a la sección "Abrir los puertos necesarios".

Si recibes el mensaje "Unit firewalld.service could not be found", entonces instala el firewall.

# Instalación del Firewall (si no está instalado)
sudo dnf install firewalld -y # Añadido -y para confirmar la instalación automáticamente

# Iniciar y habilitar el servicio firewall (para que inicie en el arranque)
sudo systemctl enable firewalld --now

# Verificar que el servicio firewall está corriendo
sudo systemctl status firewalld



2. Abrir los puertos necesarios
Para aprovechar al máximo Splunk, necesitamos abrir los siguientes puertos. Hemos incluido los puertos comunes de Splunk listados en la documentación y en la preparación para CentOS 7.

8000 TCP - Para permitir la Interfaz Web de Splunk

8089 TCP - Para permitir la Interfaz de Gestión de Splunk / API REST

8443 TCP - Para permitir la Interfaz de Gestión de Splunk (SSL)

9997 TCP - Para permitir la comunicación con Universal Forwarder (Recepción de datos del Indexer)

8088 TCP - Para permitir la comunicación con HTTP Event Collector (HEC)

8191 TCP - Para permitir KV Store (relevante para entornos clusterizados)

443 TCP - Para permitir la Interfaz Web Segura (HTTPS) si está configurada, o para conexiones de salida

22 TCP - Para permitir SSH (usualmente ya abierto, pero bueno confirmarlo)

# Abrir los puertos necesarios permanentemente

# Permitir Interfaz Web de Splunk (TCP 8000)
sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent

# Permitir Interfaz de Gestión / API REST de Splunk (TCP 8089)
sudo firewall-cmd --zone=public --add-port=8089/tcp --permanent

# Permitir Interfaz de Gestión de Splunk (SSL) (TCP 8443)
sudo firewall-cmd --zone=public --add-port=8443/tcp --permanent

# Permitir Recepción de Datos del Indexer (TCP 9997)
sudo firewall-cmd --zone=public --add-port=9997/tcp --permanent

# Permitir HTTP Event Collector (HEC) (TCP 8088)
sudo firewall-cmd --zone=public --add-port=8088/tcp --permanent

# Permitir KV Store (TCP 8191)
sudo firewall-cmd --zone=public --add-port=8191/tcp --permanent

# Permitir Interfaz Web Segura (HTTPS) (TCP 443) - Opcional, solo necesario si configuras Splunk para HTTPS en 443
sudo firewall-cmd --zone=public --add-port=443/tcp --permanent

# Permitir SSH (TCP 22) - Usualmente ya abierto
sudo firewall-cmd --zone=public --add-port=22/tcp --permanent


3. Aplicar cambios y verificar
# Recargar firewall para aplicar las reglas permanentes a la configuración en ejecución
sudo firewall-cmd --reload

# Verificar configuración permanente (listar puertos permitidos)
sudo firewall-cmd --zone=public --list-ports --permanent


Próximos Pasos
El siguiente paso recomendado para instalar Splunk Enterprise es Deshabilitar Transparent Huge Pages (THP)

Referencias
Splunk Enterprise Network and Port Requirements
