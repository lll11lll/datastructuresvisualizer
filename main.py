# Nicholas Greiner 
# 03/18/2025
# This is a project utilizing the pygame library to visualize data structures

import pygame
from DataStructures.LinkedList import LinkedList
from Visualizers.LinkedListVisualizer import LinkedListVisualizer
from Visualizers.MenuSystem import MainMenu, SelectionMenu
# Constants and Variables
# Window dimensions
WIDTH = 800
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Data Structures Visualized")

# Clock 
clock = pygame.time.Clock()

def main():
    # Init pygame
    pygame.init()

    # Menu 
    main_menu = MainMenu(WIN, WIDTH, HEIGHT)
    selection_menu = SelectionMenu(WIN, WIDTH, HEIGHT)

    # Initialize current state
    current_state = "main_menu"
    selected_structure = None
    visualizer = None
    # test visualizer
    
    
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle state-specific events
            if current_state == "main_menu":
                result = main_menu.handle_events(event)
                if result == "selection":
                    current_state = "selection"

            elif current_state == "selection":
                result = selection_menu.handle_events(event)
                if result == "main_menu":
                    current_state = "main_menu"
                elif result in ["Linked List"]:
                    
                    selected_structure = result
                    current_state = "visualization"

                    # Initialize the visualizer for the selected structure
                    if selected_structure == "Linked List":
                        my_ll = LinkedList(1)
                        LL_vis = LinkedListVisualizer(WIN, WIDTH, HEIGHT)
                        LL_vis.set_linked_list(my_ll)
                        visualizer = LinkedListVisualizer(WIN, WIDTH, HEIGHT)
                        visualizer.set_linked_list(my_ll)

            elif current_state == "visualization":

                # handle visualizer events and check for back button
                if visualizer:
                    handle = visualizer.handle_events(event)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        current_state = "selection"
                        visualizer = None
        if current_state == "main_menu":
            main_menu.update()
            main_menu.draw()
        elif current_state == "selection":
            selection_menu.draw()
        elif current_state == "visualization":
            if visualizer:
                visualizer.draw()
        pygame.display.flip()


main()

