from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()
engine = create_engine("sqlite:///malina.db")
Session = sessionmaker(bind=engine)
db_session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    balance = Column(Integer, default=1000)
    inventory = relationship("Inventory", back_populates="user")

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    item_name = Column(String)
    user = relationship("User", back_populates="inventory")

class Promocode(Base):
    __tablename__ = 'promocodes'
    code = Column(String, primary_key=True)
    reward_type = Column(String)
    reward_value = Column(String)
    used_by = Column(String)

def init_db():
    Base.metadata.create_all(engine)

def get_user(user_id):
    user = db_session.query(User).filter_by(id=user_id).first()
    if not user:
        user = User(id=user_id)
        db_session.add(user)
        db_session.commit()
    return user

def add_item_to_inventory(user_id, item_name):
    get_user(user_id)
    item = Inventory(user_id=user_id, item_name=item_name)
    db_session.add(item)
    db_session.commit()

def get_promocode(code):
    return db_session.query(Promocode).filter_by(code=code).first()

def promocode_used(code, user_id):
    promo = get_promocode(code)
    if promo:
        used = promo.used_by.split(",") if promo.used_by else []
        used.append(user_id)
        promo.used_by = ",".join(set(used))
        db_session.commit()
