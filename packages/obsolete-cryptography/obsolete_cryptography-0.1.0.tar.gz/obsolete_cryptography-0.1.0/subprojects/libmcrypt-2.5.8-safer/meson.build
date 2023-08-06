project('mcrypt', 'c',
    version : '2.5.8',
    meson_version : '>=0.56.0',
)

ac_mod = import('unstable_external_project')

p = ac_mod.add_project(
    'configure',
    configure_options : [
        '--prefix=@PREFIX@',
        '--libdir=@PREFIX@/@LIBDIR@',
        '--includedir=@PREFIX@/@INCLUDEDIR@',
        '--enable-static',
        '--disable-shared',
    ],
    env : [
        'CFLAGS=-fPIC',
    ],
)

mcrypt_dep = p.dependency('mcrypt')
