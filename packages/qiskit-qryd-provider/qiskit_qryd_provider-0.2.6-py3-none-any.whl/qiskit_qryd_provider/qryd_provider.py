from qiskit.providers import ProviderV1 as Provider
from qiskit.providers.providerutils import filter_backends
from .qryd_backend import QRydSimulator


class QRydProvider(Provider):
    def __init__(self, token):
        super().__init__()
        self.token = token

    def backends(self, name=None, filters=None, **kwargs):
        backends = [
            QRydSimulator(provider=self, lattice="triangle"),
            QRydSimulator(provider=self, lattice="triangle_uncompiled"),
            QRydSimulator(provider=self, lattice="square"),
            QRydSimulator(provider=self, lattice="square_uncompiled"),
        ]
        if name:
            backends = [backend for backend in backends if backend.name() == name]
        return filter_backends(backends, filters=filters, **kwargs)
