import json
import redis

def charge():

    redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)
    
    redis_client.flushall()
    
    # Load JSON data from file
    with open('book_data.json', 'r') as file:
        json_data = json.load(file)
    
    
    # Now json_data is a Python object
    print(json_data)
    
    # Import each element of the dictionary into Redis
    for key, value in json_data.items():
        # Convert value (book data) to JSON string
        value_json = json.dumps(value)
        # Store JSON string in Redis with key as 'book_data:<key>'
        redis_client.set(f'book_data:{key}', value_json)
    
    # Save indexes of books for each category
    category_indexes = {}
    for key, value in json_data.items():
        category = value["categoria"]
        if category not in category_indexes:
            category_indexes[category] = []
        category_indexes[category].append(int(key))
    
    # Store category indexes in Redis
    for category, indexes in category_indexes.items():
        # Convert indexes list to JSON string
        indexes_json = json.dumps(indexes)
        # Store JSON string in Redis with key as '{category}'
        redis_client.set(category, indexes_json)
    
charge()

# Example: Retrieving and printing indexes of books in the 'Fantasy' category
# fantasy_indexes = redis_client.get('Fantasía')
# if fantasy_indexes:
#     fantasy_indexes = json.loads(fantasy_indexes)
#     print("Indexes of books in the 'Fantasy' category:", fantasy_indexes)
# else:
#     print("No books found in the 'Fantasy' category.")    
    


# # Example: Retrieve and print book data for book with ID 1
# book_id = 1
# book_data = retrieve_book_data(book_id)
# if book_data:
#     print("Book data for book with ID", book_id, ":", book_data)
# else:
#     print("Book data not found for book with ID", book_id)    