import csv


class DiliReader:

    def __init__(self, file_name):
        self.handler = open(file_name, "r")

    def read_all(self):
        reader = csv.reader(self.handler)
        for row in reader:
            print(row)

    def close(self):
        self.handler.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __enter__(self):
        return self


class DiliWriter:

    def __init__(self, file_name):
        self.handler = open(file_name, "w")

    def write_all(self, mesh_term_dict):
        for term_key, term_val in mesh_term_dict.items():
            self.handler.write("{0};{1}\n".format(term_key, term_val))

    def close(self):
        self.handler.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __enter__(self):
        return self
