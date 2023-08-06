from flask_restx import Api, Namespace


api = Api(
    version="1.0",
    title="DMS API",
    description="A simple DMS API ",
    catch_all_404s=True,
)
ns = Namespace("/DMS", description="Autoplant DMS operations")
api.add_namespace(ns, path="/DMS")

