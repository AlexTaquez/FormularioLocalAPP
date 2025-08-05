import json
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Formulario, Pregunta, Opcion, UsuarioRespuesta, Respuesta

# Create your views here.



def home(request):
    return render(request, 'formularios/home.html')

def seleccionar_formulario(request):
    formularios = Formulario.objects.all()
    return render(request, 'formularios/seleccionar_formulario.html', {'formularios': formularios})

def responder_formulario(request, formulario_id):
    formulario = get_object_or_404(Formulario, pk=formulario_id)
    preguntas = formulario.preguntas.all().prefetch_related('opciones')
    return render(request, 'formularios/responder_formulario.html', {
        'formulario': formulario,
        'preguntas': preguntas,
    })

def calcular_calificacion(formulario, respuestas):
    preguntas = formulario.preguntas.all()
    puntaje_max = sum([max([op.puntuacion for op in p.opciones.all()]) for p in preguntas])
    puntaje_usuario = 0
    for r in respuestas:
        pregunta = preguntas.get(id=r['pregunta_id'])
        opcion = pregunta.opciones.get(id=r['opcion_id'])
        puntaje_usuario += opcion.puntuacion
    if puntaje_max == 0:
        return 1.0
    # Calificación proporcional entre 1.0 y 5.0
    calificacion = 1.0 + (puntaje_usuario / puntaje_max) * 4.0
    return round(calificacion, 1)

@csrf_exempt
def guardar_respuesta(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre_completo')
        formulario_id = data.get('formulario_id')
        respuestas = data.get('respuestas', [])
        if not nombre or not formulario_id or not respuestas:
            return JsonResponse({'success': False, 'error': 'Datos incompletos'})
        formulario = Formulario.objects.get(id=formulario_id)
        if UsuarioRespuesta.objects.filter(nombre_completo=nombre, formulario_id=formulario_id).exists():
            return JsonResponse({'success': False, 'error': 'Ya has respondido este formulario'})
        calificacion = calcular_calificacion(formulario, respuestas)
        usuario_respuesta = UsuarioRespuesta.objects.create(
            nombre_completo=nombre,
            formulario_id=formulario_id,
            calificacion=calificacion
        )
        for r in respuestas:
            Respuesta.objects.create(
                usuario_respuesta=usuario_respuesta,
                pregunta_id=r['pregunta_id'],
                opcion_seleccionada_id=r['opcion_id']
            )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@staff_member_required
def resultados_formularios(request):
    formularios = Formulario.objects.all()
    resultados = []
    for formulario in formularios:
        usuarios = UsuarioRespuesta.objects.filter(formulario=formulario)
        usuarios_resultados = []
        for usuario in usuarios:
            respuestas = Respuesta.objects.filter(usuario_respuesta=usuario)
            puntaje_total = sum([r.opcion_seleccionada.puntuacion for r in respuestas])
            usuarios_resultados.append({
                'nombre': usuario.nombre_completo,
                'puntaje': puntaje_total,
                'fecha': usuario.fecha_respuesta,
                'calificacion': usuario.calificacion,
            })
        resultados.append({
            'formulario': formulario,
            'usuarios': usuarios_resultados,
        })
    return render(request, 'formularios/resultados_formularios.html', {'resultados': resultados})