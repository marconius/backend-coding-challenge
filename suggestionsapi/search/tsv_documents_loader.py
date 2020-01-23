import csv

class TsvDocumentsLoader():

    def __init__(self, path_to_cities_tsv):
        self.path_to_data_file = path_to_cities_tsv

    def load_documents(self):
        self.documents = []
        with open(self.path_to_data_file, 'r') as file:
            headers = file.readlines(1)[0].split('\t')
            for line in file.readlines():
                document = {}
                values = line.split('\t')
                for i, header in enumerate(headers):
                    document[header] = values[i]
                self.documents.append(document)
