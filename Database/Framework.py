import os
from Utils import files_op


class Structure:
    db_file = os.path.realpath("Data/apply_data.sqlite")

    def __init__(self):
        pass

    def load_db(self):
        files_op.create_dir_if_notexist(self.db_file)  # creates the db folder if it doesn't exist
