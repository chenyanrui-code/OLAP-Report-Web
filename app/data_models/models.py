from app import db
from datetime import datetime

class DataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data_source_id = db.Column(db.Integer, db.ForeignKey('data_source.id'), nullable=False)
    table_name = db.Column(db.String(100), nullable=False)
    fields = db.Column(db.Text, nullable=False)  # JSON格式存储所选字段
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    charts = db.relationship('Chart', backref='data_model', lazy=True)
    
    def __repr__(self):
        return f"<DataModel {self.name}>"
