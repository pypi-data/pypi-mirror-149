# -*- coding: utf-8 -*-
"""處理i10n的相關檔案
"""

import glob
import pathlib
import os
import subprocess

from typing import List

def create_pot():
    """讀取所有py檔案，生成pot翻譯樣板。
    """
    py_parser = 'asaloader/*.py'
    py_files = glob.glob(py_parser)
    with open('build/py-file-list.txt', 'w+') as f:
        for py_file in py_files:
            f.write(py_file)
            f.write('\n')
    subprocess.run([
        'xgettext',
        '--files-from=build/py-file-list.txt',
        '-d', 'asaloader',
        '-o', 'asaloader/locale/asaloader.pot',
        '--from-code=utf-8']
    )


def create_mo_files() -> List[str]:
    """將所有翻譯檔.po編譯成.mo。

    Returns:
        List[str]: .mo檔案的列表。
    """
    po_parser = 'asaloader/locale/*/LC_MESSAGES/asaloader.po'
    mo_files = []
    po_files = glob.glob(po_parser)

    for po_file in po_files:
        mo_file = po_file.replace('.po', '.mo')
        subprocess.run(['msgfmt', '-o', mo_file, po_file], check=True)
        mo_files.append(mo_file)

    return [(os.path.split(mo_file)[0], [mo_file]) for mo_file in mo_files]


def get_l10n_files() -> List[str]:
    """取得所有翻譯相關檔案列表，包括.pot .po .mo。

    Returns:
        List[str]: 翻譯相關檔案列表，包括.pot .po .mo。
    """
    po_parser = 'asaloader/locale/*/LC_MESSAGES/asaloader.po'
    pot_file = 'asaloader/locale/asaloader.pot'
    po_files = glob.glob(po_parser)
    mo_files = [po_file.replace('.po', '.mo') for po_file in po_files]

    files = [pot_file] + po_files + mo_files
    return files


if __name__ == "__main__":
    create_pot()
    create_mo_files()
    print(get_l10n_files())
