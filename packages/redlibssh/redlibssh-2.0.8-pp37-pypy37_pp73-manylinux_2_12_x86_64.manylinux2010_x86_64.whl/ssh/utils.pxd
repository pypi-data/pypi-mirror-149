# This file is part of RedLibSSH.
#
# Copyright (C) 2017-2020 Panos Kittenis
# Copyright (C) 2022 Red-M
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, version 2.1.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from .c_ssh cimport ssh_session, ssh_string

cdef bytes to_bytes(_str)
cdef object to_str(const char *c_str)
cdef object to_str_len(const char *c_str, int length)
cdef int handle_error_codes(int errcode, ssh_session) except -1
cdef int handle_auth_error_codes(int errcode, ssh_session) except -1
cdef int handle_sftp_error_codes(int errcode, ssh_session) except -1
cdef bytes ssh_string_to_bytes(ssh_string _str)

IF HAVE_POLL==1:
    cdef extern from "poll.h" nogil:
        ctypedef unsigned int nfds_t
        enum:
            POLLIN
            POLLPRI
            POLLOUT
            POLLERR
            POLLHUP
            POLLNVAL
        struct pollfd:
            int fd
            short events
            short revents
        int poll(pollfd *fds, nfds_t nfds, int timeout)

cdef extern from "openssl/opensslv.h" nogil:
    char* OPENSSL_VERSION_TEXT
