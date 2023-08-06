# exported from libmcrypt 2.5.8

cdef extern from "mcrypt.h":
    ctypedef struct CRYPT_STREAM:
        pass
    ctypedef CRYPT_STREAM* MCRYPT

    MCRYPT mcrypt_module_open(char *algorithm, char *a_directory, char *mode, char *m_directory)
    int mcrypt_module_close(MCRYPT td)
    int mcrypt_module_support_dynamic()

    int mcrypt_generic_init(const MCRYPT td, void *key, int lenofkey, void *IV)
    int mcrypt_generic_deinit(const MCRYPT td)
    int mcrypt_generic_end(const MCRYPT td)
    int mdecrypt_generic(MCRYPT td, void *plaintext, int len)
    int mcrypt_generic(MCRYPT td, void *plaintext, int len)

    int mcrypt_enc_set_state(MCRYPT td, void *st, int size)
    int mcrypt_enc_get_state(MCRYPT td, void *st, int *size)

    int mcrypt_enc_self_test(MCRYPT td)
    int mcrypt_enc_get_block_size(MCRYPT td)
    int mcrypt_enc_get_iv_size(MCRYPT td)
    int mcrypt_enc_get_key_size(MCRYPT td)

    int mcrypt_enc_is_block_algorithm(MCRYPT td)

    int mcrypt_enc_is_block_mode(MCRYPT td)

    int mcrypt_enc_is_block_algorithm_mode(MCRYPT td)
    int mcrypt_enc_mode_has_iv(MCRYPT td)

    char *mcrypt_enc_get_algorithms_name(MCRYPT td)
    char *mcrypt_enc_get_modes_name(MCRYPT td)

    int *mcrypt_enc_get_supported_key_sizes(MCRYPT td, int *len)

    char **mcrypt_list_algorithms(char *libdir, int *size)
    char **mcrypt_list_modes(char *libdir, int *size)

    void mcrypt_free_p(char **p, int size)
    void mcrypt_free(void *ptr)

    void mcrypt_perror(int err)
    const char* mcrypt_strerror(int err)

    int mcrypt_module_self_test(char *algorithm, char *a_directory)

    int mcrypt_module_is_block_algorithm(char *algorithm, char *a_directory)
    int mcrypt_module_is_block_algorithm_mode(char *mode, char *m_directory)
    int mcrypt_module_is_block_mode(char *mode, char *m_directory)

    int mcrypt_module_get_algo_key_size(char *algorithm, char *a_directory)
    int mcrypt_module_get_algo_block_size(char *algorithm, char *a_directory)

    int *mcrypt_module_get_algo_supported_key_sizes(char *algorithm, char *a_directory, int *len)

    int mcrypt_module_algorithm_version(char *algorithm, char *a_directory)
    int mcrypt_module_mode_version(char *mode, char *a_directory)

    int mcrypt_mutex_register (void (*mutex_lock)(), void (*mutex_unlock)(), void (*set_error)(const char*), const char* (*get_error)())

    const char *mcrypt_check_version(const char *)
