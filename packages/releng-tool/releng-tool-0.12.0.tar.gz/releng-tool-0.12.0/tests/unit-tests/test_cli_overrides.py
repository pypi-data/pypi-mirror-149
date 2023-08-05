# -*- coding: utf-8 -*-
# Copyright 2022 releng-tool

from tests import prepare_testenv
import os
import unittest

class TestCliOverrides(unittest.TestCase):

    def test_cli_overrides(self):
        cfg = {
            'injected_kv': {
                'TEST_OVERRIDE': '123',
            },
        }
        expected_file_flag = 'override-detected'

        with prepare_testenv(config=cfg, template='override-check') as engine:
            engine.run()

            file_flag = os.path.join(engine.opts.target_dir, expected_file_flag)
            self.assertTrue(os.path.exists(file_flag))
