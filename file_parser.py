import sys
from pathlib import Path

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

REGISTER_EXTENSION = { "JPEG": JPEG_IMAGES, "JPG": JPG_IMAGES, "PNG": PNG_IMAGES, "SVG": SVG_IMAGES,
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


if __name__ == "__main__":
    folder_to_scan = sys.argv[1]
    print(f"Start in folder {folder_to_scan}")
    scan_and_transfer(Path(folder_to_scan))
    # print(f"Images jpeg: {JPEG_IMAGES}")
    # print(f"Images jpg: {JPG_IMAGES}")
    # print(f"Images svg: {SVG_IMAGES}")
    # print(f"Audio mp3: {MP3_AUDIO}")
    # print(f"Zip archives: {ZIP_ARCHIVES}")

    print(f"Types of files in folder: {EXTENSION}")
    print(f"Unknown files of types: {UNKNOWN}")
    print(f"Not sorted: {MY_OTHER}")

    # print(FOLDERS)