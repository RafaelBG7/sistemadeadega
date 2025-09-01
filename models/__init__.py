from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models_adega import *
from .fornecedor import *
from .lote import * 