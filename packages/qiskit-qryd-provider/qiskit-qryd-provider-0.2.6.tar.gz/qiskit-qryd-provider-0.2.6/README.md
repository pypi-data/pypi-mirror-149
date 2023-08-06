# Qiskit QRyd Provider

This Python library contains a provider for the [Qiskit](https://qiskit.org) quantum computing framework. The provider allows for accessing the GPU-based emulator and the future Rydberg quantum computer of the [QRydDemo](https://thequantumlaend.de/qryddemo/) consortium.

## Installation

The provider can be installed via
```bash
pip install qiskit-qryd-provider
```

## Basic Usage

To use the provider, a QRydDemo API token is required. The token can be obtained via our [online registration form](https://thequantumlaend.de/get-access/).

You can use the token to initialize the provider:

```python
from qiskit_qryd_provider import QRydProvider
provider = QRydProvider("MY_TOKEN")
```

Afterwards, you can choose a backend. Different backends are available that are capable of running ideal simulations of quantum circuits. An inclusion of noise models is planned for the future. You can either choose a backend emulating 30 qubits arranged in a 5x6 square lattice with nearest-neighbor connectivity

```python
backend = provider.get_backend("qryd_emu_localcomp_square")
```

or a backend emulating 30 qubits arranged in a triangle lattice with nearest-neighbor connectivity

```python
backend = provider.get_backend("qryd_emu_localcomp_triangle")
```

If you use these backends, Qiskit automatically transpiles arbitrary quantum circuits to comply with the native gate set and connectivity of the Rydberg platform. The backends are also available as variants where the compilation happens on our servers (`"qryd_emu_cloudcomp_square"` and `"qryd_emu_cloudcomp_triangle"`), using a decomposer developed by [HQS Quantum Simulations](https://quantumsimulations.de/).

After selecting a backend, you can run a circuit on the backend:

```python
from qiskit import QuantumCircuit, execute
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
job = execute(qc, backend, shots=200, optimization_level=3)
print(job.result().get_counts())
```

## Expert Options

The value of the phase shift of the [PCZ gate](https://arxiv.org/abs/2202.13849) can be modified before using the backend via:

```python
from qiskit_qryd_provider import PCZGate
PCZGate.set_pcz_theta(VALUE)
```

## License

The Qiskit QRyd Provider is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). 
