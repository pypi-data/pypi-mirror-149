# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2021-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxrun.tests import Test


class LTPTest(Test):
    devices = ["qemu-*", "fvp-aemva"]
    cmdfile: str = ""
    need_test_definition = True

    def render(self, **kwargs):
        kwargs["name"] = self.name
        kwargs["timeout"] = self.timeout
        kwargs["cmdfile"] = (
            self.cmdfile if self.cmdfile else self.name.replace("ltp-", "")
        )

        return self._render("ltp.yaml.jinja2", **kwargs)


class LTPController(LTPTest):
    name = "ltp-controllers"
    timeout = 90


class LTPFcntlLockTests(LTPTest):
    name = "ltp-fcntl-locktests"
    timeout = 2


class LTPFSBind(LTPTest):
    name = "ltp-fs_bind"
    timeout = 25


class LTPFSPermsSimple(LTPTest):
    name = "ltp-fs_perms_simple"
    timeout = 2


class LTPFSX(LTPTest):
    name = "ltp-fsx"
    timeout = 1


class LTPNPTL(LTPTest):
    name = "ltp-nptl"
    timeout = 15


class LTPSmoke(LTPTest):
    name = "ltp-smoke"
    cmdfile = "smoketest"
    timeout = 2
