import sys
import pathlib
import shutil

suffix_dict = {
    'JPEG': 'images', 'PNG': 'images', 'JPG': 'images', 'SVG': 'images', 'BMP': 'images',
    'AVI': 'video', 'MP4': 'video', 'MOV': 'video', 'MKV': 'video',
    'DOC': 'documents', 'DOCX': 'documents', 'TXT': 'documents', 'PDF': 'documents',
    'XLS': 'documents', 'XLSX': 'documents', 'PPTX': 'documents',
    'MP3': 'audio', 'OGG': 'audio', 'WAV': 'audio', 'AMR': 'audio',
    'ZIP': 'archives', 'GZ': 'archives', 'TAR': 'archives',
}
files_dict = {'images': [], 'video': [], 'documents': [],
              'audio': [], 'archives': [], 'unknown': []}
known_suffix = set()
unknown_suffix = set()
folders_list = []

def write_dict(path):  # save files_dict, known_suffix, unknown_suffix
    with open(path / "TS_FileList.txt", 'w') as f:
        for categ in files_dict.keys():
            if len(files_dict[categ]) > 0:
                f.write(f'>>> {categ}\n')
                for file in files_dict[categ]:
                    f.write(f'{file}\n')

    with open(path / "TS_SuffixKnown.txt", 'w') as f:
        for suf in known_suffix:
            f.write(f'{suf}\n')

    with open(path / "TS_SuffixUnknown.txt", 'w') as f:
        for suf in unknown_suffix:
            f.write(f'{suf}\n')


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s",
               "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")


def normalize(name):
    newname = ""
    for ch in name:
        newname += (ch if ch.isalnum() else '_')

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    return newname.translate(TRANS)


def select_file(path):  # fill files_dict() depending on  file suffix
    suf = path.suffix[1:].upper()
    categ = suffix_dict.get(suf)
    if categ:
        files_dict[categ].append(path)
        known_suffix.add(suf)
    else:
        files_dict['unknown'].append(path)
        unknown_suffix.add(suf)


def view_folder(path):  # view & preparing files & folders 
    for file in path.iterdir():
        if file.is_dir():
            folders_list.append(file)
            view_folder(file)
        else:
            select_file(file)
    folders_list.sort(key=lambda Path: len(Path.parts), reverse=True)


def check_folders(path):  # create & fill new folder for nonempty category
    for categ in files_dict.keys():
        # not empty
        if (categ != 'unknown') and (len(files_dict[categ]) > 0):
            try:
                pathlib.Path.mkdir(path/categ)
            except FileExistsError:
                continue


def move_files(path):
    for categ in files_dict.keys():
        for file in files_dict[categ]:
            stem = normalize(file.stem)
            newname = (path/categ/(stem+file.suffix) if categ !=
                       'unknown' else file.parent/(stem+file.suffix))
            # .replace(newname) doesn't need try..except
            file.replace(newname)


def unpack_archives(path):  # remove archive files into archives folders
    archivpath = path/'archives'
    if archivpath.exists():
        for arch in archivpath.iterdir():
            shutil.unpack_archive(arch, archivpath/arch.stem)
            pathlib.Path.unlink(arch)


def sweep_folders():
    for fold in folders_list:
        if fold.name not in files_dict.keys():
            if any(fold.iterdir()):  # not empty => normalize
                newname = normalize(fold.name)
                if newname != fold.name:
                    try:
                        fold.rename(fold.parent / newname)
                    except FileExistsError:
                        continue
            else:   # empty
                try:
                    pathlib.Path.rmdir(fold)
                except OSError:
                    continue


def main():
    if len(sys.argv) < 2:
        print("ERROR: working directory not specified")
        exit()

    workpath = pathlib.Path(sys.argv[1])
    if not workpath.exists():
        print("ERROR: working directory not exist")
        exit()

    view_folder(workpath)
    write_dict(workpath)

    check_folders(workpath)
    move_files(workpath)
    unpack_archives(workpath)
    sweep_folders()


if __name__ == "__main__":
    main()
