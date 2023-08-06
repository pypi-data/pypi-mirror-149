#cython: language_level=3, binding=True
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

from ._mhash cimport *

import enum


class MHashAlgorithm(enum.IntEnum):
    CRC32 = MHASH_CRC32
    CRC32B = MHASH_CRC32B
    ADLER32 = MHASH_ADLER32
    MD2 = MHASH_MD2
    MD4 = MHASH_MD4
    RIPEMD128 = MHASH_RIPEMD128
    RIPEMD160 = MHASH_RIPEMD160
    RIPEMD256 = MHASH_RIPEMD256
    RIPEMD320 = MHASH_RIPEMD320
    MD5 = MHASH_MD5
    SHA1 = MHASH_SHA1
    SHA224 = MHASH_SHA224
    SHA256 = MHASH_SHA256
    SHA384 = MHASH_SHA384
    SHA512 = MHASH_SHA512
    HAVAL128 = MHASH_HAVAL128
    HAVAL160 = MHASH_HAVAL160
    HAVAL192 = MHASH_HAVAL192
    HAVAL224 = MHASH_HAVAL224
    HAVAL256 = MHASH_HAVAL256
    TIGER128 = MHASH_TIGER128
    TIGER160 = MHASH_TIGER160
    TIGER192 = MHASH_TIGER192
    GOST = MHASH_GOST
    WHIRLPOOL = MHASH_WHIRLPOOL
    SNEFRU128 = MHASH_SNEFRU128
    SNEFRU256 = MHASH_SNEFRU256
    AR = MHASH_AR
    BOOGNISH = MHASH_BOOGNISH
    CELLHASH = MHASH_CELLHASH
    FFT_HASH_I = MHASH_FFT_HASH_I
    FFT_HASH_II = MHASH_FFT_HASH_II
    NHASH = MHASH_NHASH
    PANAMA = MHASH_PANAMA
    SMASH = MHASH_SMASH
    SUBHASH = MHASH_SUBHASH
    HAVAL = MHASH_HAVAL
    TIGER = MHASH_TIGER


cdef class MHash:
    cdef MHASH mhash_ctx
    cdef readonly mutils_word32 digest_size
    cdef readonly str algorithm
    cdef readonly hashid algorithm_id

    def __init__(self, hashid algorithm_id, initial_data=None):
        cdef const mutils_word8 *calgorithm_str = NULL
        cdef unsigned char *cinitial_data = NULL

        # Try to destroy any open context in advance if __init__ is called
        # multiple times to prevent potential leak.
        # Fields should be implicitly cleared when allocating so the simple
        # NULL check in _close() should be sufficient.
        self._close()

        self.mhash_ctx = mhash_init(algorithm_id)
        if self.mhash_ctx == NULL:
            raise ValueError('Invalid algorithm ID.')

        # Determine and save algorithm name
        calgorithm_str = mhash_get_hash_name_static(algorithm_id)
        if calgorithm_str != NULL:
            self.algorithm = calgorithm_str.decode('utf-8')
        else:
            self.algorithm = None

        # Save digest size and algorithm ID
        self.digest_size = mhash_get_block_size(algorithm_id)
        self.algorithm_id = algorithm_id

        # Import initial data if applicable
        if initial_data is not None:
            self.update(initial_data)

    def __dealloc__(self):
        self._close()

    cpdef _close(self):
        '''
        Destroy the context.
        '''
        if self.mhash_ctx != NULL:
            mhash_deinit(self.mhash_ctx, NULL)
            self.mhash_ctx = NULL

    cpdef update(self, data):
        '''
        Hash string into the current state of the hashing object. update() can
        be called any number of times during a hashing object's lifetime.
        '''
        cdef unsigned char *cdata = data
        mhash(self.mhash_ctx, cdata, len(data))

    cpdef digest(self):
        '''
        Return the hash value of this hashing object as a string containing
        8-bit data. The object is not altered in any way by this function;
        you can continue updating the object after calling this function.
        '''
        # PEP-247 requires the digest() method to not close the context. However
        # mhash does not support such operation. Therefore we create a copy of
        # the context with mhash_cp and close the copy instead.
        cdef unsigned char *cdigest = NULL
        cdef MHASH mhash_ctx_copy = NULL
        cdef bytes digest = None
        try:
            cdigest = <unsigned char *> malloc(self.digest_size)
            if cdigest == NULL:
                raise MemoryError(f'Cannot allocate {self.digest_size} bytes.')

            mhash_ctx_copy = mhash_cp(self.mhash_ctx)
            if mhash_ctx_copy == NULL:
                raise RuntimeError('Unable to duplicate mhash context.')

            mhash_deinit(mhash_ctx_copy, cdigest)
            mhash_ctx_copy = NULL

            digest = cdigest[:self.digest_size]

        finally:
            if cdigest != NULL:
                free(cdigest)
            if mhash_ctx_copy != NULL:
                mhash_deinit(mhash_ctx_copy, NULL)

        return digest

    cpdef hexdigest(self):
        '''
        Return the hash value of this hashing object as a string containing
        hexadecimal digits. Lowercase letters are used for the digits a through
        f.
        '''
        return self.digest().hex()


cpdef list_algorithms():
    '''
    List all hash algorithms supported by the library.
    '''
    cdef mutils_word32 max_algorithm_id = mhash_count()
    cdef set result = set()
    for algorithm_id in MHashAlgorithm:
        if algorithm_id.value <= max_algorithm_id:
            result.add(algorithm_id.name)
    return result

cpdef get_block_size(hashid algorithm_id):
    '''
    Get hash block size by algorithm ID.
    '''
    return mhash_get_block_size(algorithm_id)
