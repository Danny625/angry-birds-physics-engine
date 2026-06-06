from __future__ import annotations

from pathlib import Path
from typing import Optional

import pygame

from angrybirds.constants import (
    ACCENT_GOLD,
    ASSET_DIR,
    BIRD_RESET_CENTER,
    BUILDER_PLAY_CENTER,
    BUILDER_RESET_CENTER,
    BUTTON_FILL,
    BUTTON_HIGHLIGHT,
    BUTTON_TEXT,
    DARK_TEXT,
    FLOOR_GREEN,
    FPS,
    FLOOR_Y,
    GRID_LINE,
    HOME_BUTTON_CENTER,
    HOME_MENU_BUTTON_HEIGHT,
    HOME_MENU_BUTTON_WIDTH,
    HOME_MENU_GAP,
    HOME_MENU_TOP,
    INIT_BIRD_X,
    INIT_BIRD_Y,
    PANEL_DARK,
    PANEL_FILL,
    PANEL_OUTLINE,
    PANEL_SOFT,
    PALETTE_BOX_SIZE,
    PALETTE_CENTERS,
    SKY_BLUE,
    SPRITE_SIZES,
    SPRITE_PATHS,
    SUCCESS_GREEN,
    TEXT_MUTED,
    TILE_SIZE,
    TRAJECTORY_BLUE,
    UNDO_BUTTON_CENTER,
    WARNING_RED,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from angrybirds.engine import GameEngine, distance
from angrybirds.levels import delete_saved_builder_level, list_saved_builder_levels, load_all_levels
from angrybirds.models import GameState, LevelSpec
from angrybirds.scores import get_high_score, save_high_score


class PygameClient:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Angry Birds - Physics Sandbox")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.micro_font = pygame.font.SysFont("arial", 18)
        self.tiny_font = pygame.font.SysFont("arial", 20)
        self.small_font = pygame.font.SysFont("arial", 24)
        self.medium_font = pygame.font.SysFont("arial", 34, bold=True)
        self.large_font = pygame.font.SysFont("arial", 52, bold=True)
        self.hero_font = pygame.font.SysFont("arial", 28, bold=True)
        self.engine = GameEngine(load_all_levels())
        self.assets = self._load_assets()
        self.mode = "home"
        self.running = True
        self.show_help_overlay = False
        self.show_builder_load_menu = False
        self.builder_load_entries: list[tuple[Path, LevelSpec]] = []
        self.builder_load_page = 0
        self.show_save_dialog = False
        self.save_dialog_mode = "new"
        self.save_dialog_text = ""
        self.result_recorded_level_id: Optional[str] = None
        self.status_message = ""
        self.status_message_frames = 0
        self.home_buttons = self._build_home_buttons()

    def _load_assets(self) -> dict[str, pygame.Surface]:
        assets: dict[str, pygame.Surface] = {}
        for key, relative_path in SPRITE_PATHS.items():
            path = ASSET_DIR / relative_path
            if path.exists():
                assets[key] = pygame.image.load(str(path)).convert_alpha()

        if "bird_blue" not in assets:
            base_bird = assets.get("bird_yellow") or assets.get("bird_red")
            if base_bird is not None:
                assets["bird_blue"] = self._build_blue_bird_surface(base_bird)

        for key, size in SPRITE_SIZES.items():
            if key in assets:
                assets[key] = pygame.transform.smoothscale(assets[key], size)

        if "background" in assets:
            assets["background"] = pygame.transform.smoothscale(
                assets["background"], (WINDOW_WIDTH, WINDOW_HEIGHT)
            )
        if "title" in assets:
            assets["title"] = pygame.transform.smoothscale(assets["title"], (560, 188))
        if "home_button" in assets:
            assets["home_button"] = pygame.transform.smoothscale(
                assets["home_button"], (60, 60)
            )
        if "back_button" in assets:
            assets["back_button"] = pygame.transform.smoothscale(
                assets["back_button"], (60, 60)
            )
        return assets

    def _build_blue_bird_surface(self, surface: pygame.Surface) -> pygame.Surface:
        blue_surface = surface.copy()
        tint = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        tint.fill((70, 95, 255, 255))
        blue_surface.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        brighten = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        brighten.fill((35, 45, 125, 0))
        blue_surface.blit(brighten, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return blue_surface

    def _build_home_buttons(self) -> list[tuple[str, pygame.Rect, str, str]]:
        subtitles = {
            "level1": "Warm-up build and basic materials",
            "level2": "Tall stacks and falling columns",
            "level3": "Rolling hazards and timing shots",
            "level4": "Mixed materials with tighter windows",
            "level5": "Longer siege with layered defenses",
        }
        buttons: list[tuple[str, pygame.Rect, str, str]] = []
        ordered_ids = sorted(self.engine.levels)
        for index, level_id in enumerate(ordered_ids):
            rect = pygame.Rect(0, 0, HOME_MENU_BUTTON_WIDTH, HOME_MENU_BUTTON_HEIGHT)
            rect.center = (1010, HOME_MENU_TOP + index * HOME_MENU_GAP)
            buttons.append(
                (
                    level_id,
                    rect,
                    self.engine.levels[level_id].name,
                    subtitles.get(level_id, "Story level"),
                )
            )

        builder_rect = pygame.Rect(0, 0, HOME_MENU_BUTTON_WIDTH, HOME_MENU_BUTTON_HEIGHT)
        builder_rect.center = (1010, HOME_MENU_TOP + len(ordered_ids) * HOME_MENU_GAP)
        buttons.append(
            ("builder", builder_rect, "Builder Mode", "Sandbox, playtest, and iterate")
        )
        return buttons

    def run(self) -> None:
        while self.running:
            self._handle_events()
            if self.mode == "level" or (
                self.mode == "builder" and self.engine.state.builder_playing
            ):
                self.engine.tick()
                self._record_completed_score()
            if self.status_message_frames > 0:
                self.status_message_frames -= 1
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_down(*event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(*event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._handle_mouse_up(*event.pos)

    def _start_level(self, level_id: str) -> None:
        self.engine.start_level(level_id)
        self.mode = "level"
        self.result_recorded_level_id = None
        self.show_help_overlay = False
        self.show_builder_load_menu = False
        self.show_save_dialog = False
        self.status_message_frames = 0

    def _start_builder(self) -> None:
        self.engine.start_builder()
        self.mode = "builder"
        self.result_recorded_level_id = None
        self.show_help_overlay = False
        self.show_builder_load_menu = False
        self.show_save_dialog = False
        self.status_message_frames = 0

    def _record_completed_score(self) -> None:
        state = self.engine.state
        if (
            self.mode != "level"
            or not state.won
            or not state.level_id
            or self.result_recorded_level_id == state.level_id
        ):
            return

        score = max(0, state.score)
        is_new_best = save_high_score(state.level_id, score)
        self.result_recorded_level_id = state.level_id
        if is_new_best:
            self._set_status_message(f"New best for {state.level_name}: {score}")

    def _open_builder_load_menu(self) -> None:
        self._refresh_builder_load_entries()
        if not self.builder_load_entries:
            self._set_status_message("No saved builder levels yet. Use Save first.")
            return
        self._clamp_builder_load_page()
        self.show_builder_load_menu = True

    def _open_save_dialog(self, mode: str) -> None:
        self.save_dialog_mode = mode
        if mode == "replace" and self.engine.current_builder_save_path is not None:
            self.save_dialog_text = self.engine.export_builder_level().name
            for save_path, level in list_saved_builder_levels():
                if save_path == self.engine.current_builder_save_path:
                    self.save_dialog_text = level.name
                    break
        else:
            slot_number = len(list_saved_builder_levels()) + 1
            self.save_dialog_text = f"Builder Level {slot_number:02d}"
        self.show_save_dialog = True
        self.show_builder_load_menu = False

    def _handle_save_dialog_keydown(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            self.show_save_dialog = False
            return
        if event.key == pygame.K_RETURN:
            self._commit_save_dialog()
            return
        if event.key == pygame.K_BACKSPACE:
            self.save_dialog_text = self.save_dialog_text[:-1]
            return
        if event.unicode and len(self.save_dialog_text) < 32:
            if event.unicode.isprintable():
                self.save_dialog_text += event.unicode

    def _commit_save_dialog(self) -> None:
        level_name = self.save_dialog_text.strip() or "Untitled Builder Level"
        if self.save_dialog_mode == "replace":
            saved_level, save_path = self.engine.replace_current_builder_level(
                name=level_name
            )
        else:
            saved_level, save_path = self.engine.save_builder_level_to_next_slot(
                name=level_name
            )
        self.show_save_dialog = False
        self._set_status_message(f"Saved {saved_level.name} to {save_path.name}")

    def _handle_hud_button_click(self, mouse_x: int, mouse_y: int) -> bool:
        for action, _label, rect, _color in self._hud_button_specs():
            if not rect.collidepoint(mouse_x, mouse_y):
                continue
            if action == "replace" and self.engine.current_builder_save_path is None:
                self._set_status_message("Load a saved level before replacing it.")
                return True
            if action == "menu":
                self.mode = "home"
                self.status_message_frames = 0
            elif action == "help":
                self.show_help_overlay = not self.show_help_overlay
            elif action == "replay":
                if self.engine.state.builder_playing:
                    self.engine.restart_builder_play()
                else:
                    self.engine.reset_level()
                self.result_recorded_level_id = None
            elif action == "edit":
                self.engine.restore_builder_editor()
            elif action == "save":
                self._open_save_dialog("new")
            elif action == "replace":
                self._open_save_dialog("replace")
            elif action == "load":
                self._open_builder_load_menu()
            return True
        return False

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        if self.show_save_dialog:
            self._handle_save_dialog_keydown(event)
            return

        if self.show_builder_load_menu:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_l:
                self.show_builder_load_menu = False
                return
            if event.key == pygame.K_LEFT:
                self.builder_load_page = max(0, self.builder_load_page - 1)
                return
            if event.key == pygame.K_RIGHT:
                self.builder_load_page = min(
                    self._builder_load_page_count() - 1,
                    self.builder_load_page + 1,
                )
                return
            if event.unicode.isdigit():
                visible_index = int(event.unicode) - 1
                if not 0 <= visible_index < 6:
                    return
                index = self._builder_load_visible_start() + visible_index
                if 0 <= index < len(self.builder_load_entries):
                    self._load_saved_builder_entry(index)
                return

        if event.key == pygame.K_ESCAPE:
            self.show_help_overlay = False
            self.show_builder_load_menu = False
            self.show_save_dialog = False
            if self.mode in {"level", "builder"}:
                self.mode = "home"
            else:
                self.running = False
            return

        if event.key == pygame.K_h and self.mode in {"level", "builder"}:
            self.show_help_overlay = not self.show_help_overlay
            return

        if self.mode == "home":
            if event.unicode.isdigit():
                index = int(event.unicode) - 1
                ordered_ids = sorted(self.engine.levels)
                if 0 <= index < len(ordered_ids):
                    self._start_level(ordered_ids[index])
            elif event.key == pygame.K_b:
                self._start_builder()
            return

        if self.mode == "level":
            if event.key == pygame.K_r:
                self.engine.reset_level()
            elif event.key == pygame.K_SPACE:
                self.engine.activate_ability()
            return

        if self.mode == "builder":
            if event.key == pygame.K_SPACE and self.engine.state.builder_playing:
                self.engine.activate_ability()
            elif event.key == pygame.K_p and not self.engine.state.builder_playing:
                self.engine.begin_builder_play()
            elif event.key == pygame.K_r and self.engine.state.builder_playing:
                self.engine.restart_builder_play()
            elif event.key == pygame.K_e and self.engine.state.builder_playing:
                self.engine.restore_builder_editor()
            elif event.key == pygame.K_s and not self.engine.state.builder_playing:
                self._open_save_dialog("new")
            elif event.key == pygame.K_l and not self.engine.state.builder_playing:
                self._open_builder_load_menu()

    def _handle_mouse_down(self, mouse_x: int, mouse_y: int) -> None:
        if self.show_save_dialog:
            self._handle_save_dialog_mouse_down(mouse_x, mouse_y)
            return

        if self.show_builder_load_menu:
            self._handle_builder_load_menu_mouse_down(mouse_x, mouse_y)
            return

        if self.mode == "home":
            for level_id, rect, _title, _subtitle in self.home_buttons:
                if rect.collidepoint(mouse_x, mouse_y):
                    if level_id == "builder":
                        self._start_builder()
                    else:
                        self._start_level(level_id)
                    return
            return

        if self._handle_hud_button_click(mouse_x, mouse_y):
            return

        if distance(mouse_x, mouse_y, *HOME_BUTTON_CENTER) <= 30:
            self.mode = "home"
            self.status_message_frames = 0
            return

        if self.mode == "level":
            self.engine.begin_drag(mouse_x, mouse_y)
            return

        if self.engine.state.builder_playing:
            self.engine.begin_drag(mouse_x, mouse_y)
        else:
            self._handle_builder_editor_mouse_down(mouse_x, mouse_y)

    def _handle_mouse_motion(self, mouse_x: int, mouse_y: int) -> None:
        if self.mode == "level":
            if self.engine.state.dragging:
                self.engine.update_drag(mouse_x, mouse_y)
            return

        if self.mode == "builder":
            self.engine.set_builder_mouse(mouse_x, mouse_y)
            if self.engine.state.builder_playing and self.engine.state.dragging:
                self.engine.update_drag(mouse_x, mouse_y)

    def _handle_mouse_up(self, mouse_x: int, mouse_y: int) -> None:
        if self.mode == "level":
            self.engine.release_bird()
            return

        if self.mode == "builder":
            if self.engine.state.builder_playing:
                self.engine.release_bird()
            elif self.engine.state.dragging_palette_item:
                self.engine.place_builder_item(
                    self.engine.state.dragging_palette_item, mouse_x, mouse_y
                )
                self.engine.finish_palette_drag()

    def _handle_builder_editor_mouse_down(self, mouse_x: int, mouse_y: int) -> None:
        self.engine.set_builder_mouse(mouse_x, mouse_y)
        reset_rect, clear_birds_rect, play_rect = self._builder_action_rects()

        if reset_rect.collidepoint(mouse_x, mouse_y):
            self.engine.clear_builder_world()
            return
        if clear_birds_rect.collidepoint(mouse_x, mouse_y):
            self.engine.clear_builder_birds()
            return
        if play_rect.collidepoint(mouse_x, mouse_y):
            self.engine.begin_builder_play()
            return
        if distance(mouse_x, mouse_y, *UNDO_BUTTON_CENTER) <= 30:
            self.engine.pop_builder_menu()
            return

        menu = self.engine.state.builder_menu
        palette_rects = self._palette_rects()

        if menu == "main":
            if palette_rects[0].collidepoint(mouse_x, mouse_y):
                self.engine.push_builder_menu("birds")
            elif palette_rects[1].collidepoint(mouse_x, mouse_y):
                self.engine.push_builder_menu("pigs")
            elif palette_rects[2].collidepoint(mouse_x, mouse_y):
                self.engine.push_builder_menu("blocks")
            return

        if menu == "blocks":
            if palette_rects[0].collidepoint(mouse_x, mouse_y):
                self.engine.push_builder_menu("boxes")
            elif palette_rects[1].collidepoint(mouse_x, mouse_y):
                self.engine.push_builder_menu("wheels")
            elif palette_rects[2].collidepoint(mouse_x, mouse_y):
                self.engine.push_builder_menu("columns")
            return

        if menu == "birds":
            if distance(mouse_x, mouse_y, *BIRD_RESET_CENTER) <= 15:
                self.engine.clear_builder_birds()
                self._set_status_message("Cleared bird queue")
                return
            if palette_rects[0].collidepoint(mouse_x, mouse_y):
                self.engine.add_builder_bird("red")
            elif palette_rects[1].collidepoint(mouse_x, mouse_y):
                self.engine.add_builder_bird("yellow")
            elif palette_rects[2].collidepoint(mouse_x, mouse_y):
                self.engine.add_builder_bird("blue")
            elif palette_rects[3].collidepoint(mouse_x, mouse_y):
                self.engine.add_builder_bird("eagle")
            return

        if menu == "pigs" and palette_rects[0].collidepoint(mouse_x, mouse_y):
            self.engine.begin_palette_drag("pig1")
            return

        if menu == "boxes":
            if palette_rects[0].collidepoint(mouse_x, mouse_y):
                self.engine.begin_palette_drag("wood_box")
            elif palette_rects[1].collidepoint(mouse_x, mouse_y):
                self.engine.begin_palette_drag("stone_box")
            return

        if menu == "wheels":
            if palette_rects[0].collidepoint(mouse_x, mouse_y):
                self.engine.begin_palette_drag("wood_wheel")
            elif palette_rects[1].collidepoint(mouse_x, mouse_y):
                self.engine.begin_palette_drag("stone_wheel")
            return

        if menu == "columns":
            if palette_rects[0].collidepoint(mouse_x, mouse_y):
                self.engine.begin_palette_drag("wood_column")
            elif palette_rects[1].collidepoint(mouse_x, mouse_y):
                self.engine.begin_palette_drag("stone_column")

    def _draw(self) -> None:
        if "background" in self.assets:
            self.screen.blit(self.assets["background"], (0, 0))
        else:
            self.screen.fill(SKY_BLUE)

        if self.mode == "home":
            self._draw_home()
        else:
            self._draw_game()

    def _draw_home(self) -> None:
        self._draw_home_shell()

        if "title" in self.assets:
            title_rect = self.assets["title"].get_rect(center=(330, 210))
            self.screen.blit(self.assets["title"], title_rect)
        else:
            self._blit_text("Angry Birds", self.large_font, WHITE, (330, 210))

        self._blit_text(
            "Physics Sandbox Edition",
            self.hero_font,
            ACCENT_GOLD,
            (300, 350),
        )
        intro_lines = [
            "Arcade physics puzzle game with five handcrafted levels,",
            "four bird types, and a built-in sandbox level builder.",
            "Designed to feel polished, replayable, and easy to extend.",
        ]
        for index, line in enumerate(intro_lines):
            self._blit_text_left(
                line,
                self.small_font,
                PANEL_SOFT,
                (110, 405 + index * 32),
            )

        home_lines = [
            "Birds: Red standard, Yellow burst, Blue split, Eagle slam.",
            "Builder mode: create layouts and instantly playtest them.",
            "Hotkeys: 1-5 launch levels, B opens builder mode, H opens help.",
        ]
        for index, line in enumerate(home_lines):
            self._blit_text_left(
                line,
                self.tiny_font,
                PANEL_SOFT,
                (110, 520 + index * 34),
            )

        mouse_pos = pygame.mouse.get_pos()
        for level_id, rect, title, subtitle in self.home_buttons:
            hovered = rect.collidepoint(mouse_pos)
            fill = BUTTON_HIGHLIGHT if hovered else BUTTON_FILL
            shadow_rect = rect.move(0, 8)
            pygame.draw.rect(self.screen, (17, 27, 48), shadow_rect, border_radius=22)
            pygame.draw.rect(self.screen, fill, rect, border_radius=22)
            pygame.draw.rect(self.screen, WHITE, rect, width=3, border_radius=22)
            y_offset = -18 if level_id != "builder" else -10
            self._blit_text(title, self.medium_font, BUTTON_TEXT, (rect.centerx, rect.centery + y_offset))
            self._blit_text(subtitle, self.micro_font, PANEL_SOFT, (rect.centerx, rect.centery + 18))
            if level_id != "builder":
                best_score = get_high_score(level_id)
                best_label = f"Best: {best_score}" if best_score else "Best: --"
                self._blit_text(best_label, self.micro_font, ACCENT_GOLD, (rect.centerx, rect.centery + 44))

    def _draw_home_shell(self) -> None:
        hero_rect = pygame.Rect(60, 110, 660, 560)
        button_panel = pygame.Rect(760, 70, 520, 820)
        for rect in (hero_rect, button_panel):
            panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            panel.fill((24, 34, 57, 160))
            self.screen.blit(panel, rect.topleft)
            pygame.draw.rect(self.screen, WHITE, rect, width=2, border_radius=26)

        badge_rect = pygame.Rect(90, 130, 195, 44)
        pygame.draw.rect(self.screen, ACCENT_GOLD, badge_rect, border_radius=20)
        self._blit_text("UPGRADED BUILD", self.small_font, PANEL_DARK, badge_rect.center)

    def _draw_game(self) -> None:
        state = self.engine.state
        pygame.draw.line(self.screen, FLOOR_GREEN, (0, FLOOR_Y), (WINDOW_WIDTH, FLOOR_Y), 4)
        self._draw_grid()

        if "home_button" in self.assets:
            rect = self.assets["home_button"].get_rect(center=HOME_BUTTON_CENTER)
            self.screen.blit(self.assets["home_button"], rect)

        self._draw_game_hud(state)

        if "sling" in self.assets:
            sling_rect = self.assets["sling"].get_rect(center=(200, 600))
            self.screen.blit(self.assets["sling"], sling_rect)

        if state.dragging and state.birds_waiting:
            bird = state.birds_waiting[0]
            pygame.draw.line(
                self.screen,
                (90, 49, 24),
                (INIT_BIRD_X, INIT_BIRD_Y),
                (bird.x, bird.y),
                10,
            )
            for point in state.trajectory[:-1]:
                pygame.draw.circle(
                    self.screen,
                    TRAJECTORY_BLUE,
                    (int(point[0]), int(point[1])),
                    4,
                )

        for bird in state.birds_in_flight:
            self._draw_sprite(bird.sprite_key, bird.x, bird.y)
        for bird in state.birds_waiting:
            self._draw_sprite(bird.sprite_key, bird.x, bird.y)
        for pig in state.pigs:
            self._draw_sprite(pig.sprite_key, pig.x, pig.y)
        for obj in state.objects:
            self._draw_sprite(obj.sprite_key, obj.x, obj.y, obj.angle)

        if self.mode == "builder" and not state.builder_playing:
            self._draw_builder_editor()

        self._draw_overlay()
        if self.show_help_overlay:
            self._draw_help_overlay(state)
        if self.show_builder_load_menu:
            self._draw_builder_load_menu()
        if self.show_save_dialog:
            self._draw_save_dialog()
        self._draw_status_message()

    def _draw_game_hud(self, state: GameState) -> None:
        score_rect = pygame.Rect(WINDOW_WIDTH - 385, 18, 345, 96)
        control_rect = pygame.Rect(WINDOW_WIDTH - 520, 124, 480, 86)
        queue_rect = pygame.Rect(108, 22, 360, 118)
        for rect in (score_rect, control_rect, queue_rect):
            panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            panel.fill((246, 248, 255, 210))
            self.screen.blit(panel, rect.topleft)
            pygame.draw.rect(self.screen, PANEL_OUTLINE, rect, width=2, border_radius=20)

        self._blit_text(
            state.level_name,
            self.medium_font,
            PANEL_DARK,
            (score_rect.centerx, score_rect.y + 28),
        )
        self._blit_text(
            f"Score: {max(0, state.score)}",
            self.small_font,
            TEXT_MUTED,
            (score_rect.centerx - 56, score_rect.y + 68),
        )
        if state.level_id and state.level_id != "builder":
            best = get_high_score(state.level_id)
            self._blit_text(
                f"Best: {best}",
                self.micro_font,
                TEXT_MUTED,
                (score_rect.centerx + 90, score_rect.y + 70),
            )
        self._draw_hud_buttons(control_rect)

        next_bird = state.birds_waiting[0] if state.birds_waiting else None
        next_label = (
            f"Next Bird: {next_bird.display_name}"
            if next_bird is not None
            else "Next Bird: none"
        )
        self._blit_text(
            next_label,
            self.small_font,
            PANEL_DARK,
            (queue_rect.centerx, queue_rect.y + 24),
        )

        preview_x = queue_rect.x + 48
        for index, bird in enumerate(state.birds_waiting[:4]):
            sprite, size = self._bird_preview_style(bird.bird_type)
            self._draw_scaled_sprite(
                sprite,
                (preview_x + index * 72, queue_rect.y + 82),
                size,
            )

    def _hud_button_specs(self) -> list[tuple[str, str, pygame.Rect, tuple[int, int, int]]]:
        if self.mode == "level":
            actions = [
                ("replay", "Replay", BUTTON_FILL),
                ("help", "Help", BUTTON_FILL),
                ("menu", "Menu", WARNING_RED),
            ]
        elif self.engine.state.builder_playing:
            actions = [
                ("replay", "Replay", BUTTON_FILL),
                ("edit", "Edit", SUCCESS_GREEN),
                ("help", "Help", BUTTON_FILL),
                ("menu", "Menu", WARNING_RED),
            ]
        else:
            actions = [
                ("save", "Save", SUCCESS_GREEN),
                ("replace", "Replace", BUTTON_FILL),
                ("load", "Load", BUTTON_FILL),
                ("help", "Help", BUTTON_FILL),
                ("menu", "Menu", WARNING_RED),
            ]

        button_count = len(actions)
        button_width = 82 if button_count == 5 else 102
        gap = 8
        total_width = button_count * button_width + (button_count - 1) * gap
        start_x = WINDOW_WIDTH - 280 - total_width // 2
        rects: list[tuple[str, str, pygame.Rect, tuple[int, int, int]]] = []
        for index, (action, label, color) in enumerate(actions):
            rect = pygame.Rect(start_x + index * (button_width + gap), 148, button_width, 38)
            rects.append((action, label, rect, color))
        return rects

    def _draw_hud_buttons(self, control_rect: pygame.Rect) -> None:
        title = "Controls"
        if self.mode == "builder" and not self.engine.state.builder_playing:
            title = "Builder Tools"
        self._blit_text(title, self.micro_font, TEXT_MUTED, (control_rect.centerx, control_rect.y + 16))
        for action, label, rect, color in self._hud_button_specs():
            disabled = action == "replace" and self.engine.current_builder_save_path is None
            fill = TEXT_MUTED if disabled else color
            pygame.draw.rect(self.screen, fill, rect, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, rect, width=2, border_radius=10)
            self._blit_text(label, self.micro_font, WHITE, rect.center)


    def _draw_overlay(self) -> None:
        state = self.engine.state
        if not state.won and not state.lost:
            return

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 10, 10, 120))
        self.screen.blit(overlay, (0, 0))

        if state.won:
            self._blit_text("You Win!", self.large_font, WHITE, (WINDOW_WIDTH // 2, 170))
            star_surface = self._star_surface()
            if star_surface is not None:
                star_rect = star_surface.get_rect(center=(WINDOW_WIDTH // 2, 290))
                self.screen.blit(star_surface, star_rect)
        else:
            self._blit_text("Game Over", self.large_font, WHITE, (WINDOW_WIDTH // 2, 220))

        footer = (
            "Press R to replay or Esc to return to the menu."
            if self.mode == "level"
            else "Press R to replay, E to edit, or Esc to return to the menu."
        )
        self._blit_text(footer, self.medium_font, WHITE, (WINDOW_WIDTH // 2, 370))

    def _draw_help_overlay(self, state: GameState) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 12, 22, 145))
        self.screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(130, 110, 580, 340)
        panel = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel.fill((245, 248, 255, 235))
        self.screen.blit(panel, panel_rect.topleft)
        pygame.draw.rect(self.screen, PANEL_OUTLINE, panel_rect, width=2, border_radius=24)

        self._blit_text_left("Help", self.medium_font, PANEL_DARK, (panel_rect.x + 32, panel_rect.y + 34))
        help_lines = [
            "Drag the bird back and release to launch.",
            "Red bird: standard impact shot with no special ability.",
            "Yellow bird: press Space during flight for a speed burst.",
            "Blue Bird: press Space to split into three lighter birds.",
            "Mighty Eagle: press Space to slam straight down.",
            "R replays the current level or playtest.",
            "Builder mode: Save names a JSON slot; Replace overwrites the loaded slot.",
            "Use Load to open the saved-level menu.",
            "Esc returns to the menu. H closes this help panel.",
        ]
        for index, line in enumerate(help_lines):
            self._blit_text_left(
                line,
                self.tiny_font if index < 5 else self.micro_font,
                TEXT_MUTED,
                (panel_rect.x + 32, panel_rect.y + 92 + index * 28),
            )

    def _star_surface(self) -> Optional[pygame.Surface]:
        score = self.engine.state.score
        one, two, three = self.engine.state.stars
        key: Optional[str] = None
        if score >= three:
            key = "three_star"
        elif score >= two:
            key = "two_star"
        elif score >= one:
            key = "one_star"
        if key is None:
            return None
        return self.assets.get(key)

    def _draw_grid(self) -> None:
        grid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
            pygame.draw.line(grid_surface, GRID_LINE, (0, y), (WINDOW_WIDTH, y), 1)
        for x in range(0, WINDOW_WIDTH, TILE_SIZE):
            pygame.draw.line(grid_surface, GRID_LINE, (x, 0), (x, WINDOW_HEIGHT), 1)
        self.screen.blit(grid_surface, (0, 0))

    def _builder_action_panel_rect(self) -> pygame.Rect:
        return pygame.Rect(24, FLOOR_Y + 44, 650, 116)

    def _bird_preview_style(
        self, bird_type: str, *, large: bool = False
    ) -> tuple[str, tuple[int, int]]:
        if bird_type == "red":
            return "bird_red", ((125, 125) if large else (60, 60))
        if bird_type == "blue":
            return "bird_blue", ((86, 86) if large else (48, 48))
        if bird_type == "eagle":
            return "bird_eagle", ((100, 66) if large else (58, 38))
        return "bird_yellow", ((100, 80) if large else (58, 44))

    def _bird_display_name(self, bird_type: str) -> str:
        if bird_type == "blue":
            return "Blue Bird"
        if bird_type == "eagle":
            return "Mighty Eagle"
        return bird_type.title()

    def _palette_rects(self) -> list[pygame.Rect]:
        rects: list[pygame.Rect] = []
        for center in PALETTE_CENTERS:
            rect = pygame.Rect(0, 0, PALETTE_BOX_SIZE, PALETTE_BOX_SIZE)
            rect.center = center
            rects.append(rect)
        return rects

    def _builder_action_rects(self) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        panel_rect = self._builder_action_panel_rect()
        reset_rect = pygame.Rect(0, 0, 170, 44)
        clear_birds_rect = pygame.Rect(0, 0, 170, 44)
        play_rect = pygame.Rect(0, 0, 170, 44)
        button_y = panel_rect.bottom - 32
        reset_rect.center = (panel_rect.centerx - 190, button_y)
        clear_birds_rect.center = (panel_rect.centerx, button_y)
        play_rect.center = (panel_rect.centerx + 190, button_y)
        return reset_rect, clear_birds_rect, play_rect

    def _draw_builder_editor(self) -> None:
        state = self.engine.state
        palette_rects = self._palette_rects()
        for rect in palette_rects:
            pygame.draw.rect(self.screen, PANEL_FILL, rect, border_radius=12)
            pygame.draw.rect(self.screen, PANEL_OUTLINE, rect, width=3, border_radius=12)

        action_panel = self._builder_action_panel_rect()
        panel_surface = pygame.Surface((action_panel.width, action_panel.height), pygame.SRCALPHA)
        panel_surface.fill((241, 245, 255, 205))
        self.screen.blit(panel_surface, action_panel.topleft)
        pygame.draw.rect(self.screen, PANEL_OUTLINE, action_panel, width=2, border_radius=24)

        reset_rect, clear_birds_rect, play_rect = self._builder_action_rects()
        pygame.draw.rect(self.screen, WARNING_RED, reset_rect, border_radius=18)
        pygame.draw.rect(self.screen, BUTTON_FILL, clear_birds_rect, border_radius=18)
        pygame.draw.rect(self.screen, SUCCESS_GREEN, play_rect, border_radius=18)
        pygame.draw.rect(self.screen, WHITE, reset_rect, width=2, border_radius=18)
        pygame.draw.rect(self.screen, WHITE, clear_birds_rect, width=2, border_radius=18)
        pygame.draw.rect(self.screen, WHITE, play_rect, width=2, border_radius=18)
        self._blit_text("Clear Blocks", self.small_font, WHITE, reset_rect.center)
        self._blit_text("Clear Birds", self.small_font, WHITE, clear_birds_rect.center)
        self._blit_text("Play Test", self.small_font, WHITE, play_rect.center)

        if "back_button" in self.assets:
            rect = self.assets["back_button"].get_rect(center=UNDO_BUTTON_CENTER)
            self.screen.blit(self.assets["back_button"], rect)

        self._blit_text(
            "Builder Sandbox",
            self.small_font,
            PANEL_DARK,
            (action_panel.x + 124, action_panel.y + 24),
        )
        self._blit_text_left(
            "Build above the grass. Save/Load is top right.",
            self.micro_font,
            TEXT_MUTED,
            (action_panel.x + 250, action_panel.y + 18),
        )
        self._blit_text_left(
            "Clear Blocks keeps birds. Clear Birds keeps builds.",
            self.micro_font,
            TEXT_MUTED,
            (action_panel.x + 250, action_panel.y + 44),
        )

        self._draw_builder_palette_contents(state.builder_menu)
        self._draw_builder_drag_preview()

    def _draw_builder_palette_contents(self, menu: str) -> None:
        rects = self._palette_rects()
        if menu == "main":
            self._draw_scaled_sprite("bird_red", rects[0].center, (125, 125))
            self._draw_scaled_sprite("pig_failed", rects[1].center, (125, 125))
            self._draw_scaled_sprite("box_wood", rects[2].center, (100, 100))
            self._blit_text("Birds", self.small_font, PANEL_DARK, (rects[0].centerx, rects[0].bottom + 18))
            self._blit_text("Pigs", self.small_font, PANEL_DARK, (rects[1].centerx, rects[1].bottom + 18))
            self._blit_text("Blocks", self.small_font, PANEL_DARK, (rects[2].centerx, rects[2].bottom + 18))
            return

        if menu == "birds":
            red_sprite, red_size = self._bird_preview_style("red", large=True)
            yellow_sprite, yellow_size = self._bird_preview_style("yellow", large=True)
            blue_sprite, blue_size = self._bird_preview_style("blue", large=True)
            eagle_sprite, eagle_size = self._bird_preview_style("eagle", large=True)
            self._draw_scaled_sprite(red_sprite, rects[0].center, red_size)
            self._draw_scaled_sprite(yellow_sprite, rects[1].center, yellow_size)
            self._draw_scaled_sprite(blue_sprite, rects[2].center, blue_size)
            self._draw_scaled_sprite(eagle_sprite, rects[3].center, eagle_size)
            self._blit_text("Red / Standard", self.small_font, PANEL_DARK, (rects[0].centerx, rects[0].bottom + 18))
            self._blit_text("Yellow / Speed", self.small_font, PANEL_DARK, (rects[1].centerx, rects[1].bottom + 18))
            self._blit_text("Blue / Split", self.small_font, PANEL_DARK, (rects[2].centerx, rects[2].bottom + 18))
            self._blit_text("Eagle / Slam", self.small_font, PANEL_DARK, (rects[3].centerx, rects[3].bottom + 18))
            birds = self.engine.state.birds_waiting
            red_count = sum(1 for bird in birds if bird.bird_type == "red")
            yellow_count = sum(1 for bird in birds if bird.bird_type == "yellow")
            blue_count = sum(1 for bird in birds if bird.bird_type == "blue")
            eagle_count = sum(1 for bird in birds if bird.bird_type == "eagle")
            count_box = pygame.Rect(24, 598, 438, 136)
            count_panel = pygame.Surface((count_box.width, count_box.height), pygame.SRCALPHA)
            count_panel.fill((241, 245, 255, 225))
            self.screen.blit(count_panel, count_box.topleft)
            pygame.draw.rect(self.screen, PANEL_OUTLINE, count_box, width=2, border_radius=16)
            pygame.draw.circle(self.screen, WARNING_RED, BIRD_RESET_CENTER, 15)
            self._blit_text_left(
                "Clear Queue",
                self.small_font,
                PANEL_DARK,
                (count_box.x + 18, count_box.y + 14),
            )
            self._blit_text_left(
                "Tap the red button to clear queued birds.",
                self.tiny_font,
                TEXT_MUTED,
                (count_box.x + 18, count_box.y + 44),
            )
            self._blit_text_left(
                f"Red birds: {red_count}",
                self.small_font,
                PANEL_DARK,
                (count_box.x + 18, count_box.y + 82),
            )
            self._blit_text_left(
                f"Yellow birds: {yellow_count}",
                self.small_font,
                PANEL_DARK,
                (count_box.x + 18, count_box.y + 108),
            )
            self._blit_text_left(
                f"Blue birds: {blue_count}",
                self.small_font,
                PANEL_DARK,
                (count_box.x + 224, count_box.y + 82),
            )
            self._blit_text_left(
                f"Eagles: {eagle_count}",
                self.small_font,
                PANEL_DARK,
                (count_box.x + 224, count_box.y + 108),
            )
            return

        if menu == "pigs":
            self._draw_scaled_sprite("pig", rects[0].center, (100, 100))
            self._blit_text("Pig", self.small_font, PANEL_DARK, (rects[0].centerx, rects[0].bottom + 18))
            return

        if menu == "blocks":
            self._draw_scaled_sprite("box_wood", rects[0].center, (100, 100))
            self._draw_scaled_sprite("wheel_wood", rects[1].center, (100, 100))
            self._draw_scaled_sprite("column_wood", rects[2].center, (18, 100))
            self._blit_text("Boxes", self.small_font, PANEL_DARK, (rects[0].centerx, rects[0].bottom + 18))
            self._blit_text("Wheels", self.small_font, PANEL_DARK, (rects[1].centerx, rects[1].bottom + 18))
            self._blit_text("Columns", self.small_font, PANEL_DARK, (rects[2].centerx, rects[2].bottom + 18))
            return

        if menu == "boxes":
            self._draw_scaled_sprite("box_wood", rects[0].center, (100, 100))
            self._draw_scaled_sprite("box_stone", rects[1].center, (100, 100))
            self._blit_text("Wood Box", self.small_font, PANEL_DARK, (rects[0].centerx, rects[0].bottom + 18))
            self._blit_text("Stone Box", self.small_font, PANEL_DARK, (rects[1].centerx, rects[1].bottom + 18))
            return

        if menu == "wheels":
            self._draw_scaled_sprite("wheel_wood", rects[0].center, (100, 100))
            self._draw_scaled_sprite("wheel_stone", rects[1].center, (100, 100))
            self._blit_text("Wood Wheel", self.small_font, PANEL_DARK, (rects[0].centerx, rects[0].bottom + 18))
            self._blit_text("Stone Wheel", self.small_font, PANEL_DARK, (rects[1].centerx, rects[1].bottom + 18))
            return

        if menu == "columns":
            self._draw_scaled_sprite("column_wood", rects[0].center, (18, 100))
            self._draw_scaled_sprite("column_stone", rects[1].center, (18, 100))
            self._blit_text("Wood Column", self.small_font, PANEL_DARK, (rects[0].centerx, rects[0].bottom + 18))
            self._blit_text("Stone Column", self.small_font, PANEL_DARK, (rects[1].centerx, rects[1].bottom + 18))

    def _draw_builder_drag_preview(self) -> None:
        item = self.engine.state.dragging_palette_item
        if item is None:
            return

        sprite_map = {
            "pig1": ("pig", (100, 100)),
            "wood_box": ("box_wood", (100, 100)),
            "stone_box": ("box_stone", (100, 100)),
            "wood_wheel": ("wheel_wood", (100, 100)),
            "stone_wheel": ("wheel_stone", (100, 100)),
            "wood_column": ("column_wood", (18, 100)),
            "stone_column": ("column_stone", (18, 100)),
        }
        sprite_key, size = sprite_map[item]
        self._draw_scaled_sprite(
            sprite_key,
            self.engine.state.builder_mouse,
            size,
            alpha=170,
        )

    def _refresh_builder_load_entries(self) -> None:
        self.builder_load_entries = list_saved_builder_levels()

    def _builder_load_visible_start(self) -> int:
        return self.builder_load_page * 6

    def _builder_load_page_count(self) -> int:
        return max(1, (len(self.builder_load_entries) + 5) // 6)

    def _clamp_builder_load_page(self) -> None:
        self.builder_load_page = min(
            self.builder_load_page,
            self._builder_load_page_count() - 1,
        )
        self.builder_load_page = max(0, self.builder_load_page)

    def _builder_load_menu_rects(
        self,
    ) -> tuple[pygame.Rect, list[pygame.Rect], list[pygame.Rect], pygame.Rect, pygame.Rect]:
        panel_rect = pygame.Rect(0, 0, 760, 570)
        panel_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        row_rects: list[pygame.Rect] = []
        delete_rects: list[pygame.Rect] = []
        visible_count = min(
            6,
            len(self.builder_load_entries) - self._builder_load_visible_start(),
        )
        for index in range(max(0, visible_count)):
            row_rect = pygame.Rect(panel_rect.x + 42, panel_rect.y + 120 + index * 58, 576, 46)
            delete_rect = pygame.Rect(panel_rect.x + 632, row_rect.y, 86, 46)
            row_rects.append(row_rect)
            delete_rects.append(delete_rect)
        prev_rect = pygame.Rect(panel_rect.x + 238, panel_rect.bottom - 64, 118, 42)
        next_rect = pygame.Rect(panel_rect.x + 404, panel_rect.bottom - 64, 118, 42)
        return panel_rect, row_rects, delete_rects, prev_rect, next_rect

    def _handle_builder_load_menu_mouse_down(self, mouse_x: int, mouse_y: int) -> None:
        panel_rect, row_rects, delete_rects, prev_rect, next_rect = self._builder_load_menu_rects()
        if not panel_rect.collidepoint(mouse_x, mouse_y):
            self.show_builder_load_menu = False
            return
        if prev_rect.collidepoint(mouse_x, mouse_y):
            self.builder_load_page = max(0, self.builder_load_page - 1)
            return
        if next_rect.collidepoint(mouse_x, mouse_y):
            self.builder_load_page = min(
                self._builder_load_page_count() - 1,
                self.builder_load_page + 1,
            )
            return
        visible_start = self._builder_load_visible_start()
        for row_index, delete_rect in enumerate(delete_rects):
            if delete_rect.collidepoint(mouse_x, mouse_y):
                self._delete_saved_builder_entry(visible_start + row_index)
                return
        for index, row_rect in enumerate(row_rects):
            if row_rect.collidepoint(mouse_x, mouse_y):
                self._load_saved_builder_entry(visible_start + index)
                return

    def _save_dialog_rects(self) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect]:
        panel_rect = pygame.Rect(0, 0, 560, 300)
        panel_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        input_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 112, 460, 48)
        primary_rect = pygame.Rect(panel_rect.x + 64, panel_rect.y + 208, 150, 48)
        replace_rect = pygame.Rect(panel_rect.x + 230, panel_rect.y + 208, 150, 48)
        cancel_rect = pygame.Rect(panel_rect.x + 396, panel_rect.y + 208, 110, 48)
        return panel_rect, input_rect, primary_rect, replace_rect, cancel_rect

    def _handle_save_dialog_mouse_down(self, mouse_x: int, mouse_y: int) -> None:
        panel_rect, _input_rect, primary_rect, replace_rect, cancel_rect = self._save_dialog_rects()
        if cancel_rect.collidepoint(mouse_x, mouse_y) or not panel_rect.collidepoint(mouse_x, mouse_y):
            self.show_save_dialog = False
            return
        if primary_rect.collidepoint(mouse_x, mouse_y):
            self.save_dialog_mode = "new"
            self._commit_save_dialog()
            return
        if replace_rect.collidepoint(mouse_x, mouse_y):
            if self.engine.current_builder_save_path is None:
                self._set_status_message("Load a saved level before replacing it.")
                return
            self.save_dialog_mode = "replace"
            self._commit_save_dialog()

    def _load_saved_builder_entry(self, index: int) -> None:
        save_path, _level = self.builder_load_entries[index]
        loaded_level = self.engine.load_builder_level(save_path)
        self.show_builder_load_menu = False
        self._set_status_message(f"Loaded {loaded_level.name}")

    def _delete_saved_builder_entry(self, index: int) -> None:
        save_path, level = self.builder_load_entries[index]
        delete_saved_builder_level(save_path)
        self.engine.current_builder_save_path = None
        self._refresh_builder_load_entries()
        self._clamp_builder_load_page()
        if not self.builder_load_entries:
            self.show_builder_load_menu = False
        self._set_status_message(f"Deleted {level.name}; saved levels renumbered")

    def _draw_builder_load_menu(self) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 12, 22, 130))
        self.screen.blit(overlay, (0, 0))

        panel_rect, row_rects, delete_rects, prev_rect, next_rect = self._builder_load_menu_rects()
        panel = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel.fill((245, 248, 255, 242))
        self.screen.blit(panel, panel_rect.topleft)
        pygame.draw.rect(self.screen, PANEL_OUTLINE, panel_rect, width=3, border_radius=26)

        self._blit_text("Saved Builder Levels", self.medium_font, PANEL_DARK, (panel_rect.centerx, panel_rect.y + 44))
        self._blit_text(
            "Click a level to load it. Delete removes a slot and renumbers the rest.",
            self.micro_font,
            TEXT_MUTED,
            (panel_rect.centerx, panel_rect.y + 82),
        )

        visible_start = self._builder_load_visible_start()
        for row_index, row_rect in enumerate(row_rects):
            save_path, level = self.builder_load_entries[visible_start + row_index]
            delete_rect = delete_rects[row_index]
            pygame.draw.rect(self.screen, BUTTON_FILL, row_rect, border_radius=14)
            pygame.draw.rect(self.screen, WARNING_RED, delete_rect, border_radius=14)
            pygame.draw.rect(self.screen, WHITE, row_rect, width=2, border_radius=14)
            pygame.draw.rect(self.screen, WHITE, delete_rect, width=2, border_radius=14)
            display_name = level.name
            if len(display_name) > 26:
                display_name = f"{display_name[:23]}..."
            label = f"{visible_start + row_index + 1}. {display_name}"
            details = f"{len(level.birds)} birds, {len(level.pigs)} pigs, {len(level.objects)} objects"
            self._blit_text_left(label, self.tiny_font, WHITE, (row_rect.x + 18, row_rect.y + 8))
            self._blit_text_left(details, self.micro_font, PANEL_SOFT, (row_rect.x + 360, row_rect.y + 12))
            self._blit_text("Delete", self.micro_font, WHITE, delete_rect.center)

        page_count = self._builder_load_page_count()
        prev_color = TEXT_MUTED if self.builder_load_page == 0 else BUTTON_FILL
        next_color = TEXT_MUTED if self.builder_load_page >= page_count - 1 else BUTTON_FILL
        pygame.draw.rect(self.screen, prev_color, prev_rect, border_radius=12)
        pygame.draw.rect(self.screen, next_color, next_rect, border_radius=12)
        pygame.draw.rect(self.screen, WHITE, prev_rect, width=2, border_radius=12)
        pygame.draw.rect(self.screen, WHITE, next_rect, width=2, border_radius=12)
        self._blit_text("Previous", self.micro_font, WHITE, prev_rect.center)
        self._blit_text("Next", self.micro_font, WHITE, next_rect.center)
        self._blit_text(
            f"Page {self.builder_load_page + 1} of {page_count}",
            self.micro_font,
            TEXT_MUTED,
            (panel_rect.centerx, panel_rect.bottom - 82),
        )

    def _draw_save_dialog(self) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 12, 22, 125))
        self.screen.blit(overlay, (0, 0))

        panel_rect, input_rect, primary_rect, replace_rect, cancel_rect = self._save_dialog_rects()
        panel = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel.fill((245, 248, 255, 244))
        self.screen.blit(panel, panel_rect.topleft)
        pygame.draw.rect(self.screen, PANEL_OUTLINE, panel_rect, width=3, border_radius=24)

        title = "Save Builder Level"
        self._blit_text(title, self.medium_font, PANEL_DARK, (panel_rect.centerx, panel_rect.y + 44))
        self._blit_text(
            "Name this layout, then save a new slot or replace the loaded one.",
            self.micro_font,
            TEXT_MUTED,
            (panel_rect.centerx, panel_rect.y + 82),
        )

        pygame.draw.rect(self.screen, WHITE, input_rect, border_radius=12)
        pygame.draw.rect(self.screen, PANEL_OUTLINE, input_rect, width=2, border_radius=12)
        input_text = self.save_dialog_text or "Untitled Builder Level"
        self._blit_text_left(input_text, self.small_font, PANEL_DARK, (input_rect.x + 16, input_rect.y + 12))

        replace_disabled = self.engine.current_builder_save_path is None
        buttons = [
            (primary_rect, "Save New", SUCCESS_GREEN),
            (replace_rect, "Replace", TEXT_MUTED if replace_disabled else BUTTON_FILL),
            (cancel_rect, "Cancel", WARNING_RED),
        ]
        for rect, label, color in buttons:
            pygame.draw.rect(self.screen, color, rect, border_radius=14)
            pygame.draw.rect(self.screen, WHITE, rect, width=2, border_radius=14)
            self._blit_text(label, self.micro_font, WHITE, rect.center)

    def _draw_sprite(self, sprite_key: str, x: float, y: float, angle: float = 0) -> None:
        surface = self.assets.get(sprite_key)
        if surface is None:
            pygame.draw.circle(self.screen, DARK_TEXT, (int(x), int(y)), 20)
            return

        render_surface = surface
        if angle != 0:
            render_surface = pygame.transform.rotate(surface, -angle)
        rect = render_surface.get_rect(center=(int(x), int(y)))
        self.screen.blit(render_surface, rect)

    def _draw_scaled_sprite(
        self,
        sprite_key: str,
        center: tuple[float, float],
        size: tuple[int, int],
        *,
        alpha: Optional[int] = None,
    ) -> None:
        surface = self.assets.get(sprite_key)
        if surface is None:
            return
        render_surface = pygame.transform.smoothscale(surface, size)
        if alpha is not None:
            render_surface = render_surface.copy()
            render_surface.set_alpha(alpha)
        rect = render_surface.get_rect(center=(int(center[0]), int(center[1])))
        self.screen.blit(render_surface, rect)

    def _set_status_message(self, message: str, *, frames: int = 180) -> None:
        self.status_message = message
        self.status_message_frames = frames

    def _draw_status_message(self) -> None:
        if self.status_message_frames <= 0 or not self.status_message:
            return

        panel_rect = pygame.Rect(0, 0, 540, 44)
        panel_rect.midtop = (WINDOW_WIDTH // 2, 22)
        panel = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel.fill((39, 52, 80, 215))
        self.screen.blit(panel, panel_rect.topleft)
        pygame.draw.rect(self.screen, WHITE, panel_rect, width=2, border_radius=18)
        self._blit_text(
            self.status_message,
            self.micro_font,
            WHITE,
            panel_rect.center,
        )

    def _blit_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        center: tuple[int, int],
    ) -> None:
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=center)
        self.screen.blit(surface, rect)

    def _blit_text_left(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        topleft: tuple[int, int],
    ) -> None:
        surface = font.render(text, True, color)
        rect = surface.get_rect(topleft=topleft)
        self.screen.blit(surface, rect)


def run() -> None:
    client = PygameClient()
    client.run()


if __name__ == "__main__":
    run()
