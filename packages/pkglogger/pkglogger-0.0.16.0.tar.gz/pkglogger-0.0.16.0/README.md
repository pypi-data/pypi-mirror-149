"""

## Using this Package you can able to track majorly Sysstem Generated followings :
    
    1. Log Time
    2. Exception
    3. Exception Type
    4. Exception Object
    5. Exception Traceback Summary
    6. Exception Traceback Detailed
    7. Exception Traceback Line No.

"""

*##Steps to run the package :*

1. pip install pkglogger==<version number>
2. from pkglogger import pkglogger

*logger()*
'''
You need to call this function at TRY block

Var 1 : Pass the file name you want to create \n
Var 2 : Pass Function name if you want to track function wise logs. To do this, you want keep this call at Function Level\n
Var 3 : If you want to give any specific value as Task Status\n
Var 4 : Path where you want to create the log file. Please pass value as string.\n
Var 5 : If any other parameter you want keep track, pass variable name as you want\n
Var 6 : Pass the value of the additional variable you have added
'''
Example : logger('log3','loggertest','','','URL','http://test.com123')


*exceptionlogger()*
'''
You need to call this funcion at EXCEPTION bloack

Var 1 : Pass the file name you want to create\n
Var 2 : Pass Function name if you want to track function wise logs. To do this, you want keep this call at Function Level\n
Var 3 : Please pass the exception value. Example : except Exception as e\n
Var 4 : If you want to give any specific value as Task Status\n
Var 5 : Path where you want to create the log file. Please pass value as string.\n
Var 6 : If any other parameter you want keep track, pass variable name as you want\n
Var 7 : Pass the value of the additional variable you have added\n
'''

*Return the exception details as well *
