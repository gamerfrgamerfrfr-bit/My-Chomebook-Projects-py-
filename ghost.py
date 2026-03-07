import random
import time
import os
import sys
from datetime import datetime

SAVE_FILE = "phasmo_pro_v3.txt"

# --- GHOST DATA ---
GHOST_HANDBOOK = {
    "Spirit": ["EMF 5", "Spirit Box", "Ghost Writing"],
    "Wraith": ["EMF 5", "Spirit Box", "D.O.T.S"],
    "Phantom": ["Spirit Box", "Ultraviolet", "D.O.T.S"],
    "Poltergeist": ["Spirit Box", "Ultraviolet", "Ghost Writing"],
    "Banshee": ["Ghost Orb", "Ultraviolet", "D.O.T.S"],
    "Demon": ["Ultraviolet", "Ghost Writing", "Freezing Temps"],
    "Revenant": ["Ghost Orb", "Ghost Writing", "Freezing Temps"],
    "Shade": ["EMF 5", "Ghost Writing", "Freezing Temps"],
    "Oni": ["EMF 5", "Freezing Temps", "D.O.T.S"]
}

class Player:
    def __init__(self):
        self.money, self.xp, self.level, self.prestige = 100, 0, 1, 0
        self.tiers = {"Thermometer": 1, "EMF": 1, "Camera": 1}
        self.load_game()

    def save_game(self):
        with open(SAVE_FILE, "w") as f:
            f.write(f"{self.money},{self.xp},{self.level},{self.prestige}\n")
            f.write(",".join([f"{k}:{v}" for k, v in self.tiers.items()]))

    def load_game(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    lines = f.readlines()
                    s = lines[0].strip().split(",")
                    self.money, self.xp, self.level, self.prestige = map(int, s)
                    for pair in lines[1].strip().split(","):
                        k, v = pair.split(":")
                        self.tiers[k] = int(v)
            except: pass

class Investigation:
    def __init__(self, p):
        self.p = p
        self.rooms = ["Foyer", "Kitchen", "Basement", "Attic", "Garage"]
        self.ghost_room = random.choice(self.rooms)
        self.ghost_type = random.choice(list(GHOST_HANDBOOK.keys()))
        self.evidence_pool = list(GHOST_HANDBOOK[self.ghost_type])
        self.found_clues = []
        self.sanity = 100
        self.location = "Van"

    def show_handbook(self):
        print(f"\n{'='*10} 📖 INVESTIGATOR HANDBOOK {'='*10}")
        for ghost, ev_list in GHOST_HANDBOOK.items():
            display_ev = []
            for ev in ev_list:
                # Mark off evidence already found
                mark = "[✓]" if ev in self.found_clues else "[ ]"
                display_ev.append(f"{mark} {ev}")
            print(f"{ghost.ljust(12)}: {', '.join(display_ev)}")
        print('='*40)

    def run(self):
        print(f"\n[CONTRACT] Find the entity. Possible rooms: {', '.join(self.rooms)}")
        while self.sanity > 0:
            print(f"\nLocation: {self.location} | Sanity: {int(self.sanity)}%")
            act = input("[Move] [Investigate] [Photo] [Monkey Paw] [Handbook] [Guess]: ").lower()

            if act == "move":
                new_loc = input(f"Go to ({', '.join(self.rooms)} or Van): ").title()
                if new_loc in self.rooms or new_loc == "Van":
                    self.location = new_loc
                    if self.location != "Van": self.sanity -= 5
            
            elif act == "handbook":
                self.show_handbook()

            elif act == "investigate":
                if self.location == "Van": continue
                print(f"Using T{self.p.tiers['EMF']} EMF...")
                if self.location == self.ghost_room:
                    if random.random() < (0.3 * self.p.tiers["EMF"]) and self.evidence_pool:
                        ev = self.evidence_pool.pop(random.randrange(len(self.evidence_pool)))
                        self.found_clues.append(ev)
                        print(f"✨ FOUND EVIDENCE: {ev}")
                    else: print("No activity.")
                else: print("The room is quiet.")
                self.sanity -= (10 / self.p.tiers["Thermometer"])

            elif act == "photo":
                dist = 0.5 if self.location == self.ghost_room else 10.0
                stars = 3 if dist < 2 else 1
                reward = int(stars * 20 * self.p.tiers["Camera"])
                self.p.money += reward
                print(f"📸 {stars}-Star Photo! +${reward}")

            elif act == "monkey paw":
                self.sanity -= 30
                if self.evidence_pool:
                    ev = self.evidence_pool.pop(0)
                    self.found_clues.append(ev)
                    print(f"🐵 The paw curls... You know of: {ev}")
                print("The ghost is angered.")

            elif act == "guess":
                g = input("Identify the ghost: ").title()
                if g == self.ghost_type:
                    payout = 150 * (1 + self.p.prestige)
                    self.p.money += int(payout)
                    print(f"✅ CORRECT! It was a {self.ghost_type}. Payout: ${int(payout)}")
                else: print(f"❌ WRONG! It was a {self.ghost_type}.")
                break
        
        self.p.save_game()

def main():
    player = Player()
    while True:
        print(f"\nLVL {player.level} | PRESTIGE {player.prestige} | $: {player.money}")
        choice = input("1. Hunt  2. Shop  3. Handbook  4. Exit: ")
        if choice == "1": Investigation(player).run()
        elif choice == "2":
            print(f"\n--- UPGRADES (Current Tiers: {player.tiers}) ---")
            up = input("Upgrade (Thermometer/EMF/Camera) - $200: ").title()
            if up in player.tiers and player.money >= 200:
                player.money -= 200
                player.tiers[up] += 1
                player.save_game()
        elif choice == "3": Investigation(player).show_handbook()
        elif choice == "4": break

if __name__ == "__main__": main()
