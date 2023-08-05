from ..create_serializer.create_serializer import create_serializer
import argparse
import sys
import os
import configparser


class Converter():
    
    _parser = None


    def parse_args(self):
        self._parser = argparse.ArgumentParser(
            description="Matuamod's custom serializer"
        )
        self._parser.add_argument(
            "--src_file", type=str, help="file_path for parse"
        )
        self._parser.add_argument(
            "--to_file", type=str, help="file_path to write"
        )
        self._parser.add_argument(
            "--make_config", type=str, help="use only config file and ignore other args"
        )
        return self._parser.parse_args()


    def get_args(self, args):
        src_file = None
        to_file = None
        if args.src_file and args.to_file:
            src_file, to_file = args.src_file, args.to_file
        elif args.make_config:
            print(args.make_config)
            src_file, to_file = self.get_config(args.make_config)
        if src_file and to_file:
            if os.path.exists(src_file) and os.path.isfile(src_file)\
                and os.path.exists(to_file) and os.path.isfile(to_file):
                # Get path of files
                abs_src_path = os.path.abspath(src_file)
                abs_to_path = os.path.abspath(to_file)
                self.make_convert(abs_src_path, abs_to_path)

            else:
                self._parser.error(f'No such files : {src_file} or {to_file}')
        else:
            self.__parser.error(
                f'Invalid --src_file and --to_file args: src_file="{src_file}", to_file="{to_file}"')


    
    def get_config(self, config_path: str) -> tuple:
        config_file = os.path.abspath(config_path)
        if os.path.isfile(config_file) and os.path.exists(config_file):
            config = configparser.RawConfigParser()
            config.read(config_file)
            src_file = config.get("DEFAULT", "src_file")
            to_file = config.get("DEFAULT", "to_file")
            return (src_file.replace('"', ''), to_file.replace('"', ''))
        else:
            self._parser.error(f'No such config file : {config_file}')


    def make_convert(self, src_file: str, to_file: str):
        src_format = os.path.splitext(src_file)[1][1:]
        to_format = os.path.splitext(to_file)[1][1:]
        if src_format != to_format:
            create_src_ser = create_serializer(src_format)
            create_to_ser = create_serializer(to_format)
            if create_src_ser and create_to_ser:
                ser_obj = create_src_ser.load(src_file)
                print(ser_obj)
                create_to_ser.dump(ser_obj, to_file)
        else:
            print("Chosen formats are equal.")
