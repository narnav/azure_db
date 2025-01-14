from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 
import pyodbc

app = Flask(__name__)

# Define connection string
# Update the values with your server, database, username, and password
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc:///?odbc_connect='
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=tcp:dbsamp.database.windows.net,1433;'
    'DATABASE=waga;'
    'UID=waga;'
    'PWD=Itay!123;'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# SQLAlchemy model corresponding to the 'Persons' table
class Person(db.Model):
    __tablename__ = 'Persons'  # Name of the table in the database

    PersonID = db.Column(db.Integer, primary_key=True, nullable=True)
    LastName = db.Column(db.String(255), nullable=True)
    FirstName = db.Column(db.String(255), nullable=True)
    Address = db.Column(db.String(255), nullable=True)
    City = db.Column(db.String(255), nullable=True)

    def __init__(self, PersonID, LastName, FirstName, Address, City):
        self.PersonID = PersonID
        self.LastName = LastName
        self.FirstName = FirstName
        self.Address = Address
        self.City = City

    def __repr__(self):
        return f'<Person {self.FirstName} {self.LastName}>'

@app.route('/')
def index():
    return 'Hello, World!'

# Example route to fetch all persons from the table
@app.route('/persons')
def get_persons():
    try:
        persons = Person.query.all()  # Query all rows from the Persons table
        data = []
        for person in persons:
            data.append({
                'PersonID': person.PersonID,
                'LastName': person.LastName,
                'FirstName': person.FirstName,
                'Address': person.Address,
                'City': person.City
            })
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)