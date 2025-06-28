import tkinter as tk
from tkinter import messagebox, simpledialog
import keyboard
import threading

mappings = {}
is_mapping_active = False

# Preset mappings list
presets = {
    "WASD to Arrows": {"w": "up", "a": "left", "s": "down", "d": "right"},
    "Invert Arrows": {"up": "down", "down": "up", "left": "right", "right": "left"},
    "Classic Vim": {"h": "left", "j": "down", "k": "up", "l": "right"}
}

# Function to add mapping
def add_mapping():
    from_key = from_entry.get().strip().lower()
    to_key = to_entry.get().strip().lower()

    if not from_key or not to_key:
        messagebox.showwarning("Input Error", "Both fields must be filled!")
        return

    if len(from_key) != 1 or len(to_key) != 1:
        messagebox.showwarning("Key Length", "Please enter only single character keys.")
        return

    if from_key == to_key:
        messagebox.showwarning("Invalid Mapping", "Cannot map a key to itself!")
        return

    if from_key in mappings:
        messagebox.showinfo("Duplicate", f"Key '{from_key}' is already mapped.")
        return

    mappings[from_key] = to_key
    mapping_list.insert(tk.END, f"{from_key.upper()} → {to_key.upper()}")
    from_entry.delete(0, tk.END)
    to_entry.delete(0, tk.END)

# Load preset mapping
def load_preset():
    selected = preset_var.get()
    if selected not in presets:
        return

    preset_map = presets[selected]
    for from_key, to_key in preset_map.items():
        if from_key not in mappings:
            mappings[from_key] = to_key
            mapping_list.insert(tk.END, f"{from_key.upper()} → {to_key.upper()}")

# Save current mappings as a new preset
def save_custom_preset():
    if not mappings:
        messagebox.showwarning("No Mappings", "There are no mappings to save!")
        return

    name = simpledialog.askstring("Save Preset", "Enter a name for your custom preset:")
    if name:
        if name in presets:
            overwrite = messagebox.askyesno("Overwrite?", f"Preset '{name}' already exists. Overwrite?")
            if not overwrite:
                return
        presets[name] = mappings.copy()
        preset_menu['menu'].add_command(label=name, command=tk._setit(preset_var, name))
        messagebox.showinfo("Preset Saved", f"Preset '{name}' saved successfully!")

# Start remapping
def start_mapping():
    global is_mapping_active
    if is_mapping_active:
        return

    if not mappings:
        messagebox.showinfo("No Mappings", "Please add at least one mapping before starting.")
        return

    try:
        for from_key, to_key in mappings.items():
            keyboard.remap_key(from_key, to_key)
        is_mapping_active = True
        status_label.config(text="Mapping Active (Press ESC to Stop)", fg="green")
        threading.Thread(target=wait_for_esc, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start mapping:\n{e}")

# Stop remapping
def stop_mapping():
    global is_mapping_active
    if not is_mapping_active:
        return

    keyboard.unhook_all()
    is_mapping_active = False
    status_label.config(text="Mapping Stopped", fg="red")

# Stop with ESC key
def wait_for_esc():
    keyboard.wait('esc')
    stop_mapping()

# GUI Setup
root = tk.Tk()
root.title("Python Key Mapper")
root.geometry("450x650")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

style_font = ("Segoe UI", 11)
label_fg = "#ffffff"
entry_bg = "#2e2e2e"
entry_fg = "#ffffff"
button_bg = "#3a3a3a"
button_fg = "#ffffff"

header = tk.Label(root, text="Key Mapping Utility", font=("Segoe UI", 16, "bold"), bg="#1e1e1e", fg="#00ffcc")
header.pack(pady=20)

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

tk.Label(frame, text="From Key:", font=style_font, bg="#1e1e1e", fg=label_fg).grid(row=0, column=0, padx=5, pady=5)
from_entry = tk.Entry(frame, width=10, font=style_font, bg=entry_bg, fg=entry_fg, insertbackground="white")
from_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="To Key:", font=style_font, bg="#1e1e1e", fg=label_fg).grid(row=1, column=0, padx=5, pady=5)
to_entry = tk.Entry(frame, width=10, font=style_font, bg=entry_bg, fg=entry_fg, insertbackground="white")
to_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = tk.Button(frame, text="➕ Add Mapping", command=add_mapping, font=style_font, bg="#0066cc", fg="white", activebackground="#005cbf")
add_button.grid(row=2, column=0, columnspan=2, pady=15)

# Preset dropdown
preset_frame = tk.Frame(root, bg="#1e1e1e")
preset_frame.pack(pady=10)

preset_var = tk.StringVar(root)
preset_var.set("Select Preset")
preset_menu = tk.OptionMenu(preset_frame, preset_var, *presets.keys())
preset_menu.config(font=style_font, bg=entry_bg, fg=entry_fg, width=20, highlightbackground="#1e1e1e")
preset_menu.pack(side=tk.LEFT, padx=5)

preset_button = tk.Button(preset_frame, text="📥 Load Preset", command=load_preset, font=style_font, bg="#555555", fg="white")
preset_button.pack(side=tk.LEFT, padx=5)

save_preset_button = tk.Button(preset_frame, text="💾 Save as Preset", command=save_custom_preset, font=style_font, bg="#777777", fg="white")
save_preset_button.pack(side=tk.LEFT, padx=5)

mapping_list = tk.Listbox(root, width=30, height=10, font=style_font, bg=entry_bg, fg=entry_fg, selectbackground="#00ffcc")
mapping_list.pack(pady=10)

start_button = tk.Button(root, text="▶ Start Mapping", command=start_mapping, font=style_font, bg="#4caf50", fg="white", width=20)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="⛔ Stop Mapping", command=stop_mapping, font=style_font, bg="#f44336", fg="white", width=20)
stop_button.pack(pady=5)

status_label = tk.Label(root, text="Mapping Inactive", font=style_font, bg="#1e1e1e", fg="gray")
status_label.pack(pady=15)

footer = tk.Label(root, text="Press ESC anytime to stop", font=("Segoe UI", 9), bg="#1e1e1e", fg="#555555")
footer.pack(pady=10)

root.mainloop()