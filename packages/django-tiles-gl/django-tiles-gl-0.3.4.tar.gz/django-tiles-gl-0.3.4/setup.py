# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_tiles_gl', 'django_tiles_gl.templatetags']

package_data = \
{'': ['*'],
 'django_tiles_gl': ['static/django-tiles-gl/fonts/Open Sans Bold Italic/*',
                     'static/django-tiles-gl/fonts/Open Sans Bold/*',
                     'static/django-tiles-gl/fonts/Open Sans Extra Bold '
                     'Italic/*',
                     'static/django-tiles-gl/fonts/Open Sans Extra Bold/*',
                     'static/django-tiles-gl/fonts/Open Sans Italic/*',
                     'static/django-tiles-gl/fonts/Open Sans Light Italic/*',
                     'static/django-tiles-gl/fonts/Open Sans Light/*',
                     'static/django-tiles-gl/fonts/Open Sans Regular/*',
                     'static/django-tiles-gl/fonts/Open Sans Semibold Italic/*',
                     'static/django-tiles-gl/fonts/Open Sans Semibold/*',
                     'static/django-tiles-gl/maplibre/*',
                     'static/django-tiles-gl/sprites/*',
                     'templates/django_tiles_gl/*']}

install_requires = \
['Django>=3.1,<4.1']

setup_kwargs = {
    'name': 'django-tiles-gl',
    'version': '0.3.4',
    'description': 'Integrated Django Vector Tile Server based on mbtiles',
    'long_description': '# Django Tiles GL\n\nIntegrated Django Vector Tile Server based on mbtiles.\n\n\n## Description\n\nSimple app to serve [Mabpox Vector Tiles](https://docs.mapbox.com/data/tilesets/guides/vector-tiles-standards/) directly from [MBTiles files](https://github.com/mapbox/mbtiles-spec) via Django views.\n\nDjango Tiles has a minimal dependencies. It does not require GeoDjano or any other libraries. Its only dependency is Django itself.\n\nDjango Tiles GL **does not create raster tiles**. It may only be used with map libraries that support to render vector tiles like  [MapLibre](https://maplibre.org/) or [OpenLayers](https://openlayers.org/).\n\nDjango Tiles GL contains the [OSM Bright map style](https://openmaptiles.org/styles/#osm-bright) which can be used to render Vector Tiles following the [OpenMapTiles vector tile  schema](https://openmaptiles.org/schema).\n\nNote that this default style is using [OpenSans fonts](https://github.com/openmaptiles/fonts) which does only contain Latin, Greek and Cyrillic alphabets.\n\nOther tile schemes are possible by creating a custom [map style specification](https://docs.mapbox.com/mapbox-gl-js/style-spec/) and referencing Django Tiles GL [TileJSON endpoint](https://github.com/mapbox/tilejson-spec) as a source.\n\n## Usage\n\nSee the [`demo`](https://github.com/kleingeist/django-tiles-gl/tree/main/demo) Django application for a simple usage example.\n\n\n### Setup\n\n- Add `django_tiles_gl` to you `INSTALLED_APPS` setting.\n- Add `django_tiles_gl.urls` to your url patterns.\n  For example with the `tiles` prefix:\n  ```python\n  urlpatterns = [\n      ...\n      path("tiles/", include("django_tiles_gl.urls")),\n  ]\n  ```\n- Set path to your MBTiles files in you application settings.\n  ```python\n  MBTILES_DATABASE = BASE_DIR / "demo" / "data" / "berlin.mbtiles"\n  ```\n- Optionally set the default center to be set on the default map style.\n  ```python\n  MBTILES_CENTER = [13.4, 52.5, 13]   # [longitude, latitude, zoom]\n  ```\n- Force absolute urls to use SSL by prefixing them with "https://".\n  This might be required if you app is running behind a reverse proxy and you\n  are not able to set [`SECURE_PROXY_SSL_HEADER`](https://docs.djangoproject.com/en/4.0/ref/settings/#secure-proxy-ssl-header)\n  from the SSL enabled proxy server.\n  ```python\n  MBTILES_FORCE_SSL = True\n  ```\n\n### Views\nTo render a map you have to include a JavaScript mapping library and refer to the `tile` endpoint or the default integrated style.\n\nDjango Tiles GL provides the following endpoints:\n\n- `{% url \'django_tiles_gl:openmaptiles_style\' %}` - Default [OpenMapTiles style defintion](https://openmaptiles.org) using the [OSM Bright map style](https://openmaptiles.org/styles/#osm-bright).\n- `{% url \'django_tiles_gl:tilejson\' %}` - [TileJSON](https://github.com/mapbox/tilejson-spec) describing the configured MBTiles files and providing the correct tile urls.\n- `{% url \'django_tiles_gl:tile\' x y z %}` - Actual tile endpoint, returning vector data in the [PBF format](https://wiki.openstreetmap.org/wiki/PBF_Format).\n\n\nDjango Tiles GL is bundles with [MapLibre](https://maplibre.org/) and provides a template tag for easy inclusion. A minimal working example has to contain the following defintions:\n\n```html\n{% load tiles_gl_tags %}\n<!DOCTYPE html>\n<html>\n<head>\n    {% maplibre_head %}\n\n    <style>\n        body { margin:0; padding:0; }\n        #map { position:absolute; top:0; bottom:0; width:100%; }\n    </style>\n</head>\n<body>\n\n<div id=\'map\'></div>\n\n<script>\nvar map = new maplibregl.Map({\n\tcontainer: \'map\',\n\tstyle: \'{% url \'django_tiles_gl:openmaptiles_style\' %}\',\n});\n</script>\n\n</body>\n</html>\n```\n\n## Data / MBTiles generation\n\nThere are mutiple tools to generate valid MBTiles databases. The easiest to use with Django Tiles GL is [OpenMapTiles](https://github.com/openmaptiles/openmaptiles) as it is compatible with the bundled default style.\n\nFor a quickstart you may generate the MbTiles for an area with the following commands:\n```sh\ngit clone https://github.com/openmaptiles/openmaptiles.git\ncd openmaptiles\n./quickstart.sh <area>\n```\n\nFo further information and optiones see [https://github.com/openmaptiles/openmaptiles](https://github.com/openmaptiles/openmaptiles)\n\n\n\n## Further Topics\n\n### Caching\n\nIt is advised setup a caching proxy for the `tile` endpoint. Please refer to you HTTP servers documentation. For example the [nginx proxy cache config](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache)\n\n\n\n## Other Django tile server solutions\n\n- [django-geojson-tiles](https://github.com/glenrobertson/django-geojson-tiles) - Generates GeoJSON tiles from a GeoDjango model. No MBTiles support.  Not to be used as a base layer.\n\n- [django-vectortiles](https://github.com/submarcos/django-vectortiles) - Generates Vector Tile layers from GeoDjango. No MBTiles support. Not to be used as a base layer.\n\n- [django-mbtiles](https://github.com/makinacorpus/django-mbtiles) - Uses MBTiles to generate rastered tiles and [UTFGrid](https://github.com/mapbox/mbtiles-spec/blob/master/1.1/utfgrid.md). Does not support modern vector tiles. Strong inspiration for this project.\n',
    'author': 'Johannes Dillmann',
    'author_email': 'dev@ae35.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kleingeist/django-tiles-gl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
