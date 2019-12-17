from service.model import db

class Log(db.Model):
    """Store check person request result."""
    
    # Table name.
    __tablename__ = 'check_log'

    # Flow number of request.
    num = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # User's id.
    uid = db.Column(db.String(32))
    
    # Type of user id.
    uid_type = db.Column(db.String(16))
    
    # User name.
    name = db.Column(db.String(15))
    
    # Upload channel.
    channel = db.Column(db.String(16))
    
    # Timestamp for this request.
    check_time = db.Column(db.String(19))
    
    # Path to save image.
    img_path = db.Column(db.String(4096))
    
    # Comparasion result.
    result = db.Column(db.Integer)
    
    # Comparasion similarity.
    sim = db.Column(db.Float)

