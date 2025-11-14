# Quantum Backends: Factory functions for creating backends
# Author: John Graham Reynolds
# *************************************************************

from typing import Optional
from .base import QuantumBackend
from .config import BackendConfig, BackendType
from .cirq_simulator import CirqSimulatorBackend


def create_backend(config: Optional[BackendConfig] = None, backend_type: Optional[BackendType] = None) -> QuantumBackend:
    """Create a quantum backend instance.
    
    Args:
        config: Backend configuration (if None, loads from environment)
        backend_type: Backend type (if provided, overrides config)
        
    Returns:
        QuantumBackend instance
        
    Raises:
        ValueError: If backend type is not supported
        ValueError: If configuration is invalid
    """
    if config is None:
        config = BackendConfig.from_env()
    
    if backend_type is not None:
        config.backend_type = backend_type
    
    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        # For simulator, validation is lenient
        if config.backend_type != BackendType.SIMULATOR:
            raise
    
    # Create backend based on type
    if config.backend_type == BackendType.SIMULATOR:
        return CirqSimulatorBackend(config)
    
    elif config.backend_type == BackendType.AWS_BRAKET:
        # Import here to avoid dependency if not using AWS
        try:
            from .aws_braket import AWSBraketBackend
            return AWSBraketBackend(config)
        except ImportError:
            raise ValueError(
                "AWS Braket backend requires amazon-braket-sdk. "
                "Install it with: pip install amazon-braket-sdk"
            )
        except NotImplementedError as e:
            raise NotImplementedError(
                f"AWS Braket backend is not yet implemented: {e}. "
                "See README.md for implementation roadmap."
            )
    
    elif config.backend_type == BackendType.AZURE_QUANTUM:
        # Import here to avoid dependency if not using Azure
        try:
            from .azure_quantum import AzureQuantumBackend
            return AzureQuantumBackend(config)
        except ImportError:
            raise ValueError(
                "Azure Quantum backend requires azure-quantum. "
                "Install it with: pip install azure-quantum"
            )
        except NotImplementedError as e:
            raise NotImplementedError(
                f"Azure Quantum backend is not yet implemented: {e}. "
                "See README.md for implementation roadmap."
            )
    
    else:
        raise ValueError(f"Unsupported backend type: {config.backend_type}")


def get_backend() -> QuantumBackend:
    """Get the default quantum backend.
    
    This function loads the backend configuration from environment variables
    and creates the appropriate backend instance.
    
    Returns:
        QuantumBackend instance configured from environment
        
    Example:
        >>> backend = get_backend()
        >>> result = backend.run(circuit, repetitions=1000)
    """
    config = BackendConfig.from_env()
    return create_backend(config)

