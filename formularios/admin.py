from django.contrib import admin
from .models import Formulario, Pregunta, Opcion, UsuarioRespuesta, Respuesta

admin.site.register(Formulario)
admin.site.register(Pregunta)
admin.site.register(Opcion)
admin.site.register(UsuarioRespuesta)
admin.site.register(Respuesta)
