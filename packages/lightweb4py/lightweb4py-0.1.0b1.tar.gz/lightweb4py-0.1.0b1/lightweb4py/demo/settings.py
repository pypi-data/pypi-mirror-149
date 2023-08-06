# Global app settings
from lightweb4py.persistence import ENGINE_JSON
from lightweb4py.persistence_sqlite import ENGINE_SQLITE
from lightweb4py import settings

PATH_JINJA_TEMPLATES = "templates/"     # jinja templates directory
PATH_DB = "database/"    # database directory
PATH_LOGS = "logs/"      # logs path
PATH_CONTACT_MESSAGES = "contact_messages/"     # Папка для файлов сообщений (used by app_student.py)

TEMPLATES_APP = settings.TEMPLATES_APP  # import Jinja tag for app templates

# SQLite datafile
SQLITE_DATA_FILE = PATH_DB + "database.db"

# Categories data config
CATEGORIES_DATA_FILE = PATH_DB + "categories.json"      # Data file
CATEGORIES_STORAGE = ENGINE_JSON                        # Storage engine
#CATEGORIES_DATA_FILE = SQLITE_DATA_FILE                 # Data file
#CATEGORIES_STORAGE = ENGINE_SQLITE                      # Storage engine
# Courses data config
COURSES_DATA_FILE = PATH_DB + "courses.json"            # Data file
COURSES_STORAGE = ENGINE_JSON                           # Storage engine
#COURSES_DATA_FILE = SQLITE_DATA_FILE                    # Data file
#COURSES_STORAGE = ENGINE_SQLITE                         # Storage engine
# Students data config
STUDENTS_DATA_FILE = PATH_DB + "students.json"          # Data file
STUDENTS_STORAGE = ENGINE_JSON                          # Storage engine
#STUDENTS_DATA_FILE = SQLITE_DATA_FILE                   # Data file
#STUDENTS_STORAGE = ENGINE_SQLITE                        # Storage engine
# Feedback data config
FEEDBACK_DATA_FILE = PATH_DB + "feedback.json"          # Data file
FEEDBACK_STORAGE = ENGINE_JSON                          # Storage engine
#FEEDBACK_DATA_FILE = SQLITE_DATA_FILE                   # Data file
#FEEDBACK_STORAGE = ENGINE_SQLITE                        # Storage engine

# Logger types
LOGGER_DEBUG = "debug"                                  # Debug logger name
LOGGER_RUNTIME = "runtime"                              # Runtime logger name
