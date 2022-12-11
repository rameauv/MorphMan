# -*- coding: utf-8 -*-

import sys
import os
import platform
import re
import subprocess

try:
    import aqt.utils
    from anki.utils import stripHTML, isWin, isMac
    from anki.hooks import addHook
    from aqt import mw
    from aqt.qt import *
    from aqt.utils import showInfo
    config = mw.addonManager.getConfig(__name__)
except:
    isMac = sys.platform.startswith("darwin")
    isWin = sys.platform.startswith("win32")
    pass

supportDir = os.path.join(os.path.dirname(__file__))

if sys.platform == "win32":
    si = subprocess.STARTUPINFO()
    try:
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    except:
        si.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
else:
    si = None

# Mecab
##########################################################################


def mungeForPlatform(popen):
    if isWin:
        popen = [os.path.normpath(x) for x in popen]
        popen[0] += ".exe"
    elif not isMac:
        popen[0] += ".lin"
    return popen


class MecabController(object):

    def __init__(self):
        self.mecab = None

    def setup(self):
        self.mecabCmd = mungeForPlatform(
            [os.path.join(supportDir, "mecab")] + [
                '-d', "/usr/local/lib/mecab/dic/mecab-ko-dic", '--node-format=%m\t%f[0]\r', '--eos-format=\n'])
        self.mecabCmdAlt = mungeForPlatform([
            os.path.join(supportDir, "mecab"),
            "-d", "/usr/local/lib/mecab/dic/mecab-ko-dic", '--node-format=%m\t%f[0]\r', '--eos-format=\n'
        ])
        os.environ['DYLD_LIBRARY_PATH'] = supportDir
        os.environ['LD_LIBRARY_PATH'] = supportDir
        if not isWin:
            os.chmod(self.mecabCmd[0], 0o755)

    def ensureOpen(self, details=False):
        if not self.mecab:
            self.setup()
            if details:
                cmd = self.mecabCmdAlt
            else:
                cmd = self.mecabCmd
            try:
                self.mecab = subprocess.Popen(
                    cmd, bufsize=-1, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    startupinfo=si)
            except OSError:
                raise Exception(
                    "Please ensure your Linux system has 64 bit binary support.")

    def accents(self, text):
        self.ensureOpen(True)
        self.mecab.stdin.write(text + b"\n")
        self.mecab.stdin.flush()
        results, err = self.mecab.communicate()
        results = results.decode('utf-8', "ignore").split("\n")
        self.mecab = None

        return results

    def reading(self, expr):

        self.ensureOpen()
        print(expr.encode('utf-8', "ignore") + b'\n')
        self.mecab.stdin.write(expr.encode('utf-8', "ignore") + b'\n')
        self.mecab.stdin.flush()
        expr = self.mecab.stdout.readline().rstrip(b'\r\n').decode('utf-8', "ignore")
        return expr

# Init
##########################################################################

mecab = MecabController()

# Tests
##########################################################################

if __name__ == "__main__":
    expr = "이 의자 정말 편안하다! 어디서 샀어?"
    print(mecab.reading(expr))
