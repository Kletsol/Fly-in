import pygame


class Visualizer:
    def __init__(self, zones, connections, drones):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._zones = zones
        self._connections = connections
        self.drones = drones
        self.size = self.width, self.height = 3840, 2160
        self.camera_offset = [0, 0]
        self.scroll_speed = 20
        self.clock = pygame.time.Clock()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size,
                                                     pygame.HWSURFACE |
                                                     pygame.DOUBLEBUF)
        self.font = pygame.font.SysFont("Arial", 26)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and self.camera_offset[1] < 0:
                self.camera_offset[1] += self.scroll_speed
            if event.button == 5 and self.camera_offset[1] > -3000:
                self.camera_offset[1] -= self.scroll_speed

    def on_loop(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.camera_offset[0] < 0:
            self.camera_offset[0] += self.scroll_speed
        if keys[pygame.K_RIGHT] and self.camera_offset[0] > -3800:
            self.camera_offset[0] -= self.scroll_speed
        if keys[pygame.K_UP] and self.camera_offset[1] < 0:
            self.camera_offset[1] += self.scroll_speed
        if keys[pygame.K_DOWN] and self.camera_offset[1] > -3000:
            self.camera_offset[1] -= self.scroll_speed

    def on_render_zone(self, zone):
        coords = zone.get_visual_coords()
        color = zone.get_rgb()
        x_coord = coords[0] + self.camera_offset[0]
        y_coord = coords[1] + self.camera_offset[1]
        text_surf = self.font.render(zone.name, True, color)
        x_text = x_coord
        y_text = y_coord - 32
        self._display_surf.blit(text_surf, (x_text, y_text))
        pygame.draw.rect(self._display_surf, color, (x_coord, y_coord, 61, 61))

    def on_render_connection(self, connection):
        zones = connection.get_linked_zones()
        for zone in self._zones:
            if zone.name == zones[0]:
                start = zone.get_visual_coords()
                start[0] += 30 + self.camera_offset[0]
                start[1] += 30 + self.camera_offset[1]
            if zone.name == zones[1]:
                end = zone.get_visual_coords()
                end[0] += 30 + self.camera_offset[0]
                end[1] += 30 + self.camera_offset[1]
        pygame.draw.line(self._display_surf, (255, 255, 255), start, end, 2)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False
        image = pygame.transform.scale(
            pygame.image.load("image_test.jpg").convert(), self.size)
        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self._display_surf.blit(image, (0, 0))
            for connection in self._connections:
                self.on_render_connection(connection)
            for zone in self._zones:
                self.on_render_zone(zone)
            pygame.display.set_caption("Fly-in")
            pygame.display.flip()
            self.clock.tick(60)
        self.on_cleanup()
