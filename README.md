# KreoPix

**KreoPix** is an open-source image editing application built in Python that explores how modern software engineering practices can be applied to desktop tools.

At its core, KreoPix is designed as a **learning-driven project**: not just to edit images, but to demonstrate how to structure a complex application in a clean, scalable, and maintainable way. It combines a multi-layer canvas system, custom brush engines, and image processing capabilities with a carefully designed architecture that separates responsibilities across the entire system.

The application is built using `tkinter` for the graphical interface and leverages `Pillow (PIL)` and `NumPy` for efficient pixel-level operations.

---

## 🏗️ Architecture

KreoPix is organized using a **layered architecture combined with the MVC pattern**, ensuring that each part of the system has a clear and isolated responsibility.


### How it works

* The **UI Layer** captures user interactions and renders the application.
* The **Controller Layer** interprets those actions and decides what should happen.
* The **Services Layer** contains the actual business logic (image processing, brushes, file handling).
* The **Core Layer** represents the application state and domain models.

The entire system is initialized through a central entry point (`AppRoot`), which wires dependencies together and starts the application lifecycle.

---

## ▶️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/kreopix.git
cd kreopix
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python -m kreopix
```

---

## 📚 Documentation

Detailed documentation, development notes, and the user manual are available here:

  **Notion Workspace:**
[View documentation](https://www.notion.so/Documentation-KreoPix-32efa6590dc180d2981cfa74e93bb6c5?source=copy_link)

---

## 📄 License

This project is licensed under the MIT License.
