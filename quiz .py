import tkinter as tk
from tkinter import messagebox

# ----------------- QUIZ DATA -----------------
questions = [
    {"q": "Which of these is a Python keyword?",
     "options": ["range", "def", "Val", "loop"], "answer": "def"},

    {"q": "Which of the following is a built-in function in Python?",
     "options": ["factorial()", "print()", "sqrt()", "seed()"], "answer": "print()"},

    {"q": "Which is NOT a core data type in Python?",
     "options": ["Tuple", "Dictionary", "Lists", "Class"], "answer": "Class"},

    {"q": "Who developed Python programming language?",
     "options": ["Wick Van Rossum", "Rasmus Lerdorf", "Guido Van Rossum", "Niene Stom"],
     "answer": "Guido Van Rossum"},

    {"q": "What is the correct extension for Python files?",
      "options": [".py", ".python", ".p", ".pl"], "answer": ".py"},

    {"q": "What does the len() function return?",
     "options": ["Number of items", "Length in cm", "Memory size", "None of these"],
     "answer": "Number of items"},

    {"q": "Which operator is used for floor division?",
     "options": ["/", "//", "%", "**"], "answer": "//"},

    {"q": "Default value of 'end' in print() is?",
     "options": ["space", "tab", "newline (\\n)", "None"], "answer": "newline (\\n)"},

    {"q": "Which of the following is immutable?",
     "options": ["List", "Set", "Tuple", "Dictionary"], "answer": "Tuple"},

    {"q": "Which statement is used to handle exceptions?",
     "options": ["catch", "try-except", "error", "handle"], "answer": "try-except"},
]

# ----------------- APP -----------------
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quiz")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)

        # State
        self.username = ""
        self.score = 0
        self.q_index = 0

        # Timer state
        self.time_per_question = 30
        self.time_left = self.time_per_question
        self.timer_job = None  # holds .after() id so we can cancel

        # --- Layout containers ---
        # Top bar (persistent)
        self.topbar = tk.Frame(self.root, pady=8)
        self.topbar.pack(fill="x")
        self.title_lbl = tk.Label(self.topbar, text="🐍 Python Quiz", font=("Arial", 22, "bold"))
        self.title_lbl.pack(side="left", padx=12)

        self.exit_btn = tk.Button(self.topbar, text="Exit", font=("Arial", 12), command=self.on_exit)
        self.exit_btn.pack(side="right", padx=12)

        # Main content area (switches screens)
        self.main = tk.Frame(self.root)
        self.main.pack(expand=True, fill="both", padx=20, pady=10)

        self.show_welcome()

    # ---------- Screens ----------
    def show_welcome(self):
        self.clear_main()

        tk.Label(self.main, text="Welcome!", font=("Arial", 34, "bold")).pack(pady=20)
        tk.Label(self.main, text="Enter your name:", font=("Arial", 18)).pack(pady=(10, 4))

        self.name_entry = tk.Entry(self.main, font=("Arial", 18), justify="center")
        self.name_entry.pack(pady=8)
        self.name_entry.focus_set()

        tk.Button(self.main, text="Start Quiz", font=("Arial", 18),
                  command=self.start_quiz).pack(pady=18)

    def load_question(self):
        self.clear_main()
        if self.q_index >= len(questions):
            self.show_result()
            return

        q = questions[self.q_index]

        # Timer label (top of question)
        self.timer_lbl = tk.Label(self.main, text=f"Time left: {self.time_per_question} s",
                                  font=("Arial", 16), fg="red")
        self.timer_lbl.pack(pady=(5, 0))

        # Question text
        self.q_lbl = tk.Label(self.main,
                              text=f"Q{self.q_index + 1}. {q['q']}",
                              font=("Arial", 22),
                              wraplength=820,
                              justify="left")
        self.q_lbl.pack(pady=30)

        # Options
        self.opt_btns = []
        for opt in q["options"]:
            btn = tk.Button(self.main, text=opt, font=("Arial", 18), width=28,
                            command=lambda choice=opt: self.on_answer(choice))
            btn.pack(pady=6)
            self.opt_btns.append(btn)

        # Start/Reset the timer cleanly
        self.start_timer()

    def show_result(self):
        self.stop_timer()
        self.clear_main()
        msg = f"🎉 Well done, {self.username}!\n\nYour Score: {self.score}/{len(questions)}"
        tk.Label(self.main, text=msg, font=("Arial", 28), fg="green", justify="center").pack(pady=40)

        tk.Button(self.main, text="Restart", font=("Arial", 16),
                  command=self.restart_quiz).pack(pady=6)

    # ---------- Timer ----------
    def start_timer(self):
        """Start a fresh 30s timer and ensure any old timer is cancelled."""
        self.stop_timer()
        self.time_left = self.time_per_question
        self.update_timer_label()
        # schedule first tick after 1 second
        self.timer_job = self.root.after(1000, self._tick)

    def _tick(self):
        """Called every second while the question is active."""
        self.time_left -= 1
        if self.time_left <= 0:
            self.update_timer_label(0)
            self.timer_job = None
            self.on_time_up()
        else:
            self.update_timer_label()
            self.timer_job = self.root.after(1000, self._tick)

    def update_timer_label(self, val=None):
        if hasattr(self, "timer_lbl") and self.timer_lbl.winfo_exists():
            seconds = self.time_left if val is None else val
            self.timer_lbl.config(text=f"Time left: {seconds} s")

    def stop_timer(self):
        """Cancel any scheduled tick before changing screen."""
        if self.timer_job is not None:
            try:
                self.root.after_cancel(self.timer_job)
            except Exception:
                pass
            self.timer_job = None

    # ---------- Events ----------
    def start_quiz(self):
        name = getattr(self, "name_entry", None).get().strip() if hasattr(self, "name_entry") else ""
        if not name:
            messagebox.showwarning("Name required", "Please enter your name to start.")
            return
        self.username = name
        self.q_index = 0
        self.score = 0
        self.load_question()

    def on_answer(self, choice):
        # Stop timer immediately to avoid overlaps
        self.stop_timer()
        correct = questions[self.q_index]["answer"]
        if choice == correct:
            self.score += 1
        self.q_index += 1
        self.load_question()

    def on_time_up(self):
        # Time up: move to next question without changing score
        self.q_index += 1
        self.load_question()

    def restart_quiz(self):
        self.stop_timer()
        self.score = 0
        self.q_index = 0
        self.show_welcome()

    def on_exit(self):
        self.stop_timer()
        self.root.destroy()

    # ---------- Helpers ----------
    def clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()


# ----------------- RUN -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
