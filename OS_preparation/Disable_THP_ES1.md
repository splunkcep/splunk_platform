# Cómo Deshabilitar Transparent Hughe Pages (THP) antes de instalar Splunk Enterprise Trial

Las PTransparent Hughe Pages (THP) pueden impactar negativamente el rendimiento de Splunk. Por lo tanto, Splunk recomienda deshabilitar esta configuración antes de la instalación.

## 1. Verificar el estado actual de THP

Antes de realizar cualquier cambio, asegúrate de que THP esté habilitado en tu sistema. Puedes verificar si THP está habilitado y cómo está configurado revisando el archivo `enabled` en el sistema de archivos `/sys`.

```
cat /sys/kernel/mm/transparent_hugepage/enabled

```

La salida mostrará la configuración actual entre corchetes `[]`.

* `[always] madvise never`: THP está completamente habilitado.

* `always [madvise] never`: THP está habilitado pero solo se usa para regiones de memoria solicitadas explícitamente por las aplicaciones.

* `always madvise [never]`: THP está deshabilitado.

## 2. Editar el archivo de configuración de GRUB

La forma recomendada de deshabilitar THP de forma persistente es agregando un parámetro de arranque del kernel a la configuración de GRUB.
Abre el archivo de configuración de GRUB con vi (u otro editor de tu elección):

1. **Editar el archivo de configuración predeterminado de GRUB:**

   ```
   sudo vi /etc/default/grub
   
   ```

2. **Encontrar la línea `GRUB_CMDLINE_LINUX`:**
   Busca la línea que comienza con `GRUB_CMDLINE_LINUX="...`. Esta línea contiene los parámetros que se pasan al kernel durante el arranque.

3. **Agregar `transparent_hugepage=never` a la línea:**
   Agrega `transparent_hugepage=never` dentro de las comillas dobles de la línea `GRUB_CMDLINE_LINUX`. Asegúrate de dejar un espacio entre los parámetros existentes y el nuevo.

   **Ejemplo (antes):**

   ```
   GRUB_CMDLINE_LINUX="crashkernel=auto rhgb quiet"
   
   ```

   **Ejemplo (después):**

   ```
   GRUB_CMDLINE_LINUX="crashkernel=auto rhgb quiet transparent_hugepage=never"
   
   ```

   (Los parámetros exactos dentro de las comillas pueden variar en tu sistema).

4. **Guardar y cerrar el archivo.**

   Escribe `[esc]` luego `:wq` (para guardar y salir) y luego `[enter]`.

5. **Actualizar la configuración de GRUB:**
   Necesitas regenerar el archivo de configuración de GRUB que el sistema usa realmente para arrancar.

   ```
   sudo grub2-mkconfig -o /boot/grub2/grub.cfg
   
   ```

   *Nota: La ruta del archivo de salida (`-o`) puede variar ligeramente dependiendo de tu distribución específica de Linux y si usas arranque BIOS o UEFI. El comando mostrado es común para CentOS/RHEL 7/8 con arranque BIOS.*

## 4. Reiniciar y Verificar

Después de modificar la configuración de GRUB, debes **reiniciar el sistema** para que el nuevo parámetro del kernel tenga efecto.

```
sudo reboot

```

Una vez que el servidor se haya reiniciado, verifica nuevamente el estado de THP para confirmar que ahora está configurado en `[never]`:

```
cat /sys/kernel/mm/transparent_hugepage/enabled

```

Como resultado deberíamos ver: `always madvise [never]`

Siguiendo estos pasos, habrás deshabilitado Transparent Hughe Pages de forma persistente en tu sistema Linux.

