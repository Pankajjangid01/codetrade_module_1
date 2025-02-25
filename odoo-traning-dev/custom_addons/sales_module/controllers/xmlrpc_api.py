import xmlrpc.client

url = 'http://localhost:8045'
db = 'demo'
uid = 2
password = 'admin'

# def xmlrpc_api():
#     info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
#     url, db, username, password = info['host'],info['database'], info['user'], info['password']
#     return f"url:{url},db:{db},username:{username},password:{password}"
# print(xmlrpc_api())

# def server_test():
#     url = 'http://localhost:8045'
#     common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
#     uid = common.authenticate('demo', 'admin', 'admin', {})
#     return uid,common.version()


def calling_method(url,db,uid,password):
    """search method to search using xmlrpc"""
    try:
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        return models.execute_kw(db, uid, password, 'company.hr', 'search', [[['name', '=', "Pankaj Kumar"]]])
    except Exception as exe:
        return f'Error in searching the record{exe}'

def serach_count_test(url,db,uid,password):
    """search count method to count total record using xmlrpc"""
    try:
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        return models.execute_kw(db,uid,password,'company.employee','search_count',[[['tech_stack','=','tester']]])
    except Exception as exe:
        return f'Error in counting the record{exe}'

def read_test(url,db,uid,password):
    """read method to access the record using xmlrpc"""
    try:
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        ids = models.execute_kw(db, uid, password, 'company.hr', 'search',[[['name', '=', "Pankaj Kumar"]]])
        [record] = models.execute_kw(db, uid, password, 'company.hr', 'read', [ids])
        return len(record)
    except Exception as exe:
        return f'Error in Reading the record{exe}'

def list_record_fields(url, db, uid, password):
    """Retrieve and display all fields of the module"""
    try:
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        fields = models.execute_kw(db, uid, password, 'company.hr', 'fields_get', [], {'attributes': ['string', 'type']})
        
        print("\nAvailable Fields in 'company.hr':")
        for field, info in fields.items():
            print(f"- {field} ({info['type']})")
        
        return fields
    except Exception as exe:
        return f'Error in listing the fields{exe}'

def create_new_hr(url, db, uid, password):
    """Create method to create a new record using XML-RPC with user input"""
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    try:
        fields = models.execute_kw(db, uid, password, 'company.hr', 'fields_get', [], {'attributes': ['string', 'type']})
        record_data = {}
        
        print("\nEnter values for the new HR record (leave blank to skip a field):")
        for field, info in fields.items():
            if field in ['hr_office']:
                hr_post_list = ['Jaipur','Mumbai','Gujrat']
                while value not in hr_post_list:
                    value = input(f"Enter value for {info['string']} ({info['type']})(Jaipur/Mumbai/Gujrat): ")
                    if value not in hr_post_list:
                        print("Enter valid input")

            if info['type'] in ['char', 'text', 'integer', 'float', 'boolean']:

                if field in  ['display_name','created_by','created_at','hr_office']:
                    continue

                value = input(f"Enter value for {info['string']} ({info['type']}): ")

                if value:
                    if info['type'] == 'integer':
                        value = int(value)
                    elif info['type'] == 'float':
                        value = float(value)
                    elif info['type'] == 'boolean':
                        value = value.lower() in ['true', '1', 'yes']
                    record_data[field] = value
        
        if not record_data:
            print("No valid data entered. Record creation aborted.")
            return False

        record_id = models.execute_kw(db, uid, password, 'company.hr', 'create', [record_data])
        print(f"Record created successfully with ID: {record_id}")
        return record_id

    except Exception as e:
        print(f"Error creating record: {e}")
        return False


def delete_hr(url, db, uid, password):
    """Ask user which record to delete and delete it"""
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    record_id = int(input("\nEnter the ID of the record you want to delete: "))
    confirm = input(f"Are you sure you want to delete record ID {record_id}? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Deletion cancelled.")
        return False

    result = models.execute_kw(db, uid, password, 'company.hr', 'unlink', [[record_id]])
    
    if result:
        print("Record deleted successfully!")
    else:
        print("Failed to delete the record.")
    
    return result


def update_record(url, db, uid, password):
    """Ask user which field to update and update it"""
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    fields = list_record_fields(url, db, uid, password)

    while True:
        record_id_input = input("\nEnter the ID of the record you want to update: ")
        if record_id_input.isdigit():
            record_id = int(record_id_input)
            break
        else:
            print("Invalid input! Please enter a valid numeric ID.")

    field_to_update = input("\nEnter the field name you want to update: ")
    if field_to_update not in fields:
        print("Invalid field name!")
        return False

    new_value = input(f"\nEnter new value for {field_to_update}: ")
    
    try:
        result = models.execute_kw(db, uid, password, 'company.hr', 'write', [[record_id], {field_to_update: new_value}])
        if result:
            print("Record updated successfully!")
        else:
            print("Failed to update the record.")
    except Exception as e:
        print(f"Error updating record: {e}")

    return result

# print(calling_method(url,db,uid,password))
# print(f"Total Testers--->>{serach_count_test(url,db,uid,password)}")
# print(read_test(url,db,uid,password))
print(f"List of fields---->>>{list_record_fields(url,db,uid,password)}")
# print(f"Created New HR----->>>>{create_new_hr(url,db,uid,password)}")
# print(f"Update the Record---->>>>>{update_record(url,db,uid,password)}")
# print(f"Deleted the record------>>>>>>{delete_hr(url,db,uid,password)}")
# print(f"\nserver authenticate test result-->{server_test()}")
