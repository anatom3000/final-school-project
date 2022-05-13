from constants import MENU_FONT


def make_menu(screen):
    screen.blit(MENU_FONT.render("some text i guess", True, (255,) * 3), (0, 0))
