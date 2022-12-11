# -*- coding: utf-8 -*-
import importlib
import importlib.util
import os
import re
import subprocess
import sys

from .morphemes import Morpheme
from .util_external import memoize
from .deps.mecabko import reading as MecabReading

####################################################################################################
# Mecab Morphemizer
####################################################################################################

MECAB_POS_BLACKLIST = [
    'JKV', # vocative case
    'EF', # termination particle
    'EC', # connection particle
    'IC', # interjection
    'NNP', # proper noun
    'NR',  # literal numbers
    'SN',  # numbers
    'SH',  # hanja
    'SL',  # non korean
    'SY',  # ponctuaction
    'SC',  # ponctuaction
    'SSC',  # ponctuaction
    'SSO',  # ponctuaction
    'SE',  # ponctuaction
    'SF',  # ponctuaction
]

MECAB_ENCODING = None

mecab_source = ""

def extract_unicode_block(unicode_block, string):
    """ extracts and returns all texts from a unicode block from string argument.
        Note that you must use the unicode blocks defined above, or patterns of similar form """
    return re.findall(unicode_block, string)


def getMecabIdentity():
    # Initialize mecab before we get the identity
    m = mecab()

    # identify the mecab being used
    return mecab_source

def getMorpheme(parts):
    word = parts[0]
    pos = u'UNKNOWN'
    subPos = u'UNKNOWN'
    norm = word
    base = word
    inflected = word
    reading = word

    if len(parts) > 1:
        pos = parts[1]
    if pos in MECAB_POS_BLACKLIST:
        return None
    m = Morpheme(norm, base, inflected, reading, pos, subPos)
    return m


control_chars_re = re.compile('[\x00-\x1f\x7f-\x9f]')

@memoize
def getMorphemesMecab(e):
    # Remove Unicode control codes before sending to MeCab.
    e = control_chars_re.sub('', e)
    ms = [getMorpheme(m.split('\t')) for m in interact(e).split('\r')]
    ms = [m for m in ms if m is not None]
    return ms


# [Str] -> subprocess.STARTUPINFO -> IO MecabProc
def spawnMecab(base_cmd, startupinfo):
    """Try to start a MeCab subprocess in the given way, or fail.

    Raises OSError if the given base_cmd and startupinfo don't work
    for starting up MeCab, or the MeCab they produce has a dictionary
    incompatible with our assumptions.
    """
    global MECAB_ENCODING

    # [Str] -> subprocess.STARTUPINFO -> IO subprocess.Popen
    def spawnCmd(cmd, startupinfo):
        return subprocess.Popen(cmd, startupinfo=startupinfo, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

    dicinfo_dump = spawnCmd(base_cmd + ['-D'], startupinfo).stdout.read()
    charset_match = re.search(
        '^charset:\t(.*)$', str(dicinfo_dump, 'utf-8'), flags=re.M)
    if charset_match is None:
        raise OSError('Can\'t find charset in MeCab dictionary info (`$MECAB -D`):\n\n'
                      + dicinfo_dump)
    MECAB_ENCODING = charset_match.group(1)

    print(base_cmd)
    return spawnCmd(base_cmd, startupinfo)


@memoize
def mecab():  # IO MecabProc
    """Start a MeCab subprocess and return it.
    `mecab` reads expressions from stdin at runtime, so only one
    instance is needed.  That's why this function is memoized.
    """

    global mecab_source # make it global so we can query it later

    if sys.platform.startswith('win'):
        si = subprocess.STARTUPINFO()
        try:
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        except:
            # pylint: disable=no-member
            si.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
    else:
        si = None

    m = MecabReading.MecabController()
    m.setup()

    print('Using morphman: [%s] with command line [%s]' % (mecab_source, m.mecabCmd))

    return spawnMecab(m.mecabCmd, si), mecab_source


@memoize
def interact(expr):  # Str -> IO Str
    """ "interacts" with 'mecab' command: writes expression to stdin of 'mecab' process and gets all the morpheme
    info from its stdout. """

    p, _ = mecab()
    expr2 = expr.encode(MECAB_ENCODING, 'ignore')
    # expr = expr.encode('utf-8', "ignore")
    p.stdin.write(expr2 + b'\n')
    p.stdin.flush()
    res = '\r'.join([str(p.stdout.readline().rstrip(b'\r\n'), 'utf-8') for l in expr2.split(b'\n')])
    return res
