from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Task(db.Model):
    """Modelo de dados para tarefas"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    category = db.Column(db.String(50), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    estimated_time = db.Column(db.Integer, nullable=True)  # em minutos
    tags = db.Column(db.String(200), nullable=True)  # armazenado como string JSON
    
    def __init__(self, title, description=None, priority='medium', category=None, 
                 due_date=None, estimated_time=None, tags=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.category = category
        self.due_date = due_date
        self.estimated_time = estimated_time
        self.tags = json.dumps(tags) if tags else None
    
    def to_dict(self):
        """Converte o objeto Task para dicionário"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'category': self.category,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'estimated_time': self.estimated_time,
            'tags': json.loads(self.tags) if self.tags else []
        }
    
    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'


class ProductivityStats(db.Model):
    """Modelo para estatísticas de produtividade"""
    __tablename__ = 'productivity_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow().date, unique=True)
    tasks_completed = db.Column(db.Integer, default=0)
    tasks_created = db.Column(db.Integer, default=0)
    total_time_spent = db.Column(db.Integer, default=0)  # em minutos
    focus_score = db.Column(db.Float, default=0.0)  # 0-100
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'tasks_completed': self.tasks_completed,
            'tasks_created': self.tasks_created,
            'total_time_spent': self.total_time_spent,
            'focus_score': self.focus_score
        }
    
    def __repr__(self):
        return f'<ProductivityStats {self.date}>'
