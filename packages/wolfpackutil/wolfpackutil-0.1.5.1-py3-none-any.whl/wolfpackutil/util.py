import logging
from argparse import ArgumentParser
from datetime import datetime
from os.path import join
from pathlib import Path
from random import choice
from time import time

from requests import Session as r_Session
from dateutil import tz
from owoify import owoify
from pyfiglet import Figlet
from rich.console import Console
from tinydb import TinyDB, Query


class Session(r_Session):
    pass


class DB(TinyDB):
    def __init__(self, path):
        super().__init__(path)
        self.q = Query()


class Parser(ArgumentParser):
    def args(self, description):
        self.description = description
        return self


class Log(Console):
    log_contents = {}
    log_cache = ""

    def warn(self, msg):
        logging.root.level <= logging.WARN and self.log(f"[yellow][WARN][white] {msg}")

    def warning(self, msg):
        self.warn(msg)

    def info(self, msg):
        logging.root.level <= logging.INFO and self.log(f"[cyan][INFO][white] {msg}")

    def debug(self, msg):
        logging.root.level <= logging.DEBUG and self.log(f"[green][DEBUG][white] {msg}")

    def critical(self, msg):
        logging.root.level <= logging.CRITICAL and self.log(f"[red][CRITICAL][white] {msg}")

    def log(self, msg):
        super().log(msg)
        t = time()
        self.log_contents[t] = msg

    def parse_log(self, args):
        if args.verbose:
            logging.root.level = logging.DEBUG
            self.debug("Enabling verbose mode.")
        else:
            logging.root.level = logging.INFO

    def fancy_intro(self, name, description='', version=''):
        f = Figlet()
        keywords = choice(
            ['A custom made Minecraft modpack script. Nothing special, hehe.',
             'Please don\'t tell anyone about this...',
             'Hehe. UwU, It\'s all we have, I know. I\'m sorry!',
             'I should probably get a better idea for this list...',
             'Not sponsored by Awoos!'
             ]
        )
        self.info(''.join(['####' for _ in range(16)]))
        self.info(f'\n[blue]{f.renderText(name)}[white]\n\t[green]{version}[white]\n\t\t{owoify(keywords)}')
        self.info(''.join(['####' for _ in range(16)]))
        self.info(description)

    def save_log(self, name, directory):
        cache_folder = join(directory, "log", name)
        Path(cache_folder).mkdir(exist_ok=True, parents=True)
        self.debug("Saving log...")
        tzinfo = tz.gettz('EDT')
        logfile_time = datetime.fromtimestamp(time(), tz=tzinfo)
        logfile_date = datetime.strftime(logfile_time, "%m_%d_%Y-%H_%M_%S")
        with open(f"{cache_folder}/{logfile_date}.log", "w", encoding="utf-8") as f:
            for k, v in self.log_contents.items():
                format_time = datetime.fromtimestamp(k, tz=tzinfo)
                format_date = datetime.strftime(format_time, "%m-%d-%Y-%H:%M:%S")
                f.write(f"[{format_date}] {v}\n")

# TODO: Create a session class that comes from requests instead