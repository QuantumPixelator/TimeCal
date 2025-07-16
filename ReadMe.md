# TimeCal

**TimeCal** is a simple desktop application for tracking daily work hours, locations, and per diem, with reporting and calendar-based entry. It is built with Python and PySide6 (Qt for Python).

## Features

- **Calendar View:** See your entries highlighted on a monthly calendar.
- **Quick Entry:** Click any date to add, edit, or delete an entry for that day.
- **Entry Details:** Track hours worked, location, and per diem for each day.
- **Reporting:** Generate reports for any date range, with totals for hours and per diem.
- **Simple UI:** Clean, responsive interface with a native look and feel.
- **Data Storage:** All data is stored locally in a SQLite database (`caldata.db`).
- **Custom Icon:** Uses `icon.ico` if present in the app folder.

## Requirements

- Python 3.8+
- [PySide6](https://pypi.org/project/PySide6/)

## Installation

1. Clone or download this repository.
2. Install dependencies:
    ```
    pip install PySide6
    ```
3. Place your `icon.ico` in the same folder as `timecal.pyw` (optional).

## Usage

Run the application with:

```
python timecal.pyw
```

- **Add/Edit Entry:** Click a date. If an entry exists, you can edit or delete it.
- **Delete Entry:** Select a date with an entry, choose "Delete" and confirm.
- **Reporting:** Click the "Reporting" button, select a start and end date, and generate your report.

## License

MIT License

Copyright (c) 2025 David Bowlin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.