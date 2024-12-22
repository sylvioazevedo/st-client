from st_client.stc import STClient

import argparse
import json

ACTION_CHOICES = ['login', 'ping', 'dbs', 'colls', 'insert', 'all', 'first', 'last', 'get', 'find', 'update', 'delete', 'count']

def save_credentials(access_token, refresh_token):
            
    print(f"Access token: {access_token}", )
    print(f"Refresh token: {refresh_token}")          
    
    # save credentials
    with open('credentials.json', 'w') as f:
        json.dump({'access_token': access_token, 'refresh_token': refresh_token}, f)
        

def main():
    
    parser = argparse.ArgumentParser(prog="stc", description='Silver Tree Command Line Interface')
    
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1-beta')
    
    parser.add_argument('-u', '--username', type=str, help='Username')
    parser.add_argument('-p', '--password', type=str, help='Password')
    parser.add_argument('-db', '--database', type=str, help='Database')
    parser.add_argument('-c', '--collection', type=str, help='Collection')
    parser.add_argument('-d', '--document', type=str, help='Document')
    parser.add_argument('-i', '--id', type=str, help='Document identification')
    parser.add_argument('-q', '--query', type=str, help='Document query')
    
    
    parser.add_argument('action', metavar='<action>', nargs="?", type=str, help=", ".join(ACTION_CHOICES), choices=ACTION_CHOICES)
    
    args = parser.parse_args()
    
    client = STClient()    
    
    if args.action == 'login':
        
        if args.username is None:
            print("Username is required.")
            exit(1)
            
        if args.password is None:
            print("Password is required.")
            exit(1)
            
        try:
            print("Logging in to st server", end="...")                        
            client.login(args.username, args.password)                    
            access_token = client.get_access_token()
            refresh_token = client.get_refresh_token()   
            
            print("OK")       
                 
            save_credentials(access_token, refresh_token)          
                
        except Exception as e:
            print(e)
            exit(1)
              
    try: 
        
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)
            client.set_access_token(credentials['access_token'])
            client.set_refresh_token(credentials['refresh_token'])
            
    except FileNotFoundError:        
        print("Credentials file not found. Please login.")
        exit(1)
            
    # check connection to server
    try:
        print("Checking connection to st server", end="...")
        client.ping()
        print("OK")
    
    except Exception as e:
        
        print(f"FAILED: {e}")
        print("Refreshing access token", end="...")
        
        try:
            client.refresh()                        
            access_token = client.get_access_token()
            refresh_token = client.get_refresh_token()   
            
            print("OK")
            
            save_credentials(access_token, refresh_token)
            
        except Exception as e:
            print(f"FAILED: {e}")
            exit(1)
        
    if args.action:
        
        if args.action == "ping":
            
            try:
                response = client.ping()
                print(f"Connection to server OK - {response}")
            
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
            
        
        if args.action == "dbs":
            
            try:
                response = client.get_databases()
                print(response)
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
                
        if args.action == "colls":
            
            if args.database is None:
                print("Database is required.")
                exit(1)
            
            try:
                response = client.get_collections(args.database)
                print(response)
                
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
                
                
        if args.action == "drop":
            
            if args.database is None:
                print("Database is required.")
                exit(1)
                
            if args.collection is None:
                print("Collection is required.")
                exit(1)
                
            try:
                response = client.drop_collection(args.database, args.collection)
                print(response)
                
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
                
        if args.action == "insert":
            
            if args.database is None:
                print("Database is required.")
                exit(1)
                
            if args.collection is None:
                print("Collection is required.")
                exit(1)
                
            if args.document is None:
                print("Document is required.")
                exit(1)
        
        
            doc = json.loads(args.document)
            
            if type(doc) is not dict:
                print("Document must be a valid JSON object.")
                exit(1)
                
            try:
                response = client.insert(args.database, args.collection, doc)
                print(response)
            
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
    
        if args.action == "all":
            
            if args.database is None:
                print("Database is required.")
                exit(1)
                
            if args.collection is None:
                print("Collection is required.")
                exit(1)
                
            try:
                response = client.find_all(args.database, args.collection)
                print(response)
            
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
                
                
        if args.action == "first":
            
            if args.database is None:
                print("Database is required.")
                exit(1)
                
            if args.collection is None:
                print("Collection is required.")
                exit(1)
                
            try:
                response = client.find_first(args.database, args.collection)
                print(response)
            
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
                
                
        if args.action == "last":
            
            if args.database is None:
                print("Database is required.")
                exit(1)
            
            if args.collection is None:
                print("Collection is required.")
                exit(1)
                
            try:
                response = client.find_last(args.database, args.collection)
                print(response)
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
                
                
        if args.action == "get":
                
            if args.database is None:
                print("Database is required.")
                exit(1)
                
            if args.collection is None:
                print("Collection is required.")
                exit(1)
                
            if args.id is None:
                print("Document id is required.")
                exit(1)
                
            try:
                response = client.find_by_id(args.database, args.collection, args.id)
                print(response)
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
                    
                    
        if args.action == "find":
            
            if args.database is None:
                print("Database is required.")
                exit(1)
                    
            if args.collection is None:
                print("Collection is required.")
                exit(1)
                    
            if args.query is None:
                print("Query is required.")
                exit(1)
                    
            try:
                response = client.find_by(args.database, args.collection, json.loads(args.query))
                print(response)
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)

        if args.action == "update":
            
            if args.database is None:
                print("Database is required.")
                exit(1)
                    
            if args.collection is None:
                print("Collection is required.")
                exit(1)
                    
            if args.id is None:
                print("Document id is required.")
                exit(1)
                    
            if args.document is None:
                print("Document is required.")
                exit(1)
                    
            try:
                response = client.update(args.database, args.collection, args.id, json.loads(args.document))
                print(response)
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
                
                
        if args.action == "delete":
            
            if args.database is None:
                print("Database is required.")
                exit(1)
                    
            if args.collection is None:
                print("Collection is required.")
                exit(1)
                    
            if args.id is None:
                print("Document id is required.")
                exit(1)
                    
            try:
                response = client.delete(args.database, args.collection, args.id)
                print(response)
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
                
                
        if args.action == "count":
            
            if args.database is None:
                print("Database is required.")
                exit(1)
                    
            if args.collection is None:
                print("Collection is required.")
                exit(1)
                    
            try:
                response = client.count(args.database, args.collection)
                print(response)
            except Exception as e:
                print(f"FAILED - {e}")
                exit(1)
    
    