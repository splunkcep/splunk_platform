# Preparación del Firewall

## Verifique el estado del firewalld:
### Compruebe que el servicio firewalld está en ejecución.

```bash
sudo systemctl status firewalld
```

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
