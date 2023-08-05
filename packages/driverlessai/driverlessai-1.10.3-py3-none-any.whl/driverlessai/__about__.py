#!/usr/bin/env python
# Copyright 2020 H2O.ai; Proprietary License;  -*- encoding: utf-8 -*-
import pkg_resources

__all__ = ["__version__", "__build_info__"]

# Build defaults
build_info = {
    "git_build": "dev",
    "git_commit": "",
    "git_describe": "",
    "build_os": "",
    "build_machine": "",
    "build_date": "",
    "build_user": "",
    "version": "0.0.0",
}

if pkg_resources.resource_exists("driverlessai", "BUILD_INFO.txt"):
    exec(pkg_resources.resource_string("driverlessai", "BUILD_INFO.txt"), build_info)

# Exported properties
__version__ = build_info["version"]
__build_info__ = build_info
