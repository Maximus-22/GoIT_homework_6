from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize


def handle_defined(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)  # робимо папку для архіва
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ""))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)  # TODO: Check!
    except shutil.ReadError:
        print(f"File {filename} is not archive")
        folder_for_file.rmdir()
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can\'t delete folder: {folder}")


def main(folder: Path):
    parser.scan_and_transfer(folder)
    for file in parser.JPEG_IMAGES:
        handle_defined(file, folder / "images" / "JPEG")
    for file in parser.JPG_IMAGES:
        handle_defined(file, folder / "images" / "JPG")
    for file in parser.PNG_IMAGES:
        handle_defined(file, folder / "images" / "PNG")
    for file in parser.SVG_IMAGES:
        handle_defined(file, folder / "images" / "SVG")
        
    for file in parser.AVI_VIDEO:
        handle_defined(file, folder / "video" / "AVI")
    for file in parser.MKV_VIDEO:
        handle_defined(file, folder / "video" / "MKV")
    for file in parser.MOV_VIDEO:
        handle_defined(file, folder / "video" / "MOV")
    for file in parser.MP4_VIDEO:
        handle_defined(file, folder / "video" / "MP4")

    for file in parser.AMR_AUDIO:
        handle_defined(file, folder / "audio" / "AMR")
    for file in parser.MP3_AUDIO:
        handle_defined(file, folder / "audio" / "MP3")
    for file in parser.OGG_AUDIO:
        handle_defined(file, folder / "audio" / "OGG")
    for file in parser.MP3_AUDIO:
        handle_defined(file, folder / "audio" / "MP3")

    for file in parser.DOC_DOCUMENTS:
        handle_defined(file, folder / "documents" / "DOC")
    for file in parser.DOCX_DOCUMENTS:
        handle_defined(file, folder / "documents" / "DOCX")
    for file in parser.PDF_DOCUMENTS:
        handle_defined(file, folder / "documents" / "PDF")
    for file in parser.PPTX_DOCUMENTS:
        handle_defined(file, folder / "documents" / "PPTX")
    for file in parser.TXT_DOCUMENTS:
        handle_defined(file, folder / "documents" / "TXT")
    for file in parser.XLS_DOCUMENTS:
        handle_defined(file, folder / "documents" / "XLS")
    for file in parser.XLSX_DOCUMENTS:
        handle_defined(file, folder / "documents" / "XLSX")

    for file in parser.GZ_ARCHIVES:
        handle_archive(file, folder / "archives")
    for file in parser.TAR_ARCHIVES:
        handle_archive(file, folder / "archives")
    for file in parser.ZIP_ARCHIVES:
        handle_archive(file, folder / "archives")

    for file in parser.MY_OTHER:
        handle_other(file, folder / "MY_OTHER")

    # Garbage collector
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


if __name__ == "__main__":
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f"Start in folder: {folder_for_scan.resolve()}")
        main(folder_for_scan.resolve())