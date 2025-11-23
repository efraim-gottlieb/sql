from sqlmodel import SQLModel, Session,create_engine, select, Field

DB_URL = 'mysql+pymysql://root:root@localhost:3306/testdb'
engine = create_engine(DB_URL)

class User(SQLModel, table = True):
  __tablename__ = 'users'
  id :int | None = Field(default=None, primary_key=True)
  user_name :str = Field(min_length=2)

SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

# with Session(engine) as session:
#   user = User(user_name='sari')
#   session.add(user)
#   session.commit()
#   session.refresh(user)
#   print(user)

with Session(engine) as session:
  users = session.exec(select(User).where(User.id == 1)).first()
  print(users)
  session.commit()
  print(users)

