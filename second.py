import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from sklearn.linear_model import LinearRegression
from fpdf import FPDF
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

# -------------------- Theme Configuration --------------------
LIGHT_THEME = {
    "PRIMARY_COLOR": "#3498db",
    "BACKGROUND": "#ecf0f1",
    "TEXT_COLOR": "#2C3E50",
    "BUTTON_COLOR": "#2980b9",
    "BUTTON_TEXT": "#ffffff",
}

DARK_THEME = {
    "PRIMARY_COLOR": "#2C3E50",
    "BACKGROUND": "#17202A",
    "TEXT_COLOR": "#ffffff",
    "BUTTON_COLOR": "#1ABC9C",
    "BUTTON_TEXT": "#000000",
}

current_theme = LIGHT_THEME

# -------------------- Helper Functions --------------------
def apply_theme():
    root.configure(bg=current_theme["BACKGROUND"])
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Button):
            widget.configure(style="Custom.TButton")
        elif isinstance(widget, ttk.Label):
            widget.configure(background=current_theme["BACKGROUND"], foreground=current_theme["TEXT_COLOR"])

    style.configure(
        "Custom.TButton",
        background=current_theme["BUTTON_COLOR"],
        foreground=current_theme["BUTTON_TEXT"],
        font=("Arial", 12),
    )
    style.configure("TLabel", background=current_theme["BACKGROUND"], foreground=current_theme["TEXT_COLOR"])

def toggle_theme():
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    apply_theme()

def show_flash_screen():
    flash = tk.Toplevel()
    flash.geometry("1024x700")
    flash.configure(bg=current_theme["PRIMARY_COLOR"])
    flash.overrideredirect(True)

    tk.Label(
        flash,
        text="Welcome to Energy Bill Predictor",
        font=("Arial", 36, "bold"),
        fg=current_theme["BUTTON_TEXT"],
        bg=current_theme["PRIMARY_COLOR"],
    ).pack(expand=True)
    flash.after(2000, flash.destroy)

def navigate_to_frame(frame_name):
    for frame in frames.values():
        frame.pack_forget()
    frames[frame_name].pack(expand=True, fill="both")

# -------------------- Navigation Bar --------------------
def create_navigation_bar(parent_frame):
    nav_bar = tk.Frame(parent_frame, bg=current_theme["PRIMARY_COLOR"], height=50)
    nav_bar.pack(side="top", fill="x")

    for text, frame_name in menu_buttons:
        button = tk.Button(
            nav_bar,
            text=text,
            bg=current_theme["BUTTON_COLOR"],
            fg=current_theme["BUTTON_TEXT"],
            font=("Arial", 12),
            relief="flat",
            command=lambda f=frame_name: navigate_to_frame(f)
        )
        button.pack(side="left", padx=10, pady=5)

# -------------------- Root Window --------------------
root = tk.Tk()
root.title("Energy Bill Predictor")
root.geometry("1024x700")
style = ttk.Style()

# -------------------- Frames Setup --------------------
frames = {
    "home": ttk.Frame(root),
    "add_appliance": ttk.Frame(root),
    "predict": ttk.Frame(root),
    "chatbot": ttk.Frame(root),
    "report": ttk.Frame(root),
    "analysis": ttk.Frame(root),
}
frames["home"].pack(expand=True, fill="both")

# -------------------- Navigation Menu --------------------
menu_buttons = [
    ("🏠 Home", "home"),
    ("➕ Add Appliance", "add_appliance"),
    ("📊 Predict Bill", "predict"),
    ("💬 Chatbot", "chatbot"),
    ("📈 Usage Report", "report"),
    ("📉 Analysis", "analysis"),
    ("📉 Analysis ML", "analysis"),
]

# -------------------- Home Page --------------------
create_navigation_bar(frames["home"])

ttk.Label(frames["home"], text="Welcome to Energy Bill Predictor", font=("Arial", 24, "bold")).pack(pady=20)

for text, frame_name in menu_buttons:
    ttk.Button(frames["home"], text=text, command=lambda f=frame_name: navigate_to_frame(f)).pack(pady=10)

# -------------------- Add Appliance Page --------------------
create_navigation_bar(frames["add_appliance"])

appliance_var = tk.StringVar()
hours_var = tk.StringVar()

ttk.Label(frames["add_appliance"], text="Add an Appliance", font=("Arial", 20)).pack(pady=10)
appliance_menu = ttk.Combobox(
    frames["add_appliance"],
    textvariable=appliance_var,
    values=["Fan", "Air Conditioner", "Refrigerator", "TV", "Washing Machine"],
    font=("Arial", 12),
)
appliance_menu.pack(pady=5)
tk.Entry(frames["add_appliance"], textvariable=hours_var, font=("Arial", 12)).pack(pady=5)

user_appliances = {}
home_listbox = tk.Listbox(frames["add_appliance"], height=8, font=("Arial", 12))
home_listbox.pack(pady=10)

def update_home_list():
    home_listbox.delete(0, tk.END)
    for app, hrs in user_appliances.items():
        home_listbox.insert(tk.END, f"{app} - {hrs} hrs/day")

def add_appliance():
    appliance, hours = appliance_var.get(), hours_var.get()
    if not appliance or not hours.isdigit():
        messagebox.showerror("Input Error", "Enter valid values")
        return
    user_appliances[appliance] = int(hours)
    update_home_list()
    messagebox.showinfo("Success", "Appliance added successfully!")

def remove_appliance():
    selection = home_listbox.curselection()
    if not selection:
        messagebox.showerror("Selection Error", "Select an appliance to remove")
        return
    appliance = home_listbox.get(selection[0]).split(" - ")[0]
    del user_appliances[appliance]
    update_home_list()

ttk.Button(frames["add_appliance"], text="Add Appliance", command=add_appliance).pack(pady=10)
ttk.Button(frames["add_appliance"], text="Remove Appliance", command=remove_appliance).pack(pady=5)

# -------------------- Predict Bill Page --------------------
create_navigation_bar(frames["predict"])

prev_bill_vars = [tk.StringVar() for _ in range(3)]
result_text = tk.StringVar()

ttk.Label(frames["predict"], text="Enter Last 3 Months' Bills (₹):", font=("Arial", 14)).pack(pady=5)
for var in prev_bill_vars:
    tk.Entry(frames["predict"], textvariable=var, font=("Arial", 12)).pack(pady=5)

def predict_bill():
    try:
        bills = np.array([float(var.get()) for var in prev_bill_vars])
        model = LinearRegression().fit(np.array([1, 2, 3]).reshape(-1, 1), bills)
        result_text.set(f"📊 Predicted Bill: ₹{model.predict(np.array([[4]]))[0]:.2f}")
    except ValueError:
        messagebox.showerror("Input Error", "Enter valid bill amounts")

ttk.Button(frames["predict"], text="Predict Bill", command=predict_bill).pack(pady=10)
tk.Label(frames["predict"], textvariable=result_text, font=("Arial", 14, "bold")).pack(pady=10)

# -------------------- Chatbot Page --------------------
create_navigation_bar(frames["chatbot"])

chatbot_text = tk.Text(frames["chatbot"], height=15, width=70, font=("Arial", 12))
chatbot_text.pack(pady=10)

question_var = tk.StringVar()
tk.Entry(frames["chatbot"], textvariable=question_var, font=("Arial", 12)).pack(pady=5)

def chatbot_reply():
    question = question_var.get().lower()
    answers = {
        "how to save energy?": "Turn off unused appliances, use LED bulbs, and limit AC usage.",
        "why is my bill high?": "Check for high-consumption appliances and reduce their usage.",
    }
    chatbot_text.insert(tk.END, f"You: {question}\n")
    chatbot_text.insert(tk.END, f"Bot: {answers.get(question, 'I am not sure, please check with your provider.')}\n\n")

ttk.Button(frames["chatbot"], text="Ask", command=chatbot_reply).pack(pady=10)



# -------------------- Usage Report Page --------------------
create_navigation_bar(frames["report"])

ttk.Label(frames["report"], text="Energy Usage Report", font=("Arial", 24, "bold")).pack(pady=20)

def generate_usage_report():
    if not user_appliances:
        messagebox.showinfo("No Data", "No appliances data to generate report.")
        return
    
    report_text = "Appliance Usage Report\n\n"
    total_hours = sum(user_appliances.values())
    
    report_text += f"Total Hours of Appliance Usage: {total_hours} hrs/day\n\n"
    
    for appliance, hours in user_appliances.items():
        report_text += f"{appliance}: {hours} hrs/day\n"

    report_display = tk.Text(frames["report"], height=15, width=70, font=("Arial", 12))
    report_display.pack(pady=10)
    report_display.insert(tk.END, report_text)

ttk.Button(frames["report"], text="Generate Report", command=generate_usage_report).pack(pady=10)

# -------------------- Analysis Page --------------------
create_navigation_bar(frames["analysis"])

ttk.Label(frames["analysis"], text="Energy Usage Analysis", font=("Arial", 24, "bold")).pack(pady=20)

def plot_usage_graph():
    if not user_appliances:
        messagebox.showinfo("No Data", "No appliances data to plot.")
        return
    
    appliances = list(user_appliances.keys())
    usage = list(user_appliances.values())
    
    plt.figure(figsize=(8, 5))
    plt.bar(appliances, usage, color="skyblue")
    plt.title("Appliance Usage", fontsize=16)
    plt.xlabel("Appliance", fontsize=12)
    plt.ylabel("Hours/day", fontsize=12)
    
    canvas = FigureCanvasTkAgg(plt.gcf(), master=frames["analysis"])
    canvas.get_tk_widget().pack(pady=20)
    canvas.draw()

ttk.Button(frames["analysis"], text="Plot Usage Graph", command=plot_usage_graph).pack(pady=10)

# -------------------- Main Program --------------------
apply_theme()
show_flash_screen()
root.mainloop()





# 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import numpy as np

# Sample data for appliances usage and energy costs
# user_appliances = {
#     "Fan": 6,
#     "Air Conditioner": 5,
#     "Refrigerator": 8,
#     "Washing Machine": 2,
#     "TV": 4,
#     "Heater": 3
# }

# Model setup and training
data = {
    "Appliance": ["Fan", "Air Conditioner", "Refrigerator", "Washing Machine", "TV", "Heater"],
    "Usage_Hours_Per_Day": [6, 5, 8, 2, 4, 3],
    "Energy_Cost_Per_Day": [30, 100, 20, 10, 25, 50]  # Example energy cost per day
}

# Convert data into DataFrame
import pandas as pd
df = pd.DataFrame(data)

# Features and target variable
X = df[["Usage_Hours_Per_Day"]]
y = df["Energy_Cost_Per_Day"]

# Initialize and train the Linear Regression model
model = LinearRegression()
model.fit(X, y)

def get_energy_savings(appliance_usage):
    """
    Predicts energy savings for reducing appliance usage by 2 hours based on trained model.
    :param appliance_usage: Current appliance usage in hours per day.
    :return: Suggested savings in ₹ for reducing usage by 2 hours.
    """
    # Use the trained model to predict the energy cost for the current usage
    predicted_cost = model.predict([[appliance_usage]])[0]
    
    # Calculate the potential savings by reducing 2 hours of usage
    reduced_usage_cost = model.predict([[appliance_usage - 2]])[0]
    
    # Savings = current predicted cost - reduced predicted cost
    savings = predicted_cost - reduced_usage_cost
    
    return savings

def analyze_usage_with_ml():
    if not user_appliances:
        messagebox.showinfo("No Data", "No appliance data available for analysis.")
        return

    sorted_apps = sorted(user_appliances.items(), key=lambda x: x[1], reverse=True)[:3]
    apps, hours = zip(*sorted_apps) if sorted_apps else ([], [])

    # Display usage in a bar chart (as before)
    plt.figure(figsize=(6, 4))
    plt.bar(apps, hours, color='skyblue')
    plt.title("Top 3 Energy-Consuming Appliances", fontsize=14)
    plt.ylabel("Hours/Day")
    plt.xlabel("Appliance")
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(plt.gcf(), master=frames["analysis"])  # Assuming frames["analysis"] is defined
    canvas.get_tk_widget().pack()
    canvas.draw()

    # Generate feedback based on appliance usage with ML predictions
    feedback = "Feedback on Reducing Energy Usage:\n"
    for appliance, usage_hours in user_appliances.items():
        savings = get_energy_savings(usage_hours)
        feedback += f"- Reduce {appliance} by 2 hrs: Save ₹{savings:.2f} on your bill.\n"
    
    feedback_label = ttk.Label(frames["analysis"], text=feedback, font=("Arial", 12), anchor="w")
    feedback_label.pack(pady=10)

# Assuming a button is used to trigger the analysis
ttk.Button(frames["analysis"], text="Analyze Usage", command=analyze_usage_with_ml).pack(pady=10)