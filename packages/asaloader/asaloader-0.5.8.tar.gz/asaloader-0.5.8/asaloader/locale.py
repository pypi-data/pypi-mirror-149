# -*- coding: utf-8 -*-
"""負責處理語系載入
"""

from os import path

import gettext
import locale
import sys

__all__ = ['_']


def _(s: str) -> str:
    """字串翻譯函式

    此函式會將傳入的字串，依據設定的語系，轉換成對應的翻譯字串，
    如果沒有設定與細則會回傳傳入的字串。

    可透過 update_lc 來更新使用的語系，並且此函式會因為 update_lc 的呼叫，
    而有不同的 Reference。

    Args:
        s (str): 待翻譯的字串。

    Returns:
        str: 翻譯後的字串。

    Examples:
        有設定語系

        >>> update_lc('zh_TW')
        >>> _('test')
        測試

        沒有設定語系

        >>> _('test')
        test
    """
    ...


def get_shell_lc() -> str:
    """取得當前shell的語言代碼。

    Returns:
        str: 當前shell的語言代碼。
    """
    loc = locale.getdefaultlocale()
    lc = loc[0]

    return lc


def update_lc() -> None:
    """依據語言代碼更新當前應用的語系

    此函式會解析 sys.argv 傳入的參數，取得設定的語系，
    去更新字串翻譯函式`_`。

    若 sys.argv 沒有，則使用 shell 的語言代碼，
    去更新字串翻譯函式`_`。
    
    """

    package_dir = path.abspath(path.dirname(__file__))
    locale_dir = path.join(package_dir, 'locale')

    lc = None
    if '--lc' in sys.argv:
        i = sys.argv.index('--lc')
        if len(sys.argv) > i + 1:
            lc = sys.argv[i + 1]

    if lc is None:
        lc = get_shell_lc()

    global _

    if gettext.find('asaloader', locale_dir, [lc]):
        translate = gettext.translation('asaloader', locale_dir, [lc])
        _ = translate.gettext
    else:
        translate = None
        def _(s): return s


update_lc()
