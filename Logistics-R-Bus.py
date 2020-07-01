#Importing modules
import Bus_Logistics
import Bus_Logistics_DAO

User = Bus_Logistics.User
Driver = Bus_Logistics.Driver
Owner = Bus_Logistics.Owner
Admin = Bus_Logistics.Admin


#Driver
do = Driver(fName=None, lName=None, uName=None, pWord=None, phone=None, bus=None, ID=None)
#aseif asei51673
do.driver_options()
  
#Owner
own = Owner(fName=None, lName=None, uName=None, pWord=None, phone=None, active=None, ID=None)
#nlyimo, nlyi22913
own.owner_options()

#Admin :)
admin = Admin(adm_name=None, adm_pass=None)
#admin 4santeDr.Hu!
admin.admin_sign_in()