from sultan.api import Sultan


class FileManager:
    def __init__(self):
        super().__init__()

    def selectFile(self):
        with Sultan.load(sudo=False) as sultan:
            result = sultan.exc('./script/fileSelect.sh')
            resultArray = result.stdout[0].split('|')
            return resultArray

fm = FileManager()
