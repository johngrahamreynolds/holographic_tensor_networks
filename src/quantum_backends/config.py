# Quantum Backends: Configuration management
# Author: John Graham Reynolds
# *************************************************************

import os
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class BackendType(Enum):
    """Enumeration of supported backend types."""
    SIMULATOR = "simulator"
    AWS_BRAKET = "aws_braket"
    AZURE_QUANTUM = "azure_quantum"


@dataclass
class BackendConfig:
    """Configuration for quantum computing backends.
    
    This class holds configuration parameters for different backend types.
    Credentials and sensitive information should be loaded from environment
    variables rather than stored directly in configuration objects.
    """
    backend_type: BackendType = BackendType.SIMULATOR
    device_name: Optional[str] = None
    
    # AWS Braket configuration
    aws_region: Optional[str] = None
    s3_bucket: Optional[str] = None
    aws_profile: Optional[str] = None
    
    # Azure Quantum configuration
    azure_subscription_id: Optional[str] = None
    azure_resource_group: Optional[str] = None
    azure_workspace_name: Optional[str] = None
    
    # Generic settings
    default_repetitions: int = 1000
    timeout_seconds: Optional[int] = None
    
    @classmethod
    def from_env(cls) -> 'BackendConfig':
        """Load configuration from environment variables.
        
        Environment variables:
            QUANTUM_BACKEND: Backend type (simulator, aws_braket, azure_quantum)
            QUANTUM_DEVICE: Device name/ARN for cloud backends
            AWS_REGION: AWS region for Braket (default: us-east-1)
            AWS_S3_BUCKET: S3 bucket for Braket job results
            AWS_PROFILE: AWS profile name for credentials
            AZURE_SUBSCRIPTION_ID: Azure subscription ID
            AZURE_RESOURCE_GROUP: Azure resource group name
            AZURE_WORKSPACE_NAME: Azure Quantum workspace name
            
        Returns:
            BackendConfig instance configured from environment
        """
        backend_str = os.getenv('QUANTUM_BACKEND', 'simulator').lower()
        try:
            backend_type = BackendType(backend_str)
        except ValueError:
            backend_type = BackendType.SIMULATOR
        
        return cls(
            backend_type=backend_type,
            device_name=os.getenv('QUANTUM_DEVICE'),
            aws_region=os.getenv('AWS_REGION', 'us-east-1'),
            s3_bucket=os.getenv('AWS_S3_BUCKET'),
            aws_profile=os.getenv('AWS_PROFILE'),
            azure_subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID'),
            azure_resource_group=os.getenv('AZURE_RESOURCE_GROUP'),
            azure_workspace_name=os.getenv('AZURE_WORKSPACE_NAME'),
            default_repetitions=int(os.getenv('QUANTUM_DEFAULT_REPETITIONS', '1000')),
            timeout_seconds=int(os.getenv('QUANTUM_TIMEOUT_SECONDS', '3600')) if os.getenv('QUANTUM_TIMEOUT_SECONDS') else None,
        )
    
    def validate(self) -> None:
        """Validate configuration parameters.
        
        Raises:
            ValueError: If required parameters are missing for the selected backend type
        """
        if self.backend_type == BackendType.AWS_BRAKET:
            if not self.device_name:
                raise ValueError("device_name is required for AWS Braket backend")
            if not self.s3_bucket:
                raise ValueError("s3_bucket is required for AWS Braket backend")
        
        elif self.backend_type == BackendType.AZURE_QUANTUM:
            if not self.azure_subscription_id:
                raise ValueError("azure_subscription_id is required for Azure Quantum backend")
            if not self.azure_resource_group:
                raise ValueError("azure_resource_group is required for Azure Quantum backend")
            if not self.azure_workspace_name:
                raise ValueError("azure_workspace_name is required for Azure Quantum backend")


