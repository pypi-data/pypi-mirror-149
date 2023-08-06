#cython: language_level=3, binding=True
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

from ._mcrypt cimport *


class MCryptError(OSError):
    @classmethod
    def from_errno(cls, int mcrypt_errno):
        err_desc = 0
        cdef const char *cerr_desc = mcrypt_strerror(mcrypt_errno)
        if cerr_desc == NULL:
            err_desc = ''
        else:
            err_desc = cerr_desc.decode('utf-8').rstrip()
        return cls(mcrypt_errno, err_desc)


cdef class MCrypt:
    '''
    Bindings for libmcrypt. Loosely follows PEP-272 API.
    '''
    cdef MCRYPT mcrypt_ctx
    cdef readonly int block_size
    cdef readonly str algorithm
    cdef readonly str mode
    cdef readonly bytes IV
    cdef readonly bint is_block
    cdef readonly str state

    def __init__(self, algorithm, key, mode, iv=None):
        cdef int i = 0
        b_algorithm = algorithm.encode('ascii')
        b_mode = mode.encode('ascii')
        cdef char *c_algorithm = b_algorithm
        cdef char *c_mode = b_mode

        # Try to destroy any open context in advance if __init__ is called
        # multiple times to prevent potential leak.
        # Fields should be implicitly cleared when allocating so the simple
        # NULL check in _close() should be sufficient.
        self._close()

        self.mcrypt_ctx = mcrypt_module_open(c_algorithm, NULL, c_mode, NULL)

        if self.mcrypt_ctx == NULL:
            # The partially initialized object will be deleted by the GC, which
            # will also call _close, therefore no explicit mcrypt_generic_end is
            # needed here.
            raise ValueError('Invalid algorithm and method combination.')

        cdef:
            int size_keylen = 0
            int *c_keylen = mcrypt_enc_get_supported_key_sizes(self.mcrypt_ctx, &size_keylen)
            int ivlen = mcrypt_enc_get_iv_size(self.mcrypt_ctx)

        keylen = []

        for i in range(size_keylen):
            keylen.append(c_keylen[i])

        if len(key) not in keylen:
            raise ValueError(f'Invalid key length. Valid lengths are: {keylen}.')

        if iv is not None and len(iv) != ivlen:
            raise ValueError(f'IV must be {ivlen} bytes long.')

        cdef:
            unsigned char *c_key = key
            unsigned char *c_iv = NULL

        if iv is not None:
            c_iv = iv

        cdef int init_result = mcrypt_generic_init(self.mcrypt_ctx, c_key, len(key), c_iv)
        if init_result < 0:
            raise MCryptError.from_errno(init_result)

        self.state = 'initialized'

        self.algorithm = algorithm
        self.mode = mode
        self.IV = iv

        self.is_block = mcrypt_enc_is_block_algorithm_mode(self.mcrypt_ctx)
        self.block_size = mcrypt_enc_get_block_size(self.mcrypt_ctx)

    def __dealloc__(self):
        self._close()

    cpdef _close(self):
        '''
        Destroy the context.
        '''
        if self.mcrypt_ctx != NULL:
            mcrypt_generic_end(self.mcrypt_ctx)
            self.mcrypt_ctx = NULL

    cpdef self_test(self):
        '''
        Perform mcrypt self test.
        Raises MCryptError when self test fails.
        '''
        cdef int result = mcrypt_enc_self_test(self.mcrypt_ctx)
        if result < 0:
            raise MCryptError.from_errno(result)

    cpdef encrypt(self, data):
        '''
        Encrypt data.
        For a cipher in block mode the data must be aligned to the block size.
        '''
        cdef unsigned char *cdata = data
        cdef unsigned char *cresult = NULL
        cdef bytes result = None
        cdef int encrypt_result = 0

        if self.state != 'initialized' and self.state != 'encrypting':
            raise RuntimeError('Cannot encrypt data using a decryption context.')
        self.state = 'encrypting'

        if self.is_block and len(data) % self.block_size != 0:
            raise ValueError(f'Data size must be multiple of {self.block_size} bytes.')

        try:
            cresult = <unsigned char *> malloc(len(data))
            if cresult == NULL:
                raise MemoryError(f'Unable to allocate {len(data)} bytes.')
            memcpy(cresult, cdata, len(data))

            encrypt_result = mcrypt_generic(self.mcrypt_ctx, cresult, len(data))
            if encrypt_result < 0:
                raise MCryptError.from_errno(encrypt_result)

            result = cresult[:len(data)]
        finally:
            if cresult != NULL:
                free(cresult)

        return result

    cpdef decrypt(self, data):
        '''
        Decrypt data.
        For a cipher in block mode the data must be aligned to the block size.
        '''
        cdef unsigned char *cdata = data
        cdef unsigned char *cresult = NULL
        cdef bytes result = None
        cdef int decrypt_result = 0

        if self.state != 'initialized' and self.state != 'decrypting':
            raise RuntimeError('Cannot decrypt data using an encryption context.')
        self.state = 'decrypting'

        if self.is_block and len(data) % self.block_size != 0:
            raise ValueError(f'Data size must be multiple of {self.block_size} bytes.')

        try:
            cresult = <unsigned char *> malloc(len(data))
            if cresult == NULL:
                raise MemoryError(f'Unable to allocate {len(data)} bytes.')
            memcpy(cresult, cdata, len(data))

            decrypt_result = mdecrypt_generic(self.mcrypt_ctx, cresult, len(data))
            if decrypt_result < 0:
                raise MCryptError.from_errno(decrypt_result)

            result = cresult[:len(data)]
        finally:
            if cresult != NULL:
                free(cresult)

        return result


cdef _list_features(type_):
    '''
    List features.
    '''
    cdef char **features = NULL
    cdef int nfeatures = 0

    cdef set result = set()
    try:
        if type_ == 'algo':
            features = mcrypt_list_algorithms(NULL, &nfeatures)
        elif type_ == 'mode':
            features = mcrypt_list_modes(NULL, &nfeatures)
        if features != NULL:
            for i in range(nfeatures):
                result.add(features[i].decode('ascii'))
    finally:
        if features != NULL:
            free(features)
    return result

cpdef list_algorithms():
    '''
    List all ciphers supported by the library.
    '''
    return _list_features('algo')

cpdef list_modes():
    '''
    List all modes supported by the library.
    '''
    return _list_features('mode')

cpdef get_algorithm_props(algorithm):
    '''
    Return a dictionary that describes the properties of the selected algorithm.
    '''
    cdef bytes balgorithm = algorithm.encode('ascii')
    cdef char *calgorithm = balgorithm

    cdef int nsizes = 0
    cdef int *csizes = NULL
    cdef dict result = {}
    cdef set sizes = set()

    result['block_size'] = mcrypt_module_get_algo_block_size(calgorithm, NULL)
    result['max_key_size'] = mcrypt_module_get_algo_key_size(calgorithm, NULL)

    try:
        csizes = mcrypt_module_get_algo_supported_key_sizes(calgorithm, NULL, &nsizes)
        if csizes != NULL:
            for i in range(nsizes):
                sizes.add(csizes[i])
        result['accepted_key_sizes'] = sizes
    finally:
        if csizes != NULL:
            free(csizes)

    return result
