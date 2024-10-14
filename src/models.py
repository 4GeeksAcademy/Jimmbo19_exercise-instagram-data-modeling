import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from eralchemy2 import render_er

Base = declarative_base()


from enum import Enum as PyEnum

class ReactionType(PyEnum):
    LIKE = "like"
    LOVE = "love"
    HAHA = "haha"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"


class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(250), nullable=False)
    apellido = Column(String(250), nullable=False)
    username = Column(String(250), unique=True, nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())

    posts = relationship('Post', back_populates='usuario')
    comentarios = relationship('Comentario', back_populates='usuario')
    reacciones = relationship('Reaccion', back_populates='usuario')


class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    contenido = Column(String(500), nullable=False)
    imagen = Column(String(250))  # Opcional: puedes almacenar la ruta de la imagen
    fecha_creacion = Column(DateTime, default=func.now())
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    
    comentarios = relationship('Comentario', back_populates='post')
    reacciones = relationship('Reaccion', back_populates='post')
    usuario = relationship('Usuario', back_populates='posts')


class Comentario(Base):
    __tablename__ = 'comentario'
    
    id = Column(Integer, primary_key=True)
    contenido = Column(String(500), nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    
    usuario = relationship('Usuario', back_populates='comentarios')
    post = relationship('Post', back_populates='comentarios')

class Reaccion(Base):
    __tablename__ = 'reaccion'
    
    id = Column(Integer, primary_key=True)
    tipo = Column(Enum(ReactionType), nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    
    usuario = relationship('Usuario', back_populates='reacciones')
    post = relationship('Post', back_populates='reacciones')

class Amistad(Base):
    __tablename__ = 'amistad'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    amigo_id = Column(Integer, ForeignKey('usuario.id'))
    fecha_creacion = Column(DateTime, default=func.now())
    es_aceptado = Column(Boolean, default=False)
    
    usuario = relationship('Usuario', foreign_keys=[usuario_id])
    amigo = relationship('Usuario', foreign_keys=[amigo_id])


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
