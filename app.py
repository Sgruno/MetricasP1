from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.MetricasDB
coleccion = db.tareas

@app.route('/')
def index():
    backlog = list(coleccion.find({"estado": "Backlog"}))
    doing = list(coleccion.find({"estado": "Doing"}))
    done = list(coleccion.find({"estado": "Done"}))
    return render_template('index.html', backlog=backlog, doing=doing, done=done)

@app.route('/add_task', methods=['POST'])
def add_task():
    titulo = request.form.get('titulo')
    
    try:
        story_points = int(request.form.get('story_points'))
    except (ValueError, TypeError):
        story_points = 0
        
    try:
        lineas_agregadas = int(request.form.get('lineas_agregadas'))
    except (ValueError, TypeError):
        lineas_agregadas = 0
        
    try:
        lineas_eliminadas = int(request.form.get('lineas_eliminadas'))
    except (ValueError, TypeError):
        lineas_eliminadas = 0
    
    fecha_creacion_str = request.form.get('fecha_creacion')
    fecha_inicio_str = request.form.get('fecha_inicio')
    fecha_entrega_str = request.form.get('fecha_entrega')

    fechas = {}
    if fecha_creacion_str:
        fechas['creacion'] = datetime.strptime(fecha_creacion_str, '%Y-%m-%d')
    else:
        fechas['creacion'] = datetime.utcnow()
        
    if fecha_inicio_str:
        fechas['inicio'] = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        
    if fecha_entrega_str:
        fechas['entrega'] = datetime.strptime(fecha_entrega_str, '%Y-%m-%d')

    nueva_tarea = {
        "titulo": titulo,
        "story_points": story_points,
        "estado": "Backlog",
        "fechas": fechas,
        "churn": {"agregadas": lineas_agregadas, "eliminadas": lineas_eliminadas}
    }
    coleccion.insert_one(nueva_tarea)
    return redirect(url_for('index'))

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    tarea_id = data.get('id')
    nuevo_estado = data.get('nuevo_estado')
    ahora = datetime.utcnow()

    update_data = {"$set": {"estado": nuevo_estado}}

    if nuevo_estado == "Doing":
        tarea = coleccion.find_one({"_id": ObjectId(tarea_id)})
        if 'inicio' not in tarea.get('fechas', {}):
            update_data["$set"]["fechas.inicio"] = ahora

    elif nuevo_estado == "Done":
        tarea = coleccion.find_one({"_id": ObjectId(tarea_id)})
        if 'entrega' not in tarea.get('fechas', {}):
            update_data["$set"]["fechas.entrega"] = ahora
        if 'inicio' not in tarea.get('fechas', {}):
            update_data["$set"]["fechas.inicio"] = ahora

    coleccion.update_one({"_id": ObjectId(tarea_id)}, update_data)
    return jsonify({"status": "ok"})

@app.route('/edit_task/<task_id>', methods=['POST'])
def edit_task(task_id):
    titulo = request.form.get('titulo')
    try:
        story_points = int(request.form.get('story_points'))
    except (ValueError, TypeError):
        story_points = 0
    try:
        lineas_agregadas = int(request.form.get('lineas_agregadas'))
    except (ValueError, TypeError):
        lineas_agregadas = 0
    try:
        lineas_eliminadas = int(request.form.get('lineas_eliminadas'))
    except (ValueError, TypeError):
        lineas_eliminadas = 0

    update_data = {
        "titulo": titulo,
        "story_points": story_points,
        "churn.agregadas": lineas_agregadas,
        "churn.eliminadas": lineas_eliminadas
    }

    fecha_creacion_str = request.form.get('fecha_creacion')
    fecha_inicio_str = request.form.get('fecha_inicio')
    fecha_entrega_str = request.form.get('fecha_entrega')

    if fecha_creacion_str:
        update_data["fechas.creacion"] = datetime.strptime(fecha_creacion_str, '%Y-%m-%d')
    if fecha_inicio_str:
        update_data["fechas.inicio"] = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
    if fecha_entrega_str:
        update_data["fechas.entrega"] = datetime.strptime(fecha_entrega_str, '%Y-%m-%d')

    coleccion.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})
    return redirect(url_for('index'))

@app.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    coleccion.delete_one({"_id": ObjectId(task_id)})
    return jsonify({"status": "ok"})

@app.route('/metricas')
def metricas():
    tareas_done = list(coleccion.find({"estado": "Done"}))
    lead_times = []
    cycle_times = []
    task_names = []
    total_agregadas = 0
    total_eliminadas = 0

    for t in tareas_done:
        fechas = t.get('fechas', {})
        nombre_tarea = t.get('titulo', 'Sin título')[:15] + "..." 
        task_names.append(nombre_tarea)
        
        lt = 0
        if 'entrega' in fechas and 'creacion' in fechas:
            lt = (fechas['entrega'] - fechas['creacion']).days
        lead_times.append(lt)
        
        ct = 0
        if 'entrega' in fechas and 'inicio' in fechas:
            ct = (fechas['entrega'] - fechas['inicio']).days
        cycle_times.append(ct)
        
        churn = t.get('churn', {})
        total_agregadas += churn.get('agregadas', 0)
        total_eliminadas += churn.get('eliminadas', 0)

    valid_lead = [x for x in lead_times if x >= 0]
    valid_cycle = [x for x in cycle_times if x >= 0]
    avg_lead = sum(valid_lead) / len(valid_lead) if valid_lead else 0
    avg_cycle = sum(valid_cycle) / len(valid_cycle) if valid_cycle else 0

    pipeline = [{"$group": {"_id": "$estado", "puntos": {"$sum": "$story_points"}}}]
    agregacion = list(coleccion.aggregate(pipeline))
    stats_puntos = {item['_id']: item['puntos'] for item in agregacion}

    return render_template('metricas.html', 
                           avg_lead=round(avg_lead, 1), avg_cycle=round(avg_cycle, 1),
                           stats_puntos=stats_puntos, churn_total=total_agregadas + total_eliminadas,
                           total_agregadas=total_agregadas, total_eliminadas=total_eliminadas,
                           task_names=task_names, lead_times=lead_times, cycle_times=cycle_times)

if __name__ == '__main__':
    app.run(debug=True)