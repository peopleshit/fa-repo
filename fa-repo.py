import argparse
import csv
import os
from git import Repo


class Entry:

    def __init__(self, name, repo, group):
        self.group = group
        self.name = name
        self.repo = repo

    def has_repo(self):
        if self.repo == '':
            return 0
        return 1


class CsvParser:

    def __init__(self, path_to_file):
        self.file = path_to_file

    def process(self):
        data = []
        with open(self.file, 'r') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';', fieldnames=['name', 'repo', 'group'])
            first_line = 1
            for row in reader:
                entity = Entry(row['name'], row['repo'], row['group'])
                if entity.has_repo() and first_line == 0:
                    data.append(entity)
                if first_line == 1:
                    first_line = 0
        return data


class Repository:

    def __init__(self, root_dir):
        self.directory = os.path.abspath(root_dir)

    def process(self, entries):
        groups = set(item.group for item in entries)
        for group in groups:
            group_folder = self.directory + "/" + group
            if not os.path.exists(group_folder):
                os.makedirs(group_folder)
        for entry in entries:
            path = self.directory + "/" + entry.group + "/" + entry.name
            if not os.path.exists(path):
                os.makedirs(path)
                Repo.clone_from(entry.repo, path)
                print(entry.group + " " + entry.name + " repo cloned")
            else:
                print(entry.group + " " + entry.name + " skipping, already exists")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates fa repo')
    parser.add_argument('file', metavar='CSV', help='CSV file with student information')
    parser.add_argument('path', metavar='string', help='Generated repo root directory')

    args = parser.parse_args()

    csv_parser = CsvParser(args.file)
    data = csv_parser.process()
    repo = Repository(args.path)
    repo.process(data)
