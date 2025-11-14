# Quantum Backends

## Overview

This directory provides an abstraction layer for executing quantum circuits on various backends, including local simulators and cloud-based quantum processing units (QPUs). The design allows algorithms to remain backend-agnostic, making it easy to switch between simulators and real hardware without modifying algorithm code.

## Architecture

### Base Interface

All backends implement the `QuantumBackend` abstract base class, which provides a consistent interface for:
- Executing circuits synchronously
- Submitting jobs asynchronously
- Retrieving job results
- Querying backend capabilities and properties

### Supported Backends

1. **Cirq Simulator** (`cirq_simulator.py`)
   - Local simulation using Cirq's built-in simulator
   - Fast, ideal for development and testing
   - No additional setup required

2. **AWS Braket** (`aws_braket.py`) - *Placeholder*
   - Support for AWS Braket devices (IonQ, Rigetti, Quantinuum, etc.)
   - Native Cirq circuit support
   - Requires AWS account and credentials

3. **Azure Quantum** (`azure_quantum.py`) - *Placeholder*
   - Support for Azure Quantum devices (Quantinuum, IonQ, etc.)
   - May require circuit conversion from Cirq to Qiskit
   - Requires Azure account and workspace setup

## Usage

### Basic Usage

```python
from quantum_backends import get_backend
import cirq

# Get default backend (reads from environment/config)
backend = get_backend()

# Create a circuit
circuit = cirq.Circuit(cirq.H(cirq.LineQubit(0)), cirq.measure(cirq.LineQubit(0)))

# Execute synchronously
result = backend.run(circuit, repetitions=1000)
print(result)
```

### Using Specific Backends

```python
from quantum_backends import create_backend, BackendType
from quantum_backends.config import BackendConfig

# Create a specific backend
config = BackendConfig(backend_type=BackendType.SIMULATOR)
backend = create_backend(config)

# Or use the factory function
backend = create_backend(BackendType.SIMULATOR)
```

### Asynchronous Job Submission

```python
# Submit a job (for QPU backends)
job_id = backend.submit_job(circuit, repetitions=1000)

# Later, retrieve results
result = backend.get_job_result(job_id)
```

## Configuration

Backend configuration can be provided via:
1. Environment variables (see `.env.example`)
2. Configuration file
3. Programmatic configuration via `BackendConfig`

### Environment Variables

```bash
QUANTUM_BACKEND=simulator  # Options: simulator, aws_braket, azure_quantum
QUANTUM_DEVICE=            # Device name/ARN for cloud backends
```

## Development Status

- ✅ **Cirq Simulator**: Fully implemented and tested
- 🚧 **AWS Braket**: Scaffolding in place, implementation pending AWS account setup
- 🚧 **Azure Quantum**: Scaffolding in place, implementation pending Azure account setup

## Future Enhancements

- Job queuing and retry logic
- Cost tracking and budgeting
- Circuit optimization and transpilation
- Noise model support for simulators
- Device capability checking
- Result caching

## See Also

- Quantum algorithms: [`../quantum_algorithms/`](../quantum_algorithms/)
- Quantum machine learning: [`../quantum_machine_learning/`](../quantum_machine_learning/)
- Tensor networks: [`../tensor_networks/`](../tensor_networks/)

