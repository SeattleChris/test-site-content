from dotenv import load_dotenv
import config
import application
load_dotenv()


app = application.create_app(config)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
