import pygame
import sys

class MainMenu:
    def __init__(self, win, width, height):
        self.win = win
        self.width = width
        self.height = height
        self.title_font = pygame.font.SysFont('Arial', 50, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 24)
        self.button_font = pygame.font.SysFont('Arial', 30)
        self.selected = None
        
        # Colors
        self.BACKGROUND = (30, 30, 30)  # Dark gray
        self.TEXT_COLOR = (255, 255, 255)  # White
        self.BUTTON_COLOR = (70, 130, 180)  # Steel blue
        self.BUTTON_HOVER = (100, 160, 210)  # Lighter blue for hover
        self.BUTTON_TEXT = (255, 255, 255)  # White
        
        # Button dimensions
        button_width = 200
        button_height = 60
        self.start_button = pygame.Rect(
            (width - button_width) // 2,
            height // 2 + 50,
            button_width,
            button_height
        )
        
        # Animation variables
        self.title_y = -50
        self.title_target_y = height // 4
        self.fade_alpha = 0  # For fade-in effect
        
    def update(self):
        # Animate title sliding down
        if self.title_y < self.title_target_y:
            self.title_y += 5
            
        # Animate fade in
        if self.fade_alpha < 255:
            self.fade_alpha += 5
            
    def draw(self):
        # Clear the screen
        self.win.fill(self.BACKGROUND)
        
        # Draw title with animation
        title_text = self.title_font.render("Data Structures", True, self.TEXT_COLOR)
        subtitle_text = self.title_font.render("Visualized", True, self.TEXT_COLOR)
        
        title_rect = title_text.get_rect(center=(self.width // 2, self.title_y))
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, self.title_y + 60))
        
        self.win.blit(title_text, title_rect)
        self.win.blit(subtitle_text, subtitle_rect)
        
        # Draw author info
        author_text = self.subtitle_font.render("Created by Nicholas Greiner", True, self.TEXT_COLOR)
        author_rect = author_text.get_rect(center=(self.width // 2, self.height - 30))
        self.win.blit(author_text, author_rect)
        
        # Draw start button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_color = self.BUTTON_HOVER if self.start_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        
        pygame.draw.rect(self.win, button_color, self.start_button, border_radius=15)
        pygame.draw.rect(self.win, (255, 255, 255), self.start_button, 2, border_radius=15)
        
        # Button text
        start_text = self.button_font.render("START", True, self.BUTTON_TEXT)
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        self.win.blit(start_text, start_text_rect)
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                return "selection"  # Transition to selection screen
        return None


class SelectionMenu:
    def __init__(self, win, width, height):
        self.win = win
        self.width = width
        self.height = height
        self.title_font = pygame.font.SysFont('Arial', 40, bold=True)
        self.button_font = pygame.font.SysFont('Arial', 24)
        self.info_font = pygame.font.SysFont('Arial', 18)
        
        # Colors
        self.BACKGROUND = (30, 30, 30)  # Dark gray
        self.TEXT_COLOR = (255, 255, 255)  # White
        self.BUTTON_COLOR = (70, 130, 180)  # Steel blue
        self.BUTTON_HOVER = (100, 160, 210)  # Lighter blue
        self.BUTTON_TEXT = (255, 255, 255)  # White
        
        # Available data structures with descriptions
        self.structures = [
            {
                "name": "Linked List",
                "description": "A linear collection of elements where each element points to the next",
                "button": pygame.Rect(100, 150, 250, 80)
            },
            {
                "name": "Stack",
                "description": "A LIFO (Last In, First Out) data structure",
                "button": pygame.Rect(450, 150, 250, 80)
            },
            {
                "name": "Queue",
                "description": "A FIFO (First In, First Out) data structure",
                "button": pygame.Rect(100, 300, 250, 80)
            },
            {
                "name": "Binary Tree",
                "description": "A tree data structure where each node has at most two children",
                "button": pygame.Rect(450, 300, 250, 80)
            },
        ]
        
        # Back button
        self.back_button = pygame.Rect(30, 30, 100, 40)
        
        # Structure info display
        self.selected_structure = None
        self.info_box = pygame.Rect(150, 450, 500, 100)
        
    def draw(self):
        # Clear the screen
        self.win.fill(self.BACKGROUND)
        
        # Draw title
        title_text = self.title_font.render("Select a Data Structure", True, self.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(self.width // 2, 70))
        self.win.blit(title_text, title_rect)
        
        # Draw structure buttons
        mouse_pos = pygame.mouse.get_pos()
        
        for structure in self.structures:
            button = structure["button"]
            is_hover = button.collidepoint(mouse_pos)
            button_color = self.BUTTON_HOVER if is_hover else self.BUTTON_COLOR
            
            # Draw button
            pygame.draw.rect(self.win, button_color, button, border_radius=10)
            pygame.draw.rect(self.win, (255, 255, 255), button, 2, border_radius=10)
            
            # Draw button text
            text = self.button_font.render(structure["name"], True, self.BUTTON_TEXT)
            text_rect = text.get_rect(center=button.center)
            self.win.blit(text, text_rect)
            
            # Update selected structure for info display
            if is_hover:
                self.selected_structure = structure
        
        # Draw back button
        back_color = self.BUTTON_HOVER if self.back_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        pygame.draw.rect(self.win, back_color, self.back_button, border_radius=5)
        pygame.draw.rect(self.win, (255, 255, 255), self.back_button, 2, border_radius=5)
        
        back_text = self.button_font.render("Back", True, self.BUTTON_TEXT)
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.win.blit(back_text, back_text_rect)
        
        # Draw info box
        pygame.draw.rect(self.win, (50, 50, 50), self.info_box, border_radius=5)
        pygame.draw.rect(self.win, (150, 150, 150), self.info_box, 2, border_radius=5)
        
        if self.selected_structure:
            info_text = self.info_font.render(self.selected_structure["description"], True, self.TEXT_COLOR)
            info_rect = info_text.get_rect(center=self.info_box.center)
            self.win.blit(info_text, info_rect)
        else:
            info_text = self.info_font.render("Hover over a data structure for information", True, self.TEXT_COLOR)
            info_rect = info_text.get_rect(center=self.info_box.center)
            self.win.blit(info_text, info_rect)
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check for data structure selection
            for structure in self.structures:
                if structure["button"].collidepoint(event.pos):
                    return structure["name"]  # Return the selected structure
            
            # Check for back button
            if self.back_button.collidepoint(event.pos):
                return "main_menu"  # Go back to main menu
        
        return None