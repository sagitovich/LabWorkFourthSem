import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                             QPushButton, QDialog, QVBoxLayout, QLineEdit, QLabel)


class FilmApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Фильмы")
        self.setGeometry(550, 250, 800, 500)

        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(0, 0, 800, 400)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Название", "Год выпуска", "Длительность", "Жанр"])

        self.load_data()

        add_button = QPushButton("Добавить", self)
        add_button.setGeometry(20, 440, 100, 30)
        add_button.clicked.connect(self.add_film)

        delete_button = QPushButton("Удалить", self)
        delete_button.setGeometry(140, 440, 100, 30)
        delete_button.clicked.connect(self.delete_film)

        self.table_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

    def load_data(self):
        connection = sqlite3.connect("films_db.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT f.title, f.year, f.duration, g.title AS genre "
                       "FROM films f JOIN genres g ON f.genre = g.id")
        films = cursor.fetchall()
        connection.close()

        self.table_widget.setRowCount(len(films))
        for row, film in enumerate(films):
            for col, value in enumerate(film):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(value)))

    def save_film(self, name, year, duration, genre, rowid=None):
        connection = sqlite3.connect("films_db.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM genres WHERE title = ?", (genre,))
        genre_id = cursor.fetchone()

        if not genre_id:
            cursor.execute("INSERT INTO genres (title) VALUES (?)", (genre,))
            connection.commit()
            cursor.execute("SELECT id FROM genres WHERE title = ?", (genre,))
            genre_id = cursor.fetchone()

        genre_id = genre_id[0]

        if rowid is None:
            cursor.execute("INSERT INTO films (title, year, duration, genre) VALUES (?, ?, ?, ?)",
                           (name, year, duration, genre_id))
        else:
            cursor.execute("UPDATE films SET title = ?, year = ?, duration = ?, genre = ? WHERE rowid = ?",
                           (name, year, duration, genre_id, rowid))
        connection.commit()
        connection.close()
        self.load_data()

    def add_film(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить фильм")
        layout = QVBoxLayout()

        name_label = QLabel("Название:")
        name_input = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(name_input)

        year_label = QLabel("Год выпуска:")
        year_input = QLineEdit()
        layout.addWidget(year_label)
        layout.addWidget(year_input)

        duration_label = QLabel("Длительность:")
        duration_input = QLineEdit()
        layout.addWidget(duration_label)
        layout.addWidget(duration_input)

        genre_label = QLabel("Жанр:")
        genre_input = QLineEdit()
        layout.addWidget(genre_label)
        layout.addWidget(genre_input)

        save_button = QPushButton("Сохранить", dialog)
        save_button.clicked.connect(lambda: self.save_film(name_input.text(), year_input.text(),
                                                           duration_input.text(), genre_input.text()))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def delete_film(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            connection = sqlite3.connect("films_db.sqlite")
            cursor = connection.cursor()
            cursor.execute("SELECT rowid FROM films LIMIT 1 OFFSET ?", (selected_row,))
            rowid = cursor.fetchone()[0]
            cursor.execute("DELETE FROM films WHERE rowid = ?", (rowid,))
            connection.commit()
            connection.close()
            self.load_data()

    def on_item_double_clicked(self, item):
        row = item.row()
        film_data = [self.table_widget.item(row, col).text() for col in range(4)]
        connection = sqlite3.connect("films_db.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT rowid FROM films LIMIT 1 OFFSET ?", (row,))
        rowid = cursor.fetchone()[0]
        connection.close()

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Film")
        layout = QVBoxLayout()

        name_label = QLabel("Название:")
        name_input = QLineEdit(film_data[0])
        layout.addWidget(name_label)
        layout.addWidget(name_input)

        year_label = QLabel("Год выпуска:")
        year_input = QLineEdit(film_data[1])
        layout.addWidget(year_label)
        layout.addWidget(year_input)

        duration_label = QLabel("Длительность:")
        duration_input = QLineEdit(film_data[2])
        layout.addWidget(duration_label)
        layout.addWidget(duration_input)

        genre_label = QLabel("Жанр:")
        genre_input = QLineEdit(film_data[3])
        layout.addWidget(genre_label)
        layout.addWidget(genre_input)

        save_button = QPushButton("Save", dialog)
        save_button.clicked.connect(
            lambda: self.save_film(name_input.text(), year_input.text(), duration_input.text(), genre_input.text(),
                                   rowid))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FilmApp()
    window.show()
    sys.exit(app.exec_())
