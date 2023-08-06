from qiskit.providers import JobV1 as Job
from qiskit.providers.jobstatus import JobStatus
from qiskit.providers import JobTimeoutError
from qiskit.providers import JobError
from qiskit.result import Result
import requests
import time


class QRydSimulatorJob(Job):
    _async = True

    def __init__(self, backend, job_url, token, options, circuit):
        super().__init__(backend, job_url.split("/")[-1])

        self._session = requests.Session()
        self._session.headers.update({"X-API-Key": token})
        self._job_url = job_url
        self._circuit = circuit
        self._memory = options["memory"]
        self._shots = options["shots"]

    def submit(self):
        raise NotImplementedError("Please use QRydSimulator.run() to submit a job.")

    def cancel(self):
        response = self._session.delete(self._job_url)
        if response.status_code == 200:
            return True
        else:
            return False

    def status(self):
        result = self._get_job_status(self._job_url, self._session)
        if result["status"] == "running":
            status = JobStatus.RUNNING
        elif result["status"] == "completed":
            status = JobStatus.DONE
        elif result["status"] == "pending":
            status = JobStatus.QUEUED
        elif result["status"] == "cancelled":
            status = JobStatus.CANCELLED
        elif result["status"] == "initializing" or result["status"] == "compiling":
            status = JobStatus.INITIALIZING
        elif result["status"] == "completing":
            status = JobStatus.VALIDATING
        else:
            status = JobStatus.ERROR
        return status

    def result(self, timeout=None, wait=0.5):
        result = self._wait_for_result(timeout, wait)
        return Result.from_dict(
            {
                "results": [
                    {
                        "success": True,
                        "metadata": {
                            "noise": result["noise"],
                            "method": result["method"],
                            "device": result["device"],
                            "num_qubits": result["num_qubits"],
                            "num_clbits": result["num_clbits"],
                            "fusion_max_qubits": result["fusion_max_qubits"],
                            "fusion_avg_qubits": result["fusion_avg_qubits"],
                            "fusion_generated_gates": result["fusion_generated_gates"],
                            "executed_single_qubit_gates": result[
                                "executed_single_qubit_gates"
                            ],
                            "executed_two_qubit_gates": result[
                                "executed_two_qubit_gates"
                            ],
                        },
                        "shots": self._shots,
                        "data": result["data"],
                        "time_taken": result["time_taken"],
                        "header": {
                            "memory_slots": self._circuit.num_clbits,
                            "name": self._circuit.name,
                        },
                    }
                ],
                "backend_name": self._backend.configuration().backend_name,
                "backend_version": self._backend.configuration().backend_version,
                "job_id": self._job_id,
                "qobj_id": id(self._circuit),
                "success": True,
            }
        )

    def _wait_for_result(self, timeout=None, wait=0.5):
        start_time = time.time()
        while True:
            elapsed = time.time() - start_time
            if timeout and elapsed >= timeout:
                raise JobTimeoutError("Timed out waiting for result")
            result = self._get_job_status(self._job_url, self._session)
            if result["status"] == "completed":
                break
            if result["status"] == "error":
                if result["msg"]:
                    raise JobError(f"Job error ({result['msg']})")
                else:
                    raise JobError("Job error")
            time.sleep(wait)
        return self._get_job_result(self._job_url, self._session)

    def _get_job_status(self, job_url, session):
        response = session.get(job_url + "/status")
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
        return response.json()

    def _get_job_result(self, job_url, session):
        response = session.get(job_url + "/result")
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
        return response.json()
