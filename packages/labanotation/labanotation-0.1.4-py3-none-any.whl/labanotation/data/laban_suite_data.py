from pathlib import Path

import gdown


base_url = 'https://raw.githubusercontent.com/microsoft/LabanotationSuite/master/GestureAuthoringTools/LabanEditor/data_input/'  # NOQA


def get_laban_suite_sample_data():
    filenames = [
        'Ges01_wavehand.csv',
        'Ges02_balancinghands.csv',
        'Ges03_drawlines.csv',
        'Ges04_comehere.csv',
        'Ges05_demopoint.csv',
        'Ges06_chickenwing.csv',
    ]
    filepaths = []
    for fn in filenames:
        filepath = gdown.cached_download(
            url=f"{base_url}/{fn}",
            quiet=True,
        )
        filepaths.append(Path(filepath))
    return filepaths
