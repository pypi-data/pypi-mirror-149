# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qiskit_qryd_provider']

package_data = \
{'': ['*']}

install_requires = \
['qiskit-terra>=0.20.0,<0.21.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'qiskit-qryd-provider',
    'version': '0.2.6',
    'description': 'Qiskit provider that allows for accessing the emulator and future Rydberg quantum computer of the QRydDemo consortium.',
    'long_description': '# Qiskit QRyd Provider\n\nThis Python library contains a provider for the [Qiskit](https://qiskit.org) quantum computing framework. The provider allows for accessing the GPU-based emulator and the future Rydberg quantum computer of the [QRydDemo](https://thequantumlaend.de/qryddemo/) consortium.\n\n## Installation\n\nThe provider can be installed via\n```bash\npip install qiskit-qryd-provider\n```\n\n## Basic Usage\n\nTo use the provider, a QRydDemo API token is required. The token can be obtained via our [online registration form](https://thequantumlaend.de/get-access/).\n\nYou can use the token to initialize the provider:\n\n```python\nfrom qiskit_qryd_provider import QRydProvider\nprovider = QRydProvider("MY_TOKEN")\n```\n\nAfterwards, you can choose a backend. Different backends are available that are capable of running ideal simulations of quantum circuits. An inclusion of noise models is planned for the future. You can either choose a backend emulating 30 qubits arranged in a 5x6 square lattice with nearest-neighbor connectivity\n\n```python\nbackend = provider.get_backend("qryd_emu_localcomp_square")\n```\n\nor a backend emulating 30 qubits arranged in a triangle lattice with nearest-neighbor connectivity\n\n```python\nbackend = provider.get_backend("qryd_emu_localcomp_triangle")\n```\n\nIf you use these backends, Qiskit automatically transpiles arbitrary quantum circuits to comply with the native gate set and connectivity of the Rydberg platform. The backends are also available as variants where the compilation happens on our servers (`"qryd_emu_cloudcomp_square"` and `"qryd_emu_cloudcomp_triangle"`), using a decomposer developed by [HQS Quantum Simulations](https://quantumsimulations.de/).\n\nAfter selecting a backend, you can run a circuit on the backend:\n\n```python\nfrom qiskit import QuantumCircuit, execute\nqc = QuantumCircuit(2, 2)\nqc.h(0)\nqc.cx(0, 1)\nqc.measure([0, 1], [0, 1])\njob = execute(qc, backend, shots=200, optimization_level=3)\nprint(job.result().get_counts())\n```\n\n## Expert Options\n\nThe value of the phase shift of the [PCZ gate](https://arxiv.org/abs/2202.13849) can be modified before using the backend via:\n\n```python\nfrom qiskit_qryd_provider import PCZGate\nPCZGate.set_pcz_theta(VALUE)\n```\n\n## License\n\nThe Qiskit QRyd Provider is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). \n',
    'author': 'Sebastian Weber',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
