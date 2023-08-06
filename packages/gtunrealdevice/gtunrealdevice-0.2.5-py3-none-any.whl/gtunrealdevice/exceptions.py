"""Module containing the exception class for gtunrealdevice."""


class WrapperError(Exception):
    """Use to capture error for using invalid decorator."""


class DevicesInfoError(Exception):
    """Use to capture devices info"""


class UnrealDeviceError(Exception):
    """Use to capture error for creating GTUnrealDevice."""


class UnrealDeviceConnectionError(UnrealDeviceError):
    """Use to capture error when GTUnrealDevice establishes connection."""


class UnrealDeviceOfflineError(UnrealDeviceError):
    """Use to capture error when GTUnrealDevice is offline."""


class SerializedError(Exception):
    """Use to capture error for serialized file."""


class InvalidSerializedFile(SerializedError):
    """Use to capture error for serialized file."""


class InvalidSerializedInstance(SerializedError):
    """Use to capture error for serialized file."""
