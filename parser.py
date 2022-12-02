import json
import os
from json import JSONDecodeError
from pathvalidate import ValidationError, validate_filename


class Parser:
    def __init__(self, root_path: str, json_path: str):
        self.validate_params(root_path, json_path)
        self.root_path = root_path
        self.json_path = json_path

    @staticmethod
    def validate_params(root_path: str, json_path: str) -> None:
        if not os.path.isdir(root_path):
            raise Exception(f"The root directory path given '{root_path}' is not a valid path!")
        if not os.path.isfile(json_path):
            raise Exception(f"The json file path given '{json_path}' is not a valid path!")

    @staticmethod
    def warn_that_path_exists(item_path: str) -> None:
        print(f"[WARNING] {item_path} already exists. "
              f"Do you want to override the current structure?")
        while True:
            answer = input(f"[yes|no]? ")
            if answer == "yes":
                print("OK. The current structure will be overriden.")
                break
            if answer == "no":
                print("As you requested, the current process will be now aborted... Bye!")
                exit()
            print("Please type 'yes' or 'no'!")

    @staticmethod
    def validate_item(item_name: str, item_path: str) -> None:
        try:
            validate_filename(item_name)
            if os.path.exists(item_path):
                Parser.warn_that_path_exists(item_path)
        except ValidationError as exception:
            # only extract the explanation of the error
            raise Exception(f"The name='{item_name}' isn't valid because: {str(exception).split(sep=',')[0]}")

    @staticmethod
    def validate_dir_structure(dir_structure: dict, root: str) -> None:
        for key in dir_structure.keys():
            Parser.validate_item(key, os.path.join(root, key))
            if type(dir_structure[key]) == dict:
                Parser.validate_dir_structure(dir_structure[key], os.path.join(root, key))

    def get_json_dict(self) -> dict:
        try:
            file = open(self.json_path, "r")
            dir_structure = json.loads(file.read())
            self.validate_dir_structure(dir_structure, self.root_path)
            file.close()
            return dir_structure
        except OSError:
            raise Exception(f"The json file '{self.json_path}' can't be opened!")
        except JSONDecodeError:
            raise Exception(f"The json file '{self.json_path}' isn't a valid json file!")
