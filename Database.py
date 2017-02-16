from sqlalchemy import Table, Column, String, Integer, Boolean, ForeignKey, create_engine, Date
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    team = relationship("Team", back_populates="members")
    team_id = Column(Integer, ForeignKey('team.id'))
    password_hash = Column(String(255))
    date_of_birth = Column(String)
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    members = relationship("User", back_populates="team")



class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True)
    time = Column(String)
    location = Column(String)
    score = Column(String)
    age_below = Column(Integer)
    phone_number = Column(Integer)
    game_complete = Column(Boolean)
    team1_id = Column(Integer, ForeignKey("team.id"))
    team2_id = Column(Integer, ForeignKey("team.id"))
    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])


engine = create_engine('sqlite:///Database.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()