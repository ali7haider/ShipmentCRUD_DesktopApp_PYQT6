import sqlite3
import csv
from shipment import Shipment  # Assuming Shipment class is defined in shipment.py

class ShipmentDB:
    def __init__(self, db_file):
        # Initialize the database connection and cursor
        self.conn = sqlite3.connect(db_file)  # Connect to the SQLite database
        self.cursor = self.conn.cursor()  # Create a cursor object to execute SQL commands

    def create_table(self):
        # Drop the table if it exists and create a new Shipment table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Shipment (
                            ShipmentID Integer PRIMARY KEY,
                            ItemID Integer,
                            Quantity Integer,
                            LocationID Integer
                        )''')
        self.conn.commit()  # Commit the transaction to save changes to the database

    def insert_shipment(self, shipment):
        # Insert a Shipment object into the Shipment table
        self.cursor.execute('''INSERT INTO Shipment VALUES (?, ?, ?, ?)''', 
                            (shipment.ShipmentID, shipment.ItemID, shipment.Quantity, shipment.LocationID))
        self.conn.commit()  # Commit the transaction to save changes to the database
    def update_shipment(self, shipment):
        # Execute the SQL query to update the shipment in the Shipment table
        self.cursor.execute("""
                            UPDATE Shipment
                            SET ItemID = ?,
                                Quantity = ?,
                                LocationID = ?
                            WHERE ShipmentID = ?
                            """,
                            (shipment.ItemID, shipment.Quantity, shipment.LocationID, shipment.ShipmentID))
        
        # Commit the transaction to save changes to the database
        self.conn.commit()
    def delete_shipment(self, shipment_id):
        # Execute the SQL query to delete the shipment from the Shipment table
        self.cursor.execute("""
                            DELETE FROM Shipment
                            WHERE ShipmentID = ?
                            """,
                            (shipment_id,))
        
        # Commit the transaction to save changes to the database
        self.conn.commit()


    def fetch_all_shipment(self):
        # Fetch all Shipment records from the Shipment table
        self.cursor.execute('''SELECT * FROM Shipment''')
        return self.cursor.fetchall()  # Return all fetched records

    def close_connection(self):
        # Close the database connection
        self.conn.close()

