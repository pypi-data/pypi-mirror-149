import argparse
import os
import sys
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
from file_extension import extension_hash_map
import json


class GetRepoMetrics:
    def __init__(self):
        """
        initial ArgumentParser and parse the argument
        """
        # initial parser
        parser = argparse.ArgumentParser(description='Detect content programing language')
        # add argument tobe parsed
        parser.add_argument('Path',
                            metavar='start_folder_path',
                            type=str,
                            help="Start folder path. Use 'NA' to use current working folder as start folder")
        parser.add_argument('--method',
                            metavar='by_xxxx',
                            dest='detect_method',
                            default='by_extension',
                            choices=['by_extension', 'by_content'],
                            type=str,
                            help="choose detect method to detect file programing language between 'by_extension' and" \
                                 " 'by_pygments'. Default with 'by_extension' ")
        # parse the argument
        self.args = parser.parse_args()
        # some variable
        self.start_path = str()
        self.total_file = 0
        self.summary = dict()
        self.result = dict()
        self.unknown_extension = list()

    def check_path(self):
        # get input path
        input_path = self.args.Path
        # if not input path will get the file location folder as default folder
        if input_path.upper() == 'NA':
            print(f"set start folder path as {os.getcwd()}")
            input_path = os.getcwd()

        # check is it a folder path
        if not os.path.isdir(input_path):
            print('The path specified does not valid, please check an retry')
            sys.exit()
        # print('\n'.join(os.listdir(input_path)))
        self.start_path = input_path

    def detect_file_language(self):
        if self.args.detect_method == 'by_extension':
            detect_detail_dict = self._detect_file_language_by_extension()
        elif self.args.detect_method == 'by_content':
            detect_detail_dict = self._detect_file_language_by_content()
        self._show_conclusion(detect_detail_dict)

    def _detect_file_language_by_extension(self):
        """
        # use file extension to decide file language
        :return: list of dict contain file path and detected programing language
        """
        detect_results = list()

        # get file list for file in folder
        for dirname, _, filenames in os.walk(self.start_path, topdown=True):
            for filename in filenames:
                # get file path
                file_path = os.path.join(dirname, filename)
                # get file extension
                _name, extension = os.path.splitext(filename)
                if extension_hash_map.get(extension):
                    language = extension_hash_map.get(extension)
                else:
                    # print(f"Error: Cano not detect file type for file {file_path}")
                    self.unknown_extension.append(extension)
                    language = "Unknown"
                # count language frequent
                self._count_language(language)
                # append result to detect_results dictionary
                detect_results.append({
                    "path": file_path,
                    "language": language
                })
        return detect_results

    # deprecated guesslang need python 3.7 and tensorflow 4.5.0
    # def detect_file_language_by_guesslang(self):
    #     # use guesslang to
    #     pass

    def _detect_file_language_by_content(self) -> list:
        """
        # use file extension to decide file language
        :return: list of dict contain file path and detected programing language
        """
        detect_results = list()
        # get file list for file in folder
        for dirname, _, filenames in os.walk(self.start_path, topdown=True):
            for filename in filenames:
                file_path = os.path.join(dirname, filename)
                try:
                    with open(file_path, 'rb') as _file:
                        _content = _file.read()
                        language = guess_lexer_for_filename(filename, _content).name

                except ClassNotFound as error:
                    # print(f"Error: Cano not detect file type for file {file_path}")
                    self.unknown_extension.append(os.path.splitext(filename)[1])
                    language = "Unknown"
                # count language frequent
                self._count_language(language)
                # append result to detect_results dictionary
                detect_results.append({
                    "path": file_path,
                    "language": language
                })
        return detect_results

    def _count_language(self, language: str) -> None:
        # count total processed file
        self.total_file += 1
        # count correspond language frequent
        if self.summary.get(language):
            # add 1 if it in the summary dictionary
            self.summary[language] += 1
        else:
            # add language to summary dictionary and set frequent to 1 if first appear
            self.summary[language] = 1

    def _show_conclusion(self, detect_detail: list) -> None:
        for key, value in self.summary.items():
            self.summary[key] = value / self.total_file
        self.result = {
            "summary": self.summary,
            "unknow_extension": list(set(self.unknown_extension)),
            "results": detect_detail
        }
        print("\n#################################################################################################")
        print(f"Detect done, detection result is as follow:\n{json.dumps(self.result, indent=4)}")


if __name__ == '__main__':
    print(f"Start detection...")
    metric_explore = GetRepoMetrics()
    metric_explore.check_path()
    metric_explore.detect_file_language()
