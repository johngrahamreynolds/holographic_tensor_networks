# Quantum Backends: Azure Quantum backend (placeholder)
# Author: John Graham Reynolds
# *************************************************************

"""
Azure Quantum Backend - Placeholder Implementation

This module will provide integration with Azure Quantum for executing quantum
circuits on cloud-based QPUs (Quantinuum, IonQ, etc.).

Implementation Status: Scaffolding only
- Requires Azure account setup
- Requires Azure Quantum workspace creation
- Requires azure-quantum package installation
- May require Cirq-to-Qiskit conversion for circuit execution

When implemented, this backend will support:
- Circuit execution on Azure Quantum devices
- Asynchronous job submission and retrieval
- Multiple device types (Quantinuum, IonQ, etc.)
- Job cost tracking
"""

from typing import Dict, Any
import cirq
from .base import QuantumBackend
from .config import BackendConfig


class AzureQuantumBackend(QuantumBackend):
    """Azure Quantum backend for cloud-based QPU execution.
    
    This backend provides integration with Azure Quantum for executing quantum
    circuits on real hardware. Implementation is pending Azure account setup.
    
    Note: Azure Quantum primarily uses Qiskit, so Cirq circuits may need
    conversion. This will be handled by the backend implementation.
    
    Status: Placeholder - Not yet implemented
    """
    
    def __init__(self, config: BackendConfig):
        """Initialize the Azure Quantum backend.
        
        Args:
            config: Backend configuration with Azure-specific parameters
        """
        self.config = config
        self._device_name = config.device_name or "azure_quantum_placeholder"
        raise NotImplementedError(
            "Azure Quantum backend is not yet implemented. "
            "This requires Azure account setup, workspace creation, and "
            "azure-quantum package installation. "
            "See README.md for implementation roadmap."
        )
    
    def run(self, circuit: cirq.Circuit, repetitions: int = 1000, **kwargs) -> cirq.Result:
        """Execute a circuit synchronously on Azure Quantum.
        
        Note: This is a placeholder. Implementation pending.
        """
        raise NotImplementedError("Azure Quantum backend is not yet implemented")
    
    def submit_job(self, circuit: cirq.Circuit, repetitions: int = 1000, **kwargs) -> str:
        """Submit a circuit for asynchronous execution on Azure Quantum.
        
        Note: This is a placeholder. Implementation pending.
        """
        raise NotImplementedError("Azure Quantum backend is not yet implemented")
    
    def get_job_result(self, job_id: str, **kwargs) -> cirq.Result:
        """Retrieve results for a previously submitted job.
        
        Note: This is a placeholder. Implementation pending.
        """
        raise NotImplementedError("Azure Quantum backend is not yet implemented")
    
    @property
    def device_name(self) -> str:
        """Return the device name."""
        return self._device_name
    
    @property
    def is_simulator(self) -> bool:
        """Return whether this backend is a simulator."""
        return False  # Azure Quantum provides real QPUs
    
    def supports_asynchronous_execution(self) -> bool:
        """Check if this backend supports asynchronous execution."""
        return True  # Azure Quantum supports async execution


