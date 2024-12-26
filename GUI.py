import tkinter
from tkinter import messagebox
from quiz_brain import QuizBrain
import random
import html

BACKGROUND = "#1F316F"
FONT_NAME = "Aptos"
RED = "#821131"
GREEN = "#A5DD9B"


class UserInterface:

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("My QUIZ.")
        self.window.config(padx=20, pady=20, bg=BACKGROUND)

        img_yes = tkinter.PhotoImage(file="true.png")
        self.yes_button = tkinter.Button(image=img_yes, command=self.click_yes)
        self.yes_button.grid(column=0, row=5)

        img_no = tkinter.PhotoImage(file="false.png")
        self.no_button = tkinter.Button(image=img_no, command=self.click_no)
        self.no_button.grid(column=2, row=5)

        img_a = tkinter.PhotoImage(file="A_letter.png")
        self.a_button = tkinter.Button(image=img_a, command=self.check_a)
        self.a_button.grid_forget()

        img_b = tkinter.PhotoImage(file="B_letter.png")
        self.b_button = tkinter.Button(image=img_b, command=self.check_b)
        self.b_button.grid_forget()

        img_c = tkinter.PhotoImage(file="C_letter.png")
        self.c_button = tkinter.Button(image=img_c, command=self.check_c)
        self.c_button.grid_forget()

        img_d = tkinter.PhotoImage(file="D_letter.png")
        self.d_button = tkinter.Button(image=img_d, command=self.check_d)
        self.d_button.grid_forget()

        self.score = 0
        self.score_label = tkinter.Label(text=f"{self.score} points.",
                                         bg=BACKGROUND, fg=BACKGROUND,
                                         font=(FONT_NAME, 20, "bold"))
        self.score_label.grid(column=2, row=0)

        ghost_label = tkinter.Label(text="", font=(FONT_NAME, 24, "bold"), bg=BACKGROUND)
        ghost_label.grid(column=0, row=4)

        ghost_label_2 = tkinter.Label(text="", font=(FONT_NAME, 24, "bold"), bg=BACKGROUND)
        ghost_label_2.grid(column=0, row=1)

        self.ghost_label_3 = tkinter.Label(text="", font=(FONT_NAME, 24, "bold"), bg=BACKGROUND)

        self.canvas = tkinter.Canvas(width=300, height=300, bg="white", highlightthickness=0)
        self.texto_canvas = self.canvas.create_text(150, 150, text="Press ✔ to begin.",
                                                    fill="black", font=(FONT_NAME, 16, "bold"), width=280)
        self.canvas.grid(row=2, column=0, columnspan=3)

        self.brain = QuizBrain()
        self.question_deck = []
        self.this_question = {}
        self.deck_length = 0
        self.possible_answers = []

        self.window.mainloop()

    def click_yes(self):
        self.question_deck = self.brain.new_questions()
        self.first_question()

    def first_question(self):
        self.this_question = {}
        self.deck_length = len(self.question_deck["results"])
        self.score_label.config(bg="white")
        self.next_question()

    def click_no(self):
        self.window.destroy()

    def next_question(self):
        try:
            self.this_question = random.choice(self.question_deck["results"])
            index = self.question_deck["results"].index(self.this_question)
            self.question_deck["results"].pop(index)
            if self.this_question["type"] == "multiple":
                self.mode_multiple()
                self.possible_answers = self.this_question["incorrect_answers"]
                self.possible_answers.append(self.this_question["correct_answer"])
                random.shuffle(self.possible_answers)
                letters = ["A", "B", "C", "D"]
                multiple_text = self.this_question["question"] + "\n"
                for i in range(4):
                    multiple_text += f"\n{letters[i]}. {self.possible_answers[i]}."
                    self.canvas.itemconfig(self.texto_canvas, text=html.unescape(multiple_text))
            else:
                self.canvas.itemconfig(self.texto_canvas, text=html.unescape(self.this_question["question"]))
                self.mode_boolean()
        except IndexError:
            self.buttons_off()
            self.game_completed()
        except TypeError:
            pass

    def buttons_off(self):
        pass
        self.a_button.config(command=None)
        self.b_button.config(command=None)
        self.c_button.config(command=None)
        self.d_button.config(command=None)
        self.yes_button.config(command=None)
        self.no_button.config(command=None)

    def game_completed(self):
        click = messagebox.askyesno("You finished your question deck!",
                                    f"""You got {self.score} points out of {self.deck_length} questions.
    Do you want play again?""")
        if click is False:
            self.window.destroy()
        else:
            self.back_to_menu()

    def back_to_menu(self):
        self.score = 0
        self.score_label.configure(text=f"{self.score} points.")
        self.mode_boolean()
        self.yes_button.config(command=self.click_yes)
        self.no_button.config(command=self.click_no)
        self.this_question = {}
        self.deck_length = 0
        self.question_deck = []
        self.score_label.config(bg=BACKGROUND)
        self.canvas.itemconfig(self.texto_canvas, text="Press ✔ to begin.")

    def mode_multiple(self):
        self.yes_button.grid_forget()
        self.no_button.grid_forget()
        self.a_button.grid(column=0, row=5)
        self.b_button.grid(column=2, row=5)
        self.ghost_label_3.grid(column=0, row=6)
        self.c_button.grid(column=0, row=7)
        self.d_button.grid(column=2, row=7)

    def mode_boolean(self):
        self.a_button.grid_forget()
        self.b_button.grid_forget()
        self.c_button.grid_forget()
        self.d_button.grid_forget()
        self.ghost_label_3.grid_forget()
        self.yes_button.config(command=self.check_yes)
        self.yes_button.grid(column=0, row=5)
        self.no_button.config(command=self.check_no)
        self.no_button.grid(column=2, row=5)

    def show_result(self, status):
        if status == "right":
            self.canvas.configure(bg="green")
            self.window.update()
            self.window.after(100)
            self.canvas.configure(bg="white")
            self.score += 1
            self.score_label.config(text=f"{self.score} points.")
            self.next_question()
        else:
            self.canvas.configure(bg="red")
            self.window.update()
            self.window.after(100)
            self.canvas.configure(bg="white")
            self.next_question()

    def check_yes(self):
        self.buttons_off()
        if self.this_question["correct_answer"] == "True":
            self.show_result("right")
        else:
            self.show_result("")

    def check_no(self):
        self.buttons_off()
        if self.this_question["correct_answer"] == "True":
            self.show_result("")
        else:
            self.show_result("right")

    def check_a(self):
        self.buttons_off()
        if self.possible_answers[0] == self.this_question["correct_answer"]:
            self.show_result("right")
        else:
            self.show_result("")

    def check_b(self):
        self.buttons_off()
        if self.possible_answers[1] == self.this_question["correct_answer"]:
            self.show_result("right")
        else:
            self.show_result("")

    def check_c(self):
        self.buttons_off()
        if self.possible_answers[2] == self.this_question["correct_answer"]:
            self.show_result("right")
        else:
            self.show_result("")

    def check_d(self):
        self.buttons_off()
        if self.possible_answers[3] == self.this_question["correct_answer"]:
            self.show_result("right")
        else:
            self.show_result("")
