import customtkinter as ctk
import crypto_price as cp

# We will ignore default themes and apply our own professional color palette.
ctk.set_appearance_mode("Dark")

class MyGui:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Crypto -> Fiat Converter")
        self.root.geometry("450x720")
        self.root.resizable(False, False)

        # Base background: Pure Black
        self.root.configure(fg_color="#010409")

        # Top Title Label
        self.title_label = ctk.CTkLabel(
            self.root,
            text="CRYPTO -> FIAT CONVERTER",
            text_color="#FF9900",
            font=("Consolas", 28, "bold"),
        )
        self.title_label.pack(padx=20, pady=(40, 10))

        # Main layout frame (The "Card")
        self.frame = ctk.CTkFrame(
            self.root,
            fg_color="#0D0D0D",
            corner_radius=20,
            border_width=1,
            border_color="#262626"
        )
        self.frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Content inside the card
        # Crypto input
        self.cryp_label = ctk.CTkLabel(
            self.frame,
            text="Cryptocurrency",
            text_color="#A3A3A3",
            font=("Segoe UI", 14, "bold")
        )
        self.cryp_label.pack(anchor="w", padx=30, pady=(30, 5))

        self.choice = ctk.CTkEntry(
            self.frame,
            placeholder_text="e.g. bitcoin (no shortcodes)",
            height=45,
            corner_radius=10,
            fg_color="#000000",
            border_color="#262626",
            border_width=1,
            text_color="#FFFFFF",
            font=("Segoe UI", 14)
        )
        self.choice.pack(fill="x", padx=30, pady=(0, 20))

        # Amount input
        self.amt_label = ctk.CTkLabel(
            self.frame,
            text="Amount",
            text_color="#A3A3A3",
            font=("Segoe UI", 14, "bold")
        )
        self.amt_label.pack(anchor="w", padx=30, pady=(0, 5))

        self.amount = ctk.CTkEntry(
            self.frame,
            placeholder_text="e.g. 1.5",
            height=45,
            corner_radius=10,
            fg_color="#000000",
            border_color="#262626",
            border_width=1,
            text_color="#FFFFFF",
            font=("Segoe UI", 14)
        )
        self.amount.pack(fill="x", padx=30, pady=(0, 20))

        # Currency selection
        self.currency_label = ctk.CTkLabel(
            self.frame,
            text="Target Currency",
            text_color="#A3A3A3",
            font=("Segoe UI", 14, "bold")
        )
        self.currency_label.pack(anchor="w", padx=30, pady=(0, 10))

        self.selected_value = ctk.IntVar(value=1)

        self.radio_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.radio_frame.pack(fill="x", padx=30, pady=(0, 30))

        # Grid configure for radios to be evenly spaced
        self.radio_frame.columnconfigure((0,1), weight=1)
        self.radio_currency()

        # Modern conversion button
        self.button = ctk.CTkButton(
            self.frame,
            height=50,
            text="Convert",
            command=self.get_amount,
            font=("Segoe UI", 16, "bold"),
            text_color="#000000",
            fg_color="#FF9900",
            hover_color="#E68A00",
            corner_radius=12
        )
        self.button.pack(fill="x", padx=30, pady=(0, 30))

        # Result Textbox
        self.result_textbox = ctk.CTkTextbox(
            self.frame,
            height=70,
            corner_radius=10,
            fg_color="#000000",
            border_color="#262626",
            border_width=1,
            text_color="#22C55E",
            font=("Segoe UI", 16, "bold"),
            state="disabled"
        )
        self.result_textbox.pack(fill="x", padx=30, pady=(0, 20))

        # Bind the Enter key to the convert action
        self.root.bind('<Return>', self.get_amount)

        self.root.mainloop()

    def radio_currency(self):
        radio_style = {
            "font": ("Segoe UI", 13, "bold"),
            "text_color": "#FFFFFF",
            "border_color": "#333333",
            "border_width_checked": 6,
            "border_width_unchecked": 2,
            "fg_color": "#FF9900",  # Active inner color
            "hover_color": "#E68A00"
        }

        self.r_usd = ctk.CTkRadioButton(self.radio_frame, text="USD ($)", variable=self.selected_value, value=1, **radio_style)
        self.r_usd.grid(row=0, column=0, sticky="w", pady=10)

        self.r_ngn = ctk.CTkRadioButton(self.radio_frame, text="NGN (₦)", variable=self.selected_value, value=2, **radio_style)
        self.r_ngn.grid(row=0, column=1, sticky="w", pady=10)

        self.r_eur = ctk.CTkRadioButton(self.radio_frame, text="EUR (€)", variable=self.selected_value, value=3, **radio_style)
        self.r_eur.grid(row=1, column=0, sticky="w", pady=10)

        self.r_gbp = ctk.CTkRadioButton(self.radio_frame, text="GBP (£)", variable=self.selected_value, value=4, **radio_style)
        self.r_gbp.grid(row=1, column=1, sticky="w", pady=10)

    def show_result(self, text, is_error=False):
        font_size = 16
        text_color = "#EF4444" if is_error else "#22C55E"  # Red for errors, Green for success
        
        self.result_textbox.configure(state="normal", font=("Segoe UI", font_size, "bold"), text_color=text_color)
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", text)
        self.result_textbox.configure(state="disabled")

    def get_amount(self, event=None):
        # Visual feedback for button click
        original_text = self.button.cget("text")
        original_color = self.button.cget("fg_color")
        self.button.configure(text="Converting...", fg_color="#CC7A00")
        self.root.update()

        try:
            crypto_token = self.choice.get().lower().strip()
            amount_input = self.amount.get().strip()

            if not crypto_token or not amount_input:
                raise ValueError("Empty Fields")
                

            # Using float to allow inputs like "0.5" Bitcoin
            crypto_amount = float(amount_input)
            currency_selection = self.selected_value.get()

            result_text = ""
            if currency_selection == 1:
                usd_amount = cp.get_price(crypto_token, crypto_amount)
                result_text = f"${usd_amount}"

            elif currency_selection == 2:
                ngn_amount = cp.get_price(crypto_token, crypto_amount, "NGN")
                result_text = f"₦{ngn_amount}"

            elif currency_selection == 3:
                eur_amount = cp.get_price(crypto_token, crypto_amount, "EUR")
                result_text = f"€{eur_amount}"

            elif currency_selection == 4:
                gbp_amount = cp.get_price(crypto_token, crypto_amount, "GBP")
                result_text = f"£{gbp_amount}"

            self.show_result(f"Conversion Result:\n{result_text}")

        except ValueError:
            self.show_result("Error: Please ensure fields are filled \n          with actual values.", is_error=True)
            print("Empty or invalid input")
        except KeyError:  # cant find crypto with said api
            self.show_result("Error: Invalid cryptocurrency. \nEnsure it is spelled correctly.", is_error=True)
        except Exception as e:
            self.show_result(f"Error: {str(e)}", is_error=True)
        finally:
            # Restore the original button state
            self.button.configure(text=original_text, fg_color=original_color)

if __name__ == "__main__":
    MyGui()
