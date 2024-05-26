
from datetime import datetime
from app.extension import db


class TrafficViolation(db.Model):
    __tablename__ = 'traffic_violations'

    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    camera_id = db.Column(db.String(50), nullable=False)
    violation_type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<TrafficViolation {self.number_plate}>'

    def to_dict(self):
        """Convert the data model instance into a dictionary."""
        return {
            'id': self.id,
            'number_plate': self.number_plate,
            'timestamp': self.timestamp.isoformat(),
            'camera_id': self.camera_id,
            'violation_type': self.violation_type
        }

    @classmethod
    def from_dict(cls, data):
        """Create a data model instance from a dictionary."""
        return cls(
            number_plate=data.get('number_plate'),
            timestamp=data.get('timestamp', datetime.utcnow()),  # Default to current UTC time if not provided
            camera_id=data.get('camera_id'),
            violation_type=data.get('violation_type')
        )
