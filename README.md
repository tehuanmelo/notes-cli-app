# 📝 Notes CLI App

## 📌 Description

This is a simple terminal-based notes application built with Python and Textual.

The main idea behind this project is to provide a personal tool for quickly writing notes during the learning process while coding. Instead of switching between applications, everything is available directly in the terminal.

It also improves how I search and revisit my learnings, making the process faster and more efficient — all at my fingertips in the terminal.

---

## 🚀 Features

- Create notes quickly while coding
- Edit and update existing notes
- Delete notes
- Search notes by title or content
- Automatic title generation from content
- Notes sorted by last update
- Clean terminal UI using Textual

---

## 🧰 Tech Stack

- Python 3
- SQLite (local database)
- Textual (terminal UI framework)

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/tehuanmelo/notes-cli-app
cd notes-cli-app
```

---

### Option 1 — Automated setup (recommended)

```bash
chmod +x install.sh
./install.sh
```

Activate the environment:

```bash
source .venv/bin/activate
```

---

### Option 2 — Manual setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Run the application

```bash
python -m src.app.main
```

---

### Run the app using a terminal command (alias)

Add this line to your `.zshrc` file:

```bash
alias notes="PYTHONPATH=<full_path_to_project> <full_path_to_project>/.venv/bin/python -m src.app.main"
```

This exposes the project to `PYTHONPATH` and uses the virtual environment Python interpreter where all dependencies are installed.

Reload your shell:

```bash
source ~/.zshrc
```

Run the app:

```bash
notes
```

You do not need to activate the virtual environment manually because the alias uses the virtual environment Python interpreter.

---

## ⌨️ Controls

- Ctrl + S → Save note
- Ctrl + N → New note
- Ctrl + D → Delete note
- Ctrl + E → Exit
- Search bar → Filter notes instantly

---

## 📁 Project Structure

```bash
notes-cli-app/
│
├── install.sh
├── requirements.txt
└── src
    ├── app
    │   ├── main.py        # Main application (UI + logic)
    │   └── notes.css      # UI styles
    │
    ├── data
    │   ├── database.py    # Database operations (CRUD)
    │   └── notes.db       # SQLite database
    │
    └── models
        └── model.py       # Note data model
```

---

## 🧠 How It Works

- Notes are stored in a local SQLite database (`notes.db`)
- Each note contains:
  - title
  - content
  - created_at
  - updated_at
  - id
- The UI is built with Textual using:
  - Sidebar (notes list + search)
  - Main area (text editor)
- Notes are automatically sorted by the most recently updated

---

## 🔍 Search

You can type in the search bar to filter notes by:

- Title
- Content

Filtering happens instantly as you type.

---

## ⚠️ Notes

- The database is created automatically on first run
- Notes are stored locally on your machine
- No internet connection is required

---

## 🎯 Purpose of the Project

This project was created to solve a real problem during my learning journey:

- Capture ideas quickly while coding
- Avoid context switching between applications
- Keep all learning notes in one place
- Improve the ability to search and revisit knowledge

The goal is to make learning faster and more practical by keeping everything inside the terminal.

---

## 🔮 Future Improvements

- Add tags or categories
- Improve search (filters, keywords)
- Export notes (JSON / CSV)
- Improve UI/UX
- Add keyboard navigation enhancements

---

## 👨‍💻 Author

- Tehuan Melo
- Python Developer | Jiu-Jitsu Coach

---

Simple tool, built for real use 🚀