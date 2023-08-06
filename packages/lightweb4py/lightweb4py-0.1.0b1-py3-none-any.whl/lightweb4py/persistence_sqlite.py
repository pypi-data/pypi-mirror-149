from uuid import UUID
from pprint import pprint
import sqlite3

from lightweb4py.persistence import Persistence, PersistenceEngine

ENGINE_SQLITE = 'sqlite'                # Engine name constant


# SQLite persistence storage class
# PARAMS:
# connection - SQLite database connection (__init__())
# dataClass - Python Class name to correctly restore it from the SQLite database (__init__()
# cursor - SQLite database cursor (__init__())
class PersistenceSQLite(PersistenceEngine):
    _connections = {}                   # existing connections to sqlite databases dictionary with file names as keys

    error_object = None                     # Error object of the last unsuccessful operation
    error_message = ""                      # Error message of the last unsuccessful operation

    # The initializer of the class obtains the Connection object of the existing or a new connection to
    # the dada_source database file, or sqlite3.Error exception from sqlite3.connect is passed on
    # if it fails to create a new connection
    def __init__(self, data_source: str, class_initializer):
        super().__init__(data_source=data_source, class_initializer=class_initializer)
        try:                            # get existing connection from dict if it exists
            self.connection = self.__class__._connections[data_source]
        except KeyError:                # create connection if it doesn't
            self.connection = sqlite3.connect(data_source,
                                              detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.__class__._connections[data_source] = self.connection
        # if connection is None, it means that database file could not be created
        self.cursor = self.connection.cursor()
        self.dataClass = class_initializer
        self._prepare_table()

    @staticmethod
    def register() -> bool:
        return Persistence.register_engine(ENGINE_SQLITE, PersistenceSQLite)

    # element_id - specify the required element id if you want to find specific record
    def get(self, element_id: UUID = None):
        class_name = self.dataClass.__name__
        request = f"select * from {class_name}"
        if element_id:
            request += " where id=?"
            result = self.cursor.execute(request,
                                         (element_id.hex if element_id.__class__ == UUID else element_id,))
        else:
            result = self.cursor.execute(request)
        # get property names from table column names
        # (column name is the first element of a 7-tuple, one 7-tuple for each column)
        property_names = [column[0] for column in result.description]
        # instantiate objects of type dataClass from tuples returned by fetchall()
        # ( dict(zip(property_names, values)) converts property_names and values lists into a dictionary with
        #   property_names as keys and values as values )
        instances = [self.dataClass(**dict(zip(property_names, values))) for values in result.fetchall()]
        return instances

    def _prepare_table(self):
        # get class name and attributes dict
        class_name = self.dataClass.__name__
        attribute_dict = self.dataClass.__dict__['__annotations__']
        # generate CREATE TABLE request for the class
        request = f"create table {class_name}" \
                  f"({', '.join(key + ' ' + value.__name__ for key, value in attribute_dict.items())})"
        try:
            self.cursor.execute(request)
        except sqlite3.OperationalError as e:
            pass                # table <class_name> already exists

    def set(self, element) -> bool:
        class_name = self.dataClass.__name__            # Get class name
        values = []                                     # Build values list
        for value in element.__dict__.values():
            values.append(value.hex if value.__class__ == UUID else value)
        if self.get(element.id):          # Element already exists - compose update request
            key_string = '=?,'.join(element.__dict__.keys()) + "=?"
            request = f"update {class_name} set {key_string} where id=?"
            # append element id if updating
            values.append(element.id.hex if element.id.__class__ == UUID else element.id)
        else:                                   # New element - compose insert request
            key_string = ','.join(element.__dict__.keys())
            parameter_str = ','.join('?' for _ in range(len(element.__dict__)))
            request = f"insert into {class_name}({key_string}) values ({parameter_str})"
        self.cursor.execute(request, values)
        self.connection.commit()
        return True

    def delete(self, element_id: UUID) -> bool:
        class_name = self.dataClass.__name__
        request = f"delete from {class_name} where id=?"
        self.cursor.execute(request, (element_id.hex if element_id.__class__ == UUID else element_id,))
        self.connection.commit()
        return True

    def append(self, element) -> bool:
        class_name = self.dataClass.__name__            # Get class name
        values = []                                     # Build values list
        for value in element.__dict__.values():
            values.append(value.hex if value.__class__ == UUID else value)
        key_string = ','.join(element.__dict__.keys())
        parameter_str = ','.join('?' for _ in range(len(element.__dict__)))
        request = f"insert into {class_name}({key_string}) values ({parameter_str})"
        self.cursor.execute(request, values)
        self.connection.commit()
        return True
