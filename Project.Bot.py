import configparser
import os
from prettytable import PrettyTable

# Class to represent notes
class Note:
    def __init__(self, note_id, text, tags):
        self.note_id = note_id
        self.text = text
        self.tags = tags

# Function to load notes from file
def load_notes(config):
    notes_file = config.get("DEFAULT", "notes_file", fallback="notes.txt")
    try:
        with open(notes_file, "r") as f:
            notes = [Note(*line.strip().split("|", 2), tags=line.strip().split("|")[2].split(",")) for line in f]
        return notes
    except FileNotFoundError:
        print("File not found. Using default notes.txt.")
        return []
    except Exception as e:
        print(f"Unknown error while loading notes: {e}")
        return []

# Function to save notes to file
def save_notes(notes, config):
    notes_file = config.get("DEFAULT", "notes_file", fallback="notes.txt")
    try:
        with open(notes_file, "w") as f:
            for note in notes:
                f.write(f"{note.note_id}|{note.text}|{','.join(note.tags)}\n")
    except Exception as e:
        print(f"Error while saving notes: {e}")

# Function to add a new note
def add_note(notes, config):
    text = input("Enter note text: ").strip()
    if not text:
        print("Error: Note text cannot be empty.")
        return
    tags = input("Enter tags (comma-separated): ").split(",")
    note_id = max((note.note_id for note in notes), default=0) + 1
    notes.append(Note(note_id, text, tags))
    save_notes(notes, config)

# Function to search notes by text
def search_notes(notes):
    text = input("Enter text to search: ").lower().strip()
    results = [note for note in notes if text in note.text.lower()]
    return results

# Function to edit an existing note
def edit_note(notes, config):
    try:
        note_id = int(input("Enter the ID of the note you want to edit: "))
        note = find_note_by_id(notes, note_id)
        if note is None:
            print("Note not found.")
            return
        choice = input("What do you want to edit? (text/tags): ").strip().lower()
        if choice == "text":
            note.text = input("Enter new text: ").strip()
        elif choice == "tags":
            note.tags = [tag.strip() for tag in input("Enter new tags (comma-separated): ").split(",")]
        save_notes(notes, config)
    except ValueError:
        print("Invalid input. Note ID must be an integer.")

# Function to delete a note
def delete_note(notes, config):
    try:
        note_id = int(input("Enter the ID of the note you want to delete: "))
        note = find_note_by_id(notes, note_id)
        if note is None:
            print("Note not found.")
            return
        notes.remove(note)
        save_notes(notes, config)
    except ValueError:
        print("Invalid input. Note ID must be an integer.")

# Function to find a note by ID
def find_note_by_id(notes, note_id):
    return next((note for note in notes if note.note_id == note_id), None)

# Function to show all notes in a tabular format
def show_all_notes(notes):
    if not notes:
        print("No notes found.")
    else:
        table = PrettyTable(["ID", "Text", "Tags"])
        for note in notes:
            table.add_row([note.note_id, note.text, ', '.join(note.tags)])
        print(table)

# Main function of the program
def main():
    config = configparser.ConfigParser()
    config_file = "config.ini"
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            f.write("[DEFAULT]\nnotes_file = notes.txt\n")
    config.read(config_file)
    notes = load_notes(config)
    
    while True:
        print("A1 - Add a note")
        print("A2 - Search notes")
        print("A3 - Edit a note")
        print("A4 - Delete a note")
        print("A5 - Show all notes")
        print("A0 - Finish")
        choice = input("Enter the command number: ").strip()
        
        if choice == "A1":
            add_note(notes, config)
        elif choice == "A2":
            results = search_notes(notes)
            show_all_notes(results)
        elif choice == "A3":
            edit_note(notes, config)
        elif choice == "A4":
            delete_note(notes, config)
        elif choice == "A5":
            show_all_notes(notes)
        elif choice == "A0":
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
