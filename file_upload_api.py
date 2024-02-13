# sample skeleton of secure file uploader api


database = []
folders = {}


# initial folder creation
def create_folder(profile, folder):
    if profile not in database:
        return -1
    if profile in database:
        folders.append(folder)
        return 0


# file authentication
def authenticate(profile, file):
    if profile not in database:
        return -1
    if profile in database:
        name = file.split(".")
        if name[-1] != "pdf" or "png" or "txt":
            return 0
        else:
            return -1


# file upload
def upload(profile, folder, file):
    if profile not in database:
        return -1
    if profile in database:
        if folder not in folders:
            return -1
        if folder in folders:
            if authenticate(file):
                folders[folder].append(file)
            else:
                return -1


# file deletion
def delete(profile, folder, file):
    if profile not in database:
        return -1
    if profile in database:
        if folder not in folders:
            return -1
        if folder in folders:
            if authenticate(file):
                folders[folder].delete(file)
            else:
                return -1
