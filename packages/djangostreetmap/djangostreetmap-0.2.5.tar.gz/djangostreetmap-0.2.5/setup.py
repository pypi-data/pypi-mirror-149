# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangostreetmap',
 'djangostreetmap.management.commands',
 'djangostreetmap.maplibre',
 'djangostreetmap.migrations',
 'maplibre']

package_data = \
{'': ['*'], 'djangostreetmap': ['templates/*']}

install_requires = \
['osmflex>=0.2.0,<0.3.0', 'pydantic>=1.9.0,<1.10.0']

setup_kwargs = {
    'name': 'djangostreetmap',
    'version': '0.2.5',
    'description': 'Deliver OpenstreetMap data in GeoJSON and MVT tile formats',
    'long_description': '[![codecov](https://codecov.io/gh/joshbrooks/djangostreetmap/branch/main/graph/badge.svg?token=MXcJUkbOMf)](https://codecov.io/gh/joshbrooks/djangostreetmap)\n\n# DjangoStreetMap\n\nDjangSstreetMap is a Django application to load OSM data into a postgis database and deliver OSM data as\nMVT tiles.\n\n## Openstreetmap Vector Tiles\n\n> "A vector tile is a lightweight data format for storing geospatial vector data"\n\nFor an introduction to MVT (Mapbox Vector Tiles) see the [mapbox docs](https://docs.mapbox.com/help/glossary/vector-tiles/)\nFor an introduction to OSM see [openstreetmap.org](https://www.openstreetmap.org/)\n\n## Purpose of this project\n\nThis is a Django application to\n\n1. Import OSM data as Django models\n2. Expose Django models as MVT (Mapbox Vector Tile) geographic format data\n\nTile generation is much faster when geometry is in srid=3857 (or maybe with an index in that SRID?)\n\n## Prerequisites\n\nYou need the `gdal` libraries installed\n\nOn Ubuntu:\n```\nsudo apt install binutils libproj-dev gdal-bin\n```\n\nOtherwise refer to the Django docs "Installing geospatial libraries"\n## Adding to a Project\n\nIf necessary install psycopg2 in your env\n\nExtend installed_apps with the following apps:\n\n`pip install osmflex`\n\n```python\n[\n    "django.contrib.gis",\n    "djangostreetmap",\n    "osmflex",\n]\n```\n\n## (Recommended) Set your cache\n\nYou likely want to set a fast cache for your tiles like Memcached. If this is not found\nthe default cache will be used; this can be a bit slower and is very much non persistent\nThis assumes you\'re running memcached (Linux: `apt install memcached`) and installed memcached(`pip install python-memcached`)\n\n```python\nCACHES = {\n    \'default\': {\n        \'BACKEND\': \'django.core.cache.backends.memcached.MemcachedCache\',\n        \'LOCATION\': \'127.0.0.1:11211\',\n    }\n}\n```\n\n## Running faster in testing\n\nRun `poetry install`\n\nTo run pytest, you need to have an appropriate postgis database\nIf you use docker one option is to run the following:\n\n```bash\ndocker run \\\n    --rm \\\n    -p 49155:5432 \\\n    --name=djangostreetmap \\\n    -e POSTGRES_PASSWORD=post1234 \\\n    postgis/postgis:14-3.2 \\\n    -c fsync=off \\\n    -c shared_buffers=4096MB\n```\nRun `poetry run pytest`\n\n\nRunserver is "ok" but this recipe will give faster performance for demonstration purposes\n\n\n\n```bash\npip install gunicorn\ngunicorn -w 8 djangostreetmap.wsgi:application\n```\n\n## Building\n\npoetry version patch\npoetry build\npoetry publish\n\n## Writing Views\n\nTo set up a new View, create a subclass of TileLayerView with some `MvtQuery` instances as layers:\n\n```python\nclass RoadLayerView(TileLayerView):\n    layers = [\n        MvtQuery(table=OsmHighway._meta.db_table, attributes=["name"], filters=[f"\\"highway\\"=\'{road_class}\'"], layer=road_class)\n        for road_class in ("primary", "secondary", "tertiary")\n    ]\n```\n\nAppend the URL to your urls.py as follows. Note the zoom, x and y are mandatory.\n\n```python\n    path("highways/<int:zoom>/<int:x>/<int:y>.pbf", RoadLayerView.as_view()),\n```\n\n## Running in Development\n\n### Set up postgis\n\n```bash\ndocker run --name=osm \\\n    -e POSTGRES_DB=postgres \\\n    -e POSTGRES_USER=postgres \\\n    -e POSTGRES_PASSWORD=post1234 \\\n    -p 49155:5432 \\\n    postgis/postgis:12-3.1\n```\n\nFind your port: if you do not use `49155` as above:\n\n```sh\n(env) josh@m4800:~/github/joshbrooks/djangostreetmap$ docker ps\nCONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS             PORTS                                         NAMES\nc619232fe38a   postgis/postgis:12-3.1           "docker-entrypoint.s…"   33 seconds ago   Up 32 seconds      0.0.0.0:49155->5432/tcp, :::49155->5432/tcp   osm\n...\n```\n\nOSM is on port 49155\n\nTo apply this to your project:\n\n```python\n  DATABASES = {\n    "default": {\n        "ENGINE": "django.contrib.gis.db.backends.postgis",\n        "USER": "postgres",\n        "PASSWORD": "post1233",\n        "HOST": "localhost",\n        "PORT": "49154",\n        "NAME": "postgres",\n    }\n}\n```\n\n### Fetch your data\n\nwget https://download.geofabrik.de/australia-oceania/papua-new-guinea-latest.osm.pbf\n\nor\n\nwget https://download.geofabrik.de/asia/east-timor-latest.osm.pbf\n\n### Installing osm2psql\n\nTo run the management command below you\'ll need an `osm2pgsql` version of around 1.3 or greater. This is not available in the ubuntu package manager (yet)...\n\n### Import Data\n\nThe "osmflex" app has two management commands to run which will populate osmflex models\n\n```sh\n./manage.py run_osm2pgsql /media/josh/blackgate/osm/asia/east-timor-latest.osm.pbf\n```\n\n```sh\n./manage.py import_from_pgosmflex\n```\n\n### Exploring data\n\nSee the Django admin for osmflex:\n\nhttp://localhost:8000/admin/osmflex\n\npsql --host localhost --username postgres --port 49159\n\n### Qgis\n\n- Add a new Postgres Connection with the following settings:\n\nName: DjangoStreetMap\nHost: localhost\nPort: 49155\nDatabase: postgres\n\nAuthentication: Basic\npostgres / post1233\n\n## Development\n\nCode is blacked, flaked, isorted and mypy\'d.\n\n`pip install pre-commit`\n',
    'author': 'Joshua Brooks',
    'author_email': 'josh.vdbroek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joshbrooks/djangostreetmap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
