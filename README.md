# 🐍 Snake Game

A modern and feature-rich Snake game built with Python Turtle graphics, featuring stunning visual effects, multiple difficulty levels, and engaging gameplay mechanics.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5.0-green.svg)
![Turtle](https://img.shields.io/badge/Turtle-Graphics-orange.svg)

## 🎮 Features

- **🎯 Multiple Difficulty Levels**
  - Easy: Simple gameplay with static obstacles
  - Medium: Added stationary hurdles
  - Hard: Moving obstacles that bounce around the screen

- **✨ Visual Effects**
  - Snake body wave animations
  - Color-changing segments when eating food
  - Eye and tongue movements
  - Screen shake effects on game over
  - Progress bars for special items

- **⚡ Game Mechanics**
  - Speed boost when moving in the same direction
  - Reverse mechanic when pressing opposite direction
  - Special food items with time-based bonuses
  - Increasing speed as you progress

- **🏆 Scoring System**
  - Real-time score display
  - High score tracking (top 3)
  - Bonus points for special food
  - Visual feedback for eating

- **🎵 Audio & Feedback**
  - Eating sound effects (with pygame)
  - System beeps and vibration effects
  - Visual feedback for all actions

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/snake-game.git
   cd snake-game
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt

   ```
3. **Run the game**
   ```bash
   python snake.py
   ```
   Online Play
- [snake Game](https://replit.com/@badarbhattpk786/snake-game)

- Click the badge above to play instantly in your browser!

## 🎯 Controls
**Movement**
- ↑ Arrow or W - Move Up

- ↓ Arrow or S - Move Down

- ← Arrow or A - Move Left

- → Arrow or D - Move Right

- **Game Actions**
- Spacebar - Pause/Resume game

- Mouse Click - Select menu buttons

- Same Direction - Speed boost

- Opposite Direction - Reverse snake

## 🎲 Game Modes
**Easy Mode**
- No obstacles

- Slower pace

- Perfect for beginners

**Medium Mode**
- Stationary hurdles

- Moderate speed

- Strategic navigation required

**Hard Mode**
- Moving obstacles

- Fast-paced gameplay

- Maximum challenge for experts

## 🍎 Food System
**Regular Food**
- Appears in random colors

I- ncreases score by 10 points

- Grows snake length by 10 segments

- Slightly increases game speed

  **Special Food (Black)**
- Spawns every 4 regular foods

- Time-based bonus points (50 + remaining time × 10)

- Grows snake by 20 segments

- Significant speed increase

- Progress bar shows time remaining

## 🎨 Visual Features
- Animated Snake Body: Wave-like movement throughout the body

- Dynamic Eyes: Eyes and pupils follow movement direction

- Extendable Tongue: Tongue extends when moving

- Color Effects: Snake segments change color based on eaten food

- Food Preview: Next food color shown in corner

- Screen Effects: Vibration and shaking on game over

## 🛠️ Technical Details
**Built With**
- Python 3 - Core programming language

- Turtle Graphics - Main graphics and animation engine

- Pygame - Sound effects and audio management

- Math Module - Precise movement calculations and wave animations

Project Structure
```bash
snake-game/
├── snake.py          # Main game file
├── requirements.txt  # Python dependencies
├── README.md        # This file
└── .gitignore       # Git ignore rules
```
**Dependencies**
- pygame==2.5.0 - For sound effects and audio playback


## 🐛 Known Issues
- Vibration Effects: May not work on all operating systems

- Sound Effects: Requires pygame and system audio support

- Window Shake: Dependent on turtle graphics implementation

## 🤝 Contributing
- Contributions are welcome! Feel free to:

- Report bugs and issues

- Suggest new features

- Submit pull requests

- Improve documentation

## 📝 License
- This project is open source and available under the MIT License.

## 👨‍💻 Developer
- Created with ❤️ using Python Turtle Graphics

- Enjoy the game! 🎉

- If you like this project, don't forget to give it a ⭐ on GitHub!



- ✅ Visual appeal with emojis and badges

- ✅ Clear installation instructions

- ✅ Comprehensive feature list

- ✅ Detailed controls and gameplay

- ✅ Technical documentation

- ✅ Online play option

- ✅ Professional structure
