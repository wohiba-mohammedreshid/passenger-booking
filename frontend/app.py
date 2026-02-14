import tkinter as tk
from tkinter import messagebox

class BusGoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BusGo Passenger Booking")
        self.current_step = 1
        self.booking_data = {}

        # Initialize UI
        self.create_home_screen()

    def create_home_screen(self):
        self.clear_screen()
        self.current_step = 1

        label = tk.Label(self.root, text="Welcome to BusGo", font=("Arial", 24))
        label.pack(pady=20)

        book_now_btn = tk.Button(self.root, text="Book Now", command=self.show_route_selection)
        book_now_btn.pack(pady=10)

    def show_route_selection(self):
        self.clear_screen()
        self.current_step = 2

        label = tk.Label(self.root, text="Select Your Route", font=("Arial", 20))
        label.pack(pady=20)

        # Departure Station
        departure_label = tk.Label(self.root, text="Departure Station:")
        departure_label.pack()
        self.departure_var = tk.StringVar()
        self.departure_dropdown = tk.OptionMenu(self.root, self.departure_var, *["Station A", "Station B", "Station C"])
        self.departure_dropdown.pack()

        # Destination Station
        destination_label = tk.Label(self.root, text="Destination Station:")
        destination_label.pack()
        self.destination_var = tk.StringVar()
        self.destination_dropdown = tk.OptionMenu(self.root, self.destination_var, *["Station A", "Station B", "Station C"])
        self.destination_dropdown.pack()

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.create_home_screen)
        cancel_btn.pack(side=tk.LEFT, padx=5)

        undo_btn = tk.Button(button_frame, text="Undo", command=self.clear_selections)
        undo_btn.pack(side=tk.LEFT, padx=5)

        continue_btn = tk.Button(button_frame, text="Continue", command=self.validate_route_selection)
        continue_btn.pack(side=tk.LEFT, padx=5)

    def validate_route_selection(self):
        departure = self.departure_var.get()
        destination = self.destination_var.get()

        if not departure or not destination:
            messagebox.showerror("Error", "Please select both departure and destination stations.")
            return
        if departure == destination:
            messagebox.showerror("Error", "Departure and destination cannot be the same.")
            return

        self.booking_data["departure"] = departure
        self.booking_data["destination"] = destination
        self.show_passenger_identification()

    def show_passenger_identification(self):
        self.clear_screen()
        self.current_step = 3

        label = tk.Label(self.root, text="Passenger Identification", font=("Arial", 20))
        label.pack(pady=20)

        fan_label = tk.Label(self.root, text="Enter your FAN:")
        fan_label.pack()
        self.fan_entry = tk.Entry(self.root)
        self.fan_entry.pack()

        send_code_btn = tk.Button(self.root, text="Send Code", command=self.send_otp)
        send_code_btn.pack(pady=10)

    def send_otp(self):
        fan = self.fan_entry.get()
        if fan:
            # Simulate OTP sending
            messagebox.showinfo("Success", "OTP sent successfully!")
            self.show_otp_verification()
        else:
            messagebox.showerror("Error", "Please enter your FAN.")

    def show_otp_verification(self):
        self.clear_screen()
        self.current_step = 4

        label = tk.Label(self.root, text="OTP Verification", font=("Arial", 20))
        label.pack(pady=20)

        otp_label = tk.Label(self.root, text="Enter verification code:")
        otp_label.pack()
        self.otp_entry = tk.Entry(self.root)
        self.otp_entry.pack()

        verify_btn = tk.Button(self.root, text="Verify", command=self.verify_otp)
        verify_btn.pack(pady=10)

    def verify_otp(self):
        otp = self.otp_entry.get()
        if otp == "1234":  # Simulate OTP verification
            messagebox.showinfo("Success", "OTP verified successfully!")
            self.show_payment_selection()
        else:
            messagebox.showerror("Error", "Invalid OTP. Please try again.")

    def show_payment_selection(self):
        self.clear_screen()
        self.current_step = 5

        label = tk.Label(self.root, text="Select Payment Method", font=("Arial", 20))
        label.pack(pady=20)

        self.payment_var = tk.StringVar(value="credit_card")

        credit_card_radio = tk.Radiobutton(self.root, text="Credit Card", variable=self.payment_var, value="credit_card")
        credit_card_radio.pack()

        paypal_radio = tk.Radiobutton(self.root, text="PayPal", variable=self.payment_var, value="paypal")
        paypal_radio.pack()

        google_pay_radio = tk.Radiobutton(self.root, text="Google Pay", variable=self.payment_var, value="google_pay")
        google_pay_radio.pack()

        confirm_payment_btn = tk.Button(self.root, text="Confirm Payment", command=self.confirm_payment)
        confirm_payment_btn.pack(pady=10)

    def confirm_payment(self):
        payment_method = self.payment_var.get()
        self.booking_data["payment_method"] = payment_method

        # Simulate booking confirmation
        booking_id = "B12345"
        self.show_booking_confirmation(booking_id)

    def show_booking_confirmation(self, booking_id):
        self.clear_screen()
        self.current_step = 6

        label = tk.Label(self.root, text="Booking Confirmation", font=("Arial", 20))
        label.pack(pady=20)

        details = f"""
        Booking ID: {booking_id}
        Departure: {self.booking_data["departure"]}
        Destination: {self.booking_data["destination"]}
        Payment Status: Success
        """
        details_label = tk.Label(self.root, text=details, justify=tk.LEFT)
        details_label.pack()

        new_booking_btn = tk.Button(self.root, text="New Booking", command=self.create_home_screen)
        new_booking_btn.pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_selections(self):
        self.departure_var.set("")
        self.destination_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = BusGoApp(root)
    root.mainloop()