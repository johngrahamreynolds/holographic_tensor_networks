# Quantum Backends: Abstract base class for quantum computing backends
# Author: John Graham Reynolds
# *************************************************************

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import cirq


class QuantumBackend(ABC):
    """Abstract base class for quantum computing backends.
    
    This class defines the interface that all quantum backends must implement,
    allowing algorithms to remain backend-agnostic and easily switch between
    simulators and real hardware.
    """
    
    @abstractmethod
    def run(self, circuit: cirq.Circuit, repetitions: int = 1000, **kwargs) -> cirq.Result:
        """Execute a circuit synchronously and return results.
        
        Args:
            circuit: The quantum circuit to execute
            repetitions: Number of times to run the circuit (shots)
            **kwargs: Additional backend-specific parameters
            
        Returns:
            cirq.Result object containing measurement results
            
        Raises:
            NotImplementedError: If synchronous execution is not supported
        """
        raise NotImplementedError(
            "This method must be implemented by a concrete backend class. "
            "See CirqSimulatorBackend, AWSBraketBackend, or AzureQuantumBackend for examples."
        )
    
    @abstractmethod
    def submit_job(self, circuit: cirq.Circuit, repetitions: int = 1000, **kwargs) -> str:
        """Submit a circuit for asynchronous execution.
        
        Args:
            circuit: The quantum circuit to execute
            repetitions: Number of times to run the circuit (shots)
            **kwargs: Additional backend-specific parameters
            
        Returns:
            Job ID string that can be used to retrieve results later
            
        Raises:
            NotImplementedError: If async execution is not supported
        """
        raise NotImplementedError(
            "This method must be implemented by a concrete backend class. "
            "See CirqSimulatorBackend, AWSBraketBackend, or AzureQuantumBackend for examples."
        )
    
    @abstractmethod
    def get_job_result(self, job_id: str, **kwargs) -> cirq.Result:
        """Retrieve results for a previously submitted job.
        
        Args:
            job_id: The job ID returned from submit_job
            **kwargs: Additional backend-specific parameters
            
        Returns:
            cirq.Result object containing measurement results
            
        Raises:
            ValueError: If job_id is invalid
            RuntimeError: If job is not yet complete or failed
        """
        raise NotImplementedError(
            "This method must be implemented by a concrete backend class. "
            "See CirqSimulatorBackend, AWSBraketBackend, or AzureQuantumBackend for examples."
        )
    
    @property
    @abstractmethod
    def device_name(self) -> str:
        """Return the device name or identifier."""
        raise NotImplementedError(
            "This property must be implemented by a concrete backend class. "
            "See CirqSimulatorBackend, AWSBraketBackend, or AzureQuantumBackend for examples."
        )
    
    @property
    @abstractmethod
    def is_simulator(self) -> bool:
        """Return whether this backend is a simulator or real hardware."""
        raise NotImplementedError(
            "This property must be implemented by a concrete backend class. "
            "See CirqSimulatorBackend, AWSBraketBackend, or AzureQuantumBackend for examples."
        )
    
    def supports_synchronous_execution(self) -> bool:
        """Check if this backend supports synchronous execution.
        
        Returns:
            True if run() is supported, False otherwise
        """
        return True
    
    def supports_asynchronous_execution(self) -> bool:
        """Check if this backend supports asynchronous execution.
        
        Returns:
            True if submit_job() is supported, False otherwise
        """
        return False
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get information about the device capabilities.
        
        Returns:
            Dictionary containing device information (qubit count, connectivity, etc.)
        """
        return {
            'device_name': self.device_name,
            'is_simulator': self.is_simulator,
            'supports_sync': self.supports_synchronous_execution(),
            'supports_async': self.supports_asynchronous_execution(),
        }


