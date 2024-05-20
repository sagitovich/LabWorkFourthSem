import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

# Импортируем из библитеки SqlAlchemy нужные функции и классы
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, CheckConstraint
from sqlalchemy import Integer, String, Boolean, DateTime, Numeric, SmallInteger

# Импортируем из подмодуля ORM функции и классы, предназначенные для
# высокоуровневой работы с базой данных посредством построения объектной модели ORM
# (ORM ~ object-relational model)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


# Так просто надо сделать
class Basis(DeclarativeBase):
    pass


class User(Basis):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    created_on = Column(DateTime(), default=dt.datetime.now)
    updated_on = Column(DateTime(), default=dt.datetime.now, onupdate=dt.datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    stories = relationship("Story", back_populates="author")

    def __str__(self):
        return f"<{self.id}> {self.first_name} {self.last_name} aka {self.username}"

    def __repr__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Story(Basis):
    __tablename__ = "stories"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False, default="(без темы)")
    content = Column(String())
    author_id = Column(Integer(), ForeignKey('users.id'))
    is_private = Column(Boolean(), default=True, nullable=False)
    created_on = Column(DateTime(), default=dt.datetime.now)
    updated_on = Column(DateTime(), default=None, onupdate=dt.datetime.now)

    author = relationship("User", back_populates="stories")
    categories = relationship("Category", back_populates="stories",
            secondary="stories_categories")

    def __str__(self):
        return f"<{self.id}> {self.title}: {self.content[:20]}"

    def __repr__(self):
        return f"<{self.id}> {self.title}"


class Category(Basis):
    __tablename__ = "categories"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    color = Column(String(6), nullable=False, default="808080")

    stories = relationship("Story", back_populates="categories",
            secondary="stories_categories", )


class StoryCategory(Basis):
    __tablename__ = "stories_categories"
    story_id = Column(Integer(), ForeignKey('stories.id'), primary_key=True)
    category_id = Column(Integer(), ForeignKey('categories.id'), primary_key=True)   


engine = create_engine("sqlite:///My Database/blog.db?echo=True")

Basis.metadata.create_all(engine)

factory = sessionmaker(bind=engine)
