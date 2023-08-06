"""Stream type classes for tap-rev_io."""

#from msilib.schema import Property
from pathlib import Path
from tokenize import String
from typing import Any, Dict, Optional, Union, List, Iterable
from xml.dom.minicompat import StringTypes

from singer_sdk import typing as th
from sqlalchemy import null  # JSON Schema typing helpers

from tap_rev_io.client import rev_ioStream


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class InventoryItemStream(rev_ioStream):
    """Define custom stream."""
    name = "InventoryItem"
    path = "/InventoryItem"
    primary_keys = ["inventory_item_id"]
    schema_filepath = SCHEMAS_DIR / "InventoryItem.json"

class AddressesStream(rev_ioStream):
    """Define custom stream."""
    name = "Addresses"
    path = "/Addresses"
    primary_keys = ["address_id"]              
    schema_filepath = SCHEMAS_DIR / "Addresses.json"


class AgentsStream(rev_ioStream):
    """Define custom stream."""
    name = "Agents"
    path = "/Agents"
    primary_keys = ["agent_id"]   
    schema_filepath = SCHEMAS_DIR / "Agents.json"        

class AnnouncementsStream(rev_ioStream):
    """Define custom stream."""
    name = "Announcements"
    path = "/Announcements"
    primary_keys = ["announcement_id"]   
    schema_filepath = SCHEMAS_DIR / "Agents.json"        

class AuditsStream(rev_ioStream):
    """Define custom stream."""
    name = "Audits"
    path = "/Audits"
    primary_keys = ["audit_id"]     
    replication_key = "created_date"
    schema_filepath = SCHEMAS_DIR / "Audits.json"           

class BillProfilesStream(rev_ioStream):
    """Define custom stream."""
    name = "BillProfiles"
    path = "/BillProfiles"
    primary_keys = ["bill_profile_id"]     
    schema_filepath = SCHEMAS_DIR / "BillProfiles.json"           

class BillsStream(rev_ioStream):
    """Define custom stream."""
    name = "Bills"
    path = "/Bills"
    primary_keys = ["bill_id"]    
    replication_key = "created_date"     
    schema_filepath = SCHEMAS_DIR / "Bills.json"           

class ChargesStream(rev_ioStream):
    """Define custom stream."""
    name = "Charges"
    path = "/Charges"
    primary_keys = ["charge_id"]    
    replication_key = "created_date"     
    schema_filepath = SCHEMAS_DIR / "Charges.json"                  

class ContactsStream(rev_ioStream):
    """Define custom stream."""
    name = "Contacts"
    path = "/Contacts"
    primary_keys = ["contact_id"]     
    schema_filepath = SCHEMAS_DIR / "Contacts.json" 

class ContactTypesStream(rev_ioStream):
    """Define custom stream."""
    name = "ContactTypes"
    path = "/ContactTypes"
    primary_keys = ["contact_type_id"]     
    schema_filepath = SCHEMAS_DIR / "ContactTypes.json"   

class CreditsStream(rev_ioStream):
    """Define custom stream."""
    name = "Credits"
    path = "/Credits"
    primary_keys = ["credit_memo_id"]     
    replication_key = "created_date"     
    schema_filepath = SCHEMAS_DIR / "Credits.json"       

class CustomerRelationshipsStream(rev_ioStream):
    """Define custom stream."""
    name = "CustomerRelationships"
    path = "/CustomerRelationships"
    primary_keys = ["customer_relationship_id"]          
    schema_filepath = SCHEMAS_DIR / "CustomerRelationships.json"           

class CustomersStream(rev_ioStream):
    """Define custom stream."""
    name = "Customers"
    path = "/Customers"
    primary_keys = ["customer_id"]  
    replication_key = "updated_date"                 
    schema_filepath = SCHEMAS_DIR / "Customers.json"                     

class InventoryTypesStream(rev_ioStream):
    """Define custom stream."""
    name = "InventoryTypes"
    path = "/InventoryTypes"
    primary_keys = ["inventory_type_id"]                
    schema_filepath = SCHEMAS_DIR / "InventoryTypes.json"           

class NotesStream(rev_ioStream):
    """Define custom stream."""
    name = "Notes"
    path = "/Notes"
    primary_keys = ["note_id"]    
    replication_key = "created_date"                
    schema_filepath = SCHEMAS_DIR / "Notes.json"             

class NotesTypesStream(rev_ioStream):
    """Define custom stream."""
    name = "NoteTypes"
    path = "/NoteTypes"
    primary_keys = ["note_type_id"]              
    schema_filepath = SCHEMAS_DIR / "NoteTypes.json"       

class OrdersStream(rev_ioStream):
    """Define custom stream."""
    name = "Orders"
    path = "/Orders"
    primary_keys = ["order_id"]  
    replication_key = "status_date"             
    schema_filepath = SCHEMAS_DIR / "Orders.json"     

class OrderServiceProductsStream(rev_ioStream):
    """Define custom stream."""
    name = "OrderServiceProducts"
    path = "/OrderServiceProducts"
    primary_keys = ["order_id"]        
    schema_filepath = SCHEMAS_DIR / "OrderServiceProducts.json"       

class OrderServicesStream(rev_ioStream):
    """Define custom stream."""
    name = "OrderServices"
    path = "/OrderServices"
    primary_keys = ["order_id"]        
    schema_filepath = SCHEMAS_DIR / "OrderServices.json"


class PackageProductsStream(rev_ioStream):
    """Define custom stream."""
    name = "PackageProducts"
    path = "/PackageProducts"
    primary_keys = ["package_product_id"]        
    schema_filepath = SCHEMAS_DIR / "PackageProducts.json"     

class PackagesStream(rev_ioStream):
    """Define custom stream."""
    name = "PackageProducts"
    path = "/PackageProducts"
    primary_keys = ["package_id"]        
    schema_filepath = SCHEMAS_DIR / "Packages.json"     


class PaymentAccountsStream(rev_ioStream):
    """Define custom stream."""
    name = "PaymentAccounts"
    path = "/PaymentAccounts"
    primary_keys = ["package_id"]        
    schema_filepath = SCHEMAS_DIR / "PaymentAccounts.json"          

class PaymentMethodsStream(rev_ioStream):
    """Define custom stream."""
    name = "PaymentMethods"
    path = "/PaymentMethods"
    primary_keys = ["payment_method_id"]        
    schema_filepath = SCHEMAS_DIR / "PaymentMethods.json"     

class PaymentsStream(rev_ioStream):
    """Define custom stream."""
    name = "Payments"
    path = "/Payments"
    primary_keys = ["payment_id"]     
    replication_key = "created_date"              
    schema_filepath = SCHEMAS_DIR / "Payments.json"    


class ProcessesStream(rev_ioStream):
    """Define custom stream."""
    name = "Processes"
    path = "/Processes"
    primary_keys = ["process_id"]     
    replication_key = "created_date"              
    schema_filepath = SCHEMAS_DIR / "Processes.json"   

class ProcessPhasesStream(rev_ioStream):
    """Define custom stream."""
    name = "ProcessPhases"
    path = "/ProcessPhases"
    primary_keys = ["process_phase_id"]               
    schema_filepath = SCHEMAS_DIR / "ProcessPhases.json"    

class ProcessTasksStream(rev_ioStream):
    """Define custom stream."""
    name = "ProcessTasks"
    path = "/ProcessTasks"
    primary_keys = ["process_task_id"]               
    schema_filepath = SCHEMAS_DIR / "ProcessTasks.json"    

class ProductGroupsStream(rev_ioStream):
    """Define custom stream."""
    name = "ProductGroups"
    path = "/ProductGroups"
    primary_keys = ["product_group_id"]               
    schema_filepath = SCHEMAS_DIR / "ProductGroups.json"    

class ProductsStream(rev_ioStream):
    """Define custom stream."""
    name = "Products"
    path = "/Products"
    primary_keys = ["product_id"]       
    replication_key = "created_date"            
    schema_filepath = SCHEMAS_DIR / "Products.json"    

class ProductTypesStream(rev_ioStream):
    """Define custom stream."""
    name = "ProductTypes"
    path = "/ProductTypes"
    primary_keys = ["product_type_id"]               
    schema_filepath = SCHEMAS_DIR / "ProductTypes.json"    

class ProviderAccountsStream(rev_ioStream):
    """Define custom stream."""
    name = "ProviderAccounts"
    path = "/ProviderAccounts"
    primary_keys = ["provider_account_id"]               
    schema_filepath = SCHEMAS_DIR / "ProviderAccounts.json"    

class ProvidersStream(rev_ioStream):
    """Define custom stream."""
    name = "Providers"
    path = "/Providers"
    primary_keys = ["provider_id"]     
    replication_key = "created_date"                     
    schema_filepath = SCHEMAS_DIR / "Providers.json"   

class ReportCategoriesStream(rev_ioStream):
    """Define custom stream."""
    name = "ReportCategories"
    path = "/ReportCategories"
    primary_keys = ["report_category_id"]                          
    schema_filepath = SCHEMAS_DIR / "ReportCategories.json"   

class ReportsStream(rev_ioStream):
    """Define custom stream."""
    name = "Reports"
    path = "/Reports"
    primary_keys = ["report_id"]                          
    schema_filepath = SCHEMAS_DIR / "Reports.json"       

class RequestAddressesStream(rev_ioStream):
    """Define custom stream."""
    name = "RequestAddresses"
    path = "/RequestAddresses"
    primary_keys = ["request_address_id"]                          
    schema_filepath = SCHEMAS_DIR / "RequestAddresses.json"       

class RequestContactsStream(rev_ioStream):
    """Define custom stream."""
    name = "RequestContacts"
    path = "/RequestContacts"
    primary_keys = ["request_contact_id"]                          
    schema_filepath = SCHEMAS_DIR / "RequestContacts.json"       


class RequestProductsStream(rev_ioStream):
    """Define custom stream."""
    name = "RequestProducts"
    path = "/RequestProducts"
    primary_keys = ["request_product_id"]                          
    schema_filepath = SCHEMAS_DIR / "RequestProducts.json"             

class RequestsStream(rev_ioStream):
    """Define custom stream."""
    name = "Requests"
    path = "/Requests"
    primary_keys = ["request_id"]                          
    schema_filepath = SCHEMAS_DIR / "Requests.json"        

class RequestServicesStream(rev_ioStream):
    """Define custom stream."""
    name = "RequestServices"
    path = "/RequestServices"
    primary_keys = ["request_service_id"]                          
    schema_filepath = SCHEMAS_DIR / "RequestServices.json"  

class RequestStatusesStream(rev_ioStream):
    """Define custom stream."""
    name = "RequestStatuses"
    path = "/RequestStatuses"
    primary_keys = ["request_status_id"]                          
    schema_filepath = SCHEMAS_DIR / "RequestStatuses.json"      

class RequestTemplatesStream(rev_ioStream):
    """Define custom stream."""
    name = "RequestTemplates"
    path = "/RequestTemplates"
    primary_keys = ["request_template_id"]                          
    schema_filepath = SCHEMAS_DIR / "RequestTemplates.json"      

class ServiceInventoryStream(rev_ioStream):
    """Define custom stream."""
    name = "ServiceInventory"
    path = "/ServiceInventory"
    primary_keys = ["inventory_item_id"]     
    replication_key = "created_date"                        
    schema_filepath = SCHEMAS_DIR / "ServiceInventory.json"      

class ServiceProductStream(rev_ioStream):
    """Define custom stream."""
    name = "ServiceProduct"
    path = "/ServiceProduct"
    primary_keys = ["service_product_id"]     
    replication_key = "created_date"                        
    schema_filepath = SCHEMAS_DIR / "ServiceProduct.json"      


class ServicesStream(rev_ioStream):
    """Define custom stream."""
    name = "Services"
    path = "/Services"
    primary_keys = ["service_id"]     
    replication_key = "created_date"                        
    schema_filepath = SCHEMAS_DIR / "Services.json"      

class ServiceTypesStream(rev_ioStream):
    """Define custom stream."""
    name = "ServiceTypes"
    path = "/ServiceTypes"
    primary_keys = ["service_type_id"]                         
    schema_filepath = SCHEMAS_DIR / "ServiceTypes.json"      

class TasksStream(rev_ioStream):
    """Define custom stream."""
    name = "Tasks"
    path = "/Tasks"
    primary_keys = ["task_id"]                     
    replication_key = "created_date"          
    schema_filepath = SCHEMAS_DIR / "Tasks.json"          

class TaskStepsStream(rev_ioStream):
    """Define custom stream."""
    name = "TaskSteps"
    path = "/TaskSteps"
    primary_keys = ["task_step_id"]                         
    schema_filepath = SCHEMAS_DIR / "TaskSteps.json"            


class TaskTypesStream(rev_ioStream):
    """Define custom stream."""
    name = "TaskTypes"
    path = "/TaskTypes"
    primary_keys = ["task_type_id"]                         
    schema_filepath = SCHEMAS_DIR / "TaskTypes.json"         

class TicketJournalsStream(rev_ioStream):
    """Define custom stream."""
    name = "TicketJournals"
    path = "/TicketJournals"
    primary_keys = ["ticket_journal_id"]                   
    replication_key = "created_date"            
    schema_filepath = SCHEMAS_DIR / "TicketJournals.json"          

class TicketProcessesStream(rev_ioStream):
    """Define custom stream."""
    name = "TicketProcesses"
    path = "/TicketProcesses"
    primary_keys = ["ticket_process_id"]                             
    schema_filepath = SCHEMAS_DIR / "TicketProcesses.json"         

class TicketsStream(rev_ioStream):
    """Define custom stream."""
    name = "Tickets"
    path = "/Tickets"
    primary_keys = ["ticket_id"]                                      
    schema_filepath = SCHEMAS_DIR / "Tickets.json"             

class UsagePlanGroupsStream(rev_ioStream):
    """Define custom stream."""
    name = "UsagePlanGroups"
    path = "/UsagePlanGroups"
    primary_keys = ["usage_plan_group_id"]   
    replication_key = "created_date"                                     
    schema_filepath = SCHEMAS_DIR / "UsagePlanGroups.json"                        

class UserGroupsStream(rev_ioStream):
    """Define custom stream."""
    name = "UserGroups"
    path = "/UserGroups"
    primary_keys = ["user_group_id"]                                    
    schema_filepath = SCHEMAS_DIR / "UserGroups.json"         

class UsersStream(rev_ioStream):
    """Define custom stream."""
    name = "Users"
    path = "/Users"
    primary_keys = ["user_id"]                                    
    schema_filepath = SCHEMAS_DIR / "Users.json"         