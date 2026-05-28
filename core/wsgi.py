import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

try:
    from django.core.management import call_command
    print("🤖 INYECTANDO DATOS DEL GESTOR DE RESERVAS EN RENDER...")
    call_command('loaddata', 'datos_gestor_reservas.json')
    print("🎉 ¡ÉXITO! ANFITRIONES, HUÉSPEDES Y RESERVAS CARGADOS.")
except Exception as e:
    import traceback
    print("❌ ERROR EN LA INYECCIÓN:")
    print(traceback.format_exc())
