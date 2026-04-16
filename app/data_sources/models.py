from app import db
from datetime import datetime

class DataSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # mysql, postgresql, excel
    host = db.Column(db.String(255))
    port = db.Column(db.Integer)
    username = db.Column(db.String(100))
    password = db.Column(db.String(255))  # 加密存储
    database = db.Column(db.String(100))
    file_path = db.Column(db.String(255))  # excel文件路径
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    data_models = db.relationship('DataModel', backref='data_source', lazy=True)
    
    def __repr__(self):
        return f"<DataSource {self.name} ({self.type})>"
