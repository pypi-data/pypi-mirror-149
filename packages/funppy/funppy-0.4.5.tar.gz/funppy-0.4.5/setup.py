# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['funppy', 'funppy.examples']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.44.0,<2.0.0', 'grpcio>=1.44.0,<2.0.0']

setup_kwargs = {
    'name': 'funppy',
    'version': '0.4.5',
    'description': 'Python plugin over gRPC for funplugin',
    'long_description': '# Python plugin over gRPC\n\n## install SDK\n\nBefore you develop your python plugin, you need to install an dependency as SDK.\n\n```bash\n$ python3 -m pip install funppy\n```\n\n## create plugin functions\n\nThen you can write your plugin functions in python. The functions can be very flexible, only the following restrictions should be complied with.\n\n- function should return at most one value and one error.\n- `funppy.register()` must be called to register plugin functions and `funppy.serve()` must be called to start a plugin server process.\n\nHere is some plugin functions as example.\n\n```python\nimport logging\nfrom typing import List\n\nimport funppy\n\n\ndef sum_two_int(a: int, b: int) -> int:\n    return a + b\n\ndef sum_ints(*args: List[int]) -> int:\n    result = 0\n    for arg in args:\n        result += arg\n    return result\n\ndef Sum(*args):\n    result = 0\n    for arg in args:\n        result += arg\n    return result\n\n\nif __name__ == \'__main__\':\n    funppy.register("sum_two_int", sum_two_int)\n    funppy.register("sum_ints", sum_ints)\n    funppy.register("sum", Sum)\n    funppy.serve()\n```\n\nYou can get more examples at [funppy/examples/].\n\n## build plugin\n\nPython plugins do not need to be complied, just make sure its file suffix is `.py` by convention and should not be changed.\n\n## use plugin functions\n\nFinally, you can use `Init` to initialize plugin via the `xxx.py` path, and you can call the plugin API to handle plugin functionality.\n\n\n[funppy/examples/]: ../funppy/examples/\n',
    'author': 'debugtalk',
    'author_email': 'mail@debugtalk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/httprunner/funplugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
