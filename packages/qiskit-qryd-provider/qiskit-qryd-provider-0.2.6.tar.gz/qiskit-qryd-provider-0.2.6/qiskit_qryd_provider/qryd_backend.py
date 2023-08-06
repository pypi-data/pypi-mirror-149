from qiskit.providers import BackendV1 as Backend
from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options
from math import pi
import warnings
import requests
from .qryd_job import QRydSimulatorJob
from .qryd_gates import PCZGate


class QRydSimulator(Backend):
    url_base = "https://api.qryddemo.itp3.uni-stuttgart.de/v1_0/jobs"

    def __init__(self, provider, lattice):
        si = 5
        sj = 6
        configuration = {
            "backend_version": "1.0.0",
            "n_qubits": si * sj,
            "basis_gates": ["p", "r", "rx", "ry", "pcz"],
            "simulator": True,
            "local": True,
            "conditional": False,
            "open_pulse": False,
            "memory": True,
            "max_shots": 2**18,
            "max_experiments": 1,
            "gates": [],
        }
        if lattice == "square_uncompiled":
            configuration["backend_name"] = "qryd_emu_cloudcomp_square"
            configuration["coupling_map"] = []

            # For examples of basis_gates see https://github.com/Qiskit/qiskit-aer/blob/bb47adcf2e49b1e486e9ed15b3d55b6c4a345b1b/qiskit/providers/aer/backends/backend_utils.py#L52  # noqa: B950
            configuration["basis_gates"] += ["cx", "rz", "u", "h", "swap", "cu1", "cz"]

        elif lattice == "triangle_uncompiled":
            configuration["backend_name"] = "qryd_emu_cloudcomp_triangle"
            configuration["coupling_map"] = []

            # For examples of basis_gates see https://github.com/Qiskit/qiskit-aer/blob/bb47adcf2e49b1e486e9ed15b3d55b6c4a345b1b/qiskit/providers/aer/backends/backend_utils.py#L52  # noqa: B950
            configuration["basis_gates"] += ["cx", "rz", "u", "h", "swap", "cu1", "cz"]

        elif lattice == "square":
            configuration["backend_name"] = "qryd_emu_localcomp_square"
            configuration["coupling_map"] = [
                [i + si * j, i + si * j + 1] for i in range(si - 1) for j in range(sj)
            ]
            configuration["coupling_map"] += [
                [i + si * j + 1, i + si * j] for i in range(si - 1) for j in range(sj)
            ]
            configuration["coupling_map"] += [
                [i + si * j, i + si * j + si] for i in range(si) for j in range(sj - 1)
            ]
            configuration["coupling_map"] += [
                [i + si * j + si, i + si * j] for i in range(si) for j in range(sj - 1)
            ]

        elif lattice == "triangle":
            configuration["backend_name"] = "qryd_emu_localcomp_triangle"
            configuration["coupling_map"] = [
                [i + si * j, i + si * j + 1] for i in range(si - 1) for j in range(sj)
            ]
            configuration["coupling_map"] += [
                [i + si * j + 1, i + si * j] for i in range(si - 1) for j in range(sj)
            ]
            configuration["coupling_map"] += [
                [i + si * j, i + si * j + si]
                for i in range(si)
                for j in range(0, sj - 1, 2)
            ]
            configuration["coupling_map"] += [
                [i + si * j + si, i + si * j]
                for i in range(si)
                for j in range(0, sj - 1, 2)
            ]
            configuration["coupling_map"] += [
                [i + si * j, i + si * j + si - 1]
                for i in range(1, si)
                for j in range(1, sj - 1, 2)
            ]
            configuration["coupling_map"] += [
                [i + si * j + si - 1, i + si * j]
                for i in range(1, si)
                for j in range(1, sj - 1, 2)
            ]
            configuration["coupling_map"] += [
                [i + si * j, i + si * j + si + 1]
                for i in range(si - 1)
                for j in range(0, sj - 1, 2)
            ]
            configuration["coupling_map"] += [
                [i + si * j + si + 1, i + si * j]
                for i in range(si - 1)
                for j in range(0, sj - 1, 2)
            ]
            configuration["coupling_map"] += [
                [i + si * j, i + si * j + si + 1 - 1]
                for i in range(si - 1 + 1)
                for j in range(1, sj - 1, 2)
            ]
            configuration["coupling_map"] += [
                [i + si * j + si + 1 - 1, i + si * j]
                for i in range(si - 1 + 1)
                for j in range(1, sj - 1, 2)
            ]

        else:
            raise RuntimeError("The lattice must either be triangle or square.")

        super().__init__(
            configuration=BackendConfiguration.from_dict(configuration),
            provider=provider,
        )

    @classmethod
    def _default_options(cls):
        return Options(
            shots=1024,
            memory=False,
            seed_simulator=None,
            parameter_binds=None,
            develop=False,
        )

    def set_option(self, key, value):
        if hasattr(self.options, key):
            if value is not None:
                setattr(self.options, key, value)
            else:
                setattr(self.options, key, getattr(self._default_options(), key))
        else:
            raise NotImplementedError(f'"{key}" is not a valid option.')

    def run(self, circuit, **kwargs):
        for kwarg in kwargs:
            if not hasattr(self.options, kwarg):
                warnings.warn(
                    "Option %s is not used by this backend." % kwarg,
                    UserWarning,
                    stacklevel=2,
                )

        options = {
            "develop": kwargs.get("develop", self.options.develop),
            "shots": kwargs.get("shots", self.options.shots),
            "memory": kwargs.get("memory", self.options.memory),
            "seed_simulator": kwargs.get("seed_simulator", self.options.seed_simulator),
            "parameter_binds": kwargs.get(
                "parameter_binds", self.options.parameter_binds
            ),
        }

        if options["parameter_binds"] is not None:
            warnings.warn(
                "Parameter binds are not yet supported.",
                UserWarning,
                stacklevel=2,
            )

        if options["memory"] is not False:
            warnings.warn(
                "Memory is not yet supported.",
                UserWarning,
                stacklevel=2,
            )

        if options["shots"] > self.configuration().max_shots:
            raise ValueError(
                f"The number of shots specified ({options['shots']}) exceeds "
                f"max_shots property of the backend ({self.configuration().max_shots})."
            )

        job_dict = self._convert_to_wire_format(circuit, options)
        job_handle = self._submit(job_dict, self._provider.token)
        job_url = job_handle.headers["Location"]

        return QRydSimulatorJob(self, job_url, self._provider.token, options, circuit)

    def _convert_to_wire_format(self, circuit, options):
        circuit_dict = {
            "ClassicalRegister": {
                "measurement": {
                    "constant_circuit": {
                        "definitions": [
                            {
                                "DefinitionBit": {
                                    "name": "ro",
                                    "length": len(circuit.clbits),
                                    "is_output": True,
                                }
                            }
                        ],
                        "operations": [],
                        "_roqoqo_version": {
                            "major_version": 0,
                            "minor_version": 11,
                        },
                    },
                },
            },
        }
        qubits_map = {bit: n for n, bit in enumerate(circuit.qubits)}
        clbits_map = {bit: n for n, bit in enumerate(circuit.clbits)}
        for instruction in circuit.data:
            inst = instruction[0]
            params = [param for param in inst.params]
            qubits = [qubits_map[bit] for bit in instruction[1]]
            clbits = [clbits_map[bit] for bit in instruction[2]]

            if inst.name == "barrier":
                continue
            elif inst.name == "measure":
                assert len(qubits) == len(clbits)
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "PragmaRepeatedMeasurement": {
                            "readout": "ro",
                            "number_measurements": options["shots"],
                            "qubit_mapping": dict(zip(qubits, clbits)),
                        }
                    }
                )
            elif inst.name == "p":
                assert len(qubits) == 1
                assert len(params) == 1
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "PhaseShiftState1": {
                            "qubit": qubits[0],
                            "theta": float(params[0]),
                        }
                    }
                )
            elif inst.name == "rx":
                assert len(qubits) == 1
                assert len(params) == 1
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "RotateX": {
                            "qubit": qubits[0],
                            "theta": float(params[0]),
                        }
                    }
                )
            elif inst.name == "ry":
                assert len(qubits) == 1
                assert len(params) == 1
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "RotateY": {
                            "qubit": qubits[0],
                            "theta": float(params[0]),
                        }
                    }
                )
            elif inst.name == "r":
                assert len(qubits) == 1
                assert len(params) == 2
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "RotateXY": {
                            "qubit": qubits[0],
                            "theta": float(params[0]),
                            "phi": float(params[1]),
                        }
                    }
                )
            elif inst.name == "pcz":
                assert len(qubits) == 2
                assert len(params) == 0
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "PhaseShiftedControlledZ": {
                            "control": qubits[0],
                            "target": qubits[1],
                            "phi": float(PCZGate().get_pcz_theta()),
                        }
                    }
                )
            elif inst.name == "cx":
                assert len(qubits) == 2
                assert len(params) == 0
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "CNOT": {
                            "control": qubits[0],
                            "target": qubits[1],
                        }
                    }
                )
            elif inst.name == "swap":
                assert len(qubits) == 2
                assert len(params) == 0
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "SWAP": {
                            "control": qubits[0],
                            "target": qubits[1],
                        }
                    }
                )
            elif inst.name == "cu1":
                assert len(qubits) == 2
                assert len(params) == 1
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "ControlledPhaseShift": {
                            "control": qubits[0],
                            "target": qubits[1],
                            "theta": float(params[0]),
                        }
                    }
                )
            elif inst.name == "cz":
                assert len(qubits) == 2
                assert len(params) == 0
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "ControlledPauliZ": {
                            "control": qubits[0],
                            "target": qubits[1],
                        }
                    }
                )
            elif inst.name == "rz":
                assert len(qubits) == 1
                assert len(params) == 1
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "RotateZ": {
                            "qubit": qubits[0],
                            "theta": float(params[0]),
                        }
                    }
                )
            elif inst.name == "h":
                assert len(qubits) == 1
                assert len(params) == 0
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ].append(
                    {
                        "Hadamard": {
                            "qubit": qubits[0],
                        }
                    }
                )
            elif inst.name == "u":
                assert len(qubits) == 1
                assert len(params) == 3
                theta = float(params[0])
                phi = float(params[1])
                lam = float(params[2])
                circuit_dict["ClassicalRegister"]["measurement"]["constant_circuit"][
                    "operations"
                ] += [
                    {
                        "RotateZ": {
                            "qubit": qubits[0],
                            "theta": lam - pi / 2,
                        }
                    },
                    {
                        "RotateX": {
                            "qubit": qubits[0],
                            "theta": theta,
                        }
                    },
                    {
                        "RotateZ": {
                            "qubit": qubits[0],
                            "theta": phi + pi / 2,
                        }
                    },
                ]
            else:
                raise RuntimeError("Operation '%s' not supported." % inst.name)

        job_dict = {
            "backend": self.configuration().backend_name,
            "develop": options["develop"],
            "seed": options["seed_simulator"],
            "pcz_theta": float(PCZGate().get_pcz_theta()),
            "program": circuit_dict,
        }
        return job_dict

    def _submit(self, job_dict, token):
        response = requests.post(
            self.url_base, headers={"X-API-Key": token}, json=job_dict
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            try:
                error = requests.HTTPError(
                    f"{error} ({error.response.json()['detail']})"
                )
            except BaseException:
                pass
            raise error
        if response.status_code != 201:
            raise RuntimeError("Error creating a new job on the QRydDemo server")
        return response
