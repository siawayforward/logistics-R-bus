#Importing module and define classes needed
import Bus_Logistics

Driver = Bus_Logistics.Driver
Owner = Bus_Logistics.Owner
Admin = Bus_Logistics.Admin
c = Bus_Logistics.color

def main():
    note = '\nPlease select user type: \n 1 - Driver \t 2 - Owner \t 3 - Admin:\t'
    bad = '\nInvalid entry, try again'
    response = None
    try:
        response = int((input(note)).strip())
        while response not in range(1,4):
            response = int((input(c.RED + c.BOLD + bad + c.END + note)).strip())
    except:
        while response not in range(1,4):
            response = int((input(c.RED + c.BOLD + bad + c.END + note)).strip())
    finally:
        start_system(response)

def start_system(response):
    #allow prompts according to user5
    if response == 1:
        #Driver
        do = Driver(fName=None, lName=None, uName=None, pWord=None, phone=None, bus=None, ID=None)
        do.driver_options()
    if response == 2:
        #Owner
        own = Owner(fName=None, lName=None, uName=None, pWord=None, phone=None, active=None, ID=None)
        own.owner_options()
    if response == 3:
        #Admin :)
        admin = Admin(adm_name=None, adm_pass=None)
        admin.admin_sign_in()


if __name__ == '__main__':
    main()
