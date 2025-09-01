
import tkinter as tk
import random
import time
import threading

# ASCII Art for Rock, Paper, Scissors
ASCII_ART = {
    "r": r"""
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
    """,
    "p": r"""
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
    """,
    "s": r"""
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
    """
}

CHOICES = {"Rock": "r", "Paper": "p", "Scissors": "s"}
WIN_MAP = {("r", "s"), ("p", "r"), ("s", "p")}


class RPSGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors")
        self.root.geometry("400x400")

        self.user_score = 0
        self.comp_score = 0
        self.rounds_played = 0
        self.max_rounds = 5

        self.label = tk.Label(root, text="Rock-Paper-Scissors", font=("Arial", 18, "bold"))
        self.label.pack(pady=10)

        self.result_label = tk.Label(root, text="Make your move!", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.score_label = tk.Label(root, text="Score -> You: 0  Computer: 0", font=("Arial", 12))
        self.score_label.pack(pady=10)

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=20)

        for choice in CHOICES.keys():
            tk.Button(self.buttons_frame, text=choice, width=12,
                      command=lambda c=choice: self.play_round(c)).pack(side=tk.LEFT, padx=5)

        self.final_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
        self.final_label.pack(pady=20)

    def play_round(self, user_choice):
        if self.rounds_played >= self.max_rounds:
            return

        user = CHOICES[user_choice]
        comp = random.choice(list(CHOICES.values()))

        # Start animation in a new popup window
        threading.Thread(target=self.show_ascii_animation, args=(user, comp)).start()

    def show_ascii_animation(self, user, comp):
        popup = tk.Toplevel(self.root)
        popup.title("Computer Choosing...")
        popup.geometry("500x300")

        text_box = tk.Text(popup, font=("Courier", 12), bg="black", fg="lime")
        text_box.pack(expand=True, fill="both")

        # Animation loop (cycling ASCII rapidly)
        frames = list(ASCII_ART.values())
        for _ in range(15):  # 15 cycles = illusion
            for art in frames:
                text_box.delete("1.0", tk.END)
                text_box.insert(tk.END, art)
                popup.update()
                time.sleep(0.1)

        # Stop at computer's real choice
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, ASCII_ART[comp])

        # Decide winner
        winner = self.decide_winner(user, comp)
        if winner == "user":
            self.user_score += 1
            result_text = f"You WIN this round!"
        elif winner == "comp":
            self.comp_score += 1
            result_text = f"Computer WINS this round!"
        else:
            result_text = f"It's a TIE!"

        self.rounds_played += 1

        # Show round result in popup
        result_label = tk.Label(popup, text=result_text, font=("Arial", 14, "bold"), fg="yellow")
        result_label.pack(pady=10)

        # Update main GUI
        self.result_label.config(text=f"Your choice vs Computer decided!")
        self.score_label.config(text=f"Score -> You: {self.user_score}  Computer: {self.comp_score}")

        if self.rounds_played == self.max_rounds:
            self.end_game()

    def decide_winner(self, user, comp):
        if user == comp:
            return "tie"
        elif (user, comp) in WIN_MAP:
            return "user"
        return "comp"

    def end_game(self):
        if self.user_score > self.comp_score:
            final_text = f"🎉 You win the game! {self.user_score} to {self.comp_score}"
        elif self.comp_score > self.user_score:
            final_text = f"💻 Computer wins! {self.comp_score} to {self.user_score}"
        else:
            final_text = f"🤝 It's a tie: {self.user_score} to {self.comp_score}"
        self.final_label.config(text=final_text)


if __name__ == "__main__":
    root = tk.Tk()
    game = RPSGameGUI(root)
    root.mainloop()
