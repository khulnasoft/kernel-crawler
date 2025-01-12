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

from . import repo
from .aliyunlinux import AliyunLinuxMirror
from .almalinux import AlmaLinuxMirror
from .amazonlinux import (
    AmazonLinux1Mirror,
    AmazonLinux2Mirror,
    AmazonLinux2022Mirror,
    AmazonLinux2023Mirror,
)
from .archlinux import ArchLinuxMirror
from .bottlerocket import BottleRocketMirror
from .centos import CentosMirror
from .debian import DebianMirror
from .fedora import FedoraMirror
from .flatcar import FlatcarMirror
from .minikube import MinikubeMirror
from .opensuse import OpenSUSEMirror
from .oracle import OracleMirror
from .photon import PhotonOsMirror
from .redhat import RedhatContainer
from .rockylinux import RockyLinuxMirror
from .talos import TalosMirror
from .ubuntu import UbuntuMirror

# Keys are taken from /etc/os-release where available.
# Must be the same used by driverkit builders (https://github.com/khulnasoft/driverkit).
DISTROS = {
    "alinux": AliyunLinuxMirror,
    "almalinux": AlmaLinuxMirror,
    "amazonlinux": AmazonLinux1Mirror,
    "amazonlinux2": AmazonLinux2Mirror,
    "amazonlinux2022": AmazonLinux2022Mirror,
    "amazonlinux2023": AmazonLinux2023Mirror,
    "centos": CentosMirror,
    "fedora": FedoraMirror,
    "ol": OracleMirror,
    "photon": PhotonOsMirror,
    "rocky": RockyLinuxMirror,
    "opensuse": OpenSUSEMirror,
    "debian": DebianMirror,
    "ubuntu": UbuntuMirror,
    "flatcar": FlatcarMirror,
    "minikube": MinikubeMirror,
    "redhat": RedhatContainer,
    "arch": ArchLinuxMirror,
    "bottlerocket": BottleRocketMirror,
    "talos": TalosMirror,
}


def to_driverkit_config(d, res):
    dk_configs = []
    # Note, this is not good performance-wise because we are post-processing the list
    # while we could do the same at generation time.
    # But this is much simpler and involved touching less code.
    # Moreover, we do not really care about performance here.
    for ver, deps in res.items():
        dk_conf = d.to_driverkit_config(ver, deps)
        if dk_conf is not None:
            try:
                # Ubuntu returns multiple for each
                dk_configs.extend(dk_conf)
            except TypeError:
                # Others return just a single dk config
                dk_configs.append(dk_conf)

    return dk_configs


def crawl_kernels(distro, version, arch, images):
    ret = {}

    for distname, dist in DISTROS.items():
        if distname == distro or distro == "*":
            # If the distro requires an image (Redhat only so far), we need to amalgamate
            # the kernel versions from the supplied images before choosing the output.
            if issubclass(dist, repo.ContainerDistro):
                if images:
                    kv = {}
                    for image in images:
                        d = dist(image)
                        if len(kv) == 0:
                            kv = d.get_kernel_versions()
                        else:
                            kv.update(d.get_kernel_versions())
                    # We should now have a list of all kernel versions for the supplied images
                    res = kv
                else:
                    d = None
            else:
                d = dist(arch)
                res = d.get_package_tree(version)

            if d and res:
                ret[distname] = to_driverkit_config(d, res)
    return ret
