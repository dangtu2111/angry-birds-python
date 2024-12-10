import time
import pygame


class GameStateManager():
    """Manages game objects like birds, pigs, and structures"""
    def __init__(self, resources):
        self.game_state = 0
        self.resource=resources

    def draw_level_cleared(self):
        """Draw level cleared"""
        
        level_cleared = self.resource.font01.render("LEVEL CLEARED!", 1, self.resource.WHITE)
        text_score = self.resource.font03.render("HIGHT SCORE!", 1, self.resource.WHITE)
        score_level_cleared = self.resource.font02.render(str(self.resource.score), 1, self.resource.WHITE)
        image = pygame.image.load("./resources/images/color.jpg")  # Đường dẫn tới ảnh của bạn
        image = pygame.transform.scale(image, (400, 300))  # Đảm bảo ảnh đủ lớn để phủ lên văn bản
        text_width, text_height = score_level_cleared.get_size()
        # Tạo mask từ văn bản
        text_mask = pygame.mask.from_surface(score_level_cleared)
        text_image_surface = pygame.Surface((text_width, text_height), pygame.SRCALPHA)
        # Áp dụng hình ảnh vào từng pixel hiển thị của văn bản
        for x in range(text_width):
            for y in range(text_height):
                if text_mask.get_at((x, y)):
                    # Lấy màu từ hình ảnh tại vị trí tương ứng
                    color = image.get_at((x, y))
                    text_image_surface.set_at((x, y), color)
        if self.resource.level.number_of_birds >= 0 and len(self.resource.pigs) == 0 and len(self.resource.pigsBoss)==0:
            if self.resource.bonus_score_once:
                self.resource.score += (self.resource.level.number_of_birds-1) * 10000
            self.resource.bonus_score_once = False
            self.game_state = 4
            overlay = pygame.Surface((self.resource.SCREEN_WIDTH, self.resource.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Màu đen bán trong suốt (150 là giá trị alpha)
                # Tạo vùng trong suốt trên overlay
            rect = pygame.Rect(380, 0, 450, 800)
            pygame.draw.rect(overlay, (0, 0, 0, 0), rect)  # Xóa màu vùng rect (alpha = 0)

            # Vẽ overlay lên màn hình
            self.resource.screen.blit(overlay, (0, 0))
            rect = pygame.Rect(380, 0, 450, 800)
            pygame.draw.rect(self.resource.screen, self.resource.BLACK, rect)
            self.resource.screen.blit(level_cleared, (470, 70))
            if self.resource.score >= self.resource.level.one_star and self.resource.score <= self.resource.level.two_star:
                self.resource.screen.blit(self.resource.star2, (500, 150))
                self.resource.screen.blit(text_score, (550, 420))

                self.resource.count_start=self.resource.count_start+1
            elif self.resource.score >= self.resource.level.two_star and self.resource.score <= self.resource.level.three_star:
                self.resource.screen.blit(self.resource.star1, (310, 190))
                self.resource.screen.blit(text_score, (550, 420))
                self.resource.screen.blit(self.resource.star2, (500, 150))
                self.resource.count_start=self.resource.count_start+2
            elif self.resource.score >= self.resource.level.three_star:
                self.resource.screen.blit(self.resource.star1, (310, 150))
                self.resource.screen.blit(self.resource.star2, (500, 130))
                self.resource.screen.blit(self.resource.star3, (700, 160))
                self.resource.screen.blit(text_score, (550, 420))

                self.resource.count_start=self.resource.count_start+3
            else:
                self.resource.screen.blit(self.resource.scaled_false_score, (485, 150))
                text_score = self.resource.font03.render("LOW SCORE!", 1, self.resource.WHITE)
                self.resource.screen.blit(text_score, (550, 420))


            self.resource.screen.blit(text_image_surface, (500, 350))
            scaled_surface = pygame.transform.scale(self.resource.smile, (100, 100))
            self.resource.screen.blit(scaled_surface, (800, 480))
            self.resource.screen.blit(self.resource.replay_button, (510, 480))
            self.resource.screen.blit(self.resource.next_button, (620, 480))


    def draw_level_failed(self):
        """Draw level failed"""
        failed = self.resource.font01.render("Level Failed", 1, self.resource.WHITE)
        if self.resource.level.number_of_birds <= 0 and time.time() - self.resource.t2 > 5 and len(self.resource.pigs) > 0:
            self.game_state = 3
            rect = pygame.Rect(300, 0, 600, 800)
            pygame.draw.rect(self.resource.screen, self.resource.BLACK, rect)
            self.resource.screen.blit(failed, (450, 90))
            self.resource.screen.blit(self.resource.pig_happy, (380, 120))
            self.resource.screen.blit(self.resource.replay_button, (520, 460))


    def restart(self):
        """Delete all objects of the level"""
        pigs_to_remove = []
        boss_to_remove = []
        self.resource.birds_to_remove = []
        columns_to_remove = []
        beams_to_remove = []
        for pig in self.resource.pigs:
            pigs_to_remove.append(pig)
        for pig in pigs_to_remove:
            self.resource.space.remove(pig.shape, pig.shape.body)
            self.resource.pigs.remove(pig)
        for bird in self.resource.birds:
            self.resource.birds_to_remove.append(bird)
        for bird in self.resource.birds_to_remove:
            self.resource.space.remove(bird.shape, bird.shape.body)
            self.resource.birds.remove(bird)
        for column in self.resource.columns:
            columns_to_remove.append(column)
        for column in columns_to_remove:
            self.resource.space.remove(column.shape, column.shape.body)
            self.resource.columns.remove(column)
        for beam in self.resource.beams:
            beams_to_remove.append(beam)
        for beam in beams_to_remove:
            self.resource.space.remove(beam.shape, beam.shape.body)
            self.resource.beams.remove(beam)
        for boss in self.resource.pigsBoss:
            boss_to_remove.append(boss)
        for boss in boss_to_remove:
            self.resource.space.remove(boss.shape,boss.shape.body)
            self.resource.pigsBoss.remove(boss)