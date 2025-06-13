import tkinter as tk
import random

class UndertaleBlackjack:
    def __init__(self, root):
        self.root = root
        self.root.title("🃏 BLACKJACK – UNDERTALE STYLE 🖤")
        self.root.configure(bg="black")

        self.font = ("Courier New", 12, "bold")
        self.score = {"Player": 0, "Dealer": 0, "Tie": 0}
        self.player_hand = []
        self.dealer_hand = []

        # Title
        self.title = tk.Label(root, text="★ BLACKJACK ★", font=("Courier New", 20, "bold"), fg="white", bg="black")
        self.title.pack(pady=10)

        self.status = tk.Label(root, text="▶ Your Soul is in the cards...", font=self.font, fg="white", bg="black")
        self.status.pack(pady=5)

        # Hand displays
        self.player_label = tk.Label(root, text="", font=self.font, fg="white", bg="black")
        self.player_label.pack()

        self.dealer_label = tk.Label(root, text="", font=self.font, fg="white", bg="black")
        self.dealer_label.pack()

        # Buttons
        self.buttons = tk.Frame(root, bg="black")
        self.buttons.pack(pady=10)

        self.hit_btn = tk.Button(self.buttons, text="HIT", font=self.font, bg="black", fg="white",
                                 activebackground="white", activeforeground="black", command=self.hit)
        self.hit_btn.grid(row=0, column=0, padx=10)

        self.stand_btn = tk.Button(self.buttons, text="STAND", font=self.font, bg="black", fg="white",
                                   activebackground="white", activeforeground="black", command=self.stand)
        self.stand_btn.grid(row=0, column=1, padx=10)

        self.restart_btn = tk.Button(root, text="▶ PLAY AGAIN", font=self.font, bg="black", fg="white",
                                     activebackground="white", activeforeground="black", command=self.restart)
        self.restart_btn.pack(pady=5)

        # Scoreboard
        self.score_label = tk.Label(root, text="", font=self.font, fg="white", bg="black")
        self.score_label.pack(pady=5)

        self.restart()

    def draw_card(self):
        return random.choice(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])

    def card_value(self, card):
        return 11 if card == 'A' else 10 if card in ['J', 'Q', 'K'] else int(card)

    def total(self, hand):
        val = sum(self.card_value(card) for card in hand)
        aces = hand.count('A')
        while val > 21 and aces:
            val -= 10
            aces -= 1
        return val

    def update_display(self):
        p_total = self.total(self.player_hand)
        d_total = self.total(self.dealer_hand) if self.revealed else "??"
        d_hand = self.dealer_hand if self.revealed else ["??", self.dealer_hand[1]]

        self.player_label.config(text=f"PLAYER: {self.player_hand}  ▶ Total: {p_total}")
        self.dealer_label.config(text=f"DEALER: {d_hand}  ▶ Total: {d_total}")
        self.score_label.config(
            text=f"[ WINS: {self.score['Player']} | LOSSES: {self.score['Dealer']} | TIES: {self.score['Tie']} ]"
        )

    def hit(self):
        if self.total(self.player_hand) < 21:
            self.player_hand.append(self.draw_card())
            self.update_display()
            if self.total(self.player_hand) > 21:
                self.status.config(text="✖ You busted. You feel your soul fading...")
                self.score["Dealer"] += 1
                self.end_round()

    def stand(self):
        self.revealed = True
        while self.total(self.dealer_hand) < 17:
            self.dealer_hand.append(self.draw_card())

        p, d = self.total(self.player_hand), self.total(self.dealer_hand)

        if d > 21:
            self.status.config(text="✓ Dealer busted! You feel Determined.")
            self.score["Player"] += 1
        elif p > d:
            self.status.config(text="✓ You won! Your soul glows bright.")
            self.score["Player"] += 1
        elif p < d:
            self.status.config(text="✖ Dealer wins. A chill runs down your spine.")
            self.score["Dealer"] += 1
        else:
            self.status.config(text="◎ It's a tie... fate is undecided.")
            self.score["Tie"] += 1

        self.end_round()

    def end_round(self):
        self.hit_btn.config(state="disabled")
        self.stand_btn.config(state="disabled")
        self.update_display()

    def restart(self):
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]
        self.revealed = False
        self.status.config(text="▶ The cards are dealt. Your move.")
        self.hit_btn.config(state="normal")
        self.stand_btn.config(state="normal")
        self.update_display()

# Start the game
root = tk.Tk()
game = UndertaleBlackjack(root)
root.mainloop()
