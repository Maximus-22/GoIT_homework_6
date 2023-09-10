from pathlib import Path
import re, shutil


# Section of Normalize
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", \
               "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", \
               "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}

for cyr_symb, letter in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyr_symb)] = letter
    TRANS[ord(cyr_symb.upper())] = letter.upper()


def normalize(name: str) -> str:
    transl_name = name.translate(TRANS)
    transl_name = re.sub(r"[^a-zA-Z0-9_\.]", "_", transl_name)
    return transl_name


# Section of Parser
GIF_IMAGES = []
JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []

AVI_VIDEO = []
MKV_VIDEO = []
MOV_VIDEO = []
MP4_VIDEO = []

AMR_AUDIO = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []

DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
PDF_DOCUMENTS = []
PPTX_DOCUMENTS = []
TXT_DOCUMENTS = []
XLS_DOCUMENTS = []
XLSX_DOCUMENTS = []

GZTAR_ARCHIVES = []
TAR_ARCHIVES = []
ZIP_ARCHIVES = []

MY_OTHER = []

REGISTER_EXTENSION = { "GIF": GIF_IMAGES, "JPEG": JPEG_IMAGES, "JPG": JPG_IMAGES, "PNG": PNG_IMAGES, "SVG": SVG_IMAGES,
                       "AVI": AVI_VIDEO, "MKV": MKV_VIDEO,"MOV": MOV_VIDEO, "MP4": MP4_VIDEO,
                       "AMR": AMR_AUDIO, "MP3": MP3_AUDIO,"OGG": OGG_AUDIO, "WAV": WAV_AUDIO,
                       "DOC": DOC_DOCUMENTS, "DOCX": DOCX_DOCUMENTS,"PDF": PDF_DOCUMENTS, "PPTX": PPTX_DOCUMENTS,
                       "TXT": TXT_DOCUMENTS, "XLS": XLS_DOCUMENTS, "XLSX": XLSX_DOCUMENTS, 
                       "GZ": GZTAR_ARCHIVES, "TAR": TAR_ARCHIVES, "ZIP": ZIP_ARCHIVES}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()

def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()  # перетворюємо розширення файлу на назву папки jpg -> JPG

def scan_and_transfer(folder: Path) -> None:
    for item in folder.iterdir():
        # Якщо це папка то додаємо її до списку FOLDERS і переходимо до наступного елемента папки
        if item.is_dir():
            # перевіряємо, щоб папка не була тією в яку ми складаємо вже файли
            if item.name not in ("archives", "video", "audio", "documents", "images", "MY_OTHER"):
                FOLDERS.append(item)
                # скануємо вкладену папку
                scan_and_transfer(item)  # рекурсія
            continue  # переходимо до наступного елементу в сканованій папці

        #  Робота з файлом
        ext = get_extension(item.name)  # беремо розширення файлу
        fullname = folder / item.name  # беремо шлях до файлу
        if not ext:  # якщо файл немає розширення то додаєм до невідомих
            MY_OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                # Якщо ми не зареєстрували розширення у REGISTER_EXTENSION, то додаємо до невідомих
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)


# Premium Section
def handle_defined(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)  # робимо папку для архіва
    # filename.replace(target_folder / normalize(filename.name))
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ""))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    
    try:
        if filename.suffix[1:].casefold() == "gz":
            shutil.unpack_archive(filename, folder_for_file, "gztar")  # TODO: Check!
        elif filename.suffix[1:].casefold() == "tar":
            shutil.unpack_archive(filename, folder_for_file, "tar")
        else:
            shutil.unpack_archive(filename, folder_for_file, "zip")
        
        filename.unlink()        
    
    except shutil.ReadError:
        print(f"File {filename} is not archive!")
        filename.replace(target_folder / normalize(filename.name))
        folder_for_file.rmdir()

    # filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can\'t delete folder: {folder}")


def files_runner(folder: Path):
    scan_and_transfer(folder)
    for file in GIF_IMAGES:
        handle_defined(file, folder / "images" / "GIF")
    for file in JPEG_IMAGES:
        handle_defined(file, folder / "images" / "JPEG")
    for file in JPG_IMAGES:
        handle_defined(file, folder / "images" / "JPG")
    for file in PNG_IMAGES:
        handle_defined(file, folder / "images" / "PNG")
    for file in SVG_IMAGES:
        handle_defined(file, folder / "images" / "SVG")
        
    for file in AVI_VIDEO:
        handle_defined(file, folder / "video" / "AVI")
    for file in MKV_VIDEO:
        handle_defined(file, folder / "video" / "MKV")
    for file in MOV_VIDEO:
        handle_defined(file, folder / "video" / "MOV")
    for file in MP4_VIDEO:
        handle_defined(file, folder / "video" / "MP4")

    for file in AMR_AUDIO:
        handle_defined(file, folder / "audio" / "AMR")
    for file in MP3_AUDIO:
        handle_defined(file, folder / "audio" / "MP3")
    for file in OGG_AUDIO:
        handle_defined(file, folder / "audio" / "OGG")
    for file in WAV_AUDIO:
        handle_defined(file, folder / "audio" / "WAV")

    for file in DOC_DOCUMENTS:
        handle_defined(file, folder / "documents" / "DOC")
    for file in DOCX_DOCUMENTS:
        handle_defined(file, folder / "documents" / "DOCX")
    for file in PDF_DOCUMENTS:
        handle_defined(file, folder / "documents" / "PDF")
    for file in PPTX_DOCUMENTS:
        handle_defined(file, folder / "documents" / "PPTX")
    for file in TXT_DOCUMENTS:
        handle_defined(file, folder / "documents" / "TXT")
    for file in XLS_DOCUMENTS:
        handle_defined(file, folder / "documents" / "XLS")
    for file in XLSX_DOCUMENTS:
        handle_defined(file, folder / "documents" / "XLSX")

    for file in GZTAR_ARCHIVES:
        handle_archive(file, folder / "archives")
    for file in TAR_ARCHIVES:
        handle_archive(file, folder / "archives")
    for file in ZIP_ARCHIVES:
        handle_archive(file, folder / "archives")

    for file in MY_OTHER:
        handle_other(file, folder / "MY_OTHER")

    # Garbage collector
    for folder in FOLDERS[::-1]:
        handle_folder(folder)


def main(source_folder):
    try:
        folder_for_scan = Path(source_folder)
        print(f"Start in folder: {folder_for_scan.resolve()}")
        files_runner(folder_for_scan.resolve())
    except OSError:
        print(f"Folder {source_folder} not found.")
        quit()



if __name__ == "__main__":
    main("Мотлох")