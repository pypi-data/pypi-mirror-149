from .figures import *
import pygame
import pygame.freetype
from string import ascii_lowercase


class Main():
    alphabet = ascii_lowercase + "0123456789;,_()' +-"

    class_names = [
        'Поле',
        'Точка',
        'Линия',
        'Прямоугольник',
        'Квадрат',
        'Треугольник',
        'Ромб',
        'Круг',
    ]
    classes = [
        f.canvas,
        f.dot,
        f.line,
        f.rectangle,
        f.square,
        f.triangle,
        f.rhomb,
        f.circle,
    ]
    functions = [
        dir(f.Canvas),
        dir(f.Dot),
        dir(f.Line),
        dir(f.Rectangle),
        dir(f.Square),
        dir(f.Triangle),
        dir(f.Rhomb),
        dir(f.Circle),
    ]
    current_menu = 0

    def __init__(self):
        pygame.init()
        pygame.font.init()

        screen = pygame.display.set_mode((1020, 670))
        pygame.display.set_caption('Графический редактор')
        clock = pygame.time.Clock()

        font = pygame.freetype.Font('Anonymous_Pro.ttf', 36)
        font1 = pygame.font.SysFont('Anonymous_Pro.ttf', 24)
        font2 = pygame.freetype.Font('Anonymous_Pro.ttf', 20)

        function_get = input_function(460, 10, 550, font1, 60, self)
        fg = pygame.sprite.Group(function_get)

        f.canvas = f.Canvas('-')
        to_print = []
        to_print_functions = []
        canvas_size = f.canvas.size

        isUpdate = True
        run = True
        while run:
            clock.tick(60)
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    p = pygame.mouse.get_pos()
                    if p[0] in list(range(0, 300)) and p[1] in list(range(0, 50)):
                        self.current_menu += 1
                        self.current_menu %= len(self.class_names)
                        isUpdate = True

            fg.update(event_list)

            screen.fill(0)

            fg.draw(screen)

            font.render_to(screen, (10, 10), self.class_names[self.current_menu], (255, 255, 255))

            if isUpdate:
                isUpdate = False
                canvas_size = f.canvas.size
                to_print = f.canvas.print

                function_get.render_text()

                a = []
                for i in self.functions[self.current_menu]:
                    if '__' not in i or i == '__init__':
                        k = i + '('
                        b = f.get_function(self.classes[self.current_menu], i)
                        if b == ('', '', '', ''):
                            k += 'self)'
                        else:
                            if b[0][0] == 'self':
                                k += b[0][0]
                                if len(b[0]) > 1 or b[1] == 'args':
                                    k += ', '

                            for j in range(1, len(b[0])):
                                k += b[0][j]

                                if b[0][j] in list(b[3].keys()):
                                    d = str(b[3][b[0][j]])
                                    k += ': ' + d[8: -2]

                                if isinstance(b[2], tuple):
                                    d = str(b[2][j - 1])
                                    if d == '':
                                        d = "\'\'"
                                    k += ' = ' + d

                                if j < len(b[0]) - 1:
                                    k += ', '
                                else:
                                    if b[1] == 'args':
                                        k += ', '

                            if b[1] == 'args':
                                k += '*args'

                            k += ')'

                        a.append(k)

                if len(a[0]) > 50:
                    k = [a[0][:50], a[0][50:]]
                    for i in range(1, len(a)):
                        k.append(a[i])
                    a = list(k)
                to_print_functions = list(a)

            current_pos = 60
            for i in range(canvas_size):
                font2.render_to(screen, (10, current_pos), ''.join(to_print[i * canvas_size: (i + 1) * canvas_size]),
                                (255, 255, 255))
                current_pos += 15

            current_pos = 40
            for i in range(len(to_print_functions)):
                font2.render_to(screen, (460, current_pos), ''.join(to_print_functions[i]), (255, 255, 255))
                current_pos += 20

            pygame.display.flip()

        pygame.quit()
        exit()


class input_function(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font, max_len, m):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.max_len = max_len
        self.render_text()
        self.mo = m

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft = self.pos)

    def update(self, event_list):
        global isUpdate

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False

                    if self.text != '':
                        a = self.text.split(';')

                        for i in a:
                            func = i[: i.find('(')]

                            if func in self.mo.functions[self.mo.current_menu]:
                                args = i[i.find('(') + 1 : -1]
                                args_l = []

                                if args != '':
                                    args_l = args.split(',')

                                    for j in range(len(args_l)):
                                        if "'" in args_l[j]:
                                            args_l[j] = args_l[j][args_l[j].find("'") + 1: args_l[j].rfind("'")]
                                        else:
                                            try:
                                                args_l[j] = int(args_l[j])
                                            except:
                                                self.text = 'error'
                                                args_l = 0
                                                break

                                if isinstance(args_l, list):
                                    try:
                                        c = getattr(self.mo.classes[self.mo.current_menu], func)
                                        c(*args_l)

                                        self.text = 'ok'
                                    except:
                                        self.text = 'error'
                            else:
                                self.text = 'error'


                        isUpdate = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.max_len and event.unicode in self.mo.alphabet:
                        self.text += event.unicode
                self.render_text()
