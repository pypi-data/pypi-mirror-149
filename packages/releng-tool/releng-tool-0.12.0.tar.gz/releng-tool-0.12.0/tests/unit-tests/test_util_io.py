# -*- coding: utf-8 -*-
# Copyright 2018-2022 releng-tool

from collections import OrderedDict
from releng_tool.util.io import ensure_dir_exists
from releng_tool.util.io import execute
from releng_tool.util.io import interpret_stem_extension as ise
from releng_tool.util.io import opt_file
from releng_tool.util.io import path_copy
from releng_tool.util.io import path_exists
from releng_tool.util.io import path_move
from releng_tool.util.io import path_remove
from releng_tool.util.io import prepare_arguments
from releng_tool.util.io import prepare_definitions
from releng_tool.util.io import prepend_shebang_interpreter as psi
from releng_tool.util.io import run_script
from releng_tool.util.io import touch
from releng_tool.util.log import is_verbose
from tests import compare_contents
from tests import prepare_workdir
from tests import redirect_stdout
import os
import sys
import unittest

ASSETS_DIR = 'assets'

class TestUtilIo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.realpath(__file__))
        cls.assets_dir = os.path.join(base_dir, ASSETS_DIR)

        def assertExists(cls, path, *args):
            cls.assertTrue(path_exists(path, *args),
                'missing file: ' + os.path.join(path, *args))
        cls.assertExists = assertExists

    def test_utilio_copy(self):
        check_dir_01 = os.path.join(self.assets_dir, 'copy-check-01')
        check_dir_02 = os.path.join(self.assets_dir, 'copy-check-02')

        with prepare_workdir() as work_dir:
            # (directories)

            # copy the first batch of assets into the working directory
            result = path_copy(check_dir_01, work_dir, critical=False)
            self.assertTrue(result)
            self.assertExists(work_dir, 'test-file-a')
            self.assertExists(work_dir, 'test-file-b')
            self.assertExists(work_dir, 'test-file-x')
            cc1 = compare_contents(
                os.path.join(check_dir_01, 'test-file-b'),
                os.path.join(work_dir, 'test-file-b'))
            self.assertIsNone(cc1, cc1)

            # override the working directory with the second batch
            result = path_copy(check_dir_02, work_dir, critical=False)
            self.assertTrue(result)
            self.assertExists(work_dir, 'test-file-a')
            self.assertExists(work_dir, 'test-file-b')
            self.assertExists(work_dir, 'test-file-c')
            self.assertExists(work_dir, 'test-file-x')
            cc2 = compare_contents(
                os.path.join(check_dir_02, 'test-file-b'),
                os.path.join(work_dir, 'test-file-b'))
            self.assertIsNone(cc2, cc2)

            # (files)
            sub_dir = os.path.join(work_dir, 'sub', 'dir', 'xyz', '')
            copied_file_a = os.path.join(work_dir, 'test-file-a')
            copied_file_b = os.path.join(work_dir, 'test-file-b')
            target_ow = os.path.join(sub_dir, 'test-file-a')

            # copy individual files (file to new directory)
            result = path_copy(copied_file_a, sub_dir, critical=False)
            self.assertTrue(result)
            self.assertExists(target_ow)
            cc3 = compare_contents(copied_file_a, target_ow)
            self.assertIsNone(cc3, cc3)

            # copy individual files (overwrite)
            result = path_copy(copied_file_b, target_ow, critical=False)
            self.assertTrue(result)
            cc4 = compare_contents(copied_file_b, target_ow)
            self.assertIsNone(cc4, cc4)

            # attempt to copy a missing file
            missing_file = os.path.join(work_dir, 'test-file-missing')
            target = os.path.join(work_dir, 'container')
            result = path_copy(missing_file, target, critical=False)
            self.assertFalse(result)

            # attempt to copy a missing file (critical)
            with self.assertRaises(SystemExit):
                path_copy(missing_file, target)

            # attempt to copy a file to itself
            src = copied_file_a
            with self.assertRaises(SystemExit):
                path_copy(src, src)

            # attempt to copy a directory to itself in legacy python, to ensure
            # `DistutilsFileError` is handled properly (windows only)
            if sys.version_info < (3, 0) and sys.platform == 'win32':
                with self.assertRaises(SystemExit):
                    path_copy(work_dir, work_dir)

            # force a directory target with a non-trailing path separator
            force_src = os.path.join(work_dir, 'test-file-a')
            self.assertExists(force_src)

            force1 = os.path.join(work_dir, 'force1')
            result = path_copy(force_src, force1, critical=False)
            self.assertTrue(result)
            self.assertTrue(os.path.isfile(force1))

            force2 = os.path.join(work_dir, 'force2')
            result = path_copy(force_src, force2, critical=False, dst_dir=True)
            self.assertTrue(result)
            self.assertTrue(os.path.isdir(force2))

    def test_utilio_ensuredirexists(self):
        with prepare_workdir() as work_dir:
            result = ensure_dir_exists(work_dir)
            self.assertTrue(result)

            new_dir = os.path.join(work_dir, 'test1')
            self.assertFalse(os.path.exists(new_dir))

            result = ensure_dir_exists(new_dir)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(new_dir))

            new_file = os.path.join(work_dir, 'test2')
            with open(new_file, 'ab'):
                pass
            self.assertTrue(os.path.isfile(new_file))

            result = ensure_dir_exists(new_file)
            self.assertFalse(result)
            self.assertTrue(os.path.isfile(new_file))

    def test_utilio_execution(self):
        result = execute(None, quiet=True, critical=False)
        self.assertFalse(result)

        result = execute([], quiet=True, critical=False)
        self.assertFalse(result)

        test_cmd = ['python', '-c', 'print("Hello")']
        result = execute(test_cmd, quiet=True, critical=False)
        self.assertTrue(result)

        result = execute(['an_unknown_command'], quiet=True, critical=False)
        self.assertFalse(result)

        # skip output checks if verbose mode is enabled
        if is_verbose():
            raise unittest.SkipTest(
                'ignoring execution output checks while in verbose mode')

        # verify output
        with redirect_stdout() as stream:
            test_cmd = [sys.executable, '-c', 'print("Hello")']
            result = execute(test_cmd, critical=False)
            self.assertTrue(result)
        self.assertEqual(stream.getvalue().strip(), 'Hello')

        # verify quiet mode
        with redirect_stdout() as stream:
            test_cmd = [sys.executable, '-c', 'print("Hello")']
            result = execute(test_cmd, quiet=True, critical=False)
            self.assertTrue(result)
        self.assertEqual(stream.getvalue().strip(), '')

        # verify capture mode which will be silent
        out = []
        with redirect_stdout() as stream:
            test_cmd = [sys.executable, '-c', 'print("Hello")']
            result = execute(test_cmd, critical=False, capture=out)
            self.assertTrue(result)
        self.assertEqual(''.join(out), 'Hello')
        self.assertEqual(stream.getvalue().strip(), '')

        # verify capture mode that is also verbose
        out = []
        with redirect_stdout() as stream:
            test_cmd = [sys.executable, '-c', 'print("Hello")']
            result = execute(test_cmd, quiet=False, critical=False, capture=out)
            self.assertTrue(result)
        self.assertEqual(''.join(out), 'Hello')
        self.assertEqual(stream.getvalue().strip(), 'Hello')

    def test_utilio_ise(self):
        provided = 'my-file.txt'
        expected = ('my-file', 'txt')
        self.assertEqual(ise(provided), expected)

        provided = 'my-file.tar.Z'
        expected = ('my-file', 'tar.Z')
        self.assertEqual(ise(provided), expected)

        provided = 'my-file.tar.gz'
        expected = ('my-file', 'tar.gz')
        self.assertEqual(ise(provided), expected)

        provided = 'my-file.tar.xz'
        expected = ('my-file', 'tar.xz')
        self.assertEqual(ise(provided), expected)

        provided = 'my.file.name.dat'
        expected = ('my.file.name', 'dat')
        self.assertEqual(ise(provided), expected)

        provided = 'my-file'
        expected = ('my-file', None)
        self.assertEqual(ise(provided), expected)

        provided = None
        expected = (None, None)
        self.assertEqual(ise(provided), expected)

    def test_utilio_move(self):
        with prepare_workdir() as work_dir:
            def _(*args):
                return os.path.join(work_dir, *args)

            # setup
            directories = [
                _('dir1'),
                _('dir2', 'dir3'),
                _('dir4', 'dir5', 'dir6'),
            ]
            for dir_ in directories:
                os.makedirs(dir_)

            files = [
                _('file1'),
                _('dir2', 'file2'),
                _('dir2', 'dir3', 'file3'),
                _('dir4', 'file4'),
                _('dir4', 'dir5', 'file5'),
                _('dir4', 'dir5', 'dir6', 'file6'),
            ]
            for file in files:
                with open(file, 'a') as f:
                    f.write(file)

            # (simple file move)
            src = _('file1')
            dst = _('file7')
            moved = path_move(src, dst, critical=False)
            self.assertTrue(moved)
            self.assertFalse(os.path.isfile(src))
            self.assertTrue(os.path.isfile(dst))

            # (another file move)
            src = _('dir4', 'dir5', 'dir6', 'file6')
            dst = _('dir9', 'dir10', 'file8')
            moved = path_move(src, dst, critical=False)
            self.assertTrue(moved)
            self.assertFalse(os.path.isfile(src))
            self.assertTrue(os.path.isfile(dst))

            # (another file move)
            src = _('dir9', 'dir10', 'file8')
            dst = _('dir9', 'dir11', '')
            moved = path_move(src, dst, critical=False)
            self.assertTrue(moved)
            self.assertFalse(os.path.isfile(src))
            self.assertTrue(os.path.isfile(_('dir9', 'dir11', 'file8')))

            # (overwriting file move)
            src = _('dir2', 'file2')
            dst = _('file7')
            moved = path_move(src, dst, critical=False)
            self.assertTrue(moved)
            self.assertFalse(os.path.isfile(src))
            self.assertTrue(os.path.isfile(dst))

            # (bad file move attempt)
            src = _('file7')
            dst_part = _('dir4', 'file4')
            dst = _(dst_part, 'bad')
            moved = path_move(src, dst, quiet=True, critical=False)
            self.assertFalse(moved)
            self.assertTrue(os.path.isfile(src))
            self.assertTrue(os.path.isfile(dst_part))

            # (bad directory move self container)
            src = _('dir2')
            dst = _('dir2', 'dir3')
            moved = path_move(src, dst, quiet=True, critical=False)
            self.assertFalse(moved)
            self.assertTrue(os.path.isdir(src))
            self.assertTrue(os.path.isdir(dst))

            # (simple directory move)
            src = _('dir2', 'dir3')
            dst = _('dir4')
            moved = path_move(src, dst, critical=False)
            self.assertTrue(moved)
            self.assertFalse(os.path.isdir(src))
            self.assertFalse(os.path.isdir(_(dst, 'dir3')))
            self.assertTrue(os.path.isfile(_(dst, 'file3')))

            # (another directory move)
            src = _('dir4')
            dst = _('dir9', 'dir10')
            moved = path_move(src, dst, critical=False)
            self.assertTrue(moved)
            self.assertFalse(os.path.isdir(src))
            self.assertTrue(os.path.isdir(dst))
            self.assertTrue(os.path.isfile(_(dst, 'file3')))
            self.assertTrue(os.path.isfile(_(dst, 'file4')))
            self.assertTrue(os.path.isdir(_(dst, 'dir5')))

            # (check directory replacing a file)
            src = _('dir9')
            dst = _('file7')
            self.assertTrue(os.path.isdir(src))
            self.assertTrue(os.path.isfile(dst))
            moved = path_move(src, dst, quiet=True, critical=False)
            self.assertTrue(moved)
            self.assertFalse(os.path.isdir(src))
            self.assertTrue(os.path.isdir(dst))

    def test_utilio_optfile(self):
        with prepare_workdir() as work_dir:
            def _(*args):
                return os.path.join(work_dir, *args)

            # setup
            files = [
                _('file1'),
                _('file2.py'),
                _('file3'),
                _('file3.py'),
            ]
            for file in files:
                with open(file, 'a') as f:
                    f.write(file)

            # checks
            src = _('file1')
            target, existence = opt_file(src)
            self.assertTrue(existence)
            self.assertEqual(target, src)

            src = _('file2')
            opt = _('file2.py')
            target, existence = opt_file(src)
            self.assertTrue(existence)
            self.assertEqual(target, opt)

            src = _('file3')
            target, existence = opt_file(src)
            self.assertTrue(existence)
            self.assertEqual(target, src)

            src = _('file4')
            target, existence = opt_file(src)
            self.assertFalse(existence)
            self.assertEqual(target, src)

    def test_utilio_prepare_helpers(self):
        prepared = prepare_arguments(None)
        expected = []
        self.assertEqual(prepared, expected)

        prepared = prepare_arguments({})
        expected = []
        self.assertEqual(prepared, expected)

        args = OrderedDict()
        args['foo'] = 'bar'
        args['xyz'] = ''
        prepared = prepare_arguments(args)
        expected = ['foo', 'bar', 'xyz']
        self.assertEqual(prepared, expected)

        args = OrderedDict()
        args['foo'] = 'bar'
        args['test'] = None
        prepared = prepare_arguments(args)
        expected = ['foo', 'bar']
        self.assertEqual(prepared, expected)

        prepared = prepare_definitions(None)
        expected = []
        self.assertEqual(prepared, expected)

        prepared = prepare_definitions({})
        expected = []
        self.assertEqual(prepared, expected)

        args = OrderedDict()
        args['foo'] = 'bar'
        args['xyz'] = ''
        prepared = prepare_definitions(args)
        expected = ['foo=bar', 'xyz']
        self.assertEqual(prepared, expected)

        args = OrderedDict()
        args['foo'] = 'bar'
        args['test'] = None
        prepared = prepare_definitions(args)
        expected = ['foo=bar']
        self.assertEqual(prepared, expected)

    def test_utilio_remove(self):
        with prepare_workdir() as work_dir:
            def _(*args):
                return os.path.join(work_dir, *args)

            # setup
            directories = [
                _('dir1'),
                _('dir2', 'dir3'),
                _('dir4', 'dir5', 'dir6'),
            ]
            for dir_ in directories:
                os.makedirs(dir_)

            files = [
                _('file1'),
                _('dir2', 'file2'),
                _('dir2', 'dir3', 'file3'),
                _('dir4', 'file4'),
                _('dir4', 'dir5', 'file5'),
                _('dir4', 'dir5', 'dir6', 'file6'),
            ]
            for file in files:
                with open(file, 'a') as f:
                    f.write(file)

            path = _('file7')
            removed = path_remove(path)
            self.assertTrue(removed)
            self.assertFalse(os.path.isfile(path))

            container = _('dir2')
            path = _(container, 'file2')
            removed = path_remove(path)
            self.assertTrue(removed)
            self.assertFalse(os.path.isfile(path))
            self.assertTrue(os.path.isdir(container))
            self.assertFalse(os.path.isfile(path))

            container = _('dir2')
            path = _(container, 'dir3')
            file = _(path, 'file3')
            removed = path_remove(path)
            self.assertTrue(removed)
            self.assertFalse(os.path.isdir(path))
            self.assertFalse(os.path.isfile(file))
            self.assertTrue(os.path.isdir(container))

            path = _('dir4')
            files = [
                _(path, 'file4'),
                _(path, 'dir5', 'file5'),
                _(path, 'dir5', 'dir6', 'file6'),
            ]
            removed = path_remove(path)
            self.assertTrue(removed)
            self.assertFalse(os.path.isdir(path))
            for file in files:
                self.assertFalse(os.path.isfile(file))

            # allow noop calls to be true
            path = _('missing')
            removed = path_remove(path)
            self.assertTrue(removed)

    def test_utilio_runscript(self):
        with prepare_workdir() as work_dir:
            valid_script = os.path.join(work_dir, 'valid')
            with open(valid_script, 'a') as f:
                f.write('test=1\n')

            result = run_script(valid_script, {})
            self.assertEqual(result['test'], 1)

            invalid_script = os.path.join(work_dir, 'invalid')
            with open(invalid_script, 'a') as f:
                f.write('bad-line\n')

            result = run_script(invalid_script, {})
            self.assertIsNone(result)

            with self.assertRaises(NameError):
                run_script(invalid_script, {}, catch=False)

    def test_utilio_shebang_interpreter(self):
        si_dir = os.path.join(self.assets_dir, 'shebang-interpreter')
        si01 = [os.path.join(si_dir, 'interpreter')]
        si02 = [os.path.join(si_dir, 'interpreter-arg')]
        si03 = [os.path.join(si_dir, 'interpreter-args-multiple')]
        si04 = [os.path.join(si_dir, 'interpreter-extremely-long')]
        si05 = [os.path.join(si_dir, 'interpreter-whitespaces')]
        si06 = [os.path.join(si_dir, 'example.py')]

        # encode helper as helper utility will execute with encoded strings
        def E(val):
            rv = []
            for v in val:
                rv.append(v.encode())
            return rv

        # simple interpreter
        self.assertEqual(psi(si01), [b'interpreter'] + E(si01))
        # interpreter with a single argument
        self.assertEqual(psi(si02), [b'interpreter', b'arg'] + E(si02))
        # interpreter with a single argument (with whitespaces)
        self.assertEqual(psi(si03), [b'interpreter', b'arg1 arg2'] + E(si03))
        # too long of an interpreter
        self.assertEqual(psi(si04), si04)
        # interpreter with whitespaces
        self.assertEqual(psi(si05), [b'interpreter'] + E(si05))
        # real example of an interpreter
        self.assertEqual(psi(si06), [b'/usr/bin/env', b'python'] + E(si06))

    def test_utilio_touch(self):
        with prepare_workdir() as work_dir:
            test_file = os.path.join(work_dir, 'test-file')

            created = touch(test_file)
            self.assertTrue(created)

            exists = os.path.isfile(test_file)
            self.assertTrue(exists)

            updated = touch(test_file)
            self.assertTrue(updated)
