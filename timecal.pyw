import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QCalendarWidget, QPushButton, QDialog, QFormLayout, QLineEdit,
    QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QDateEdit
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QTextCharFormat, QIcon
from PySide6.QtCore import Qt

DB_FILE = "caldata.db"

def init_db():
    """Initialize the SQLite database and create the entries table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            date TEXT PRIMARY KEY,
            hours REAL,
            location TEXT,
            per_diem REAL
        )
    """)
    conn.commit()
    conn.close()

class EntryDialog(QDialog):
    """Dialog for entering or editing a time entry."""
    def __init__(self, date, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle(f"Entry for {date.toString('MM/dd/yyyy')}")
        self.date = date
        self.data = data or {}
        layout = QFormLayout(self)

        self.hours_edit = QLineEdit(str(self.data.get("hours", "")))
        self.location_edit = QLineEdit(self.data.get("location", ""))
        self.per_diem_edit = QLineEdit(str(self.data.get("per_diem", "")))

        layout.addRow("Hours Worked:", self.hours_edit)
        layout.addRow("Location:", self.location_edit)
        layout.addRow("Per Diem:", self.per_diem_edit)

        btns = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(save_btn)
        btns.addWidget(cancel_btn)
        layout.addRow(btns)

    def get_data(self):
        """Return the entry data as a dictionary."""
        try:
            hours = float(self.hours_edit.text())
        except ValueError:
            hours = 0.0
        try:
            per_diem = float(self.per_diem_edit.text())
        except ValueError:
            per_diem = 0.0
        return {
            "date": self.date.toString("MM/dd/yyyy"),
            "hours": hours,
            "location": self.location_edit.text(),
            "per_diem": per_diem
        }

class ReportDialog(QDialog):
    """Dialog for generating and displaying reports."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Report")
        self.resize(325, 425)
        layout = QVBoxLayout(self)

        date_layout = QHBoxLayout()

        self.start_date = QDate.currentDate()
        self.end_date = QDate.currentDate()

        self.start_btn = QPushButton(f"Start Date: {self.start_date.toString('MM/dd/yyyy')}")
        self.end_btn = QPushButton(f"End Date: {self.end_date.toString('MM/dd/yyyy')}")
        self.start_btn.clicked.connect(self.select_start_date)
        self.end_btn.clicked.connect(self.select_end_date)

        date_layout.addWidget(self.start_btn)
        date_layout.addWidget(self.end_btn)
        layout.addLayout(date_layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        btn = QPushButton("Generate Report")
        btn.clicked.connect(self.generate_report)
        layout.addWidget(btn)

    def select_start_date(self):
        """Show a calendar dialog to select the start date."""
        dlg = QCalendarWidget()
        dlg.setSelectedDate(self.start_date)
        dlg.setWindowTitle("Select Start Date")
        dlg.setGridVisible(True)
        dlg.setMinimumDate(QDate(1900, 1, 1))
        dlg.setMaximumDate(QDate(2999, 12, 31))
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.resize(300, 200)
        temp_dialog = QDialog(self)
        temp_layout = QVBoxLayout(temp_dialog)
        temp_layout.addWidget(dlg)
        ok_btn = QPushButton("OK")
        temp_layout.addWidget(ok_btn)
        ok_btn.clicked.connect(temp_dialog.accept)
        if temp_dialog.exec():
            self.start_date = dlg.selectedDate()
            self.start_btn.setText(f"Start Date: {self.start_date.toString('MM/dd/yyyy')}")

    def select_end_date(self):
        """Show a calendar dialog to select the end date."""
        dlg = QCalendarWidget()
        dlg.setSelectedDate(self.end_date)
        dlg.setWindowTitle("Select End Date")
        dlg.setGridVisible(True)
        dlg.setMinimumDate(QDate(1900, 1, 1))
        dlg.setMaximumDate(QDate(2999, 12, 31))
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.resize(300, 200)
        temp_dialog = QDialog(self)
        temp_layout = QVBoxLayout(temp_dialog)
        temp_layout.addWidget(dlg)
        ok_btn = QPushButton("OK")
        temp_layout.addWidget(ok_btn)
        ok_btn.clicked.connect(temp_dialog.accept)
        if temp_dialog.exec():
            self.end_date = dlg.selectedDate()
            self.end_btn.setText(f"End Date: {self.end_date.toString('MM/dd/yyyy')}")

    def generate_report(self):
        """Generate and display the report for the selected date range."""
        start = self.start_date.toString("MM/dd/yyyy")
        end = self.end_date.toString("MM/dd/yyyy")
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            SELECT date, hours, location, per_diem FROM entries
            WHERE date BETWEEN ? AND ?
            ORDER BY date
        """, (start, end))
        rows = c.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Hours", "Location", "Per Diem"])
        total_hours = 0
        total_per_diem = 0
        for i, (date, hours, location, per_diem) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(date))
            self.table.setItem(i, 1, QTableWidgetItem(str(hours)))
            self.table.setItem(i, 2, QTableWidgetItem(location))
            self.table.setItem(i, 3, QTableWidgetItem(str(per_diem)))
            total_hours += hours
            total_per_diem += per_diem
        self.table.resizeColumnsToContents()
        QMessageBox.information(self, "Totals",
            f"Total Hours: {total_hours}\nTotal Per Diem: {total_per_diem}")

class MainWindow(QMainWindow):
    """Main application window for the time calendar."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Calendar v1.5")
        self.resize(600, 400)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        layout.addWidget(self.calendar)

        # Select the first day of the current month on startup
        today = QDate.currentDate()
        first_of_month = QDate(today.year(), today.month(), 1)
        self.calendar.setSelectedDate(first_of_month)

        btn_layout = QHBoxLayout()
        self.report_btn = QPushButton("Reporting")
        self.report_btn.clicked.connect(self.show_report)
        btn_layout.addWidget(self.report_btn)
        layout.addLayout(btn_layout)

        self.calendar.selectionChanged.connect(self.on_date_selected)
        self.highlight_dates()

        self.last_selected_date = None

    def delete_entry(self, date):
        """Delete an entry for the given date."""
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM entries WHERE date=?", (date.toString("MM/dd/yyyy"),))
        conn.commit()
        conn.close()

    def highlight_dates(self):
        """Highlight all dates in the calendar that have entries.
        Note: highlights for deleted entries will persist until restart.
        """
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT date FROM entries")
        current_dates = c.fetchall()
        conn.close()

        fmt = QTextCharFormat()
        fmt.setBackground(Qt.cyan)
        
        for (date_str,) in current_dates:
            qdate = QDate.fromString(date_str, "MM/dd/yyyy")
            if qdate.isValid():
                self.calendar.setDateTextFormat(qdate, fmt)

    def on_date_selected(self):
        """Handle logic when a date is selected in the calendar."""
        date = self.calendar.selectedDate()
        if self.last_selected_date == date:
            return
        self.last_selected_date = date

        entry = self.get_entry(date)
        if entry:
            summary = (
                f"Entry for {date.toString('MM/dd/yyyy')} found.\n\n"
                f"Hours: {entry['hours']}\n"
                f"Location: {entry['location']}\n"
                f"Per Diem: {entry['per_diem']}\n\n"
                "What would you like to do?"
            )
            menu = QMessageBox(self)
            menu.setWindowTitle("Entry Options")
            menu.setText(summary)
            edit_btn = menu.addButton("Edit", QMessageBox.AcceptRole)
            delete_btn = menu.addButton("Delete", QMessageBox.DestructiveRole)
            cancel_btn = menu.addButton("Cancel", QMessageBox.RejectRole)
            menu.exec()
            if menu.clickedButton() == edit_btn:
                dlg = EntryDialog(date, self, entry)
                if dlg.exec():
                    data = dlg.get_data()
                    self.save_entry(data)
                    self.highlight_dates()
            elif menu.clickedButton() == delete_btn:
                confirm = QMessageBox.question(self, "Confirm Delete",
                    f"Delete entry for {date.toString('MM/dd/yyyy')}?",
                    QMessageBox.Yes | QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    self.delete_entry(date)
                    self.highlight_dates()
            today = QDate.currentDate()
            first_of_month = QDate(today.year(), today.month(), 1)
            self.calendar.blockSignals(True)
            self.calendar.setSelectedDate(first_of_month)
            self.calendar.blockSignals(False)
            self.last_selected_date = None
        else:
            dlg = EntryDialog(date, self, entry)
            if dlg.exec():
                data = dlg.get_data()
                self.save_entry(data)
                self.highlight_dates()
            today = QDate.currentDate()
            first_of_month = QDate(today.year(), today.month(), 1)
            self.calendar.blockSignals(True)
            self.calendar.setSelectedDate(first_of_month)
            self.calendar.blockSignals(False)
            self.last_selected_date = None

    def get_entry(self, date):
        """Retrieve an entry for the given date."""
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT hours, location, per_diem FROM entries WHERE date=?", (date.toString("MM/dd/yyyy"),))
        row = c.fetchone()
        conn.close()
        if row:
            return {"hours": row[0], "location": row[1], "per_diem": row[2]}
        return {}

    def save_entry(self, data):
        """Save or update an entry in the database."""
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            INSERT INTO entries (date, hours, location, per_diem)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                hours=excluded.hours,
                location=excluded.location,
                per_diem=excluded.per_diem
        """, (data["date"], data["hours"], data["location"], data["per_diem"]))
        conn.commit()
        conn.close()

    def show_report(self):
        """Show the report dialog."""
        dlg = ReportDialog(self)
        dlg.exec()

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())