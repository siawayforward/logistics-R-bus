
#import other needed modules
!pip install mysqlclient -q
import MySQLdb   
import DAO_Modules

#import needed python modules
import datetime as d
import calendar as cal
import getpass as gp

#Formatting class (https://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python)
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

#Main class for users, generic class for bus owner, will be extended for driver
class User:
    
    #Constructor/Initializer for user
    def __init__(self, **kwargs):
        self._first_name = kwargs['fName']
        self._last_name = kwargs['lName']
        self._username = kwargs['uName']
        self._password = kwargs['pWord']
        self._phone_number = kwargs['phone']

    #Accessors/tantamount to getters and setters
    #having additional arg allows to check if value is available, if not, set value then return it or return whatever exists
    def first_name(self, fn = None):
        if fn: self._first_name = fn
        return self._first_name

    def last_name(self, ln = None):
        if ln: self._last_name = ln
        return self._last_name

    def username(self, un = None):
        if un: self._username = un
        return self._username

    def password(self, pw = None):
        if pw: self._password = pw
        return self._password
    
    def phone_number(self, pn = None):
        if pn: self._phone_number = pn
        return self._phone_number
            
    #Function to get credentials for log in:
    def get_credentials(self, error_note):
        #get the username and password
        self.username = input('Username: ')
        while self.username is None:
            self.username = input(error_note, 'username: ') 
        #only get PW if username is entered
        self.password = gp.getpass('Password: ')
        while self.password is None:
            self.password = gp.getpass(error_note, 'password: ')
            
    #method to copy one object into another
    def copy(self, user, table):
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.username = user.username
        self.password = user.password
        self.phone_number = user.phone_number
        if table == 'driver':
            self.assigned_bus = user.assigned_bus
            self.driver_ID = user.driver_ID
        if table == 'owner':
            self.active = user.active
            self.owner_ID = user.owner_ID
        
    #Allows user to log into account        
    def user_login(self, table):
        #check database to see if values exist (by count) and return value or error message
        print('\n' + color.DARKCYAN + color.BOLD +  'Log in to Logistics-R-Bus:' + color.END)
        #Driver check
        if table == 'driver':
            #get credentials and object from database
            self.get_credentials('Error! Please enter a valid')
            driver_cred = DAO_Modules.Driver_DAO.get_driver(self.username, self.password, 'Invalid credentials. Try again' ) 
            while driver_cred is None:
                self.get_credentials('Error! Please enter a valid')
                driver_cred = DAO_Modules.Driver_DAO.get_driver(self.username, self.password, 'Invalid credentials. Try again' ) 
            return self.copy(driver_cred, 'driver')
        #Owner check
        if table == 'owner':
            #get credentials and object from database
            self.get_credentials('Error! Please enter a valid')
            owner_cred = DAO_Modules.Owner_DAO.get_owner(self.username, self.password, 'Invalid credentials. Try again' )
            while owner_cred is None:
                self.get_credentials('Error! Please enter a valid')
                owner_cred = DAO_Modules.Owner_DAO.get_owner(self.username, self.password, 'Invalid credentials. Try again' ) 
            return self.copy(owner_cred, 'owner')       
    
    #Function to send user back to log in page
    def back_to_login(self, table):
        if input('To log in, enter 1. Enter 0 to exit ') == '1':
            if table == 'driver':
                self.user_login(table)
            if table == 'owner':
                self.user_login(table)
        else:
            print('Thank you for using Logistics-R-Bus!')
    
    #Function to get user inputs for making a new profile
    def get_sign_up_values(self, table):
        #get values
        self.first_name = input('First Name: ')
        self.last_name = input('Last Name: ')
        self.phone_number = input('Phone Number: ')
        #Username, password, and account specific credentials
        if table == 'driver':
            self.get_credentials('Duplicate credential! Please choose a unique')
            driver_cred = DAO_Modules.Driver_DAO.get_driver(self.username, self.password,' ')
            while driver_cred:
                self.get_credentials('Duplicate credential! Please choose a unique')
                driver_cred = DAO_Modules.Driver_DAO.get_driver(self.username, self.password,' ')
                self.copy(driver_cred, 'driver')
        if table == 'owner':
            self.active = 1
            self.get_credentials('Duplicate credential! Please choose a unique')
            owner_cred = DAO_Modules.Owner_DAO.get_owner(self.username, self.password,' ')
            while owner_cred:
                self.get_credentials('Duplicate credential! Please choose a unique')
                owner_cred = DAO_Modules.Owner_DAO.get_owner(self.username, self.password,' ')
                self.copy(owner_cred, 'owner')
        
    #Function to add new user (bus owner in this case)
    def add_new_user(self, table):
        added = False #account creation flag
        print(color.BOLD + '\nNew Account Sign Up:' + color.END, \
              '\nPlease provide the following credentials for a new account:')
        if table == 'driver':
            #Driver sign up
            self.get_sign_up_values('driver') #get values
            #insert/create account
            DAO_Modules.Driver_DAO.add_new_driver(self)
        if table == 'owner':
            #Owner sign up
            self.get_sign_up_values('owner') #get values
            #insert/create account
            DAO_Modules.Owner_DAO.add_new_owner(self)        
            

#Subclass of the user class
class Owner(User):
    
    #Initializer for a new owner (using some user methods from super class)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._active = kwargs['active']
        self._owner_ID = kwargs['ID']
        
    #getters and setters
    def owner_ID(self, ID = None):
        if ID: self._owner_ID = int(ID)
        return self._owner_ID
    
    def active(self, act = None):
        if act: self._active = int(act)
        return self._active
    
    #method to redirect back to the log in or exit
    def redirect(self):
        print(color.BOLD + '\nRedirecting to owner options...' + color.END)
        self.own_login_options()
    
    #method to show user view of system
    def owner_options(self):
        print(color.DARKCYAN + color.BOLD + 'Welcome to Logistics-R-Bus!' + color.END)
        decide = input('\n1 = Log in \n2 = Sign Up: ')
        while decide != '1' and decide != '2':
            decide = input('Invalid Entry! Enter: \n1 = Log in \n2 = Sign Up: ')
        if decide == '1':
            self.user_login('owner')
            self.own_login_options()
        elif decide == '2':
            self.add_new_user('owner')
            #give option to log in
            self.user_login('owner')
            self.own_login_options()
        else: 
            print('Invalid selection. Redirecting...')
            self.owner_options()
    
    #method to distinguish owner messages and options based on account status
    def owner_view(self):
        view = [] #owner messages and options
        #owner items
        messages = '\nYou have no new messages.'
        options = color.BOLD + '\nFor your options, enter:' + color.END
        if self.active() == 0:
            messages = '\nYour account has been deactivated. Contact local office for details.'
            options = '\nOwner functions disabled \nThank you for using Logistics-R-Bus!'
        view.extend([messages, options])
        return view    
            
    #method to login and use/view options
    def own_login_options(self):
        #display options for owner to pick from
        view = self.owner_view()
        print('\nHello, ', self.first_name(), '!', view[0], view[1])
        #Add logic for deactivated owner
        if self.active() == 1:
            #user actions
            proceed = input('1 = Add Buses \n2 = Assign Buses \n0 = Exit: ')
            if proceed == '1':
                print(color.BOLD +'\nAdd a New Bus:' + color.END)
                self.add_new_bus()
                self.redirect() #back to options    
            elif proceed == '2':
                bus = self.validate_bus_addition('Please provide the bus license plate number (T000 LLL): ')
                self.assign_bus_to_driver(bus)
                self.redirect() #back to options    
            else:
                print('Thank you for using Logistics-R-Bus!')
                   
            
    #method to validate bus inputs before adding a new bus
    def validate_bus_addition(self, input_note): 
        #get user input
        new_bus = input(input_note)
        #see if bus is already in the system or in wrong format
        #check entry format
        while new_bus is None or len(new_bus) != 8 \
        or (new_bus[0] != 'T' or new_bus[5:].isalpha() == False) \
        or new_bus[1:4].isdigit() == False or new_bus[4].isspace() == False:
            new_bus = input('Invalid format. {}'.format(input_note))
        return new_bus       
    
    #method to add a new bus
    def add_new_bus(self):
        #get bus information from owner and validate inputs
        bus_no = self.validate_bus_addition('Please provide the bus license plate number (T000 LLL): ')
        #check system for comparison
        buses = DAO_Modules.Bus_DAO.get_owner_buses(self.owner_ID())
        flag = False
        for bus in buses:
            if bus.bus_number() == bus_no: flag = True
        if flag == True: 
            print('Bus {} is already in the system'.format(bus_no))
            self.redirect()
        else:
            #define bus item
            new_bus = Bus(bus = bus_no, owner=str(self.owner_ID()), active=0)
            #confirm addition and add/ confirmation message
            proceed = input('Confirm you would like to add bus {} (Y/N): '.format(bus_no))
            if proceed.upper() == 'Y':
                proceed = None #reset
                if DAO_Modules.Bus_DAO.add_new_bus(new_bus):
                    #check if owner wants to assign bus to a driver immediately
                    proceed = input('Would you like to assign bus {} to a driver? (Y/N): '.format(bus_no))
                    if proceed.upper() == 'Y': self.assign_bus_to_driver(bus_no)
                    else: self.redirect()
                else: self.redirect()
            else: #redirect
                print(color.DARKCYAN + color.BOLD + 'Bus {} will not be added to your inventory'.format(bus_no) + color.END)
                self.redirect()            
    
    #method to assign or reassign buses to drivers
    def assign_bus_to_driver(self, new_bus):
        print(color.BOLD + '\nAssign Bus to Driver:' + color.END)
        bus_detail = DAO_Modules.Bus_DAO.get_bus(new_bus)
        for row in bus_detail:
            if row[0]:
                #Get driver that owner wants to assign bus to
                fName = input('Please enter driver\'s credentials \nFirst Name: ')
                lName = input('Last Name: ')
                #check system to see if driver exists or ask owner to update name
                driver = DAO_Modules.Driver_DAO.get_driver_by_name(fName, lName)
                if driver:
                    if str(driver.assigned_bus()) and str(driver.assigned_bus()) != 'T000 LLL':
                        #change status of current bus assignment to active = 0 if exists
                        DAO_Modules.Bus_DAO.change_bus_status(driver.assigned_bus(), 0)
                        #change to the new bus and confirm
                        driver.assigned_bus(new_bus)
                        DAO_Modules.Driver_DAO.assign_bus(driver)
                        #change status of the newly assigned bus to active
                        DAO_Modules.Bus_DAO.change_bus_status(driver.assigned_bus(), 1)
                    if str(driver.assigned_bus()) == 'T000 LLL':
                        #change to the new bus and confirm
                        driver.assigned_bus(new_bus)
                        DAO_Modules.Driver_DAO.assign_bus(driver)
                        #change status of the newly assigned bus to active
                        DAO_Modules.Bus_DAO.change_bus_status(driver.assigned_bus(), 1)
                else:
                    print('{} {} could not be found on our list of drivers'.format(fName, lName))
            else:
                print('Bus {} could not be found in your inventory'.format(new_bus))
            
        

#Subclass of the user class
class Driver(User):
    
    #Initializer for a new driver (using add new user method from super class)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._assigned_bus = kwargs['bus']
        self._driver_ID = kwargs['ID']
    
    #Getters and setters
    def driver_ID(self, ID = None):
        if ID: self._driver_ID = int(ID)
        return self._driver_ID
    
    def assigned_bus(self, ab = None):
        if ab: self._assigned_bus = ab
        return self._assigned_bus
    
    #method to show message on login
    def driver_login_view(self):
        #check bus status
        buses = DAO_Modules.Bus_DAO.get_bus(self.assigned_bus())
        #check admin scheduled runs
        runs = DAO_Modules.Schedule_DAO.get_upcoming_runs(self.assigned_bus())
        admin_dates = []
        if runs:
            for run in runs: 
                if run.added_by() == 1: admin_dates.append(run.schedule_date())
        if buses: 
            for x in buses: bus = x
        #Messages viewed
        print('\nHello, ', self.first_name() + '!')
        messages = ''
        options = ''
        if self.assigned_bus() == 'T000 LLL':
            messages = 'Contact your owner to request a bus assignment'
        if self.assigned_bus() != 'T000 LLL': 
            messages = '\n{}'.format(self.assigned_bus()) + messages
        if int(bus[3]) == 0 and self.assigned_bus() != 'T000 LLL':  #bus status
            messages = '\nBus {} has been deactivated. Contact the bus owner for details.'.format(self.assigned_bus())
        if len(admin_dates) != 0: #admin scheduled dates
            messages = '\nTZ transit has scheduled you to work on:'
            for x in admin_dates: 
                messages += ' ' + x.strftime('%Y-%m-%d') 
            options = color.BOLD + '\nFor your options, enter:' + color.END
        if self.assigned_bus() == None or (int(bus[3]) != 0 and len(admin_dates) == 0):
            messages = '\nYou have no new messages.'
            options = color.BOLD + '\nFor your options, enter:' + color.END
        #display login message
        print(messages, options)
        return str(bus[3])
        
    #method to show user view of system
    def driver_options(self):
        print(color.DARKCYAN + color.BOLD + 'Welcome to Logistics-R-Bus!' + color.END)
        decide = input('\n1 = Log in \n2 = Sign Up: ')
        while decide != '1' and decide != '2':
            decide = input('Invalid Entry! Enter: \n1 = Log in \n2 = Sign Up: ')
        if decide == '1':
            self.user_login('driver')            
            self.dr_login_options(self.driver_login_view())
        elif decide == '2':
            self.add_new_user('driver')
            #give them the option to log in
            self.user_login('driver')            
            self.dr_login_options(self.driver_login_view())
        else: 
            print('Invalid selection. Redirecting...')
            self.driver_options()
            
    #method to log in and view options
    def dr_login_options(self, decide):
        proceed = ''
        if decide == '1': proceed = input('1 = Set your schedule \n0 = Exit: ')
        else: proceed = '0'
        while proceed != '1' and proceed != '0':
            proceed = input('\nError! Select: \n1 = to Set your schedule \n0 = Exit: ') 
        if proceed == '1':
            proceed = None #reset
            #show more options
            print(color.BOLD + '\nSchedule Selection (enter number to select)' + color.END)
            proceed = input('1 = Add new schedule run(s) \n2 = Change current scheduled run(s): ')
            while proceed != '1' and proceed != '2':
                proceed = input('\nInvalid selection! \n1 = Add new schedule run(s) \n2 = Change current scheduled run(s): ')
            if proceed == '1':
                self.set_driver_run() #set a new schedule
            elif proceed == '2':
                proceed = None
                #update current schedule
                proceed = input('\n1 = Change scheduled run(s) \n2 = Delete scheduled run(s): ')
                while proceed != '1' and proceed != '2':
                    proceed = input('\nInvalid selection! \n1 = Change scheduled run(s) \n2 = Delete scheduled run(s): ')
                if proceed == '1':
                    print('Note: You can only update runs at least two days from today \n')
                    update = input('Enter 1 to proceed or 0 to add a new run: ')
                    while update != '1' and update != '0':
                        update = input('\nError! Enter 1 to proceed or 0 to add a new run: ')
                    if update == '1':
                        self.update_scheduled_run()
                    elif update == '0':
                        self.set_driver_run() 
                    else: self.redirect()
                elif proceed == '2': #delete a run
                    self.delete_scheduled_run()
                else: self.redirect()
            else: self.redirect()
        else:
            print('No tasks here! Thanks for using Logistics-R-Bus!')
    
    #method to redirect back to the log in or exit
    def redirect(self):
        print(color.BOLD + '\nRedirecting to driver options...' + color.END)
        self.dr_login_options('1')
            
    #method to get next possible schedule day depending on the type of schedule
    def get_next_day(self, sch_type):
        dt = d.date.today().weekday()  
        target = 0 #mondays
        #weekly schedule, have to start with a Monday
        if sch_type == '1' and target <= dt:
            next_day = d.date.today() + d.timedelta(-1*(dt - target) + 7)
        elif sch_type == '1' and target > dt:
            next_day = d.date.today() + d.timedelta(-1*(dt - target))
        else:
            #otherwise have to schedule at least two days in advance
            next_day = d.date.today() + d.timedelta(2) 
        #return the date value
        return next_day

    #method to get schedule type from driver and provide next available opening
    def get_schedule_type(self):
        #show options
        print(color.BOLD + '\nSchedule Options: 1 = Weekly, 2 = Daily' + color.END)
        sch_type = input('Please enter a preferred schedule type: ')
        while sch_type == None:
            sch_type = input('Error: Please specify schedule type before proceeding: ')
        #format scheduled days
        next_day = self.get_next_day(sch_type)
        date_val = date_val = next_day.strftime("%a, %d %b, %Y")
        #show next day and ask for times of day and collect info to search available routes
        if sch_type == '1':    
            print('\nThe next week starts on: ', date_val)
        if sch_type == '2':
            print('\nThe next day available to schedule is: ', date_val)
        return sch_type
    
    #method to get and collect driver preference for run time and dates based on schedule type (Weekly, daily, custom)
    def get_driver_days(self):
        #get the next available day for the driver to schedule
        sch_type = self.get_schedule_type()
        #inquiry to check for routes
        inquiry = None
        #Check if user wants to proceed with the next available day
        if input('Enter "1" to proceed, or "0" to exit: ') == '1':
            #set values and add to inquiries list
            run = input('\nTo select preferred run time, enter "AM" (6am-2pm) or "PM" (2pm-10pm): ')
            while run.upper() != 'AM' and run.upper() != 'PM':
                run = input('\nError! Please select a preferred run time: "AM" and "PM": ')
            #store entry as inquiry for the driver to select a route based on given dates
            next_day = self.get_next_day(sch_type)
            if sch_type == '1': #weekly, add to list of inquiries
                #create a schedule inquiry instance to save the data to
                inquiry = Schedule(bus=self.assigned_bus(), route=None, run=run.upper(), start_date=next_day, end_date=next_day + d.timedelta(6), added=0)  
            #check if daily user wants to schedule another day (daily schedule)
            if sch_type == '2':
                decision = input('\nEnter "1" to schedule the next day and same time run or 0 to finish: ')
                count = 0 #how many more days to add
                while decision == '1':
                    count += 1 
                    decision = input('\nEnter "1" to schedule the next day and same time run or 0 to finish: ')
                    if count == 5: #can add up to 5 more days
                        print('You have reached the maximum number of days for a maximum schedule')
                        break                        
                inquiry = Schedule(bus=self.assigned_bus(), route=None, run=run.upper(), start_date=next_day, end_date=next_day + d.timedelta(count), added=0)
        else:
            self.redirect() #option to exit           
        #return schedule inquiry to check for route need
        return inquiry
    
    #method to get driver route selection and verify bus code entry from the options given based on their availability
    def route_validation(self, need_routes):
        code = input('Please enter the route code for your preferred route: ')
        #check if code entered is valid from options given
        flag = False
        for row in need_routes:
            if code.upper() == row[0]: flag = True
        #confirm with driver and schedule route runs
        while flag == False:
            code = input('Error! Enter a route code from the offered options: ')
            for row in need_routes:
                if code.upper() == row[0]: flag = True
        #continue to confirmation and set up
        yes = input('Please enter 1 to confirm route and 0 to pick another route: ')
        if yes == '1': return code.upper() #now ready for insertion
        else: return self.route_validation(need_routes)
    
    def add_new_driver_run(self, need_routes, inq):
        if need_routes is not None and inq is not None:
            inq.route_number(self.route_validation(need_routes))
            #date objects
            delta = d.timedelta(1)
            start = d.datetime.strptime(str(inq.schedule_date()), '%Y-%m-%d')
            end = d.datetime.strptime(str(inq.end_schedule_date()), '%Y-%m-%d')
            count = 0 #tracking number of runs added
            while start <= end:
                #check if such a run already exists
                inq.schedule_date(start)
                if DAO_Modules.Schedule_DAO.get_scheduled_run(inq):
                    print('Error! You are already scheduled to drive on {}'.format(inq.schedule_date()))
                    count +=1 #track number of scheduled runs that week
                    start += delta
                else: #insert and track each run
                    count += DAO_Modules.Schedule_DAO.add_new_schedule(inq)
                    start += delta #move to next date
            #Prompt the user for their upcoming scheduled runs
            print('You have {} {} runs scheduled from {} to {}.'\
                  .format(str(count), inq.run_time(), inq.schedule_date(start + d.timedelta(count*-1)), inq.end_schedule_date()))
        else: #no run to add
            print('Driver run will not be scheduled.')
        
    #method to set driver route based on specified availability
    def set_driver_run(self):
        #get an inquiry from user
        inq = self.get_driver_days()
        #check for available routes
        need_routes = DAO_Modules.Route_DAO.get_need_routes(inq)
        #format and display availability to driver
        if need_routes is not None and inq is not None:
            print(color.BOLD + '\nFor your availability of {sd} to {ed} for {r:2s} run(s) '\
                  .format(sd=inq.schedule_date(), ed=inq.end_schedule_date(), r=inq.run_time()) \
                  +'\nThe following routes are available to schedule:'+ color.END)
            #formatter for route list
            formatter = '{code:15s} {start:20s} {end:20s} {need:5s}'
            #display all available routes
            print(color.BOLD + formatter.format(code='Route Code', start='From Location',\
                                                end='To Location', need='Drivers Needed')+ color.END)
            for row in need_routes:
                if row[0] is not None:
                    print(formatter.format(code=row[0], start=row[1], end=row[2], need=str(row[3])))
            #code validation and insertion
            #ask the driver to enter preferred route, validate and inserting
            self.add_new_driver_run(need_routes, inq)
            #give option to exit or log back in
            self.redirect()
        else:
            print('Driver run will not be scheduled')

    #method to check update item and get user input
    def check_update_item(self, item):
        value = None #return value
        #ask user about item to update (could be run, date)
        decide = input('To update the {}, Enter Y/N: '.format(item)).upper()
        while decide.upper() != 'Y' and decide.upper() != 'N':
            decide = input('\nError! Enter Y/N to update the {}: '.format(item)).upper()
        if decide.upper() =='Y':
            if item == 'run': 
                value = input('\nPlease enter desired {} (AM or PM) : '.format(item)).upper()
                while value != 'AM' and value != 'PM':
                    value = input('\nError! Please enter valid {} (AM or PM) : '.format(item)).upper()
            if item == 'date':
                value = Admin(adm_name=None, adm_pass=None)\
                .check_date_entry('\nPlease enter desired {} (YYYY-MM-DD) : '.format(item))
        else:
            print('\n{} will remain unchanged for your scheduled run.'.format(item.title()))
        return value
    
    #method to get the run that a user wants to update
    def get_update_run(self, note):
        #get all routes for verification
        runs = DAO_Modules.Schedule_DAO.get_upcoming_runs(self.assigned_bus())
        if len(runs) == 0:
            print('You do not have any upcoming runs scheduled')
            self.redirect()
        else:
            #formatter for run list
            form = '{x:2s} {date:15s} {route:15s} {run:5s}'
            print(color.BOLD + form.format(x='#', date='Scheduled For', route='Route Code', run='Run Time') + color.END)
            for sch_run in runs:
                idx = runs.index(sch_run) + 1
                print(form.format(x=str(idx), date=str(sch_run.schedule_date()), route=sch_run.route_number(), run=sch_run.run_time()))
            #get item from user
            item = int(input('Please enter the number of the run you\'d like to update: ')) - 1
            while item not in range(len(runs)):
                item = int(input('\nError! Please enter the number of the run you\'d like to {}: '.format(note)))
            #access and return current run how it is
            return runs[item]        
    
    #method to update a current schedule run (only can update time of day, route, date)
    def update_scheduled_run(self):
        current = self.get_update_run('update')
        if current:
            new_run = Schedule(route=current.route_number(), run=current.run_time(), start_date=current.schedule_date(), \
                               end_date=current.schedule_date(), bus=self.assigned_bus(),added='0')
            #check what the driver wants to update (both run and date) and assign to new object
            new_date =  self.check_update_item('date')
            if new_date: 
                new_run.schedule_date(d.datetime.strptime(new_date, '%Y-%m-%d'))
                print('New date: ', str(new_run.schedule_date()))
            new_runtime = self.check_update_item('run')
            if new_runtime: 
                new_run.run_time(new_runtime)
                print('New run: ',new_run.run_time())
            #check with user before updating current item
            decide = input('\nAccept new changes? (1 for Yes, 0 for No): ')
            while decide != '1' and decide != '0':
                decide = input('\nError! Accept new changes? (1 for Yes, 0 for No): ')
            #make changes and notify user
            if decide == '1': 
                #see if updated run exists before changing to it
                print(color.BOLD + 'Run Details: ' + color.END , str(new_run.schedule_date()), new_run.bus_code() ,\
                      new_run.run_time(), new_run.route_number()+ color.END)
                if DAO_Modules.Schedule_DAO.get_scheduled_run(new_run):
                    print(color.RED + 'Error! Another identical run for {} exists.'.format(str(new_run.schedule_date()))+ color.END)
                    self.redirect()
                else:  #add to database and notify user
                    DAO_Modules.Schedule_DAO.update_schedule_run(new_run, current)
                    self.redirect()
            else: #no updates 
                print('Your scheduled run on {} will remain unchanged.'.format(str(current.schedule_date())))
                self.redirect() #redirect
        else: self.redirect()
            
    #method to delete a scheduled run
    def delete_scheduled_run(self):
        #get driver's upcoming run to delete
        current = self.get_update_run('delete')
        #confirm with user before deleting
        decide = input('Are you sure you would like to delete this run? (Y/N): ')
        while decide.upper() != 'Y' and decide.upper() != 'N':
            decide = input('Error! Please inform if you want to delete this run (Y/N): ')
        if decide.upper() == 'Y':
            DAO_Modules.Schedule_DAO.delete_schedule_run(current)
        else:
            print('Your run on {} will remain as scheduled.'.format(str(current.schedule_date())))
        #back to home page
        self.redirect()
        

import calendar as cal
class Admin:
    
    #Initializer
    def __init__(self, **kwargs): 
        self._ad_name = kwargs['adm_name']
        self._ad_pass = kwargs['adm_pass']
    
    #getters and setters
    def username(self, un = None):
        if un: self._ad_name = un
        return self._ad_name

    def password(self, pw = None):
        if pw: self._ad_pass = pw
        return self._ad_pass
        
    #method to redirect back to the log in or exit
    def redirect(self):
        print(color.BOLD + '\nRedirecting to options...' + color.END)
        self.admin_options()
            
    #method for admin to sign into the system
    def admin_sign_in(self):
        print('\n' + color.BLUE + color.BOLD +  'Admin Log in to Logistics-R-Bus:' + color.END)
        #actual credentials
        f = open('Admin.txt', 'r')
        user = f.readline()
        passwd = f.readline()
        #get user inputs
        self.ad_name = input('Admin username: ')
        while self.ad_name is None and self.ad_name != user:
            self.ad_name = input('Invalid credentials! Enter Admin username: ')
        self.ad_pass = gp.getpass('Admin password: ')
        while self.ad_pass is None and self.ad_pass != passwd:
            self.ad_pass = gp.getpass('Invalid credentials! Enter Admin password: ')
        #go on to admin functions if credentials are valid
        self.admin_options()    
        
    #method to define the options the admin user can navigate through
    def admin_options(self):
        #show options
        print(color.BOLD + '\nFor your options, select:' + color.END)
        decide = input('1 = Route Daily Report \n2 = Change Route Schedule \n3 = Change Route Need '\
                       ' \n4 = Change Bus Status \n5 = Change Owner Status \n0 = Exit: ')
        if decide == '1': #get route and date of interest on display
            print(color.BOLD+'\nFuture Route Needs by Date:'+color.END)
            self.check_route_need('Enter the date to review (YYYY-MM-DD): ')
        elif decide == '2': #allow to change drivers assigned to a route based on need
            #check route need and reassign
            self.check_route_need('Please enter the date for route changes (YYYY-MM-DD): ')
            self.redirect()
        elif decide == '3': #change route metrics
            print(color.BOLD + '\nRoute Updates: '+color.END)
            self.change_route_need()
            self.redirect()
        elif decide == '4': #change a bus status
            self.change_bus_status()
            self.redirect() #back home
        elif decide == '5': #change owner status
            print(color.BOLD + '\nOwner Updates:' + color.END)
            fName = input('Enter owner first name: ')
            lName = input('Enter owner last name: ')
            action = input('Enter: \n1 to activate owner \n0 to deactivate owner: ')
            while action != '1' and action != '0':
                action = input('Invalid selection! Enter \n1 to activate owner \n0 to deactivate owner: ')
            #get owner
            own = DAO_Modules.Owner_DAO.get_owner_by_name(fName, lName, 'Invalid credentials. Try again' )
            if own: #update owner account and buses if owner exists
                DAO_Modules.Owner_DAO.change_owner_status(own.owner_ID(), int(action))
                #update buses if owner is deactivated
                if int(action) == 0: 
                    own_buses = DAO_Modules.Bus_DAO.get_owner_buses(own.owner_ID()) 
                    for bus in own_buses: #deactivate all buses
                        DAO_Modules.Bus_DAO.change_bus_status(bus.bus_number(), 0)
                self.redirect()
            else: 
                print('{} {} is not listed as one of the bus owners in your system.'.format(fName, lName))
                self.redirect()
        elif decide == '0': #log out
            print('Admin user has been logged out')
        else: #invalid option, go back to front page
            print('Invalid selection')
            self.admin_options()            
    
    #method to get driver route selection and verify bus code entry from the options given based on their availability
    def route_validation(self, need_routes):
        code = input('Please enter the route code for your preferred route: ')
        #check if code entered is valid from options given
        flag = False
        for row in need_routes:
            if code.upper() == row[0]: flag = True
        #confirm with driver and schedule route runs
        while flag == False:
            code = input('Error! Enter a route code from the offered options: ')
            for row in need_routes:
                if code.upper() == row[0]: flag = True
        #continue to confirmation and set up
        yes = input('Please enter 1 to confirm route and 0 to pick another route: ')
        if yes == '1': return code.upper() #now ready for insertion
        else: return self.route_validation(need_routes)
        
    #method to deactivate a bus
    def change_bus_status(self):
        print(color.BOLD + 'Bus Changes:' + color.END)
        #get bus and validate input
        bus_x = input('Please provide the license plate code for the bus (T000 LLL): ')
        while bus_x is None or len(bus_x) != 8 \
        or (bus_x[0] != 'T' or bus_x[5:].isalpha() == False) \
        or bus_x[1:4].isdigit() == False or bus_x[4].isspace() == False:
            bus_x = input('Invalid format. Please provide the license plate code for the bus (T000 LLL): ')
        #see if bus exists to proceed
        bus = DAO_Modules.Bus_DAO.get_bus(bus_x) #retrieve bus
        for row in bus:
            if row: 
                print('Bus Details: ', row[0], 'Owner: ', row[1], row[2])
                action = int(input('Enter \n1 = Activate bus \n0 = Deactivate bus'))
                while action != 1 and action !=0:
                    action = int(input('Enter \n1 = Activate bus \n0 = Deactivate bus'))
                ##change bus status
                DAO_Modules.Bus_DAO.change_bus_status(bus_x, action)
            else: print('This bus doesn\'t exist in the system.')
    
    #method to change route need for a specific route
    def change_route_need(self):
        #get and display all routes
        routes = DAO_Modules.Route_DAO.get_all_routes()
        formatter = '{i:5s} {rc:15s} {s:15s} {e:15s} {am:10s} {pm:10s}'
        print(color.BOLD + formatter.format(i='#', rc='Route Code', s='Start Location', e='End Location', am='AM Need', pm='PM Need') + color.END)
        for route in routes:
            if route.route_code():
                idx = routes.index(route) + 1 #item number
                print(formatter.format(i=str(idx), rc=route.route_code(), s=route.start_location(),\
                                       e=route.end_location(), am=str(route.AM_need()), pm=str(route.PM_need())))
        #check with admin which route they want to change
        choice = int(input('Please select the # for the route you\'d like to update: ')) - 1
        while choice not in range(len(routes)):
            choice = int(input('Error! Please select the driver you\'d like to assign to route {}: '.format(route))) - 1
        route = routes[choice]
        #update and confirm with admin
        AM = input('New Morning Need: ')
        PM = input('New Afternoon Need: ')
        while (AM is not None and AM.isdigit() == False) or (PM is not None and PM.isdigit() == False):
            AM = input('Invalid entry! New Morning Need: ')
            PM = input('Invalid entry! New Afternoon Need: ')
        #update route
        route.AM_need(AM)
        route.PM_need(PM)
        DAO_Modules.Route_DAO.update_route_need(route)
        
    #method to check if date was entered correctly
    def check_date_entry(self, input_note):
        #get user input
        date = input(input_note)
        while date is None or len(date) != 10:
            date = input('Error! Enter a valid date in form (YYYY-MM-DD): ')
        #split the date into its parts
        date_store = [int(date[:4]), int(date[5:7]), int(date[8:])] #store date
        #get year bandwidth
        yr_period = [int(d.datetime.now().year) - 1, int(d.datetime.now().year) + 1] 
        days = 7 #week period for checking dates (needs to be within a week of two days from now)
        valid_dates = [(d.datetime.now() + d.timedelta(x+2)).strftime('%Y-%m-%d') for x in range(days)]
        #check that a year, month, date are valid
        while (date_store[0] < yr_period[0] or date_store[0] > yr_period[1]) \
        or (date_store[1] not in range(1,13)) \
        or date_store[2] not in range(1, cal.monthrange(date_store[0], date_store[1])[1] + 1) \
        or date not in valid_dates:
            date = input('Error! The date is invalid or out of scheduling range ({} to {}).\nRe-enter date in form (YYYY-MM-DD): '.format(valid_dates[0], valid_dates[6]))
            date_store = [int(date[:4]), int(date[5:7]), int(date[8:])] #replace date
        return date
    
    #method to check how many routes need drivers scheduled
    def check_route_need(self, note):
        #get date of interest
        day = self.check_date_entry(note)
        need_areas = DAO_Modules.Route_DAO.get_next_route_need(day)
        #display schedules for that day
        formatter = '{r:15s} {runAM:10s} {runPM:5s}'
        print(color.BOLD + day + color.END)
        print(color.BOLD + formatter.format(r='\nRoute Code', runAM='AM Need', runPM='PM Need') + color.END)
        for row in need_areas:
            if row[0]: print(formatter.format(r=row[0], runAM=str(row[1]), runPM=str(row[2])))
        #check if admin wants to reassign a driver
        decide = input('Would you like to reassign a driver based on the above needs? (Y/N): ')
        if decide.upper() == 'Y':
            decide = None #reset
            #get route for reassignment
            route = self.route_validation(need_areas)
            self.assign_driver_routes(day, route)
        else:
            self.admin_options()
   
    #method to re-assign drivers to different routes in need
    def assign_driver_routes(self, day, route):
        print(color.BOLD + '\nAssign Drivers to Routes:' + color.END)
        #see drivers and assign a route to them
        print('Here is a list of drivers who are active to drive on {}: '.format(day))
        drivers = DAO_Modules.Driver_DAO.get_available_drivers(day)
        formatter = '{n:5s} {fn:15s} {ln:15s} {bus:10s}'
        print(color.BOLD + formatter.format(n='#', fn = 'First Name', ln='Last Name', bus='Bus Code') + color.END)
        for driver in drivers:
            if driver.first_name():
                idx = drivers.index(driver) + 1
                print(formatter.format(n=str(idx), fn=driver.first_name(), ln=driver.last_name(), bus=driver.assigned_bus()))
        #select driver to assign to route
        choice = int(input('Please select the driver you\'d like to assign to route {}: '.format(route))) - 1
        while choice not in range(len(drivers)):
            choice = int(input('Error! Please select the driver you\'d like to assign to route {}: '.format(route))) - 1
        dr = drivers[choice]
        run = input('Please provide the run you\'d like to schedule {} for (AM/PM): '.format(dr.first_name()+' ' +dr.last_name()))
        while run.upper() != 'AM' and run.upper() != 'PM':
            run = input('Invalid run. Please enter run to schedule {} (AM/PM)'.format(dr.first_name()+' ' +dr.last_name()))
        #create a schedule instance and add to the system
        sch_run = Schedule(route=route, run=run, bus=dr.assigned_bus(), start_date=day, end_date=None, added=1)
        #add a schedule run to the system (add column to indicate if admin scheduled or not in DB)
        print('{} {} has now been assigned to route {} on {}'.format(dr.first_name(), dr.last_name(), route, day))
        dr_note = '{} shift for route {} on {}'.format(run, route, day)
        return dr_note
         

class Schedule:    
    #Initializer/Constructor 
    def __init__(self, **kwargs): 
        if kwargs['bus']: self._bus_code = kwargs['bus']
        if kwargs['route']: self._route_number = kwargs['route']
        if kwargs['run']: self._run_time = kwargs['run']
        if kwargs['start_date']: self._schedule_date = kwargs['start_date']
        if kwargs['end_date']: self._end_schedule_date = kwargs['end_date']
        if kwargs['added']: self._added_by = int(kwargs['added'])
    
    #Getters and setters
    def bus_code(self, bc = None):
        if bc: self._bus_code = bc
        return self._bus_code
    
    def route_number(self, rn = None):
        if rn: self._route_number = rn
        return self._route_number
    
    def run_time(self, run = None):
        if run: self._run_time = run
        return self._run_time

    def schedule_date(self, sd = None):
        if sd: self._schedule_date = sd.strftime('%Y-%m-%d')
        return self._schedule_date

    def end_schedule_date(self, esd = None):
        if esd: self._end_schedule_date = esd
        return self._end_schedule_date
    
    def added_by(self, added = None):
        if added: self._added_by = int(added)
        return self._added_by

    #method to insert a new schedule run for a driver
    def add_new_run(self, schedule_run):        
        #flag for whether or not line was added
        checker = False 
        #access DAO method and add schedule
        count = DAO_Modules.Schedule_DAO.add_new_schedule(self)
        #check if schedule has been added
        if count > 0:
            checker = True
        return checker    

    
class Route:    
    #Initializer/Constructor 
    def __init__(self, **kwargs): 
        if kwargs['route']: self._route_code = kwargs['route']
        if kwargs['start']: self._start_location = kwargs['start']
        if kwargs['end']: self._end_location = kwargs['end']
        if kwargs['AM']: self._AM_need = kwargs['AM']
        if kwargs['PM']: self._PM_need = kwargs['PM']
    
    #Getters and setters
    def route_code(self, rc = None):
        if rc: self._route_code = rc
        return self._route_code
    
    def start_location(self, sl = None):
        if sl: self._start_location = sl
        return self._start_location
    
    def end_location(self, el = None):
        if el: self._end_location = el
        return self._end_location

    def AM_need(self, am = None):
        if am: self._AM_need = am
        return self._AM_need

    def PM_need(self, pm = None):
        if pm: self._PM_need = pm
        return self._PM_need

    #method to insert a new schedule run for a driver
    def add_new_route(self):    
        #create a new route code from getting user input
        start = input('Enter start location: ')
        if start: end = input('Enter end location: ')
        #flag for whether or not line was added
        checker = False 
        #access DAO method and add schedule
        checker = DAO_Modules.Route_DAO.add_new_schedule(None, new_route)
        #check if schedule has been added
        if checker == True:
            print(color.DARKCYAN + 'The new route ', new_route.route_code(), ' has been added' + color.END)
        return checker    

    
class Bus:
    #Initializer
    def __init__(self, **kwargs):
        if kwargs['bus']: self._bus_number = kwargs['bus']
        if kwargs['owner']: self._bus_owner = int(kwargs['owner'])
        if kwargs['active']: self._status = int(kwargs['active'])
    
    #getters and setters
    def bus_number(self, bn = None):
        if bn: self._bus_number = bn
        return self._bus_number
    
    def bus_owner(self, own = None):
        if own: self._bus_owner = int(own)
        return self._bus_owner
    
    def status(self, state = None):
        if state: self._status = int(state)
        return self._status
