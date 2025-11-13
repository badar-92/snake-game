import turtle
import time
import math
import random
import pygame
import platform

# Initialize pygame for sound
pygame.mixer.init()

# Screen setup
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("#cceecd")
screen.setup(width=1000, height=600)
screen.tracer(0)

# vibration helper (only addition)
def vibrate_system():
    # Beep sound
    if platform.system() == "Windows":
        try:
            import winsound
            for i in range(3):
                winsound.Beep(600, 120)
        except:
            pass
    else:
        for i in range(3):
            print("\a")
            time.sleep(0.1)

    # Window shake (best-effort; may not work on all systems)
    try:
        canvas = screen.getcanvas().winfo_toplevel()
        x, y = canvas.winfo_x(), canvas.winfo_y()
        for i in range(6):
            offset = 15 if i % 2 == 0 else -15
            canvas.geometry(f"+{x + offset}+{y}")
            screen.update()
            time.sleep(0.05)
        canvas.geometry(f"+{x}+{y}")
    except:
        pass

# Game states
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3

# Global variables
game_state = MENU
difficulty = None
score = 0
high_scores = [0, 0, 0]
last_score = 0
paused = False
normal_step = 6
max_length = 40
positions = []
angle = 0
wave_amplitude = 6
wave_frequency = 0.25
boost_level = 1
food_bumps = []
current_body_color = "lightgreen"
food_counter = 0
delay = 0.03
buttons = []
hurdles = []

# Special food variables (added)
special_food = turtle.Turtle()
special_food.shape("circle")
special_food.color("black")
special_food.shapesize(1.8, 1.8)
special_food.penup()
special_food.hideturtle()

special_food_active = False
special_food_start_time = 0
special_food_duration = 10  # seconds

progress_bar = turtle.Turtle()
progress_bar.hideturtle()
progress_bar.speed(0)
progress_bar.pensize(6)
progress_bar.color("black")


# Try to load sound
try:
    eating_sound = pygame.mixer.Sound("eat-323883.mp3")
except:
    eating_sound = None

# Create turtle objects
head = turtle.Turtle()
head.shape("circle")
head.color("darkgreen")
head.shapesize(1.3, 1.3)
head.penup()
head.goto(0, 0)

# Preview of next food
next_food_preview = turtle.Turtle()
next_food_preview.shape("circle")
next_food_preview.penup()
next_food_preview.hideturtle()
next_food_color = None


# Create mouth shape
def create_mouth_shape():
    poly = turtle.Shape("compound")
    mouth = [(0, 0)]
    for a in range(110, 430):
        x = 20 * math.cos(math.radians(a))
        y = 20 * math.sin(math.radians(a))
        mouth.append((x, y))
    poly.addcomponent(mouth, "darkgreen")
    try:
        turtle.register_shape("open_mouth", poly)
    except:
        pass

create_mouth_shape()

# Eyes and pupils
eye1 = turtle.Turtle()
eye1.shape("circle")
eye1.color("white")
eye1.shapesize(0.35, 0.35)
eye1.penup()

eye2 = turtle.Turtle()
eye2.shape("circle")
eye2.color("white")
eye2.shapesize(0.35, 0.35)
eye2.penup()

pupil1 = turtle.Turtle()
pupil1.shape("square")
pupil1.color("black")
pupil1.shapesize(0.25, 0.1)
pupil1.penup()

pupil2 = turtle.Turtle()
pupil2.shape("square")
pupil2.color("black")
pupil2.shapesize(0.25, 0.1)
pupil2.penup()

# Tongue
tongue = turtle.Turtle()
tongue.shape("square")
tongue.color("red")
tongue.shapesize(0.1, 0.6)
tongue.penup()

# Body
body = turtle.Turtle()
body.shape("circle")
body.penup()
body.hideturtle()

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food_colors = ["red", "blue", "orange", "yellow", "cyan", "magenta", "brown", "pink"]

# Score display
pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

# Menu turtle
menu_turtle = turtle.Turtle()
menu_turtle.hideturtle()
menu_turtle.penup()

# Button class for menu items
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback
        self.visible = False
        
        # Create text turtle
        self.text_turtle = turtle.Turtle()
        self.text_turtle.hideturtle()
        self.text_turtle.penup()
        # center text
        self.text_turtle.goto(x + width/2, y - height/2 - 5)

        # Create clickable area (outline only)
        self.click_area = turtle.Turtle()
        self.click_area.shape("square")
        self.click_area.shapesize(height/20, width/20)
        self.click_area.pensize(3)
        self.click_area.color("black")  # outline
        self.click_area.penup()
        self.click_area.goto(x + width/2, y - height/2)
        # transparent fill (turtle has no direct transparent fill method; keep default)
        try:
            self.click_area.fillcolor("")
        except:
            pass

        # Set up click handler
        self.click_area.onclick(lambda x, y: callback())
        
    def show(self):
        self.text_turtle.clear()
        self.text_turtle.write(self.text, align="center", font=("Arial", 16, "bold"))
        self.click_area.showturtle()
        self.visible = True
        
    def hide(self):
        self.text_turtle.clear()
        self.click_area.hideturtle()
        self.visible = False


# Game functions
def place_food_safe():
    global next_food_color
    attempts = 0
    while True:
        attempts += 1
        x = random.randint(-460, 460)
        y = random.randint(-260, 260)
        safe = True
        
        for h in hurdles:
            if abs(x - h.xcor()) < 80 and abs(y - h.ycor()) < 40:
                safe = False
                break
                
        if safe:
            food.goto(x, y)
            if next_food_color is None:
                food.color(random.choice(food_colors))
            else:
                food.color(next_food_color)

            # Pick next preview color
            next_food_color = random.choice(food_colors)
            next_food_preview.goto(430, -270)  # bottom-right corner
            next_food_preview.color(next_food_color)
            next_food_preview.showturtle()
            break
            
        if attempts > 300:
            food.goto(0, 0)
            if next_food_color is None:
                food.color(random.choice(food_colors))
            else:
                food.color(next_food_color)

            next_food_color = random.choice(food_colors)
            next_food_preview.goto(430, -270)
            next_food_preview.color(next_food_color)
            next_food_preview.showturtle()
            break

def init_hurdles_for_difficulty(diff):
    global hurdles
    
    # Clear old hurdles
    for h in hurdles:
        h.hideturtle()
        h.clear()
    
    hurdles = []
    
    if diff == "medium":
        coords = [(-220, 0), (-60, 80), (60, -80), (220, 0)]
        for c in coords:
            h = turtle.Turtle()
            h.shape("square")
            h.color("gray")
            h.shapesize(1, 4)
            h.penup()
            h.goto(c)
            h.dx = 0
            h.dy = 0
            hurdles.append(h)
    elif diff == "hard":
        coords = [(-180, 0), (180, 0), (0, 120)]
        for c in coords:
            h = turtle.Turtle()
            h.shape("square")
            h.color("gray")
            h.shapesize(1, 5)
            h.penup()
            h.goto(c)
            h.dx = random.choice([-2, 2])
            h.dy = random.choice([-2, 2])
            hurdles.append(h)

def update_score_display():
    pen.clear()
    pen.write(f"Score: {score}  Boost: x{boost_level}  High Scores: {high_scores[0]} {high_scores[1]} {high_scores[2]}",
              align="center", font=("Courier", 18, "normal"))

def reverse_snake():
    global positions, angle, food_bumps, boost_level
    
    if len(positions) > 0:
        L = len(positions)
        for bump in food_bumps:
            bump["index"] = L - 1 - bump.get("index", 0)
        positions.reverse()
        head.goto(positions[0][0], positions[0][1])
    
    angle = (angle + 180) % 360
    if angle == 270:
        angle = -90
    
    boost_level = 1

def set_direction(new_angle):
    global angle, boost_level
    
    if game_state != PLAYING:
        return
        
    if angle == new_angle:
        boost_level += 1
    elif (angle == 0 and new_angle == 180) or (angle == 180 and new_angle == 0) or \
         (angle == 90 and new_angle == -90) or (angle == -90 and new_angle == 90):
        reverse_snake()
        update_score_display()
    else:
        angle = new_angle
        boost_level = 1

def go_up():
    set_direction(90)

def go_down():
    set_direction(-90)

def go_left():
    set_direction(180)

def go_right():
    set_direction(0)

def toggle_pause():
    global game_state, paused
    
    if game_state == PLAYING:
        game_state = PAUSED
        paused = True
        show_pause_menu()
    elif game_state == PAUSED:
        game_state = PLAYING
        paused = False
        clear_menu()

def move():
    global positions, food_bumps, current_body_color
    
    step = normal_step * boost_level
    x = head.xcor() + step * math.cos(math.radians(angle))
    y = head.ycor() + step * math.sin(math.radians(angle))
    
    t = time.time()
    shake = 2 * math.sin(t * 6)
    wx = x + shake * math.cos(math.radians(angle + 90))
    wy = y + shake * math.sin(math.radians(angle + 90))
    
    head.goto(wx, wy)
    head.setheading(angle)

    # Update eyes and pupils
    eye1.goto(wx + 10 * math.cos(math.radians(angle + 40)), wy + 10 * math.sin(math.radians(angle + 40)))
    eye2.goto(wx + 10 * math.cos(math.radians(angle - 40)), wy + 10 * math.sin(math.radians(angle - 40)))
    pupil1.goto(eye1.xcor(), eye1.ycor())
    pupil2.goto(eye2.xcor(), eye2.ycor())
    
    # Update tongue
    tongue.goto(wx + 18 * math.cos(math.radians(angle)), wy + 18 * math.sin(math.radians(angle)))
    tongue.setheading(angle)

    # Add new positions
    steps_to_add = max(1, int(round(step / normal_step)))
    dx = step * math.cos(math.radians(angle))
    dy = step * math.sin(math.radians(angle))
    
    for i in range(steps_to_add):
        frac = (i + 1) / steps_to_add
        ix = wx - dx * (1 - frac)
        iy = wy - dy * (1 - frac)
        positions.insert(0, (ix, iy))
    
    # Remove old positions if exceeding max length
    while len(positions) > max_length:
        positions.pop()

    # Update food bumps
    new_bumps = []
    for bump in food_bumps:
        bump["index"] += 1
        if bump["index"] < len(positions):
            new_bumps.append(bump)
    
    food_bumps = new_bumps

    # Draw body segments
    body.clearstamps()
    
    for i, pos in enumerate(positions):
        if i < len(positions) - 1:
            seg_angle = math.degrees(math.atan2(positions[i][1] - positions[i+1][1],
                                                positions[i][0] - positions[i+1][0]))
        else:
            seg_angle = angle
        
        wave = wave_amplitude * math.sin(t - i * wave_frequency * 4)
        bx = pos[0] + wave * math.cos(math.radians(seg_angle + 90))
        by = pos[1] + wave * math.sin(math.radians(seg_angle + 90))
        
        body.goto(bx, by)
        scale = max(0.05, 1.2 - (i / max_length) * 1.15)
        body.color(current_body_color)
        
        if any(b["index"] == i for b in food_bumps):
            body.shapesize(scale * 2, scale * 2)
        elif any(b["index"] in [i-1, i+1] for b in food_bumps):
            body.shapesize(scale * 1.5, scale * 1.5)
        else:
            body.shapesize(scale, scale)
        
        body.stamp()

def move_hurdles():
    for h in hurdles:
        if hasattr(h, 'dx') and hasattr(h, 'dy'):
            if h.dx != 0 or h.dy != 0:
                h.setx(h.xcor() + h.dx)
                h.sety(h.ycor() + h.dy)
                
                if abs(h.xcor()) > 450:
                    h.dx *= -1
                if abs(h.ycor()) > 250:
                    h.dy *= -1

def reset_game_state():
    global score, positions, max_length, delay, food_bumps, current_body_color, boost_level, angle, food_counter, normal_step
    
    score = 0
    food_bumps = []
    current_body_color = "lightgreen"
    boost_level = 1
    positions = []
    angle = 0
    max_length = 40
    food_counter = 0
    
    if difficulty == "easy":
        delay = 0.06
        normal_step = 6
    elif difficulty == "medium":
        delay = 0.045
        normal_step = 6
    else:
        delay = 0.03
        normal_step = 6

    head.goto(0, 0)
    body.clearstamps()
    eye1.goto(0, 0)
    eye2.goto(0, 0)
    pupil1.goto(0, 0)
    pupil2.goto(0, 0)
    tongue.goto(0, 0)
    
    positions.append((head.xcor(), head.ycor()))
    update_score_display()

def start_game(diff):
    global game_state, difficulty, paused
    
    difficulty = diff
    game_state = PLAYING
    paused = False
    clear_menu()
    init_hurdles_for_difficulty(diff)
    reset_game_state()
    place_food_safe()

def game_over():
    global game_state, last_score, high_scores
    
    last_score = score
    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:3]
    
    vibrate_system()

    game_state = GAME_OVER
    show_game_over_menu()

# Menu functions
def clear_menu():
    menu_turtle.clear()
    for btn in buttons:
        btn.hide()
    buttons.clear()

def show_main_menu():
    global game_state
    game_state = MENU
    clear_menu()
    
    menu_turtle.goto(0, 150)
    menu_turtle.write("Snake Game", align="center", font=("Courier", 28, "bold"))
    
    buttons.append(Button(-60, 50, 120, 40, "Easy", lambda: start_game("easy")))
    buttons.append(Button(-60, -10, 120, 40, "Medium", lambda: start_game("medium")))
    buttons.append(Button(-60, -70, 120, 40, "Hard", lambda: start_game("hard")))
    
    for btn in buttons:
        btn.show()

def show_pause_menu():
    clear_menu()
    
    menu_turtle.goto(0, 150)
    menu_turtle.write("Paused", align="center", font=("Courier", 28, "bold"))
    
    buttons.append(Button(-60, 50, 120, 40, "Resume", toggle_pause))
    buttons.append(Button(-60, -10, 120, 40, "Restart", lambda: start_game(difficulty)))
    buttons.append(Button(-60, -70, 120, 40, "Main Menu", show_main_menu))
    
    for btn in buttons:
        btn.show()

def show_game_over_menu():
    clear_menu()
    
    menu_turtle.goto(0, 150)
    menu_turtle.write("Game Over", align="center", font=("Courier", 28, "bold"))
    
    menu_turtle.goto(0, 100)
    menu_turtle.write(f"Score: {last_score}", align="center", font=("Courier", 18, "normal"))
    
    buttons.append(Button(-60, 0, 120, 40, "Play Again", lambda: start_game(difficulty)))
    buttons.append(Button(-60, -60, 120, 40, "Main Menu", show_main_menu))
    
    for btn in buttons:
        btn.show()

# Special food helper functions (added) - progress bar drawn at bottom (y = -280)
def place_special_food():
    global special_food_active, special_food_start_time
    # try to place special food in a safe location (not overlapping hurdles)
    attempts = 0
    while True:
        attempts += 1
        x = random.randint(-420, 420)
        y = random.randint(-220, 220)
        safe = True
        for h in hurdles:
            if abs(x - h.xcor()) < 80 and abs(y - h.ycor()) < 40:
                safe = False
                break
        if safe:
            special_food.goto(x, y)
            break
        if attempts > 300:
            special_food.goto(0, 0)
            break
    special_food.showturtle()
    special_food_active = True
    special_food_start_time = time.time()
    progress_bar.clear()

def hide_special_food():
    global special_food_active
    special_food.hideturtle()
    special_food_active = False
    progress_bar.clear()

def update_progress_bar():
    if not special_food_active:
        return
    elapsed = time.time() - special_food_start_time
    remaining = max(0, special_food_duration - elapsed)
    progress_bar.clear()

    # bottom position of the bar
    bottom_y = -280
    progress_bar.penup()
    progress_bar.goto(-200, bottom_y)
    progress_bar.pendown()

    # length proportional to remaining time 
    length = int((remaining / special_food_duration) * 400)

    # color transitions (green -> yellow -> red)
    ratio = remaining / special_food_duration
    if ratio > 0.66:
        progress_bar.color("green")
    elif ratio > 0.33:
        progress_bar.color("yellow")
    else:
        progress_bar.color("red")

    if length > 0:
        progress_bar.forward(length)

    if remaining <= 0:
        hide_special_food()


# Input handling
screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")
screen.onkeypress(go_up, "w")
screen.onkeypress(go_down, "s")
screen.onkeypress(go_left, "a")
screen.onkeypress(go_right, "d")
screen.onkeypress(toggle_pause, "space")

# Main game loop
def main_loop():
    global game_state, score, max_length, delay, food_counter, current_body_color, special_food_active, special_food_start_time
    
    while True:
        screen.update()
        
        if game_state == MENU:
            time.sleep(0.02)
            continue
            
        elif game_state == PAUSED:
            time.sleep(0.02)
            continue
            
        elif game_state == GAME_OVER:
            time.sleep(0.02)
            continue
            
        elif game_state == PLAYING:
            # Move the snake
            move()
            
            # Check for border collision
            if abs(head.xcor()) > 480 or abs(head.ycor()) > 280:
                game_over()
                continue
                
            # Move hurdles if in hard mode
            if difficulty == "hard":
                move_hurdles()
                
            # Check for hurdle collision
            for h in hurdles:
                if head.distance(h) < 30:
                    game_over()
                    break
            else:
                # Check for food collision
                if head.distance(food) < 20:
                    # Eating sound
                    if eating_sound:
                        try:
                            eating_sound.play()
                        except:
                            pass
                    
                    # Change head to open mouth
                    head.shape("open_mouth")
                    
                    # Get the color of the eaten food
                    eaten_color = food.color()[0]
                    
                    # Place new food
                    place_food_safe()
                    
                    # Update game state
                    score += 10
                    max_length += 10
                    food_counter += 1
                    food_bumps.append({"index": 0})
                    current_body_color = eaten_color
                    delay = max(0.005, delay * 0.88)
                    
                    # Update display and wait a bit
                    update_score_display()
                    screen.update()
                    time.sleep(0.08)
                    
                    # Change head back to circle
                    head.shape("circle")
                    
                    # Spawn special food every 4 normal foods
                    if food_counter % 4 == 0:
                        place_special_food()
                
                # Special food collision (if active)
                if special_food_active and head.distance(special_food) < 30:
                    if eating_sound:
                        try:
                            eating_sound.play()
                        except:
                            pass
                    head.shape("open_mouth")
                    # compute time-based bonus
                    elapsed = time.time() - special_food_start_time
                    remaining = max(0, special_food_duration - elapsed)
                    bonus = 50 + int(remaining * 10)  # base 50 + time-left*10
                    score += bonus
                    max_length += 20
                    food_bumps.append({"index": 0})
                    # give a slightly stronger speedup on special food
                    delay = max(0.005, delay * 0.85)
                    hide_special_food()
                    update_score_display()
                    screen.update()
                    time.sleep(0.08)
                    head.shape("circle")
                
                # Check for self collision (skip first few segments)
                for i, pos in enumerate(positions[15:], 15):
                    if head.distance(pos[0], pos[1]) < 12:
                        game_over()
                        break
            
            # If special food active: blink it and update progress bar (bottom)
            if special_food_active:
                # blink visibility
                if int(time.time() * 5) % 2 == 0:
                    special_food.showturtle()
                else:
                    special_food.hideturtle()
                update_progress_bar()
            
            # Update score display
            update_score_display()
            
            # Control game speed
            time.sleep(delay)

# Start the game
show_main_menu()
main_loop()
 