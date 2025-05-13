# Preparación del Firewall

## Verifique el estado del firewall, utilice el comando correspondiente según el tipo de SO usado. El orden de los SOs es el siguiente: Fedora, CentOS y CentOS/RHEL 6 and earlier:
### Compruebe que el servicio firewall está en ejecución.

### Fedora: ```bash sudo firewall-cmd --state ```
### CentOS: ```bash systemctl status firewalld ```
### CentOS/RHEL 6 and earlier: ```bash sudo iptables -L ```

## Agregación adicional del puerto TCP:
### Utilice el comando firewall-cmd para agregar la excepeción del puerto TCP.

```bash
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --permanent --add-port=8088/tcp
sudo firewall-cmd --permanent --add-port=8089/tcp
```
## Recargar el firewall:
### Después de agregar la excepción del puerto, vuelva a cargar el firewall para aplicar los cambios.

```bash
sudo firewall-cmd --reload
```

## Verificación de la excepción:
### Para verificar que se ha agregado el puerto, enumere todos los puertos abiertos.

```bash
sudo firewall-cmd --list-ports
```
