# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopulsar']

package_data = \
{'': ['*']}

install_requires = \
['pulsar-client>=2.10.0,<3.0.0']

setup_kwargs = {
    'name': 'aiopulsar-py',
    'version': '0.0.0a0',
    'description': 'Asynchronous wrapper for the python pulsar-client.',
    'long_description': '# aiopulsar-py\n**aiopulsar-py** is a Python 3.5+ module that makes it possible to interact with pulsar servers with asyncio. \n**aiopulsar-py** serves as an asynchronous wrapper for the \n[official python pulsar-client](https://pulsar.apache.org/docs/en/client-libraries-python/) and preserves the look and \nfeel of the original pulsar-client. It is written using the async/await syntax and hence not compatible with Python\nversions older than 3.5. Internally, aiopulsar-py employs threads to avoid blocking the event loop.\n\n**aiopulsar-py** takes inspiration from other asyncio wrappers released in the \n[aio-libs project](https://github.com/aio-libs).\n## Basic example\n**aiopulsar-py** is built around the [python pulsar-client](https://pulsar.apache.org/docs/en/client-libraries-python/)\nand provides the same api. You just need to use asynchronous context managers and await for every method. Setting up a\npulsar client that can be used to create readers, producers and consumers requires a call to the ``aiopulsar.connect`` \nmethod.\n````python\nimport asyncio\nimport aiopulsar\nimport pulsar\n\n\nasync def test_example():\n    topic = "persistent://some-test-topic/"\n\n    async with aiopulsar.connect("localhost") as client:\n        async with client.subscribe(\n            topic=topic,\n            subscription_name=\'my-subscription\',\n            consumer_name="my-consumer",\n            initial_position=pulsar.InitialPosition.Earliest,\n        ) as consumer:\n            while True:\n                msg = await consumer.receive()\n                print(msg)\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(test_example())\n````\n## Install\n**aiopulsar-py** cannot be installed on windows systems since the wrapped \n[pulsar-client](https://pulsar.apache.org/docs/en/client-libraries-python/) library only functions on Linux and MacOS.\nThe package is available on PyPi and can be installed with:\n````shell\npip install aiopulsar-py\n````\n## Contributing\nYou can contribute to the project by reporting an issue. This is done via GitHub. Please make sure to include \ninformation on your environment and please make sure that you can express the issue with a reproducible test case. \n\nYou can also contribute by making pull requests. To install the project please use poetry:\n````shell\npoetry install\n````\nThe project relies on ``mypy``, `black` and `flake8` and these are configured as git hooks. \nTo configure the git hooks run:\n````shell\npoetry run githooks setup\n````\nEvery time the git hooks are changed in the ``[tool.githooks]`` section of `pyproject.toml` you will need to set up\nthe git hooks again with the command above.',
    'author': 'Mads Hansen Baattrup',
    'author_email': 'mads@baattrup.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mads-hb/aiopulsar-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
