from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Voice, Base

# Create an engine to connect to the SQLite database
engine = create_engine('sqlite:///tts_system.db')

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if they don't already exist
Base.metadata.create_all(engine)

u0 = User(user_token=0, username="Admin")
u1 = User(user_token=1, username="Jose")
u2 = User(user_token=2, username="Ana")
u3 = User(user_token=3, username="Pedro")
u4 = User(user_token=4, username="Maria")
u5 = User(user_token=5, username="Carlos") 


v1 = Voice(voice_name="ai-female-voice", file_path="inputs/voices/ai-female-voice.wav")
v2 = Voice(voice_name="duarte", file_path="inputs/voices/duarte.wav")
v3 = Voice(voice_name="morgan-freeman", file_path="inputs/voices/eng_morgan_freeman.wav")

session.add(u0)
session.add(u1)
session.add(u2)
session.add(u3)
session.add(u4)
session.add(u5)

session.add(v1)
session.add(v2)
session.add(v3)

session.commit() #commit users and voices
print("User and Voice added to the database!")


u1.voices.append(v1)
u2.voices.append(v2)
u3.voices.append(v3)
u4.voices.append(v1)
u4.voices.append(v2)
u5.voices.append(v2)
u5.voices.append(v3)

session.commit() #commit associations
print("User associated to voices")

# Querying Users and Voices to verify
users = session.query(User).all()

for user in users:
    print(f"User: {user.username} (Token: {user.user_token})")
    for voice in user.voices:
        print(f"  Voice: {voice.voice_name}, File Path: {voice.file_path}")

# Close the session
session.close()