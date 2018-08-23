from application import create_app

config_name = 'development'
app = create_app(config_name)
# method to run app.py
if __name__ == '__main__':
    app.run()
