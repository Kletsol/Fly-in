from src import Zone, Connection
from typing import Any
import colorsys
import contextlib
with contextlib.redirect_stdout(None):
    import pygame


class Visualizer:
    def __init__(self, zones: list[Any], connections: list[Any],
                 schedule: dict[str, list[list[Any]]]) -> None:
        self._running = True
        self.restart = False
        self._image_surf = None
        self._zones = zones
        self._connections = connections
        self.schedule = schedule
        self.camera_offset = [0, 0]
        self.scroll_speed = 20
        self.clock = pygame.time.Clock()
        self.animation_speed = 0.02
        self.color_loop = 0.0
        self.render_capacity = False
        self.logs: list[list[int | str]] = []

    def on_init(self) -> bool:
        pygame.init()
        self.size = self.width, self.height = 3840, 2160
        self._display_surf = pygame.display.set_mode(self.size,
                                                     pygame.HWSURFACE |
                                                     pygame.DOUBLEBUF)
        self._drone_image = pygame.transform.scale(
            pygame.image.load("src/assets/drone.png").convert_alpha(),
            (61, 61))
        self.font = pygame.font.SysFont("Arial", 26, True)
        self._running = True
        return True

    def on_event(self, event: Any) -> None:
        if event.type == pygame.QUIT:
            self.restart = False
            self._running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                if self.animation_speed > 0:
                    self.animation_speed = 0
                else:
                    self.animation_speed = 0.02
            if event.key == pygame.K_c:
                if self.render_capacity:
                    self.render_capacity = False
                else:
                    self.render_capacity = True
            if event.key == pygame.K_ESCAPE:
                self.restart = False
                self._running = False
            if event.key == pygame.K_r:
                self.restart = True
                self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and self.camera_offset[1] < 0:
                self.camera_offset[1] += self.scroll_speed
            if event.button == 5 and self.camera_offset[1] > -3000:
                self.camera_offset[1] -= self.scroll_speed

    def on_loop(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and self.animation_speed < 0.2:
            self.animation_speed += 0.001
        if keys[pygame.K_s] and self.animation_speed > 0:
            self.animation_speed -= 0.001
        if keys[pygame.K_LEFT] and self.camera_offset[0] < 0:
            self.camera_offset[0] += self.scroll_speed
        if keys[pygame.K_RIGHT] and self.camera_offset[0] > -3800:
            self.camera_offset[0] -= self.scroll_speed
        if keys[pygame.K_UP] and self.camera_offset[1] < 0:
            self.camera_offset[1] += self.scroll_speed
        if keys[pygame.K_DOWN] and self.camera_offset[1] > -3000:
            self.camera_offset[1] -= self.scroll_speed

    def rainbow_color(self, speed: float = 0.2) -> tuple[int, int, int]:
        color = (pygame.time.get_ticks() * speed / 1000) % 1.0
        r, g, b = colorsys.hsv_to_rgb(color, 1, 1)
        return (int(r * 255), int(g * 255), int(b * 255))

    def on_render_zone(self, zone: Zone) -> None:
        coords = zone.get_visual_coords()
        if zone.get_color() == 'rainbow':
            color = self.rainbow_color()
        else:
            color = zone.get_rgb()

        x_coord = coords[0] + self.camera_offset[0]
        y_coord = coords[1] + self.camera_offset[1]
        x_text = x_coord
        y_text = y_coord - 32

        text_surf = self.font.render(zone.name, True, color)
        capacity_surf = self.font.render(str(zone.get_capacity()), True, color)
        pygame.draw.rect(self._display_surf, color, (x_coord, y_coord, 61, 61))
        self._display_surf.blit(text_surf, (x_text, y_text))
        self._display_surf.blit(capacity_surf, (x_text, y_text - 46))

    def on_render_connection(self, connection: Connection) -> None:
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

    def on_render_drone(self, current_zone: Zone, next_zone: Zone,
                        progress: float) -> None:
        start_pos = current_zone.get_visual_coords()
        end_pos = next_zone.get_visual_coords()

        if start_pos == end_pos:
            draw_x = float(end_pos[0] + self.camera_offset[0])
            draw_y = float(end_pos[1] + self.camera_offset[1])

        elif start_pos and end_pos:
            # Linear interpolation between zone and next zone positions
            interp_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
            interp_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress

            # Camera offset application
            draw_x = interp_x + self.camera_offset[0]
            draw_y = interp_y + self.camera_offset[1]

        # Display
        self._display_surf.blit(self._drone_image, (draw_x, draw_y))

    def on_render_turn(self, turn: int) -> None:
        text_surf = self.font.render(f"Turn counter: {str(turn)}", True,
                                     (255, 255, 0))
        self._display_surf.blit(text_surf, (8, 8))

    def on_render_occupancy(self, current_time: int) -> None:
        occupancy_counts = {zone.name: 0 for zone in self._zones}

        # 2. Broswe schedule to find where each drone is
        for drone, path in self.schedule.items():
            for i in range(len(path) - 1):
                t1, z1 = path[i]
                t2, z2 = path[i+1]

                # Restricted connections management
                if t1 <= current_time < t2:
                    if z1 in occupancy_counts:
                        occupancy_counts[z1] += 1
                    break
            else:
                # If current time reaches the last turn, all drones are on goal
                if current_time >= path[-1][0]:
                    final_zone = path[-1][1]
                    if final_zone in occupancy_counts:
                        occupancy_counts[final_zone] += 1

        for zone in self._zones:
            count = occupancy_counts[zone.name]
            coords = zone.get_visual_coords()
            x_text = coords[0] + self.camera_offset[0]
            y_text = coords[1] + self.camera_offset[1] + 65

            summary = f"{count} / {zone.get_capacity()}"
            color = (255, 255, 255) if count <= zone.get_capacity() else (255,
                                                                          0, 0)

            text_surf = self.font.render(summary, True, color)
            self._display_surf.blit(text_surf, (x_text, y_text))

    def get_steps(self, turn: int, drone: str, path: list[list[Any]]) -> str:
        step_summary = ''

        for i in range(1, len(path)):
            current_turn, current_zone = path[i]
            previous_zone = path[i - 1][1]
            if (
                current_turn == turn
                and current_zone != 'start'
                and current_zone != previous_zone
            ):
                step_summary += f" {drone}-{current_zone}"

        return step_summary

    def on_render_steps(self, turn_steps: str) -> None:
        text_surf = self.font.render(turn_steps, True, (255, 255, 255))
        self._display_surf.blit(text_surf, (100, 100))

    def on_cleanup(self) -> None:
        pygame.display.quit()
        pygame.quit()

    def get_zones(self, path: list[list[Any]], turn: int) -> tuple[Zone, Zone]:
        for zone in self._zones:
            if zone.name == path[turn][1]:
                current_zone = zone
            if turn >= 0:
                if zone.name == path[turn + 1][1]:
                    next_zone = zone
            elif zone.name == path[turn][1]:
                next_zone = zone
        return current_zone, next_zone

    def on_execute(self) -> bool:
        turn = 0
        self.color_loop = 0.0
        self.global_time = 0.0
        stop = False
        final_turn = 0
        if self.on_init() is False:
            self._running = False

        image = pygame.transform.scale(
            pygame.image.load("src/assets/background.jpg").convert(),
            self.size)
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()

            # Turn counter, connections and zones rendering
            self._display_surf.blit(image, (0, 0))
            if not stop:
                self.on_render_turn(int(self.global_time))
            else:
                self.on_render_turn(final_turn)
            for connection in self._connections:
                self.on_render_connection(connection)
            for zone in self._zones:
                self.on_render_zone(zone)

            turn_steps = 'Current turn :'
            if self.render_capacity is True:
                self.on_render_occupancy(int(self.global_time))

            # Drones animation management
            for drone, path in self.schedule.items():
                final_turn = int(
                        self.schedule[list(self.schedule.keys())[-1]][-1][0])
                if int(self.global_time) >= final_turn:
                    stop = True
                turn_steps += self.get_steps(int(self.global_time) + 1, drone,
                                             path)

                for i in range(len(path) - 1):
                    t1, z1 = path[i]
                    t2, z2 = path[i + 1] if '-' not in path[i + 1][1] else\
                        path[i + 2]

                    if t1 <= self.global_time <= t2:
                        duration = t2 - t1
                        local_progress = (self.global_time - t1) / duration
                        zone = next(zone for zone in self._zones if
                                    zone.name == z1)
                        next_zone = next(zone for zone in self._zones if
                                         zone.name == z2)
                        self.on_render_drone(zone, next_zone, local_progress)
                        break

            if [int(self.global_time) + 1, turn_steps.split(':')[-1]] not in \
                    self.logs and int(self.global_time) < final_turn:
                self.logs.append([int(self.global_time) + 1,
                                  turn_steps.split(':')[-1]])
            if not stop:
                self.on_render_steps(turn_steps)
            self.global_time += self.animation_speed
            self.color_loop += 0.1
            if self.color_loop > 0.6:
                self.color_loop = 0.0
            turn += 1
            pygame.display.flip()
            self.clock.tick(60)
        self.on_cleanup()
        return self.restart
