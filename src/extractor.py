import os
from config import OUTPUT_DIR

"""
Parent class for reading sources and writing out XML
This is specialised for different data source types
"""
class Extractor:
    def __init__(self):
        print(f"{OUTPUT_DIR=}")
        try:
            os.mkdir(OUTPUT_DIR)
        except FileExistsError:
            pass
        self.output_dir = OUTPUT_DIR

    def write_record(self, bbox, model_endpath):
        """ NB: The input  parameters for this function should match the parameters defined in the configuration file
        """
        pass
