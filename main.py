import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout,QLineEdit,QMessageBox
from PyQt6.QtCore import Qt
from modelview import TableViewWindow
from shipment_db import ShipmentDB
from shipment import Shipment

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shipment")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.table_window = None  # Initialize table_window as an instance variable

        # Set spacing to 0 for the main layout
        self.layout.setSpacing(0)

        # Create a vertical layout for the information frame
        info_layout = QHBoxLayout()
        info_frame = QWidget()
        info_frame.setLayout(info_layout)

        # Set spacing to 0 for the info_layout
        info_layout.setSpacing(0)

        # Create a vertical layout for the frames within info_frame
        info_vlayout = QVBoxLayout()

        # Create and customize the frames for each vertical layout
        info_frame1 = QWidget()
        label1 = QLabel("Shipment ID:")
        self.line_edit1 = QLineEdit()  # Make line edit an instance variable
        info_frame1_layout = QHBoxLayout()
        info_frame1_layout.addWidget(label1)
        info_frame1_layout.addWidget(self.line_edit1)
        info_frame1.setLayout(info_frame1_layout)

        info_frame2 = QWidget()
        label2 = QLabel("Item ID:        ")
        self.line_edit2 = QLineEdit()  # Make line edit an instance variable
        info_frame2_layout = QHBoxLayout()
        info_frame2_layout.addWidget(label2)
        info_frame2_layout.addWidget(self.line_edit2)
        info_frame2.setLayout(info_frame2_layout)

        info_frame3 = QWidget()
        label3 = QLabel("Quantity:      ")
        self.line_edit3 = QLineEdit()  # Make line edit an instance variable
        info_frame3_layout = QHBoxLayout()
        info_frame3_layout.addWidget(label3)
        info_frame3_layout.addWidget(self.line_edit3)
        info_frame3.setLayout(info_frame3_layout)

        info_frame4 = QWidget()
        label4 = QLabel("Location ID:  ")
        self.line_edit4 = QLineEdit()  # Make line edit an instance variable
        info_frame4_layout = QHBoxLayout()
        info_frame4_layout.addWidget(label4)
        info_frame4_layout.addWidget(self.line_edit4)
        info_frame4.setLayout(info_frame4_layout)
        
        # Add frames to the vertical layout
        info_vlayout.addWidget(info_frame1)
        info_vlayout.addWidget(info_frame2)
        info_vlayout.addWidget(info_frame3)
        info_vlayout.addWidget(info_frame4)

        # Add the vertical layout to the horizontal layout
        info_layout.addLayout(info_vlayout)
        
        # Create and customize the push buttons for info_frame
        self.btnAdd = QPushButton("Add Shipment")
        self.btnEdit = QPushButton("Edit Shipment")
        self.btnDelete = QPushButton("Delete Shipment")
        self.btnExit = QPushButton("Exit")
        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(10, 3, 0, 0)  # Set margins to zero
        buttons_layout.setSpacing(10)  # Set spacing to 10 pixels
        buttons_layout.addWidget(self.btnAdd)
        buttons_layout.addWidget(self.btnEdit)
        buttons_layout.addWidget(self.btnDelete)
        buttons_layout.addWidget(self.btnExit)

        # Create and customize the second widget for info_frame
        buttons_widget = QWidget()
        info_layout.addWidget(buttons_widget)
        buttons_widget.setLayout(buttons_layout)

        # Add info_frame to the main layout
        self.layout.addWidget(info_frame)

        # Initialize Shipment
        self.init_shipment()

        self.setFixedWidth(500)
        self.setFixedHeight(400)


        self.btnEdit.setEnabled(False)
        self.btnDelete.setEnabled(False)
        # Connect button click signals to slots
        self.btnAdd.clicked.connect(self.add_shipment)
        self.btnEdit.clicked.connect(self.edit_shipment)
        self.btnDelete.clicked.connect(self.delete_shipment)


        self.btnExit.clicked.connect(self.close)

    def init_shipment(self):
        # Create a shipment database instance
        self.shipment_db = ShipmentDB("shipments.db")
        self.shipment_db.create_table()

        # Fetch all shipment data from the database
        shipment_data = self.shipment_db.fetch_all_shipment()

        # Create TableView
        self.table_view = TableViewWindow(shipment_data, "Shipment Data")
        # Connect selectionChanged signal to slot method
        self.table_view.table.selectionModel().selectionChanged.connect(self.load_selected_row_data)


        # Add TableView to display_layout
        display_layout = QWidget()  # Define display_layout here
        display_layout_layout = QVBoxLayout(display_layout)
        display_layout_layout.addWidget(self.table_view)

        # Customize display_layout (if needed)
        self.layout.addWidget(display_layout)


    def load_selected_row_data(self, selected, deselected):
        # Get the selected indexes

        indexes = selected.indexes()
        if indexes:
            # Get the data from the selected row
            row = indexes[0].row()
            data = [self.table_view.model.data(self.table_view.model.index(row, col), Qt.ItemDataRole.DisplayRole) for col in range(4)]

            # Update line edits with selected data
            self.line_edit1.setText(str(data[0]))
            self.line_edit2.setText(str(data[1]))
            self.line_edit3.setText(str(data[2]))
            self.line_edit4.setText(str(data[3]))
            self.btnEdit.setEnabled(True)
            self.btnDelete.setEnabled(True)
            self.line_edit1.setEnabled(False)




    def show_message_box(self, title, message, error_message=None, icon=QMessageBox.Icon.Information):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        if error_message:
            msg_box.setInformativeText(error_message)
        msg_box.exec()
    def clear_line_edits(self):
        self.line_edit1.setEnabled(True)
        self.line_edit1.clear()
        self.line_edit2.clear()
        self.line_edit3.clear()
        self.line_edit4.clear()
    def add_shipment(self):
        # Get data from line edits
        shipment_id = self.line_edit1.text().strip()
        item_id = self.line_edit2.text().strip()
        quantity = self.line_edit3.text().strip()
        location_id = self.line_edit4.text().strip()

        # Validate inputs
        if not all([shipment_id, item_id, quantity, location_id]):
            self.show_message_box("Error", "Please fill in all fields.", icon=QMessageBox.Icon.Critical)
            return

        try:
            # Convert to integers and perform additional validation
            shipment_id = int(shipment_id)
            item_id = int(item_id)
            quantity = int(quantity)
            location_id = int(location_id)

            # Check if IDs are positive integers
            if shipment_id <= 0 or item_id <= 0 or location_id <= 0:
                self.show_message_box("Error", "Shipment ID, Item ID, and Location ID must be positive integers.", icon=QMessageBox.Icon.Critical)
                return

            # Check if quantity is non-negative
            if quantity < 0:
                self.show_message_box("Error", "Quantity cannot be negative.", icon=QMessageBox.Icon.Critical)
                return
        except ValueError:
            # Error occurred during conversion to integers
            self.show_message_box("Error", "Invalid input format. Please enter positive integers for IDs and non-negative integer for quantity.", icon=QMessageBox.Icon.Critical)
            return

        # Create a Shipment object
        shipment = Shipment(shipment_id, item_id, quantity, location_id)

        # Insert data into the database
        self.shipment_db.insert_shipment(shipment)

        # Update TableView
        shipment_data = self.shipment_db.fetch_all_shipment()
        self.table_view.update_data(shipment_data)

        # Clear line edits
        self.clear_line_edits()

    def edit_shipment(self):
        # Get data from line edits
        shipment_id = self.line_edit1.text().strip()
        item_id = self.line_edit2.text().strip()
        quantity = self.line_edit3.text().strip()
        location_id = self.line_edit4.text().strip()

        # Validate inputs
        if not all([shipment_id, item_id, quantity, location_id]):
            self.show_message_box("Error", "Please fill in all fields.", icon=QMessageBox.Icon.Warning)
            return

        try:
            # Convert to integers and perform additional validation
            shipment_id = int(shipment_id)
            item_id = int(item_id)
            quantity = int(quantity)
            location_id = int(location_id)

            # Check if IDs are positive integers
            if shipment_id <= 0 or item_id <= 0 or location_id <= 0:
                self.show_message_box("Error", "Shipment ID, Item ID, and Location ID must be positive integers.", icon=QMessageBox.Icon.Warning)
                return

            # Check if quantity is non-negative
            if quantity < 0:
                self.show_message_box("Error", "Quantity cannot be negative.", icon=QMessageBox.Icon.Warning)
                return
        except ValueError:
            # Error occurred during conversion to integers
            self.show_message_box("Error", "Invalid input format. Please enter positive integers for IDs and non-negative integer for quantity.", icon=QMessageBox.Icon.Warning)
            return

        # Create a Shipment object
        shipment = Shipment(shipment_id, item_id, quantity, location_id)

        # Update data in the database
        self.shipment_db.update_shipment(shipment)

        # Update TableView
        shipment_data = self.shipment_db.fetch_all_shipment()
        self.table_view.update_data(shipment_data)

        # Clear line edits
        self.clear_line_edits()
        self.btnEdit.setEnabled(False)
        self.btnDelete.setEnabled(False)

        self.btnDelete.setEnabled(False)



    def delete_shipment(self):
        # Get the shipment ID from the line edit
        shipment_id = self.line_edit1.text().strip()
        shipment_id=int(shipment_id)

        # Validate the shipment ID
        if not shipment_id:
            self.show_message_box("Error", "Please enter a Shipment ID to delete.", QMessageBox.Icon.Critical)
            return

        # Ask for confirmation before deleting
        confirm = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete Shipment ID: {shipment_id}?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            # Delete the shipment from the database
            self.shipment_db.delete_shipment(shipment_id)

            # Update TableView
            shipment_data = self.shipment_db.fetch_all_shipment()
            self.table_view.update_data(shipment_data)

            # Clear line edits
            self.clear_line_edits()
            # Disable Edit and Delete buttons after deletion
            self.btnEdit.setEnabled(False)
            self.btnDelete.setEnabled(False)


if __name__ == "__main__":
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create MainWindow and show
    window = MainWindow()
    window.show()
    
    # Exit application on window close
    sys.exit(app.exec())

