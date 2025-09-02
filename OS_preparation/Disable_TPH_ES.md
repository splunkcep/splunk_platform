# Desabilitando Transparent Huge Pages

## Qué son las Transparent Huge Pages (TPH)?
THP es una característica del kernel de Linux diseñada para mejorar el rendimiento de la gestión de memoria utilizando páginas de memoria más grandes (2 MB en lugar de los 4 KB estándar). Si bien esto puede beneficiar a algunas aplicaciones, puede afectar negativamente el rendimiento de aplicaciones que consumen mucha memoria, como Splunk. Esto se debe a que la desfragmentación constante de memoria de THP puede generar un alto uso de CPU y latencia de E/S. Deshabilitar THP es una práctica común y recomendada para las implementaciones de Splunk.

## Cómo deshabilitar las THP?

Puede deshabilitar THP creando un servicio dedicado de systemd que se ejecute al arrancar. Este método se considera más fiable que editar GRUB, ya que es menos probable que sea sobrescrito por actualizaciones del kernel.

1. **Verificar el estado actual de THP**

Primero, verifique si THP está habilitado actualmente en su sistema.

``` 
cat /sys/kernel/mm/transparent_hugepage/enabled
```

Si la salida muestra [always] o [madvise], THP está activo. El objetivo es cambiar esto a [never].

2. **Crear un archivo de servicio de Systemd**

Cree un nuevo archivo de servicio de systemd para deshabilitar THP. Use su editor de texto preferido (como nano o vim).

``` 
sudo vi /etc/systemd/system/disable-thp.service
```

Pegue el siguiente contenido en el archivo: (presione 'i')



```
[Unit]
Description=Disable Transparent Huge Pages (THP)
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c "echo never > /sys/kernel/mm/transparent_hugepage/enabled"
ExecStart=/bin/sh -c "echo never > /sys/kernel/mm/transparent_hugepage/defrag"

[Install]
WantedBy=multi-user.target
``` 

Salva y cierra el archivo. (presione [ESC], ":wq")

3. **Habilitar e iniciar el nuevo servicio**

Ahora, habilite e inicie el servicio para aplicar los cambios inmediatamente y asegurarse de que persistan después de un reinicio.

```
# Recargar systemd para reconocer el nuevo servicio
sudo systemctl daemon-reload

# Habilitar el servicio para que se ejecute al inicio
sudo systemctl enable disable-thp.service

# Iniciar el servicio inmediatamente
sudo systemctl start disable-thp.service
```
