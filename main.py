import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import csv

class FancyBudgetPlanner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fancy Budget Planner")
        self.geometry("800x600")
        self.configure(bg="#f0f4f8")  # Light pastel background
        self.expenses = []
        self.total_budget = 0
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self, text="Fancy Budget Planner", font=("Verdana", 24, "bold"), bg="#f0f4f8", fg="#2c3e50").pack(pady=20)
        
        # Budget Entry
        tk.Label(self, text="Set Your Budget:", font=("Verdana", 14), bg="#f0f4f8").pack(pady=5)
        self.budget_entry = tk.Entry(self, font=("Verdana", 14), width=20)
        self.budget_entry.pack(pady=5)
        tk.Button(self, text="Set Budget", command=self.set_budget, font=("Verdana", 12), bg="#3498db", fg="white", width=15).pack(pady=10)
        
        # Expense Entry
        tk.Label(self, text="Add an Expense:", font=("Verdana", 14), bg="#f0f4f8").pack(pady=5)
        tk.Label(self, text="Category:", font=("Verdana", 12), bg="#f0f4f8").pack(pady=2)
        self.category_var = tk.StringVar(value="Select Category")
        self.category_menu = ttk.Combobox(self, textvariable=self.category_var, font=("Verdana", 12), state="readonly", values=["Accommodation", "Food", "Travel", "Shopping", "Miscellaneous"])
        self.category_menu.pack(pady=2)
        
        tk.Label(self, text="Amount:", font=("Verdana", 12), bg="#f0f4f8").pack(pady=2)
        self.amount_entry = tk.Entry(self, font=("Verdana", 12), width=20)
        self.amount_entry.pack(pady=5)
        
        tk.Button(self, text="Add Expense", command=self.add_expense, font=("Verdana", 12), bg="#2ecc71", fg="white", width=15).pack(pady=10)
        
        # Expense List
        self.expense_listbox = tk.Listbox(self, font=("Verdana", 12), height=10, width=80)
        self.expense_listbox.pack(pady=10)
        
        # Summary Buttons
        button_frame = tk.Frame(self, bg="#f0f4f8")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Show Summary", command=self.show_summary, font=("Verdana", 12), bg="#f39c12", fg="white", width=15).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Save to CSV", command=self.save_to_csv, font=("Verdana", 12), bg="#e74c3c", fg="white", width=15).grid(row=0, column=1, padx=10)

    def set_budget(self):
        try:
            self.total_budget = float(self.budget_entry.get())
            messagebox.showinfo("Budget Set", f"Your budget is set to ₹{self.total_budget:.2f}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the budget.")

    def add_expense(self):
        category = self.category_var.get()
        try:
            amount = float(self.amount_entry.get())
            if category == "Select Category":
                messagebox.showwarning("Invalid Category", "Please select a valid category.")
                return
            self.expenses.append((category, amount))
            self.expense_listbox.insert(tk.END, f"{category}: ₹{amount:.2f}")
            self.amount_entry.delete(0, tk.END)
            messagebox.showinfo("Expense Added", f"Added {category} expense of ₹{amount:.2f}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")

    def show_summary(self):
        if not self.expenses:
            messagebox.showwarning("No Expenses", "No expenses to summarize.")
            return
        categories = [expense[0] for expense in self.expenses]
        amounts = [expense[1] for expense in self.expenses]
        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=categories, autopct="%.1f%%", startangle=140, colors=["#3498db", "#2ecc71", "#f39c12", "#e74c3c", "#9b59b6"])
        plt.title("Expense Distribution")
        plt.show()

    def save_to_csv(self):
        if not self.expenses:
            messagebox.showwarning("No Expenses", "No expenses to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], title="Save as CSV")
        if file_path:
            try:
                with open(file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Category", "Amount"])
                    writer.writerows(self.expenses)
                messagebox.showinfo("Success", f"Expenses saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = FancyBudgetPlanner()
    app.mainloop()
