import argparse
import glob
import subprocess
import os
import json
import shutil
from colorama import Fore

with open("config.json") as file:
    data = json.load(file)

# Config
PARPAR = data["PARPAR"]
NYUU = data["NYUU"]
NYUU_CONFIG = data["NYUU_CONFIG"]

def get_mkv_files(input_path: str) -> list[str]:
    mkv_files = list(glob.glob(pathname="**/*.mkv", root_dir=input_path, recursive=True))
    return mkv_files

def parpar(input_path, move=False) -> None:
    args = "-s700k --slice-size-multiple=700K --max-input-slices=4000 -r1n*1.2 -R --filepath-format basename -o"
    if len(get_mkv_files(input_path)) != 0:
        for file in get_mkv_files(input_path):
            file_without_ext = os.path.splitext(file)[0]
            # check if move is True, if yes, it will move the files
            if move is not False:
                # Create a directory to move the files
                try:
                    destination_folder_path = os.path.join(input_path, file_without_ext)
                    os.makedirs(destination_folder_path, exist_ok= False)
                except FileExistsError:
                    print("Folder already exists, jumping...")
                
                # move the files to the new directory
                shutil.move(os.path.join(input_path, file), destination_folder_path)
                input_path_new = destination_folder_path

                parpar_cmd = f'{PARPAR} {args} "{file_without_ext}" "{file}"'
                print(Fore.GREEN + f"Generating PAR2 files for {file} with parpar\n")
                subprocess.run(parpar_cmd, cwd=input_path_new)
            else:
                parpar_cmd = f'{PARPAR} {args} "{file_without_ext}" "{file}"'
                print(Fore.GREEN + f"Generating PAR2 files for {file} with parpar\n")
                subprocess.run(parpar_cmd, cwd=input_path)
        print("All files were compressed")
    else:
        print("0 .mkv found, please put a valid path")

def nyuu(input_path: str) -> None:
    args = f'-C "{NYUU_CONFIG}" -o'
    if len(get_mkv_files(input_path)) != 0:
        for file in get_mkv_files(input_path):
            # get the file name without the extension
            file_without_ext = os.path.splitext(file)[0]
            # get the file name without extension + folder location
            file_without_ext2 = os.path.splitext(os.path.basename(file))[0]

            # search for all the par2 files that have the same name as the mkv file
            par2_files = list(glob.glob(pathname=f"{glob.escape(file_without_ext)}*.par2", root_dir=input_path, recursive=True))
            filtered_par2_files = [par2_file for par2_file in par2_files if file_without_ext in par2_file]
            par2_files_str = " ".join([f'"{par2_file}"' for par2_file in filtered_par2_files])

            nyuu_cmd = f'{NYUU} {args} "{file_without_ext2}.nzb" "{file}" {par2_files_str}'
            print(nyuu_cmd)
            if os.path.isfile(os.path.join(input_path, f"{file_without_ext}.nzb")):
                print(Fore.YELLOW + f"{file_without_ext2}.nzb already exists, skipping...")
                continue
            else:
                print(Fore.GREEN + f"Uploading {file} along with PAR2 files with nyuu\n")
                subprocess.run(nyuu_cmd, cwd=input_path)
    else:
        print("0 .mkv found, please put a valid path")

def main():
    parser = argparse.ArgumentParser(description="A script for uploading MKV files to usenet")
    parser.add_argument("path", type=str, help="Path to directory containing .mkv files")
    parser.add_argument("-p", "--parpar", action="store_true", help="Only run Parpar")
    parser.add_argument("-n", "--nyuu", action="store_true", help="Only run Nyuu")
    parser.add_argument("-m", "--move", action="store_true", help="Allow the script to create folders and move the files")
    args = parser.parse_args()

    # check if script has the args -p and -m
    if args.parpar and args.move:
        parpar(args.path, move=True)
    # if only -p is passed, run parpar without moving the files
    elif args.parpar:
        parpar(args.path)

    elif args.nyuu:
        nyuu(args.path)
    
    elif args.move:
        parpar(args.path, move=True)
        nyuu(args.path)
    # if no args are passed, run parpar and nyuu
    else:
        parpar(args.path)
        nyuu(args.path)


if __name__ == "__main__":
    main()
