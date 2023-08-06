# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pckit']

package_data = \
{'': ['*']}

install_requires = \
['MPh>=1.1.5,<2.0.0',
 'mpi4py>=3.1.3,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'pckit',
    'version': '0.1.0',
    'description': 'A simple package for parallel computing with Python',
    'long_description': "# pckit\n\nThis is a simple package for parallel computing with Python.\n\n## Usage\n### Multiprocessing\nSimple multiprocess solver usage.\nHere the square of 2 and 3 are evaluated by 2 workers.\n\n```python\nimport pckit.task\nimport pckit\n\n\nclass MyModel(pckit.Model):\n    def results(self, x):\n        # solve here your problem f(x) = x^2\n        return x ** 2\n\n\nif __name__ == '__main__':\n    model = MyModel()\n    worker = pckit.SimpleMultiprocessingWorker(model)\n    with pckit.get_solver(worker, workers_num=2) as solver:\n        # create tasks to solve. You can put args or kwargs here\n        tasks = [pckit.task.Task(2), pckit.task.Task(x=3)]\n        results = solver.solve(tasks)\n        print(results)\n        # >>> [4, 9]\n```\n\n### MPI\nYou can simply run scripts on the cluster with [mpi4py](https://github.com/mpi4py/mpi4py) implementation on MPI. \nSimply by changing `SimpleMultiprocessingWorker` to `SimpleMPIWorker` in previous example and starting script with MPI `mpiexec -np 3 python -m mpi4py your_script.py`.\n\n```python\nworker = pckit.SimpleMPIWorker(model)\n```\n\n### Examples\n[More examples](./examples)\n\n## Features\n### Cache\nDict based cache is available by `caching` argument in solver.\n`tag` property in `Task` is required and has to be Hashable.\n\n```python\nwith pckit.get_solver(worker, caching=True) as solver:\n    tasks = [pckit.Task(2, tag='2'), pckit.Task(2, tag='2')]\n```\nSecond result will be reused from cache.",
    'author': 'djiboshin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/djiboshin/pckit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
