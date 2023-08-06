from dms_app.resources.login_register import Login, AddUser, SearchUser, UserRoleFilter, ChangeUserPassword, SuperLogin
from dms_app.resources.driver_functions import Driver, Status
from dms_app.resources.add_profile import AddEmployee, GetEmployee, EmployeeStatusFilter
from dms_app.resources.add_profile import SearchEmployee
from dms_app.resources.violation import ViolationOperations, ActiveViolations, SearchViolations, ViolationFilter, UpdateViolation
from dms_app.resources.schema import AddSchema
from dms_app.resources.person import ViolationsEmployee
from dms_app.resources.settings import PersonIdAutoIncrement
from dms_app.resources.fingerprint import AddFingerprint, MatchFingerprint
from dms_app.resources.roles_privileges import AddRolePrivileges, GetAllRolesPrivileges



def register_routes(api):
    api.add_resource(Login, "/LoginRegister")
    api.add_resource(AddUser, "/RegisterUser")
    api.add_resource(SearchUser, "/SearchUser")
    api.add_resource(UserRoleFilter, "/UserRoleFilter")
    api.add_resource(ChangeUserPassword, "/ ")
    api.add_resource(Driver, "/Employee")
    api.add_resource(Status, "/EmployeeStatus")
    api.add_resource(AddEmployee, "/EmployeeProfile")
    api.add_resource(GetEmployee, "/GetAllEmployees")
    api.add_resource(EmployeeStatusFilter, "/EmployeeStatusFilter")
    api.add_resource(SearchEmployee, "/SearchEmployee")
    api.add_resource(ViolationOperations, "/Violation")
    api.add_resource(ActiveViolations, "/GetActiveViolations")
    api.add_resource(SearchViolations, "/SearchViolations")
    api.add_resource(ViolationFilter, "/ViolationFilter")
    api.add_resource(UpdateViolation, "/UpdateViolation")
    api.add_resource(AddSchema, "/Schema")
    api.add_resource(ViolationsEmployee, "/Employee_Violations")
    api.add_resource(PersonIdAutoIncrement, "/PersonIdAutoIncrement")
    api.add_resource(AddFingerprint, "/AddFingerprint")
    api.add_resource(MatchFingerprint, "/MatchFingerprint")
    api.add_resource(AddRolePrivileges, "/AddRolePrivileges")
    api.add_resource(GetAllRolesPrivileges, "/GetAllRolePrivileges")
    api.add_resource(ChangeUserPassword, "/ChangeUserPassword")
    api.add_resource(SuperLogin, "/AdminLogin")