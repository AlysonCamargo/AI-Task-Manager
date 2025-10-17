from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import db, Task, ProductivityStats
from datetime import datetime, timedelta
import os
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'seu-secret-key-super-seguro-aqui'

# Inicializar extensões
db.init_app(app)
CORS(app)

# Criar tabelas
with app.app_context():
    db.create_all()


# ===================== ROTAS DE VISUALIZAÇÃO =====================

@app.route('/')
def index():
    """Página principal da aplicação"""
    return render_template('index.html')


# ===================== API ENDPOINTS - TASKS =====================

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Retorna todas as tarefas com filtros opcionais"""
    status = request.args.get('status')
    priority = request.args.get('priority')
    category = request.args.get('category')
    
    query = Task.query
    
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if category:
        query = query.filter_by(category=category)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'tasks': [task.to_dict() for task in tasks],
        'count': len(tasks)
    })


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Retorna uma tarefa específica"""
    task = Task.query.get_or_404(task_id)
    return jsonify({
        'success': True,
        'task': task.to_dict()
    })


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Cria uma nova tarefa"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'success': False, 'error': 'Title is required'}), 400
    
    # Processar data de vencimento
    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except:
            pass
    
    task = Task(
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        category=data.get('category'),
        due_date=due_date,
        estimated_time=data.get('estimated_time'),
        tags=data.get('tags', [])
    )
    
    db.session.add(task)
    db.session.commit()
    
    # Atualizar estatísticas
    update_daily_stats('created')
    
    return jsonify({
        'success': True,
        'task': task.to_dict(),
        'message': 'Task created successfully'
    }), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Atualiza uma tarefa existente"""
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'priority' in data:
        task.priority = data['priority']
    if 'status' in data:
        old_status = task.status
        task.status = data['status']
        
        # Registrar conclusão
        if old_status != 'completed' and data['status'] == 'completed':
            task.completed_at = datetime.utcnow()
            update_daily_stats('completed', task.estimated_time or 30)
    
    if 'category' in data:
        task.category = data['category']
    if 'due_date' in data:
        try:
            task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except:
            pass
    if 'estimated_time' in data:
        task.estimated_time = data['estimated_time']
    if 'tags' in data:
        task.tags = str(data['tags'])
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'task': task.to_dict(),
        'message': 'Task updated successfully'
    })


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Deleta uma tarefa"""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Task deleted successfully'
    })


# ===================== API ENDPOINTS - STATISTICS =====================

@app.route('/api/stats/overview', methods=['GET'])
def get_stats_overview():
    """Retorna estatísticas gerais"""
    total_tasks = Task.query.count()
    pending_tasks = Task.query.filter_by(status='pending').count()
    in_progress_tasks = Task.query.filter_by(status='in_progress').count()
    completed_tasks = Task.query.filter_by(status='completed').count()
    
    # Tarefas por prioridade
    urgent_tasks = Task.query.filter_by(priority='urgent', status='pending').count()
    high_tasks = Task.query.filter_by(priority='high', status='pending').count()
    
    # Produtividade da semana
    week_ago = datetime.utcnow() - timedelta(days=7)
    completed_this_week = Task.query.filter(
        Task.completed_at >= week_ago,
        Task.status == 'completed'
    ).count()
    
    return jsonify({
        'success': True,
        'stats': {
            'total_tasks': total_tasks,
            'pending': pending_tasks,
            'in_progress': in_progress_tasks,
            'completed': completed_tasks,
            'urgent_pending': urgent_tasks,
            'high_pending': high_tasks,
            'completed_this_week': completed_this_week,
            'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
        }
    })


@app.route('/api/stats/productivity', methods=['GET'])
def get_productivity_stats():
    """Retorna estatísticas de produtividade dos últimos 7 dias"""
    days = int(request.args.get('days', 7))
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    stats = ProductivityStats.query.filter(
        ProductivityStats.date >= start_date
    ).order_by(ProductivityStats.date).all()
    
    return jsonify({
        'success': True,
        'productivity': [stat.to_dict() for stat in stats]
    })


# ===================== API ENDPOINTS - AI FEATURES =====================

@app.route('/api/ai/suggestions', methods=['GET'])
def get_ai_suggestions():
    """Retorna sugestões inteligentes baseadas nas tarefas"""
    pending_tasks = Task.query.filter_by(status='pending').all()
    
    suggestions = []
    
    # Sugestão 1: Tarefas urgentes próximas do prazo
    urgent_tasks = [t for t in pending_tasks if t.priority == 'urgent' and t.due_date]
    if urgent_tasks:
        suggestions.append({
            'type': 'urgent',
            'icon': '⚠️',
            'title': 'Tarefas Urgentes!',
            'message': f'Você tem {len(urgent_tasks)} tarefa(s) urgente(s). Comece por elas!',
            'action': 'filter_urgent'
        })
    
    # Sugestão 2: Tarefas pequenas (quick wins)
    quick_tasks = [t for t in pending_tasks if t.estimated_time and t.estimated_time <= 15]
    if quick_tasks:
        suggestions.append({
            'type': 'quick_win',
            'icon': '⚡',
            'title': 'Quick Wins Disponíveis',
            'message': f'{len(quick_tasks)} tarefa(s) rápida(s) (≤15min). Ganhe momentum!',
            'action': 'show_quick_tasks'
        })
    
    # Sugestão 3: Melhor horário para focar
    current_hour = datetime.now().hour
    if 9 <= current_hour <= 11:
        suggestions.append({
            'type': 'focus_time',
            'icon': '🎯',
            'title': 'Horário Premium de Foco',
            'message': 'Manhã é ideal para tarefas complexas. Aproveite sua energia!',
            'action': 'filter_high_priority'
        })
    
    # Sugestão 4: Organização por categoria
    categories = {}
    for task in pending_tasks:
        if task.category:
            categories[task.category] = categories.get(task.category, 0) + 1
    
    if categories:
        top_category = max(categories, key=categories.get)
        suggestions.append({
            'type': 'category_focus',
            'icon': '📂',
            'title': 'Foco em Categoria',
            'message': f'Você tem {categories[top_category]} tarefas de "{top_category}". Que tal focar nelas?',
            'action': f'filter_category_{top_category}'
        })
    
    # Sugestão 5: Motivacional
    motivational_quotes = [
        "Pequenos passos diários levam a grandes conquistas! 🚀",
        "Cada tarefa concluída é uma vitória. Continue assim! 💪",
        "Organize suas tarefas, organize sua mente! 🧠",
        "Produtividade é escolher o que importa. Você está no caminho certo! ✨"
    ]
    
    suggestions.append({
        'type': 'motivation',
        'icon': '💡',
        'title': 'Dica do Dia',
        'message': random.choice(motivational_quotes),
        'action': None
    })
    
    return jsonify({
        'success': True,
        'suggestions': suggestions
    })


@app.route('/api/ai/smart-sort', methods=['POST'])
def smart_sort_tasks():
    """Ordena tarefas inteligentemente baseado em múltiplos fatores"""
    data = request.get_json()
    tasks = Task.query.filter_by(status='pending').all()
    
    # Sistema de pontuação inteligente
    def calculate_priority_score(task):
        score = 0
        
        # Prioridade base
        priority_scores = {'urgent': 100, 'high': 75, 'medium': 50, 'low': 25}
        score += priority_scores.get(task.priority, 50)
        
        # Proximidade do prazo
        if task.due_date:
            days_until_due = (task.due_date - datetime.utcnow()).days
            if days_until_due < 0:
                score += 150  # Atrasada
            elif days_until_due == 0:
                score += 120  # Hoje
            elif days_until_due == 1:
                score += 90  # Amanhã
            elif days_until_due <= 3:
                score += 60  # Esta semana
        
        # Tempo estimado (quick wins)
        if task.estimated_time:
            if task.estimated_time <= 15:
                score += 30  # Tarefas rápidas ganham boost
        
        return score
    
    # Ordenar tarefas
    sorted_tasks = sorted(tasks, key=calculate_priority_score, reverse=True)
    
    return jsonify({
        'success': True,
        'sorted_tasks': [task.to_dict() for task in sorted_tasks],
        'message': 'Tasks sorted by AI priority algorithm'
    })


# ===================== FUNÇÕES AUXILIARES =====================

def update_daily_stats(action, time_spent=0):
    """Atualiza estatísticas diárias"""
    today = datetime.utcnow().date()
    stats = ProductivityStats.query.filter_by(date=today).first()
    
    if not stats:
        stats = ProductivityStats(date=today)
        db.session.add(stats)
    
    if action == 'created':
        stats.tasks_created += 1
    elif action == 'completed':
        stats.tasks_completed += 1
        stats.total_time_spent += time_spent
        
        # Calcular focus score baseado em conclusões
        if stats.tasks_created > 0:
            stats.focus_score = min(100, (stats.tasks_completed / stats.tasks_created) * 100)
    
    db.session.commit()


# ===================== ERROR HANDLERS =====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


# ===================== EXECUTAR APLICAÇÃO =====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
