from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableView,QHeaderView
from PyQt6.QtCore import Qt, QAbstractTableModel
import pandas as pd 

# Custom table model for 2D tabular data
class TableModel(QAbstractTableModel):
    def __init__(self, data, header_labels=None):
        super().__init__()
        self._data = data
        self._header_labels = header_labels

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        if len(self._data) > 0:
            return len(self._data[0])
        return 0

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if 0 <= section < len(self._header_labels):
                return self._header_labels[section]
        return super().headerData(section, orientation, role)
    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

# Window widget for displaying a table view
class TableViewWindow(QWidget):
    def __init__(self, data, title):
        super().__init__()

        self.setWindowTitle(title)  # Set the window title

        self.table = QTableView()  # Create a QTableView widget
        header_labels = ["Shipment ID", "Item ID", "Quantity", "Location ID"]

        # Determine if the data is a DataFrame or a list
        if isinstance(data, pd.DataFrame):
            self.model = DataFrameModel(data, header_labels)  # Create a DataFrameModel if data is a DataFrame
        else:
            self.model = TableModel(data, header_labels)  # Create a TableModel if data is a list

        self.table.setModel(self.model)  # Set the model for the table view

        # Set the stretch factor for each column to make the table stretch
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout()  # Create a vertical layout
        layout.addWidget(self.table)  # Add the table view to the layout
        self.setLayout(layout)  # Set the layout for the widget
    
    def update_data(self, data):
        # Update the model with new data
        if hasattr(self.model, 'update_data'):
            self.model.update_data(data)

# Custom model for DataFrame data
class DataFrameModel(QAbstractTableModel):
    def __init__(self, data, header_labels=None):
        super(DataFrameModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row()][index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if 0 <= section < len(self._header_labels):
                return self._header_labels[section]
        return super().headerData(section, orientation, role)
    def update_data(self, new_data):
            self.beginResetModel()
            self._data = new_data
            self.endResetModel()