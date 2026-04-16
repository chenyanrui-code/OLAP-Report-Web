from app import db
from datetime import datetime

class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 图表类型
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboard.id'), nullable=False)
    data_model_id = db.Column(db.Integer, db.ForeignKey('data_model.id'), nullable=False)
    dimensions = db.Column(db.Text, nullable=False)  # JSON格式存储维度
    metrics = db.Column(db.Text, nullable=False)  # JSON格式存储指标
    config = db.Column(db.Text)  # JSON格式存储其他配置
    position_x = db.Column(db.Integer, nullable=False)
    position_y = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Chart {self.name} ({self.type})>"
