from dotenv import load_dotenv
from os import getenv
load_dotenv()


class Settings:
    db_user = getenv('DB_USER')
    db_password = getenv('DB_PASSWORD')
    db_name = getenv('DB_NAME')
    db_host = getenv('DB_HOST')
    db_port = getenv('DB_PORT')

    default_admin_emails = getenv('DEFAULT_ADMIN_EMAILS')


# database malumotlarni sozlash
db_info = {
    'user': Settings.db_user,
    'password': Settings.db_password,
    'dbname': Settings.db_name,
    'host': Settings.db_host,
    'port': Settings.db_port
}

# default admin emaillari
admins = Settings.default_admin_emails