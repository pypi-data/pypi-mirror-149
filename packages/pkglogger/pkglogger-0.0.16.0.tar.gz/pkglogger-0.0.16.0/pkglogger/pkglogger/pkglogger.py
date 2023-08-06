# -*- coding: utf-8 -*-
"""

Using this Package you can able to track majorly Sysstem Generated followings :
    
    1. Log Time
    2. Exception
    3. Exception Type
    4. Exception Object
    5. Exception Traceback Summary
    6. Exception Traceback Detailed
    7. Exception Traceback Line No.

"""
import datetime,os,sys
import traceback

def logger(logger_no, function_name, task_status = '', path_output = '', other_var_name='',other_var=''):
    '''
    You need to call this function at TRY block
    
    Var 1 : Pass the file name you want to create \n
    Var 2 : Pass Function name if you want to track function wise logs. To do this, you want keep this call at Function Level\n
    Var 3 : If you want to give any specific value as Task Status\n
    Var 4 : Path where you want to create the log file. Please pass value as string.\n
    Var 5 : If any other parameter you want keep track, pass variable name as you want\n
    Var 6 : Pass the value of the additional variable you have added
    '''
    try :
        if logger_no == '':
            logger_no = "Mention Logger Name"
        if function_name == '':
            function_name = "Mention Funtion Name"
        if task_status == '':
            task_status = "Code Status Healthy"
        # if error == '':
        error = "No Error"
        
        if other_var_name == '':
            other_var_name = ""
            
        if other_var == '':
            other_var = ""
            
        if path_output == '':
            log_file = open(os.getcwd() + '/' + logger_no + '.txt', 'a+')
            log_file.write("========================================================\n")
            log_file.write("<<<<<<<< Logger Log Data : Default Output path >>>>>>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["[ Logged Time :",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"]",
                                 "[ Logger Name :",logger_no,"]",
                                 "[ Funtion Name :",function_name,"]",
                                 "[ Task Status :",task_status,"]",
                                 "[ Error :",error,"]",
                                 "[ Output Path :",path_output,"]",
                                 "[ ",other_var_name," :",other_var,"]"
                                 ])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            
            
        else:
            log_file = open(path_output + '/' + logger_no + '.txt', 'a+')
            log_file.write("========================================================\n")
            log_file.write("<<<<< Logger Log Data : Output path passed by User >>>>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["[ Logged Time :",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"]",
                                 "[ Logger Name :",logger_no,"]",
                                 "[ Funtion Name :",function_name,"]",
                                 "[ Task Status :",task_status,"]",
                                 "[ Error :",error,"]",
                                 "[ Output Path :",path_output,"]",
                                 "[ ",other_var_name," :",other_var,"]",
                                 ])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            
            
            
    except Exception as err:
        # pass
        if path_output == '':
            # System Generated Info
            exception_type, exception_object, exception_traceback = sys.exc_info()
            
            log_file = open(os.getcwd() +'/'+ logger_no + '.txt', 'a+')
            log_file.write("========================================================\n")
            log_file.write("<<<< Logger Exception Data : Default Output path >>>>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["[ Logged Time :",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"]",
                                 "[ Logger Name :",logger_no,"]",
                                 "[ Funtion Name :",function_name,"]",
                                 "[ Task Status :",task_status,"]",
                                 "[ Logger_Exception_Error :",str(err.args[0]),"]",
                                 "[ Exception Type :",str(exception_type),"]",
                                 "[ Exception Object :",str(exception_object),"]",
                                 "[ Exception Traceback Summary :",str(traceback.extract_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Detailed :",str(traceback.format_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Line No. :",str(exception_traceback.tb_lineno),"]",
                                 "[ Output Path :",path_output,"]",
                                 "[ ",other_var_name," :",other_var,"]",
                                 ])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            
        else:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            log_file = open(os.getcwd() +'/'+ logger_no + '.txt', 'a+')
            log_file.write("========================================================\n")
            log_file.write("< Logger Exception Data : Output path passed by User >\n")
            log_file.write("========================================================\n")
            log_file.writelines(["[ Logged Time :",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"]",
                                 "[ Logger Name :",logger_no,"]",
                                 "[ Funtion Name :",function_name,"]",
                                 "[ Task Status :",task_status,"]",
                                 "[ Logger_Exception_Error :",str(err.args[0]),"]",
                                 "[ Exception Type :",str(exception_type),"]",
                                 "[ Exception Object :",str(exception_object),"]",
                                 "[ Exception Traceback Summary :",str(traceback.extract_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Detailed :",str(traceback.format_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Line No. :",str(exception_traceback.tb_lineno),"]",
                                 "[ Output Path :",path_output,"]",
                                 "[ ",other_var_name," :",other_var,"]",
                                 ])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            
    
##############################################################################################################
# Exception Logger
##############################################################################################################
def exceptionlogger(logger_no, function_name , e , task_status = '', path_output = '' ,other_var_name='',other_var=''):
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
    try :
        if logger_no == '':
            logger_no = "Mention Logger Name"
        if function_name == '':
            function_name = "Mention Funtion Name"
        if task_status == '':
            task_status = "Exception Occured"
       
        if other_var_name == '':
            other_var_name = ""
            
        if other_var == '':
            other_var = ""
            
        exception_type, exception_object, exception_traceback = sys.exc_info()
        if path_output == '':
            log_file = open(os.getcwd() + '/' + logger_no + '.txt', 'a+')
            log_file.write("========================================================\n")
            log_file.write("<<< ExceptionLogger Log Data : Default Output path >>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["[ Logged Time :",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"]",
                                 "[ Logger Name :",logger_no,"]",
                                 "[ Funtion Name :",function_name,"]",
                                 "[ Task Status :",task_status,"]",
                                 "[ Logger_Exception_Error :",str(e),"]",
                                 "[ Exception Type :",str(exception_type),"]",
                                 "[ Exception Object :",str(exception_object),"]",
                                 "[ Exception Traceback Summary :",str(traceback.extract_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Detailed :",str(traceback.format_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Line No. :",str(exception_traceback.tb_lineno),"]",
                                 "[ Output Path :",path_output,"]",
                                 "[ ",other_var_name," :",other_var,"]",
                                 ])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            
        else:
            log_file = open(path_output + '/' + logger_no + '.txt', 'a+')
            log_file.write("===========================================================\n")
            log_file.write("< ExceptionLogger Log Data : Output path passed by User >\n")
            log_file.write("===========================================================\n")
            log_file.writelines(["[ Logged Time :",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"]",
                                 "[ Logger Name :",logger_no,"]",
                                 "[ Funtion Name :",function_name,"]",
                                 "[ Task Status :",task_status,"]",
                                 "[ Logger_Exception_Error :",str(e),"]",
                                 "[ Exception Type :",str(exception_type),"]",
                                 "[ Exception Object :",str(exception_object),"]",
                                 "[ Exception Traceback Summary :",str(traceback.extract_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Detailed :",str(traceback.format_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Line No. :",str(exception_traceback.tb_lineno),"]",
                                 "[ Output Path :",path_output,"]",
                                 "[ ",other_var_name," :",other_var,"]",
                                 ])
            log_file.write("\n=========================================================\n")
            log_file.write("===========================================================\n")
            log_file.close()
            
    except Exception as err:
        # System Generated Info
        exception_type, exception_object, exception_traceback = sys.exc_info()
        if path_output == '':
            log_file = open(os.getcwd() +'/'+ logger_no + '.txt', 'a+')
            log_file.write("==============================================================\n")
            log_file.write("< ExceptionLogger Log Exception Data : Default Output path >\n")
            log_file.write("==============================================================\n")
            log_file.writelines(["[ Logged Time :",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"]",
                                 "[ Logger Name :",logger_no,"]",
                                 "[ Funtion Name :",function_name,"]",
                                 "[ Task Status :",task_status,"]",
                                 "[ Logger_Exception_Error :",str(err.args[0]),"]",
                                 "[ Exception Type :",str(exception_type),"]",
                                 "[ Exception Object :",str(exception_object),"]",
                                 "[ Exception Traceback Summary :",str(traceback.extract_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Detailed :",str(traceback.format_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Line No. :",str(exception_traceback.tb_lineno),"]",
                                 "[ Output Path :",path_output,"]",
                                 "[ ",other_var_name," :",other_var,"]",
                                 ])
            log_file.write("\n============================================================\n")
            log_file.write("==============================================================\n")
            log_file.close()
            
        else:
            log_file = open(path_output +'/'+ logger_no + '.txt', 'a+')
            log_file.write("=====================================================================\n")
            log_file.write("< ExceptionLogger Log Exception Data : Output path passed by User >\n")
            log_file.write("=====================================================================\n")
            log_file.writelines(["[ Logged Time :",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"]",
                                 "[ Logger Name :",logger_no,"]",
                                 "[ Funtion Name :",function_name,"]",
                                 "[ Task Status :",task_status,"]",
                                 "[ Logger_Exception_Error :",str(err.args[0]),"]",
                                 "[ Exception Type :",str(exception_type),"]",
                                 "[ Exception Object :",str(exception_object),"]",
                                 "[ Exception Traceback Summary :",str(traceback.extract_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Detailed :",str(traceback.format_tb(exception_traceback)),"]",
                                 "[ Exception Traceback Line No. :",str(exception_traceback.tb_lineno),"]",
                                 "[ Output Path :",path_output,"]",
                                 "[ ",other_var_name," :",other_var,"]",
                                 ])
            log_file.write("\n===================================================================\n")
            log_file.write("=====================================================================\n")
            log_file.close()
            
        
##############################################################################################################         

# logger('log3','loggertest','','','URL','http://test.com123') #


