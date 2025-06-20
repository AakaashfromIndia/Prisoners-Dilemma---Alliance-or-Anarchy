import pygame
import random
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg

pygame.init()

# Constants
WIDTH, HEIGHT = 1204, 674
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
LIGHT_BLUE = (100, 100, 255)
FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 48)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Iterated Prisoner's Dilemma")
bg_image = pygame.image.load("MainBG.png")
game_bg_image = pygame.image.load("GameBG.png")
end_bg_image = pygame.image.load("EndBG2.png")
strategy_bg_image = pygame.image.load("SelectBG.png")

stats = {
    'user_cooperate_count': 0,
    'user_defect_count': 0,
    'opponent_cooperate_count': 0,
    'opponent_defect_count': 0,
    'mutual_cooperation': 0,
    'mutual_defection': 0,
    'user_exploit': 0,
    'opponent_exploit': 0,
    'round_scores': [],
    'cumulative_scores': [],
}

def main_menu():
    menu_running = True
    while menu_running:
        screen.blit(bg_image, (0, 0))

        start_button = pygame.draw.rect(screen, GREEN, (930, 170, 220, 80))
        about_button = pygame.draw.rect(screen, YELLOW, (930, 270, 220, 80))
        how_to_play_button = pygame.draw.rect(screen, YELLOW, (930, 370, 220, 80))
        quit_button = pygame.draw.rect(screen, RED, (930, 470, 220, 80))

        arial_font = pygame.font.SysFont("arial", 36)
        kitchenpolicefont = 'KITCHENPOLICE.ttf'
        kp_font = pygame.font.Font(kitchenpolicefont, 28)

        start_text = kp_font.render("Start", True, WHITE)
        about_text = kp_font.render("About", True, BLACK)
        how_to_play_text = kp_font.render("How to Play", True, BLACK)
        quit_text = kp_font.render("Quit", True, WHITE)

        screen.blit(start_text, (990, 195))
        screen.blit(about_text, (990, 295))
        screen.blit(how_to_play_text, (940, 395))
        screen.blit(quit_text, (1000, 495))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_button.collidepoint(x, y):
                    return
                elif about_button.collidepoint(x, y):
                    print("About button clicked")
                elif how_to_play_button.collidepoint(x, y):
                    print("How to Play button clicked")
                elif quit_button.collidepoint(x, y):
                    pygame.quit()
                    exit()

def select_strategy_spin_machine():
    strategies = list(strategy_map.keys())
    current_index = 0
    clock = pygame.time.Clock()
    while True:
        screen.blit(strategy_bg_image, (0, 0))

        prisonwallsfont = 'PrisonWalls.ttf'
        pw_font = pygame.font.Font(prisonwallsfont, 34)

        title_text = pw_font.render("Select Opponent Strategy", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        
        total_strategies = len(strategies)
        center_y = HEIGHT // 2
        positions = [
            (current_index - 2) % total_strategies,
            (current_index - 1) % total_strategies,
            current_index,
            (current_index + 1) % total_strategies,
            (current_index + 2) % total_strategies
        ]
        
        strategy_rects = []
        for i, pos in enumerate(positions):
            strategy = strategies[pos]
            
            if i == 2:
                scale = 1.5
                alpha = 255
            elif i == 1 or i == 3:
                scale = 1.0
                alpha = 220
            else:
                scale = 0.6
                alpha = 150
            
            y_offsets = [-160, -90, 0, 90, 160]
            y = center_y + y_offsets[i]

            youmurdererfont = "youmurdererbb_reg.ttf"
            
            scaled_font = pygame.font.Font(youmurdererfont, int(42 * scale))
            strategy_text = scaled_font.render(strategy, True, WHITE)
            strategy_text.set_alpha(alpha)
            text_rect = strategy_text.get_rect(center=(WIDTH // 2, y))
            screen.blit(strategy_text, text_rect)
            strategy_rects.append(text_rect)
        
        current_text_rect = strategy_rects[2]
        pointer_width = 50
        pointer_x = current_text_rect.left - pointer_width - 10
        pointer_y_center = current_text_rect.centery
        
        pointer_points = [
            (pointer_x, pointer_y_center - 40),
            (pointer_x + pointer_width, pointer_y_center),
            (pointer_x, pointer_y_center + 40)
        ]
        
        pygame.draw.polygon(screen, GREEN, pointer_points)
        
        pygame.display.flip()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                if y < HEIGHT // 2:
                    current_index = (current_index - 1) % total_strategies
                elif y > HEIGHT // 2:
                    current_index = (current_index + 1) % total_strategies
                if HEIGHT // 2 - 100 < y < HEIGHT // 2 + 100:
                    return strategies[current_index]
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return strategies[current_index]
                elif event.key == pygame.K_UP:
                    current_index = (current_index - 1) % total_strategies
                elif event.key == pygame.K_DOWN:
                    current_index = (current_index + 1) % total_strategies

main_menu()

# Define strategies
def tit_for_tat():
    return user_last_move

def tit_for_two_tats():
    if len(history) >= 2 and history[-1][0] == "D" and history[-2][0] == "D":
        return "D"
    return "C"

def always_cooperate():
    return "C"

def always_defect():
    return "D"

def grim_trigger():
    if any(user_move == "D" for user_move, _, _ in history):
        return "D"
    return "C"

def tit_for_tat():
    return user_last_move

def tit_for_two_tats():
    if len(history) >= 2 and history[-1][0] == "D" and history[-2][0] == "D":
        return "D"
    return "C"

def always_cooperate():
    return "C"

def always_defect():
    return "D"

def grim_trigger():
    if any(user_move == "D" for user_move, _, _ in history):
        return "D"
    return "C"

def random_strategy():
    return random.choice(["C", "D"])

def pavlov():
    # Win-Stay, Lose-Shift
    if not history:
        return "C"
    last_move, last_opponent_move, _ = history[-1]
    if last_move == "C" and last_opponent_move == "C":
        return "C"
    elif last_move == "D" and last_opponent_move == "C":
        return "D"
    elif last_move == "D" and last_opponent_move == "D":
        return "C"
    else:
        return "D"

def soft_grim_trigger():
    if not history:
        return "C"
    
    defection_count = sum(1 for user_move, _, _ in history if user_move == "D")
    if defection_count > 0:
        try:
            rounds_since_defection = len(history) - next(
                i for i in range(len(history)-1, -1, -1) 
                if history[i][0] == "C"
            )
            return "D" if rounds_since_defection <= 2 else "C"
        except StopIteration:
            return "D"
    return "C"

def suspicious_tit_for_tat():
    if not history:
        return "D"
    return user_last_move

def generous_tit_for_tat():
    if not history:
        return "C"
    if history[-1][0] == "D":
        return "C" if random.random() < 0.1 else "D"
    return "C"

def win_stay_lose_shift():
    if not history:
        return "C"
    last_move, last_opponent_move, _ = history[-1]
    if last_opponent_move == "C":
        return last_move
    return "D" if last_move == "C" else "C"

def tit_for_two_tats_extended():
    if len(history) >= 2 and history[-1][0] == "D" and history[-2][0] == "D":
        return "D"
    return "C"

def forgiving_tit_for_tat():
    if not history:
        return "C"
    if history[-1][0] == "D":
        return "C"
    return user_last_move

def echo():
    if not history:
        return "C"
    return history[-1][1]

def pavlov_with_twist():
    if not history:
        return "C"
    cycle = ["C", "D", "C", "C", "D", "D"]
    return cycle[len(history) % len(cycle)]

def shadow():
    if not history:
        return "C"
    if any(opponent_move == "D" for _, opponent_move, _ in history):
        return "D"
    return "C"

def alternate():
    return "C" if len(history) % 2 == 0 else "D"

def tit_for_three_tats():
    defection_count = sum(1 for _, opponent_move, _ in history if opponent_move == "D")
    return "D" if defection_count >= 3 else "C"

def contrite_tit_for_tat():
    if not history:
        return "C"
    return "C" if history[-1][0] == "D" else user_last_move

def copycat():
    if not history:
        return "C"
    return history[-1][1]

def tit_for_tat_with_forgiveness():
    if not history:
        return "C"
    return "C" if history[-1][0] == "D" else user_last_move

def tit_for_tat_with_retribution():
    if not history:
        return "C"
    if history[-1][0] == "D":
        return "D"
    return user_last_move

def prober():
    if len(history) < 3:
        probing_sequence = ["D", "C", "C"]
        return probing_sequence[len(history)]
    return user_last_move

def tit_for_two_tactics():
    if len(history) >= 2 and history[-1][0] == "D" and history[-2][0] == "D":
        return "D"
    return "C"

def choose_random_strategy():
    return strategy_map[random.choice(list(strategy_map.keys()))]()

strategy_map = {
    "Tit for Tat": tit_for_tat,
    "Tit for Two Tats": tit_for_two_tats,
    "Always Cooperate": always_cooperate,
    "Always Defect": always_defect,
    "Grim Trigger": grim_trigger,
    "Random": random_strategy,
    "Pavlov": pavlov,
    "Soft Grim Trigger": soft_grim_trigger,
    "Suspicious Tit for Tat": suspicious_tit_for_tat,
    "Generous Tit for Tat": generous_tit_for_tat,
    "Win-Stay, Lose-Shift": win_stay_lose_shift,
    "Tit for Two Tats Extended": tit_for_two_tats_extended,
    "Forgiving Tit for Tat": forgiving_tit_for_tat,
    "Echo": echo,
    "Pavlov with a Twist": pavlov_with_twist,
    "Shadow": shadow,
    "Alternate": alternate,
    "Tit for Three Tats": tit_for_three_tats,
    "Contrite Tit for Tat": contrite_tit_for_tat,
    "Copycat": copycat,
    "Tit for Tat with Forgiveness": tit_for_tat_with_forgiveness,
    "Tit for Tat with Retribution": tit_for_tat_with_retribution,
    "Prober": prober,
    "Tit for Two Tactics": tit_for_two_tactics,
    "Choose Random Strategy": choose_random_strategy
}

# Game variables
user_score = 0
opponent_score = 0
rounds_total = random.randint(5, 10)
rounds_left = rounds_total
user_last_move = "C"
opponent_last_move = "C"
history = []
move_counter = 0
selected_strategy = select_strategy_spin_machine()

# Animation variables
animation_speed = 10
animating = False
circle_data = []
animation_stage = 0
selected_circle = None

# Score animation variables
score_animations = []
score_anim_speed = 2
score_anim_lifespan = 60

# Winner highlight variables
user_is_winner = False
opponent_is_winner = False
highlight_thickness = 4

def update_stats(user_move, opponent_move, user_points, opponent_points):
    # Count move types
    if user_move == "C":
        stats['user_cooperate_count'] += 1
    else:
        stats['user_defect_count'] += 1
        
    if opponent_move == "C":
        stats['opponent_cooperate_count'] += 1
    else:
        stats['opponent_defect_count'] += 1
    
    # Count outcome types
    if user_move == "C" and opponent_move == "C":
        stats['mutual_cooperation'] += 1
    elif user_move == "D" and opponent_move == "D":
        stats['mutual_defection'] += 1
    elif user_move == "D" and opponent_move == "C":
        stats['user_exploit'] += 1
    elif user_move == "C" and opponent_move == "D":
        stats['opponent_exploit'] += 1
    
    # Track scores
    stats['round_scores'].append((user_points, opponent_points))
    
    # Update cumulative scores
    if not stats['cumulative_scores']:
        stats['cumulative_scores'].append((user_points, opponent_points))
    else:
        prev_user, prev_opp = stats['cumulative_scores'][-1]
        stats['cumulative_scores'].append((prev_user + user_points, prev_opp + opponent_points))


def create_decision_pie_chart():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 2.4))
    
    # User pie chart
    user_labels = ['Cooperate', 'Defect']
    user_sizes = [stats['user_cooperate_count'], stats['user_defect_count']]
    user_colors = ['#00c800', '#c80000']
    ax1.pie(user_sizes, labels=user_labels, colors=user_colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Your Decisions')
    
    # Opponent pie chart
    opp_labels = ['Cooperate', 'Defect']
    opp_sizes = [stats['opponent_cooperate_count'], stats['opponent_defect_count']]
    opp_colors = ['#00c800', '#c80000']
    ax2.pie(opp_sizes, labels=opp_labels, colors=opp_colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Opponent Decisions')
    
    plt.tight_layout()
    buf = io.BytesIO()
    FigureCanvasAgg(fig).print_png(buf)
    plt.close(fig)
    
    buf.seek(0)
    img_str = buf.read()
    buf.close()
    
    return pygame.image.load(io.BytesIO(img_str))

def create_outcome_bar_chart():
    fig, ax = plt.subplots(figsize=(8, 2.4))
    outcome_types = ['Mutual\nCooperation', 'Mutual\nDefection', 'You Exploited\nOpponent', 'Opponent\nExploited You']
    outcome_counts = [stats['mutual_cooperation'], stats['mutual_defection'], 
                     stats['user_exploit'], stats['opponent_exploit']]
    
    colors = ['#00c800', '#c80000', '#0000c8', '#c8c800']
    ax.bar(outcome_types, outcome_counts, color=colors)
    
    for i, v in enumerate(outcome_counts):
        ax.text(i, v + 0.1, str(v), ha='center')
    
    # Add labels and title
    ax.set_ylabel('Count')
    ax.set_title('Game Outcomes')
    
    # Adjust layout and save to BytesIO
    plt.tight_layout()
    buf = io.BytesIO()
    FigureCanvasAgg(fig).print_png(buf)
    plt.close(fig)
    
    # Create a Pygame surface from the PNG data
    buf.seek(0)
    img_str = buf.read()
    buf.close()
    
    return pygame.image.load(io.BytesIO(img_str))

def create_score_line_chart():
    # Create a figure for the line chart
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Extract cumulative scores
    rounds = range(1, len(stats['cumulative_scores']) + 1)
    user_scores = [score[0] for score in stats['cumulative_scores']]
    opp_scores = [score[1] for score in stats['cumulative_scores']]
    
    # Plot lines
    ax.plot(rounds, user_scores, 'g-', label='Your Score', linewidth=2)
    ax.plot(rounds, opp_scores, 'r-', label='Opponent Score', linewidth=2)
    
    # Add labels and title
    ax.set_xlabel('Round')
    ax.set_ylabel('Cumulative Score')
    ax.set_title('Score Progression')
    ax.legend()
    
    # Add grid for better readability
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout and save to BytesIO
    plt.tight_layout()
    buf = io.BytesIO()
    FigureCanvasAgg(fig).print_png(buf)
    plt.close(fig)
    
    # Create a Pygame surface from the PNG data
    buf.seek(0)
    img_str = buf.read()
    buf.close()
    
    return pygame.image.load(io.BytesIO(img_str))

# Function to display the stats screen
def show_stats_screen():
    # Create background for stats screen
    stats_bg_image = pygame.image.load("StatsBG.png").convert()
    stats_bg_image = pygame.transform.scale(stats_bg_image, (WIDTH, HEIGHT))
    
    # Font setup
    title_font = pygame.font.Font(pixelpurlfont, 48)
    header_font = pygame.font.Font(pixelpurlfont, 36)
    text_font = pygame.font.Font(pixelpurlfont, 24)
    
    # Analytics screen variables
    page = 0
    total_pages = 3
    stats_running = True
    
    while stats_running:
        # Clear screen with background
        screen.blit(stats_bg_image, (0, 0))
        
        # Title
        title_text = title_font.render("Game Analytics", True, WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 20))
        
        # Page indicator
        page_text = text_font.render(f"Page {page+1}/{total_pages}", True, WHITE)
        screen.blit(page_text, (WIDTH - page_text.get_width() - 20, HEIGHT - page_text.get_height() - 20))
        
        # Navigation instructions
        nav_text = text_font.render("Arrow Keys: Navigate | ESC: Exit", True, WHITE)
        screen.blit(nav_text, (20, HEIGHT - nav_text.get_height() - 20))
        
        # Display different content based on current page
        if page == 0:
            # Summary statistics page
            header_text = header_font.render("Game Summary", True, YELLOW)
            screen.blit(header_text, (WIDTH//2 - header_text.get_width()//2, 90))
            
            # Game info
            info_texts = [
                f"Strategy: {selected_strategy}",
                f"Total Rounds: {rounds_total}",
                f"Final Score - You: {user_score} | Opponent: {opponent_score}",
                f"Your Cooperation Rate: {stats['user_cooperate_count']/rounds_total*100:.1f}%",
                f"Opponent Cooperation Rate: {stats['opponent_cooperate_count']/rounds_total*100:.1f}%",
                f"Mutual Cooperation: {stats['mutual_cooperation']/rounds_total*100:.1f}% of rounds",
                f"Mutual Defection: {stats['mutual_defection']/rounds_total*100:.1f}% of rounds",
                f"You Exploited Opponent: {stats['user_exploit']} times",
                f"Opponent Exploited You: {stats['opponent_exploit']} times",
            ]
            
            for i, text in enumerate(info_texts):
                rendered_text = text_font.render(text, True, WHITE)
                screen.blit(rendered_text, (WIDTH//2 - rendered_text.get_width()//2, 150 + i*40))
                
        elif page == 1:
            # Decision analysis page
            header_text = header_font.render("Decision Analysis", True, YELLOW)
            screen.blit(header_text, (WIDTH//2 - header_text.get_width()//2, 90))
            
            # Display pie charts for decisions
            pie_chart = create_decision_pie_chart()
            screen.blit(pie_chart, (WIDTH//2 - pie_chart.get_width()//2, 140))
            
            # Display bar chart for outcomes
            outcome_chart = create_outcome_bar_chart()
            screen.blit(outcome_chart, (WIDTH//2 - outcome_chart.get_width()//2, 350))
            
        elif page == 2:
            # Score progression page
            header_text = header_font.render("Score Progression", True, YELLOW)
            screen.blit(header_text, (WIDTH//2 - header_text.get_width()//2, 90))
            
            # Display line chart for score progression
            score_chart = create_score_line_chart()
            screen.blit(score_chart, (WIDTH//2 - score_chart.get_width()//2, 140))
            
            # Calculate and display some additional statistics
            user_points = [score[0] for score in stats['round_scores']]
            opp_points = [score[1] for score in stats['round_scores']]
            
            avg_user_points = sum(user_points) / len(user_points)
            avg_opp_points = sum(opp_points) / len(opp_points)
            
            stats_texts = [
                f"Your Average Points Per Round: {avg_user_points:.2f}",
                f"Opponent Average Points Per Round: {avg_opp_points:.2f}",
                f"Your Best Round: {max(user_points)} points",
                f"Your Worst Round: {min(user_points)} points",
                f"Rounds Where You Outscored Opponent: {sum(1 for u, o in stats['round_scores'] if u > o)}"
            ]
            
            for i, text in enumerate(stats_texts):
                rendered_text = text_font.render(text, True, WHITE)
                screen.blit(rendered_text, (WIDTH//2 - rendered_text.get_width()//2, 400 + i*40))
        
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stats_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stats_running = False
                elif event.key == pygame.K_RIGHT:
                    page = (page + 1) % total_pages
                elif event.key == pygame.K_LEFT:
                    page = (page - 1) % total_pages


def update_circle_positions():
    global animating, animation_stage
    
    animating = False
    all_at_target = True
    
    for i in range(len(circle_data)):
        current_x, current_y = circle_data[i]['current_pos']
        target_x, target_y = circle_data[i]['target_pos']
        
        if current_x != target_x or current_y != target_y:
            animating = True
            all_at_target = False
            
            dx = target_x - current_x
            dy = target_y - current_y
            distance = (dx**2 + dy**2)**0.5
            
            if distance <= animation_speed:
                circle_data[i]['current_pos'] = (target_x, target_y)
            else:
                move_ratio = animation_speed / distance
                circle_data[i]['current_pos'] = (current_x + dx * move_ratio, current_y + dy * move_ratio)
    
    if all_at_target:
        if animation_stage == 1:
            animation_stage = 2
            for i, circle in enumerate(circle_data):
                current_x, current_y = circle['current_pos']
                
                if circle['type'] == 'user' and circle['is_new']:
                    circle['target_pos'] = (WIDTH // 2 - 100, current_y)
                elif circle['type'] == 'opponent' and circle['is_new']:
                    circle['target_pos'] = (WIDTH // 2 + 100, current_y)
        
        elif animation_stage == 2:
            animation_stage = 3
            
            user_circles = [c for c in circle_data if c['type'] == 'user']
            opponent_circles = [c for c in circle_data if c['type'] == 'opponent']
            
            for circle in circle_data:
                if circle['is_new']:
                    circle['is_new'] = False
            
            user_circles_sorted = sorted(user_circles, key=lambda c: c['number'])
            opponent_circles_sorted = sorted(opponent_circles, key=lambda c: c['number'])
            
            center_x = WIDTH // 2
            spacing = 80
            
            for i, circle in enumerate(user_circles_sorted):
                _, current_y = circle['current_pos']
                
                reverse_index = len(user_circles_sorted) - 1 - i
                pos_x = center_x - 100 - (reverse_index * spacing)
                circle['target_pos'] = (pos_x, 640)
                
            for i, circle in enumerate(opponent_circles_sorted):
                _, current_y = circle['current_pos']
                
                reverse_index = len(opponent_circles_sorted) - 1 - i
                pos_x = center_x + 100 + (reverse_index * spacing)
                circle['target_pos'] = (pos_x, 640)
        
        elif animation_stage == 3:
            animation_stage = 0

def update_score_animations():
    global score_animations
    for i in range(len(score_animations) - 1, -1, -1):
        anim = score_animations[i]
        anim['y'] -= score_anim_speed
        anim['life'] -= 1
        
        if anim['life'] <= 0:
            score_animations.pop(i)

def draw_progress_bar():
    if user_score + opponent_score > 0:
        total_score = user_score + opponent_score
        user_proportion = user_score / total_score
        bar_width = 400
        bar_height = 30
        bar_x = (WIDTH - bar_width) // 2
        bar_y = 20
        
        pygame.draw.rect(screen, WHITE, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, (99, 133, 158), (bar_x, bar_y, bar_width, bar_height))
        
        user_width = int(bar_width * user_proportion)
        pygame.draw.rect(screen, (142, 191, 185), (bar_x, bar_y, user_width, bar_height))

def check_circle_click(x, y):
    global selected_circle
    
    selected_circle = None
    
    for i, circle in enumerate(circle_data):
        circle_x, circle_y = circle['current_pos']
        distance = ((x - circle_x) ** 2 + (y - circle_y) ** 2) ** 0.5
        
        if distance <= 20:
            selected_circle = i
            circle_data[i]['selected'] = True
            print(f"Circle clicked: {circle['type']} move #{circle['number']}, {'Cooperate' if circle['color'] == GREEN else 'Defect'}")
            return True
    return False

running = True
max_displayed_circles = 6
clock = pygame.time.Clock()

while running and rounds_left > 0:
    screen.blit(game_bg_image, (0, 0))

    pixelpurlfont = 'PixelPurl.ttf'
    pp_font = pygame.font.Font(pixelpurlfont, 40)
    
    # Display scores in white at top left and right
    user_score_text = pp_font.render(f"Your Score: {user_score}", True, WHITE)
    opponent_score_text = pp_font.render(f"Opponent: {opponent_score}", True, WHITE)
    screen.blit(user_score_text, (20, 20))
    screen.blit(opponent_score_text, (WIDTH - opponent_score_text.get_width() - 20, 20))
    
    # Draw the progress bar between the scores
    draw_progress_bar()
    
    update_circle_positions()    
    update_score_animations()
    button_color_coop = (45, 92, 108)
    button_color_defect = (23, 44, 72)

    coop_surface = pygame.Surface((156, 35), pygame.SRCALPHA)
    defect_surface = pygame.Surface((156, 35), pygame.SRCALPHA)

    coop_surface.fill(button_color_coop + (1,))
    defect_surface.fill(button_color_defect + (1,))

    # Blit surfaces to screen
    screen.blit(coop_surface, (342, 547))
    coop_button = pygame.Rect(342, 547, 185, 33)

    screen.blit(defect_surface, (650, 523))
    defect_button = pygame.Rect(668, 545, 190, 36)

    kitchenpolicefont = 'KITCHENPOLICE.ttf'
    kp_font = pygame.font.Font(kitchenpolicefont, 20)
    prisonwallsfont = 'PrisonWalls.ttf'
    pw_font = pygame.font.Font(prisonwallsfont, 20)
        
    coop_text = pw_font.render("Cooperate", True, WHITE)
    defect_text = pw_font.render("Defect", True, WHITE)
    screen.blit(coop_text, (356, 552))
    screen.blit(defect_text, (710, 552))

    # Draw larger circles for user's and opponent's current moves
    user_circle_color = GREEN if user_last_move == "C" else RED
    opponent_circle_color = GREEN if opponent_last_move == "C" else RED
    
    pygame.draw.circle(screen, user_circle_color, (500, 340), 50)  # User's Circle
    pygame.draw.circle(screen, opponent_circle_color, (700, 340), 50)  # Opponent's Circle
    
    if user_is_winner and opponent_is_winner:  # Both get the same score (tie)
        pygame.draw.circle(screen, YELLOW, (500, 340), 50 + highlight_thickness, highlight_thickness)
        pygame.draw.circle(screen, YELLOW, (700, 340), 50 + highlight_thickness, highlight_thickness)
    elif user_is_winner:
        pygame.draw.circle(screen, YELLOW, (500, 340), 50 + highlight_thickness, highlight_thickness)
    elif opponent_is_winner:
        pygame.draw.circle(screen, YELLOW, (700, 340), 50 + highlight_thickness, highlight_thickness)
    
    for i, circle in enumerate(circle_data):
        pos_x, pos_y = circle['current_pos']
        color = circle['color']
        number = circle['number']
        
        pygame.draw.circle(screen, color, (int(pos_x), int(pos_y)), 20)
        
        if selected_circle == i:
            pygame.draw.circle(screen, WHITE, (int(pos_x), int(pos_y)), 24, 2)
            info_text = f"Move #{number}: {'Cooperate' if color == GREEN else 'Defect'}"
            text_surface = FONT.render(info_text, True, WHITE)
            
            text_x = int(pos_x) - text_surface.get_width() // 2
            text_y = int(pos_y) - 40
            
            text_bg = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 6))
            text_bg.set_alpha(180)
            text_bg.fill((0, 0, 0))
            screen.blit(text_bg, (text_x - 5, text_y - 3))
            screen.blit(text_surface, (text_x, text_y))

    pixelpurlfont = 'PixelPurl.ttf'
    pp_font = pygame.font.Font(pixelpurlfont, 40)
    
    for anim in score_animations:
        alpha = min(255, int(255 * (anim['life'] / score_anim_lifespan)))
        
        anim_text = pp_font.render(anim['text'], True, anim['color'])
        text_surface = pygame.Surface(anim_text.get_size(), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 0))
        
        anim_text.set_alpha(alpha)
        text_surface.blit(anim_text, (0, 0))
        
        screen.blit(text_surface, (anim['x'] - anim_text.get_width() // 2, anim['y']))

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            if check_circle_click(x, y):
                continue
            
            if not animating:
                if coop_button.collidepoint(x, y):
                    user_move = "C"
                elif defect_button.collidepoint(x, y):
                    user_move = "D"
                else:
                    continue
                    
                move_counter += 1
                opponent_move = strategy_map[selected_strategy]()
                
                user_is_winner = False
                opponent_is_winner = False
                
                user_points = 0
                opponent_points = 0
                
                if user_move == "C" and opponent_move == "C":
                    user_points = 3
                    opponent_points = 3
                    score_text_user = "+3"
                    score_text_opponent = "+3"
                    user_is_winner = True
                    opponent_is_winner = True
                elif user_move == "D" and opponent_move == "C":
                    user_points = 5
                    opponent_points = 0
                    user_is_winner = True
                    score_text_user = "+5"
                    score_text_opponent = "+0"
                elif user_move == "C" and opponent_move == "D":
                    user_points = 0
                    opponent_points = 5
                    opponent_is_winner = True
                    score_text_user = "+0"
                    score_text_opponent = "+5"
                else:  # Both defect
                    user_points = 1
                    opponent_points = 1
                    user_is_winner = True
                    opponent_is_winner = True
                    score_text_user = "+1"
                    score_text_opponent = "+1"
                
                user_score += user_points
                opponent_score += opponent_points
                update_stats(user_move, opponent_move, user_points, opponent_points)
                
                if user_points > 0:
                    score_animations.append({
                        'x': 525,
                        'y': 310,
                        'text': score_text_user,
                        'color': WHITE,
                        'life': score_anim_lifespan
                    })
                    
                if opponent_points > 0:
                    score_animations.append({
                        'x': 750,
                        'y': 310,
                        'text': score_text_opponent,
                        'color': WHITE,
                        'life': score_anim_lifespan
                    })
                
                history.append((user_move, opponent_move, move_counter))
                user_last_move = user_move
                opponent_last_move = opponent_move
                rounds_left -= 1
                
                user_color = GREEN if user_move == "C" else RED
                opponent_color = GREEN if opponent_move == "C" else RED
                
                if len(circle_data) >= max_displayed_circles * 2:
                    user_circles = [i for i, c in enumerate(circle_data) if c['type'] == 'user']
                    opponent_circles = [i for i, c in enumerate(circle_data) if c['type'] == 'opponent']
                    
                    if user_circles and opponent_circles:
                        oldest_user = min(user_circles, key=lambda i: circle_data[i]['number'])
                        oldest_opponent = min(opponent_circles, key=lambda i: circle_data[i]['number'])
                        
                        if oldest_user > oldest_opponent:
                            circle_data.pop(oldest_user)
                            circle_data.pop(oldest_opponent)
                        else:
                            circle_data.pop(oldest_opponent)
                            circle_data.pop(oldest_user)
                
                new_user_circle = {
                    'current_pos': (500, 340),
                    'target_pos': (500, 640),
                    'color': user_color,
                    'number': move_counter,
                    'type': 'user',
                    'is_new': True,
                    'selected': False
                }
                
                new_opponent_circle = {
                    'current_pos': (700, 340),
                    'target_pos': (700, 640),
                    'color': opponent_color,
                    'number': move_counter,
                    'type': 'opponent',
                    'is_new': True,
                    'selected': False
                }
                
                circle_data.append(new_user_circle)
                circle_data.append(new_opponent_circle)
                
                animation_stage = 1
                animating = True

odfont = 'RoyalBrand-Regular.otf'
od_font = pygame.font.Font(odfont, 40)
pixelpurlfont = 'PixelPurl.ttf'
pp_font = pygame.font.Font(pixelpurlfont, 40)

# Draw end screen
screen.blit(end_bg_image, (0, 0))
final_text = pp_font.render(f"Final Scores : {user_score}-{opponent_score}", True, BLACK)
text_width = final_text.get_width()
text_height = final_text.get_height()

x = 599 - text_width // 2
screen.blit(final_text, (x, 169))

FONT = pygame.font.Font(None, 48)

if user_score > opponent_score:
    winner_text = od_font.render("You Won!", True, GREEN)
elif opponent_score > user_score:
    winner_text = od_font.render("Opponent Won!", True, RED)
else:
    winner_text = od_font.render("It's a Tie!", True, YELLOW)

text_width = winner_text.get_width()
text_height = winner_text.get_height()

x = 599 - text_width // 2
y = 247 - text_height // 2

screen.blit(winner_text, (x, y))

stats_button = pygame.draw.rect(screen, GREEN, (WIDTH//2 - 150, HEIGHT - 150, 300, 70))
stats_button_text = pp_font.render("View Statistics", True, WHITE)
screen.blit(stats_button_text, (WIDTH//2 - stats_button_text.get_width()//2, HEIGHT - 135))

pygame.display.flip()

end_screen_active = True
while end_screen_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_screen_active = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if stats_button.collidepoint(x, y):
                show_stats_screen() 
            else:
                end_screen_active = False
        elif event.type == pygame.KEYDOWN:
            end_screen_active = False

pygame.quit()
