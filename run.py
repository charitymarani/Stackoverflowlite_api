from application import create_app


from stackoverflow import create_app
from stackoverflow import settings
from manage import DBMigration

migrate = DBMigration()
config_name = 'development'
app = create_app(config_name)

if __name__ == "__main__":
    migrate.create_all()
    app.run(debug=True)
