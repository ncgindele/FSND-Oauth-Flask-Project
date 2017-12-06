from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """Stores information about users. Accounts are necessary to create, edit, and delete items and catagories"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Returns Item data in JSON form"""
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'picture': self.picture,
        }


class Category(Base):
    """Contains information about catagories which are collections of Items"""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    items = relationship('Item', cascade="save-update, merge, delete")

    @property
    def serialize(self):
        """Returns Item data in JSON form"""
        return {
            'name': self.name,
            'id': self.id,
            'user_id': self.user_id,
        }


class Item(Base):
    """Contains information about items which fall under a related category"""
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    icon = Column(String(250))
    year = Column(Integer)
    description = Column(String(2000), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Returns Item data in JSON form"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'category_id': self.category_id,
            'user_id': self.user_id,
        }


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
