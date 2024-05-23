import mysql.connector
from mysql.connector import Error

class RestaurantDatabase:
    def __init__(self, host="127.0.0.1", port="3306", database="restaurant_reservations", user='root', password='PASSWORD'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password)
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Successfully connected to the database")
        except Error as e:
            print("Error while connecting to MySQL", e)
            self.connection = None

    def addReservation(self, customer_id, reservation_time, number_of_guests, special_requests):
        ''' Method to insert a new reservation into the reservations table '''
        if self.connection and self.connection.is_connected():
            try:
                # Check if the customer exists
                if not self.customerExists(customer_id):
                    print(f"Customer with ID {customer_id} does not exist.")
                    return
                
                query = "INSERT INTO Reservations (customerId, reservationTime, numberOfGuests, specialRequests) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(query, (customer_id, reservation_time, number_of_guests, special_requests))
                self.connection.commit()
                print("Reservation added successfully")
            except Error as e:
                print("Failed to add reservation", e)

    def getAllReservations(self):
        ''' Method to get all reservations from the reservations table '''
        if self.connection and self.connection.is_connected():
            try:
                query = """
                SELECT Reservations.reservationId, Customers.customerName, Customers.contactInfo, 
                       Reservations.reservationTime, Reservations.numberOfGuests, Reservations.specialRequests
                FROM Reservations
                JOIN Customers ON Reservations.customerId = Customers.customerId
                """
                self.cursor.execute(query)
                records = self.cursor.fetchall()
                return records
            except Error as e:
                print("Failed to fetch reservations", e)
                return []
        else:
            print("No connection to the database.")
            return []

    def addCustomer(self, customer_name, contact_info):
        ''' Method to add a new customer to the customers table '''
        if self.connection and self.connection.is_connected():
            try:
                query = "INSERT INTO Customers (customerName, contactInfo) VALUES (%s, %s)"
                self.cursor.execute(query, (customer_name, contact_info))
                self.connection.commit()
                print("Customer added successfully")
            except Error as e:
                print("Failed to add customer", e)

    def getCustomerPreferences(self, customer_id):
        ''' Method to retrieve dining preferences for a specific customer '''
        if self.connection and self.connection.is_connected():
            try:
                query = "SELECT * FROM DiningPreferences WHERE customerId = %s"
                self.cursor.execute(query, (customer_id,))
                preferences = self.cursor.fetchall()
                return preferences
            except Error as e:
                print("Failed to fetch customer preferences", e)
                return []
        else:
            print("No connection to the database.")
            return []

    def updateReservation(self, reservation_id, customer_id, reservation_time, number_of_guests, special_requests):
        ''' Method to update an existing reservation '''
        if self.connection and self.connection.is_connected():
            try:
                query = """
                UPDATE Reservations 
                SET customerId = %s, reservationTime = %s, numberOfGuests = %s, specialRequests = %s 
                WHERE reservationId = %s
                """
                self.cursor.execute(query, (customer_id, reservation_time, number_of_guests, special_requests, reservation_id))
                self.connection.commit()
                print("Reservation updated successfully")
            except Error as e:
                print("Failed to update reservation", e)

    def deleteReservation(self, reservation_id):
        ''' Method to delete a reservation '''
        if self.connection and self.connection.is_connected():
            try:
                query = "DELETE FROM Reservations WHERE reservationId = %s"
                self.cursor.execute(query, (reservation_id,))
                self.connection.commit()
                print("Reservation deleted successfully")
            except Error as e:
                print("Failed to delete reservation", e)

    def customerExists(self, customer_id):
        ''' Method to check if a customer exists '''
        if self.connection and self.connection.is_connected():
            try:
                query = "SELECT 1 FROM Customers WHERE customerId = %s"
                self.cursor.execute(query, (customer_id,))
                result = self.cursor.fetchone()
                return result is not None
            except Error as e:
                print("Failed to check if customer exists", e)
                return False

    def addSpecialRequest(self, reservation_id, special_requests):
        ''' Method to add special requests to an existing reservation '''
        if self.connection and self.connection.is_connected():
            try:
                query = "UPDATE Reservations SET specialRequests = %s WHERE reservationId = %s"
                self.cursor.execute(query, (special_requests, reservation_id))
                self.connection.commit()
                print("Special requests updated successfully")
            except Error as e:
                print("Failed to update special requests", e)

    def findReservations(self, customer_id):
        ''' Method to find reservations for a specific customer '''
        if self.connection and self.connection.is_connected():
            try:
                query = "SELECT * FROM Reservations WHERE customerId = %s"
                self.cursor.execute(query, (customer_id,))
                reservations = self.cursor.fetchall()
                return reservations
            except Error as e:
                print("Failed to find reservations", e)
                return []
        else:
            print("No connection to the database.")
            return []

    def searchPreferences(self, customer_id):
        ''' Method to search dining preferences for a specific customer '''
        if self.connection and self.connection.is_connected():
            try:
                query = "SELECT * FROM DiningPreferences WHERE customerId = %s"
                self.cursor.execute(query, (customer_id,))
                preferences = self.cursor.fetchall()
                return preferences
            except Error as e:
                print("Failed to search dining preferences", e)
                return []
        else:
            print("No connection to the database.")
            return []

    def closeConnection(self):
        ''' Method to close the database connection '''
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed")

def main():
    db = RestaurantDatabase(password='PASSWORD')

    if db.connection and db.connection.is_connected():
        while True:
            print("\nRestaurant Reservation System")
            print("1. Add Customer")
            print("2. Add Reservation")
            print("3. View Reservations")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                customer_name = input("Enter customer name: ")
                contact_info = input("Enter contact info: ")
                db.addCustomer(customer_name, contact_info)

            elif choice == '2':
                customer_id = int(input("Enter customer ID: "))
                reservation_time = input("Enter reservation time (YYYY-MM-DD HH:MM:SS): ")
                number_of_guests = int(input("Enter number of guests: "))
                special_requests = input("Enter special requests: ")
                db.addReservation(customer_id, reservation_time, number_of_guests, special_requests)

            elif choice == '3':
                reservations = db.getAllReservations()
                for reservation in reservations:
                    print(reservation)

            elif choice == '4':
                db.closeConnection()
                break

            else:
                print("Invalid choice. Please try again.")
    else:
        print("Failed to connect to the database. Exiting.")

if __name__ == "__main__":
    main()
