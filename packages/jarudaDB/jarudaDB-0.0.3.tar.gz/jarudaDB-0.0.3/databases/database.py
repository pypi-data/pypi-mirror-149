import mysql.connector
from mysql.connector import errorcode


class DBHandler():
    def __init__(self, host:str, user:str, pw:str, database:str, port=3306, raise_on_warnings=True, use_pure=False):
        ''' mysql init and create config\n
        param -> host = database host\n
        param -> user = database user name\n
        param -> pw = database password\n
        param -> database = database name\n
        param -> port = database port\n
        param -> raise_on_warnings = warnings option\n
        param -> use_pure = use_pure option '''
        self.config = {
            'user': user,
            'password': pw,
            'host': host,
            'database': database,
            'port': port,
            'raise_on_warnings': raise_on_warnings,
            'use_pure': use_pure
        }


    def config_modify(self, host='', user='', pw='', database='', port=3306, raise_on_warnings=True, use_pure=False):
        ''' config edit\n
        param -> host = edit if there is a value\n
        param -> user = edit if there is a value\n
        param -> pw = edit if there is a value\n
        param -> database = edit if there is a value\n
        param -> port = default 3306\n
        param -> raise_on_warnings = default True\n
        param -> use_pure = default False '''
        if user != '':
            self.config['user'] = user

        if pw != '':
            self.config['password'] = pw

        if host != '':
            self.config['host'] = host

        if database != '':
            self.config['database'] = database

        self.config['port'] = port
        self.config['raise_on_warnings'] = raise_on_warnings
        self.config['user_pure'] = use_pure


    def connector(self):
        ''' connector\n
        error -> raise Exception(error message)\n
        return db connector object '''
        try:
            conn = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception("Database does not exist")
            else:
                # error_code = err.errno
                # sql_state = err.sqlstate
                raise Exception(err.msg)
        else:
            return conn

    
    def query(self, sql, value=None, is_all=True, is_dictionary=True):
        ''' SELECT\n
        param -> sql = sql\n 
        param -> value = Condition, type(tuple)\n
        param -> is_all = True(fetchall)/False(fetchone)\n
        param -> is_dictionary = True(dictionary result)/False(result)\n
        error -> raise Exception(error message)\n
        return result query '''
        try:
            conn = self.connector()
            with conn.cursor(dictionary=is_dictionary) as cursor:
                cursor.execute(sql, value) if value else cursor.execute(sql)
                result = cursor.fetchall() if is_all else cursor.fetchone()
        except mysql.connector.Error as err:
            raise Exception(err.msg)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            cursor.close()
            conn.close()
            return result

    
    def executer(self, sql, value=None, is_lastrowid=False, is_dictionary=True):
        ''' CREATE, UPDATE, INSERT\n
        param -> sql = sql\n 
        param -> value = Condition, type(tuple)\n
        param -> is_lastrowid - True(lastrowid)/False(rowcount)\n
        param -> is_dictionary - True(dictionary result)/False(result)\n
        error -> raise Exception(error message)\n
        return success(0↑)/fail(0) '''
        try:
            conn = self.connector()
            with conn.cursor(dictionary=is_dictionary) as cursor:
                cursor.execute(sql, value) if value else cursor.execute(sql)
                if is_lastrowid:
                    result = cursor.lastrowid
                conn.commit()
                if is_lastrowid == False:
                    result = cursor.rowcount
        except mysql.connector.Error as err:
            raise Exception(err.msg)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            cursor.close()
            conn.close()
            return result


    def querys(self, sql_list:list, is_dictionary=True):
        ''' mysql curd\n
        param -> datas = [
                {
                    'sql': 'SELECT * FROM tb;',
                    'type': 'query',
                    'is_all': True
                },
                {
                    'sql': 'UPDATE tb SET value1=%s value2=%s',
                    'value': ('test', 'test'),
                    'type': 'executer',
                    'is_lastrowid': False
                }
            ]\n
        error -> raise Exception(error message)\n
        return Result query list of input array order
        '''
        try:
            conn = self.connector()            
            with conn.cursor(dictionary=is_dictionary) as cursor:
                result = []
                for data in sql_list:
                    sql = data['sql']
                    value = data.get('value', None)
                    type = data['type']
                    if type == 'query':
                        all = data['is_all']
                        cursor.execute(sql, value) if value else cursor.execute(sql)
                        result.append(cursor.fetchall() if all else cursor.fetchone())
                    elif type == 'executer':
                        last_id = data['is_lastrowid']
                        cursor.execute(sql, value) if value else cursor.execute(sql)
                        if last_id:
                            result.append(cursor.lastrowid) 
                        conn.commit()
                        if last_id == False:
                            result.append(cursor.rowcount)
                    else:
                        raise Exception('value error')
        except mysql.connector.Error as err:
            raise Exception(err.msg)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            cursor.close()
            conn.close()
            return result


    def executer_file_list(self, file_list):
        ''' INSERT TO sql file
        param -> file_list = open('file.sql', 'r').readlines()\n
        error -> raise Exception(error message) '''
        DELIMITER = ';'
        sql_list = []
        sql = ''

        for index, value in enumerate(file_list):
            if not value.strip():
                continue

            if value.startswith('--'):
                continue

            if 'DELIMITER' in value:
                DELIMITER = value.split()[1]
                continue

            if (DELIMITER not in value):
                sql += value.replace(DELIMITER, ';')
                continue

            if sql:
                sql += value
                sql_list.append(sql.strip())
                sql = ''
            else:
                sql_list.append(value.strip())

        try:
            conn = self.connector()
            with conn.cursor(dictionary=True) as cursor:
                for query in sql_list:
                    cursor.execute(query)
                conn.commit()
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            cursor.close()
            conn.close()    