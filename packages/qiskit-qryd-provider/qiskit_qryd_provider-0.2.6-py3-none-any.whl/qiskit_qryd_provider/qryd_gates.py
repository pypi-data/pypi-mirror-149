from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import CZGate, CXGate
from qiskit.quantum_info import Kraus
from cmath import exp


class PCZGate(Gate):
    def __init__(self, label=None):
        super().__init__("pcz", 2, [], label=label)

    def _define(self):
        qc = QuantumCircuit(2)
        qc.u(0, 0, self._theta, 0)
        qc.u(0, 0, self._theta, 1)
        qc.cz(0, 1)
        self.definition = qc

    def to_matrix(self):
        return [
            [1, 0, 0, 0],
            [0, exp(1j * self._theta), 0, 0],
            [0, 0, exp(1j * self._theta), 0],
            [0, 0, 0, -exp(2j * self._theta)],
        ]

    def to_kraus(self):
        return self._kraus

    @classmethod
    def set_pcz_theta(cls, theta):
        cls._theta = theta

        # Reset equivalence library
        default = []
        for c in SessionEquivalenceLibrary.get_entry(CXGate()):
            if not c.get_instructions("pcz"):
                default.append(c)
        SessionEquivalenceLibrary.set_entry(CXGate(), default)

        default = []
        for c in SessionEquivalenceLibrary.get_entry(CZGate()):
            if not c.get_instructions("pcz"):
                default.append(c)
        SessionEquivalenceLibrary.set_entry(CZGate(), default)

        # Attach new decomposition to the equivalence library
        def_pcz_cz = QuantumCircuit(2)
        def_pcz_cz.append(PCZGate(), [0, 1])
        def_pcz_cz.u(0, 0, -cls._theta, 0)
        def_pcz_cz.u(0, 0, -cls._theta, 1)
        SessionEquivalenceLibrary.add_equivalence(CZGate(), def_pcz_cz)

        def_pcz_cx = QuantumCircuit(2)
        def_pcz_cx.h(1)
        def_pcz_cx.append(PCZGate(), [0, 1])
        def_pcz_cx.u(0, 0, -cls._theta, 0)
        def_pcz_cx.u(0, 0, -cls._theta, 1)
        def_pcz_cx.h(1)
        SessionEquivalenceLibrary.add_equivalence(CXGate(), def_pcz_cx)

    @classmethod
    def get_pcz_theta(cls):
        return cls._theta

    @classmethod
    def set_pcz_kraus(cls, kraus):
        if kraus is not None:
            cls._kraus = Kraus(kraus).to_instruction()
        else:
            cls._kraus = None


PCZGate.set_pcz_theta(2.13)
PCZGate.set_pcz_kraus(None)
