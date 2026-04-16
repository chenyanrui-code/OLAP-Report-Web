from app import db
from datetime import datetime

class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    layout = db.Column(db.Text, nullable=False)  # JSON格式存储布局信息
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    charts = db.relationship('Chart', backref='dashboard', lazy=True)
    
    def __repr__(self):
        return f"<Dashboard {self.name}>"
