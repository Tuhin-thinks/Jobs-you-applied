from datetime import datetime
from typing import Union
import sqlite3

from Utils.files_op import convertToBinaryData
from Utils import Interact

today_date = datetime.date(datetime.today()).isoformat()


class Access:
    def __init__(self, sqlite_file):
        self.db_file = sqlite_file
        self.conn: Union[None, sqlite3.Connection] = None
        self.cursor = None
        self.create_connection()
        self.create_schema()

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_file)

    def create_table(self, query):
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        self.conn.commit()
        print("[+] TABLE CREATED\n")
        self.cursor.close()

    def insert_into_table(self, query, data=None):
        self.cursor = self.conn.cursor()
        if not data:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)
        self.conn.commit()
        self.cursor.close()

    def check_if_exists(self, column, table, data, return_data=False):
        if type(data) == str and type(column) == str and type(table) == str:
            search_query = f"SELECT COUNT(*) FROM {table} WHERE {column}={data}"
            self.cursor = self.conn.cursor()
            self.cursor.execute(search_query)
            data = self.cursor.fetchall()
            self.cursor.close()
            if data:
                if return_data:
                    return True, data
                return True
            else:
                if return_data:
                    return False, None
                return False
        else:
            if return_data:
                print(f"Invalid data format passed, check if all passed parameters are <Class 'str'>\n", 'f')
                return False, None
            return False

    def create_schema(self):
        """
        Tables:
            Applications
            Resume_Files
        """
        create_table_applications_query = "CREATE TABLE IF NOT EXISTS Application(" \
                                          "id INTEGER PRIMARY KEY AUTO_INCREMENT," \
                                          " COMPANY_NAME VARCHAR(120)," \
                                          " COMPANY_WEBSITE TEXT, APPLY_WEBSITE TEXT," \
                                          " RESUME_ID INTEGER" \
                                          "FOREIGN KEY (RESUME_ID)" \
                                          "REFERENCES Resume_Files(RESUME_ID);" \
                                          ")"  # this will use a id from the resume files table

        create_table_resume_query = "CREATE TABLE IF NOT EXISTS Resume_Files(" \
                                    "RESUME_ID INTEGER PRIMARY KEY AUTO_INCREMENT," \
                                    " FIRST_REGISTER_DATE TEXT," \
                                    " RESUME_FILE BLOB," \
                                    " RESUME_FILE_PATH TEXT);"

        self.create_table(create_table_resume_query)
        self.create_table(create_table_applications_query)

    def add_resume_file(self, resumeFilePath):
        try:
            res = self.check_if_exists('RESUME_FILE_PATH', "Resume_Files", resumeFilePath)
            if res:
                Interact.Display.str(f"Resume File path already in database.\n", 'f')  # show search fail message
                return
            sqlite_insert_blob_query = """ INSERT INTO Resume_Files
                                      (FIRST_REGISTER_DATE, RESUME_FILE, RESUME_FILE_PATH)
                                       VALUES (?, ?, ?);"""

            resume = convertToBinaryData(resumeFilePath)

            data_tuple = (today_date, resume, resumeFilePath)
            self.insert_into_table(sqlite_insert_blob_query, data_tuple)
            Interact.Display.str(f"Resume file and path registered to date : {today_date}",
                                 'success')  # success message

        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)

        # --------------- DON'T CLOSE SQLITE CONNECT WHILE PROGRAM IS STILL RUNNING ------------
        # finally:
        #     if self.conn:
        #         self.conn.close()
        #         print("the sqlite connection is closed")
