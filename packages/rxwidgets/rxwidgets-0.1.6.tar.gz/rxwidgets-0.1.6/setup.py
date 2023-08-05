# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rxwidgets',
 'rxwidgets.ipython',
 'rxwidgets.ipython.pandas',
 'rxwidgets.ipython.pandas.dataframe',
 'rxwidgets.ipython.widgets',
 'rxwidgets.rx']

package_data = \
{'': ['*']}

install_requires = \
['ipywidgets>=7.6.3,<8.0.0', 'reactivex>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'rxwidgets',
    'version': '0.1.6',
    'description': 'iPython notebooks with reactive UI - powered by RxPy and ipywidgets',
    'long_description': '# General\n\nThis package adds functionality useful for making [ReactiveX](https://rxpy.readthedocs.io) powered [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/).\n\nNote that this package is in its Beta stage and may change interfaces slightly before a 1.0 release.\n\n# Installation\n\nRun `poetry add rxwidgets`\n\n# Usage\n\n```py\nimport rxwidgets.ipython as rxi\n\n@rxi.interact_manual\ndef b(a=(1,5)):\n    return a * 5\n\n@rxi.interact\ndef c(b=b, c=(10, 20)):\n    c = b + c\n    print(f"C: {c}")\n```\n\nCorresponds roughly to native ipywidgets:\n\n```py\nfrom ipywidgets import interact, interact_manual\n\n@interact_manual\ndef b(a=(1,5)):\n    b = a * 5\n\n    @interact\n    def c(c=(10, 20)):\n        c = b + c\n        print(f"C: {c}")\n```\n\nAn incomprehensive feature list is provided in the `examples` folder.\n\n# Streams\n\nA function stream consists of these steps:\n\n1. `@rxi.stream_defaults`\n   - Convert parameter defaults into observables - may display ipywidgets.\n   - Convert function into a stream of its results from input streams.\n   - In stream: Curry the function and make wrap into a `ValueBox`.\n   - Object in stream: `ValueBox(partial(fn, ...))`\n2. `@rxi.defer`, `@rxi.pre_load`, ...\n   - If desired, apply operators to the call-ready function\n3. `@rxi.apply`\n    - Create and display an `rxi.Screen`.\n    - In stream: Run the function inside the screen and return results as a `ValueBox`.\n    - Object in stream: `ValueBox(fn(...))`\n4. `@rxi.Automap`\n    - If desired, pack the final stream into an `Automap` object. This object maps all operators to operators applied inside the stream.\n',
    'author': 'Lukas Tenbrink',
    'author_email': 'lukas.tenbrink@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ivorforce/rxwidgets',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
