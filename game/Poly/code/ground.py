import pygame as pg

pg.init()

class Ground():
    def __init__(self, screen):
        # Размеры поля
        self.width = screen.get_size()[0]
        self.height = screen.get_size()[1]
        self.screen = screen
        pg.display.set_caption("Vampire Survivors")
        
        # Загрузка спрайта земли
        self.ground_sprite = pg.image.load("./Poly/sprites/ground.webp").convert_alpha()
        
        # Размеры тайла (если тайлим)
        self.tile_width = self.ground_sprite.get_width()
        self.tile_height = self.ground_sprite.get_height()
        
    def render_tiled(self):
        tiles_x = (self.width + self.tile_width - 1) // self.tile_width
        tiles_y = (self.height + self.tile_height - 1) // self.tile_height
        
        for y in range(tiles_y):
            for x in range(tiles_x):
                self.screen.blit(self.ground_sprite, 
                                 (x * self.tile_width, y * self.tile_height))
    
    
    
    def render(self):
        self.render_tiled()
        

# Тестовый запуск
if __name__ == "__main__":
    game = Ground("/Users/kazak/VS Code/Codes/game/Poly/sprites/ground.webp")