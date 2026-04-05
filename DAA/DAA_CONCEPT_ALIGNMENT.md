# Smart Parking System - DAA Concept Alignment

This folder now has two visual approaches and one simulation script:

- Python GUI app: smart_parking_gui.py
- Web visual app: smart_parking_system.html
- Console simulation and benchmark: smart_parking.py

## Common Functional Requirements Covered

1. Shows available and occupied slots.
2. Shows parked vehicle numbers.
3. Tracks live parked duration for active vehicles.
4. On vehicle exit, slot becomes empty again.
5. Supports type-wise parking spaces:
   - 2-Wheeler
   - Auto
   - Car
   - Mini Van
   - Truck/Lorry

## DAA Concepts Used

1. Greedy method:
   - Always assign the nearest available slot for the selected vehicle type.

2. Min-Heap:
   - Each vehicle type keeps free slots in a min-heap by distance.
   - Allocation and re-insertion on exit are O(log n).

3. Hash Map:
   - Active vehicles are stored by vehicle number.
   - Lookup during exit is O(1) average.

4. Partitioning by type:
   - Independent slot pools improve organization and clarity.

## How to Run

Python GUI:

- python smart_parking_gui.py

Web UI:

- Open smart_parking_system.html in any browser.
