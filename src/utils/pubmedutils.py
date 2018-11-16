


class PubmedReader:

    def __init__(self, file_name):
        self.handler = open(file_name, "r")

    def read_all(self):
        for line in self.handler:
            yield int(line.strip())

    def close(self):
        self.handler.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __enter__(self):
        return self


class PubmedWriter:

    def __init__(self, file_name):
        self.handler = open(file_name, "w")

    def write_all(self, pmids):
        for pmid in pmids:
            self.handler.write("{0}\n".format(pmid))

    def close(self):
        self.handler.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __enter__(self):
        return self


