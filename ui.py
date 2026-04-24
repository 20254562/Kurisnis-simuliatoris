import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from domain import Defender, Weapon
from factory_wiring import build_app_wiring


class SimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("40k Combat Simulator")
        self.root.configure(bg="#111214")
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        wiring = build_app_wiring()
        self.weapon_repo = wiring.weapon_repo
        self.defender_repo = wiring.defender_repo
        self.simulator = wiring.simulator
        self.attacker_groups = []

        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Root.TFrame", background="#111214")
        style.configure(
            "Card.TLabelframe",
            background="#17191d",
            foreground="#f2f2f2",
            bordercolor="#2b2f36",
            relief="solid",
            borderwidth=1,
            padding=8,
        )
        style.configure(
            "Card.TLabelframe.Label",
            background="#17191d",
            foreground="#f2f2f2",
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "Body.TLabel",
            background="#17191d",
            foreground="#d8dbe1",
            font=("Segoe UI", 9),
        )
        style.configure(
            "Section.TLabelframe",
            background="#17191d",
            foreground="#f2f2f2",
            bordercolor="#2b2f36",
            relief="solid",
            borderwidth=1,
            padding=8,
        )
        style.configure(
            "Section.TLabelframe.Label",
            background="#17191d",
            foreground="#f2f2f2",
            font=("Segoe UI", 10, "bold"),
        )

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, padding=12, style="Root.TFrame")
        main_frame.grid(sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)

        self._build_weapon_frame(main_frame)
        self._build_defender_frame(main_frame)
        self._build_simulation_frame(main_frame)

    def _build_weapon_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="Weapon", style="Card.TLabelframe")
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)

        name_row = ttk.Frame(frame, style="Root.TFrame")
        name_row.grid(row=0, column=0, sticky="ew", pady=(2, 8))
        name_row.columnconfigure(1, weight=1)

        ttk.Label(name_row, text="Profile Name", style="Body.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.weapon_name_entry = tk.Entry(
            name_row,
            bg="#101114",
            fg="#f2f2f2",
            insertbackground="#f2f2f2",
            relief="solid",
            bd=1,
            font=("Segoe UI", 11),
        )
        self.weapon_name_entry.grid(row=0, column=1, sticky="ew")

        stats_frame = ttk.Frame(frame, style="Root.TFrame")
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        for i in range(5):
            stats_frame.columnconfigure(i, weight=1)

        weapon_spec = [
            ("Attacks:", "A"),
            ("Weapon Skill:", "WS"),
            ("Strength:", "S"),
            ("Armour Penetration:", "AP"),
            ("Damage:", "D"),
        ]
        self.weapon_entries = {"Name:": self.weapon_name_entry}
        for col, (field_key, short_label) in enumerate(weapon_spec):
            self._create_stat_box(
                stats_frame,
                col,
                short_label,
                field_key,
                self.weapon_entries)

        button_frame = ttk.Frame(frame, style="Root.TFrame")
        button_frame.grid(row=2, column=0, sticky="ew")
        ttk.Button(
            button_frame,
            text="Load Weapon profile",
            command=self.load_weapon_file,
        ).grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(
            button_frame,
            text="Save Weapon profile",
            command=self.save_selected_weapon,
        ).grid(row=0, column=1, sticky="ew", padx=2)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        roster_controls = ttk.Frame(frame, style="Root.TFrame")
        roster_controls.grid(row=3, column=0, sticky="ew", pady=(8, 4))
        roster_controls.columnconfigure(1, weight=1)

        ttk.Label(roster_controls, text="Count", style="Body.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 6)
        )
        self.weapon_group_count_entry = tk.Entry(
            roster_controls,
            bg="#101114",
            fg="#f2f2f2",
            insertbackground="#f2f2f2",
            relief="solid",
            bd=1,
            justify="center",
            width=6,
        )
        self.weapon_group_count_entry.grid(row=0, column=1, sticky="w")
        self.weapon_group_count_entry.insert(0, "1")

        ttk.Button(
            roster_controls,
            text="Add/Update Attacker",
            command=self.add_or_update_attacker_group,
        ).grid(row=0, column=2, sticky="ew", padx=(8, 4))

        ttk.Label(
            frame,
            text="Attacker roster",
            style="Body.TLabel",
        ).grid(row=4, column=0, sticky="w", pady=(6, 4))

        roster_wrap = tk.Frame(frame, bg="#0f1012", highlightthickness=1, highlightbackground="#2b2f36")
        roster_wrap.grid(row=5, column=0, sticky="nsew")
        roster_wrap.columnconfigure(0, weight=1)
        roster_wrap.rowconfigure(0, weight=1)

        self.attacker_roster_canvas = tk.Canvas(
            roster_wrap,
            bg="#0f1012",
            highlightthickness=0,
            bd=0,
        )
        self.attacker_roster_canvas.grid(row=0, column=0, sticky="nsew")

        attacker_scrollbar = ttk.Scrollbar(
            roster_wrap,
            orient="vertical",
            command=self.attacker_roster_canvas.yview,
        )
        attacker_scrollbar.grid(row=0, column=1, sticky="ns")
        self.attacker_roster_canvas.configure(yscrollcommand=attacker_scrollbar.set)

        self.attacker_roster_inner = tk.Frame(self.attacker_roster_canvas, bg="#0f1012")
        self.attacker_roster_canvas.create_window(
            (0, 0),
            window=self.attacker_roster_inner,
            anchor="nw",
            tags="attacker_inner",
        )
        self.attacker_roster_inner.bind("<Configure>", self._on_attacker_roster_inner_configure)
        self.attacker_roster_canvas.bind("<Configure>", self._on_attacker_roster_canvas_configure)
        self._refresh_attacker_cards()

        frame.rowconfigure(5, weight=1)

    def _build_defender_frame(self, parent):
        frame = ttk.LabelFrame(
            parent,
            text="Defender",
            style="Card.TLabelframe")
        frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)

        name_row = ttk.Frame(frame, style="Root.TFrame")
        name_row.grid(row=0, column=0, sticky="ew", pady=(2, 8))
        name_row.columnconfigure(1, weight=1)

        ttk.Label(name_row, text="Profile Name", style="Body.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.defender_name_entry = tk.Entry(
            name_row,
            bg="#101114",
            fg="#f2f2f2",
            insertbackground="#f2f2f2",
            relief="solid",
            bd=1,
            font=("Segoe UI", 11),
        )
        self.defender_name_entry.grid(row=0, column=1, sticky="ew")

        stats_frame = ttk.Frame(frame, style="Root.TFrame")
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        for i in range(5):
            stats_frame.columnconfigure(i, weight=1)

        defender_spec = [
            ("Toughness:", "T"),
            ("Wounds:", "W"),
            ("Save:", "Sv"),
            ("Inv. Save:", "Inv"),
            ("Model Count:", "Models"),
        ]
        self.defender_entries = {"Name:": self.defender_name_entry}
        for col, (field_key, short_label) in enumerate(defender_spec):
            self._create_stat_box(
                stats_frame,
                col,
                short_label,
                field_key,
                self.defender_entries)
        self.defender_entries["Model Count:"].insert(0, "1")

        button_frame = ttk.Frame(frame, style="Root.TFrame")
        button_frame.grid(row=2, column=0, sticky="ew")
        ttk.Button(
            button_frame,
            text="Load Defender profile",
            command=self.load_defender_file,
        ).grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(
            button_frame,
            text="Save Defender profile",
            command=self.save_selected_defender,
        ).grid(row=0, column=1, sticky="ew", padx=2)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

    def _create_stat_box(
            self,
            parent,
            column,
            label_text,
            field_key,
            target_dict):
        cell = tk.Frame(parent, bg="#111214")
        cell.grid(row=0, column=column, sticky="nsew", padx=4)
        cell.columnconfigure(0, weight=1)

        label = ttk.Label(cell, text=label_text, style="Body.TLabel")
        label.grid(row=0, column=0, pady=(0, 4))

        entry = tk.Entry(
            cell,
            width=5,
            justify="center",
            bg="#101114",
            fg="#f2f2f2",
            insertbackground="#f2f2f2",
            relief="solid",
            bd=1,
            font=("Segoe UI", 16, "bold"),
        )
        entry.grid(row=1, column=0, ipady=12, sticky="ew")
        target_dict[field_key] = entry

    def _build_simulation_frame(self, parent):
        frame = ttk.LabelFrame(
            parent,
            text="Simulation",
            style="Section.TLabelframe")
        frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5)
        frame.columnconfigure(1, weight=1)

        ttk.Label(
            frame,
            text="Build attacker roster (max 10). Defender model count is in Defender card.",
            style="Body.TLabel",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=2)

        ttk.Button(
            frame,
            text="Run Simulation",
            command=self.run_simulation).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=5,
        )

        self.avg_result = ttk.Label(
            frame,
            text="Average damage: N/A",
            style="Body.TLabel")
        self.avg_result.grid(row=2, column=0, columnspan=2, sticky="w", pady=2)
        self.kill_result = ttk.Label(
            frame, text="Kill chance: N/A", style="Body.TLabel")
        self.kill_result.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="w",
            pady=2)

    def _parse_positive_int(self, text, field_name):
        value = int(text)
        if value < 1:
            raise ValueError(f"{field_name} must be a positive integer.")
        return value

    def _find_group_index(self, groups, name):
        for index, group in enumerate(groups):
            if group["name"].lower() == name.lower():
                return index
        return None

    def _on_attacker_roster_inner_configure(self, _event):
        self.attacker_roster_canvas.configure(
            scrollregion=self.attacker_roster_canvas.bbox("all")
        )

    def _on_attacker_roster_canvas_configure(self, event):
        self.attacker_roster_canvas.itemconfig("attacker_inner", width=event.width)

    def _create_card_stat(self, parent, short_label, value):
        stat_box = tk.Frame(
            parent,
            bg="#101114",
            highlightthickness=1,
            highlightbackground="#3a3f49",
            padx=6,
            pady=4,
        )
        stat_box.pack(side="left", padx=(0, 6), fill="y")
        tk.Label(
            stat_box,
            text=short_label,
            bg="#101114",
            fg="#a8afbc",
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="center")
        tk.Label(
            stat_box,
            text=str(value),
            bg="#101114",
            fg="#f2f2f2",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="center")

    def _refresh_attacker_cards(self):
        for child in self.attacker_roster_inner.winfo_children():
            child.destroy()

        if not self.attacker_groups:
            tk.Label(
                self.attacker_roster_inner,
                text="No attacker profiles yet. Add one above.",
                bg="#0f1012",
                fg="#9aa2af",
                font=("Segoe UI", 10),
                pady=10,
            ).pack(anchor="w", padx=8)
            return

        for group in self.attacker_groups:
            weapon = group["weapon"]
            card = tk.Frame(
                self.attacker_roster_inner,
                bg="#15181c",
                highlightthickness=1,
                highlightbackground="#2f3440",
                padx=10,
                pady=8,
            )
            card.pack(fill="x", padx=8, pady=6)

            title_row = tk.Frame(card, bg="#15181c")
            title_row.pack(fill="x")
            tk.Label(
                title_row,
                text=group["name"],
                bg="#15181c",
                fg="#f2f2f2",
                font=("Segoe UI", 11, "bold"),
            ).pack(side="left")

            controls_row = tk.Frame(title_row, bg="#15181c")
            controls_row.pack(side="right")
            tk.Button(
                controls_row,
                text="-",
                width=2,
                bg="#3b3b3f",
                fg="#f2f2f2",
                activebackground="#4a4a50",
                activeforeground="#ffffff",
                bd=0,
                relief="flat",
                command=lambda n=group["name"]: self._adjust_attacker_count(n, -1),
            ).pack(side="left")
            tk.Label(
                controls_row,
                text=f" x{group['count']} ",
                bg="#15181c",
                fg="#f2f2f2",
                font=("Segoe UI", 11, "bold"),
            ).pack(side="left")
            tk.Button(
                controls_row,
                text="+",
                width=2,
                bg="#4b4b50",
                fg="#f2f2f2",
                activebackground="#595a61",
                activeforeground="#ffffff",
                bd=0,
                relief="flat",
                command=lambda n=group["name"]: self._adjust_attacker_count(n, 1),
            ).pack(side="left", padx=(0, 8))
            tk.Button(
                controls_row,
                text="Remove",
                bg="#612528",
                fg="#ffe9e9",
                activebackground="#7b2f34",
                activeforeground="#ffffff",
                bd=0,
                relief="flat",
                command=lambda n=group["name"]: self._remove_attacker_group_by_name(n),
            ).pack(side="left")

            stats_row = tk.Frame(card, bg="#15181c")
            stats_row.pack(fill="x", pady=(8, 0))
            weapon_skill = "Auto" if weapon.weapon_skill is None else weapon.weapon_skill
            self._create_card_stat(stats_row, "A", weapon.attacks)
            self._create_card_stat(stats_row, "WS", weapon_skill)
            self._create_card_stat(stats_row, "S", weapon.strength)
            self._create_card_stat(stats_row, "AP", weapon.armour_penetration)
            self._create_card_stat(stats_row, "D", weapon.damage)

    def _adjust_attacker_count(self, name, delta):
        index = self._find_group_index(self.attacker_groups, name)
        if index is None:
            return
        current = self.attacker_groups[index]["count"]
        updated = current + delta
        if updated < 1:
            return
        self.attacker_groups[index]["count"] = updated
        self._refresh_attacker_cards()

    def _remove_attacker_group_by_name(self, name):
        self.attacker_groups = [
            g for g in self.attacker_groups if g["name"].lower() != name.lower()
        ]
        self._refresh_attacker_cards()

    def add_or_update_attacker_group(self):
        weapon = self._parse_weapon_entries(require_name=True, fallback_name="Weapon")
        if weapon is None:
            return

        try:
            count = self._parse_positive_int(
                self.weapon_group_count_entry.get().strip(),
                "Attacker count",
            )
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Input error", str(exc))
            return

        existing_index = self._find_group_index(self.attacker_groups, weapon.name)
        if existing_index is None and len(self.attacker_groups) >= 10:
            messagebox.showerror("Limit reached", "You can add up to 10 attacker profiles.")
            return

        group_data = {"name": weapon.name, "weapon": weapon, "count": count}
        if existing_index is None:
            self.attacker_groups.append(group_data)
        else:
            self.attacker_groups[existing_index] = group_data

        self._refresh_attacker_cards()

    def _parse_weapon_entries(
            self,
            require_name=False,
            fallback_name="Weapon"):
        try:
            name = self.weapon_entries["Name:"].get().strip()
            attacks = self.weapon_entries["Attacks:"].get().strip()
            weapon_skill_text = self.weapon_entries["Weapon Skill:"].get(
            ).strip()
            weapon_skill = int(
                weapon_skill_text) if weapon_skill_text != "" else None
            strength = int(self.weapon_entries["Strength:"].get())
            armour_penetration_text = self.weapon_entries[
                "Armour Penetration:"
            ].get().strip()
            armour_penetration = (
                int(armour_penetration_text)
                if armour_penetration_text != ""
                else 0
            )
            damage = self.weapon_entries["Damage:"].get().strip()
        except ValueError:
            messagebox.showerror(
                "Input error",
                "Please enter valid values for the weapon profile.",
            )
            return None
        if not name and require_name:
            messagebox.showerror("Input error", "Weapon name is required.")
            return None

        if not name:
            name = fallback_name

        try:
            return Weapon(
                name,
                attacks,
                weapon_skill,
                strength,
                armour_penetration,
                damage,
            )
        except ValueError as exc:
            messagebox.showerror("Input error", str(exc))
            return None

    def _parse_defender_entries(
            self,
            require_name=False,
            fallback_name="Defender"):
        try:
            name = self.defender_entries["Name:"].get().strip()
            toughness = int(self.defender_entries["Toughness:"].get())
            wounds = int(self.defender_entries["Wounds:"].get())
            save = int(self.defender_entries["Save:"].get())
            inv_text = self.defender_entries["Inv. Save:"].get().strip()
            invulnerable_save = int(inv_text) if inv_text != "" else None
        except ValueError:
            messagebox.showerror(
                "Input error",
                "Please enter valid values for the defender profile.",
            )
            return None
        if not name and require_name:
            messagebox.showerror("Input error", "Defender name is required.")
            return None

        if not name:
            name = fallback_name

        try:
            return Defender(name, toughness, wounds, save, invulnerable_save)
        except ValueError as exc:
            messagebox.showerror("Input error", str(exc))
            return None

    def populate_weapon_entries(self, weapon):
        self.weapon_entries["Name:"].delete(0, tk.END)
        self.weapon_entries["Name:"].insert(0, weapon.name)
        self.weapon_entries["Attacks:"].delete(0, tk.END)
        self.weapon_entries["Attacks:"].insert(0, str(weapon.attacks))
        self.weapon_entries["Weapon Skill:"].delete(0, tk.END)
        self.weapon_entries["Weapon Skill:"].insert(
            0, str(weapon.weapon_skill))
        self.weapon_entries["Strength:"].delete(0, tk.END)
        self.weapon_entries["Strength:"].insert(0, str(weapon.strength))
        self.weapon_entries["Armour Penetration:"].delete(0, tk.END)
        self.weapon_entries["Armour Penetration:"].insert(
            0,
            str(weapon.armour_penetration),
        )
        self.weapon_entries["Damage:"].delete(0, tk.END)
        self.weapon_entries["Damage:"].insert(0, str(weapon.damage))

    def populate_defender_entries(self, defender):
        self.defender_entries["Name:"].delete(0, tk.END)
        self.defender_entries["Name:"].insert(0, defender.name)
        self.defender_entries["Toughness:"].delete(0, tk.END)
        self.defender_entries["Toughness:"].insert(0, str(defender.toughness))
        self.defender_entries["Wounds:"].delete(0, tk.END)
        self.defender_entries["Wounds:"].insert(0, str(defender.wounds))
        self.defender_entries["Save:"].delete(0, tk.END)
        self.defender_entries["Save:"].insert(0, str(defender.save))
        self.defender_entries["Inv. Save:"].delete(0, tk.END)
        invulnerable = "" if defender.invulnerable_save is None else str(
            defender.invulnerable_save)
        self.defender_entries["Inv. Save:"].insert(0, invulnerable)

    def save_selected_weapon(self):
        weapon = self._parse_weapon_entries(
            require_name=True,
            fallback_name="Weapon",
        )
        if weapon is None:
            return

        filename = filedialog.asksaveasfilename(
            title="Save Weapon",
            initialdir=self.script_dir,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not filename:
            return

        self.weapon_repo.save_weapon(weapon, filename)

    def save_selected_defender(self):
        defender = self._parse_defender_entries(
            require_name=True,
            fallback_name="Defender",
        )
        if defender is None:
            return

        filename = filedialog.asksaveasfilename(
            title="Save Defender",
            initialdir=self.script_dir,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not filename:
            return

        self.defender_repo.save_defender(defender, filename)

    def load_weapon_file(self):
        filename = filedialog.askopenfilename(
            title="Load Weapon",
            initialdir=self.script_dir,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not filename:
            return

        try:
            weapon = self.weapon_repo.load_weapon(filename)
            self.populate_weapon_entries(weapon)
            messagebox.showinfo("Loaded", f"Weapon '{weapon.name}' loaded.")
        except (FileNotFoundError, OSError):
            messagebox.showerror("Load error", "File not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Load error", "Invalid file format.")
        except (KeyError, TypeError, ValueError) as exc:
            messagebox.showerror("Load error", f"Invalid profile data: {exc}")

    def load_defender_file(self):
        filename = filedialog.askopenfilename(
            title="Load Defender",
            initialdir=self.script_dir,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not filename:
            return

        try:
            defender = self.defender_repo.load_defender(filename)
            self.populate_defender_entries(defender)
            messagebox.showinfo(
                "Loaded", f"Defender '{
                    defender.name}' loaded.")
        except (FileNotFoundError, OSError):
            messagebox.showerror("Load error", "File not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Load error", "Invalid file format.")
        except (KeyError, TypeError, ValueError) as exc:
            messagebox.showerror("Load error", f"Invalid profile data: {exc}")

    def run_simulation(self):
        if not self.attacker_groups:
            messagebox.showerror(
                "Input error",
                "Add at least one attacker profile before running simulation.",
            )
            return

        defender = self._parse_defender_entries(
            require_name=False,
            fallback_name="Temporary Defender",
        )
        if defender is None:
            return

        try:
            defender_count = self._parse_positive_int(
                self.defender_entries["Model Count:"].get().strip(),
                "Defender count",
            )
        except ValueError:
            messagebox.showerror(
                "Input error",
                "Defender count must be a positive integer.",
            )
            return

        attacker_groups = [
            (group["weapon"], group["count"])
            for group in self.attacker_groups
        ]

        try:
            result = self.simulator.simulate_armies(
                attacker_groups,
                defender,
                defender_count,
                trials=10000,
            )
        except ValueError as exc:
            messagebox.showerror("Simulation error", str(exc))
            return

        self.avg_result.config(
            text=f"Average damage: {
                result['avg_damage']:.2f}")
        self.kill_result.config(
            text=f"Kill chance (all defenders destroyed): {
                result['kill_chance']:.2%}")
