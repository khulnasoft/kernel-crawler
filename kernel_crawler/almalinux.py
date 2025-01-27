# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2023 The KhulnaSoft Authors.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import repo, rpm


def v8_only(ver):
    return ver.startswith("8")


def v9_only(ver):
    return ver.startswith("9")


class AlmaLinuxMirror(repo.Distro):
    def __init__(self, arch):
        mirrors = [
            # AlmaLinux 8
            rpm.RpmMirror(
                "http://repo.almalinux.org/almalinux/",
                "BaseOS/" + arch + "/os/",
                v8_only,
            ),
            rpm.RpmMirror(
                "http://repo.almalinux.org/almalinux/",
                "AppStream/" + arch + "/os/",
                v8_only,
            ),
            # AlmaLinux 9
            rpm.RpmMirror(
                "http://repo.almalinux.org/almalinux/",
                "BaseOS/" + arch + "/os/",
                v9_only,
            ),
            rpm.RpmMirror(
                "http://repo.almalinux.org/almalinux/",
                "AppStream/" + arch + "/os/",
                v9_only,
            ),
        ]
        super(AlmaLinuxMirror, self).__init__(mirrors, arch)

    def to_driverkit_config(self, release, deps):
        for dep in deps:
            if dep.find("devel") != -1:
                return repo.DriverKitConfig(release, "almalinux", dep)
