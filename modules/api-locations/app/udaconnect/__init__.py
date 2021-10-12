from app.udaconnect.models import Connection, Location, Person  # noqa
from app.udaconnect.schemas import  LocationSchema  # noqa


def register_routes(api, app, root="api-locations"):
    from app.udaconnect.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")
