"""
Parent class for reading sources and writing out XML
This is specialised for different data source types
"""
class Extractor:
    def write_record(self, bbox, model_endpath):
        pass
