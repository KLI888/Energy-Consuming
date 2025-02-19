import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import numpy as np
from sklearn.linear_model import LinearRegression
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

class EnergyBillPredictor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Energy Bill Predictor")
        self.root.geometry("1024x700")
        self.root.configure(bg="#F0F8FF")
        # Initialize themes
        self.LIGHT_THEME = {
            "PRIMARY_COLOR": "#2E86C1",
            "SECONDARY_COLOR": "#AED6F1",
            "BACKGROUND": "#F5F8FA",
            "TEXT_COLOR": "#2C3E50",
            "BUTTON_COLOR": "#3498DB",
            "BUTTON_TEXT": "#FFFFFF",
            "ACCENT_COLOR": "#E74C3C",
            "SUCCESS_COLOR": "#2ECC71",
            "HOVER_COLOR": "#2574A9"
        }
        
        self.current_theme = self.LIGHT_THEME
        self.frames = {}
        self.user_appliances = {}
        
        # Initialize menu buttons
        self.menu_buttons = [
            ("🏠 Home", "home"),
            ("➕ Add Appliance", "add_appliance"),
            ("📊 Predict Bill", "predict"),
            ("💬 Chatbot", "chatbot"),
            ("📈 Usage Report", "report"),
            ("📉 Analysis", "analysis"),
            ("📉 ML Report", "mlreport")
        ]
        
        # Start with splash screen
        self.show_splash_screen()
        
    def gradient_color(self, color1, color2, ratio):
        r1 = int(color1[1:3], 16)
        g1 = int(color1[3:5], 16)
        b1 = int(color1[5:7], 16)
        
        r2 = int(color2[1:3], 16)
        g2 = int(color2[3:5], 16)
        b2 = int(color2[5:7], 16)
        
        r = int(r1 * (1-ratio) + r2 * ratio)
        g = int(g1 * (1-ratio) + g2 * ratio)
        b = int(b1 * (1-ratio) + b2 * ratio)
        
        return f'#{r:02x}{g:02x}{b:02x}'

    def show_splash_screen(self):
        splash_frame = tk.Frame(self.root, bg=self.current_theme["PRIMARY_COLOR"])
        splash_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(splash_frame, width=1024, height=700, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Create gradient background
        for i in range(700):
            color = self.gradient_color(
                self.current_theme["PRIMARY_COLOR"],
                self.current_theme["SECONDARY_COLOR"],
                i/700
            )
            canvas.create_line(0, i, 1024, i, fill=color)
        
        def create_circle(progress):
            canvas.delete("progress")
            radius = 50
            x, y = 512, 450
            start = 90
            extent = progress * 360
            
            canvas.create_arc(x-radius, y-radius, x+radius, y+radius,
                            start=start, extent=extent,
                            fill=self.current_theme["SUCCESS_COLOR"],
                            tags="progress")
            
            canvas.create_text(x, y, text=f"{int(progress * 100)}%",
                            font=("Helvetica", 16, "bold"),
                            fill="white", tags="progress")
        
        # Try to load logo
        try:
            logo_image = PhotoImage(file="images/save.png")
            canvas.create_image(512, 250, image=logo_image, anchor="center")
            canvas.image = logo_image
        except:
            canvas.create_oval(462, 200, 562, 300,
                             fill=self.current_theme["SECONDARY_COLOR"])
        
        # Welcome text
        canvas.create_text(514, 352,
                          text="Welcome to Energy Bill Predictor",
                          font=("Helvetica", 36, "bold"),
                          fill="#000000", anchor="center")
        canvas.create_text(512, 350,
                          text="Welcome to Energy Bill Predictor",
                          font=("Helvetica", 36, "bold"),
                          fill="#FFFFFF", anchor="center")
        
        canvas.create_text(512, 550, text="Loading...",
                          font=("Helvetica", 14),
                          fill="#FFFFFF", anchor="center")
        
        def update_progress(step=0):
            if step <= 100:
                progress = step / 100
                create_circle(progress)
                self.root.after(30, lambda: update_progress(step + 2))
            else:
                splash_frame.destroy()
                self.initialize_main_content()
        
        update_progress()
        self.root.update()

    def create_scrollable_frame(self, parent):
        container = ttk.Frame(parent)
        canvas = tk.Canvas(container, bg=self.current_theme["BACKGROUND"])
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        container.pack(fill="both", expand=True)

        return scrollable_frame

    def initialize_main_content(self):
        # Create frames
        for _, frame_name in self.menu_buttons:
            frame = ttk.Frame(self.root)
            scrollable_frame = self.create_scrollable_frame(frame)
            self.frames[frame_name] = (frame, scrollable_frame)

        # Create pages
        self.create_home_page()
        self.create_add_appliance_page()
        self.create_predict_page()
        self.create_chatbot_page()
        self.create_report_page()
        self.create_analysis_page()
        self.create_mlreport_page()

        # Show home page
        self.show_frame('home')

    def create_navigation_bar(self, parent):
        nav_bar = tk.Frame(parent, bg=self.current_theme["PRIMARY_COLOR"], height=60)
        nav_bar.pack(side="top", fill="x")
        
        for text, frame_name in self.menu_buttons:
            btn = tk.Button(
                nav_bar,
                text=text,
                command=lambda f=frame_name: self.show_frame(f),
                bg=self.current_theme["BUTTON_COLOR"],
                fg=self.current_theme["BUTTON_TEXT"],
                font=("Helvetica", 12),
                relief="flat",
                padx=15,
                pady=5
            )
            btn.pack(side="left", padx=5, pady=5)

    def show_frame(self, frame_name):
        # Hide all frames
        for frame, _ in self.frames.values():
            frame.pack_forget()
        
        # Show selected frame
        frame, _ = self.frames[frame_name]
        frame.pack(fill="both", expand=True)

    def create_home_page(self):
        frame, scrollable_frame = self.frames['home']
        self.create_navigation_bar(frame)
        
        ttk.Label(scrollable_frame,
                 text="Welcome to Energy Bill Predictor",
                 font=("Helvetica", 24, "bold")).pack(pady=20)
        
        try:
            image = PhotoImage(file="images/save.png")
            label = tk.Label(scrollable_frame, image=image)
            label.image = image
            label.pack(pady=20)
        except:
            print("Warning: Could not load image file")

    def create_add_appliance_page(self):
        frame, scrollable_frame = self.frames['add_appliance']
        self.create_navigation_bar(frame)
        
        # Title
        ttk.Label(scrollable_frame,
                 text="Add an Appliance",
                 font=("Helvetica", 24, "bold")).pack(pady=20)
        
        # Appliance selection
        appliance_frame = ttk.Frame(scrollable_frame)
        appliance_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(appliance_frame,
                 text="Select Appliance:",
                 font=("Helvetica", 12)).pack(side="left", padx=5)
        
        self.appliance_var = tk.StringVar()
        appliance_menu = ttk.Combobox(
            appliance_frame,
            textvariable=self.appliance_var,
            values=["Fan", "Air Conditioner", "Refrigerator", "TV", "Washing Machine"],
            font=("Helvetica", 12),
            state="readonly",
            width=30
        )
        appliance_menu.pack(side="left", padx=5)
        
        # Hours input
        hours_frame = ttk.Frame(scrollable_frame)
        hours_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(hours_frame,
                 text="Hours per day:",
                 font=("Helvetica", 12)).pack(side="left", padx=5)
        
        self.hours_var = tk.StringVar()
        hours_entry = ttk.Entry(
            hours_frame,
            textvariable=self.hours_var,
            font=("Helvetica", 12),
            width=10
        )
        hours_entry.pack(side="left", padx=5)
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=20, padx=20)
        
        add_button = tk.Button(
            button_frame,
            text="Add Appliance",
            command=self.add_appliance,
            bg=self.current_theme["BUTTON_COLOR"],
            fg=self.current_theme["BUTTON_TEXT"],
            font=("Helvetica", 12),
            relief="flat",
            padx=15,
            pady=5
        )
        add_button.pack(side="left", padx=5)
        
        remove_button = tk.Button(
            button_frame,
            text="Remove Selected",
            command=self.remove_appliance,
            bg=self.current_theme["ACCENT_COLOR"],
            fg=self.current_theme["BUTTON_TEXT"],
            font=("Helvetica", 12),
            relief="flat",
            padx=15,
            pady=5
        )
        remove_button.pack(side="left", padx=5)
        
        # Listbox to show added appliances
        self.appliance_listbox = tk.Listbox(
            scrollable_frame,
            height=8,
            font=("Helvetica", 12),
            selectmode="single",
            width=50
        )
        self.appliance_listbox.pack(pady=10, padx=20)
        
        # Add some instructions
        instruction_text = """
        Instructions:
        1. Select an appliance from the dropdown menu
        2. Enter the number of hours the appliance is used per day
        3. Click 'Add Appliance' to add it to your list
        4. To remove an appliance, select it from the list and click 'Remove Selected'
        """
        ttk.Label(scrollable_frame,
                 text=instruction_text,
                 font=("Helvetica", 10),
                 justify="left").pack(pady=20, padx=20)
        
    def add_appliance(self):
        appliance = self.appliance_var.get()
        hours = self.hours_var.get()
        
        if not appliance:
            messagebox.showerror("Error", "Please select an appliance")
            return
            
        if not hours.isdigit() or int(hours) < 0 or int(hours) > 24:
            messagebox.showerror("Error", "Please enter valid hours (0-24)")
            return
            
        self.user_appliances[appliance] = int(hours)
        self.update_appliance_list()
        
        # Clear the inputs
        self.appliance_var.set("")
        self.hours_var.set("")
        
        messagebox.showinfo("Success", f"{appliance} added successfully!")
        
    def remove_appliance(self):
        selection = self.appliance_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an appliance to remove")
            return
            
        appliance = self.appliance_listbox.get(selection[0]).split(" - ")[0]
        del self.user_appliances[appliance]
        self.update_appliance_list()
        
    def update_appliance_list(self):
        self.appliance_listbox.delete(0, tk.END)
        for app, hrs in self.user_appliances.items():
            self.appliance_listbox.insert(tk.END, f"{app} - {hrs} hrs/day")
        
    # def create_predict_page(self):
    #     frame, scrollable_frame = self.frames['predict']
    #     self.create_navigation_bar(frame)
        
    #     ttk.Label(scrollable_frame,
    #              text="Predict Your Bill",
    #              font=("Helvetica", 24, "bold")).pack(pady=20)
        
    #     prev_bill_vars = [tk.StringVar() for _ in range(3)]
    #     result_text = tk.StringVar()

    #     ttk.Label(scrollable_frame, text="Enter Last 3 Months' Bills (₹):", font=("Arial", 14)).pack(pady=5)
    #     for var in prev_bill_vars:
    #         tk.Entry(scrollable_frame, textvariable=var, font=("Arial", 12)).pack(pady=5)

    #     def predict_bill():
    #         try:
    #             bills = np.array([float(var.get()) for var in prev_bill_vars])
    #             model = LinearRegression().fit(np.array([1, 2, 3]).reshape(-1, 1), bills)
    #             result_text.set(f"📊 Predicted Bill: ₹{model.predict(np.array([[4]]))[0]:.2f}")
    #         except ValueError:
    #             messagebox.showerror("Input Error", "Enter valid bill amounts")

    #     ttk.Button(scrollable_frame, text="Predict Bill", command=predict_bill).pack(pady=10)
    #     tk.Label(scrollable_frame, textvariable=result_text, font=("Arial", 14, "bold")).pack(pady=10)

        
        # Add prediction form content here

    def create_predict_page(self):
        frame, scrollable_frame = self.frames['predict']
        self.create_navigation_bar(frame)
        
        # Main container with padding
        main_container = ttk.Frame(scrollable_frame)
        main_container.pack(pady=40, padx=60, fill="both", expand=True)
        
        # Title with larger padding and bigger font
        ttk.Label(main_container,
                text="Predict Your Bill",
                font=("Helvetica", 32, "bold")).pack(pady=30)
        
        # Create container for bill inputs
        bill_container = ttk.Frame(main_container)
        bill_container.pack(pady=20, fill="x")
        
        prev_bill_vars = [tk.StringVar() for _ in range(3)]
        result_text = tk.StringVar()
        
        # Header with larger font and spacing
        ttk.Label(bill_container, 
                text="Enter Last 3 Months' Bills (₹):", 
                font=("Arial", 18, "bold")).pack(pady=20)
        
        # Create styled entry fields
        for i, var in enumerate(prev_bill_vars):
            entry_frame = ttk.Frame(bill_container)
            entry_frame.pack(pady=15)
            
            # Month label
            ttk.Label(entry_frame,
                    text=f"Month {i+1}:",
                    font=("Arial", 14)).pack(side="left", padx=10)
            
            # Styled entry with currency symbol
            entry = tk.Entry(entry_frame,
                            textvariable=var,
                            font=("Arial", 14),
                            width=20,
                            justify="center")
            entry.pack(side="left", padx=10)
            entry.insert(0, "₹")
            
            # Add placeholder text
            if not var.get():
                entry.insert(0, "Enter amount")
        
        def predict_bill():
            try:
                # Remove currency symbol and convert to float
                bills = np.array([float(var.get().replace('₹', '')) for var in prev_bill_vars])
                model = LinearRegression().fit(np.array([1, 2, 3]).reshape(-1, 1), bills)
                predicted = model.predict(np.array([[4]]))[0]
                result_text.set(f"📊 Predicted Bill: ₹{predicted:,.2f}")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid bill amounts")
        
        # Create styled button container
        button_container = ttk.Frame(main_container)
        button_container.pack(pady=30)
        
        # Large, styled predict button
        predict_button = tk.Button(button_container,
                                text="Calculate Prediction",
                                command=predict_bill,
                                font=("Arial", 14, "bold"),
                                bg="#2E86C1",
                                fg="white",
                                padx=30,
                                pady=10,
                                relief="raised",
                                cursor="hand2")
        predict_button.pack()
        
        # Add hover effect to button
        def on_enter(e):
            predict_button['background'] = '#2874A6'
        def on_leave(e):
            predict_button['background'] = '#2E86C1'
        
        predict_button.bind("<Enter>", on_enter)
        predict_button.bind("<Leave>", on_leave)
        
        # Result display with large font and padding
        result_frame = ttk.Frame(main_container)
        result_frame.pack(pady=30)
        
        tk.Label(result_frame,
                textvariable=result_text,
                font=("Arial", 18, "bold"),
                fg="#2E86C1").pack(pady=20)
        
        # Add informational text
        info_text = """
        How it works:
        • Enter your electricity bills for the last 3 months
        • Our AI model analyzes your consumption pattern
        • Get an accurate prediction for next month's bill
        • Use this information to plan your energy usage
        """
        
        ttk.Label(main_container,
                text=info_text,
                font=("Arial", 12),
                justify="left").pack(pady=20)

    def create_chatbot_page(self):
        frame, scrollable_frame = self.frames['chatbot']
        self.create_navigation_bar(frame)
        chatbot_text = tk.Text(scrollable_frame, height=15, width=70, font=("Arial", 12))
        chatbot_text.pack(pady=10)

        ttk.Label(scrollable_frame,
                 text="Chat with Energy Assistant",
                 font=("Helvetica", 24, "bold")).pack(pady=20)
        
        question_var = tk.StringVar()
        tk.Entry(scrollable_frame, textvariable=question_var, font=("Arial", 12)).pack(pady=5)

        # Function to handle chatbot reply
        def chatbot_reply():
            question = question_var.get().lower()
            answers = {
                "how to save energy?": "Turn off unused appliances, use LED bulbs, and limit AC usage.",
                "why is my bill high?": "Check for high-consumption appliances and reduce their usage.",
            }
            chatbot_text.insert(tk.END, f"You: {question}\n")
            chatbot_text.insert(tk.END, f"Bot: {answers.get(question, 'I am not sure, please check with your provider.')}\n\n")

        # Ask Button
        ttk.Button(scrollable_frame, text="Ask", command=chatbot_reply).pack(pady=10)

        instructions = [
                "1. The user is creating a `GameRound` model instance every 30 seconds and requires their view to always display the latest instance.",
                "2. The user is creating a `GameRound` model instance every 30 seconds and requires their view to always display the latest instance.",
                "3. The user is creating a `GameRound` model instance every 30 seconds and requires their view to always display the latest instance."
            ]

            # Display each instruction in a label
        for idx, instruction in enumerate(instructions):
                label = tk.Label(scrollable_frame, text=instruction, padx=10, pady=10, font=("Arial", 10))
                label.pack()
        
        # Add chatbot content here
    
    def create_report_page(self):
        frame, scrollable_frame = self.frames['report']
        self.create_navigation_bar(frame)
        
        # Title
        ttk.Label(scrollable_frame,
                text="Energy Usage Report",
                font=("Helvetica", 24, "bold")).pack(pady=20)
        
        # Create text widget first
        self.report_display = tk.Text(scrollable_frame, 
                                    height=15, 
                                    width=70, 
                                    font=("Arial", 12))
        self.report_display.pack(pady=10)
        
        def generate_report():
            # Clear previous content
            self.report_display.delete(1.0, tk.END)
            
            if not self.user_appliances:
                messagebox.showinfo("No Data", "No appliances data to generate report.")
                return
            
            report_text = "📊 Appliance Usage Report 📊\n\n"
            total_hours = sum(self.user_appliances.values())
            
            report_text += f"Total Hours of Appliance Usage: {total_hours} hrs/day\n\n"
            
            # Add appliance details
            for appliance, hours in self.user_appliances.items():
                percentage = (hours / total_hours) * 100
                report_text += f"🔌 {appliance}: {hours} hrs/day ({percentage:.1f}%)\n"
            
            # Add usage analysis
            report_text += "\n💡 Usage Analysis:\n"
            for appliance, hours in self.user_appliances.items():
                if hours > 8:
                    report_text += f"⚠️ High usage: {appliance} ({hours} hrs/day)\n"
                elif hours > 4:
                    report_text += f"ℹ️ Moderate usage: {appliance} ({hours} hrs/day)\n"
                else:
                    report_text += f"✅ Efficient usage: {appliance} ({hours} hrs/day)\n"
            
            # Insert the report text
            self.report_display.insert(tk.END, report_text)
        
        # Add generate button with styling
        generate_button = tk.Button(
            scrollable_frame,
            text="Generate Report",
            command=generate_report,
            font=("Arial", 12, "bold"),
            bg="#2E86C1",
            fg="white",
            padx=20,
            pady=10
        )
        generate_button.pack(pady=10)

    def create_analysis_page(self):
        frame, scrollable_frame = self.frames['analysis']
        self.create_navigation_bar(frame)
        
        # Title
        ttk.Label(scrollable_frame,
                text="Usage Analysis",
                font=("Helvetica", 24, "bold")).pack(pady=20)
        
        # Create frame to hold the canvas
        self.chart_frame = ttk.Frame(scrollable_frame)
        self.chart_frame.pack(pady=20, fill="both", expand=True)
        
        # Create frame for analysis text
        self.analysis_text_frame = ttk.Frame(scrollable_frame)
        self.analysis_text_frame.pack(pady=20, padx=20, fill="x")
        
        def generate_analysis():
            # Clear previous charts and analysis
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            for widget in self.analysis_text_frame.winfo_children():
                widget.destroy()
                
            if not self.user_appliances:
                messagebox.showwarning("No Data", "Please add appliances first in the 'Add Appliance' section!")
                return
                
            # Create DataFrame from user's appliances
            appliances = list(self.user_appliances.keys())
            hours = list(self.user_appliances.values())
            
            # Estimate energy costs (example calculation - you can modify this)
            energy_costs = []
            for appliance, hour in self.user_appliances.items():
                # Different base costs for different appliances
                base_cost = {
                    "Fan": 5,
                    "Air Conditioner": 20,
                    "Refrigerator": 15,
                    "TV": 8,
                    "Washing Machine": 12
                }.get(appliance, 10)  # Default cost if appliance not in dict
                
                cost = base_cost * hour
                energy_costs.append(cost)
            
            data = {
                "Appliance": appliances,
                "Usage_Hours_Per_Day": hours,
                "Energy_Cost_Per_Day": energy_costs
            }
            df = pd.DataFrame(data)
            
            # Create figure for matplotlib
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
            fig.suptitle('Your Energy Usage Analysis', fontsize=16)
            
            # Bar plot for current usage
            bars = ax1.bar(df['Appliance'], df['Energy_Cost_Per_Day'])
            ax1.set_title('Daily Energy Cost by Your Appliances')
            ax1.set_xlabel('Appliance')
            ax1.set_ylabel('Estimated Cost (₹)')
            ax1.tick_params(axis='x', rotation=45)
            
            # Add value labels on the bars
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'₹{int(height)}',
                        ha='center', va='bottom')
            
            # Scatter plot with regression line
            X = df['Usage_Hours_Per_Day']
            y = df['Energy_Cost_Per_Day']
            
            ax2.scatter(X, y)
            ax2.set_title('Your Usage Hours vs Cost')
            ax2.set_xlabel('Usage Hours Per Day')
            ax2.set_ylabel('Estimated Cost (₹)')
            
            # Add regression line if we have more than one point
            if len(X) > 1:
                model = LinearRegression()
                model.fit(X.values.reshape(-1, 1), y)
                line_x = np.linspace(X.min(), X.max(), 100)
                line_y = model.predict(line_x.reshape(-1, 1))
                ax2.plot(line_x, line_y, color='red', linestyle='--')
            
            # Adjust layout
            plt.tight_layout()
            
            # Create canvas for matplotlib figure
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)
            
            # Calculate total daily cost
            total_cost = sum(energy_costs)
            
            # Add analysis text
            analysis_text = f"""
            Analysis Summary:
            
            📊 Total Daily Energy Cost: ₹{total_cost:.2f}
            
            Breakdown by Appliance:
            """
            
            for appliance, hours, cost in zip(appliances, hours, energy_costs):
                percentage = (cost / total_cost) * 100
                analysis_text += f"\n• {appliance}: {hours} hours/day - ₹{cost:.2f} ({percentage:.1f}% of total cost)"
            
            analysis_label = ttk.Label(
                self.analysis_text_frame,
                text=analysis_text,
                font=("Helvetica", 12),
                justify="left"
            )
            analysis_label.pack(pady=10)
            
            # Add recommendations based on usage
            recommendations = "\nRecommendations for Energy Savings:\n"
            
            for appliance, hours in self.user_appliances.items():
                if hours > 6:
                    recommendations += f"\n• Consider reducing {appliance} usage ({hours} hours/day is high)"
                elif hours > 4:
                    recommendations += f"\n• Monitor {appliance} usage to optimize efficiency"
            
            recommendations_label = ttk.Label(
                self.analysis_text_frame,
                text=recommendations,
                font=("Helvetica", 12),
                justify="left"
            )
            recommendations_label.pack(pady=10)
        
        # Create styled button for generating analysis
        generate_button = tk.Button(
            scrollable_frame,
            text="Generate Analysis from Your Appliances",
            command=generate_analysis,
            font=("Arial", 12, "bold"),
            bg="#2E86C1",
            fg="white",
            padx=20,
            pady=10,
            relief="raised",
            cursor="hand2"
        )
        generate_button.pack(pady=20)
        
        # Add hover effect to button
        def on_enter(e):
            generate_button['background'] = '#2874A6'
        def on_leave(e):
            generate_button['background'] = '#2E86C1'
        
        generate_button.bind("<Enter>", on_enter)
        generate_button.bind("<Leave>", on_leave)
        
        # Add instructions
        instructions = """
        Instructions:
        1. First add your appliances in the 'Add Appliance' section
        2. Come back to this page and click 'Generate Analysis'
        3. View your personalized energy usage analysis and recommendations
        """
        
        ttk.Label(scrollable_frame,
                text=instructions,
                font=("Helvetica", 12),
                justify="left").pack(pady=20, padx=20)
    
    def create_mlreport_page(self):
        frame, scrollable_frame = self.frames['mlreport']
        self.create_navigation_bar(frame)
        
        # Title
        ttk.Label(scrollable_frame,
                text="ML Analysis Report",
                font=("Helvetica", 24, "bold")).pack(pady=20)
        
        # Create frame to hold the canvas and analysis
        self.ml_chart_frame = ttk.Frame(scrollable_frame)
        self.ml_chart_frame.pack(pady=20, fill="both", expand=True)
        
        # Create frame for analysis text
        self.ml_analysis_frame = ttk.Frame(scrollable_frame)
        self.ml_analysis_frame.pack(pady=20, padx=20, fill="x")
        
        def get_energy_savings(appliance, usage_hours):
            # Base costs for different appliances (₹ per hour)
            base_costs = {
                "Fan": 2,
                "Air Conditioner": 15,
                "Refrigerator": 4,
                "TV": 3,
                "Washing Machine": 5
            }
            
            # Get base cost for the appliance
            base_cost = base_costs.get(appliance, 5)  # Default 5 if appliance not found
            
            # Calculate current daily cost
            current_cost = base_cost * usage_hours
            
            # Calculate cost with 2 hours reduced
            reduced_hours = max(0, usage_hours - 2)  # Ensure hours don't go below 0
            reduced_cost = base_cost * reduced_hours
            
            # Return potential savings
            return current_cost - reduced_cost
        
        def analyze_usage_with_ml():
            # Clear previous charts and analysis
            for widget in self.ml_chart_frame.winfo_children():
                widget.destroy()
            for widget in self.ml_analysis_frame.winfo_children():
                widget.destroy()
            
            if not self.user_appliances:
                messagebox.showwarning("No Data", "Please add appliances first in the 'Add Appliance' section!")
                return
            
            # Create figure for plots - smaller size
            fig = plt.figure(figsize=(8, 4))
            plt.clf()  # Clear the figure
            
            # Sort appliances by usage hours
            sorted_apps = sorted(self.user_appliances.items(), key=lambda x: x[1], reverse=True)
            apps, hours = zip(*sorted_apps)
            
            # Create bar chart
            # First subplot with smaller font sizes
            plt.subplot(1, 2, 1)
            bars = plt.bar(apps, hours, color='skyblue')
            plt.title("Energy Consumption", fontsize=10)
            plt.ylabel("Hours/Day", fontsize=8)
            plt.xlabel("Appliance", fontsize=8)
            plt.xticks(rotation=45, fontsize=8)
            plt.title("Energy Consumption by Appliance", fontsize=12)
            plt.ylabel("Hours/Day")
            plt.xlabel("Appliance")
            plt.xticks(rotation=45)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}h',
                        ha='center', va='bottom')
            
            # Create pie chart
            plt.subplot(1, 2, 2)
            total_hours = sum(hours)
            plt.pie(hours, labels=apps, autopct='%1.1f%%',
                    startangle=90, colors=plt.cm.Pastel1(np.linspace(0, 1, len(apps))),
                    textprops={'fontsize': 8})
            plt.title("Usage Distribution", fontsize=10)
            
            plt.tight_layout()
            
            # Create canvas for matplotlib figure
            canvas = FigureCanvasTkAgg(fig, master=self.ml_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)
            
            # Generate ML Analysis text
            analysis_text = "🤖 Machine Learning Analysis\n\n"
            
            # Add usage patterns analysis
            analysis_text += "📊 Usage Patterns:\n"
            for appliance, hours in sorted_apps:
                if hours > 8:
                    analysis_text += f"• {appliance}: Very High Usage ({hours} hrs/day)\n"
                elif hours > 5:
                    analysis_text += f"• {appliance}: High Usage ({hours} hrs/day)\n"
                else:
                    analysis_text += f"• {appliance}: Normal Usage ({hours} hrs/day)\n"
            
            # Add savings predictions
            analysis_text += "\n💰 Predicted Daily Savings:\n"
            total_savings = 0
            for appliance, hours in sorted_apps:
                if hours > 2:
                    savings = get_energy_savings(appliance, hours)
                    total_savings += savings
                    analysis_text += f"• Reduce {appliance} by 2 hrs: Save ₹{savings:.2f}\n"
            
            analysis_text += f"\n📈 Total Potential Daily Savings: ₹{total_savings:.2f}"
            
            # Add recommendations
            analysis_text += "\n\n🎯 AI Recommendations:\n"
            for appliance, hours in sorted_apps:
                if hours > 8:
                    analysis_text += f"• Consider using {appliance} in off-peak hours\n"
                elif hours > 5:
                    analysis_text += f"• Monitor {appliance} usage patterns\n"
            
            # Create text widget for analysis
            analysis_label = ttk.Label(
                self.ml_analysis_frame,
                text=analysis_text,
                font=("Helvetica", 12),
                justify="left"
            )
            analysis_label.pack(pady=10)
        
        # Create styled button for analysis
        generate_button = tk.Button(
            scrollable_frame,
            text="Generate ML Analysis",
            command=analyze_usage_with_ml,
            font=("Arial", 12, "bold"),
            bg="#2E86C1",
            fg="white",
            padx=20,
            pady=10,
            relief="raised",
            cursor="hand2"
        )
        generate_button.pack(pady=20)
        
        # Add hover effect to button
        def on_enter(e):
            generate_button['background'] = '#2874A6'
        def on_leave(e):
            generate_button['background'] = '#2E86C1'
        
        generate_button.bind("<Enter>", on_enter)
        generate_button.bind("<Leave>", on_leave)
        
        # Add instructions
        instructions = """
        Instructions:
        1. First add your appliances in the 'Add Appliance' section
        2. Click 'Generate ML Analysis' to see detailed insights
        3. View usage patterns and AI-powered recommendations
        """
        
        ttk.Label(scrollable_frame,
                text=instructions,
                font=("Helvetica", 12),
                justify="left").pack(pady=20, padx=20)
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EnergyBillPredictor()
    app.run()
