import os
from pathlib import Path
from datetime import date

from .functions import get_client_and_project, get_date


def create_mv_folder(projectpath: str, verbose: bool):
    p = Path(projectpath)
    mv_probe = p.joinpath("MV")
    print(f"Probing {mv_probe}...") if verbose else None
    mv_subfolders = []
    for x in [x for x in Path(mv_probe).iterdir() if x.is_dir()]:
        if str(x.stem[0:2]).isdigit():
            mv_subfolders.append(str(x.stem[0:2]))

    newfolder = str(int(max(mv_subfolders))+1).zfill(2)
    projectcode = get_client_and_project(projectpath)

    foldername = f"{newfolder}_{get_date()}_{projectcode}_{os.getlogin()}_Briefing"
    resultpath = mv_probe.joinpath(foldername)
    os.mkdir(resultpath)
    return resultpath
