# Flappy Bird AI using NEAT

This project implements an AI to play Flappy Bird using the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm. The AI evolves over multiple generations to improve its performance in navigating the bird through pipes. The project uses the **Pygame** library for game rendering and **NEAT-Python** for neural network evolution.

---

## 📂 Project Structure
```
├── imgs/
│   ├── bird1.png
│   ├── bird2.png
│   ├── bird3.png
│   ├── pipe.png
│   ├── base.png
│   └── bg.png
├── config-feedforward.txt
├── flappy_bird_neat.py
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Prerequisites
Ensure you have the following installed:
- **Python 3.6+**
- **Pygame:** `pip install pygame`
- **NEAT-Python:** `pip install neat-python`

---

### 2️⃣ Running the Game
1. Clone the repository or download the project files.
2. Ensure the `imgs` folder contains the necessary images (`bird1.png`, `bird2.png`, `bird3.png`, `pipe.png`, `base.png`, `bg.png`).
3. Run the game:
   ```bash
   python flappy_bird_neat.py
   ```
4. Watch the AI learn and evolve through generations.

---

## 🧠 How It Works
### NEAT Algorithm
The NEAT algorithm evolves neural networks by:
- Starting with simple networks.
- Mutating and crossing over genomes to improve performance.
- Using fitness scores to guide evolution.

### Fitness Function
- **+0.1** fitness for each frame the bird stays alive.
- **+5** fitness when successfully passing through pipes.
- **-1** fitness for colliding with a pipe.

### Neural Network Inputs
- Bird's vertical position.
- Distance to the next pipe's top.
- Distance to the next pipe's bottom.

### Output
- **> 0.5:** The bird jumps.
- **≤ 0.5:** No jump.

---

## 🕹️ Game Elements
### Classes:
- **Bird:** Handles bird movement, animation, and collision.
- **Pipe:** Manages pipe generation, movement, and collision detection.
- **Base:** Creates a scrolling base effect.
- **Main Loop:** Evolves birds, checks for collisions, updates the score, and renders the window.

---

## 🛠️ Configuration (`config-feedforward.txt`)
Modify the NEAT settings in `config-feedforward.txt` to change network structure, mutation rates, population size, etc.

Example settings:
```
[NEAT]
fitness_criterion = max
fitness_threshold = 10000
pop_size = 50
reset_on_extinction = False

[DefaultGenome]
num_inputs = 3
num_outputs = 1
activation_default = sigmoid
```

---

## 📊 Visualization & Stats
- Score and generation number displayed on the top of the game window.
- Evolutionary statistics output in the terminal.

---

## 🐞 Troubleshooting
- **Images not loading:** Ensure the `imgs` folder is in the same directory as the Python script.
- **Dependencies not found:** Verify Pygame and NEAT-Python are installed.
- **Slow performance:** Reduce population size or number of generations in the config.

---

## 📃 License
This project is for educational purposes. Feel free to modify and share.

---

## 🙌 Acknowledgements
- **NEAT-Python:** https://github.com/CodeReclaimers/neat-python
- **Flappy Bird Game Concept:** Inspired by the original Flappy Bird game.

🚀 Happy Coding and Good Luck evolving the best Flappy Bird AI! 🐦🎮

