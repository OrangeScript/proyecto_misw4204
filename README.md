# proyecto_misw4204
International FPV Drone Racing League


## Despliegue backend FPV

### Prerequisitos:
- Git instalado
- Docker instalado
- Tener disponibilidad de 3 GB
- Tener un sistema operativo Linux o MAC. En dado caso de tener Windows ejecute en una terminal Linux como WSL. Si no tiene esta terminal, puede seguir las siguientes instrucciones:
    > https://learn.microsoft.com/en-us/windows/wsl/install

### Instrucciones:
1. Clonar el repo proyecto_misw4204 con la instrucción:
    > git clone git@github.com:OrangeScript/proyecto_misw4204.git
3. Cambiar a la rama release:
   > git checkout release
4. Asegurese de tener la última version cargada a git:
   > git pull origin release
7. En un temrinal de Linux o Mac
   > docker-compose up --build
