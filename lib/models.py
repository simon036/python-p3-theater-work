from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import create_engine

# Define the base class
Base = declarative_base()

class Audition(Base):
    __tablename__ = "auditions"

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)  # Default to False
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="auditions")

    def call_back(self):
        self.hired = True

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    auditions = relationship("Audition", back_populates="role")

    def actors(self):
        return [audition.actor for audition in self.auditions]
    
    def locations(self):
        return [audition.location for audition in self.auditions]
    
    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0] if hired_auditions else "no actor has been hired for this role."
    
    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else "no actor has been hired for understudy for this role."

# Create the database engine
engine = create_engine("sqlite:///theater.db")
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Add data to the database
role = Role(character_name="Simon")

audition1 = Audition(actor="Morgan Freeman", location="L.A California", phone=123456789, role=role)
audition2 = Audition(actor="Denzel Washington", location="L.A California", phone=987654321, role=role)

session.add(role)
session.add(audition1)
session.add(audition2)
session.commit()

# Test the methods
print(role.actors())  # Output: ['Morgan Freeman', 'Denzel Washington']
print(role.locations())  # Output: ['L.A California', 'L.A California']

# Hire Morgan Freeman
audition1.call_back()
session.commit()

print(role.lead())  # Output: <Audition object at 0x7f8b1c2b3d90>
print(role.understudy())  # Output: 'no actor has been hired for understudy for this role'