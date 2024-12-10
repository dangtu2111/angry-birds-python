import os
import sys
import pygame

from AngryBirdsGame import AngryBirds
current_path = os.getcwd()
from Resources import GameResources
from characters import Bird
from level import Level

song1 = './resources/sounds/angry-birds.ogg'
def show_prepare_page(resource,game):
    running = True
    while running:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Kiểm tra nếu nút Bắt đầu được nhấn
                if start_button.collidepoint(mouse_pos):
                    running = False  # Thoát khỏi vòng lặp này và bắt đầu trò chơi
                    game.run()

        # Vẽ nền
        background_image = pygame.image.load("./resources/images/background_start.jpg")
        background_image = pygame.transform.scale(background_image, (1200, 650))
        resource.screen.blit(background_image, (0, 0))


     

        # Vẽ hướng dẫn
        instruction_text = resource.font01.render("WELLCOME TO ANGRY BIRD", True, resource.BLACK)
        instruction_rect = instruction_text.get_rect(center=(600, 170))
        resource.screen.blit(instruction_text, instruction_rect)

       # Vẽ nút Bắt đầu với góc bo tròn
        start_button = pygame.Rect(0, 0, 200, 50)  # Khởi tạo Rect
        start_button.center = (600, 550)  
        pygame.draw.rect(resource.screen, resource.RED, start_button, border_radius=15)  # Thêm border_radius

        # Vẽ văn bản "PLAY" ở giữa nút
        start_text = resource.font01.render("PLAY", True, resource.WHITE)
        start_text_rect = start_text.get_rect(center=start_button.center)
        resource.screen.blit(start_text, start_text_rect)


        # Cập nhật màn hình
        pygame.display.flip()
def main():
    """Start the game"""
    pygame.init()
    resource = GameResources()
    game = AngryBirds(song1,resource)
    show_prepare_page(resource,game)
    pygame.quit()

if __name__ == "__main__":
    main()