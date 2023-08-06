import os  # pragma: no cover
import glob  # pragma: no cover
import shutil  # pragma: no cover
from tqdm import tqdm  # pragma: no cover


def flatten_files(basic_root):  # pragma: no cover
    """ copies files from deep nested directories into a single one with unique names
    :param basic_root: e.g. `"/home/myuser/data/werke/drei-abhandlungen-zur-sexualtheorie"`
    :type basic_root: str

    :return: A list of new filenames
    :rtype: list
    """
    glob_pattern = f"{basic_root}/**/*.xml"
    werk = basic_root.split('/')[-1]
    files = glob.glob(
        glob_pattern,
        recursive=True
    )
    storage_location = os.path.join('/', *basic_root.split('/')[:-1])
    new_files = []
    for x in tqdm(files, total=len(files)):
        unique_name = x[len(basic_root) - len(werk):]
        parts = unique_name.split('/')
        new_fn = "__".join(parts)
        target = os.path.join(storage_location, new_fn)
        shutil.copy(x, target)
        new_files.append(target)
    return new_files
