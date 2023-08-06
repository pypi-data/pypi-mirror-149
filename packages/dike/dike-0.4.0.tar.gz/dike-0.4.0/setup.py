# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dike', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['pymdown-extensions[docs]>=8.2,<9.0']

setup_kwargs = {
    'name': 'dike',
    'version': '0.4.0',
    'description': 'Python asyncio tools for web service resilience.',
    'long_description': '# dike\n\n**Python asyncio tools for web service resilience**\n\n* Documentation: <https://chr1st1ank.github.io/dike/>\n\n[<img src="https://img.shields.io/pypi/v/dike.svg" alt="Release Status">](https://pypi.python.org/pypi/dike)\n[![GitHub license](https://img.shields.io/github/license/chr1st1ank/dike)](https://github.com/chr1st1ank/dike/blob/main/LICENSE)\n[<img src="https://github.com/chr1st1ank/dike/actions/workflows/test.yml/badge.svg?branch=main" alt="CI Status">](https://github.com/chr1st1ank/dike/actions)\n[![codecov](https://codecov.io/gh/chr1st1ank/dike/branch/main/graph/badge.svg?token=4oBkRHXbfa)](https://codecov.io/gh/chr1st1ank/dike)\n\n\n## Features\n\n### Retry decorator for asynchronous functions\nA very common task especially for network calls is an automatic retry with proper exception\nlogging. There are good implementations like the [retry](https://pypi.org/project/retry/)\npackage for classic functions. But dike provides a similar implementation for coroutine functions.\nThis is available with the `@retry` decorator.\n\nSimplified example:\n```python\nimport asyncio\nimport datetime\nimport logging\nimport sys\n\nimport dike\n\n\n@dike.retry(attempts=2, delay=datetime.timedelta(milliseconds=10), exception_types=RuntimeError)\nasync def web_request():\n    raise RuntimeError("Request failed!")\n\n\nasync def main():\n    response = await web_request()\n    print(response)\n\nlogging.basicConfig(stream=sys.stdout)\nasyncio.run(main())\n```\n\nThe output shows first a warning log message including the exception info (that\'s configurable).\nThis is especially useful if you use structured logging.\n```\n# Log for first attempt:\nWARNING:dike:Caught exception RuntimeError(\'Request failed!\'). Retrying in 0.01s ...\nTraceback (most recent call last):\n...\nRuntimeError: Request failed!\n```\n\nThen, the for the final failure the exception is propagated to the function caller:\n```\nTraceback (most recent call last):\n  ...\nRuntimeError: Request failed!\n\nProcess finished with exit code 1\n```\n\n\n### Concurrency limiting for asynchronous functions\nThe `@limit_jobs` decorator allows to limit the number of concurrent excecutions of a coroutine\nfunction. This can be useful for limiting queueing times or for limiting the load put\nonto backend services.\n\nExample with an external web request using the [httpx](https://github.com/encode/httpx) library:\n\n```python\nimport asyncio\nimport dike\nimport httpx\n\n\n@dike.limit_jobs(limit=2)\nasync def web_request():\n    """Sends a slow web request"""\n    async with httpx.AsyncClient() as client:\n        response = await client.get("https://httpstat.us/200?sleep=100")\n    return response\n\n\nasync def main():\n    # Send three requests at the same time\n    call1 = web_request()\n    call2 = web_request()\n    call3 = web_request()\n    responses = await asyncio.gather(call1, call2, call3, return_exceptions=True)\n    # Print the responses\n    for r in responses:\n        if isinstance(r, dike.TooManyCalls):\n            print("too many calls")\n        else:\n            print(r)\n\n\nasyncio.run(main())\n```\n\nThe output shows that the first two requests succeed. The third one hits the concurrency limit and a TooManyCalls exception is returned:\n```\n<Response [200 OK]>\n<Response [200 OK]>\ntoo many calls\n```\n\n### Mini-batching for asynchronous function calls\nThe `@batch` decorator groups function calls into batches and only calls the wrapped function\nwith the aggregated input.\n\nThis is useful if the function scales well with the size of the input arguments but you\'re\ngetting the input data in smaller bits, e.g. as individual HTTP requests.\n\nThe arguments can be batched together as a Python list or optionally also as numpy array.\n\nExample:\n\n```python\nimport asyncio\nimport dike\n\n\n@dike.batch(target_batch_size=3, max_waiting_time=10)\nasync def add_args(arg1, arg2):\n    """Elementwise sum of the values in arg1 and arg2"""\n    print(f"arg1: {arg1}")\n    print(f"arg2: {arg2}")\n    return [a1 + a2 for a1, a2 in zip(arg1, arg2)]\n\n\nasync def main():\n    result = await asyncio.gather(\n        add_args([0], [1]),\n        add_args([1], [1]),\n        add_args([2, 3], [1, 1]),\n    )\n\n    print(f"Result: {result}")\n\n\nasyncio.run(main())\n```\n\nOutput:\n```\narg1: [0, 1, 2, 3]\narg2: [1, 1, 1, 1]\nResult: [[1], [2], [3, 4]]\n```\n\n## Installation\nSimply install from pypi. The library is pure Python without any dependencies other than the\nstandard library.\n```\npip install dike\n```\n',
    'author': 'Christian Krudewig',
    'author_email': 'chr1st1ank@krudewig-online.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chr1st1ank/dike',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
