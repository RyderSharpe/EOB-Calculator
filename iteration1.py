import tkinter as tk

# Function that calculates EOB
def calculate():
    previous_dose = float(prev_entry.get())     # get value from entry, convert to float
    current_dose = float(curr_entry.get())
    maximum_dose = float(target_entry.get())
    current = float(current_entry.get())

    current_total = previous_dose + current_dose
    remaining = maximum_dose - current_total
    hours = remaining / current
    result_lbl.config(text=f"EOB in {hours:.3f} h")

# Build GUI
root = tk.Tk()
root.title("Simple EOB Calculator")

# Previous dose
tk.Label(root, text="Previous dose:").grid(row=0, column=0)
prev_entry = tk.Entry(root)
prev_entry.grid(row=0, column=1)
prev_entry.insert(0, 0)

# Current dose
tk.Label(root, text="Current dose:").grid(row=1, column=0)
curr_entry = tk.Entry(root)
curr_entry.grid(row=1, column=1)
curr_entry.insert(0, 0)


# Target Total
tk.Label(root, text="Target total:").grid(row=2, column=0)
target_entry = tk.Entry(root)
target_entry.grid(row=2, column=1)
target_entry.insert(0, "100000")

# Current on Target
tk.Label(root, text="Beam current (µA):").grid(row=3, column=0)
current_entry = tk.Entry(root)
current_entry.grid(row=3, column=1)
current_entry.insert(0, "300")

# Calculate button
calc_btn = tk.Button(root, text="Calculate", command=calculate)
calc_btn.grid(row=4, column=0, columnspan=2)

# Result label
result_lbl = tk.Label(root, text="Result will appear here")
result_lbl.grid(row=5, column=0, columnspan=2)

# Start app
root.mainloop()
