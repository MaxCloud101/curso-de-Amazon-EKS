# 1 Introducción e instalación
## Introducción
Kubernetes es un orquestador de contedores, es decir que te va a permitir crear, administrar, y eliminar contenedores, este fue desarrollado por Google en 2014, luego fue donado y es mantenido por la CNCF (Cloud Native Compute Foundation).

Amazon EKS (Amazon Elastic Kubernetes Service) es un servicio de AWS que te ofrece Kubernetes de forma administrada. Esto te permitira lanzar rapidamente clusters de kubernetes sin la necesidad de instalar componentes en máquinas virtuales como Amazon EC2.

Eksctl es una herramienta de líneas de comando que te va a permitir administrar clústeres de Amazon EKS.

## Requerimientos para este curso

- Conocimientos básicos sobre programación
- Conocimientos básicos sobre Linux
- Conocimientos básicos en AWS
- Conocimientos intermedios en Docker

# Arquitectura de un cluster de kubernetes

Kubernetes está compuesto por un conjunto de recursos de cómputo, memoria ram y disco, en AWS seria utilizar instancias EC2. A este conjunto de instancias lo llamaremos "clúster". En un clúster de kubernetes van a correr diferentes componentes.

A continuación vamos a explicar como es la arquitectura de un clúster de Kubernetes y la función de cada uno de los componentes.

![kubernetes architecture](/img/1-1.imagen.jpg)

En la parte superior de la imagen encontramos el **"Control Plane"**, este es el cerebro del cluster. El Control Plane se encuentra compuesto por:

- **ETCD:** Es una base de datos distribuida clave-valor de código abierta. Se va a encargar de almacenar cualquier configuración lanzada contra el clúster.
- **Scheduler:** Es el encargado de asignar los pods (un pod tiene uno o más contenedores) a los nodos del cluster de manera eficiente.
- **Control Manager:** Se encarga de gestionar los controladores del cluster para mantenerlo en un estado optimo.
- **Cloud Controler Manager:** Se encarga de la integración con componentes específicos de la nube, para gestionar recursos como instancias, balanceadores de carga, almacenamiento y redes.
- **API server:** Es el front-end del control plane. Funciona como una interfaz RESTful para la gestión del cluster. Cualquier carga de trabajo y configuración que quiera lanzarse en el clúster debera ser enviado al el API server.

En la parte inferior de la imagen vamos a encontrar los **"Worker Nodes"**, este conjunto de recursos son conocidos como el **"Data Plane"**. Cada Worker Node está compuesto por:

- **Kube-Proxy:** Se ejecuta en cada Worker Node y se encarga de gestionar las reglas de red para gestionar la comunicación entre los pods y los servicios.
- **Kubelet:** Es un agente que se ejecuta en cada Worker Node. Se encarga de asegurar que se ejecuten correctamente en el nodo los contenedores asignados por el Control Plane. Cada vez que se crea un nodo también se encarga de comunicarle al Control Plane que está listo para ejecutar contenedores.

## Arquitectura de Amazon EKS

Cuando trabajamos en Amazon EKS vamos a conservar la arquitectura mostrada anteriormente. Pero vamos a ver a continuacion como se distribuyen los componentes en la nube.

![Eks architecture](/img/1-2.imagen.jpg)

En  la parte superior de la imagen vamos a encontrar el Control Plane, este se aloja en una VPC administrada por AWS, es decir nosotros no vamos a tener control de los recursos que son usados para correr el control plane.

En la parte inferior de la imagen tenemos el Data Plane, aquí nosotros vamos a lanzar diferentes recursos de cómputo (Amazon EC2, AWS Fargate) donde vamos a poder lanzar nuestros contenedores. Estos recursos serán lanzados sobre una VPC de la cual nosotros si tendremos el control.

Los Worker Nodes se van a agrupar en Node Groups, esto te va a permitir administrar un conjunto de nodos.

En Amazon EKS vamos a  poder lanzar nuestros contenedores sobre los siguientes recursos:

- **Unmanaged Node Groups:** O simplemente llamados "Node Groups" o "Self-Managed Node Groups". Tienes control total sobre las instancias EC2, incluyendo el sistema operativo, la AMI y el software instalado. Esto permite una personalización exhaustiva para cumplir con requisitos específicos o políticas de seguridad.

- **Managed Node Groups:** AWS automatiza gran parte de la gestión del ciclo de vida de los nodos, incluyendo el aprovisionamiento, la aplicación de parches y el escalado. Esto reduce significativamente la sobrecarga operativa y simplifica la gestión de los nodos. (Te recomiendo esta opción, si no deseas correr componentes especiales en tus instancias)

- **AWS Fargate:** Fargate es una capa de cómputo serverless (Aquí no vamos a manejar instancias EC2). Aquí lanzaremos nuestros contenedores en pods directamente asignando los recursos necesarios.

## Herramientas requeridas:

- **Cloudshell:** Este servicio de AWS te proveerá de un shell, mediante el cual vamos a poder interactuar con diferentes herramientas.
- **AWS cli:** Esta herramienta de líneas de comando te permite interactuar directamente con los servicios de AWS (Este viene instalado en Cloudshell) 
- **Kubectl:** Esta herramienta de líneas de comando te va a permitir interactuar con los recursos del cluster de EKS (Este viene instalado en Clodshell)
- **Eksctl:** Esta herramienta de líneas de comando te va a permitir interactuar con los cluster de Kubernetes. (No viene en el Cloudshell, debemos instalar)

# En accion

1.- Vamos a la consola de AWS y en región escogemos us-west-2 (Oregon)

2.- Ingresamos al servicio de AWS CloudShell. 

3.- Ingresamos los siguientes comandos.
```
aws --version
kubectl version
```
![Verificar versiones](/img/1-3.imagen.jpg)

En pantalla se nos mostrara las versiones de las herramientas

4.- Eksctl no viene instalado, asi que debemos instalarlo nostros. Las intrucciones las puedes encontrar aqui (https://eksctl.io/installation/). En cloudshell la carpeta `/usr/local/bin` es efimera, es decir cada vez que se reinicia sesion esta se reinicia, haremos algunos cambios en la ultima linea a la instalacion de la web oficial para no tener este problema.

```
# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH
curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"
# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check
tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz
sudo install -m 0755 /tmp/eksctl /home/cloudshell-user && rm /tmp/eksctl
```

Luego con nano editamos el archivo `~/.bash_profile`.

```
nano ~/.bash_profile.
```

Y agregamos el siguiente comando a la ultima linea del archivo

```
export PATH=/home/cloudshell-user:$PATH
```

![Verificar versiones](/img/1-4.imagen.jpg)

Lanzamos el siguiente comando:

```
source ~/.bash_profile
```

Verificamos que eksctl se haya instalado correctamente

![Verificar versiones](/img/1-5.imagen.jpg)

Ahora tenemos un ambiente listo para trabajar con Amazon EKS mediante eksctl
