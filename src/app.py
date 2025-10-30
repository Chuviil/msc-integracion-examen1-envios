from apiflask import APIFlask

app = APIFlask(__name__)


@app.get('/envios')
def get_envios():
    return {'message': 'hello'}

@app.get('/envios/<string:envio_id>')
def get_envio_by_id(envio_id):
    return {'message': 'hello', 'envio_id': envio_id}

@app.post('/envios')
def create_envio():
    return {'message': 'hello'}
