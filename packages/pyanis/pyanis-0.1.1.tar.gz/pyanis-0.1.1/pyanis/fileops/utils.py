from shutil import copy2, move
from tqdm import tqdm
import pathlib
import os


def copy_files(filelist, destination, move_files=False):
    """

    Parameters
    ----------
    filelist : list
        List of file names to copy or move.
    destination : str
        Directory of destination.
    move_files : bool
        (Default value = False)
        If this is set to true, this function moves the files isntead of the
        simply creating copies.
    Returns
    -------
    None
        Copies or moves list of files to destination.
        NOTE: it will skip existing files.
    """

    destination = os.path.abspath(destination)
    existing = os.listdir(destination)
    desc = "Moving files.." if move_files else "Copying files.." # noqa

    for f in tqdm(filelist, total=len(filelist), desc=desc):
        if ".ipynb_checkpoints" in str(f):
            continue

        f = pathlib.Path(f)
        if f.parts[-1] in existing:
            continue
        if move_files:
            move(f, destination)
        else:
            copy2(f, destination)

    print(f"Finished copying files to:\n\t{destination}")
