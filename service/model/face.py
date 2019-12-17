from service.model import db
from service import parameters


class Face(db.Model):
    """Store logined face information."""
    
    # Table name.
    __tablename__ = 'login_face'
    
    # User's id.
    uid = db.Column(db.String(32), primary_key=True)
    
    # Type of user id.
    uid_type = db.Column(db.String(16))
    
    # User name.
    name = db.Column(db.String(15))
    
    # Upload channel.
    channel = db.Column(db.String(16))
    
    # Logined time.
    login_time = db.Column(db.String(19))
    
    # Feature string.
    feature = db.Column(db.String(4096))
    
    # Path to save image.
    img_path = db.Column(db.String(4096))

    def __init__(self, feature_array, **kwargs):
        """ Constructor for Face model.
        An additional feature_array is used to initialize face feature.
        """
        super().__init__(**kwargs)
        self.feature = self.to_feature_string(feature_array)

    def to_feature_string(self, feature_array):
        """Convert feature array to a feature string.
        Use '|' to concentrate all number in feature array.
        """
        FEATURE_DIMENSION = parameters['FEATURE_DIMENSION']
        feature_string = ''
        for i in range(FEATURE_DIMENSION - 1):
            feature_string += (str(feature_array[i]) + '|')
        feature_string += str(feature_array[FEATURE_DIMENSION - 1])
        return feature_string

