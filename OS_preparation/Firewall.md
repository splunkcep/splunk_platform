# Preparación del Firewall

## Verifique el estado del firewall, utilice el comando correspondiente según el tipo de SO usado.
### Compruebe que el servicio firewall está en ejecución.

#### Fedora: 
```bash
sudo firewall-cmd --state
```

#### CentOS: 
```bash
systemctl status firewalld
```

#### CentOS/RHEL 6 and earlier: 
``` bash
sudo iptables -L
```

## ¿Qué sertvicios están corriendo?
### Confirme qué servicios están en ejecución.

#### Fedora: 
```bash
sudo firewall-cmd --list-services
```

#### CentOS: 
```bash
systemctl list-units --type=service --state=running
```

#### CentOS/RHEL 6 and earlier: 
``` bash
service --status-all
```

## Agregación adicional del puerto TCP:
### Utilice el comando firewall-cmd para agregar la excepeción del puerto TCP.

#### Fedora: 
```bash
sudo firewall-cmd --permanent --add-port=8000/tcp
```

#### CentOS: 
```bash
sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent
```

#### CentOS/RHEL 6 and earlier: 
``` bash
sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
sudo service iptables save
sudo iptables-save > /etc/sysconfig/iptables
sudo chkconfig iptables on
sudo iptables -L -n
```

## Recargar el firewall:
### Después de agregar la excepción del puerto, vuelva a cargar el firewall para aplicar los cambios.

#### Fedora: 
```bash
sudo firewall-cmd --reload
```

## Verificación de la excepción:
### Para verificar que se ha agregado el puerto, enumere todos los puertos abiertos.

#### Fedora:
```bash
sudo firewall-cmd --list-ports
```
