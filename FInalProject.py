import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class StockTracker:
    def __init__(self, root):
        self.root = root
        root.geometry("1000x800")  # Window size
        root.title("Stock Price Tracker")

        # Set the background color for the window
        root.configure(bg="#f0f0f0")

        # Input for stock symbol with custom font and padding
        tk.Label(root, text="Enter Stock Symbol", font=("Arial", 14, 'bold'), bg="#f0f0f0", pady=15).pack()

        self.stock_value = tk.StringVar()
        tk.Entry(root, textvariable=self.stock_value, font=("Arial", 12), width=20).pack(pady=10)

        # Style the Show Price button with background color and hover effect
        self.show_price_button = tk.Button(root, text="Show Price", command=self.get_vals, font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised", width=20)
        self.show_price_button.pack(pady=10)

        # Refresh button (not yet implemented)
        self.refresh_button = tk.Button(root, text="Refresh", font=("Arial", 12), bg="#008CBA", fg="white", relief="raised", width=20)
        self.refresh_button.pack(pady=5)

        # Label to show the current price
        self.result_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0")
        self.result_label.pack(pady=10)

        # Frame to hold the plot
        self.plot_frame = tk.Frame(root, bg="#f0f0f0")
        self.plot_frame.pack(pady=20)

    def get_vals(self):
        stock_name = self.stock_value.get()

        if not stock_name:
            messagebox.showerror("Input Error", "Please enter a ticker symbol.")
            return

        try:
            # Fetch stock data
            stock = yf.Ticker(stock_name)
            stock_info = stock.info
            current_price = stock_info.get('currentPrice', 'N/A')

            # Use datetime to create date ranges
            start_date = datetime.datetime(2024, 5, 1).strftime('%Y-%m-%d')
            end_date = datetime.datetime(2024, 10, 1).strftime('%Y-%m-%d')

            # Download historical stock data
            stock_data = yf.download(stock_name, start=start_date, end=end_date)
            if stock_data.empty:
                raise ValueError("No stock data found for the given ticker.")

            # Rename columns for readability
            stock_data.columns = ['Open Price', 'High Price', 'Low Price', 'Close Price', 'Adjusted Close Price', 'Volume']

            # Clear previous plots
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            # Create a new figure with a grid layout
            fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(16, 12))  # 3 rows, 2 columns

            # Flatten the axs array for easier iteration
            axs = axs.flatten()

            # Define color palette for the plots
            colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33F6', '#F6A833', '#33F6FF']

            # Plot each of the 6 data columns
            for i, col in enumerate(stock_data.columns):
                axs[i].plot(stock_data.index, stock_data[col], label=col, color=colors[i], linewidth=2)
                axs[i].set_xlabel('Date')  # Add the x-axis label
                axs[i].set_ylabel('Value')
                axs[i].legend()

                # Remove title to avoid cluttering
                axs[i].set_title('')

                # Adding gridlines with customized style
                axs[i].grid(True, linestyle='--', alpha=0.5)  # Dashed gridlines with transparency

                # Make sure dates are readable, no rotation
                axs[i].tick_params(axis='x', labelrotation=0)

            # Use tight_layout to ensure no overlapping
            fig.tight_layout(pad=3.0)

            # Create a new canvas for the plot
            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

            # Display the current price
            self.result_label.config(text=f"Current Price: {current_price}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = StockTracker(root)
    root.mainloop()
