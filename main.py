import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

TASKS_FILE = "tasks_history.json"

default_tasks = [
    {"name": "Прочитать статью", "category": "учёба"}
]

history = []

def load_history():
    global history
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []

def save_history():
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_to_history(task_name, category):
    history.append({"name": task_name, "category": category, "timestamp": str(len(history)+1)})
    save_history()
    update_history_list()

def generate_task():
    selected_category = category_filter.get()
    if selected_category == "Все":
        available_tasks = all_tasks
    else:
        available_tasks = [t for t in all_tasks if t["category"] == selected_category]
    
    if not available_tasks:
        messagebox.showwarning("Нет задач", f"Нет задач в категории '{selected_category}'")
        return
    
    task = random.choice(available_tasks)
    task_name_var.set(task["name"])
    add_to_history(task["name"], task["category"])

def add_new_task():
    new_task = new_task_entry.get().strip()
    category = new_category_var.get()
    
    if not new_task:
        messagebox.showerror("Ошибка", "Задача не может быть пустой!")
        return
    
    all_tasks.append({"name": new_task, "category": category})
    update_category_filter()
    new_task_entry.delete(0, tk.END)
    messagebox.showinfo("Успех", f"Задача '{new_task}' добавлена в категорию '{category}'")

def update_history_list():
    history_listbox.delete(0, tk.END)
    filter_cat = category_filter.get()
    
    for item in history:
        if filter_cat == "Все" or item["category"] == filter_cat:
            display_text = f"{item['timestamp']}. {item['name']} [{item['category']}]"
            history_listbox.insert(tk.END, display_text)

def update_category_filter():
    categories = list(set([t["category"] for t in all_tasks]))
    categories.insert(0, "Все")
    category_filter['values'] = categories
    if category_filter.get() not in categories:
        category_filter.set("Все")

def clear_history():
    if messagebox.askyesno("Очистка", "Очистить всю историю?"):
        global history
        history = []
        save_history()
        update_history_list()

root = tk.Tk()
root.title("Random Task Generator - Александрюк Василий Михайлович")
root.geometry("600x500")

all_tasks = default_tasks.copy()
load_history()

task_name_var = tk.StringVar()
new_category_var = tk.StringVar(value="учёба")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(main_frame, text="Генератор случайных задач", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

ttk.Label(main_frame, text="Фильтр по категории:").grid(row=1, column=0, sticky=tk.W)
category_filter = ttk.Combobox(main_frame, values=["Все", "учёба", "спорт", "работа"], state="readonly")
category_filter.set("Все")
category_filter.grid(row=1, column=1, sticky=tk.W)
category_filter.bind('<<ComboboxSelected>>', lambda e: update_history_list())

ttk.Button(main_frame, text="Сгенерировать задачу", command=generate_task).grid(row=2, column=0, columnspan=2, pady=10)

ttk.Label(main_frame, text="Текущая задача:", font=("Arial", 12)).grid(row=3, column=0, sticky=tk.W)
ttk.Entry(main_frame, textvariable=task_name_var, width=40, state='readonly').grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E))

ttk.Label(main_frame, text="История задач:", font=("Arial", 12)).grid(row=4, column=0, sticky=tk.W, pady=(10,0))
history_listbox = tk.Listbox(main_frame, height=12, width=60)
history_listbox.grid(row=5, column=0, columnspan=3, pady=5, sticky=(tk.W, tk.E))

scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=history_listbox.yview)
scrollbar.grid(row=5, column=3, sticky=(tk.N, tk.S))
history_listbox.configure(yscrollcommand=scrollbar.set)

ttk.Button(main_frame, text="Очистить историю", command=clear_history).grid(row=6, column=0, pady=5)

ttk.Separator(main_frame, orient='horizontal').grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

ttk.Label(main_frame, text="Добавить новую задачу:", font=("Arial", 10)).grid(row=8, column=0, columnspan=3)
ttk.Label(main_frame, text="Задача:").grid(row=9, column=0, sticky=tk.W)
new_task_entry = ttk.Entry(main_frame, width=30)
new_task_entry.grid(row=9, column=1, sticky=tk.W)

ttk.Label(main_frame, text="Категория:").grid(row=10, column=0, sticky=tk.W)
category_combo = ttk.Combobox(main_frame, values=["учёба", "спорт", "работа"], textvariable=new_category_var, state="readonly")
category_combo.grid(row=10, column=1, sticky=tk.W)

ttk.Button(main_frame, text="Добавить задачу", command=add_new_task).grid(row=11, column=0, columnspan=2, pady=10)

update_category_filter()
update_history_list()

root.mainloop()
