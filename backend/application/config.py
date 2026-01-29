import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
        DEBUG=False
        SQLITE_DB_DIR= None
        SQLALCHEMY_DB_URI= None
        SQLALCHEMY_TRACK_MODIFICATION = False
        JWT_SECRET_KEY = "super-secret-change-this"
        JWT_ACCESS_TOKEN_EXPIRES = 7200  # 1 hour      

class LocalConfig(Config):
        DEBUG= True 
        SQLITE_DB_DIR= os.path.join(basedir, "../database")
        SQLALCHEMY_DATABASE_URI= "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
        SQLALCHEMY_TRACK_MODIFICATION = False        

class ProductionConfig(Config):
        pass
    