import sys
import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Association table for many-to-many relationship between Users and Voices
user_voice_association = Table('user_voice_association', Base.metadata,
    Column('user_token', String, ForeignKey('Users.user_token'), primary_key=True),
    Column('voice_id', Integer, ForeignKey('Voices.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'Users'
    user_token = Column(Integer, primary_key=True, unique=True, nullable=False)
    username = Column(String, nullable=False)

    # Relationship to Voices (many-to-many)
    voices = relationship("Voice", secondary=user_voice_association, back_populates="users")


class Voice(Base):
    __tablename__ = 'Voices'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    voice_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Store the file path to the .wav file

    # Relationship to Users (many-to-many)
    users = relationship("User", secondary=user_voice_association, back_populates="voices")


# Example to use these models in an SQLite database for testing purposes
if __name__ == "__main__":
    engine = create_engine('sqlite:///tts_system.db')
    Base.metadata.create_all(engine)
    print("Tables created!")
