project(
    'obsolete-cryptography',
    ['c', 'cython'],
    version : '0.1.0',
    meson_version : '>=0.59.0',
)

py_mod = import('python')
py3 = py_mod.find_installation('python3')
py3_dep = py3.dependency()

mcrypt_subp = subproject('libmcrypt-2.5.8-safer')
mcrypt_dep = mcrypt_subp.get_variable('mcrypt_dep')

mhash_subp = subproject('mhash-0.9.9.9')
mhash_dep = mhash_subp.get_variable('mhash_dep')

subdir('obsolete_cryptography')
