from libc.stdint cimport uint8_t, uint16_t, uint32_t, uint64_t

cdef extern from "mhash.h":
    ctypedef enum hashid:
        MHASH_CRC32,
        MHASH_CRC32B,
        MHASH_ADLER32,
        MHASH_MD2,
        MHASH_MD4,
        MHASH_RIPEMD128,
        MHASH_RIPEMD160,
        MHASH_RIPEMD256,
        MHASH_RIPEMD320,
        MHASH_MD5,
        MHASH_SHA1,
        MHASH_SHA224,
        MHASH_SHA256,
        MHASH_SHA384,
        MHASH_SHA512,
        MHASH_HAVAL128,
        MHASH_HAVAL160,
        MHASH_HAVAL192,
        MHASH_HAVAL224,
        MHASH_HAVAL256,
        MHASH_TIGER128,
        MHASH_TIGER160,
        MHASH_TIGER192,
        MHASH_GOST,
        MHASH_WHIRLPOOL,
        MHASH_SNEFRU128,
        MHASH_SNEFRU256,
        MHASH_AR,
        MHASH_BOOGNISH,
        MHASH_CELLHASH,
        MHASH_FFT_HASH_I,
        MHASH_FFT_HASH_II,
        MHASH_NHASH,
        MHASH_PANAMA,
        MHASH_SMASH,
        MHASH_SUBHASH,

    # These aliases are actually quite useful and so will be kept
    enum: MHASH_HAVAL
    enum: MHASH_TIGER

    ctypedef enum mutils_error_codes:
        MUTILS_OK,
        MUTILS_SYSTEM_ERROR,
        MUTILS_UNSPECIFIED_ERROR,
        MUTILS_SYSTEM_RESOURCE_ERROR,
        MUTILS_PARAMETER_ERROR,
        MUTILS_INVALID_FUNCTION,
        MUTILS_INVALID_INPUT_BUFFER,
        MUTILS_INVALID_OUTPUT_BUFFER,
        MUTILS_INVALID_PASSES,
        MUTILS_INVALID_FORMAT,
        MUTILS_INVALID_SIZE,
        MUTILS_INVALID_RESULT,

    ctypedef enum keygenid:
        KEYGEN_MCRYPT,
        KEYGEN_ASIS,
        KEYGEN_HEX,
        KEYGEN_PKDES,
        KEYGEN_S2K_SIMPLE,
        KEYGEN_S2K_SALTED,
        KEYGEN_S2K_ISALTED,

    # These are in mutils.h and used by various types and functions
    ctypedef uint8_t mutils_word8
    ctypedef uint16_t mutils_word16
    ctypedef uint32_t mutils_word32
    ctypedef uint64_t mutils_word64
    ctypedef char mutils_boolean

    ctypedef mutils_word32 mutils_error

    ctypedef struct MHASH_INSTANCE:
        pass
    ctypedef MHASH_INSTANCE* MHASH

    # Keygen parameter object
    ctypedef struct KEYGEN:
        hashid hash_algorithm[2]
        mutils_word32 count
        void *salt
        mutils_word32 salt_size

    # Only public APIs listed in the manpage are listed below (with corrected types.)

    mutils_word32 mhash_count()
    mutils_word32 mhash_get_block_size(hashid type)
    mutils_word8 *mhash_get_hash_name(hashid type)
    const mutils_word8 *mhash_get_hash_name_static(hashid type)
    mutils_word32 mhash_get_hash_pblock(hashid type)
    hashid mhash_get_mhash_algo(MHASH tmp)

    mutils_error mhash_keygen_ext(keygenid algorithm, KEYGEN algorithm_data, void* keyword, mutils_word32 keysize, mutils_word8 *password, mutils_word32 passwordlen)

    MHASH mhash_init(hashid type)
    MHASH mhash_hmac_init(const hashid type, void *key, mutils_word32 keysize, mutils_word32 block)
    MHASH mhash_cp(MHASH from_)

    mutils_boolean mhash(MHASH thread, const void *plaintext, mutils_word32 size)

    mutils_boolean mhash_save_state_mem(MHASH thread, void *mem, mutils_word32 *mem_size)
    MHASH mhash_restore_state_mem(void *mem)

    void mhash_deinit(MHASH thread, void *result)
    void *mhash_end(MHASH thread)
    void *mhash_end_m(MHASH thread, void *(*hash_malloc)(mutils_word32))

    void *mhash_hmac_end(MHASH thread)
    void *mhash_hmac_end_m(MHASH thread, void *(*hash_malloc)(mutils_word32))
    mutils_boolean mhash_hmac_deinit(MHASH thread, void *result)

    # mhash free wrapper
    void mhash_free(void *ptr);
