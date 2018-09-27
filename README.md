# Sistema de Gestión de Medicamentos, Dosis e Inventario

Se presenta el desarrollo de un sistema para la gestión de medicamentos, dosis e inventario en una clínica de reproducción asistida.
Desarrollado con el ERP Odoo v10, el sistema permite interactuar a tres roles, jefe de farmacia, doctor y distribuidor. Cada uno de ellos tendrá acceso a sus propias funcionalidades; el jefe de farmacia se encargará de registrar fármacos, el doctor de registrar sus visitas y dosis para sus pacientes y el distribuidor de realizar un estudio de los datos recopilados por el sistema para mejorar la distribución.

[VIDEO DEMO](https://www.youtube.com/watch?v=UZxARPCNeD8)

Especifición de roles:

### Jefe de farmacia puede:

- Acceder al sistema de medicamentos, donde se le presenta un formulario para registrar nuevos fármacos en la base de datos y un listado completo de ellos con información concreta de cada uno.

### Doctor puede:

- Acceder al sistema de medicamentos, donde se le presenta un listado completo de  ellos con información concreta de cada uno, así como algunas estadísticas particulares.
- Acceder al sistema de pacientes, donde se le presenta un listado con todos ellos así como sus relaciones a patologías, visitas, dosis.
- Acceder al sistema de alertas, donde tiene la posibilidad de notificar a sus pacientes que tengan dosis a punto de caducar.

### Distribuidor puede:

- Acceder al sistema de medicamentos, donde se le presenta un listado de medicamentos con la eficacia registrada por el doctor anteriormente en cada uno de ellos
- Acceder al sistema estadístico, donde se presentan diferentes informes y gráficos para que el proveedor farmacéutico tenga la posibilidad de realizar un estudio.

### Administrador del sistema puede:

- Acceder a todos los sistemas.
