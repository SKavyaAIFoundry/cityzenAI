import os
import shutil


# empty the contents of a given directory
def resetDirectory(directory_path):
    if os.path.exists(directory_path):
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as exception:
                print('Could not delete directory: %s.  Exception: %s' % (file_path, exception))
    else:
        os.makedirs(directory_path)

