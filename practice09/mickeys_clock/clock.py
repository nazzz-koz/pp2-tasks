import pygame
from datetime import datetime


class MickeyClock:
    def __init__(self):
        import pygame
        pygame.init()

        self.clock_face_raw = pygame.image.load(
            "images/clock_face.png"
        )

        WIDTH, HEIGHT = self.clock_face_raw.get_size()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Mickey Clock")

        self.clock = pygame.time.Clock()

        self.clock_face = self.clock_face_raw.convert_alpha()

        self.mickey = pygame.image.load(
            "images/mickey_body.png"
        ).convert_alpha()
        self.mickey = pygame.transform.scale(self.mickey, (600, 600))

        self.minute_hand = pygame.image.load(
            "images/minute_hand.png"
        ).convert_alpha()
        self.minute_hand = pygame.transform.scale(self.minute_hand, (300, 300))

        self.second_hand = pygame.image.load(
            "images/second_hand.png"
        ).convert_alpha()
        self.second_hand = pygame.transform.scale(self.second_hand, (300, 320))

        self.center = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)
        self.pivot = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)

        self.minute_image_pivot = pygame.math.Vector2(30, -100)
        self.second_image_pivot = pygame.math.Vector2(-28, -125)

    def rotate_around_pivot(self, image, pivot, image_pivot, angle):
        rotated_image = pygame.transform.rotate(image, -angle)
        offset = pygame.math.Vector2(image_pivot)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect

    def get_time_angles(self):
        now = datetime.now()
        minutes = now.minute
        seconds = now.second

        minute_angle = (minutes + seconds / 60) * 6
        second_angle = seconds * 6

        return minute_angle, second_angle

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def draw(self):
        minute_angle, second_angle = self.get_time_angles()

        minute_img, minute_rect = self.rotate_around_pivot(
            self.minute_hand, self.pivot, self.minute_image_pivot, minute_angle
        )

        second_img, second_rect = self.rotate_around_pivot(
            self.second_hand, self.pivot, self.second_image_pivot, second_angle
        )

        self.screen.fill((30, 30, 30))

        self.screen.blit(self.clock_face, self.clock_face.get_rect(center=self.center))

        self.screen.blit(self.mickey, self.mickey.get_rect(center=self.center))

        self.screen.blit(minute_img, minute_rect)
        self.screen.blit(second_img, second_rect)

        pygame.display.flip()
        self.clock.tick(60)