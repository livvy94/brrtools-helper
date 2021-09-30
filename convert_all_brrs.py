import os
import pathlib
import shlex
import subprocess

current_directory = os.path.dirname(os.path.abspath(__file__))
all_wav_files = list(pathlib.Path(current_directory).glob('*.wav'))


def main():
    if len(all_wav_files) < 1:
        print("No WAV files found! Put some in this folder, then run the script again.")
        return

    brr_encoder_path = load_brrtools_path()

    for wavpath in all_wav_files:
        loop = get_loop(wavpath)
        command = get_command(brr_encoder_path, wavpath, loop)
        subprocess.run(shlex.split(command))  # This is better than using os.system()


def get_loop(wavpath):
    # TODO: does it detect unlooped WAVs correctly? Also there is probably a cleaner way to do this.
    with wavpath.open(mode="rb") as file:
        wav_filedata = file.read()
        offset = wav_filedata.find(b'smpl') + 52  # The loop point is 52 bytes after the "smpl" string
        file.seek(offset)
        return int.from_bytes(file.read(2), byteorder="little")  # Read it from that offset


def get_command(brr_encoder_path, wavpath, loop):
    message = ""
    result = ""
    if loop != 0:
        message = f"  ~ Converting {wavpath.name} with loop point {loop} ~"
        result = f"\"{brr_encoder_path}\" -l{loop} -m -g \"{wavpath.name}\" \"{wavpath.stem}.brr\""
    else:
        message = f"***** Converting {wavpath.name}, unlooped *****"
        result = f"\"{brr_encoder_path}\" -m -g \"{wavpath.name}\" \"{wavpath.stem}.brr\""

    print()
    print(message)
    return result


def load_brrtools_path():
    result = ""
    filename = pathlib.Path("encoder_path.txt")

    if (filename.is_file() == False):
        print("Please paste in brr_encoder.exe's filepath:")
        result = input().replace('\"', '')
        with open(filename, "w") as file:
            file.write(result)  # save the filepath for later
        return result

    with open(filename, 'r') as file:  # https://www.pythontutorial.net/python-basics/python-read-text-file/
        return file.read()


main()
