# Smart Chess Game Engine ♟️🤖

A complete, interactive **Chess Game Application** built in Python. This project features a beautiful graphical user interface constructed via **Tkinter** and incorporates a rule-abiding movement engine alongside a smart automated **Computer Player (AI)** built completely from scratch using Object-Oriented Programming (OOP) architectures.

---

## 🌟 About the Developer

*   **Age/Class:** 16 Years Old (Class 10th) 🎯
*   **Future Goal:** B.Tech in Artificial Intelligence and Machine Learning (AI-ML).
*   **Milestone:** Successfully completed the **100 Days of Code** challenge!
*   **Current Focus:** Learning Data Structures & Algorithms (DSA) and data science libraries like **NumPy** and **Pandas**.

---

## ✨ Key Features

*   **Tkinter Graphical UI:** A clean, custom canvas chessboard styling dynamic turns, active highlights, and custom visual player headers.
*   **Smart Computer Opponent:** Built an automated player for `Black` that dynamically scans the board array, prioritizing aggressive capture opportunities before executing strategic random moves.
*   **Interactive Controls & Visual Anchors:** Supports responsive cell clicks, tracking `SELECTED_SQUARE` indicators and capturing illegal target logs immediately on the screen interface.
*   **Comprehensive Move Validation Engines:** Full rule matrix constraints checking structural path blockages (`is_path_clear`) and blocking movements that end on friendly positions.

---

## 🛠️ OOP Concepts & Engineering Architecture

This project serves as a masterclass in component encapsulation and abstraction relationships:
*   **Polymorphic Piece Blueprints:** Features a generic parent `Piece` class inherited by individual concrete subclasses (`Pawn`, `Rook`, `Knight`, `Bishop`, `Queen`, `King`). Each subclass overrides `is_valid_move()` to run its unique geometric constraints.
*   **Grid Matrix Layering (Composition):** The structure employs a multi-tier aggregation system where the `Board` class holds a grid of `Spot` objects, which in turn encapsulate specific `Piece` objects dynamically.
*   **Decoupled State Controllers:** Separates execution states smoothly across the mathematical layout (`Board`), current game conditions (`Game`), input capturing viewports (`ChessGUI`), and decisions logic (`ComputerPlayer`).

---

## 🚀 How to Run the Project

1.  **Clone the repository:**
    ```bash
    git clone https://github.com
    ```
2.  **Navigate to the project folder:**
    ```bash
    cd smart-chess-game-oop
    ```
3.  **Run the application window:**
    ```bash
    python main.py
    ```

---

## 📝 Prerequisites
*   Python 3.x installed on your machine.
*   Standard library components (`tkinter`, `random` are included with basic Python setups).
