from quart import Quart
from quart_cors import cors
import logging
from views.user_views import user_bp
from views.plant_views import plant_bp
from views.grow_views import grow_bp

logging.basicConfig(level=logging.DEBUG)

app = Quart(__name__)
app = cors(app, allow_origin="*")

# Registro dos blueprints
app.register_blueprint(user_bp)
app.register_blueprint(plant_bp)
app.register_blueprint(grow_bp)

@app.route('/')
async def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
