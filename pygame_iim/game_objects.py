import pygame
import glob
from PIL import Image, ImageOps
from operator import add
import time
import math
from os import listdir
from random import randrange
import numpy as np

################################################# NPC types ############################################################


def npc_texter(npc_type, FRIEND):
    texts = []
    if npc_type == "Favorite":
        # Favorite NPC:
        texts.append([f"Hi {FRIEND}! Welcome to Trick-or-Treat!",
                      "My name is Noopcie and I'll help you get things started",
                      "In this town, people let you know what they want to receive by their costume.\nYou'll see",
                      "Remember, whenever you need my help, come over to me and press L"])

        texts.append(["It's Cookie Monster! he might want a cookie, don't you think?",
                      "Go to the candy jar and press K to take a candy",
                      "Then, go to the door and give Cookie Monster a candy (by pressing K)"])

        texts.append(["Our next visitor is a princess. \nprincesses like candies but they also like fruits",
                      "Give her either of them."])

        texts.append(
            ["Our next visitor is a ghost.\nHe could've been any of the other costumes when he was alive right?",
             "That's why it doesn't mind getting candy, fruit or money. Give it either of them"])

        texts.append([f"There are a few more visitors that may appear with different preferences.",
                      "I hung a LEGEND for you on the wall with different costumes and their preferences "
                      "in case you forget",
                      "Go to the LEGEND (above the shelf) and press K to read it"])

        texts.append([f"So this one is a hybrid costume.",
                      "People with hybrid costumes want something that both original costumes would like.",
                      "For Example, \nPrincesses like candies and fruits. Farmers like both fruit and money."
                      "\nWhat can we give them that they will both like?"])

        texts.append([f"Here's another hybrid, let's see if you got this"])

        # texts.append(
        #     ["Lastly, let's see you handle this hybrid. I'll be here if you need help, just come over and press L"])

        texts.append(["This one's weird huh? Because this hybrid isn't a regular one. "
                      "\nIf both parts of the hybrid don't share any preference, "
                      "\nthere's nothing you can give it.",
                      "And if we can't TREAT them, we TRICK them."
                      "\nGo take the water gun off the wall and TRICK this hybrid."])

        texts.append(["So the tutorial is now over but you can continue practicing for as long as you like"
                      "\nWhen you want to continue to the real game, press N.",
                      "During the real game, you'll need to work fast."
                      "\nYour score will be based on both time and accuracy.",
                      "I'll stay here to help when you need me until you go to the game."
                      "\nAfter that you're on your own. Hope I helped!"])

        resps = dict()
        resps["nothing"] = "First pick one of the options to give, then come back and give it :)"
        resps["legend"] = "Cool, The legend will always be available for you in case you forget something."
        resps[
            "knock"] = "Heard that knock on the door? Our first visitor is here. " \
                       "\nGo to the door and press K to open it."
        resps["yas"] = [f"Great {FRIEND}!", "Good!", "Great work!", f"Good Job {FRIEND}!", "Excellent!"]
        resps["try"] = "You might want to try something else"
        resps["hybrid"] = "What could we give both if they were separated? " \
                          "\nif there's no such thing it's kinda TRICKy."
        resps["base"] = "This one is easy. you got this LEGEND."
        resps["ghost"] = "Ghosts have no effect on our lives don't you think? " \
                         "\nHow ghosts affect other visitors?"
        resps["done"] = f"Apparently attic zombie needs my help. I gotta go, Good luck!"

    elif npc_type == "Hyper":
        # HYPER NPC:
        texts.append([f"Hello {FRIEND}!", "First time on Halloween door duty huh?",
                      "No Worries, My name is Noopcie and I'll help you getting started",
                      "In this town,"
                      "\npeople let you know what they want to receive with their costume choice."
                      "\nYou'll see what I mean", "Anyways,\nwhenever you need help,come over to me and press L"])

        texts.append([f"It's Cookie Monster!\nEveryone knows what the Cookie Monster likes. Cookies!",
                      f"Go to the candy jar and press K to take a candy"])

        #texts.append([f"Great, now go to the door and give Cookie Monster a candy (by pressing K)"])

        texts.append([f"Our next visitor is a princess.",
                      f"Princesses like Candy too but they also like fruits.\nGive her either of them."])

        texts.append([f"SPOOOOKY...", "Not really! this ghost is CUTE",
                      "In fact it's so cute that it doesn't mind getting candy, fruit or money."
                      "\nGive it either of them"])

        texts.append([f"There are a few more visitors that may appear with different preferences.",
                      "To make sure you know all these preferences, I hung a legend for you on the wall.",
                      "Go to the legend and press K to read it"])

        texts.append([f"So this one is a hybrid costume.",
                      "People with hybrid costumes want something that both original costumes would like.",
                      "\nFor Example, Princesses like candies and fruits. Farmers like both fruit and money."
                      "\nWhat can we give them that they will both like?"])

        texts.append([f"Here's another hybrid, let's see if you got this"])
        # texts.append(
        #     [f"Lastly, let's see you handle this hybrid. I'll be here if you need help, just come over and press L"])

        texts.append(
            [f"Don't know what to do huh? Because this hybrid is a special one!"
             f"\nIf both parts of the hybrid don't share any preference, you can't give anything.",
             "It means they're messing with you. And if we can't TREAT them, we TRICK them."
             "\nGo take the water gun off the wall and give them a lesson."])

        texts.append(["Alright, the tutorial is now over. You can continue practicing for as long as you like.",
                      "Whenever you feel ready,"
                      "\nContinue to the real game by pressing N.",
                      "It's important to note that during the real game, you'll need to work fast."
                      "\nYour score will be based on both time and accuracy.",
                      f"I'll stay here to help when you need me until you get to the next level."
                      f"\nAfter that you're on your own. Hope I helped you {FRIEND}!"])

        resps = dict()
        resps["nothing"] = f"We can't come empty-handed {FRIEND}, We got to choose something to give first."
        resps[
            "legend"] = "Good! The legend will always be available for you in case you forget.\nLet's see who comes now"
        resps["knock"] = "Someone knocked on the door! Let's find out who. Press K to open the door"
        resps["yas"] = [f"Great Job {FRIEND}!", "AMAZING!", "Great! You're really starting to get this",
                        f"Good Job {FRIEND}!", "Excellent!!!"]
        resps["try"] = "OOPS, Not this one Pal. Try something else you can do this!"
        resps["hybrid"] = "What could we give both if they were separated?\nif there's no such thing it's kinda TRICKy."
        resps["base"] = "You don't need my help with this one. you are a LEGEND."
        resps["ghost"] = "Funny thing about ghosts, \nWhether they exist or NOT, EVERYTHING STAYS THE SAME in life."
        resps["done"] = f"Alrighty I gotta go! attic zombie needs my help. Good luck {FRIEND}!"

    else:
        # Aloof NPC:
        texts.append(["Hi, my name is Noopcie.\nI'm here to help you learn how Trick or Treat works around here",
                      "In this town,"
                      "\npeople's costumes signify what they want you to give them, you'll see later",
                      "If you need help, come over to me and press L"])
        texts.append(["Your first visitor is Cookie Monster and he likes cookies.",
                      "Go to the candy jar and press K to take a candy"])

        #texts.append(["Good, now go to the door and give it to him (by pressing K)"])
        texts.append(["Your next visitor is a princess.",
                      "Princesses like candy and also fruits. Give her either"])

        texts.append(["This visitor is a ghost. Ghosts don't mind getting candy, fruit or money. Give it either"])

        texts.append(["There are a few more visitors that may appear with different preferences.",
                      "To make sure you know all these preferences, I hung a legend for you on the wall.",
                      "Go to the legend and press K to read it"])

        texts.append(["This one is a hybrid costume.",
                      "Hybrid costumes want to get something that satisfies both original costumes.",
                      "Princesses like candies and fruits. Farmers like both fruit and money. What can you give both?"])
        texts.append(["Try to handle this one on your own."])

        #texts.append(["Lastly, let's see you handle this one. If you need help, come over and press L"])

        texts.append(["This hybrid is a special one, if both parts of the hybrid don't share preferences"
                      "you can't TREAT them.",
                      "If you can't TREAT them, TRICK them. Go take the water gun of the wall"
                      "Then go to the visitor and press K to shoot"])

        texts.append(["The tutorial is now over. You can continue practicing for as long as you want."
                      "\nWhen you want to continue to the real game press N.",
                      "During the real game, you'll need to work fast."
                      "\nYour score will be based on both time and accuracy.",
                      "I'm still here until you get to the next level if you need help."
                      "\nAfter that you're on your own. Good luck"])

        resps = dict()
        resps["nothing"] = "You can't give nothing... First pick one of the options."
        resps["legend"] = "Okay, The legend will always be available for you in case you forget."
        resps["knock"] = "Go to the door and press K to open it"
        resps["yas"] = ["Good", "Cool", "Okay"]
        resps["try"] = "This one's wrong. Try again."
        resps["hybrid"] = "What can you give this hybrid? Can you give them both the same thing? else it's TRICK."
        resps["base"] = "Remember you can always use the LEGEND."
        resps["ghost"] = "Ghost hybrids are interesting. Think about the way they act."
        resps["done"] = "Alright, attic zombie needs my help, Don't let me down!"

    return texts, resps


CORRECT = {'Princess': {'Candy', 'Fruit'},
           'Robot': {'Candy', 'Money'},
           'Farmer': {'Fruit', 'Money'},
           'Cookie Monster': {'Candy'},
           'Tooth': {'Fruit'},
           'Businessman': {'Money'},
           'Ghost': {'Candy', 'Fruit', 'Money'}}


# TODO - Npc and Player classes
# Toggle between them as the right direction key is pressed.
# In case of an animated button - define the 'sensitive zone'? and find a way to get the button's coordinates.

class Animated_Sprite(pygame.sprite.Sprite):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, img_format='png'):
        super().__init__()
        self.sprites = []
        for f in glob.glob(animation_path + '/*.' + img_format):
            img = pygame.image.load(f)
            img = pygame.transform.smoothscale(img, game_size)
            self.sprites.append(img)
        self.current_sprite = 0
        self.speed = animation_speed
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


class Button(Animated_Sprite):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, sound_path=None, img_format='png',
                 tag='none'):
        super().__init__(animation_path, animation_speed, pos_x, pos_y, game_size, img_format)
        self.button_size = game_size
        self.key_pressed = False
        self.key_released = False
        self.tag = tag
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

    def set_hovered(self):
        self.key_pressed = True
        self.key_released = False

    def set_released(self):
        self.key_released = True
        self.key_pressed = False

    def update(self):
        if self.key_pressed and self.current_sprite == 0:
            self.current_sprite += self.speed

            if self.current_sprite >= 2:
                self.current_sprite = 0

        if self.key_released:
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def coll_check(self, event_pos, x_offset=0, y_offset=0):
        return (event_pos[0] in range(self.rect.center[0] - self.button_size[0] // 2 - x_offset,
                                      self.rect.center[0] + self.button_size[0] // 2 + x_offset)) and \
               (event_pos[1] in range(self.rect.center[1] - self.button_size[1] // 2,
                                      self.rect.center[1] + self.button_size[1] // 2 + y_offset))


class Door(Button):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, sound_path=None, img_format='png'):
        super().__init__(animation_path, animation_speed, pos_x, pos_y, game_size, sound_path, img_format)
        self.is_open = False
        self.shifted = False

    def update(self):
        super().update()
        if self.is_open:
            self.current_sprite = len(self.sprites) - 1
            if not self.shifted:
                self.rect.center = [self.rect.center[0] + 75, self.rect.center[1]]
            self.shifted = True
            self.image = self.sprites[int(self.current_sprite)]
        else:
            if self.shifted:
                self.rect.center = [self.rect.center[0] - 75, self.rect.center[1]]
            self.shifted = False
            # self.image = self.sprites[self.current_sprite]


class Player(Animated_Sprite):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, move_speed, step_sound_path=None,
                 img_format='png'):
        super().__init__(animation_path, animation_speed, pos_x, pos_y, game_size, img_format)
        self.key_dir_pressed = [False, False]
        self.key_dir_released = [False, False]
        self.deltas = [0, 0]
        self.curr_dir = 0
        if step_sound_path:
            self.sound = pygame.mixer.Sound(step_sound_path)
        self.flipped_sprites = []
        self.player_speed = move_speed
        for f in glob.glob(animation_path + '/*.' + img_format):
            image = Image.open(f)
            image = ImageOps.mirror(image)
            mode = image.mode
            size = image.size
            data = image.tobytes()
            img = pygame.image.fromstring(data, size, mode)
            img = pygame.transform.smoothscale(img, game_size)
            self.flipped_sprites.append(img)

    def set_pressed(self, dir_idx):
        self.key_dir_pressed[dir_idx] = True
        self.key_dir_released[dir_idx] = False

    def set_released(self):
        self.key_dir_pressed = [False, False]
        self.key_dir_released = [True, True]

    def update(self):

        if any(self.key_dir_pressed):
            if self.key_dir_pressed[0]:
                self.curr_dir = 0  # Right
            else:
                self.curr_dir = 1  # Left
            self.current_sprite += self.speed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

        if self.key_dir_released:
            self.current_sprite = 0

        if self.curr_dir:
            self.image = self.flipped_sprites[int(self.current_sprite)]
        else:
            self.image = self.sprites[int(self.current_sprite)]

    def update_delts(self, event, down=True):
        if down:
            if event.key == pygame.K_a:
                self.deltas[0] -= self.player_speed
                self.set_pressed(1)
            if event.key == pygame.K_d:
                self.deltas[0] += self.player_speed
                self.set_pressed(0)
            if event.key == pygame.K_w:
                self.deltas[1] -= self.player_speed
            if event.key == pygame.K_s:
                self.deltas[1] += self.player_speed
        else:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                self.deltas[0] = 0
                self.set_released()
            if event.key == pygame.K_w or event.key == pygame.K_s:
                self.deltas[1] = 0

    def move_player(self):
        self.rect.center = list(map(add, list(self.rect.center), self.deltas))


class NPC(Animated_Sprite):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, move_speed, loc_offset,
                 step_sound_path=None, img_format='png', type='Favorite', friend_name='Friend'):
        super().__init__(animation_path, animation_speed, pos_x, pos_y, game_size, img_format)
        self.key_dir_pressed = [False, False]
        self.key_dir_released = [False, False]
        self.deltas = [0, 0]
        self.curr_dir = 0
        self.subtext_i = 0
        self.text_i = 0
        self.is_talking = False
        self.curr_response = None
        self.type = type
        self.friend_name = friend_name
        self.texts, self.resps = npc_texter(type, friend_name)
        ###
        if step_sound_path:
            self.sound = pygame.mixer.Sound(step_sound_path)
        self.flipped_sprites = []
        self.move_speed = move_speed
        for f in glob.glob(animation_path + '/*.' + img_format):
            image = Image.open(f)
            image = ImageOps.mirror(image)
            mode = image.mode
            size = image.size
            data = image.tobytes()
            img = pygame.image.fromstring(data, size, mode)
            img = pygame.transform.smoothscale(img, game_size)
            self.flipped_sprites.append(img)
        self.dx, self.dy = 0, 0
        self.rect.center = [pos_x + loc_offset, pos_y + loc_offset]

    def move_towards_coords(self, coords,offset = 70):
        self.dx, self.dy = coords[0] - self.rect.center[0], coords[1] - self.rect.center[1]
        if abs(self.dx) >= offset or abs(self.dy) >= offset:
            dist = math.dist(coords, self.rect.center)
            self.dx, self.dy = self.dx / dist, self.dy / dist  # Normalize
            self.deltas[0] += self.dx * self.move_speed
            self.deltas[1] += self.dy * self.move_speed
        else:
            self.deltas = [0, 0]
        self.rect.center = list(map(add, list(self.rect.center), self.deltas))

    def update_texts(self, player_name):
        self.friend_name = player_name
        self.texts, self.resps = npc_texter(self.type, player_name)

    def npc_good(self):
        good = randrange(0, len(self.resps["yas"]))
        return self.resps["yas"][good]

    def npc_talk(self, msg_button, game_sprites, player, tut_phase, resp_conds, resp_texts, event,next_button,textfont,curr_enemy = None):
        """
        Determines what the npc should say next (if anything at all)
        :param tut_phase: How far into the tutorial are we
        :param resp_conds: Various conditions for condition-based repsonses
        :param resp_texts: Various responses incasae said condition is met
        :param event: in event.get.
        :return: msg_texts - text to be said by the npc.
        """
        if self.text_i != tut_phase:
            self.text_i = tut_phase
        texts = self.texts[self.text_i]
        if curr_enemy:  # We want to load enemy - specific texts? we're in the sandbox phase
            pass
        msg_texts = ""
        # Needed if a response is script-dependant.
        action = 0  # 0 == didn't talk, 1 == scripted talking, 2 == responding, 3 == scripted message done, 4 == response message done
        # Can only respond once, looks for the first response condition
        resp_i = np.where(resp_conds)[0]
        resp_cond = resp_conds[resp_i[0]] if resp_i.size else False
        if resp_cond or self.curr_response:  # Response
            if not self.is_talking:
                if resp_cond:  # Npc should respond to something rn.
                    self.is_talking = True
                    self.curr_response = resp_texts[resp_i[0]]
                    msg_texts = resp_texts[resp_i[0]]
                    action = 2

            else:  # npc is already talking
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:  # l was pressed to advance
                    next_button.set_hovered()
                    next_button.sound.play()
                    self.is_talking = False  # Responses are exclusively 1-panel
                    self.curr_response = None
                    action = 4
                else:  # Frame idle
                    msg_texts = self.curr_response
                    action = 2

        else:  # Scripted talk
            if not self.is_talking:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:  # Npc should start with a scripted message
                    if msg_button in game_sprites and msg_button.coll_check(player.rect.center, x_offset=50,
                                                                            y_offset=80):
                        msg_button.set_hovered()
                        msg_button.sound.play()
                        self.is_talking = True
                        msg_texts = texts[self.subtext_i]
                        action = 1
            else:  # npc is already talking
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:  # l was pressed to advance
                    next_button.set_hovered()
                    next_button.sound.play()
                    if msg_button in game_sprites:
                        self.subtext_i += 1
                        if self.subtext_i >= len(texts):
                            self.is_talking = False
                            self.text_i += 1
                            self.subtext_i = 0
                            msg_button.set_released()
                            game_sprites.remove(msg_button)
                            action = 3
                else:
                    msg_texts = texts[self.subtext_i]
                    action = 1

        return msg_texts, action

    def update(self):
        if self.dx < 0:
            self.curr_dir = 1
        else:
            self.curr_dir = 0
        if self.curr_dir:
            self.image = self.flipped_sprites[int(self.current_sprite)]
        else:
            self.image = self.sprites[int(self.current_sprite)]


class Msg_Button(Button):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, y_offset, npc: NPC, sound_path=None,
                 img_format='png'):
        super().__init__(animation_path, animation_speed, pos_x, pos_y, game_size, sound_path, img_format)
        rect_center = [npc.rect.center[0], npc.rect.center[1] + y_offset]
        self.rect.center = rect_center
        self.npc = npc
        self.y_offset = y_offset

    def update(self):
        super().update()
        self.image = self.sprites[int(self.current_sprite)]
        rect_center = [self.npc.rect.center[0], self.npc.rect.center[1] + self.y_offset]
        self.rect.center = rect_center


class Enemy(pygame.sprite.Sprite):
    def __init__(self, animation_path, pos_x, pos_y, game_size, title, title_2=None, img_format='png'):
        super().__init__()
        if title_2 is None:
            f = animation_path + '.' + img_format
            img = pygame.image.load(f)
            self.image = pygame.transform.smoothscale(img, game_size)
            self.rect = self.image.get_rect()
            self.rect.center = [pos_x, pos_y]
            self.title = title
            self.correct_answers = CORRECT[title]
        else:
            f = animation_path + '.' + img_format
            img = pygame.image.load(f)
            self.image = pygame.transform.smoothscale(img, game_size)
            self.rect = self.image.get_rect()
            self.rect.center = [pos_x, pos_y]
            self.title = f"{title}-{title_2}"
            self.correct_answers = CORRECT[title].intersection(CORRECT[title_2])
            if len(self.correct_answers) == 0:
                self.correct_answers = ["Trick"]

    def coll_check(self, event_pos, x_offset=0, y_offset=0):
        return (event_pos[0] in range(self.rect.center[0] - 100 // 2 - x_offset,
                                      self.rect.center[0] + 100 // 2 + x_offset)) and \
               (event_pos[1] in range(self.rect.center[1] - 100 // 2,
                                      self.rect.center[1] + 100 // 2 + y_offset))

    def get_enemy(self):
        return self

    # TODO: implement if necessary
    def deploy(self):
        pass


class Outcome:
    def __init__(self, V_sound_path, X_sound_path):
        self.right = False
        self.wrong = False
        self.right_sound = pygame.mixer.Sound(V_sound_path)
        self.right_sound.set_volume(0.2)
        self.wrong_sound = pygame.mixer.Sound(X_sound_path)
        self.wrong_sound.set_volume(0.2)
        self.sound = None

    def check_choice(self, choice, curr_enemy):
        if choice:
            if choice in curr_enemy.correct_answers:
                self.right = True
                self.wrong = False
                self.sound = self.right_sound
            else:
                self.right = False
                self.wrong = True
                self.sound = self.wrong_sound
        return self

    def reset(self):
        self.right = False
        self.wrong = False