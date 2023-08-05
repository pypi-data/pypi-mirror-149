

import logging
import os
import sqlite3
from hashlib import sha256

import tempfile


class SuppressKnown(logging.Filter):
    """
    This filter allows to suppress log messages that were shown before.

    The python logging module can be used as normal. This Filter needs to be
    added to the appropriate Logger and logging calls (e.g. to warning, info
    etc.) need to have an additional `extra` argument.
    This argument should be a dict that contains an identifier and a category.
    Example: `extra={"identifier":"<Record>something</Record>",
                     category="entities"}
    The identifier is used to check whether a message was shown before and
    should be a string. The category can be used to remove a specific group of
    messages from memory and the logger would show those messages again even
    when they are known.
    """

    def __init__(self, db_file=None):
        if db_file:
            self.db_file = db_file
        else:
            tmppath = tempfile.gettempdir()
            tmpf = os.path.join(tmppath, "caosadvanced_suppressed_cache.db")
            self.db_file = tmpf
        if not os.path.exists(self.db_file):
            self.create_cache()

    def create_cache(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE messages (digest text primary key, category text)''')
        conn.commit()
        conn.close()

    def tag_msg(self, txt, identifier, category):
        digest = self.hash(txt, identifier)
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''INSERT INTO messages VALUES (?,?)''', (digest, category))
        conn.commit()
        conn.close()

    def reset(self, category):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''DELETE FROM messages WHERE category=?''',
                  (category,))
        conn.commit()

    def was_tagged(self, digest):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''Select  * FROM messages WHERE digest=?''',
                  (digest,))
        res = c.fetchone()
        conn.commit()
        conn.close()

        if res is None:
            return False
        else:
            return True

    def hash(self, txt, identifier):
        return sha256((txt+str(identifier)).encode("utf-8")).hexdigest()

    def filter(self, record):
        """
        Return whether the record shall be logged.


        If either identifier of category is missing 1 is returned (logging
        enabled). If the record has both attributes, it is checked whether the
        combination was shown before (was_tagged). If so 0 is returned.
        Otherwise the combination is saved and 1 is returned
        """

        if not hasattr(record, "identifier"):
            return 1

        if not hasattr(record, "category"):
            return 1

        if self.was_tagged(self.hash(record.getMessage(), record.identifier)):
            return 0

        self.tag_msg(record.getMessage(), record.identifier, record.category)

        return 1
