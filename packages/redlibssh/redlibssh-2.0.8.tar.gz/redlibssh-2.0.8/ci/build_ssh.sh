#!/bin/bash -xe

if [ -d /usr/local/opt/openssl ]; then
    export OPENSSL_ROOT_DIR=/usr/local/opt/openssl
fi

mkdir -p src && cd src
cmake -DCMAKE_BUILD_TYPE=Release -DWITH_NACL=ON -DWITH_PKCS11_URI=ON -DWITH_GSSAPI=ON -DWITH_BLOWFISH_CIPHER=ON ../libssh
make -j
cd ..
cp src/src/libssh.so* ssh/
