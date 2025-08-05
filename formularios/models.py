from django.db import models

# Create your models here.

class Formulario(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    formulario = models.ForeignKey(Formulario, related_name='preguntas', on_delete=models.CASCADE)
    texto = models.TextField()
    imagen = models.ImageField(upload_to='preguntas/', blank=True, null=True)

    def __str__(self):
        return self.texto

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    puntuacion = models.IntegerField()

    def __str__(self):
        return self.texto

class UsuarioRespuesta(models.Model):
    nombre_completo = models.CharField(max_length=255)
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    calificacion = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)  # Ajuste: decimal

    class Meta:
        unique_together = ('nombre_completo', 'formulario')

    def __str__(self):
        return f"{self.nombre_completo} - {self.formulario.nombre}"

class Respuesta(models.Model):
    usuario_respuesta = models.ForeignKey(UsuarioRespuesta, related_name='respuestas', on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario_respuesta.nombre_completo} - {self.pregunta.texto} - {self.opcion_seleccionada.texto}"
