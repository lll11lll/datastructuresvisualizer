import pygame
import sys
import time
import math
import tkinter as tk
from tkinter import simpledialog, messagebox
from DataStructures.LinkedList import LinkedList, Node

class LinkedListVisualizer:
    def __init__(self, win, width, height):
        self.win = win
        self.width = width
        self.height = height
        self.linked_list = None
        
        # Colors
        self.NODE_COLOR = (70, 130, 180)  # Steel blue
        self.NODE_HIGHLIGHT = (255, 165, 0)  # Orange
        self.HEAD_COLOR = (124, 252, 0)  # Lawn green
        self.TAIL_COLOR = (220, 20, 60)  # Crimson
        self.ARROW_COLOR = (200, 200, 200)  # Light gray
        self.TEXT_COLOR = (255, 255, 255)  # White
        self.BACKGROUND = (30, 30, 30)  # Dark gray
        
        # Node dimensions
        self.NODE_RADIUS = 30
        self.NODE_SPACING = 100  # Space between nodes
        self.STARTING_X = 100
        self.STARTING_Y = height // 2
        
        # Font
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 20)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        # Animation speed (lower is faster)
        
        self.ANIMATION_SPEED = 0.5
        
        # Button properties
        self.buttons = []
        self.setup_buttons()

        # educational mode
        self.educational_mode = True  # Toggle educational mode
        self.setup_educational_button()


    def setup_buttons(self):
        """Setup UI buttons for operations"""
        button_width, button_height = 100, 40
        spacing = 10
        y_position = self.height - 60
        
        operations = [
            ("Append", self.append_operation),
            ("Prepend", self.prepend_operation),
            ("Insert", self.insert_operation),
            ("Remove", self.remove_operation),
            ("Pop", self.pop_operation),
            ("Pop First", self.pop_first_operation)
        ]
        
        for i, (label, callback) in enumerate(operations):
            x_pos = spacing + i * (button_width + spacing)
            self.buttons.append({
                'rect': pygame.Rect(x_pos, y_position, button_width, button_height),
                'label': label,
                'callback': callback
            })

    def setup_educational_button(self):
        """Setup the educational mode toggle button"""
        self.edu_button = {
            'rect': pygame.Rect(self.width - 120, 10, 110, 30),
            'label': 'Educational: ON' if self.educational_mode else 'Educational: OFF'
        }

    def show_educational_popup(self, title, message):
        """Show an educational popup explaining the operation"""
        if not self.educational_mode:
            return
            
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        
        # Create a custom dialog with better formatting
        messagebox.showinfo(title, message, parent=root)
        root.destroy()


    def set_linked_list(self, linked_list):
        """Set the linked list to visualize"""
        self.linked_list = linked_list
    
    def create_new_list(self, value):
        """Create a new linked list with initial value"""
        self.linked_list = LinkedList(value)
        
    def draw_node(self, x, y, value, is_head=False, is_tail=False, highlight=False):
        """Draw a node at position (x, y) with the given value"""
        # Draw the circle
        color = self.NODE_HIGHLIGHT if highlight else self.NODE_COLOR
        pygame.draw.circle(self.win, color, (x, y), self.NODE_RADIUS)
        pygame.draw.circle(self.win, (255, 255, 255), (x, y), self.NODE_RADIUS, 2)
        
        # Draw the value
        text = self.font.render(str(value), True, self.TEXT_COLOR)
        text_rect = text.get_rect(center=(x, y))
        self.win.blit(text, text_rect)
        
        # Indicate if it's head or tail
        if is_head:
            head_text = self.small_font.render("Head", True, self.HEAD_COLOR)
            self.win.blit(head_text, (x - 20, y - self.NODE_RADIUS - 20))
        
        if is_tail:
            tail_text = self.small_font.render("Tail", True, self.TAIL_COLOR)
            self.win.blit(tail_text, (x - 15, y + self.NODE_RADIUS + 5))

    def draw_arrow(self, start_x, start_y, end_x, end_y):
        """Draw an arrow from (start_x, start_y) to (end_x, end_y)"""
        # Calculate the angle of the arrow
        dx = end_x - start_x
        dy = end_y - start_y
        angle = math.atan2(dy, dx)
        
        # Arrow body
        pygame.draw.line(self.win, self.ARROW_COLOR, (start_x, start_y), (end_x, end_y), 2)
        
        # Arrow head
        arrow_size = 10
        end_x = end_x - self.NODE_RADIUS * math.cos(angle)
        end_y = end_y - self.NODE_RADIUS * math.sin(angle)
        
        pygame.draw.polygon(self.win, self.ARROW_COLOR, [
            (end_x, end_y),
            (end_x - arrow_size * math.cos(angle - math.pi/6), end_y - arrow_size * math.sin(angle - math.pi/6)),
            (end_x - arrow_size * math.cos(angle + math.pi/6), end_y - arrow_size * math.sin(angle + math.pi/6))
        ])

    def draw_linked_list(self):
        """Draw the entire linked list"""
        if not self.linked_list or self.linked_list.length == 0:
            # Draw "Empty List" text if there's no list
            text = self.font.render("Empty List", True, self.TEXT_COLOR)
            self.win.blit(text, (self.width // 2 - 50, self.height // 2))
            return
        
        # Start drawing from the head
        current = self.linked_list.head
        x, y = self.STARTING_X, self.STARTING_Y
        
        while current:
            is_head = (current == self.linked_list.head)
            is_tail = (current == self.linked_list.tail)
            
            # Draw the node
            self.draw_node(x, y, current.value, is_head, is_tail)
            
            # Draw the arrow if there's a next node
            if current.next:
                self.draw_arrow(x + self.NODE_RADIUS, y, 
                               x + self.NODE_SPACING - self.NODE_RADIUS, y)
            
            # Move to the next node position
            x += self.NODE_SPACING
            current = current.next
            
            # If we're about to go off screen, wrap to next line
            if x + self.NODE_RADIUS > self.width:
                x = self.STARTING_X
                y += 100

    def draw_buttons(self):
        """Draw UI buttons"""
        for button in self.buttons:
            pygame.draw.rect(self.win, (100, 100, 100), button['rect'])
            pygame.draw.rect(self.win, (200, 200, 200), button['rect'], 2)
            
            text = self.small_font.render(button['label'], True, self.TEXT_COLOR)
            text_rect = text.get_rect(center=button['rect'].center)
            self.win.blit(text, text_rect)

    def draw_educational_button(self):
        """Draw the educational mode toggle button"""
        color = (34, 139, 34) if self.educational_mode else (139, 69, 19)  # Green if on, brown if off
        pygame.draw.rect(self.win, color, self.edu_button['rect'])
        pygame.draw.rect(self.win, (200, 200, 200), self.edu_button['rect'], 2)
        
        text = self.small_font.render(self.edu_button['label'], True, self.TEXT_COLOR)
        text_rect = text.get_rect(center=self.edu_button['rect'].center)
        self.win.blit(text, text_rect)

    def handle_events(self, event):
        """Handle pygame events for the visualizer"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                pos = pygame.mouse.get_pos()
                
                # Check educational button
                if self.edu_button['rect'].collidepoint(pos):
                    self.educational_mode = not self.educational_mode
                    self.edu_button['label'] = 'Educational: ON' if self.educational_mode else 'Educational: OFF'
                    return True
                
                # Check operation buttons
                for button in self.buttons:
                    if button['rect'].collidepoint(pos):
                        button['callback']()
                        return True
        return False


    # Operation handlers with educational context
    def append_operation(self):
        """Handle append operation with user input and educational context"""
        if self.educational_mode:
            self.show_educational_popup(
                "Append Operation - How it Works",
                "APPEND adds a new node to the END of the linked list.\n\n"
                "Steps:\n"
                "1. Create a new node with the given value\n"
                "2. If the list is empty:\n"
                "   - Set both head and tail to point to the new node\n"
                "3. If the list has nodes:\n"
                "   - Set the current tail's 'next' pointer to the new node\n"
                "   - Update the tail pointer to point to the new node\n"
                "4. Increment the length counter\n\n"
                "Time Complexity: O(1) - constant time\n"
                "The tail pointer allows us to add at the end instantly!"
            )
        
        value = self._get_input_value("Enter value to append:")
        if value is not None:
            self.linked_list.append(value)

    def prepend_operation(self):
        """Handle prepend operation with user input and educational context"""
        if self.educational_mode:
            self.show_educational_popup(
                "Prepend Operation - How it Works",
                "PREPEND adds a new node to the BEGINNING of the linked list.\n\n"
                "Steps:\n"
                "1. Create a new node with the given value\n"
                "2. If the list is empty:\n"
                "   - Set both head and tail to point to the new node\n"
                "3. If the list has nodes:\n"
                "   - Set the new node's 'next' pointer to the current head\n"
                "   - Update the head pointer to point to the new node\n"
                "4. Increment the length counter\n\n"
                "Time Complexity: O(1) - constant time\n"
                "Adding at the beginning is always fast in a linked list!"
            )
        
        value = self._get_input_value("Enter value to prepend:")
        if value is not None:
            self.linked_list.prepend(value)

    def insert_operation(self):
        """Handle insert operation with user input and educational context"""
        if self.educational_mode:
            self.show_educational_popup(
                "Insert Operation - How it Works",
                "INSERT adds a new node at a SPECIFIC POSITION in the linked list.\n\n"
                "Steps:\n"
                "1. Check if the index is valid (0 ≤ index ≤ length)\n"
                "2. If index is 0: use prepend (add at beginning)\n"
                "3. If index equals length: use append (add at end)\n"
                "4. Otherwise:\n"
                "   - Traverse to the node BEFORE the target position\n"
                "   - Create a new node with the given value\n"
                "   - Set new node's 'next' to point to the current node at index\n"
                "   - Set previous node's 'next' to point to the new node\n"
                "5. Increment the length counter\n\n"
                "Time Complexity: O(n) - we might need to traverse the entire list\n"
                "The further the index, the longer it takes!"
            )
        
        index = self._get_input_value("Enter index to insert at:")
        if index is not None:
            value = self._get_input_value("Enter value to insert:")
            if value is not None:
                success = self.linked_list.insert(index, value)
                if not success and self.educational_mode:
                    self.show_educational_popup(
                        "Insert Failed",
                        f"Invalid index: {index}\n\n"
                        f"Valid range: 0 to {self.linked_list.length}\n"
                        "Remember: index 0 is the first position!"
                    )

    def remove_operation(self):
        """Handle remove operation with user input and educational context"""
        if self.educational_mode:
            self.show_educational_popup(
                "Remove Operation - How it Works",
                "REMOVE deletes a node at a SPECIFIC POSITION in the linked list.\n\n"
                "Steps:\n"
                "1. Check if the index is valid (0 ≤ index < length)\n"
                "2. If index is 0: use pop_first (remove first node)\n"
                "3. If index is last position: use pop (remove last node)\n"
                "4. Otherwise:\n"
                "   - Traverse to the node BEFORE the target position\n"
                "   - Store reference to the node to be removed\n"
                "   - Set previous node's 'next' to skip the target node\n"
                "   - Break the removed node's connection (set its 'next' to None)\n"
                "5. Decrement the length counter\n\n"
                "Time Complexity: O(n) - we might need to traverse the list\n"
                "Important: We must update pointers to 'bridge' the gap!"
            )
        
        index = self._get_input_value("Enter index to remove:")
        if index is not None:
            removed = self.linked_list.remove(index)
            if removed is None and self.educational_mode:
                self.show_educational_popup(
                    "Remove Failed", 
                    f"Invalid index: {index}\n\n"
                    f"Valid range: 0 to {self.linked_list.length - 1}\n"
                    "The list has indices from 0 to length-1!"
                )

    def pop_operation(self):
        """Handle pop operation with educational context"""
        if self.educational_mode:
            self.show_educational_popup(
                "Pop Operation - How it Works",
                "POP removes the LAST node from the linked list.\n\n"
                "Steps:\n"
                "1. If list is empty: return None\n"
                "2. Traverse the entire list to find:\n"
                "   - The last node (current tail)\n"
                "   - The second-to-last node (new tail)\n"
                "3. Set the second-to-last node's 'next' pointer to None\n"
                "4. Update the tail pointer to the second-to-last node\n"
                "5. Decrement the length counter\n"
                "6. Handle special case: if list becomes empty, set head and tail to None\n\n"
                "Time Complexity: O(n) - must traverse to find the second-to-last node\n"
                "This is why doubly linked lists exist - they make this O(1)!"
            )
        
        removed = self.linked_list.pop()
        if removed is None and self.educational_mode:
            self.show_educational_popup("Pop Failed", "Cannot pop from an empty list!")

    def pop_first_operation(self):
        """Handle pop_first operation with educational context"""
        if self.educational_mode:
            self.show_educational_popup(
                "Pop First Operation - How it Works",
                "POP FIRST removes the FIRST node from the linked list.\n\n"
                "Steps:\n"
                "1. If list is empty: return None\n"
                "2. Store reference to the current head node\n"
                "3. Update head pointer to point to the second node (head.next)\n"
                "4. Break the removed node's connection (set its 'next' to None)\n"
                "5. Decrement the length counter\n"
                "6. Handle special case: if list becomes empty, set tail to None\n\n"
                "Time Complexity: O(1) - constant time\n"
                "Removing from the front is always fast in a linked list!\n"
                "This is an advantage over arrays where removing first element takes O(n)!"
            )

        removed = self.linked_list.pop_first()
        if removed is None and self.educational_mode:
            self.show_educational_popup("Pop First Failed", "Cannot pop from an empty list!")







    # Operation handlers with animation
    # def append_operation(self):
    #     """Handle append operation with user input"""
    #     value = self._get_input_value("Enter value to append:")
    #     if value is not None:
    #         self.linked_list.append(value)

    # def prepend_operation(self):
    #     """Handle prepend operation with user input"""
    #     value = self._get_input_value("Enter value to prepend:")
    #     if value is not None:
    #         self.linked_list.prepend(value)

    # def insert_operation(self):
    #     """Handle insert operation with user input"""
    #     index = self._get_input_value("Enter index to insert at:")
    #     if index is not None:
    #         value = self._get_input_value("Enter value to insert:")
    #         if value is not None:
    #             self.linked_list.insert(index, value)

    # def remove_operation(self):
    #     """Handle remove operation with user input"""
    #     index = self._get_input_value("Enter index to remove:")
    #     if index is not None:
    #         self.linked_list.remove(index)

    # def pop_operation(self):
    #     """Handle pop operation"""
    #     self.linked_list.pop()

    # def pop_first_operation(self):
    #     """Handle pop_first operation"""
    #     self.linked_list.pop_first()

    def _get_input_value(self, prompt):
        """Get input value from user using a tkinter dialog"""
        # Create root tkinter window but hide it
        root = tk.Tk()
        root.withdraw()
        
        # Make the dialog stay on top of the pygame window
        root.attributes("-topmost", True)
        
        # Show the dialog and wait for input
        value = simpledialog.askinteger("Input", prompt, parent=root)
        
        # Destroy the root window
        root.destroy()
        
        # Return the input value (will be None if user cancels)
        return value
    def draw(self):
        """Main draw method to be called from the game loop"""
        # Draw background
        self.win.fill(self.BACKGROUND)
        
        # Draw list length
        length_text = f"Length: {self.linked_list.length if self.linked_list else 0}"
        text_surf = self.font.render(length_text, True, self.TEXT_COLOR)
        self.win.blit(text_surf, (10, 10))
        
        # Draw linked list
        self.draw_linked_list()
        
        # Draw buttons
        self.draw_buttons()

        # Draw educational toggle button
        self.draw_educational_button()
        
        # Draw instructions
        if self.educational_mode:
            instruction_text = "Educational Mode: ON - Click operations for detailed explanations"
            text_surf = self.small_font.render(instruction_text, True, (144, 238, 144))
            self.win.blit(text_surf, (10, self.height - 100))