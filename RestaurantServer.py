from http.server import HTTPServer, BaseHTTPRequestHandler
from restaurantDatabase import RestaurantDatabase
import cgi

class RestaurantPortalHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        self.database = RestaurantDatabase(password='PASSWORD')
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        try:
            if self.path == '/addReservation':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                customer_id = int(form.getvalue("customer_id"))
                reservation_time = form.getvalue("reservation_time")
                number_of_guests = int(form.getvalue("number_of_guests"))
                special_requests = form.getvalue("special_requests")
                
                # Call the Database Method to add a new reservation
                self.database.addReservation(customer_id, reservation_time, number_of_guests, special_requests)
                print("Reservation added for customer ID:", customer_id)
                
                self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addReservationForm'>Add Reservation</a>|\
                                 <a href='/viewReservations'>View Reservations</a>|\
                                 <a href='/addCustomerForm'>Add Customer</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Reservation has been added</h3>")
                self.wfile.write(b"<div><a href='/addReservationForm'>Add Another Reservation</a></div>")
                self.wfile.write(b"</center></body></html>")
                return

            if self.path == '/addCustomer':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                customer_name = form.getvalue("customer_name")
                contact_info = form.getvalue("contact_info")
                
                # Call the Database Method to add a new customer
                self.database.addCustomer(customer_name, contact_info)
                print("Customer added:", customer_name)
                
                self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addReservationForm'>Add Reservation</a>|\
                                 <a href='/viewReservations'>View Reservations</a>|\
                                 <a href='/addCustomerForm'>Add Customer</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Customer has been added</h3>")
                self.wfile.write(b"<div><a href='/addCustomerForm'>Add Another Customer</a></div>")
                self.wfile.write(b"</center></body></html>")
                return

            if self.path == '/deleteReservation':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                reservation_id = int(form.getvalue("reservation_id"))
                
                # Call the Database Method to delete a reservation
                self.database.deleteReservation(reservation_id)
                print("Reservation deleted for ID:", reservation_id)
                
                self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addReservationForm'>Add Reservation</a>|\
                                 <a href='/viewReservations'>View Reservations</a>|\
                                 <a href='/addCustomerForm'>Add Customer</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Reservation has been deleted</h3>")
                self.wfile.write(b"<div><a href='/deleteReservationForm'>Delete Another Reservation</a></div>")
                self.wfile.write(b"</center></body></html>")
                return

        except Exception as e:
            self.send_error(500, 'Internal Server Error: %s' % str(e))

    def do_GET(self):
        try:
            if self.path == '/':
                data = self.database.getAllReservations()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addReservationForm'>Add Reservation</a>|\
                                  <a href='/viewReservations'>View Reservations</a>|\
                                 <a href='/deleteReservationForm'>Delete Reservations</a></div>")
                self.wfile.write(b"<hr><h2>All Reservations</h2>")
                self.wfile.write(b"<table border=2> \
                                    <tr><th> Reservation ID </th>\
                                        <th> Customer Name </th>\
                                        <th> Contact Info </th>\
                                        <th> Reservation Time </th>\
                                        <th> Number of Guests </th>\
                                        <th> Special Requests </th></tr>")
                for row in data:
                    self.wfile.write(b' <tr> <td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[2]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[4]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[5]).encode())
                    self.wfile.write(b'</td></tr>')

                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")
                return
            
            if self.path == '/addReservationForm':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>Add Reservation</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<form method='POST' action='/addReservation'>")
                self.wfile.write(b"Customer ID: <input type='text' name='customer_id'><br>")
                self.wfile.write(b"Reservation Time: <input type='text' name='reservation_time'><br>")
                self.wfile.write(b"Number of Guests: <input type='text' name='number_of_guests'><br>")
                self.wfile.write(b"Special Requests: <input type='text' name='special_requests'><br>")
                self.wfile.write(b"<input type='submit' value='Add Reservation'>")
                self.wfile.write(b"</form>")
                self.wfile.write(b"</body></html>")
                return

            if self.path == '/addCustomerForm':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>Add Customer</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<form method='POST' action='/addCustomer'>")
                self.wfile.write(b"Name: <input type='text' name='customer_name'><br>")
                self.wfile.write(b"Contact Info: <input type='text' name='contact_info'><br>")
                self.wfile.write(b"<input type='submit' value='Add Customer'>")
                self.wfile.write(b"</form>")
                self.wfile.write(b"</body></html>")
                return

            if self.path == '/deleteReservationForm':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>Delete Reservation</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<form method='POST' action='/deleteReservation'>")
                self.wfile.write(b"Reservation ID: <input type='text' name='reservation_id'><br>")
                self.wfile.write(b"<input type='submit' value='Delete Reservation'>")
                self.wfile.write(b"</form>")
                self.wfile.write(b"</body></html>")
                return

            if self.path == '/findReservations':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>Find Reservations</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<form method='POST' action='/findReservations'>")
                self.wfile.write(b"Customer ID: <input type='text' name='customer_id'><br>")
                self.wfile.write(b"<input type='submit' value='Find Reservations'>")
                self.wfile.write(b"</form>")
                self.wfile.write(b"</body></html>")
                return

            if self.path == '/viewReservations':
                reservations = self.database.getAllReservations()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>View All Reservations</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>All Reservations</h1>")
                self.wfile.write(b"<table border=2> \
                                    <tr><th> Reservation ID </th>\
                                        <th> Customer Name </th>\
                                        <th> Contact Info </th>\
                                        <th> Reservation Time </th>\
                                        <th> Number of Guests </th>\
                                        <th> Special Requests </th></tr>")
                for reservation in reservations:
                    self.wfile.write(b"<tr>")
                    for item in reservation:
                        self.wfile.write(b"<td>" + str(item).encode() + b"</td>")
                    self.wfile.write(b"</tr>")
                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

def run(server_class=HTTPServer, handler_class=RestaurantPortalHandler, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

run()
