import os
import sys
sys.setrecursionlimit(2000)


def find_dirs(home_directory, start=True, iteration=2, home='', old_dir=-1,
              count_files=0, count_directories=0, find_file_or_directory=''):
    try:
        if start:
            print(home_directory.split('/')[-1] + ' >')
            home = home_directory.replace("/"+home_directory.split('/')[-1], "")

            return find_dirs(
                os.chdir(home_directory),
                start=False,
                home=home,
                find_file_or_directory=find_file_or_directory
            )

        else:
            if home_directory != home:
                directory = os.listdir(os.getcwd())

                for item in directory:

                    if directory.index(item) <= old_dir:
                        continue
                    if os.path.isdir(os.getcwd() + '/' + item) and item != 'venv' and item != '.git':
                        print('\t' * iteration + item + ' >')
                    else:
                        print('\t' * iteration + item)

                    if find_file_or_directory != '':
                        if find_file_or_directory == item:
                            return True

                    if os.path.isdir(os.getcwd() + '/' + item) and item != 'venv' and item != '.git':
                        count_directories += 1
                        os.chdir(os.getcwd() + '/' + item)
                        iteration += 2

                        return find_dirs(
                            os.getcwd(),
                            start=False,
                            iteration=iteration,
                            home=home,
                            count_files=count_files,
                            count_directories=count_directories,
                            find_file_or_directory=find_file_or_directory
                        )

                    elif item == 'venv':
                        count_directories += 1

                    elif os.path.isfile(os.getcwd() + '/' + item):
                        count_files += 1

                os.chdir('../')
                old_dir = os.listdir(os.getcwd()).index(home_directory.split('/')[-1])
                iteration -= 2

                return find_dirs(
                    os.getcwd(),
                    start=False,
                    iteration=iteration,
                    home=home,
                    old_dir=old_dir,
                    count_files=count_files,
                    count_directories=count_directories,
                    find_file_or_directory=find_file_or_directory
                )

            else:
                print('\nDirectories: ' + str(count_directories))
                print('Files: ' + str(count_files))
                return True

    except Exception as e:
        print(e)
        pass


os.chdir('../')

if sys.version_info[0] == 2:
    dir_to_count = raw_input("Input path to folder: \nExample: /path/to/directory/<name folder> \n ")
    print('_______________________________________________________________________________________________________')
    dir_or_file = raw_input("Input name of directory or file to find him. \n Input 'Enter' if you do not want anything to seek.")
else:
    dir_to_count = input("Input path to folder: \n"
                         "Example: /path/to/directory/<name folder> \n ")
    print('_______________________________________________________________________________________________________')
    dir_or_file = input(" Input name of directory or file to find him: "
                        "Input 'Enter' if you do not want anything to seek: ")


find_dirs(dir_to_count, find_file_or_directory=dir_or_file)
