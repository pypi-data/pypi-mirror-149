from setuptools import setup

name = "types-paramiko"
description = "Typing stubs for paramiko"
long_description = '''
## Typing stubs for paramiko

This is a PEP 561 type stub package for the `paramiko` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `paramiko`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/paramiko. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `4bcb1a95abb5986e67149f16fa4929a43b23eab9`.
'''.lstrip()

setup(name=name,
      version="2.10.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/paramiko.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-cryptography'],
      packages=['paramiko-stubs'],
      package_data={'paramiko-stubs': ['__init__.pyi', '_version.pyi', '_winapi.pyi', 'agent.pyi', 'auth_handler.pyi', 'ber.pyi', 'buffered_pipe.pyi', 'channel.pyi', 'client.pyi', 'common.pyi', 'compress.pyi', 'config.pyi', 'dsskey.pyi', 'ecdsakey.pyi', 'ed25519key.pyi', 'file.pyi', 'hostkeys.pyi', 'kex_curve25519.pyi', 'kex_ecdh_nist.pyi', 'kex_gex.pyi', 'kex_group1.pyi', 'kex_group14.pyi', 'kex_group16.pyi', 'kex_gss.pyi', 'message.pyi', 'packet.pyi', 'pipe.pyi', 'pkey.pyi', 'primes.pyi', 'proxy.pyi', 'py3compat.pyi', 'rsakey.pyi', 'server.pyi', 'sftp.pyi', 'sftp_attr.pyi', 'sftp_client.pyi', 'sftp_file.pyi', 'sftp_handle.pyi', 'sftp_server.pyi', 'sftp_si.pyi', 'ssh_exception.pyi', 'ssh_gss.pyi', 'transport.pyi', 'util.pyi', 'win_pageant.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
