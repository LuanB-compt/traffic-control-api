class Config():
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///bd.sqlite3"

config_by_name = {
    'config':Config
}
