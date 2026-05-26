# GoAway - Gestor de Reservas de Alojamientos de Lujo

GoAway es una plataforma web completa de reserva de alojamientos desarrollada como proyecto de Máster. La aplicación permite a los usuarios buscar propiedades, gestionar reservas mediante un flujo internacionalizado y simular el proceso de pago seguro a través de distintas pasarelas, ofreciendo además un panel de control completo para anfitriones y administradores.

---

## 🛠️ Stack Tecnológico

El proyecto está construido siguiendo estándares de desarrollo profesional, entornos aislados y arquitectura desacoplada para la base de datos:

* **Backend:** Python 3.12 & Django 6.0 (Mapeo ORM, sistema de autenticación nativo y seguridad).
* **Base de Datos:** PostgreSQL (Ejecutado de forma aislada).
* **Frontend:** Tailwind CSS v4 & Django Widget Tweaks (Para un diseño de interfaz fluido y adaptativo).
* **Internacionalización (i18n):** Middleware nativo de Django + Django Rosetta (Soporte completo Español / Inglés).
* **Infraestructura Local:** Docker & Docker Compose (Contenedores para servicios de datos).

---

## 🚀 Arquitectura y Características Clave

1.  **Multi-idioma Nativo (i18n):** Implementación de traducciones dinámicas y estáticas mediante etiquetas `{% translate %}` y `{% blocktranslate %}`, gestionadas de forma fluida desde el panel de Rosetta.
2.  **Modelo de Usuario Personalizado:** Ampliación del modelo `AbstractUser` de Django para gestionar perfiles diferenciados (Inquilinos y Anfitriones).
3.  **Entorno Seguro:** Aislamiento completo de claves secretas y credenciales de infraestructura utilizando variables de entorno (`python-dotenv`).
4.  **Pasarela de Pago Simulada:** Interfaz adaptada con flujos de control para pagos mediante Tarjeta, PayPal y Bizum.

---

## 🔑 Credenciales de Acceso (Para Evaluación / QA)

Para facilitar la auditoría y corrección del proyecto sin necesidad de registrar nuevas cuentas desde cero, se han configurado los siguientes perfiles de prueba:

* **Perfil Administrador (Django Admin):
    usuario: `bx@bx.com`  
    password: adminpass123
    *(Acceso total al panel de control de datos en `/admin`)*


* **Perfil Anfitrión (Host):
    usuario: `host1@host.com`  
    password: hostpass001
    
    *(Permisos para publicar propiedades y gestionar precios. )
* **Perfil Inquilino (Guest):
    usuario: `guest1@guest.com` 
    password: guestpass001
    *(Permisos para buscar alojamientos, interactuar con la pasarela de pago y ver historial de viajes)*

---

## 💻 Instalación y Despliegue Local

Sigue estos pasos para levantar el entorno de desarrollo en tu máquina local (Probado en distribuciones Linux):

### 1. Clonar el repositorio e instalar dependencias
```bash
git clone [https://github.com/tu-usuario/gestor_de_reservas.git](https://github.com/tu-usuario/gestor_de_reservas.git)
cd gestor_de_reservas

# Crear y activar el entorno virtual
python3.12 -m venv venv
source venv/bin/activate

# Instalar el listado de dependencias del entorno de producción
pip install -r requirements.txt

### 📥 Cómo cargar estos usuarios en el entorno:
Si estás desplegando el proyecto en una base de datos limpia, puedes inyectar de golpe toda esta estructura ejecutando el siguiente comando en la terminal con el entorno virtual activo:
```bash
python manage.py loaddata users

## ☁️ Gestión de Archivos Multimedia (Cloudinary)

Para el almacenamiento y renderizado de las imágenes de las propiedades, este proyecto está integrado con **Cloudinary**, un servicio de gestión de medios en la nube. 

Se ha seleccionado esta arquitectura por los siguientes motivos técnicos:
* **Persistencia en Producción:** Evita la pérdida de imágenes al desplegar en servidores o plataformas (como Heroku o Render) cuyos sistemas de archivos son efímeros (se borran en cada reinicio).
* **Rendimiento e Infraestructura:** Las imágenes se sirven optimizadas a través de una red de entrega de contenido (CDN), reduciendo la carga en nuestro servidor Django.
* **Buenas Prácticas de Git:** Al delegar el almacenamiento a Cloudinary, evitamos saturar el repositorio de GitHub con archivos binarios pesados. La carpeta local de medios y el archivo de configuración `.env` se encuentran estrictamente protegidos en el `.gitignore`.

### Configuración requerida
Para que el sistema de carga múltiple funcione localmente, asegúrate de añadir tu credencial en el archivo `.env` en la raíz del proyecto (puedes guiarte con el archivo `.env.example`):

```env
CLOUDINARY_URL=cloudinary://<tu_api_key>:<tu_api_secret>@<tu_cloud_name>