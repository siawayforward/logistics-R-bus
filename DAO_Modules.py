
# install mysql and import database connector
!pip install mysqlclient -q
import MySQLdb   
#import used python classes
import datetime as d
#define today's date and format
today = d.datetime.now().strftime('%Y-%m-%d')


#import user classes notebook
!pip install nbimporter -q
import nbimporter
import User_Modules
from importlib import reload
reload(User_Modules)

#colors for formatting text
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



class Schedule_DAO:
    
    #Initializer
    def __init__(self): pass
    
    #method to add a new entry to the schedule table
    def add_new_schedule(entry):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host= 'localhost', user= uname, passwd = pword, database=db)
            cursor = conn.cursor()
            #define query for new line insertion
            query = 'INSERT INTO schedule(ScheduleDate, RouteCode, BusNumber, Run) ' \
            + 'VALUES(\'{}\', \'{}\', \'{}\',\'{}\')'\
            .format(entry.schedule_date(), entry.route_number().upper(), entry.bus_code(), entry.run_time().upper())
            #execute query
            cursor.execute(query)
            conn.commit()
            #check if insert happened
            count = cursor.rowcount
            #return number of rows inserted for schedule runs
            return count
        except:
            print(color.RED + color.BOLD + 'Insertion error! Please try again later' + color.END)              
    
    #get a scheduled run
    def get_scheduled_run(entry):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host= 'localhost', user= uname, passwd = pword, database=db)
            cursor = conn.cursor()
            #define query for update
            query = 'SELECT RouteCode, BusNumber, ScheduleDate, Run, Admin '\
            + 'FROM schedule WHERE BusNumber = \'{}\' AND ScheduleDate = \'{}\''\
            .format(entry.bus_code(), str(entry.schedule_date()))
            #execute query and get data into schedule object
            cursor.execute(query)
            result = cursor.fetchall()
            run = None
            for row in result:
                run = User_Modules.Schedule(route=row[0], bus=row[1], start_date=row[2], end_date=None, run=row[3], added=str(row[4]))
            #return object
            return run
        except:
            print(color.RED + color.BOLD +'Unable to access identical schedule run' + color.END)

        
    #method to update current schedule run
    def update_schedule_run(new, current):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host= 'localhost', user= uname, passwd = pword, database=db)
            cursor = conn.cursor()
            #define query for update
            query = 'UPDATE schedule '\
            + 'SET ScheduleDate = \'{}\', Run = \'{}\' '.format(str(new.schedule_date()), new.run_time())\
            + 'WHERE ScheduleDate = \'{}\' AND BusNumber = \'{}\' AND RouteCode = \'{}\''\
            .format(str(current.schedule_date()), current.bus_code(), current.route_number())
            #execute query
            cursor.execute(query)
            conn.commit()
            #notify user
            print(color.DARKCYAN + color.BOLD +'Schedule Run Updated!' + color.END)
        except:
            print(color.RED + color.BOLD +'Error! Run update failed at this time' + color.END)
        finally:
            cursor.close()
            conn.close()
           
    #delete a scheduled run
    def delete_schedule_run(entry):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host= 'localhost', user= uname, passwd = pword, database=db)
            cursor = conn.cursor()       
            #define query for new line insertion
            query = 'DELETE FROM schedule WHERE '\
            + 'RouteCode = \'{}\' AND BusNumber = \'{}\' AND Run = \'{}\' AND ScheduleDate = \'{}\''\
            .format(entry.route_number(), entry.bus_code(), entry.run_time().upper(), str(entry.schedule_date()))            
            #execute query
            cursor.execute(query)
            conn.commit()
            #Confirm if deletion happened
            print(color.DARKCYAN + color.BOLD +'Your run for {} has been deleted.'.format(str(entry.schedule_date())) + color.END)
        except:
            print(color.RED + color.BOLD +'Error! Could not delete run at this time' + color.END)            
        finally:
            cursor.close()
            conn.close()
    
    #get the bus circulation and runs scheduled for a particular day and time
    def get_day_count(time_of_day):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host= 'localhost', user= uname, passwd = pword, database=db)
            cursor = conn.cursor()
            #define query for new line insertion
            query = 'SELECT SUM(Run) FROM schedule ' \
            + 'WHERE ScheduleDate = \'{}\' AND Run = \'{}\''.format(today, time_of_day)
            #execute query
            cursor.execute(query)
            #get the count
            count = 0
            result = cursor.fetchall()
            for row in result:
                count += row[0]            
            #return value
            return count        
        except:
            print(color.RED + color.BOLD +'Could not return value' + color.END)            
        finally:
            cursor.close()
            conn.close() 
            
    #method to check whether any dates in the future have runs scheduled
    def check_future_need(inquiry):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host= 'localhost', user= uname, passwd = pword, database=db)
            cursor = conn.cursor()
            #define query
            query = 'SELECT RouteCode, IFNULL(COUNT(RouteCode),0) AS \'Scheduled\' FROM Schedule '\
            + 'WHERE Run = \'{run:2s}\' AND ScheduleDate BETWEEN \'{d1:10s}\' AND \'{d2:10s}\' GROUP BY RouteCode'\
            .format(run=inquiry.run_time(), d1=inquiry.schedule_date(), d2=inquiry.end_schedule_date())
            #execute query
            cursor.execute(query)
            result = cursor.fetchall()
            #get counts check
            count = 0 
            for row in result:
                count += row[1]
            return count
        except:
            print(color.RED + color.BOLD +'Route counting error' + color.END)
            
    #get list of all upcoming runs for a specific driver to update
    def get_upcoming_runs(bus):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host='localhost', user=uname, passwd=pword, database=db)
            cursor = conn.cursor()
            #define and execute query
            today = d.datetime.now()
            query = 'SELECT BusNumber, ScheduleDate, RouteCode, Run, Admin FROM Schedule '\
            + 'WHERE BusNumber = \'{}\' AND ScheduleDate >= \'{}\''.format(bus, today.strftime('%Y-%m-%d'))
            cursor.execute(query)
            #get the list of routes and store in array
            result = cursor.fetchall()
            routes = []
            for row in result:
                row = User_Modules.Schedule(bus=row[0], start_date=row[1], end_date=None, route=row[2], run=row[3], added=str(row[4]))
                routes.append(row)
            return routes
        except:
            print(color.RED + color.BOLD +'Future runs extraction error' + color.END)



class Route_DAO:
    
    #Initializer
    def __init__(self): pass
    
    #method to add a new route
    def get_current_route(route_code):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()
            
            #define and execute query for insertion
            query = 'SELECT RouteCode, StartLocation, EndLocation, MorningNeed, AfternoonNeed FROM route '\
            + 'WHERE RouteCode = \'{}\''.format(route_code)
            cursor.execute(query)
            #check if deletion happened and return flag
            result = cursor.fetchall()
            for row in result: route = User_Modules.Route(route=row[0], start=row[1], end=row[2], AM=row[3], PM=row[4])
            return route
        except:
            print(color.RED + color.BOLD +'Deletion error: Route could not be deleted.' + color.END)
        finally:
            cursor.close()
            conn.close()
            
    #method to get the daily scheduling for each route
    def get_next_route_need(day):
        try:
        #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()
            #define query for execution
            query = 'SELECT R.RouteCode, R.MorningNeed - COUNT(S.Run) \'AM\', R.AfternoonNeed \'PM\' '\
             + 'FROM route R JOIN schedule S ON S.RouteCode = R.RouteCode '\
             + 'WHERE S.Run = \'AM\' AND S.ScheduleDate = \'{}\' '.format(day)\
             + 'UNION SELECT r.RouteCode, r.MorningNeed \'AM\', r.AfternoonNeed \'PM\' '\
             + 'FROM route r JOIN schedule S ON S.RouteCode = R.RouteCode '\
             + 'GROUP BY S.RouteCode UNION '\
             + 'SELECT R.RouteCode, R.MorningNeed \'AM\', R.AfternoonNeed - COUNT(S.Run) \'PM\' '\
             + 'FROM route R JOIN schedule S ON S.RouteCode = R.RouteCode '\
             + 'WHERE S.Run = \'PM\' AND S.ScheduleDate = \'{}\' '.format(day)\
             + 'UNION SELECT r.RouteCode, r.MorningNeed \'AM\', r.AfternoonNeed \'PM\' '\
             + 'FROM route r JOIN schedule S ON S.RouteCode = R.RouteCode GROUP BY S.RouteCode'
            #execute query and return values
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except:
            print(color.RED + color.BOLD +'Database route need extraction error' + color.END)            
        finally:
            cursor.close()
            conn.close()
            
    #method to update daily need for a route
    def update_route_need(route):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()            
            #define query and execute
            query = 'UPDATE route SET MorningNeed = {}, AfternoonNeed = {} WHERE RouteCode = \'{}\''\
            .format(route.AM_need(), route.PM_need(), route.route_code())
            cursor.execute(query)
            conn.commit()
            print(color.DARKCYAN + color.BOLD + 'Route updated!' + color.END)
        except:
            print(color.RED + color.BOLD +'Database route update error' + color.END)
        finally:
            cursor.close()
            conn.close()

    #method to get routes based on where drivers are needed to allow a driver to set schedule
    def get_need_routes(inq):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()
            #time to check
            if inq.run_time().upper() == 'AM':
                time = 'MorningNeed'
            if inq.run_time().upper() == 'PM':
                time = 'AfternoonNeed'
            #define and execute query
            query = 'SELECT R.RouteCode, R.StartLocation, R.EndLocation, R.{} - COUNT(S.Run) \'{}\' '\
            .format(time, inq.run_time().upper())\
            + 'FROM route R JOIN schedule S ON S.RouteCode = R.RouteCode '\
            + 'WHERE S.Run = \'{}\' AND S.ScheduleDate = \'{}\' '.format(inq.run_time().upper(), inq.schedule_date())\
            + 'UNION SELECT r.RouteCode, r.StartLocation, r.EndLocation, r.{} \'{}\' '.format(time, inq.run_time().upper())\
            + 'FROM route r JOIN schedule S ON S.RouteCode = R.RouteCode GROUP BY S.RouteCode '
            #execute query
            cursor.execute(query)
            result = cursor.fetchall()
            return result        
        except:
            print(color.RED + color.BOLD +'Error - Failed to get need routes at this time' + color.END)      
    
    #method to get list of all routes
    def get_all_routes():
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()
            #define and execute query
            query = 'SELECT RouteCode, StartLocation, EndLocation, MorningNeed, AfternoonNeed FROM Route' 
            #execute query
            cursor.execute(query)
            result = cursor.fetchall()
            routes = [] #return value
            for row in result: 
                route = User_Modules.Route(route=row[0], start=row[1], end=row[2], AM=row[3], PM=row[4])
                routes.append(route)
            return routes        
        except:
            print(color.RED + color.BOLD +'Error - Failed to get need routes at this time' + color.END)   

            

class Driver_DAO:
    
    #Initializer
    def __init__(self): pass
    
    #method to check if credentials exist and get driver profile as they log in, or the bus they are assigned
    def get_driver(username, password, note):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()            
            #define and execute query
            query = 'SELECT FirstName, LastName, Username, Password, PhoneNumber, AssignedBus, DriverID '\
            + 'FROM driver WHERE (Username = \'{}\' and Password = \'{}\') OR Username = \'{}\''\
            .format(username, password, username) 
            cursor.execute(query) 
            #check result
            result = cursor.fetchall()
            #store result in module object for driver and return it
            for row in result:
                dr = User_Modules.Driver(fName=row[0], lName=row[1], uName=row[2], pWord=row[3], phone=row[4], bus=row[5], ID=row[6])
            if dr: return dr
        except:
            print(color.RED + color.BOLD + note + color.END)     
        finally:
            cursor.close()
            conn.close() 
    
        #method to check if credentials exist and get driver profile as they log in, or the bus they are assigned
    def get_driver_by_name(first, last):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()            
            #define and execute query
            query = 'SELECT FirstName, LastName, AssignedBus, DriverID '\
            + 'FROM driver WHERE FirstName = \'{}\' and LastName = \'{}\''.format(first, last) 
            cursor.execute(query) 
            #check result
            result = cursor.fetchall()
            #store result in module object for driver and return it
            for row in result:
                dr = User_Modules.Driver(fName=row[0], lName=row[1], uName=None, pWord=None, phone=None, bus=row[2], ID=row[3])
            if dr: return dr
        except:
            print(color.RED + color.BOLD +'Invalid credentials or driver may not exist in the system. Try again' + color.END)     
        finally:
            cursor.close()
            conn.close() 
            
    #method to check if credentials exist and get driver profile as they log in, or the bus they are assigned
    def get_available_drivers(day):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()            
            #define and execute query
            query = 'SELECT d.FirstName, d.LastName, d.AssignedBus '\
            + 'FROM driver d JOIN bus b ON d.AssignedBus = b.BusNumber '\
            + 'WHERE b.Active = 1 AND D.AssignedBus NOT IN '\
            + '(SELECT BusNumber FROM Schedule WHERE ScheduleDate = \'{}\')'.format(day) 
            cursor.execute(query) 
            #get and return result
            result = cursor.fetchall()
            drivers = [] #return value
            for row in result:
                driver = User_Modules.Driver(fName=row[0], lName=row[1], uName=None, pWord=None, bus=row[2], phone=None, ID=None)
                drivers.append(driver)
            return drivers
        except:
            print(color.RED + color.BOLD +'Could not retrieve available drivers at this time.' + color.END)     
        finally:
            cursor.close()
            conn.close() 
            
    #method to get a list of routes
    def add_new_driver(dr):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()            
            #define query
            query = 'INSERT INTO driver(FirstName, LastName, Username, Password, PhoneNumber, AssignedBus) ' \
            + 'VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'T000 LLL\')'\
            .format(dr.first_name, dr.last_name, dr.username, dr.password, dr.phone_number)
            #execute query
            cursor.execute(query)
            conn.commit()
            #notify user
            print(color.DARKCYAN + color.BOLD + 'Congratulations, {}! Your account has been created.'.format(dr.first_name))
        except:
            print(color.RED + color.BOLD +'Sorry, we could not create your account at this time' + color.END)               
        finally:
            cursor.close()
            conn.close()
            
    #method used to assign a bus to a driver
    def assign_bus(driver):
        #try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()            
            #define query
            query = 'UPDATE driver SET AssignedBus = \'{}\' WHERE DriverID = {}'.format(driver.assigned_bus(), driver.driver_ID())
            #execute query
            cursor.execute(query)
            conn.commit() 
            #update user
            print(color.DARKCYAN + color.BOLD +'{} {} has been assigned to bus {}.'.format(driver.first_name(), driver.last_name(), driver.assigned_bus()) + color.END)
        #except:
        #    print(color.RED + color.BOLD +'Error: Failed to complete assignment. Please try again later' + color.END)
        #finally:
        #    cursor.close()
        #    conn.close()


        
class Owner_DAO:
   
    #Initializer
    def __init__(self): pass
    
    #method to check if credentials exist
    def get_owner(username, password, note):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()
            #define and execute query
            query = 'SELECT FirstName, LastName, Username, Password, PhoneNumber, Active, OwnerID '\
            + 'FROM owner WHERE (username = \'{}\' and password = \'{}\') OR username = \'{}\''\
            .format(username, password, username) 
            cursor.execute(query)
            #check result and add to an owner object
            result = cursor.fetchall()
            for row in result:
                own = User_Modules.Owner(fName=row[0], lName=row[1], uName=row[2], pWord=row[3], \
                                         phone=row[4], active=row[5], ID=row[6])
            #return owner if found
            if own: return own
            else: return None
        except:
            print(color.RED + color.BOLD + note + color.END)
        finally:
            cursor.close()
            conn.close() 
    
    #method to get owner by name
    def get_owner_by_name(first_name, last_name, note):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()
            #define and execute query
            query = 'SELECT FirstName, LastName, Username, Password, PhoneNumber, Active, OwnerID '\
            + 'FROM owner WHERE firstname = \'{}\' and lastname = \'{}\''.format(first_name, last_name) 
            cursor.execute(query)
            #check result and add to an owner object
            result = cursor.fetchall()
            for row in result:
                own = User_Modules.Owner(fName=row[0], lName=row[1], uName=row[2], pWord=row[3], \
                                         phone=row[4], active=row[5], ID=row[6])
            #return owner if found
            if own: return own
            else: return None
        except:
            print(color.RED + color.BOLD + note + color.END)
        finally:
            cursor.close()
            conn.close() 
            
    #method to get a list of routes
    def add_new_owner(own):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()
            #define query
            query = 'INSERT INTO owner(FirstName, LastName, Username, Password, PhoneNumber, Active) ' \
            + 'VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 1)'\
            .format(own.first_name, own.last_name, own.username, own.password, own.phone_number)
            #execute query
            cursor.execute(query)
            conn.commit()
            #notify user
            print(color.DARKCYAN + color.BOLD + 'Congratulations, {}! Your account has been created.'.format(own.first_name))
        except:
            print(color.RED + color.BOLD +'Sorry, we could not create your account at this time' + color.END)            
        finally:
            cursor.close()
            conn.close()
            
    #method used to activate or deactivate owner in system        
    def change_owner_status(owner_id, status):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connection and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor()
            #define query
            query = 'UPDATE owner ' \
            + 'SET Active = {} WHERE OwnerID = {}'.format(status, owner_id)
            #execute query
            cursor.execute(query)
            conn.commit() 
            #update user
            if status == 1:
                print(color.DARKCYAN + color.BOLD +'Update complete: This owner has been activated.' + color.END)
            if status == 0:
                print(color.DARKCYAN + color.BOLD +'Update complete: This owner has been deactivated.' + color.END)
        except:
            print(color.RED + color.BOLD +'Error: Failed to complete update. Please try again later' + color.END)
        finally:
            cursor.close()
            conn.close()
        


class Bus_DAO:
    #Initializer
    def __init__(self): pass
    
    #Method to add a new bus
    def add_new_bus(bus):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connector and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor() 
            #define query
            query = 'INSERT INTO bus(BusNumber, BusOwnerID, Active) '\
            + 'VALUES(\'{}\', {}, {})'.format(bus.bus_number(), int(bus.bus_owner()), 0)
            #execute query
            cursor.execute(query)
            conn.commit()
            print(color.DARKCYAN + color.BOLD +'Bus {} has been added!\n'.format(bus.bus_number()) + color.END)
            return True
        except:
            print(color.RED + color.BOLD +'Error! Could not insert new bus at this time' + color.END)
            return False
        finally:
            cursor.close()
            conn.close()
       
    def change_bus_status(bus, status):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connector and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor() 
            #define and execute query
            query = 'UPDATE bus SET Active = {} WHERE BusNumber = \'{}\''.format(status, bus)
            cursor.execute(query)
            conn.commit()
            results = ['assigned', 'active!'] #for displaying to user
            if(status == 0): results = ['unassigned', 'inactive.']
            print(color.DARKCYAN + color.BOLD +'\nBus {}\'s is now {} and is {}'.format(bus, results[0], results[1]) + color.END)
        except:
            print(color.RED + color.BOLD +'Database update error. Failed to change bus assignment' + color.END)
        finally:
            cursor.close()
            conn.close()
    
    #method to get all buses owned by one person
    def get_owner_buses(owner_ID):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connector and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor() 
            #define and execute query
            query = 'SELECT BusNumber, BusOwnerID, Active FROM bus WHERE BusOwnerID = {}'.format(owner_ID)
            cursor.execute(query)
            result = cursor.fetchall()
            buses = [] #list to store items extracted
            for row in result:
                bus = User_Modules.Bus(bus=row[0], owner=row[1], active=row[2])
                buses.append(bus)
            return buses
        except:
            print(color.RED + color.BOLD +'Bus retrieval error' + color.END)
        finally:
            cursor.close()
            conn.close()
            
     #method to get all buses owned by one person
    def get_bus(bus):
        try:
            #database accessor objects
            uname = 'root'
            pword = ''
            db = 'buslogistics'
            #define connector and cursor
            conn = MySQLdb.connect(host = 'localhost', user = uname, passwd = pword, database = db)
            cursor = conn.cursor() 
            #define and execute query
            query = 'SELECT b.BusNumber, o.FirstName, o.LastName, b.Active FROM bus b '\
                + 'JOIN owner o ON b.BusOwnerID = o.OwnerID WHERE b.BusNumber =  \'{}\''.format(bus)
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except:
            print(color.RED + color.BOLD +'Bus retrieval error' + color.END)
        finally:
            cursor.close()
            conn.close()           
                      
