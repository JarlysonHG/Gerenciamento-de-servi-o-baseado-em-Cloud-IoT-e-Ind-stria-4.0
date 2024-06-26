from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workshop.db'
db = SQLAlchemy(app)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

@app.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([service.to_dict() for service in services])

@app.route('/services', methods=['POST'])
def add_service():
    data = request.get_json()
    new_service = Service(description=data['description'], status=data['status'])
    db.session.add(new_service)
    db.session.commit()
    return jsonify(new_service.to_dict()), 201

@app.route('/services/<int:id>', methods=['PUT'])
def update_service(id):
    service = Service.query.get_or_404(id)
    data = request.get_json()
    service.description = data.get('description', service.description)
    service.status = data.get('status', service.status)
    db.session.commit()
    return jsonify(service.to_dict())

@app.route('/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
