import flask
import flask_restx

from backend.clusters.clusters import cluster_bp
from backend.metrics.metrics import metrics_bp

app = flask.Flask(__name__)
api_bp = flask.Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route('/')
def homepage():
    return {"message": "AlphaTeam Backend API"}


# Register the API blueprint with the app
app.register_blueprint(api_bp)
app.register_blueprint(cluster_bp)
app.register_blueprint(metrics_bp)

# add documentation
# api = flask_restx.Api(app, version='1.0', title='AlphaTeam Backend API',
#                       description='Backend API for AlphaTeam',
#                       doc='/api/v1/docs/')


if __name__ == '__main__':
    app.run()
