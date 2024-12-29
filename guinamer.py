import tkinter as tk
from tkinter import messagebox
import pyperclip
from PIL import Image, ImageTk


pack_list = ["A1 Charizard", "A1 Mewtwo", "A1 Pikachu", "A1A"]
pack_card_list = {
    "A1 Charizard": ["FA Exeggutor", "FA Charizard", "FA Moltres", "FA Starmie", "FA Machamp", "FA Erika", "FA Blaine", "FA Sabrina", "RR Moltres", "RR Machamp"],
    "A1 Mewtwo": ["FA Venusaur", "FA Articuno", "FA Gengar", "FA Mewtwo", "FA Marowak", "FA Koga", "FA Giovanni", "RR Articuno", "RR Gengar"],
    "A1 Pikachu": ["FA Arcanine", "FA Blastoise", "FA Pikachu", "FA Zapdos", "FA Wigglytuff", "FA Misty", "FA Brock", "FA Lt. Surge", "RR Zapdos", "RR Wigglytuff"],
    "A1A": ["FA Celebi", "FA Gyarados", "FA Mew", "FA Aerodactyl", "FA Pidgeot", "FA Budding Expeditioner", "FA Blue", "FA Leaf", "RR Mew", "RR Aerodactyl"]
}

class ImageMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Thread Namer")

        self.packs_frame = None
        self.cards_frame = None

        self.selected_quantities = {}
        self.total_quantity = 0

        self.pack_images = {name: tk.PhotoImage(file=f"./images/{name}.png") for name in pack_list}
        '''self.card_images = {
            key: {img: tk.PhotoImage(file=f"./images/{img}.png") for img in pack_card_list[key]} 
            for key in pack_card_list
        }'''
        self.card_images = {
            key: {img: Image.open("./images/"+img+".png") for img in pack_card_list[key]} 
            for key in pack_card_list
        }

        self.pack_count_entry = None
        self.show_packs()

    def show_packs(self):
        self.reset_frames()

        self.packs_frame = tk.Frame(self.root)
        self.packs_frame.pack(fill="both", expand=True)

        tk.Label(self.packs_frame, text="Choose your pack", font=("Arial", 16)).pack(pady=10)

        frame = tk.Frame(self.packs_frame)
        frame.pack(pady=10)

        for pack in pack_list:
            image = self.pack_images[pack]
            img_width = image.width()
            img_height = image.height()
            btn = tk.Button(
                frame,
                image=image,
                command=lambda name=pack: self.show_cards(name),
                width=img_width,
                height=img_height
            )
            btn.pack(side="left", padx=5)

    def show_cards(self, pack):
        self.reset_frames()

        self.cards_frame = tk.Frame(self.root)
        self.cards_frame.pack(fill="both", expand=True)

        header_frame = tk.Frame(self.cards_frame)
        header_frame.pack(fill="x")

        tk.Button(header_frame, text="Back", command=self.show_packs).pack(side="left")
        tk.Label(header_frame, text=f"{pack} pack", font=("Arial", 16)).pack()

        card_list = pack_card_list[pack]

        self.selected_quantities = {img: 0 for img in card_list}
        self.total_quantity = 0

        frame = tk.Frame(self.cards_frame)
        frame.pack(pady=5)

        window_width = self.root.winfo_width()
        new_card_width = int(window_width / 6.5)

        row_frame = None
        for index, card_name in enumerate(card_list):
            if index % 6 == 0:  # 6 img per row
                row_frame = tk.Frame(frame)
                row_frame.pack(anchor="w", pady=5)

            img_frame = tk.Frame(row_frame)
            img_frame.pack(side="left")



            card = self.card_images[pack][card_name]
            ratio = card.width / new_card_width
            new_size = (new_card_width, int(card.height/ratio))
            card = card.resize(new_size) # using PIL to resize
            card = ImageTk.PhotoImage(card) # convert PIL object for use by tk
            card_label = tk.Label(img_frame, image=card)
            card_label.image = card # necessary
            card_label.pack()

            control_frame = tk.Frame(img_frame)
            control_frame.pack()

            sub_width = new_card_width // 4

            # adding an image to button makes its width in pixels instead of bs units
            pixel = tk.PhotoImage(width=1, height=1)

            minus_btn = tk.Button(
                control_frame,
                text="-",
                image=pixel,
                compound="center",
                command=lambda name=card_name: self.update_quantity(name, -1),
                width=sub_width,
                height=20
            )
            minus_btn.image = pixel
            minus_btn.pack(side="left")

            quantity_label = tk.Label(control_frame, text="0", image=pixel, compound="center", width=sub_width, height=20)
            quantity_label.pack(side="left")

            plus_btn = tk.Button(
                control_frame,
                text="+",
                image=pixel,
                compound="center",
                command=lambda name=card_name: self.update_quantity(name, 1),
                width=sub_width,
                height=20
            )
            plus_btn.pack(side="left")

            self.selected_quantities[card_name] = quantity_label

        submit_frame = tk.Frame(self.cards_frame)
        submit_frame.pack(pady=5)

        tk.Label(submit_frame, text="Packs opened:").pack(side="left", padx=10)

        self.pack_count_entry = tk.Entry(submit_frame, width=10)
        self.pack_count_entry.pack(side="left", padx=10)

        tk.Button(
            submit_frame,
            text="Submit",
            command=self.submit_quantities
        ).pack(side="left", padx=10)

    def reset_frames(self):
        if self.cards_frame:
            self.cards_frame.destroy()
        if self.packs_frame:
            self.packs_frame.destroy()

    def update_quantity(self, img_name, delta):
        label = self.selected_quantities[img_name]
        current_qty = int(label.cget("text"))
        new_total = self.total_quantity + delta

        if 0 <= new_total <= 5:
            new_qty = max(0, current_qty + delta)
            if delta > 0 and new_qty > current_qty or delta < 0 and current_qty > 0:
                self.total_quantity = new_total
                label.config(text=str(new_qty))

    def submit_quantities(self):
        result = []
        for img_name, label in self.selected_quantities.items():
            qty = int(label.cget("text"))
            if qty > 0:
                if qty == 1:
                    result.append(f"{img_name}")
                else:
                    result.append(f"{qty}x {img_name}")

        pack_count = self.pack_count_entry.get() or "0"
        result_text = f"[{self.total_quantity}/5] [{pack_count}p] " + ", ".join(result)
        pyperclip.copy(result_text)

        messagebox.showinfo("Submitted", f"Copied to clipboard:\n{result_text}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')
    #root.attributes('-fullscreen', True)
    app = ImageMenuApp(root)
    root.mainloop()