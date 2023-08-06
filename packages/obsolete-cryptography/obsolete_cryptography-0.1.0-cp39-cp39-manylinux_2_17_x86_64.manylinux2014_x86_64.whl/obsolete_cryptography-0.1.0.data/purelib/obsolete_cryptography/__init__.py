#!/usr/bin/env python3

from typing import Set, Union, TypedDict, Optional

from . import mcrypt
from . import mhash


class CipherProperty(TypedDict):
    block_size: int
    max_key_size: int
    accepted_key_sizes: Set[int]


class CipherModule:
    '''
    The cipher module partially compliant with PEP-272. The constructor is not
    fully compliant with PEP-272 due to how mcrypt is designed.
    '''
    algorithms_available: Set[str] = mcrypt.list_algorithms()
    modes_available: Set[str] = mcrypt.list_modes()

    _cipher_name: str
    _properties: CipherProperty
    _block_size: int
    _key_size: Optional[int]

    def __init__(self, cipher_name: str):
        if cipher_name not in self.algorithms_available:
            raise ValueError(f'Invalid algorithm {hash_name}.')
        self._cipher_name = cipher_name

        self._properties = mcrypt.get_algorithm_props(cipher_name)
        self._block_size = self._properties['block_size']
        if len(self._properties['accepted_key_sizes']) != 1:
            self._key_size = None
        else:
            self._key_size = self._properties['max_key_size']

    def new(self, key: Union[bytes, bytearray], mode: str, IV: Union[bytes, bytearray, None] = None, **kwargs) -> mcrypt.MCrypt:
        return mcrypt.MCrypt(self._cipher_name, key, mode, IV)

    @property
    def properties(self) -> CipherProperty:
        return self._properties

    @property
    def block_size(self) -> int:
        return self._block_size

    @property
    def key_size(self) -> Optional[int]:
        return self._key_size


class HashModule:
    '''
    PEP-247 hash module.
    '''
    algorithms_available: Set[str] = mhash.list_algorithms()

    _hash_name: str
    _hash_id: int
    _digest_size: int

    def __init__(self, hash_name: str):
        # Capitalize the hash name so lower case names like "md5" will be
        # supported
        hash_name = hash_name.upper()
        if hash_name not in self.algorithms_available:
            raise ValueError(f'Invalid algorithm {hash_name}.')
        self._hash_name = hash_name
        self._hash_id = mhash.MHashAlgorithm[hash_name]

        self._digest_size = mhash.get_block_size(self._hash_id)

    def new(self, initial_data: Union[bytes, bytearray, None] = None):
        return mhash.MHash(self._hash_id, initial_data)

    @property
    def digest_size(self):
        return self._digest_size
