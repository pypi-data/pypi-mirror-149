# -*- coding: utf-8 -*-
# Copyright 2021 releng-tool

from releng_tool.defs import PackageType
from releng_tool.packages.exceptions import RelengToolInvalidPackageKeyValue
from releng_tool.packages.exceptions import RelengToolUnknownPackageType
from tests.support.pkg_config_test import TestPkgConfigsBase

class TestPkgConfigsPkgType(TestPkgConfigsBase):
    def test_pkgconfig_type_invalid_type(self):
        with self.assertRaises(RelengToolInvalidPackageKeyValue):
            self.LOAD('pkg-type-invalid-type')

    def test_pkgconfig_type_invalid_value(self):
        with self.assertRaises(RelengToolUnknownPackageType):
            self.LOAD('pkg-type-invalid-value')

    def test_pkgconfig_type_missing(self):
        pkg, _, _ = self.LOAD('missing')
        self.assertEqual(pkg.type, PackageType.SCRIPT)

    def test_pkgconfig_type_valid_autotools(self):
        pkg, _, _ = self.LOAD('pkg-type-valid-autotools')
        self.assertEqual(pkg.type, PackageType.AUTOTOOLS)

    def test_pkgconfig_type_valid_cmake(self):
        pkg, _, _ = self.LOAD('pkg-type-valid-cmake')
        self.assertEqual(pkg.type, PackageType.CMAKE)

    def test_pkgconfig_type_valid_python(self):
        pkg, _, _ = self.LOAD('pkg-type-valid-python')
        self.assertEqual(pkg.type, PackageType.PYTHON)

    def test_pkgconfig_type_valid_script(self):
        pkg, _, _ = self.LOAD('pkg-type-valid-script')
        self.assertEqual(pkg.type, PackageType.SCRIPT)
