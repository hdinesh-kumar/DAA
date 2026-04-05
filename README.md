# Smart Parking Allocation System

## DAA Concepts Used (First)

1. Greedy Method
2. Min-Heap (Priority Queue)
3. Hash Map (Dictionary-Based Lookup)
4. Type-Based Partitioning of Slots
5. Time Complexity Analysis

## Project Overview

This mini project is a visual Smart Parking Allocation System built in Python using Tkinter.
It supports vehicle entry, vehicle exit, live parked-time tracking, slot availability, and separate parking spaces for different vehicle types.

Supported vehicle categories:

1. 2-Wheeler
2. Auto
3. Car
4. Mini Van
5. Truck/Lorry

## Full Concept Explanation

### 1. Greedy Method

Greedy means selecting the best immediate option at each step.
In this project, on every parking request, the system picks the nearest available slot for that vehicle type.

Why used:

1. Quick and practical for real-time parking.
2. Gives a locally optimal decision at every entry event.

### 2. Min-Heap (Priority Queue)

For each vehicle type, free slots are stored in a min-heap ordered by distance from entry.

Operations:

1. Allocation: remove nearest free slot using heap pop.
2. Deallocation: add slot back using heap push.

Complexity:

1. Heap pop and push are O(log n).
2. Better than scanning all slots linearly.

### 3. Hash Map (Dictionary)

Active vehicles are tracked in a dictionary using vehicle number as key.

Why used:

1. Fast check if a vehicle is already parked.
2. Fast exit lookup by plate number.

Complexity:

1. Insert, search, delete are O(1) average.

### 4. Type-Based Partitioning

Parking slots are partitioned by vehicle type.
For example, truck/lorry vehicles use only truck/lorry slots, and 2-wheelers use only 2-wheeler slots.

Why used:

1. Real-world rule compliance.
2. Reduced search space for allocation.
3. Cleaner logic and better space management.

### 5. Time Tracking and Dynamic State Update

Each parked vehicle stores entry timestamp.
On exit, duration is computed and recorded.

State transitions:

1. On entry: slot state changes from free to occupied.
2. On exit: slot state changes from occupied to free and re-enters heap.

### 6. Complexity Comparison Mindset (DAA Objective)

This project demonstrates the advantage of data structures over naive linear search.

1. Naive method: linear scan over all slots can approach O(n).
2. Current method: O(log n) for allocation/deallocation with O(1) average lookup for vehicle records.

## Features Implemented

1. Visual dashboard with Available, Occupied, and Total Capacity cards.
2. Entry form with vehicle number and vehicle type.
3. Exit flow with parked duration calculation.
4. Live table of currently parked vehicles.
5. Exit history table with total parked time.
6. Availability by vehicle type.

## Files in This Folder

1. smart_parking_gui.py: Python GUI implementation.
2. smart_parking.py: Console simulation and benchmark version.
3. smart_parking_system.html: Browser-based visual version.
4. DAA_CONCEPT_ALIGNMENT.md: Short alignment summary.
5. redme.md: This detailed explanation file.

## How to Run

Python GUI:

1. Open terminal in D:/DAA
2. Activate environment (optional): ./.venv/Scripts/Activate.ps1
3. Run: python smart_parking_gui.py

Web version:

1. Open smart_parking_system.html in browser.

## Run Notes

1. Always run commands from the project folder: D:/DAA
2. If Python is not recognized, use full path:
	- d:/DAA/.venv/Scripts/python.exe smart_parking_gui.py
3. If PowerShell blocks activation, run:
	- Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
	- ./.venv/Scripts/Activate.ps1
4. If Tkinter GUI does not open, install/reinstall Python with Tk support and try again.
5. Web version does not need Python; double-click smart_parking_system.html or run:
	- start smart_parking_system.html
6. To verify Python setup quickly:
	- python --version
	- python -m py_compile smart_parking_gui.py

## Conclusion

This project is strongly related to DAA because it applies algorithmic strategy and efficient data structures to a real-world parking problem.
The combination of Greedy + Min-Heap + Hash Map makes the system practical, scalable, and easy to explain in mini-project viva and report.
