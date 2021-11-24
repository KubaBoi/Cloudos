import json
import os

class IconFinder:
    def __init__(self):
        with open(f"{os.path.dirname(__file__)}/iconDictionary.json", "r") as f:
            self.dict = json.loads(f.read())

    def find(self, fileName):
        fileType = fileName.split(".")[-1].lower()
        if (fileType in self.dict):
            return self.dict[fileType]
        else:
            return "unknown"
        