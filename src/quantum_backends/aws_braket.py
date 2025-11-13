# Quantum Backends: AWS Braket backend (placeholder)
# Author: John Graham Reynolds
# *************************************************************

"""
AWS Braket Backend - Placeholder Implementation

This module will provide integration with AWS Braket for executing quantum
circuits on cloud-based QPUs (IonQ, Rigetti, Quantinuum, etc.).

Implementation Status: Scaffolding only
- Requires AWS account setup
- Requires AWS credentials configuration
- Requires amazon-braket-sdk installation

When implemented, this backend will support:
- Native Cirq circuit execution
- Asynchronous job submission and retrieval
- Multiple device types (IonQ, Rigetti, Quantinuum, etc.)
- Job cost tracking
"""

from typing import Dict, Any
import cirq
from .base import QuantumBackend
from .config import BackendConfig


class AWSBraketBackend(QuantumBackend):
    """AWS Braket backend for cloud-based QPU execution.
    
    This backend provides integration with AWS Braket for executing quantum
    circuits on real hardware. Implementation is pending AWS account setup.
    
    Status: Placeholder - Not yet implemented
    """
    
    def __init__(self, config: BackendConfig):
        """Initialize the AWS Braket backend.
        
        Args:
            config: Backend configuration with AWS-specific parameters
        """
        self.config = config
        self._device_name = config.device_name or "aws_braket_placeholder"
        raise NotImplementedError(
            "AWS Braket backend is not yet implemented. "
            "This requires AWS account setup and amazon-braket-sdk installation. "
            "See README.md for implementation roadmap."
        )
    
    def run(self, circuit: cirq.Circuit, repetitions: int = 1000, **kwargs) -> cirq.Result:
        """Execute a circuit synchronously on AWS Braket.
        
        Note: This is a placeholder. Implementation pending.
        """
        raise NotImplementedError("AWS Braket backend is not yet implemented")
    
    def submit_job(self, circuit: cirq.Circuit, repetitions: int = 1000, **kwargs) -> str:
        """Submit a circuit for asynchronous execution on AWS Braket.
        
        Note: This is a placeholder. Implementation pending.
        """
        raise NotImplementedError("AWS Braket backend is not yet implemented")
    
    def get_job_result(self, job_id: str, **kwargs) -> cirq.Result:
        """Retrieve results for a previously submitted job.
        
        Note: This is a placeholder. Implementation pending.
        """
        raise NotImplementedError("AWS Braket backend is not yet implemented")
    
    @property
    def device_name(self) -> str:
        """Return the device name."""
        return self._device_name
    
    @property
    def is_simulator(self) -> bool:
        """Return whether this backend is a simulator."""
        return False  # AWS Braket provides real QPUs
    
    def supports_asynchronous_execution(self) -> bool:
        """Check if this backend supports asynchronous execution."""
        return True  # AWS Braket supports async execution


