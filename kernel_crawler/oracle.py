# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2023 The Falco Authors.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
    # http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import repo
from . import rpm


class OracleRepository(rpm.RpmRepository):
    @classmethod
    def kernel_package_query(cls):
        return '''(name IN ('kernel', 'kernel-devel', 'kernel-uek', 'kernel-uek-devel'))'''


class OracleMirror(repo.Distro):

    def repos(self):

        # all the base URLs for major versions of OracleLinux
        base_urls = [
            'http://yum.oracle.com/repo/OracleLinux/OL6',  # Oracle 6
            'http://yum.oracle.com/repo/OracleLinux/OL7',  # Oracle 7
            'http://yum.oracle.com/repo/OracleLinux/OL8',  # Oracle 8
            'http://yum.oracle.com/repo/OracleLinux/OL9',  # Oracle 9
        ]

        # setup list for possible UEK URLs
        possible_uek_urls = []
        # Oracle seems to stick to 0 thru 9 for UEK versions, wrapping back to 0 after 9
        possible_uek_versions = list(range(0, 10))
        # loop through base URLs and possible UEK versions to build possible UEK URLs
        for url in base_urls:
            for uek_version in possible_uek_versions:
                possible_uek_urls.append(f'{url}/UEKR{uek_version}/{self.arch}/')
                possible_uek_urls.append(f'{url}/UEKR{uek_version}/latest/{self.arch}/')  # Oracle 6 has one URL subpath for /latest

        # setup list for possible non UEK URLs
        possible_non_uek_urls = []
        # loop through base URLs and build other known URL subpaths
        for url in base_urls:
            possible_non_uek_urls.append(f'{url}/latest/{self.arch}/')         # Oracle 6 & 7
            possible_non_uek_urls.append(f'{url}/MODRHCK/{self.arch}/')        # Oracle 6 & 7
            possible_non_uek_urls.append(f'{url}/UEK/latest/{self.arch}/')     # Oracle 6 has this non-versioned UEK subpath
            possible_non_uek_urls.append(f'{url}/baseos/latest/{self.arch}/')  # Oracle 8 & 9
            possible_non_uek_urls.append(f'{url}/appstream/{self.arch}/')      # Oracle 8 & 9

        # combine the built UEK URLs list and the base URLs
        repos = [ repo for mirror in (possible_uek_urls, possible_non_uek_urls) for repo in mirror ]

        return repos


    def __init__(self, arch):
        super(OracleMirror, self).__init__([], arch)

    def list_repos(self):
        return [OracleRepository(url) for url in self.repos()]

    def to_driverkit_config(self, release, deps):
        for dep in deps:
            if dep.find("devel") != -1:
                if 'uek' in release:  # uek kernels have kernel versions of "2"
                    # example:
                    #  # uname -a
                    #  Linux vm-ol8 5.15.0-100.96.32.el8uek.x86_64 #2 SMP Tue ...
                    return repo.DriverKitConfig(release, "ol", dep, kernelversion="2")
                else:  # else return default with kernelversion=1
                    return repo.DriverKitConfig(release, "ol", dep)
