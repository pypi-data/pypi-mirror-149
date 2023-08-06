import random
from enum import IntEnum

import attr
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from elgas import utils


class EncryptionKeyId(IntEnum):
    FACTORY = 1
    TEMPORARY = 2
    ADMINISTRATOR = 3
    MAINTENANCE = 4
    USER_1 = 5
    USER_2 = 6
    USER_3 = 7


def data_padding(data: bytes):
    """
    Data needs to be padded so that data + crc is a multiple of 16 bits.
    So multiple of 2 bytes -> an even number of bytes.
    CRC is always 2 bytes so does not contribute to the evenness.

    Theis: there is a mistake in the documentation and it should be 16 bytes of
    padding and not 16 bits. this would actually give you a proper length data to
    do AES-ECB and that is why is says "no-padding".
    """
    rest = (len(data) + 2) % 16  # +2 is crc
    if not rest:
        return b""
    else:
        to_pad = 16 - rest
        padding = bytearray()
        for _ in range(0, to_pad):
            padding.append(random.randint(0, 125))

        return bytes(padding)


@attr.s(auto_attribs=True)
class CipherContext:
    key_id: EncryptionKeyId
    key: bytes

    def crc(self, data: bytes):
        for_crc = bytearray()
        for_crc.extend(len(data).to_bytes(2, "little"))  # Lenght of original data!
        for_crc.append(self.key_id)
        for_crc.extend(data)
        for_crc.extend(data_padding(data))
        return utils.calculate_crc(for_crc)

    def encrypt(self, data: bytes):
        for_crc = bytearray()
        for_crc.extend(len(data).to_bytes(2, "little"))
        for_crc.append(self.key_id)
        padded_data = data_padding(data)
        for_crc.extend(data)
        for_crc.extend(padded_data)
        crc = utils.calculate_crc(for_crc)
        unencrypted = for_crc + crc.to_bytes(2, "big")
        # we then encrypt only the data part + crc.
        header = unencrypted[:3]
        to_cipher = unencrypted[3:]

        cipher_text = encrypt(to_cipher, self.key, self.key)
        return header + cipher_text

    def decrypt(self, in_data: bytes):
        header = in_data[:3]
        encrypted = in_data[3:]
        original_length = int.from_bytes(header[:2], "little")
        key_id = header[2]
        assert key_id == self.key_id
        decrypted_data = decrypt(encrypted, self.key, self.key)
        crc = decrypted_data[-2:]
        for_crc = bytearray()
        for_crc.extend(original_length.to_bytes(2, "little"))
        for_crc.append(key_id)
        for_crc.extend(decrypted_data[:-2])
        crc = utils.calculate_crc(for_crc).to_bytes(2, "big")
        correct_crc = decrypted_data[-2:]
        if not crc == correct_crc:
            raise ValueError(
                f"Incorrect CRC in encrypted data. Got {crc} should be {correct_crc} "
            )
        original_data = decrypted_data[:original_length]
        return original_data


def encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    encryptor = Cipher(
        algorithms.AES(key), modes.CBC(initialization_vector=iv)
    ).encryptor()
    cipher_text = encryptor.update(data) + encryptor.finalize()
    return cipher_text


def decrypt(cipher_text: bytes, key: bytes, iv: bytes):
    decryptor = Cipher(
        algorithms.AES(key), modes.CBC(initialization_vector=iv)
    ).decryptor()
    decrypted_text = decryptor.update(cipher_text) + decryptor.finalize()
    return decrypted_text
