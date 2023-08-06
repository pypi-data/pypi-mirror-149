import importlib
import os
from os import listdir
from os.path import isfile, join
from typing import List, Dict
from django.db import transaction
from django.conf import settings
from django.core.management import BaseCommand

from seeding.models import Seeding


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Command(BaseCommand):
    help = "Seeding for project.\r\n" + \
           "Commands:" + \
           "- `create` - create new seeding. create new file in seeding folder" + \
           "- seed - apply new seeding"
    seeding_dir: str = None

    def add_arguments(self, parser):
        parser.add_argument(
            'command',
            nargs='+',
            type=str,
            help='Commands for seeding',
            choices=['create', 'seed', 'rollback']
        )

        # parser.add_argument(
        #     'name',
        #     nargs='?',
        #     type=str,
        #     help='Name of new seeding file'
        # )

    def handle(self, *args, **options):
        if hasattr(settings, 'SEEDING_DIR'):
            self.seeding_dir = settings.BASE_DIR / settings.SEEDING_DIR
        else:
            raise ValueError("Need to be SEEDING_DIR provided in settings file")

        if not os.path.isdir(self.seeding_dir):
            raise NotADirectoryError(f"There is no folder on path: {self.seeding_dir}")

        if options['command'][0] == 'create':
            self._create_new_seeding(options.get('name'))
        elif options['command'][0] == 'seed':
            self._seed()
        elif options['command'][0] == 'rollback':
            self._rollback()

    def _get_seeding_files_list(self) -> Dict:
        files_list = [f for f in listdir(self.seeding_dir) if isfile(join(self.seeding_dir, f))]
        files_dict = dict()
        for file_item in files_list:
            file_name_as_list = file_item.split('_')
            if len(file_name_as_list) > 0 and file_name_as_list[0].isdigit():
                files_dict[int(file_name_as_list[0])] = file_item
        return files_dict

    def _create_new_seeding(self, seeding_name: str) -> None:
        """ Create new seeding file with declared base class """
        files_dict = self._get_seeding_files_list()
        next_number = 1
        if len(files_dict) > 0:
            next_number = max(files_dict.keys()) + 1

        new_identifier = str(next_number).zfill(4)

        if seeding_name is None:
            seeding_name = 'auto_name'
        full_seeding_file_name = f'{new_identifier}_{seeding_name}.py'

        with open(f'{self.seeding_dir}/{full_seeding_file_name}', 'w') as seeding_file:
            seeding_file.write('''from seeding.seeding import BaseSeeding


class Seeding(BaseSeeding):

    def seeding(self):
        """ Seeding data in project """
        pass

    def rollback(self):
        """ Remove seeded data from project  """
        pass
''')
            print(f'{full_seeding_file_name}: was created')

    def _seed(self, rollback: bool = False) -> None:
        """ Seeding data """
        files_names_list = set(self._get_seeding_files_list().values())
        applied_seeding = set(Seeding.objects.all().values_list('name', flat=True))
        seeding_to_apply = sorted(files_names_list - applied_seeding)
        print(f'{bcolors.OKGREEN}Applying new seeding list{bcolors.ENDC}')
        if len(seeding_to_apply) > 0:
            with transaction.atomic():
                new_applied_seeding_list = []
                for seeding_item in seeding_to_apply:
                    try:
                        module_name = f'{settings.SEEDING_DIR.replace("/", ".")}.{seeding_item.replace(".py", "")}'
                        mod = importlib.import_module(module_name)
                        mod.Seeding(rollback)
                        new_applied_seeding_list.append(Seeding(
                            name=seeding_item
                        ))
                        print(f'- {seeding_item}: {bcolors.OKGREEN}was applied{bcolors.ENDC}')
                    except AttributeError as e:
                        print(f'- {seeding_item}: {bcolors.FAIL}not applied{bcolors.ENDC}')
                        print(f'{bcolors.OKCYAN}info:{bcolors.ENDC} {e.__repr__()}')

                Seeding.objects.bulk_create(new_applied_seeding_list)
        else:
            print(f'{bcolors.WARNING}There is no new seeding files{bcolors.ENDC}')

    def _rollback(self):
        """ Rollback data from seeding files """
        print('Not ready yet')
