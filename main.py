import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Файл для сохранения данных
DATA_FILE = "books.json"

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер прочитанных книг")
        self.books = []  # Список книг
        self.load_data()  # Загружаем данные при запуске

        # Создаём элементы интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для формы добавления книги
        form_frame = tk.LabelFrame(self.root, text="Добавить книгу")
        form_frame.pack(padx=10, pady=10, fill="x")

        # Поле "Название книги"
        tk.Label(form_frame, text="Название книги:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.title_entry = tk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        # Поле "Автор"
        tk.Label(form_frame, text="Автор:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.author_entry = tk.Entry(form_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)

        # Поле "Жанр"
        tk.Label(form_frame, text="Жанр:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.genre_entry = tk.Entry(form_frame, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=2)

        # Поле "Количество страниц"
        tk.Label(form_frame, text="Страниц:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.pages_entry = tk.Entry(form_frame, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=2)

        # Кнопка "Добавить книгу"
        self.add_btn = tk.Button(form_frame, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=5)

        # Фрейм для фильтрации
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация")
        filter_frame.pack(padx=10, pady=5, fill="x")

        # Фильтр по жанру
        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.genre_filter = tk.Entry(filter_frame, width=20)
        self.genre_filter.grid(row=0, column=1, padx=5, pady=2)

        # Фильтр по страницам
        tk.Label(filter_frame, text="Больше страниц:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.pages_filter = tk.Entry(filter_frame, width=20)
        self.pages_filter.grid(row=1, column=1, padx=5, pady=2)

        # Кнопка применения фильтров
        self.filter_btn = tk.Button(filter_frame, text="Применить фильтры", command=self.apply_filters)
        self.filter_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Таблица для отображения книг
        columns = ("Название", "Автор", "Жанр", "Страниц")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)

        # Заголовки колонок
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Полоса прокрутки для таблицы
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Обновляем отображение
        self.update_display()

    def add_book(self):
        # Получаем данные из полей
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_text = self.pages_entry.get().strip()

        # Проверка на пустые поля
        if not title or not author or not genre or not pages_text:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        # Проверка, что количество страниц — число
        try:
            pages = int(pages_text)
            if pages <= 0:
                messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        # Добавляем книгу в список
        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }
        self.books.append(book)

        # Сохраняем данные
        self.save_data()

        # Очищаем поля ввода
        self.clear_entries()

        # Обновляем отображение
        self.update_display()

        messagebox.showinfo("Успех", "Книга успешно добавлена!")

    def clear_entries(self):
        """Очищает поля ввода после добавления книги"""
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def save_data(self):
        """Сохраняет данные в JSON-файл"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_data(self):
        """Загружает данные из JSON-файла"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.books = json.load(f)

    def update_display(self):
        """Обновляет отображение таблицы"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу данными
        for book in self.books:
            self.tree.insert("", "end", values=(
                book["title"],
                book["author"],
                book["genre"],
                book["pages"]
            ))

    def apply_filters(self):
        """Применяет фильтры к отображению книг"""
        genre_filter = self.genre_filter.get().strip().lower()
        pages_filter_text = self.pages_filter.get().strip()

        filtered_books = []

        # Проверяем фильтр по страницам
        if pages_filter_text:
            try:
                min_pages = int(pages_filter_text)
                if min_pages < 0:
                    messagebox.showerror("Ошибка", "Минимальное количество страниц не может быть отрицательным!")
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное число для фильтра по страницам!")
                return
        else:
            min_pages = None

        # Применяем фильтры
        for book in self.books:
            # Проверяем совпадение по жанру (если фильтр задан)
            genre_match = not genre_filter or genre_filter in book["genre"].lower()

        pages_match = True
        if min_pages is not None:
            pages_match = book["pages"] >= min_pages

        # Если оба условия выполнены, добавляем книгу в отфильтрованный список
        if genre_match and pages_match:
            filtered_books.append(book)

        # Очищаем таблицу и заполняем отфильтрованными данными
        for item in self.tree.get_children():
            self.tree.delete(item)

        if filtered_books:
            for book in filtered_books:
                self.tree.insert("", "end", values=(
                    book["title"],
            book["author"],
            book["genre"],
            book["pages"]
        ))
        else:
            # Если ничего не найдено, показываем сообщение
            self.tree.insert("", "end", values=("По вашему запросу ничего не найдено", "", "", ""))

    def clear_filters(self):
        """Очищает поля фильтров и сбрасывает отображение"""
        self.genre_filter.delete(0, tk.END)
        self.pages_filter.delete(0, tk.END)
        self.update_display()

# Запускаем приложение
if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
