"""
Module for defining constants and helper methods
"""

import sys, os
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

DB_TYPE = "mysql"

MYSQL_CONFIG_FILE = ""
mycnf_file = Path(str(Path.home()) + "/.my.cnf")
if mycnf_file.is_file():
    MYSQL_CONFIG_FILE = str(mycnf_file)

MAX_ATTEMPTS = 5 #max number of times to try a query before exiting
PROGRESS_AFTER_ROWS = 5000 #the number of rows to process between each progress updated
FEATURE_TABLE_PREFIX = 'feats_'
MYSQL_ERROR_SLEEP = 4 #number of seconds to wait before trying a query again (incase there was a server restart
SQLITE_ERROR_SLEEP = 4
MYSQL_BATCH_INSERT_SIZE = 10000 # how many rows are inserted into mysql at a time
MAX_SQL_SELECT = 1000000 # how many rows are selected at a time
VARCHAR_WORD_LENGTH = 36 #length to allocate var chars per words
LOWERCASE_ONLY = True #if the db is case insensitive, set to True
MAX_TO_DISABLE_KEYS = 100000 #number of groups * n must be less than this to disable keys
MAX_SQL_PRINT_CHARS = 256

##Corpus Settings:
DEF_CORPDB = 'dla_tutorial'
DEF_CORPTABLE = 'msgs'
DEF_CORREL_FIELD = 'user_id'
DEF_MESSAGE_FIELD = 'message'
DEF_MESSAGEID_FIELD = 'message_id'
DEF_ENCODING = 'utf8mb4'
DEF_UNICODE_SWITCH = True
DEF_LEXTABLE = 'wn_O'
DEF_DATE_FIELD = 'updated_time'
DEF_COLLATIONS = {
        'utf8mb4': 'utf8mb4_bin',
        'utf8': 'utf8_general_ci',
        'latin1': 'latin1_swedish_ci',
        'latin2': 'latin2_general_ci',
        'ascii': 'ascii_general_ci',
    }
DEF_MYSQL_ENGINE = 'MYISAM'

##lexInterface settings
DEF_TERM_FIELD = 'term'
DEF_MIN_WORD_FREQ = 1000
DEF_NUM_RAND_MESSAGES = 100
MAX_WRITE_RECORDS = 1000 #maximum number of records to write at a time (for add_terms...)

##Outcome settings
DEF_OUTCOME_TABLE = ''
DEF_OUTCOME_FIELD = ''
DEF_OUTCOME_FIELDS = []
DEF_OUTCOME_CONTROLS = []
DEF_GROUP_FREQ_THRESHOLD = 1000 #min. number of total feature values that the group has, to use it
DEF_SHOW_FEAT_FREQS = True
DEF_MAX_TC_WORDS = 100
DEF_MAX_TOP_TC_WORDS = 15
DEF_TC_FILTER = True
DEF_WEIGHTS = ''
DEF_LOW_VARIANCE_THRESHOLD = 0.0

WARNING_STRING = "\n".join(["#"*68, "#"*68, "WARNING: %s", "#"*68, "#"*68])


def warn(string, attention=False):
    if attention: string = WARNING_STRING % string
    print(string, file=sys.stderr)
    
BATCH_SIZE=1