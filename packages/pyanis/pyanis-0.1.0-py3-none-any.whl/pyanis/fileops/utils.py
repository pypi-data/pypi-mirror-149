from shutil import copy2, move
from tqdm import tqdm
import pathlib
import os

def copy_files(filelist, destination, move_files=False):
    """

    Parameters
    ----------
    filelist :
        
    destination :
        
    move_files :
        (Default value = False)

    Returns
    -------

    
    """

    destination = os.path.abspath(destination)
    
    existing = os.listdir(destination)
    
    desc = "Moving files.." if move_files else "Copying files.."
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