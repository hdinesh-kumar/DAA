"""
Smart Parking Allocation System (Visual Mini Project)
DAA concepts used:
  1) Greedy + Min-Heap per vehicle type for nearest-slot allocation -> O(log n)
  2) Hash map for quick lookup by vehicle number              -> O(1) average

Run:
  python smart_parking_gui.py
"""

import heapq
import re
import time
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk, messagebox
from typing import Optional


@dataclass
class Slot:
    slot_id: int
    vehicle_type: str
    distance: float


@dataclass
class ActiveParking:
    plate: str
    vehicle_type: str
    slot: Slot
    entry_ts: float


@dataclass
class CompletedSession:
    plate: str
    vehicle_type: str
    slot_id: int
    duration_sec: int


class SmartParkingAllocator:
    """Core parking logic with DAA-friendly data structures."""

    def __init__(self, capacities: dict[str, int]):
        self.capacities = capacities.copy()

        # Min-heap per type: (distance, slot_id)
        self._free_heaps: dict[str, list[tuple[float, int]]] = {k: [] for k in capacities}

        # Slot registry and active map
        self._all_slots: dict[int, Slot] = {}
        self.active_by_plate: dict[str, ActiveParking] = {}
        self.completed_sessions: list[CompletedSession] = []

        self._build_slots()

    def _build_slots(self) -> None:
        slot_id = 1
        base_distance = {
            "2-Wheeler": 8.0,
            "Auto": 12.0,
            "Car": 18.0,
            "Mini Van": 26.0,
            "Truck/Lorry": 40.0,
        }

        for vtype, count in self.capacities.items():
            start = base_distance[vtype]
            for i in range(count):
                slot = Slot(slot_id=slot_id, vehicle_type=vtype, distance=start + i * 2.5)
                self._all_slots[slot_id] = slot
                heapq.heappush(self._free_heaps[vtype], (slot.distance, slot_id))
                slot_id += 1

    @staticmethod
    def validate_plate(plate: str) -> bool:
        # Simple broad format check; keeps project user-friendly.
        return bool(re.fullmatch(r"[A-Za-z0-9\-]{4,15}", plate.strip()))

    def park(self, plate: str, vehicle_type: str) -> Optional[ActiveParking]:
        plate = plate.strip().upper()
        if plate in self.active_by_plate:
            return None

        heap = self._free_heaps[vehicle_type]
        if not heap:
            return None

        _, sid = heapq.heappop(heap)
        slot = self._all_slots[sid]
        rec = ActiveParking(
            plate=plate,
            vehicle_type=vehicle_type,
            slot=slot,
            entry_ts=time.time(),
        )
        self.active_by_plate[plate] = rec
        return rec

    def leave(self, plate: str) -> Optional[CompletedSession]:
        plate = plate.strip().upper()
        rec = self.active_by_plate.pop(plate, None)
        if rec is None:
            return None

        now = time.time()
        duration_sec = max(0, int(now - rec.entry_ts))

        heapq.heappush(self._free_heaps[rec.vehicle_type], (rec.slot.distance, rec.slot.slot_id))

        done = CompletedSession(
            plate=rec.plate,
            vehicle_type=rec.vehicle_type,
            slot_id=rec.slot.slot_id,
            duration_sec=duration_sec,
        )
        self.completed_sessions.insert(0, done)
        return done

    def available_by_type(self) -> dict[str, int]:
        return {k: len(v) for k, v in self._free_heaps.items()}

    def total_available(self) -> int:
        return sum(len(h) for h in self._free_heaps.values())

    def total_capacity(self) -> int:
        return sum(self.capacities.values())

    def occupied_count(self) -> int:
        return len(self.active_by_plate)


class SmartParkingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Parking Allocation System ")
        self.geometry("1200x760")
        self.minsize(1050, 700)
        self.configure(bg="#f4f6f8")

        capacities = {
            "2-Wheeler": 12,
            "Auto": 7,
            "Car": 14,
            "Mini Van": 6,
            "Truck/Lorry": 5,
        }
        self.system = SmartParkingAllocator(capacities)

        self._build_style()
        self._build_layout()
        self._refresh_all()
        self._tick_clock()

    def _build_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), background="#f4f6f8", foreground="#1f2937")
        style.configure("Sub.TLabel", font=("Segoe UI", 10), background="#f4f6f8", foreground="#4b5563")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("CardTitle.TLabel", font=("Segoe UI", 11, "bold"), background="#ffffff", foreground="#111827")
        style.configure("CardValue.TLabel", font=("Segoe UI", 18, "bold"), background="#ffffff", foreground="#0f766e")

        style.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        style.configure("Park.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Exit.TButton", font=("Segoe UI", 10, "bold"), padding=8)

    def _build_layout(self) -> None:
        outer = ttk.Frame(self, padding=14)
        outer.pack(fill="both", expand=True)

        top = ttk.Frame(outer)
        top.pack(fill="x")

        ttk.Label(top, text="PARKING SYSTEM", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            top,
            text="EA MALL",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(2, 10))

        self.cards_wrap = ttk.Frame(outer)
        self.cards_wrap.pack(fill="x", pady=(0, 10))

        self.total_available_var = tk.StringVar()
        self.total_occupied_var = tk.StringVar()
        self.total_capacity_var = tk.StringVar()

        self._make_card(self.cards_wrap, "Available", self.total_available_var, 0)
        self._make_card(self.cards_wrap, "Occupied", self.total_occupied_var, 1)
        self._make_card(self.cards_wrap, "Total Capacity", self.total_capacity_var, 2)

        middle = ttk.Frame(outer)
        middle.pack(fill="x", pady=(0, 12))

        form = ttk.LabelFrame(middle, text="Vehicle Action", padding=10)
        form.pack(side="left", fill="x", expand=True)

        ttk.Label(form, text="Vehicle Number").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.plate_entry = ttk.Entry(form, width=24)
        self.plate_entry.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Vehicle Type").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.type_box = ttk.Combobox(form, width=22, state="readonly", values=list(self.system.capacities.keys()))
        self.type_box.current(0)
        self.type_box.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        btn_row = ttk.Frame(form)
        btn_row.grid(row=2, column=0, columnspan=2, sticky="w", padx=4, pady=(8, 4))

        ttk.Button(btn_row, text="Park Vehicle", style="Park.TButton", command=self._on_park).pack(side="left", padx=(0, 8))
        ttk.Button(btn_row, text="Vehicle Exit", style="Exit.TButton", command=self._on_exit).pack(side="left")

        ttk.Label(
            form,
            text="Plate format: letters/numbers/- (e.g., TN-AB-1234)",
            style="Sub.TLabel",
        ).grid(row=3, column=0, columnspan=2, sticky="w", padx=4, pady=(4, 0))

        avail = ttk.LabelFrame(middle, text="Availability by Vehicle Type", padding=10)
        avail.pack(side="left", fill="both", padx=(10, 0))

        self.type_rows: dict[str, tk.StringVar] = {}
        for idx, vtype in enumerate(self.system.capacities):
            lab = ttk.Label(avail, text=vtype)
            lab.grid(row=idx, column=0, sticky="w", pady=2)
            val = tk.StringVar(value="0")
            self.type_rows[vtype] = val
            ttk.Label(avail, textvariable=val, width=8).grid(row=idx, column=1, sticky="e", padx=(10, 0), pady=2)

        body = ttk.Frame(outer)
        body.pack(fill="both", expand=True)

        left = ttk.LabelFrame(body, text="Currently Parked Vehicles (Live)", padding=8)
        left.pack(side="left", fill="both", expand=True)

        self.active_tree = ttk.Treeview(
            left,
            columns=("plate", "type", "slot", "duration"),
            show="headings",
            height=14,
        )
        self.active_tree.heading("plate", text="Vehicle Number")
        self.active_tree.heading("type", text="Type")
        self.active_tree.heading("slot", text="Slot")
        self.active_tree.heading("duration", text="Parked Time")

        self.active_tree.column("plate", width=150, anchor="center")
        self.active_tree.column("type", width=130, anchor="center")
        self.active_tree.column("slot", width=80, anchor="center")
        self.active_tree.column("duration", width=110, anchor="center")
        self.active_tree.pack(fill="both", expand=True)

        right = ttk.LabelFrame(body, text="Recent Exits (Duration Summary)", padding=8)
        right.pack(side="left", fill="both", expand=True, padx=(10, 0))

        self.exit_tree = ttk.Treeview(
            right,
            columns=("plate", "type", "slot", "duration"),
            show="headings",
            height=14,
        )
        self.exit_tree.heading("plate", text="Vehicle Number")
        self.exit_tree.heading("type", text="Type")
        self.exit_tree.heading("slot", text="Slot")
        self.exit_tree.heading("duration", text="Total Parked")

        self.exit_tree.column("plate", width=150, anchor="center")
        self.exit_tree.column("type", width=130, anchor="center")
        self.exit_tree.column("slot", width=80, anchor="center")
        self.exit_tree.column("duration", width=110, anchor="center")
        self.exit_tree.pack(fill="both", expand=True)

    def _make_card(self, parent: ttk.Frame, title: str, value_var: tk.StringVar, col: int) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=12)
        card.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 10, 0))
        parent.columnconfigure(col, weight=1)
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, textvariable=value_var, style="CardValue.TLabel").pack(anchor="w", pady=(6, 0))

    @staticmethod
    def _fmt_duration(seconds: int) -> str:
        h, rem = divmod(seconds, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def _on_park(self) -> None:
        plate = self.plate_entry.get().strip().upper()
        vehicle_type = self.type_box.get()

        if not plate or not SmartParkingAllocator.validate_plate(plate):
            messagebox.showwarning("Invalid", "Enter a valid vehicle number (4-15 chars, letters/numbers/-).")
            return

        if plate in self.system.active_by_plate:
            messagebox.showwarning("Already Parked", f"{plate} is already parked.")
            return

        rec = self.system.park(plate, vehicle_type)
        if rec is None:
            messagebox.showerror("No Space", f"No free {vehicle_type} slots available.")
            return

        messagebox.showinfo("Allocated", f"{plate} parked in Slot {rec.slot.slot_id} ({vehicle_type}).")
        self.plate_entry.delete(0, tk.END)
        self._refresh_all()

    def _on_exit(self) -> None:
        plate = self.plate_entry.get().strip().upper()
        if not plate:
            messagebox.showwarning("Missing", "Enter vehicle number for exit.")
            return

        done = self.system.leave(plate)
        if done is None:
            messagebox.showerror("Not Found", f"{plate} is not currently parked.")
            return

        duration = self._fmt_duration(done.duration_sec)
        messagebox.showinfo("Exit Recorded", f"{plate} exited. Parked time: {duration}")
        self.plate_entry.delete(0, tk.END)
        self._refresh_all()

    def _refresh_cards_and_type_counts(self) -> None:
        self.total_available_var.set(str(self.system.total_available()))
        self.total_occupied_var.set(str(self.system.occupied_count()))
        self.total_capacity_var.set(str(self.system.total_capacity()))

        by_type = self.system.available_by_type()
        for vtype, var in self.type_rows.items():
            cap = self.system.capacities[vtype]
            var.set(f"{by_type[vtype]} / {cap}")

    def _refresh_active_table(self) -> None:
        for row in self.active_tree.get_children():
            self.active_tree.delete(row)

        now = time.time()
        active = sorted(self.system.active_by_plate.values(), key=lambda x: x.entry_ts)
        for rec in active:
            dur = self._fmt_duration(int(now - rec.entry_ts))
            self.active_tree.insert(
                "",
                "end",
                values=(rec.plate, rec.vehicle_type, rec.slot.slot_id, dur),
            )

    def _refresh_exit_table(self) -> None:
        for row in self.exit_tree.get_children():
            self.exit_tree.delete(row)

        for rec in self.system.completed_sessions[:25]:
            self.exit_tree.insert(
                "",
                "end",
                values=(
                    rec.plate,
                    rec.vehicle_type,
                    rec.slot_id,
                    self._fmt_duration(rec.duration_sec),
                ),
            )

    def _refresh_all(self) -> None:
        self._refresh_cards_and_type_counts()
        self._refresh_active_table()
        self._refresh_exit_table()

    def _tick_clock(self) -> None:
        # Keeps parked duration live-updating.
        self._refresh_active_table()
        self.after(1000, self._tick_clock)


def main() -> None:
    app = SmartParkingApp()
    app.mainloop()


if __name__ == "__main__":
    main()
