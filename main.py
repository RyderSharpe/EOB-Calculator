import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

APP_TITLE = "EOB Helper Helper (µA·h)"
DEFAULT_TARGET_UAH = 100000.0  # Target in µA·h

def compute_remaining_and_stop(prev_uah, curr_screen_uah, target_uah):
    """
    total_so_far = prev + current
    remaining_to_add = target − total_so_far
    stop_at_screen   = target − prev   (independent of current)
    """
    total_so_far = prev_uah + curr_screen_uah
    remaining_to_add = target_uah - total_so_far
    stop_at_screen = target_uah - prev_uah
    return total_so_far, remaining_to_add, stop_at_screen

class BeamDoseApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.master.title(APP_TITLE)
        self.master.minsize(145, 360)
        self.grid(sticky="nsew")
        self.create_widgets()
        self.bind_events()
        self.update_clock()

    def create_widgets(self):
        header = ttk.Label(self, text="Doses in µA·h, on-target beam current in µA.\nLogic: total = previous + screen.",
                           font=("", 10, "italic"))
        header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,8))

        # Inputs
        ttk.Label(self, text="Previous dose (µA·h):").grid(row=1, column=0, sticky="w")
        self.previous_var = tk.StringVar(value="0")
        ttk.Entry(self, textvariable=self.previous_var).grid(row=1, column=1, sticky="ew")

        ttk.Label(self, text="Current screen (µA·h):").grid(row=2, column=0, sticky="w")
        self.current_var = tk.StringVar(value="0")
        ttk.Entry(self, textvariable=self.current_var).grid(row=2, column=1, sticky="ew")

        ttk.Label(self, text="Target total (µA·h):").grid(row=3, column=0, sticky="w")
        self.target_var = tk.StringVar(value=str(DEFAULT_TARGET_UAH))
        ttk.Entry(self, textvariable=self.target_var).grid(row=3, column=1, sticky="ew")

        ttk.Label(self, text="On-target current (µA):").grid(row=4, column=0, sticky="w")
        self.beam_current_var = tk.StringVar(value="150")
        ttk.Entry(self, textvariable=self.beam_current_var).grid(row=4, column=1, sticky="ew")

        # Buttons
        ttk.Button(self, text="Calculate", command=self.on_calculate).grid(row=5, column=0, sticky="ew", pady=6)
        ttk.Button(self, text="Clear", command=self.on_clear).grid(row=5, column=1, sticky="ew", pady=6)

        ttk.Separator(self, orient="horizontal").grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)

        # Outputs
        ttk.Label(self, text="Total so far (prev + screen):").grid(row=7, column=0, sticky="w")
        self.total_value = ttk.Label(self, text="—")
        self.total_value.grid(row=7, column=1, sticky="w")

        ttk.Label(self, text="Remaining to add:").grid(row=8, column=0, sticky="w")
        self.remaining_value = ttk.Label(self, text="—")
        self.remaining_value.grid(row=8, column=1, sticky="w")

        ttk.Label(self, text="Stop when screen reaches:").grid(row=9, column=0, sticky="w")
        self.stopat_value = ttk.Label(self, text="—", font=("", 12, "bold"))
        self.stopat_value.grid(row=9, column=1, sticky="w")

        ttk.Label(self, text="Current time:").grid(row=10, column=0, sticky="w")
        self.clock_value = ttk.Label(self, text="—")
        self.clock_value.grid(row=10, column=1, sticky="w")

        ttk.Label(self, text="Estimated EOB:").grid(row=11, column=0, sticky="w")
        self.eob_value = ttk.Label(self, text="—", font=("", 11, "bold"))
        self.eob_value.grid(row=11, column=1, sticky="w")

        # Status / sanity check
        self.status = ttk.Label(self, text="", foreground="gray")
        self.status.grid(row=12, column=0, columnspan=2, sticky="w", pady=(12,0))

        self.sanity = ttk.Label(self, text="", foreground="gray")
        self.sanity.grid(row=13, column=0, columnspan=2, sticky="w", pady=(6,0))

    def bind_events(self):
        self.master.bind("<Return>", lambda e: self.on_calculate())
        self.master.bind("<Escape>", lambda e: self.on_clear())

    def parse_float(self, s): return float(s.strip().replace(",", ""))

    def on_clear(self):
        self.previous_var.set("0")
        self.current_var.set("0")
        self.target_var.set(str(DEFAULT_TARGET_UAH))
        self.beam_current_var.set("150")
        self.total_value.config(text="—")
        self.remaining_value.config(text="—")
        self.stopat_value.config(text="—")
        self.eob_value.config(text="—")
        self.status.config(text="")
        self.sanity.config(text="")

    def on_calculate(self):
        try:
            prev = self.parse_float(self.previous_var.get())
            curr = self.parse_float(self.current_var.get())
            target = self.parse_float(self.target_var.get())
            beam = self.parse_float(self.beam_current_var.get())

            total, remaining, stopat = compute_remaining_and_stop(prev, curr, target)
            self.total_value.config(text=f"{total:.1f}")

            if remaining <= 0:
                self.remaining_value.config(text="0 (target met)")
                self.stopat_value.config(text=f"{stopat:.1f}")
                self.eob_value.config(text="Already reached")
                self.status.config(text=f"Target hit: {total:.1f} ≥ {target:.1f}")
            else:
                self.remaining_value.config(text=f"{remaining:.1f}")
                self.stopat_value.config(text=f"{stopat:.1f}")
                if beam > 0:
                    hours_needed = remaining / beam
                    eob_time = datetime.now() + timedelta(hours=hours_needed)
                    self.eob_value.config(text=eob_time.strftime("%Y-%m-%d @ %H:%M"))
                    self.status.config(text=f"~{hours_needed:.2f} h at {beam:.0f} µA")
                else:
                    self.eob_value.config(text="—")
                    self.status.config(text="Enter beam current")

            self.sanity.config(text=f"stop = target − previous = {target:.1f} − {prev:.1f} = {stopat:.1f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_clock(self):
        self.clock_value.config(text=datetime.now().strftime("%Y-%m-%d @ %H:%M"))
        self.master.after(30000, self.update_clock)

def main():
    root = tk.Tk()
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    BeamDoseApp(root)
    # root.geometry("420x180")
    root.mainloop()

if __name__ == "__main__":
    main()
