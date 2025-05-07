import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
from PIL import Image, ImageTk , ImageDraw
import requests

class WardrobeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wardrobe Manager Pro")
        self.root.geometry("1200x800")
        self.root.config(bg="#F0F0F0")

        # Custom Fonts
        self.title_font = ("Segoe UI", 28, "bold")
        self.button_font = ("Segoe UI", 12)
        self.label_font = ("Segoe UI", 11)
        self.dashboard_font = ("Segoe UI", 16, "bold")
        
        # Main Container Frame
        self.main_frame = tk.Frame(root, bg="#F0F0F0")
        self.main_frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)
        # Initialize database connection FIRST
        self.conn = sqlite3.connect('wardrobe.db')
        self.cursor = self.conn.cursor()
        
        # THEN call db_setup
        self.db_setup() 

        # Header Section
        self.header_frame = tk.Frame(self.main_frame, bg="#F0F0F0")
        self.header_frame.pack(fill=tk.X)
        
        tk.Label(self.header_frame, text="👔 Wardrobe Manager Pro", 
                font=self.title_font, bg="#F0F0F0", fg="#2C3E50").pack(pady=20)

        # Button Grid Section
        self.button_grid = tk.Frame(self.main_frame, bg="#F0F0F0")
        self.button_grid.pack(pady=20)

        self.trending_colors = ["sage_green", "lavender", "cream_white"]
        self.trending_fabrics = ["linen", "organic_cotton"]
        self.color_palettes = {
            "navy": ["white", "gray", "pink"],
            "white": ["black", "blue", "red"],
            "black": ["gold", "silver", "red"]
        
        }
        
        # Button Configuration
        buttons = [
            ("Add New Item", self.add_item, "#27AE60", "add_icon.png", 0, 0),
            ("View Inventory", self.show_items, "#2980B9", "show_icon.png", 0, 1),
            ("Generate Schedule", self.schedulize, "#F39C12", "schedule_icon.png", 0, 2),
            ("View Schedule", self.open_schedule_page, "#8E44AD", "open_icon.png", 1, 0),
            ("Advanced Search", self.search_items, "#3498DB", "search_icon.png", 1, 1),
            ("Backup Data", self.backup_data, "#7F8C8D", "backup_icon.png", 1, 2),
            ("Wardrobe Analytics", self.open_dashboard, "#2C3E50", "dashboard_icon.png", 2, 0),
            ("Weather Suggestions", self.weather_suggestions, "#1ABC9C", "weather_icon.png", 2, 1),
            ("Exit Application", self.root.quit, "#E74C3C", "exit_icon.png", 2, 2)
        ]

        # Create buttons in grid
        for text, command, color, icon, row, col in buttons:
            btn = self.create_modern_button(text, command, color, icon)
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        # Configure grid columns
        for i in range(3):
            self.button_grid.columnconfigure(i, weight=1, uniform="btn_group")
            self.button_grid.rowconfigure(i, weight=1, uniform="btn_group")

    
        # Initialize database connection FIRST
        self.conn = sqlite3.connect('wardrobe.db')
        self.cursor = self.conn.cursor()
        
        # THEN call db_setup
        self.db_setup()

        # Weather API
        self.weather_api_key = "ed3fd15a9b81d0193b1722f486de6243"

    def create_modern_button(self, text, command, bg_color, icon_path):
        """Create modern flat-style buttons with icons"""
        frame = tk.Frame(self.button_grid, bg="#F0F0F0")
        
        try:
            img = Image.open(icon_path)
            img = img.resize((24, 24), Image.LANCZOS)
            icon = ImageTk.PhotoImage(img)
        except:
            icon = None

        btn = tk.Button(frame,
                      text=text,
                      command=command,
                      image=icon,
                      compound=tk.LEFT,
                      font=self.button_font,
                      bg=bg_color,
                      fg="white",
                      bd=0,
                      padx=20,
                      pady=12,
                      activebackground=self.darken_color(bg_color))
        btn.image = icon
        btn.pack(fill=tk.BOTH, expand=True)
        
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.darken_color(bg_color)))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=bg_color))
        
        return frame

    def darken_color(self, color, factor=0.2):
        hex_color = color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker = [max(0, int(c * (1 - factor))) for c in rgb]
        return f'#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}'

    def db_setup(self):      
        try:
            # Create items table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    item_type TEXT NOT NULL,
                    color TEXT NOT NULL,
                    fabric TEXT NOT NULL,
                    wear_count INTEGER DEFAULT 0,
                    rating REAL DEFAULT 0,
                    UNIQUE(name, item_type, color, fabric)
                )
            ''')

            # Create schedule table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS schedule (
                    id INTEGER PRIMARY KEY,
                    day TEXT NOT NULL,
                    shirt TEXT,
                    pant TEXT,
                    shoes TEXT
                )
            ''')

            self.conn.commit()
            print("Database tables initialized successfully")
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")
        except Exception as e:
            print(f"General error: {e}")

    def add_item(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Item")
        add_window.geometry("400x450")
        add_window.config(bg="#FFFFFF")

        # Updated type options
        type_groups = {
            'Top Wear': ['Shirt', 'T-shirt', 'Kurti', 'Kurta'],
            'Bottom Wear': ['Pant', 'Trouser', 'Skirt', 'Leggings'],
            'Footwear': ['Shoes', 'Slipper', 'Sandals']
        }

        # Category selection
        tk.Label(add_window, text="Category:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        category = ttk.Combobox(add_window, values=list(type_groups.keys()), font=self.label_font)
        category.pack(pady=5)
        category.current(0)

        # Specific type selection
        tk.Label(add_window, text="Specific Type:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        type_combo = ttk.Combobox(add_window, font=self.label_font)
        type_combo.pack(pady=5)

        # Update specific types based on selected category
        def update_types(event=None):
            selected_category = category.get()
            type_combo['values'] = type_groups[selected_category]
            type_combo.current(0)

        category.bind("<<ComboboxSelected>>", update_types)
        update_types()  # Initialize the types

        # Name
        tk.Label(add_window, text="Enter Name:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        name_entry = tk.Entry(add_window, font=self.label_font)
        name_entry.pack(pady=5)

        # Color
        tk.Label(add_window, text="Select Color:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        colors = ["Red", "Blue", "Green", "Yellow", "Black", "White", "Pink", "Gray", "Orange", "Brown", "Purple", "Cyan"]
        color_select = ttk.Combobox(add_window, values=colors, font=self.label_font)
        color_select.pack(pady=5)
        color_select.current(0)

        # Fabric
        tk.Label(add_window, text="Select Fabric:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        fabrics = [
            'Cotton', 'Silk', 'Linen', 'Wool', 'Jute','Denim', 'Hemp', 'Khadi',
            'Chanderi', 'Tussar Silk', 'Eri Silk', 'Pashmina', 'Mulmul',
            'Banarasi Brocade', 'Kanjivaram Silk', 'Maheshwari', 'Polyester',
            'Nylon', 'Rayon (Viscose)', 'Acrylic', 'Lycra (Spandex)',
            'Poly-Cotton', 'Silk-Cotton', 'Wool-Silk Blend', 'Rayon-Cotton Blend',
            'Kota Doria', 'Ikat', 'Bandhani', 'Ajrakh', 'Dhabu', 'Mashru'
        ]
        fabric_select = ttk.Combobox(add_window, values=fabrics, font=self.label_font)
        fabric_select.pack(pady=5)
        fabric_select.current(0)

        # Save button
        def save_item():
            name = name_entry.get()
            item_type = type_combo.get()
            color = color_select.get()
            fabric = fabric_select.get()

            if not name:
                messagebox.showwarning("Warning", "Name cannot be empty.")
                return
            if not item_type:
                messagebox.showwarning("Warning", "Please select a specific type.")
                return

            try:
                self.cursor.execute("INSERT INTO items (name, item_type, color, fabric) VALUES (?, ?, ?, ?)",
                                (name, item_type, color, fabric))
                self.conn.commit()
                messagebox.showinfo("Success", f"{name} added successfully!")
                add_window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showwarning("Warning", 
                    "An item with this combination (name + type + color + fabric) already exists.")

        save_button = tk.Button(
            add_window,
            text="Save Item",
            command=save_item,
            font=self.button_font,
            bg="#4CAF50",
            fg="white",
            bd=0,
            padx=20,
            pady=12
        )
        save_button.pack(pady=20)
    def show_items(self):
        """Show items with fabric column and average rating."""
        items_window = tk.Toplevel(self.root)
        items_window.title("All Items")
        items_window.geometry("1100x600")
        items_window.config(bg="#FFFFFF")

        tree = ttk.Treeview(items_window, columns=("ID", "Name", "Type", "Color", "Fabric", "Wear Count", "Rating"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Type", text="Type")
        tree.heading("Color", text="Color")
        tree.heading("Fabric", text="Fabric")
        tree.heading("Wear Count", text="Wear Count")
        tree.heading("Rating", text="Rating")
        for col in ["ID", "Name", "Type", "Color", "Fabric", "Wear Count", "Rating"]:
            tree.column(col, anchor=tk.CENTER, width=120)
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.cursor.execute("SELECT * FROM items")
        for row in self.cursor.fetchall():
            tree.insert("", tk.END, values=row)

        def edit_item():
            selected = tree.focus()
            if selected:
                item_id = tree.item(selected)['values'][0]
                self.edit_item_window(item_id)
            else:
                messagebox.showwarning("Warning", "Select an item to edit.")

        def delete_item():
            selected = tree.focus()
            if selected:
                item_id = tree.item(selected)['values'][0]
                self.cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
                self.conn.commit()
                tree.delete(selected)
                messagebox.showinfo("Deleted", "Item deleted successfully!")
            else:
                messagebox.showwarning("Warning", "Select an item to delete.")

        edit_button = tk.Button(items_window, text="Edit Item", command=edit_item, 
                              font=self.button_font, bg="#2196F3", fg="white", bd=0)
        edit_button.pack(pady=10)
        delete_button = tk.Button(items_window, text="Delete Item", command=delete_item, 
                                font=self.button_font, bg="#F44336", fg="white", bd=0)
        delete_button.pack(pady=10)

    def edit_item_window(self, item_id):
        """Edit window with fabric selection"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Item")
        edit_window.geometry("400x450")
        edit_window.config(bg="#FFFFFF")

        self.cursor.execute("SELECT * FROM items WHERE id=?", (item_id,))
        item = self.cursor.fetchone()

        # Type
        tk.Label(edit_window, text="Select Type:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        item_type = ttk.Combobox(edit_window, values=["Shirt", "Pant", "Shoes"], font=self.label_font)
        item_type.pack(pady=5)
        item_type.set(item[2])

        # Name
        tk.Label(edit_window, text="Enter Name:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        name_entry = tk.Entry(edit_window, font=self.label_font)
        name_entry.pack(pady=5)
        name_entry.insert(0, item[1])

        # Color
        tk.Label(edit_window, text="Select Color:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        colors = ["Red", "Blue", "Green", "Yellow", "Black", "White", "Pink", "Gray", "Orange", "Brown", "Purple", "Cyan"]
        color_select = ttk.Combobox(edit_window, values=colors, font=self.label_font)
        color_select.pack(pady=5)
        color_select.set(item[3])

        # Fabric
        tk.Label(edit_window, text="Select Fabric:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        fabrics = [
            'Cotton', 'Silk', 'Linen', 'Wool', 'Jute', 'Hemp', 'Khadi',
            'Chanderi', 'Tussar Silk', 'Eri Silk', 'Pashmina', 'Mulmul',
            'Banarasi Brocade', 'Kanjivaram Silk', 'Maheshwari', 'Polyester',
            'Nylon', 'Rayon (Viscose)', 'Acrylic', 'Lycra (Spandex)',
            'Poly-Cotton', 'Silk-Cotton', 'Wool-Silk Blend', 'Rayon-Cotton Blend',
            'Kota Doria', 'Ikat', 'Bandhani', 'Ajrakh', 'Dhabu', 'Mashru'
        ]
        fabric_select = ttk.Combobox(edit_window, values=fabrics, font=self.label_font)
        fabric_select.pack(pady=5)
        fabric_select.set(item[4])

        def save_edited_item():
            name = name_entry.get()
            item_type_val = item_type.get()
            color = color_select.get()
            fabric = fabric_select.get()
            if name:
                self.cursor.execute("UPDATE items SET name=?, item_type=?, color=?, fabric=? WHERE id=?", 
                                  (name, item_type_val, color, fabric, item_id))
                self.conn.commit()
                messagebox.showinfo("Success", f"{name} updated successfully!")
                edit_window.destroy()
            else:
                messagebox.showwarning("Warning", "Name cannot be empty.")

        save_button = tk.Button(edit_window, text="Save Changes", command=save_edited_item, 
                              font=self.button_font, bg="#4CAF50", fg="white", bd=0)
        save_button.pack(pady=20)

    def schedulize(self):
        """Generate a 7-day schedule using a smart algorithm."""
        try:
            print("Fetching items from the database...")
            self.cursor.execute("SELECT * FROM items")
            items = [self.Item(*row) for row in self.cursor.fetchall()]
            print(f"Found {len(items)} items in the database.")

            if len(items) < 7:
                messagebox.showwarning("Warning", "You need at least 7 items to generate a schedule.")
                return

            # Categorize items into tops, bottoms, and footwear
            tops = [item for item in items if item.item_type in ["Shirt", "T-shirt", "Kurti", "Kurta"]]
            bottoms = [item for item in items if item.item_type in ["Pant", "Trouser", "Skirt", "Leggings"]]
            footwear = [item for item in items if item.item_type in ["Shoes", "Slipper", "Sandals"]]

            print(f"Tops: {len(tops)}, Bottoms: {len(bottoms)}, Footwear: {len(footwear)}")

            if len(tops) < 7 or len(bottoms) < 7 or len(footwear) < 7:
                messagebox.showwarning("Warning", "You need at least 7 tops, 7 bottoms, and 7 footwear items to generate a schedule.")
                return

            # Generate all possible outfits
            print("Generating outfits...")
            outfits = self.generate_outfits(tops, bottoms, footwear)
            print(f"Generated {len(outfits)} possible outfits.")

            if len(outfits) < 7:
                messagebox.showwarning("Warning", "Not enough compatible outfits found.")
                return

            # Generate a 7-day schedule
            print("Generating 7-day schedule...")
            schedule = self.generate_7day_schedule(outfits)
            print("Schedule generated successfully.")

            # Save the schedule to the database
            print("Saving schedule to the database...")
            self.save_schedule_to_db(schedule)
            print("Schedule saved to the database.")

            # Show success message
            messagebox.showinfo("Success", "Smart schedule generated successfully!")
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"Failed to generate schedule: {e}")

    def generate_outfits(self, tops, bottoms, footwear):
        """Generate all possible outfits with scores."""
        outfits = []
        for top in tops:
            for bottom in bottoms:
                if self.are_compatible(top, bottom):
                    for shoe in footwear:
                        if self.matches_formality(shoe, top, bottom):
                            score = self.calculate_outfit_score(top, bottom, shoe)
                            outfits.append((score, (top, bottom, shoe)))
                        else:
                            print(f"Formality mismatch: {top.name} + {bottom.name} + {shoe.name}")
                    else:
                        print(f"Footwear not compatible: {top.name} + {bottom.name}")
                else:
                    print(f"Top and bottom not compatible: {top.name} + {bottom.name}")
        return sorted(outfits, key=lambda x: -x[0])  # Sort by score (highest first)

    def are_compatible(self, top, bottom):
        """Check if top and bottom are compatible based on color and fabric."""
        color_score = self.get_color_score(top.color, bottom.color)
        fabric_score = self.get_fabric_score(top.fabric, bottom.fabric)
        return color_score > 0.2 and fabric_score > 0.2  # Relaxed thresholds
    def get_color_score(self, top_color, bottom_color):
        """Score color compatibility."""
        if top_color == bottom_color:
            return 0.5  # Matching colors are okay but not ideal
        return 1 if bottom_color in self.color_palettes.get(top_color, []) else 0.5  # More lenient  
    def get_fabric_score(self, top_fabric, bottom_fabric):
        """Score fabric compatibility."""
        # Allow most combinations except extreme mismatches
        heavy_fabrics = ["wool", "denim"]
        light_fabrics = ["silk", "linen"]
        if top_fabric in heavy_fabrics and bottom_fabric in light_fabrics:
            return 0.3  # Allow some mismatches
        return 1

    def matches_formality(self, shoe, top, bottom):
        # Example: Formal shoes with formal tops/bottoms
        formal_items = ["Shirt", "Kurta", "Pant", "Trouser"]
        if shoe.item_type == "Shoes":
            return top.item_type in formal_items and bottom.item_type in formal_items
        return True

    def calculate_outfit_score(self, top, bottom, shoe):
        color_score = self.get_color_score(top.color, bottom.color)
        fabric_score = self.get_fabric_score(top.fabric, bottom.fabric)
        trend_score = self.get_trend_score(top) + self.get_trend_score(bottom) + self.get_trend_score(shoe)
        rating_score = (top.rating + bottom.rating + shoe.rating) / 3
        return (color_score * 0.4 + fabric_score * 0.3 + trend_score * 0.2 + rating_score * 0.1)

    def get_trend_score(self, item):
        score = 0
        if item.color in self.trending_colors: score += 0.5
        if item.fabric in self.trending_fabrics: score += 0.5
        return score

    def generate_7day_schedule(self, outfits):
        schedule = []
        used_items = set()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for day in days:
            for outfit in outfits:
                score, (top, bottom, shoe) = outfit
                if (top.id not in used_items and 
                    bottom.id not in used_items and 
                    shoe.id not in used_items):
                    schedule.append((day, (top, bottom, shoe)))
                    used_items.update({top.id, bottom.id, shoe.id})
                    print(f"Assigned {day}: {top.name}, {bottom.name}, {shoe.name}")  
                    break  
            else:
                
                schedule.append((day, (None, None, None)))
                print(f"No outfit assigned for {day}") 

        return schedule
    def save_schedule_to_db(self, schedule):
        try:
            # Clear existing schedule
            self.cursor.execute("DELETE FROM schedule")
            self.conn.commit()

            # Insert new schedule
            for day, (top, bottom, shoe) in schedule:
                if top and bottom and shoe:  # Only insert valid outfits
                    self.cursor.execute('''
                        INSERT INTO schedule (day, shirt, pant, shoes)
                        VALUES (?, ?, ?, ?)
                    ''', (day, top.name, bottom.name, shoe.name))
            
            self.conn.commit()
            print("Schedule saved to the database.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", f"Failed to save schedule: {e}")

    # Define a simple Item class for easier handling
    class Item:
        def __init__(self, id, name, item_type, color, fabric, wear_count, rating):
            self.id = id
            self.name = name
            self.item_type = item_type
            self.color = color
            self.fabric = fabric
            self.wear_count = wear_count
            self.rating = rating

    def open_schedule_page(self):
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Weekly Wardrobe Schedule")
        schedule_window.geometry("1000x600")
        schedule_window.config(bg="#FFFFFF")

        tree = ttk.Treeview(
            schedule_window,
            columns=("Day", "Top Wear", "Bottom Wear", "Footwear"),
            show="headings"
        )
        tree.heading("Day", text="Day", anchor=tk.CENTER)
        tree.heading("Top Wear", text="Top Wear (Color)", anchor=tk.CENTER)
        tree.heading("Bottom Wear", text="Bottom Wear (Color)", anchor=tk.CENTER)
        tree.heading("Footwear", text="Footwear (Color)", anchor=tk.CENTER)

        # Set column widths
        tree.column("Day", width=150, anchor=tk.CENTER)
        tree.column("Top Wear", width=280, anchor=tk.CENTER)
        tree.column("Bottom Wear", width=280, anchor=tk.CENTER)
        tree.column("Footwear", width=280, anchor=tk.CENTER)

        # Pack the Treeview
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Fetch schedule data with color information
        self.cursor.execute('''
            SELECT s.day, 
                i1.name || ' (' || i1.color || ')', 
                i2.name || ' (' || i2.color || ')', 
                i3.name || ' (' || i3.color || ')'
            FROM schedule s
            LEFT JOIN items i1 ON s.shirt = i1.name
            LEFT JOIN items i2 ON s.pant = i2.name
            LEFT JOIN items i3 ON s.shoes = i3.name
            ORDER BY 
                CASE s.day
                    WHEN 'Monday' THEN 1
                    WHEN 'Tuesday' THEN 2
                    WHEN 'Wednesday' THEN 3
                    WHEN 'Thursday' THEN 4
                    WHEN 'Friday' THEN 5
                    WHEN 'Saturday' THEN 6
                    WHEN 'Sunday' THEN 7
                END
        ''')
        schedule_data = self.cursor.fetchall()

        # Insert data into the Treeview
        for row in schedule_data:
            tree.insert("", tk.END, values=row)

        # Add Preview Colors button
        preview_button = tk.Button(
            schedule_window,
            text="Preview Colors",
            command=lambda: self.show_color_preview(tree),  # Bind to the Treeview
            font=self.button_font,
            bg="#4CAF50",
            fg="white"
        )
        preview_button.pack(pady=10)
            # Add rate button
        def rate_selected_outfit():
            selected = tree.focus()
            if selected:
                values = tree.item(selected)['values']
                day, top, bottom, shoes = values
                # Extract item names without color
                top_name = top.split(' (')[0]
                bottom_name = bottom.split(' (')[0]
                shoes_name = shoes.split(' (')[0]
                self.rate_outfit_window(top_name, bottom_name, shoes_name)
            else:
                messagebox.showwarning("Warning", "Please select an outfit to rate.")

        rate_btn = tk.Button(
            schedule_window,
            text="Rate Outfit",
            command=rate_selected_outfit,
            font=self.button_font,
            bg="#FFA500",
            fg="white"
        )
        rate_btn.pack(side=tk.LEFT, padx=20, pady=10)

        # Add clear button
        clear_btn = tk.Button(
            schedule_window,
            text="Clear Schedule",
            command=self.clear_schedule,
            font=self.button_font,
            bg="#FF4444",
            fg="white"
        )
        clear_btn.pack(side=tk.RIGHT, padx=20, pady=10)
    def clear_schedule(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear the schedule?")
        if confirm:
            self.cursor.execute("DELETE FROM schedule")
            self.conn.commit()
            messagebox.showinfo("Success", "Schedule cleared successfully!")

    def backup_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                self.cursor.execute("SELECT * FROM items")
                for row in self.cursor.fetchall():
                    file.write(f"{row}\n")
            messagebox.showinfo("Success", f"Data exported to {file_path}")

    def delete_all_items(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete all items?")
        if confirm:
            self.cursor.execute("DELETE FROM items")
            self.conn.commit()
            messagebox.showinfo("Success", "All items deleted successfully!")

    def search_items(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Items")
        search_window.geometry("400x200")
        search_window.config(bg="#FFFFFF")

        tk.Label(search_window, text="Search by:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        search_type = ttk.Combobox(search_window, values=["Name", "Type", "Color"], font=self.label_font)
        search_type.pack(pady=5)
        search_type.current(0)

        tk.Label(search_window, text="Enter search term:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        search_entry = tk.Entry(search_window, font=self.label_font)
        search_entry.pack(pady=5)

        def perform_search():
            search_term = search_entry.get()
            search_by = search_type.get().lower()
            allowed_columns = {'name', 'item_type', 'color'}
            if search_by not in allowed_columns:
                messagebox.showwarning("Warning", "Invalid search type.")
                return
            self.cursor.execute(f"SELECT * FROM items WHERE {search_by} LIKE ?", (f"%{search_term}%",))
            results = self.cursor.fetchall()
            if results:
                self.show_search_results(results)
            else:
                messagebox.showinfo("No Results", "No items found matching your search.")

        search_button = tk.Button(search_window, text="Search", command=perform_search, font=self.button_font, bg="#00BCD4", fg="white", bd=0)
        search_button.pack(pady=10)

    def show_search_results(self, results):
        results_window = tk.Toplevel(self.root)
        results_window.title("Search Results")
        results_window.geometry("1200x600")
        results_window.config(bg="#FFFFFF")

        tree = ttk.Treeview(results_window, 
                        columns=("ID", "Name", "Type", "Color", "Fabric", "Wear Count", "Rating"), 
                        show="headings")
        
        # Correct column configuration
        columns = [
            ("ID", 80), ("Name", 200), ("Type", 150), 
            ("Color", 100), ("Fabric", 200), ("Wear Count", 100), ("Rating", 100)
        ]
        
        for col, width in columns:
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor=tk.CENTER)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        for row in results:
            tree.insert("", tk.END, values=row)

    def open_dashboard(self):
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("Wardrobe Analytics Dashboard")
        dashboard_window.geometry("1400x800")
        dashboard_window.config(bg="#FFFFFF")

        # Main container
        main_frame = tk.Frame(dashboard_window, bg="#FFFFFF")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Category statistics
        categories = {
            "Top Wear": ['Shirt', 'T-shirt', 'Kurti', 'Kurta'],
            "Bottom Wear": ['Pant', 'Trouser', 'Skirt', 'Leggings'],
            "Footwear": ['Shoes', 'Slipper', 'Sandals']
        }

        # Create category frames
        for idx, (category, types) in enumerate(categories.items()):
            frame = tk.Frame(main_frame, bg="#F8F9FA", bd=2, relief=tk.GROOVE)
            frame.grid(row=0, column=idx, padx=20, pady=20, sticky="nsew")
            
            # Category header
            tk.Label(frame, text=category, font=("Segoe UI", 14, "bold"), 
                    bg="#F8F9FA", fg="#2C3E50").pack(pady=10)
            
            # Get total items in category
            self.cursor.execute(f'''
                SELECT COUNT(*) FROM items 
                WHERE item_type IN ({','.join(['?']*len(types))})
            ''', types)
            total = self.cursor.fetchone()[0]
            tk.Label(frame, text=f"Total Items: {total}", 
                    font=("Segoe UI", 12), bg="#F8F9FA").pack()
            
            # Type breakdown
            type_frame = tk.Frame(frame, bg="#F8F9FA")
            type_frame.pack(pady=10)
            
            for t_idx, item_type in enumerate(types):
                self.cursor.execute("SELECT COUNT(*) FROM items WHERE item_type=?", (item_type,))
                count = self.cursor.fetchone()[0]
                
                tk.Label(type_frame, text=f"{item_type}: {count}", 
                        font=("Segoe UI", 10), bg="#F8F9FA", 
                        anchor="w").grid(row=t_idx, column=0, sticky="w", padx=10)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

        # Add other statistics below
        stats_frame = tk.Frame(main_frame, bg="#FFFFFF")
        stats_frame.grid(row=1, column=0, columnspan=3, pady=40)

        # Most Worn Item
        self.cursor.execute('''
            SELECT name, wear_count FROM items 
            ORDER BY wear_count DESC LIMIT 1
        ''')
        most_worn = self.cursor.fetchone()
        if most_worn:
            tk.Label(stats_frame, text=f"🌟 Most Worn: {most_worn[0]} ({most_worn[1]} wears)",
                    font=("Segoe UI", 12), bg="#FFFFFF").pack(side=tk.LEFT, padx=20)

        # Highest Rated Item
        self.cursor.execute('''
            SELECT name, rating FROM items 
            ORDER BY rating DESC LIMIT 1
        ''')
        top_rated = self.cursor.fetchone()
        if top_rated:
            tk.Label(stats_frame, text=f"⭐ Top Rated: {top_rated[0]} ({top_rated[1]}/5)",
                    font=("Segoe UI", 12), bg="#FFFFFF").pack(side=tk.LEFT, padx=20)
            
    def weather_suggestions(self):
        def get_user_location():
            """Prompt user for their city."""
            location_window = tk.Toplevel(self.root)
            location_window.title("Enter Your City")
            location_window.geometry("300x150")
            location_window.config(bg="#FFFFFF")

            tk.Label(location_window, text="Enter your city:", font=self.label_font, bg="#FFFFFF").pack(pady=10)
            city_entry = tk.Entry(location_window, font=self.label_font)
            city_entry.pack(pady=10)

            def submit_city():
                city = city_entry.get()
                if city:
                    location_window.city = city
                    location_window.destroy()
                else:
                    messagebox.showwarning("Warning", "City name cannot be empty.")

            submit_button = tk.Button(location_window, text="Submit", command=submit_city,
                                    font=self.button_font, bg="#4CAF50", fg="white")
            submit_button.pack(pady=10)

            location_window.wait_window()
            return getattr(location_window, 'city', None)

        city = get_user_location()
        if not city:
            return

        # Use OpenWeatherMap API
        api_key = "ed3fd15a9b81d0193b1722f486de6243"  # Replace with your actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()

            # Check if the API returned valid data
            if data.get("cod") != 200:
                error_message = data.get("message", "Unknown error")
                messagebox.showerror("Error", f"Failed to fetch weather data: {error_message}")
                return

            # Extract weather data
            weather_main = data['weather'][0]['main']
            weather_description = data['weather'][0]['description']
            temperature_kelvin = data['main']['temp']
            temperature_celsius = round(temperature_kelvin - 273.15, 1)  # Convert to Celsius
            temperature_fahrenheit = round((temperature_kelvin - 273.15) * 9/5 + 32, 1)  # Convert to Fahrenheit
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            cloudiness = data['clouds']['all']

            # Generate outfit suggestions based on weather conditions
            suggestion = self.generate_outfit_suggestion(
                temperature_celsius, weather_main, weather_description, humidity, wind_speed, cloudiness
            )

            # Display weather and suggestion
            message = (
                f"Weather in {city}:\n"
                f"Condition: {weather_main} ({weather_description})\n"
                f"Temperature: {temperature_celsius}°C / {temperature_fahrenheit}°F\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s\n"
                f"Cloudiness: {cloudiness}%\n\n"
                f"Suggestion: {suggestion}"
            )

            messagebox.showinfo("Weather Suggestion", message)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch weather data: {e}")
        except KeyError as e:
            messagebox.showerror("Error", f"Invalid data received from the API: {e}")

    def generate_outfit_suggestion(self, temperature, weather_main, weather_description, humidity, wind_speed, cloudiness):
        suggestion = []

        # Temperature-based suggestions
        if temperature < 0:
            suggestion.append("It's freezing! Wear a heavy winter coat, thermal layers, gloves, and a scarf.")
        elif temperature < 10:
            suggestion.append("It's cold! Wear a heavy jacket, sweater, and boots.")
        elif temperature < 20:
            suggestion.append("It's cool. Wear a light jacket, long-sleeve shirt, and jeans.")
        elif temperature < 30:
            suggestion.append("It's warm. Wear a t-shirt, shorts, and sneakers.")
        else:
            suggestion.append("It's hot! Wear light, breathable fabrics like cotton or linen.")

        # Weather condition-based suggestions
        if "rain" in weather_description.lower():
            suggestion.append("Don't forget to carry an umbrella or wear waterproof shoes.")
        if "snow" in weather_description.lower():
            suggestion.append("Wear insulated boots and a waterproof jacket.")
        if "clear" in weather_description.lower() and cloudiness < 20:
            suggestion.append("It's sunny! Wear sunglasses and apply sunscreen.")
        if wind_speed > 10:
            suggestion.append("It's windy! Wear a windbreaker or scarf to protect yourself.")

        # Humidity-based suggestions
        if humidity > 70:
            suggestion.append("It's humid. Wear moisture-wicking fabrics to stay comfortable.")
        elif humidity < 30:
            suggestion.append("It's dry. Stay hydrated and consider using moisturizer.")

        # Combine all suggestions into a single string
        return "\n".join(suggestion)
    def rate_outfit_window(self, shirt, pant, shoes):
        rate_window = tk.Toplevel(self.root)
        rate_window.title("Rate Outfit Components")
        rate_window.geometry("300x250")
        rate_window.config(bg="#FFFFFF")

        # Get individual item ratings
        tk.Label(rate_window, text=f"Rate {shirt} (Top):", font=self.label_font, bg="#FFFFFF").pack(pady=5)
        top_rating = ttk.Combobox(rate_window, values=[1, 2, 3, 4, 5], font=self.label_font)
        top_rating.pack(pady=5)
        top_rating.current(0)  # Default to 1

        tk.Label(rate_window, text=f"Rate {pant} (Bottom):", font=self.label_font, bg="#FFFFFF").pack(pady=5)
        bottom_rating = ttk.Combobox(rate_window, values=[1, 2, 3, 4, 5], font=self.label_font)
        bottom_rating.pack(pady=5)
        bottom_rating.current(0)  # Default to 1

        tk.Label(rate_window, text=f"Rate {shoes} (Footwear):", font=self.label_font, bg="#FFFFFF").pack(pady=5)
        shoe_rating = ttk.Combobox(rate_window, values=[1, 2, 3, 4, 5], font=self.label_font)
        shoe_rating.pack(pady=5)
        shoe_rating.current(0)  # Default to 1

        def save_ratings():
            try:
                # Update ratings for each item
                for item_name, rating in [
                    (shirt, top_rating.get()),
                    (pant, bottom_rating.get()),
                    (shoes, shoe_rating.get())
                ]:
                    self.cursor.execute('''
                        UPDATE items 
                        SET wear_count = wear_count + 1,
                            rating = (rating + ?) / 2 
                        WHERE name = ?
                    ''', (float(rating), item_name))
                self.conn.commit()
                messagebox.showinfo("Success", "Outfit rated successfully!")
                rate_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save ratings: {str(e)}")

        tk.Button(
            rate_window,
            text="Save Ratings",
            command=save_ratings,
            font=self.button_font,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=20)
                
    def rate_outfits(self):
        rate_window = tk.Toplevel(self.root)
        rate_window.title("Rate Outfits")
        rate_window.geometry("400x300")
        rate_window.config(bg="#FFFFFF")

        tk.Label(rate_window, text="Select Outfit:", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        self.cursor.execute("SELECT name FROM items")
        outfits = [row[0] for row in self.cursor.fetchall()]
        outfit_select = ttk.Combobox(rate_window, values=outfits, font=self.label_font)
        outfit_select.pack(pady=5)
        outfit_select.current(0)

        tk.Label(rate_window, text="Enter Rating (1-5):", font=self.label_font, bg="#FFFFFF", fg="#333333").pack(pady=5)
        rating_entry = tk.Entry(rate_window, font=self.label_font)
        rating_entry.pack(pady=5)

        def save_rating():
            outfit = outfit_select.get()
            rating = rating_entry.get()
            if not outfit or not rating:
                messagebox.showwarning("Warning", "Please select an outfit and enter a rating.")
                return
            try:
                rating = float(rating)
                if 1 <= rating <= 5:
                    self.cursor.execute("UPDATE items SET rating=? WHERE name=?", (rating, outfit))
                    self.conn.commit()
                    messagebox.showinfo("Success", f"Rating for {outfit} saved successfully!")
                    rate_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Rating must be between 1 and 5.")
            except ValueError:
                messagebox.showwarning("Warning", "Rating must be a number.")

        save_button = tk.Button(rate_window, text="Save Rating", command=save_rating, font=self.button_font, bg="#4CAF50", fg="white", bd=0)
        save_button.pack(pady=20)
    color_map = {
            "navy": "#001f3f", "blue": "#0074D9", "black": "#000000",
            "white": "#FFFFFF", "red": "#FF4136", "green": "#2ECC40",
            "yellow": "#FFDC00", "pink": "#F012BE", "gray": "#AAAAAA",
            "orange": "#FF851B", "brown": "#A52A2A", "purple": "#B10DC9",
            "cyan": "#7FDBFF", "sage green": "#9DC183", "cream white": "#FFFDD0",
            "nude": "#F3E5AB", "beige": "#F5F5DC", "maroon": "#800000",
            "teal": "#008080", "lavender": "#E6E6FA", "olive": "#808000",
            "mustard": "#FFDB58", "burgundy": "#800020", "coral": "#FF7F50",
            "indigo": "#4B0082", "turquoise": "#40E0D0", "gold": "#FFD700",
            "silver": "#C0C0C0"
        }


    def show_color_preview(self, tree):
        selected = tree.focus()
        if selected:
            values = tree.item(selected)['values']
            print(f"Selected Values: {values}")  
            if len(values) == 4:  
                day, top, bottom, shoes = values

                # Extract colors from the item names
                top_color = self.extract_color(top)
                bottom_color = self.extract_color(bottom)
                shoes_color = self.extract_color(shoes)

                # Debugging: Print extracted colors
                print(f"Top Color: {top_color}")
                print(f"Bottom Color: {bottom_color}")
                print(f"Shoes Color: {shoes_color}")

                # Generate and display the color palette
                palette = self.generate_color_palette(top_color, bottom_color, shoes_color)
                palette.show()  # Display the palette image
            else:
                messagebox.showwarning("Warning", "Invalid selection. Please select a valid outfit.")
        else:
            messagebox.showwarning("Warning", "Please select an outfit to preview colors.")

    def generate_color_palette(self, top_color, bottom_color, shoe_color):
        # Convert color names to hex codes
        top_hex = self.get_hex_color(top_color)
        bottom_hex = self.get_hex_color(bottom_color)
        shoe_hex = self.get_hex_color(shoe_color)

        # Define the size of the palette image
        width, height = 300, 100
        palette = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(palette)

        # Define rectangle sizes and positions
        rect_width = width // 3
        rect_height = height

        # Draw rectangles for each color
        draw.rectangle([0, 0, rect_width, rect_height], fill=top_hex)  # Top color
        draw.rectangle([rect_width, 0, 2 * rect_width, rect_height], fill=bottom_hex)  # Bottom color
        draw.rectangle([2 * rect_width, 0, 3 * rect_width, rect_height], fill=shoe_hex)  # Shoe color

        # Save the image to a file and open it
        palette.save("color_palette.png")
        import os
        os.system("color_palette.png")  # Open the image with the default viewer
        
    def extract_color(self, item_name):
        if '(' in item_name and ')' in item_name:
            return item_name.split(' (')[1].rstrip(')')
        return "white"

    def get_hex_color(self, color_name):
        return self.color_map.get(color_name.lower(), "#FFFFFF")

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = WardrobeApp(root)
    root.mainloop()