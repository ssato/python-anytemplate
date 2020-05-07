#! /usr/bin/bats
#
# Usage:
#   [<ENV_VAR>=... ] $0
#
CURDIR=$(pwd)

PKG_NAME=${PKG_NAME:-$(sed -n 's/name = //p' ${BATS_TEST_DIRNAME:?}/../setup.cfg)}
GIT_URL=${GIT_URL:-https://github.com/ssato/python-${PKG_NAME}}

# The latest stable release
RPM_BUILD_DIST=fedora-31-x86_64

SRCDIR=${BATS_TEST_DIRNAME}/../
WORKDIR=${WORKDIR:-}

function setup () {
    [[ -n ${WORKDIR} ]] || WORKDIR=$(mktemp --directory)
}

function teardown () {
    [[ ${WORKDIR:?} != '/' ]] && {
        rm -rf ${WORKDIR}
    } || :
}

@test "Test install from PyPI" {
    run pip3 install -U -t ${WORKDIR} ${PKG_NAME:?}
    [[ ${status} -eq 0 ]]
}

@test "Test install from the local git repo" {
    run pip3 install -U -t ${WORKDIR} ${SRCDIR:?}
    [[ ${status} -eq 0 ]]
}

@test "Test install from the remote git repo" {
    run pip3 install -U -t ${WORKDIR}  git+${GIT_URL:?}
    [[ ${status} -eq 0 ]]
}

@test "Test build and install the wheel package" {
    run python3 setup.py bdist_wheel
    [[ ${status} -eq 0 ]]

    run pip3 install -U -t ${WORKDIR} $(ls -1t dist/*.whl | head -n 1)
    [[ ${status} -eq 0 ]]
}

@test "Test build and install RPM packages if available" {
    which rpm 2>/dev/null >/dev/null || skip
    run python3 setup.py bdist_rpm --source-only
    [[ ${status} -eq 0 ]]

    which mock 2>/dev/null >/dev/null || skip
    run mock -r ${RPM_BUILD_DIST:?} $(ls -1t dist/*.src.rpm | head -n 1)
    [[ ${status} -eq 0 ]]

#   run dnf install -y --installroot ${WORKDIR} /var/lib/mock/${RPM_BUILD_DIST}/result/*.noarch.rpm
#   [[ ${status} -eq 0 ]]
}

# vim:sw=4:ts=4:et:
