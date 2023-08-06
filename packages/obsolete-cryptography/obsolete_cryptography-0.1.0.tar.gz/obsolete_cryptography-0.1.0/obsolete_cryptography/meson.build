# Native extensions
py3.extension_module(
    'mcrypt',
    'mcrypt.pyx',
    dependencies : [
        py3_dep,
        mcrypt_dep,
    ],
    install : true,
    subdir : 'obsolete_cryptography',
)

py3.extension_module(
    'mhash',
    'mhash.pyx',
    dependencies : [
        py3_dep,
        mhash_dep,
    ],
    install : true,
    subdir : 'obsolete_cryptography',
)

# Pure Python modules
py3.install_sources(
    [
        '__init__.py',
    ],
    subdir : 'obsolete_cryptography',
)
