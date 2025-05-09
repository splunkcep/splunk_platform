# Guía de configuración de Splunk Enterprise

---

## Tabla de Contenidos

- [Introducción](#Introducción)
- [Pre-requisitos](#pre-requisitos)
- [Proceso Detallado](#Proceso-Detallado)
- [Conclusión](#conclusion)
- [Notas Finales](#final-notes)
  
---

## Introducción

Esta guía proporciona un procedimiento detallado para instalar y configurar Splunk Enterprise. Dirigida a ingenieros tecnológicos, facilita el aprovechamiento de los datos de las máquinas. Aprenda a transformar sus datos en inteligencia operativa.

## Pre-requisitos

Antes de comenzar, asegúrese de contar con:
* Un sistema operativo compatible instalado. Consulte [aquí](https://docs.splunk.com/Documentation/Splunk/9.4.1/Installation/Systemrequirements) la lista de sistemas operativos compatibles.
* Una licencia válida de Splunk Enterprise.
* Permisos de root en el sistema operativo.
* Su sistema operativo debe tener una conexión a internet adecuada.
* Entorno de ejecución de Python.
* Todos los puertos necesarios están abiertos. Consulte el archivo [Preparación del firewall](https://github.com/splunkcep/splunk_platform/blob/main/OS_preparation/FirewallPrep_EN.md) para ver las instrucciones paso a paso para preparar el firewall de su sistema operativo para la instalación de Splunk Enterprise.
* Las páginas transparentes de Hughe (THP) están deshabilitadas en el sistema operativo. Consulta el archivo [Deshabilitar THP](https://github.com/splunkcep/splunk_platform/blob/main/OS_preparation/Disable_THP_EN.md) para ver instrucciones paso a paso sobre cómo deshabilitar THP.


## Proceso Detallado
### Instalación de Splunk Enterprise en Linux 

### 1. Acceso al servidor por SSH

Abra una terminal y conéctese al servidor por SSH:

`ssh User_Name@<Server_IP>`

* Reemplace:
  * User_Name por el usuario del sistema operativo o del dominio.
  * <SERVER_IP> con la IP real del host donde desea instalar Splunk.

### 2. Creación de un usuario para Splunk

Para garantizar una instalación segura, crearemos un usuario dedicado para ejecutar Splunk:

```bash
# Vamos a crear un usuario llamado splunkuser.
sudo useradd -m -r splunkuser

# Ahora, debemos definir una contraseña para él:
sudo passwd splunkuser
```


### 3. Añadir el usuario de Splunk al grupo Sudo

Añadir splunkuser al grupo Sudo:

```bash
sudo usermod -aG sudo splunkuser

# Verificar que la adición se haya realizado correctamente:
groups splunkuser

# Cambiar a bash
sudo chsh -s /bin/bash splunkuser

#Aplicar los cambios cerrando sesión y volviendo a iniciarla como splunkuser:
su - splunkuser
```

¿Dónde estoy?
```bash
pwd
```

¿Quién soy?
```bash
whoami
```

¿Qué tengo?
```bash
ls
```

¿Qué permisos tengo?
```bash
ls -lha
```

🔹 4️⃣ Descargue del instalador de Splunk

🔹 Este comando:
• Descargue la versión 9.4.1 de Splunk Enterprise.
• Si desea otra versión, modifique el enlace en wget.

```bash
sudo wget -O splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz "https://download.splunk.com/products/splunk/releases/9.4.1/linux/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz"
```

Ahora, vaya a su directorio de descargas:

```bash
cd /home/splunkuser/
```

🔹 5️⃣ Ajustar los permisos del archivo de instalación

Antes de instalar, compruebe los permisos del archivo:
```bash
ls -lha /home/splunkuser
```

Asigne permisos de ejecución al archivo:

```bash
sudo chmod +x /home/splunkuser/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz
```

Verifique nuevamente los permisos:


```bash
ls -lha /home/splunkuser
```

🔹 6️⃣ Creación del directorio de instalación de Splunk


```bash
sudo mkdir /opt/splunk
```

Ahora, cambie el propietario de la carpeta al usuario splunkuser:


```python
sudo chown -R splunkuser:splunkuser /opt/splunk
```

```python
sudo chown -R splunkuser:splunkuser /opt/splunk
```

Compruebe si los permisos son correctos:

```python
ls -lha /opt/splunk
```

🔹 7️⃣ Instalación de Splunk

Extraiga el archivo descargado en /opt
(📌 Esto instalará Splunk en la carpeta /opt/splunk):

```python
tar -xzvf splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz -C /opt
```

🔹 8️⃣ Inicio de Splunk

Ahora, inicie Splunk y acepte la licencia:

```python
/opt/splunk/bin/splunk start --accept-license
```

🔑
* Credenciales predeterminadas de Splunk:
* Usuario del SO: splunkuser
* Contraseña del SO: (definida anteriormente)
* Usuario de Splunk: admin
* Contraseña de Splunk: splunkuser


🔹 9️⃣ Configurar Splunk para que se inicie automáticamente

Para garantizar que Splunk se inicie automáticamente al reiniciar el servidor:

```python
sudo /opt/splunk/bin/splunk enable boot-start -user splunkuser --accept-license --answer-yes --no-prompt
```

Esto configura el servicio Splunk para que se inicie automáticamente al iniciar el sistema.

Verifique el archivo de inicio:

```python
sudo vi /etc/init.d/splunk
```

Agregue las siguientes líneas (si es necesario):

```python
RETVAL=0
USER=splunkuser
. /etc/init.d/functions
```

🔹 🔄 Comandos básicos para administrar Splunk

Comprobar estado

```python
/opt/splunk/bin/splunk status
```

Iniciar Splunk

```python
/opt/splunk/bin/splunk start
```

Detener Splunk

```python
/opt/splunk/bin/splunk stop
```

Reiniciar Splunk

```python
/opt/splunk/bin/splunk restart
```

Splunk ya está instalado y configurado en su servidor Linux. Para acceder a él mediante un navegador web, abra:

```python
http://<IP_DO_SERVIDOR>:8000
```

