from neomodel import (
    config, 
    StructuredNode, 
    StringProperty,
    BooleanProperty,
    IntegerProperty,
    FloatProperty,
    DateProperty,
    UniqueIdProperty, 
    RelationshipTo, 
    RelationshipFrom,
    One,
    OneOrMore,
    ZeroOrOne
)

from nacl.pwhash import verify_scryptsalsa208sha256, scryptsalsa208sha256_str
from datetime import date, datetime
import uuid


# ##############################################################################
# IDENTITY OBJECTS
# ##############################################################################

# ------------------------------------------------------------------------------
# CLASS USER
# ------------------------------------------------------------------------------
class User(StructuredNode):
    
    # --------------------------------------------------------------------------
    # CLASS PROPERTIES
    # --------------------------------------------------------------------------
    
    # PROPERTIES
    user_id = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    email = StringProperty(unique_index=True, required=True)
    username = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    is_active = BooleanProperty(required=True)
    
    instruments = StringProperty(required=True)
    
    is_anonymous = False
    is_authenticated = True
    
    # RELATIONS
    groups = RelationshipTo('Group', 'IS_MEMBER_OF')
    bands = RelationshipTo('Band', "IS_MEMBER_OF")
    

    # --------------------------------------------------------------------------
    # DGET ID
    # --------------------------------------------------------------------------
    def get_id(self):
        return self.user_id
   
    # --------------------------------------------------------------------------
    # DICTIONARY PROPERTY
    # --------------------------------------------------------------------------
    @property
    def dictionary(self):
        output = {}
        for prop in self.__dict__.keys():
            if prop is not 'password' and not prop.startswith('__'):
                output[prop] = getattr(prop)
        return output
                
    # --------------------------------------------------------------------------
    # METHOD AUTHENTICATE
    # --------------------------------------------------------------------------
    def authenticate(self, password):
        """
            Compares the given password in a secure way with a value stored in
            database to determine if the password is correct or not.
            
            :param password: The password to be verified if it is the correct password
                   for the given user.
                   
            :return: True if the authentication was successful and the password is
                     correct
        """
        try:
            proposed = password.encode('utf-8')
            hashed = self.password.encode('utf-8')
            return verify_scryptsalsa208sha256(hashed, proposed)
        except Exception as ex:
            return False
        
    # --------------------------------------------------------------------------
    # METHOD UPDATE PASSWORD
    # --------------------------------------------------------------------------
    def update_password(self, password):
        """
            Hashes and securely stores the password in a way that can be verifiable
            but cannot be decrypted.
            
            :param password: The password that will be set to be used as auth mechanism
                             for the user.
                             
            :return:         True if operation completed successfully
        """
        self.password = scryptsalsa208sha256_str(password.encode('utf-8')).decode('utf-8')
        return True


# ------------------------------------------------------------------------------
# CLASS GROUP
# ------------------------------------------------------------------------------       
class Group(StructuredNode):
    
    # PROPERTIES
    group_id = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True, unique_index=True)
    description = StringProperty(required=True)
    
    # RELATIONS
    members = RelationshipTo('User', 'HAS')

    # --------------------------------------------------------------------------
    # DICTIONARY PROPERTY
    # --------------------------------------------------------------------------
    @property
    def dictionary(self):
        output = {}
        for prop in self.__dict__.keys():
            if not prop.startswith('__'):
                output[prop] = getattr(self, prop)
        return output
  
    
# ##############################################################################
# BUSINESS OBJECTS
# ##############################################################################

# ------------------------------------------------------------------------------
# CLASS BAND
# ------------------------------------------------------------------------------       
class Band(StructuredNode):
    
    # PROPERTIES
    band_id = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True, unique_index=True)   
    genres = StringProperty(required=True)  
    logo_url = StringProperty() 
    description = StringProperty(required=True) 
    founded = DateProperty(required=True)
    # Edges
    members = RelationshipTo('User', 'HAS_MEMBER')
    rehearsals = RelationshipTo('Rehearsal', 'HAS_SCHEDULED')
    
    def set_founded(self, day, month, year):
        """
            Sets the date object in Student class
            
            :param day: The day
            :param month: The month
            :param year: The year
            :return: True if well formatted and valid date provided. False if not.
            
        """
        try:
            self.founded = date(int(year), int(month), int(day))
            return True
        except Exception as ex:
            # TODO good exception handling!!!
            print(ex)
            return False
    
# ------------------------------------------------------------------------------
# CLASS BAND
# ------------------------------------------------------------------------------       
class Rehearsal(StructuredNode):
    
    # PROPERTIES
    rehearsal_id = StringProperty(unique_index=True, required=True)
    date = DateProperty(required=True, index=True)
    start_hour = IntegerProperty(required=True)
    start_minute = IntegerProperty(required=True)
    end_hour = IntegerProperty(required=True)
    end_minute = IntegerProperty(required=True)
    place= StringProperty(required=True)
    description = StringProperty(required=True)
    
    # Edges
    band = RelationshipTo('Band', 'SCHEDULED_FOR', cardinality=One)

# ##############################################################################
# TRANSACTIONAL OBJECTS
# ##############################################################################

# ##############################################################################
# STATE OBJECTS
# ##############################################################################
