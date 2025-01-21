#!/usr/bin/env python
import os, sys, subprocess


def get_formatted_name(name):
    """Gets a formatted name that will prevent escaping from the shell.

    Args:
        name (str): The name of the file.

    Returns:
        str: The resulting formatted string.
    """
    accepted_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."
    new_name = ""
    for char in name:
        if not char in accepted_chars:
            new_name += "\\" + char
        else:
            new_name += char
    return new_name


def fix_path(path):
    """Fixes a path if it doesn't have a trailing '/'.

    Args:
        path (str): The path to fix.

    Returns:
        str: The fixed path.
    """
    new_path = ""
    if not path.endswith("/"):
        new_path = path + "/"
    return new_path


def fix_file_extension(file_extension):
    """Fixes a file extension for use with ffmpeg.

    Args:
        file_extension (str): The file extension string.

    Returns:
        str: The fixed file extension.
    """
    output = ""
    if not file_extension.startswith("."):
        output += "."
    output += file_extension
    return output


def main():
    the_args = sys.argv
    if len(the_args) != 5:
        print(
            "Usage: python convert_all.py <src_dir> <dst_dir> <src_file_extension> <dst_file_extension>"
        )
        sys.exit(1)
    src_path = os.path.normpath(the_args[1])
    src_path = fix_path(src_path)
    print("+ Src path:", src_path)
    dst_path = os.path.normpath(the_args[2])
    dst_path = fix_path(dst_path)
    print("+ Dst path:", dst_path)
    src_file_extension = get_formatted_name(the_args[3])
    src_file_extension = fix_file_extension(src_file_extension)
    print("+ Src file extension:", src_file_extension)
    dst_file_extension = get_formatted_name(the_args[4])
    dst_file_extension = fix_file_extension(dst_file_extension)
    print("+ Dst file extension:", dst_file_extension)

    print(
        '+ Do conversion from "',
        src_file_extension,
        '" to "',
        dst_file_extension,
        '"',
        sep="",
    )

    files_to_convert = []
    # loop through source files
    for src_file_name in os.listdir(src_path):
        if src_file_name.endswith(src_file_extension):
            # if we have a file that is of the extension we want, look to see
            # if there is already one in the destination folder
            already_exists = False
            for dst_file_name in os.listdir(dst_path):
                if dst_file_name.endswith(dst_file_extension):
                    # change the outer file name to see if it matches this one
                    modified_name = (
                        src_file_name[: src_file_name.rfind(src_file_extension)]
                        + dst_file_extension
                    )

                    if modified_name == dst_file_name:
                        already_exists = True
                        break

            # now check to do conversion
            if not already_exists:
                files_to_convert.append(src_file_name)
            else:
                print('+ "', src_file_name, '"', " already exists!", sep="")

    print("\n\n+ Files to convert:")
    print("+ [")
    for src_file_name in files_to_convert:
        print("+ \t", src_file_name, ",", sep="")
    print("+ ]")

    if len(files_to_convert) > 0:
        print("\n\n+ ---BEGIN CONVERSION---")
    else:
        print("\n\n+ Nothing to convert!")

    for src_file_name in files_to_convert:
        src_file_name = get_formatted_name(src_file_name)
        print("\n+ Converting", src_file_name, "...")
        dst_file_name = ""
        if src_file_name.endswith(src_file_extension):
            # change the src file name
            modified_name = (
                src_file_name[: src_file_name.rfind(src_file_extension)]
                + dst_file_extension
            )
            dst_file_name = get_formatted_name(modified_name)
            print("+ The Destination File:", dst_file_name)

        command = (
            "ffmpeg -i " + src_path + src_file_name + " " + dst_path + dst_file_name
        )
        print("+ Command:", command)
        # Wait for this to finish executing
        subprocess.Popen(command, shell=True).wait()


if __name__ == "__main__":
    main()
