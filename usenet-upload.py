import argparse
import glob
import subprocess
import os
from colorama import Fore

# Config
PARPAR = ["parpar.exe"]
NYUU = ["nyuu.exe"]
NYUU_CONFIG = "config.json"

def get_mkv_files(input_path: str) -> list[str]:
    mkv_files = list(glob.glob(pathname="*.mkv", root_dir=input_path))
    return mkv_files

def parpar(input_path: str) -> None:
    args = ['-s700k', '--slice-size-multiple=700K', '--max-input-slices=4000', '-r1n*1.2', '-R', '--filepath-format', 'basename', '-o']
    for file in get_mkv_files(input_path):
        file_without_ext = os.path.splitext(file)[0]
        parpar_cmd = PARPAR + args + [file_without_ext, file]
        print(Fore.GREEN + f"Generating PAR2 files for {file} with parpar\n")
        subprocess.run(parpar_cmd, cwd=input_path)

def nyuu(input_path: str) -> None:
    args = ["-C", NYUU_CONFIG, "-o"]
    for file in get_mkv_files(input_path):
        file_without_ext = os.path.splitext(file)[0]
        par2_files = list(glob.glob(pathname=f"{glob.escape(file_without_ext)}*.par2", root_dir=input_path))
        nyuu_cmd = NYUU + args + [f"{file_without_ext}.nzb", file] + par2_files
        print(Fore.GREEN + f"Uploading {file} along with PAR2 files with nyuu\n")
        subprocess.run(nyuu_cmd, cwd=input_path)

def main():
    parser = argparse.ArgumentParser(description="A script for uploading MKV files to usenet")
    parser.add_argument("path", type=str, help="Path to directory containing .mkv files")
    parser.add_argument("-p", "--parpar", action="store_true", help="Only run Parpar")
    parser.add_argument("-n", "--nyuu", action="store_true", help="Only run Nyuu")
    args = parser.parse_args()

    if args.parpar:
        parpar(args.path)

    elif args.nyuu:
        nyuu(args.path)
    
    else:
        parpar(args.path)
        nyuu(args.path)


if __name__ == "__main__":
    main()
