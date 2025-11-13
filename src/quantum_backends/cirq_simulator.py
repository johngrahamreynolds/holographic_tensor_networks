# Quantum Backends: Cirq Simulator backend
# Author: John Graham Reynolds
# *************************************************************

from typing import Dict, Any, Optional
import cirq
from .base import QuantumBackend
from .config import BackendConfig, BackendType


class CirqSimulatorBackend(QuantumBackend):
    """Local Cirq simulator backend.
    
    This backend uses Cirq's built-in simulator for fast local execution.
    It's ideal for development, testing, and small-scale experiments.
    No additional setup or credentials are required.
    """
    
    def __init__(self, config: Optional[BackendConfig] = None):
        """Initialize the Cirq simulator backend.
        
        Args:
            config: Backend configuration (optional, uses defaults if not provided)
        """
        self.config = config or BackendConfig(backend_type=BackendType.SIMULATOR)
        self._simulator = cirq.Simulator()
        self._device_name = "cirq_simulator"
    
    def run(self, circuit: cirq.Circuit, repetitions: int = 1000, **kwargs) -> cirq.Result:
        """Execute a circuit synchronously using the Cirq simulator.
        
        Args:
            circuit: The quantum circuit to execute
            repetitions: Number of times to run the circuit (shots) (defaults to `default_repetitions` in the config, then to 1000 if not specified)
            **kwargs: Additional parameters (passed to simulator.run)
            
        Returns:
            cirq.Result object containing measurement results
        """
        
        if self.config.default_repetitions is not None:
            repetitions = self.config.default_repetitions
        
        return self._simulator.run(circuit, repetitions=repetitions, **kwargs)
    
    def submit_job(self, circuit: cirq.Circuit, repetitions: int = 1000, **kwargs) -> str:
        """Submit a circuit for asynchronous execution.
        
        Note: For the local simulator, this is just a synchronous execution
        wrapped to match the async interface. The job completes immediately.
        
        Args:
            circuit: The quantum circuit to execute
            repetitions: Number of times to run the circuit (shots)
            **kwargs: Additional parameters
            
        Returns:
            Job ID string (for simulator, this is just a placeholder)
        """
        # For simulator, execute synchronously and store result
        # In a real implementation, this would queue the job
        result = self.run(circuit, repetitions=repetitions, **kwargs)
        # Store result with a simple job ID (in practice, use proper job storage)
        job_id = f"simulator_job_{id(result)}"
        self._job_results = getattr(self, '_job_results', {})
        self._job_results[job_id] = result
        return job_id
    
    def get_job_result(self, job_id: str, **kwargs) -> cirq.Result:
        """Retrieve results for a previously submitted job.
        
        Args:
            job_id: The job ID returned from submit_job
            **kwargs: Additional parameters (unused for simulator)
            
        Returns:
            cirq.Result object containing measurement results
            
        Raises:
            ValueError: If job_id is invalid
        """
        self._job_results = getattr(self, '_job_results', {})
        if job_id not in self._job_results:
            raise ValueError(f"Job ID {job_id} not found")
        return self._job_results[job_id]
    
    @property
    def device_name(self) -> str:
        """Return the device name."""
        return self._device_name
    
    @property
    def is_simulator(self) -> bool:
        """Return whether this backend is a simulator."""
        return True
    
    def supports_asynchronous_execution(self) -> bool:
        """Check if this backend supports asynchronous execution.
        
        For the simulator, async is supported but executes synchronously.
        """
        return True
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get information about the device capabilities.
        
        Returns:
            Dictionary containing device information
        """
        info = super().get_device_info()
        info.update({
            'simulator_type': 'cirq',
            'qubit_limit': None,  # Simulator has no practical qubit limit
        })
        return info

