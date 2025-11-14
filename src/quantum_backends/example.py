# Quantum Backends: Example usage
# Author: John Graham Reynolds
# *************************************************************

"""
Example usage of the quantum backends abstraction layer.

This module demonstrates how to use the quantum backends to execute
circuits on different backends (Cirq simulator, AWS Braket, Azure Quantum).
"""

import cirq
from quantum_backends.factory import get_backend, create_backend
from quantum_backends.config import BackendType, BackendConfig


def example_basic_usage():
    """Example: Basic usage with default backend (simulator)."""
    # Get default backend (reads from environment or defaults to the Cirq simulator)
    backend = get_backend()
    
    # Create a simple circuit
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit([
        cirq.H(qubit),
        cirq.measure(qubit, key='result')
    ])
    
    # Execute the circuit
    result = backend.run(circuit, repetitions=1000)
    
    # Print results
    print(f"Device: {backend.device_name}")
    print(f"Is simulator: {backend.is_simulator}")
    print(f"Results: {result.histogram(key='result')}")
    
    return result


def example_explicit_backend():
    """Example: Explicitly create a simulator backend."""
    # Create simulator backend explicitly
    config = BackendConfig(backend_type=BackendType.SIMULATOR)
    backend = create_backend(config)
    
    # Or use the factory function directly
    backend = create_backend(backend_type=BackendType.SIMULATOR)
    
    # Create and run a circuit
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit([
        cirq.X(qubit),
        cirq.measure(qubit, key='result')
    ])
    
    result = backend.run(circuit, repetitions=100)
    print(f"Results: {result.histogram(key='result')}")
    
    return result


def example_async_execution():
    """Example: Asynchronous job submission (for simulator)."""
    backend = get_backend()
    
    # Create a circuit
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.measure(qubits, key='result')
    ])
    
    # Submit job asynchronously
    job_id = backend.submit_job(circuit, repetitions=1000)
    print(f"Submitted job: {job_id}")
    
    # Retrieve results
    result = backend.get_job_result(job_id)
    print(f"Results: {result.histogram(key='result')}")
    
    return result


def example_device_info():
    """Example: Query device information."""
    backend = get_backend()
    
    # Get device information
    info = backend.get_device_info()
    print(f"Device info: {info}")
    
    # Check capabilities
    print(f"Supports sync execution: {backend.supports_synchronous_execution()}")
    print(f"Supports async execution: {backend.supports_asynchronous_execution()}")
    
    return info


if __name__ == "__main__":
    print("Example: Basic Usage")
    print("=" * 50)
    example_basic_usage()
    print()
    
    print("Example: Explicit Backend")
    print("=" * 50)
    example_explicit_backend()
    print()
    
    print("Example: Async Execution")
    print("=" * 50)
    example_async_execution()
    print()
    
    print("Example: Device Info")
    print("=" * 50)
    example_device_info()


