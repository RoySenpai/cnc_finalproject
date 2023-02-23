import socket
import pyodbc

# DESKTOP-QH4FU0U\SQLEXPRESS - database address
# Define ip and port and database address
ip = "127.0.0.1"
port = 1234
connection = pyodbc.connect(
    'Driver={SQL Server};' 'Server=DESKTOP-QH4FU0U\SQLEXPRESS; ' 'Database=project;' 'Trusted_connection=yes;')


# Prints all the worker names in the table
def print_workers(connection):
    cursor = connection.cursor()
    print("Workers list: ")
    cursor.execute('SELECT [First Name] FROM Workers')
    for row in cursor:
        print(row)
    connection.commit()


# Prints all the worker details sorted by their last name
def print_workers_sorted(connection):
    cursor = connection.cursor()
    print("Sorted workers list: ")
    cursor.execute("SELECT CAST([First Name] as varchar(max)) as [First Name], CAST([Last name] as varchar(max)) as ["
                   "Last name], [ID], [Work ID], [Salary] FROM Workers ORDER BY [Last name]")
    for row in cursor:
        print(row)
    connection.commit()


# Adds a new worker to the table
def add_worker(connection):
    cursor = connection.cursor()
    first_Name = input("enter new worker's first name:")
    last_Name = input("enter new worker's last name:")
    id = input("enter new worker's ID:")
    w_Id = input("enter new worker's work ID:")
    salary = input("enter new worker's salary:")
    cursor.execute('insert into Workers([First Name], [Last Name], ID, [Work ID], Salary) values(?,?,?,?,?);',
                   (first_Name, last_Name, id, w_Id, salary))
    connection.commit()
    print("Worker added successfully!")


# Removes a worker from the table by work ID
def remove_worker(connection):
    cursor = connection.cursor()
    work_Id = input("enter worker's work ID:")
    cursor.execute(f"DELETE FROM Workers WHERE [Work ID] = '{work_Id}'")
    connection.commit()


# Prints a specific worker's details by his work ID
def get_worker_details(connection):
    cursor = connection.cursor()
    work_Id = input("enter worker's work ID:")
    cursor.execute('SELECT * FROM Workers WHERE [Work ID] = 'f'{work_Id}')
    for row in cursor:
        print(row)
    connection.commit()


# Prints the details for the first given amount of workers
def get_first_n_workers_details(connection):
    cursor = connection.cursor()
    num = input("enter the amount of first workers you wish to get their details: ")
    cursor.execute((f"SELECT TOP {num} * FROM Workers"))
    for row in cursor:
        print(row)
    connection.commit()


# Updates a worker's salary
def update_worker_salary(connection):
    cursor = connection.cursor()
    work_Id = input("enter worker's work ID:")
    new_Salary = input("enter the new salary:")
    query = f"UPDATE Workers SET Salary = {new_Salary} WHERE [Work ID] = '{work_Id}'"
    cursor.execute(query)
    print("Salary updated successfully!")
    connection.commit()


# Counts the amount of the workers in the table and prints the result
def count_workers(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Workers")
    count = cursor.fetchone()[0]
    print(f"There are currently {count} workers in the table.")
    connection.commit()


# Counts the amount of workers with a given salary and prints the result
def count_workers_with_given_salary(connection):
    cursor = connection.cursor()
    salary = input("Enter salary: ")
    cursor.execute("SELECT COUNT(*) FROM Workers WHERE [Salary] = ?", salary)
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"there are {count} workers with such salary")
    else:
        print("there are not workers with such salary")
    connection.commit()


# Given a name, Prints all workers with that name and their details
def check_worker_exists(connection):
    cursor = connection.cursor()
    name = input("enter the name of the worker you are looking for: ")
    cursor.execute("SELECT * FROM Workers WHERE CAST([First Name] as varchar(max)) = ?", name)
    print(f"Here is a list of workers that their name is: {name}: ")
    for row in cursor:
        print(row)
    connection.commit()


# Establish TCP connection between the client and this SQL server
def tcp_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(2)
    print("SQL Server is starting...")
    while True:
        client, address = sock.accept()
        print(f"Connected to the client - {address[0]}:{address[1]}")
        list_of_Queries = "print workers\nprint workers sorted\nadd worker\nremove worker\nget worker details\nget " \
                          "first n workers details\nupdate worker salary\ncount workers\ncount workers with given " \
                          "salary\ncheck worker exists\n "
        client.send(bytes(list_of_Queries, "utf-8"))
        while True:
            desired_Query = client.recv(1024)
            desired_Query.decode("utf-8")
            if desired_Query == b"print workers":
                print_workers(connection)
            elif desired_Query == b"print workers sorted":
                print_workers_sorted(connection)
            elif desired_Query == b"add worker":
                add_worker(connection)
            elif desired_Query == b"remove worker":
                remove_worker(connection)
            elif desired_Query == b"get worker details":
                get_worker_details(connection)
            elif desired_Query == b"get first n workers details":
                get_first_n_workers_details(connection)
            elif desired_Query == b"update worker salary":
                update_worker_salary(connection)
            elif desired_Query == b"count workers with given salary":
                count_workers_with_given_salary(connection)
            elif desired_Query == b"check worker exists":
                check_worker_exists(connection)
            elif desired_Query == b"count workers":
                count_workers(connection)
            elif desired_Query == b"nothing":
                break
            else:
                print("Query entered doesn't exist")


if __name__ == '__main__':
    tcp_connection()