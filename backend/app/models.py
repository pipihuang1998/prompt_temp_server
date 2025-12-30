from .extensions import db
from datetime import datetime

class PromptCustomTemplate(db.Model):
    __tablename__ = 'prompt_custom_templates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    temp_description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False) # The template string with placeholders
    parameters_config = db.Column(db.JSON) # List of parameter definitions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'temp_description': self.temp_description,
            'content': self.content,
            'parameters_config': self.parameters_config,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
