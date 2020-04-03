import config
import application

app = application.create_app(config)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')
    # app.run(host='0.0.0.0', port=8080)
    app.run(host='127.0.0.1', port=8080)
