class ElgasError(Exception):
    """General Elgas error"""


class LocalElgasProtocolError(ElgasError):
    """Protocol error"""


class CommunicationError(ElgasError):
    """Communication error"""


class WrongPasswordError(ElgasError):
    # Bit 0
    """Wrong password for action was used or password switch is not turned on"""


class SettingArchiveFull(ElgasError):
    # Bit 1
    """Archive of settings is full"""


class SwitchOff(ElgasError):
    # Bit 2
    """Switch is off"""


class BlockedBuffer(ElgasError):
    # Bit 3
    """Blocked buffer"""


class DataError(ElgasError):
    # Bit 4
    """Data error"""


class CipherKeyError(ElgasError):
    # Bit 5
    """Wrong key for encryption of decryption"""


class WrongEncryptionKeysError(ElgasError):
    # Bit 6
    """Wrong encryption keys"""


class WriteError(ElgasError):
    # Bit 7
    """Write Error"""
