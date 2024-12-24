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
    print("+ Src file extension:", src_file_extension)
    dst_file_extension = get_formatted_name(the_args[4])
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
    for file in os.listdir(src_path):
        if file.endswith(src_file_extension):
            # if we have a file that is of the extension we want, look to see
            # if there is already one in the destination folder
            already_exists = False
            for inner_file in os.listdir(dst_path):
                if inner_file.endswith(dst_file_extension):
                    # change the outer file name to see if it matches this one
                    modified_name = (
                        file[: file.rfind(src_file_extension)] + dst_file_extension
                    )

                    if modified_name == inner_file:
                        already_exists = True
                        break

            # now check to do conversion
            if not already_exists:
                files_to_convert.append(file)
            else:
                print('+ "', file, '"', " already exists!", sep="")

    print("\n\n+ Files to convert:")
    print("+ [")
    for file in files_to_convert:
        print("+ \t", file, ",", sep="")
    print("+ ]")

    if len(files_to_convert) > 0:
        print("\n\n+ ---BEGIN CONVERSION---")
    else:
        print("\n\n+ Nothing to convert!")

    for file in files_to_convert:
        src_file = get_formatted_name(file)
        print("\n+ Converting", src_file, "...")
        dst_file = ""
        if file.endswith(src_file_extension):
            # change the src file name
            modified_name = file[: file.rfind(src_file_extension)] + dst_file_extension
            dst_file = get_formatted_name(modified_name)
            print("+ The Destination File:", dst_file)

        command = "ffmpeg -i " + src_path + src_file + " " + dst_path + dst_file
        print("+ Command:", command)
        # Wait for this to finish executing
        subprocess.Popen(command, shell=True).wait()


if __name__ == "__main__":
    main()
