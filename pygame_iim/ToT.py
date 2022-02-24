import pygame
import time
from random import randrange
import numpy as np
import yagmail
import csv
from PIL import Image, ImageOps
from operator import add
import math
import glob
import keyring
import sys

"""
#################################################### EVALUATION CODE ###################################################
"""


def send_mail(subject, msg, who):
    my_password = "ToTResMail00"
    mail_add = "eldarnirpersonal@gmail.com"
    rec_mail = f"eldarnirpersonal+{who}@gmail.com"
    yagmail.register(mail_add, my_password)
    yag = yagmail.SMTP(mail_add)
    yag.send(
        to=rec_mail,
        subject=subject,
        contents=msg,
    )


def send_mail_csv(subject, msg, results_csv, who):
    my_password = "ToTResMail00"
    mail_add = "eldarnirpersonal@gmail.com"
    rec_mail = f"eldarnirpersonal+{who}@gmail.com"
    yagmail.register(mail_add, my_password)
    yag = yagmail.SMTP(mail_add)
    yag.send(
        to=rec_mail,
        subject=subject,
        contents=msg,
        attachments=results_csv,
    )


def accuracy(lst):
    return round(sum(lst) / len(lst), 2)


def avg_time(lst):
    return round(sum(lst) / len(lst), 2)


def prep_csv(acc, time, eng, tut, ans, NPC_type, player_id, score, replays):
    with open('game_assets_f/stats.csv', 'a', newline='') as file:
        fieldnames = ['Player', 'NPC', 'Answers', 'Accuracy', 'Time', 'Tutorial', 'Engagement', 'Score', 'Replays']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'Player': player_id, 'NPC': NPC_type, 'Answers': ans, 'Accuracy': acc, 'Time': time,
                         'Tutorial': tut, 'Engagement': eng, 'Score': score, 'Replays': replays})


# TODO: fix eng for specific NPC types
def report_performance_mail(acc, time, eng, tut, ans, NPC_type, player_id, score, replays):
    msg = f"Who: {player_id}\n \
            NPC: {NPC_type}\n \
            Answers: {ans}\n \
            Accuracy: {acc}\n \
            Time: {time}\n \
            Tutorial stats: {tut}\n \
            NPC engagement: {eng}\n \
            High Score: {score}\n \
            Replays: {replays}\n \
            "
    # TODO: try adding empty csv to exe and sending the data in the csv through mail.
    subject = f"{player_id}'s Statistics"
    prep_csv(acc, time, eng, tut, ans, NPC_type, player_id, score, replays)
    # send_mail(subject, msg, player_id)
    send_mail_csv(subject, msg, "game_assets_f/stats.csv", player_id)


"""
#################################################### END OF EVALUATION CODE ############################################
"""
"""
#################################################### GAME OBJECTS CODE #################################################
"""


################################################# NPC types ############################################################


def npc_texter(npc_type, FRIEND):
    texts = []
    if npc_type == "Favorite":
        # Favorite NPC:
        texts.append([f"Hi {FRIEND}! Welcome to Trick-or-Treat!",
                      "My name is Noopcie and I'll help you get things started.",
                      "In this town, people let you know what they want to receive by their costume.\nYou'll see.",
                      "Remember, whenever you need my help, come over to me and press [L]."])

        texts.append(["It's Cookie Monster.\nHe might want a cookie, don't you think?",
                      "Go to the candy jar (near the door) and press [K] to take a candy.",
                      "Then, go to the door and give Cookie Monster the candy (by pressing [K])."])

        texts.append(["Our next visitor is a princess. \nPrincesses like candies but they also like fruits.",
                      "The fruit basket is located in the bottom right corner of the room.",
                      "Give her either of them."])

        texts.append(
            ["Our next visitor is a ghost.\nHe could've been any of the other costumes when he was alive right?",
             "That's why it doesn't mind getting candy, fruit or money. Give it either of them."
             "\nThe wallet is in the bottom left corner of the room."])

        texts.append([f"There are a few more visitors that may appear with different preferences.",
                      "I hung a LEGEND for you on the wall above the left shelf, next to the door."
                      "\nIn it you'll find the different costumes and their preferences in case you forget.",
                      "Go to the LEGEND (above the shelf) and press [K] to read it."])

        texts.append([f"So this one is a hybrid costume."
                      f"\nA hybrid costume is a combination of 2 basic costumes.",
                      "People with hybrid costumes want something that both original costumes would like.",
                      "You can always check the legend to see what both original costumes like."
                      "\nWhat can we give them that will satisfy both?"])

        texts.append([f"Here's another hybrid, you got this."])

        texts.append(["This one's weird huh? Because this hybrid isn't a regular one."
                      "\nIf both parts of the hybrid don't share any preference, "
                      "\nthere's nothing you can give it.",
                      "If we can't TREAT them, we TRICK them."
                      "\nGo take the water gun off the wall (top left) and TRICK this hybrid."])

        texts.append(["So the tutorial is now over but you can continue practicing for as long as you like."
                      "\nWhen you want to continue to the real game, press [N].",
                      "During the real game, you'll need to work fast."
                      "\nYour score will be based on both time and accuracy.",
                      "I'll stay here to help when you need me until you press [N] to move to the next level."
                      "\nAfter that you're on your own. Hope I helped!"])

        resps = dict()
        resps["nothing"] = "First pick one of the options to give, then come back and give it :)"
        resps["legend"] = "Great, The legend will always be available for you in case you forget something."
        resps[
            "knock"] = "Heard that knock on the door? Our first visitor is here. " \
                       "\nGo to the door and press [K] to open it."
        resps["yas"] = [f"Great {FRIEND}!", "Good!", "Great work!", f"Good Job {FRIEND}!"]
        resps["try"] = "You might want to try something else pal."
        resps["hybrid"] = "What could we give both if they were separated? " \
                          "\nIf there's no such thing it's kinda TRICKy."
        resps["base"] = "This one is easy. you got this, LEGEND."
        resps["ghost"] = "Ghosts have no effect on our lives don't you think? " \
                         "\nHow do ghosts affect other visitors?"
        resps["done"] = f"Apparently attic zombie needs my help. I gotta go, Good luck!"

    elif npc_type == "Hyper":
        # HYPER NPC:
        texts.append([f"Hello {FRIEND}!!", "First time on Halloween door duty huh?",
                      "No Worries, My name is Noopcie and I'll help you get things started.",
                      "In this town,"
                      "\nPeople let you know what they want to receive with their costume choice."
                      "\nYou'll see what I mean.", "Anyways,\nwhenever you need help,come over to me and press [L]."])

        texts.append([f"It's Cookie Monster!\nEveryone knows what the Cookie Monster likes. Cookies!",
                      f"Go to the candy jar (near the door) and press [K] to take a candy.",
                      f"Then go back to the door and press [K] to give the candy."])

        # texts.append([f"Great, now go to the door and give Cookie Monster a candy (by pressing K)"])

        texts.append([f"Our next visitor is a princess, WOW!!",
                      "We're in the presence of ROYALTY!!",
                      f"Princesses like Candy too but they also like fruit."
                      f"\nOur fruit basket is in the bottom right corner of the room."
                      f"\nGive her either of them."])

        texts.append([f"SPOOOOKY...", "Not really! this ghost is CUTE.",
                      "In fact it's so cute that it doesn't mind getting candy, fruit or money."
                      "\nOur wallet is in the bottom left corner of the room."
                      "\nGive it either of them."])

        texts.append([f"There are a few more visitors that may appear with different preferences.",
                      f"To make sure my good friend {FRIEND} knows all these preferences,",
                      "I hung a legend for on the wall above the left shelf, next to the door!",
                      "Go to the legend and press [K] to read it.",
                      "a LEGEND fitting for a LEGEND like you!"])

        texts.append([f"Your first hybrid visitor, that's SO COOL!"
                      f"\nHybrid costumes are combinations of 2 basic costumes.",
                      "People with hybrid costumes want something that both original costumes would like.",
                      f"Interesting, right super-{FRIEND}?",
                      "\nFor Example, Princesses like candies and fruits, and Farmers like both fruit and money!"
                      "\nWhat can we give them that they will both like?"])

        texts.append([f"Here's another hybrid!",
                      f"You GOT this {FRIEND}!",
                      "Farmers like both fruit and money while \nthe businessman only likes money!"
                      f"Go {FRIEND}!!"])
        # texts.append(
        #     [f"Lastly, let's see you handle this hybrid. I'll be here if you need help, just come over and press L"])

        texts.append(
            [f"Well this hybrid is a special one!",
             "Bet you probably already figured it out yourself, right super-{FRIEND}?",
             f"\nIf both parts of the hybrid don't share any preference, you can't give anything.",
             "It means they're messing with you. And if we can't TREAT them, we TRICK them!!"
             "\nGo take the water gun off the wall (top left) and give them a lesson."])

        texts.append(["Alrighty, that marks the end of this tutorial. You can continue practicing for as long ",
                      "and as much",
                      "as you like.",
                      "Whenever you feel ready,"
                      "\nContinue to the real game by pressing [N].",
                      "It's important to note that during the real game, you'll need to work FAST."
                      "\nYour score will be based on both time and accuracy.",
                      f"I'll stay here to help when you need me until you press [N] to move to the next level.",
                      f"After that you're on your own. Hope I helped you super-{FRIEND}!"])

        resps = dict()
        resps["nothing"] = f"We can't come empty-handed {FRIEND}, We got to choose something to give first."
        resps["legend"] = "Awesome!! The legend will always be available for you in case you forget something." \
                          f"\nLet's see who comes in now, aren't you excited {FRIEND}?"
        resps["knock"] = "Someone knocked on the door!! EXCITING!!\n Let's find out who. Press [K] to open the door."
        resps["yas"] = [f"Great Job {FRIEND}!!", f"AMAZING {FRIEND}!!!", f"Go {FRIEND}!!", "Excellent!!!"]
        resps["try"] = "OOPS, Not this one Pal. Try something else you can do this!!"
        resps["hybrid"] = "What could we give both costumes if they were separated?\n if there's NO such thing, use the Trick Gun!"
        resps["base"] = f"Look at the LEGEND super-{FRIEND}! You got this."
        resps["ghost"] = f"Look at this ghost {FRIEND}! does it affect our visitor?\n remember regular ghosts will accept anything!"
        resps["done"] = f"Alrighty I gotta go! attic zombie needs my help.\n Good luck mega-{FRIEND}! YOU GOT THIS!"

    else:
        # Aloof NPC:
        texts.append(["Hey there new guy, my name is Noopcie."
                      "\nI'm here to help you learn how Trick or Treat works around here.",
                      "In this town,"
                      "\npeople's costumes signify what they want you to give them, you'll see later.",
                      "If you need help, come over to me and press [L]."])

        texts.append(["Your first visitor is Cookie Monster and he likes cookies.",
                      "Go to the candy jar (near the door) and press [K] to take a candy.",
                      "Then go back to the door and press K to give the candy."])

        # texts.append(["Good, now go to the door and give it to him (by pressing K)"])
        texts.append(["Your next visitor is a princess.",
                      "Princesses like candies and also fruits (which are in the bottom right)."
                      "\nGive her either."])

        texts.append(["This visitor is a ghost. Ghosts don't mind getting candy, fruit or money (bottom left)."
                      "\nGive it either."])

        texts.append(["There are a few more visitors that may appear with different preferences.",
                      "So go to the LEGEND (above the left shelf, near the door) and press K to read it."])

        texts.append(["This one is a hybrid costume, a combination of 2 basic costumes.",
                      "Check the LEGEND to see what both original costumes will like\n and give it that."])

        texts.append(["Try to handle this one on your own."])

        # texts.append(["Lastly, let's see you handle this one. If you need help, come over and press L"])

        texts.append(["This hybrid is a special one since the hybrid's parts don't share\n preferences.",
                      "If you can't TREAT them, Go take the water gun of the wall (top left)"
                      "\nThen go to the visitor and TRICK them. press K to shoot."])

        texts.append(["The tutorial is now over. You can continue practicing for as long as you want."
                      "\nWhen you want to continue to the real game press [N].",
                      "During the real game, you'll need to work fast."
                      "\nYour score will be based on both time and accuracy.",
                      "I'm still here until you press [N] to move to the next level." 
                      "\nAfter that you're on your own."])

        resps = dict()
        resps["nothing"] = "You can't give nothing... First pick one of the options."
        resps["legend"] = "Okay, The LEGEND will always be right there."
        resps["knock"] = "Go to the door and press K to open it."
        resps["yas"] = ["Good", "Cool", "Okay"]
        resps["try"] = "This one's wrong. Try again..."
        resps["hybrid"] = "Look, can you give both costume parts the same thing?\nOTHERWISE, you should know what to do."
        resps["base"] = "You might see me as a LEGEND, but I'm not..."
        resps["ghost"] = "Listen, ghosts don't exist.\n I don't see a ghost there..."
        resps["done"] = "Attic zombie needs my help, Don't let me down..."

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
                 tag=None):
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
               (event_pos[1] in range(self.rect.center[1] - self.button_size[1] // 2 - y_offset,
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


def mirror_img(f, game_size):
    image = Image.open(f)
    image = ImageOps.mirror(image)
    mode = image.mode
    size = image.size
    data = image.tobytes()
    img = pygame.image.fromstring(data, size, mode)
    img = pygame.transform.smoothscale(img, game_size)
    return img


class Player(Animated_Sprite):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, move_speed, step_sound_path=None,
                 img_format='png'):
        super().__init__(animation_path, animation_speed, pos_x, pos_y, game_size, img_format)
        self.key_dir_pressed = [False, False]
        self.key_dir_released = [False, False]
        self.deltas = [0, 0]
        self.curr_dir = 0
        self.game_size = game_size
        if step_sound_path:
            self.sound = pygame.mixer.Sound(step_sound_path)
        self.flipped_sprites = []
        self.player_speed = move_speed
        for f in glob.glob(animation_path + '/*.' + img_format):
            self.flipped_sprites.append(mirror_img(f, game_size))

    def change_sprite(self, sprite_path):
        self.sprites = []
        self.flipped_sprites = []
        img = pygame.image.load(sprite_path)
        img = pygame.transform.smoothscale(img, self.game_size)
        self.sprites.append(img)
        self.flipped_sprites.append(mirror_img(sprite_path, self.game_size))

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
            #dt = clock.tick(1000)
            if event.key == pygame.K_a:
                self.deltas[0] -= self.player_speed * stretch[0]  #* dt
                self.set_pressed(1)
            if event.key == pygame.K_d:
                self.deltas[0] += self.player_speed * stretch[0]  #* dt
                self.set_pressed(0)
            if event.key == pygame.K_w:
                self.deltas[1] -= self.player_speed * stretch[1] #* dt
            if event.key == pygame.K_s:
                self.deltas[1] += self.player_speed * stretch[1] #* dt
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

    def move_towards_coords(self, coords, offset=70):
        self.dx, self.dy = coords[0] - self.rect.center[0], coords[1] - self.rect.center[1]
        if abs(self.dx) >= offset or abs(self.dy) >= offset:
            dist = math.dist(coords, self.rect.center)
            self.dx, self.dy = self.dx / dist, self.dy / dist  # Normalize
            self.deltas[0] += self.dx * self.move_speed*stretch[0]
            self.deltas[1] += self.dy * self.move_speed*stretch[1]
        else:
            self.deltas = [0, 0]
        self.rect.center = list(map(add, list(self.rect.center), self.deltas))

    def update_texts(self, player_name):
        self.friend_name = player_name
        self.texts, self.resps = npc_texter(self.type, player_name)

    def npc_good(self):
        good = randrange(0, len(self.resps["yas"]))
        return self.resps["yas"][good]

    def npc_talk(self, msg_button, game_sprites, player, tut_phase, resp_conds, resp_texts, event, next_button,
                 textfont, force_talk=False):
        """
        Determines what the npc should say next (if anything at all)
        :param tut_phase: How far into the tutorial are we
        :param resp_conds: Various conditions for condition-based repsonses
        :param resp_texts: Various responses incasae said condition is met
        :param event: in event.get.
        :param force_talk - in case we want the npc to talk regardless of interaction.
        :return: msg_texts - text to be said by the npc.
        """
        if self.text_i != tut_phase:
            self.text_i = tut_phase
        texts = self.texts[self.text_i]
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l or \
                        (event.type == pygame.MOUSEBUTTONDOWN and next_button.coll_check(
                            event.pos)):  # l was pressed to advance
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
                if (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_l) or force_talk:  # Npc should start with a scripted message
                    if msg_button in game_sprites and msg_button.coll_check(player.rect.center, x_offset=50,
                                                                            y_offset=80):
                        msg_button.set_hovered()
                        msg_button.sound.play()
                        self.is_talking = True
                        msg_texts = texts[self.subtext_i]
                        action = 1

            else:  # npc is already talking
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l or \
                        (event.type == pygame.MOUSEBUTTONDOWN and next_button.coll_check(
                            event.pos)):  # l was pressed to advance
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


"""
############################################ END OF GAME OBJECTS #######################################################
"""

##################################################### MEASURES #########################################################
reaction_times = []
answered_correctly = []
tut_accumulative = []  # TODO: for the learning curve
curr_score = 0
best_score = 0
replays = 0


# TODO: anything else we want to measure?

################################################## MAIN.py FUNCTIONS #####################################################

def fit_bg_dims(game_dims, bg_path):
    bg = pygame.image.load(bg_path).convert()  # Tutorial guy said it's important
    bg = pygame.transform.smoothscale(bg, game_dims)  # Changes image dims
    return bg


def game_setup(game_dims, game_name, icon_path, bg_path):
    screen = pygame.display.set_mode(game_dims)  # add pygame.FULLSCREEN if fullscreen
    pygame.display.set_caption(game_name)
    icon = pygame.image.load(icon_path)
    icon = pygame.transform.smoothscale(icon, (32, 32))
    pygame.display.set_icon(icon)
    return screen, fit_bg_dims(game_dims, bg_path)


def border_check(game_dims, p_coords, player_size):
    temp = list(p_coords)
    if p_coords[0] <= 0:
        temp[0] = 0
    elif p_coords[0] >= game_dims[0] - player_size:
        temp[0] = game_dims[0] - player_size
    if p_coords[1] <= 0:
        temp[1] = 0
    elif p_coords[1] >= game_dims[1] - player_size:
        temp[1] = game_dims[1] - player_size
    p_coords = tuple(temp)
    return p_coords


def knock_on_door(cond, knocked):
    if cond:
        door_button.set_hovered()
        knock_sound.play()
        knocked = True
    return knocked


def score(ans_lst, time_lst):
    score = 0.0
    for i, ans in enumerate(ans_lst):
        if ans:
            tim = float(time_lst[i])
            score += (5.57 / tim) * 10
    acc = accuracy(ans_lst)
    avg_time = accuracy(time_lst)
    return round(score*acc, 2) if acc <= 0.5 and avg_time <= 2.5 else round(score, 2)


def adj_draw(msg_texts, core_surface, x=75, y=440):
    texts = msg_texts.splitlines()
    for i, text in enumerate(texts):
        msg_text = textfont.render(text, 1, (0, 0, 0))
        core_surface.blit(msg_text, (tf(x, 0), tf(y + i * 25, 1)))


def update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts, text_sprites, door,
                 remainder=False):
    player.move_player()
    if npc:
        npc.move_towards_coords(player.rect.center)
        npc.rect.center = border_check(game_size, npc.rect.center, 32)
    player.rect.center = border_check(game_size, player.rect.center, 32)
    if door.is_open:
        core_surface.blit(title_window, (tf(430, 0), tf(43, 1)))
        core_surface.blit(enemy_title, (tf(449, 0), tf(63, 1)))
    tool_sprites.draw(core_surface)
    tool_sprites.update()
    game_enemy.draw(core_surface)
    game_sprites.draw(core_surface)
    game_sprites.update()
    if npc and npc.is_talking:
        core_surface.blit(noopcie_pic, (tf(20, 0), tf(265, 1)))
        core_surface.blit(text_window, (tf(0, 0), tf(300, 1)))
        hint_text = textfont.render('<press the [L] key or the next button to advance>', 1, (72, 120, 170))
        core_surface.blit(hint_text, (tf(80, 0), tf(540, 1)))
        adj_draw(msg_texts, core_surface)
        text_sprites.draw(core_surface)
        text_sprites.update()
    if remainder:
        core_surface.blit(rem_window, (tf(0, 0), tf(530, 1)))
        hint_text = textfont.render('<Keep practicing, and when ready press the [N] key to test your mettle!>',
                                    1, (72, 120, 170))
        core_surface.blit(hint_text, (tf(80, 0), tf(547, 1)))


def tf(num, pos):
    return int(num * stretch[pos])


################################################# INIT STUFF ###########################################################
pygame.init()
#game_size = (1366, 748)
game_size = (800, 600)
#stretch = (1.7075, 1.24666)
stretch = (1, 1)
core_surface, main_menu = game_setup(game_size, 'Tomidos project', 'game_assets_f/Tools/Candy/candy_i.png',
                                     'game_assets_f/Backgrounds/mm_bg.png')
text_window = pygame.image.load('game_assets_f/text_window.PNG')
text_window = pygame.transform.smoothscale(text_window, [tf(825, 0), tf(400, 1)])  # Changes image dims
title_window = pygame.transform.smoothscale(text_window, [tf(300, 0), tf(70, 1)])  # Changes image dims
rem_window = pygame.transform.smoothscale(text_window, [tf(800, 0), tf(70, 1)])  # Changes image dims
textfont = pygame.font.SysFont('leelawadeeuisemilight', 20)
scorefont = pygame.font.SysFont('leelawadeeuisemilight', 32)
basefont = pygame.font.Font(None, 32)

level_0 = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/lvl_bg.png')
instruct_screen = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/instruct_bg.png')
pause_screen = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/pause_bg.png')
name_screen = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/name_bg.png')
curr_screen = main_menu

clock = pygame.time.Clock()
pop_sound = pygame.mixer.Sound('game_assets_f/sounds/msg_pop.flac')
knock_sound = pygame.mixer.Sound('game_assets_f/sounds/door_knock_sound.mp3')

# MUSIC
pygame.mixer.music.load("game_assets_f/sounds/menu_to_tutorial_music.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
# pygame.mixer.music.load("game_assets_f/sounds/game_theme_music.mp3")

stats = None
npc_flag = False
choice = None
door_open = False
door_rang = False
running = True
tut_phase = 0
phase_buttons = []
tut_lvl = 0
msg_texts = ''
ts = 0
already_named = False
################################################# CREATE ENEMIES #######################################################

game_enemy = pygame.sprite.Group()
# TODO: use For loop
single_opts = ["Princess", "Robot", "Farmer", "Cookie Monster", "Tooth", "Businessman", "Ghost"]
ghost_opts = []
for g_comb in single_opts[:-1]:
    ghost_opts.append(g_comb + "-Ghost")
Princess = Enemy("game_assets_f/game_enemies/Princess", tf(500, 0), tf(190, 1), (tf(215, 0), tf(162, 1)), "Princess", img_format='png')
Robot = Enemy("game_assets_f/game_enemies/Robot", tf(500, 0), tf(190, 1), (tf(215, 0), tf(162, 1)), "Robot", img_format='png')
Farmer = Enemy("game_assets_f/game_enemies/Farmer", tf(500, 0), tf(190, 1), (tf(215, 0), tf(162, 1)), "Farmer", img_format='png')
Cookie = Enemy("game_assets_f/game_enemies/Cookie Monster", tf(500, 0), tf(190, 1), (tf(215, 0), tf(162, 1)), "Cookie Monster", img_format='png')
Tooth = Enemy("game_assets_f/game_enemies/Tooth", tf(500, 0), tf(190, 1), (tf(215, 0), tf(162, 1)), "Tooth", img_format='png')
Business = Enemy("game_assets_f/game_enemies/Businessman", tf(500, 0), tf(190, 1), (tf(215, 0), tf(162, 1)), "Businessman", img_format='png')
Ghost = Enemy("game_assets_f/game_enemies/Ghost", tf(500, 0), tf(190, 1), (tf(215, 0), tf(162, 1)), "Ghost", img_format='png')
reg_enemies = [Princess, Robot, Farmer, Cookie, Tooth, Business, Ghost]
hybrid_enemies = []
for i, i_opt in enumerate(single_opts):
    for j in range(i + 1, len(single_opts)):
        j_opt = single_opts[j]
        hybrid_enemies.append(
            Enemy(f"game_assets_f/game_enemies/ToT - {i_opt}-{j_opt}", tf(500, 0), tf(190, 1), (tf(215, 0), tf(162, 1))
                  , i_opt, j_opt, img_format='png'))
all_enemies = reg_enemies.copy()
all_enemies.extend(hybrid_enemies)

tut_enemies = [Cookie, Princess, Ghost, hybrid_enemies[1], hybrid_enemies[13], hybrid_enemies[4]]

# Princess, Ghost-Princess, Tooth-Business(Trick), Tooth , Busi-Cookie(Trick), Ghost,
# Robot-Busi,Farmer-Princess, Farmer-Cookie(Trick),Princess-Tooth
game_enemies = [all_enemies[0], all_enemies[12], all_enemies[25], all_enemies[4], all_enemies[23], all_enemies[6],
                all_enemies[16], all_enemies[8], all_enemies[18], all_enemies[10]]

################################################# SCREENS ##############################################################

# Main Menu Screen: ####################################################################################################
menu_sprites = pygame.sprite.Group()
play_button = Button('game_assets_f/Buttons/play_button', 1, tf(400, 0), tf(200, 1),
                     (tf(215, 0), tf(162, 1)),
                     sound_path='game_assets_f/sounds/button_click.wav')
quit_button = Button('game_assets_f/Buttons/quit_button', 1, tf(400, 0), tf(400, 1), (tf(215, 0), tf(162, 1)),
                     sound_path='game_assets_f/sounds/button_click.wav')
menu_sprites.add([play_button, quit_button])

# Pause Menu Screen: ###################################################################################################
pause_sprites = pygame.sprite.Group()
p_res_button = Button('game_assets_f/Buttons/continue_button', 1, tf(400, 0), tf(400, 1), (tf(215, 0), tf(162, 1)),
                      sound_path='game_assets_f/sounds/button_click.wav')
p_quit_button = Button('game_assets_f/Buttons/quit_button', 1, tf(400, 0), tf(500, 1), (tf(215, 0), tf(162, 1)),
                       sound_path='game_assets_f/sounds/button_click.wav')
pause_sprites.add([p_res_button, p_quit_button])

# Name Menu Screen: ###################################################################################################
name_sprites = pygame.sprite.Group()
n_res_button = Button('game_assets_f/Buttons/continue_button', 1, tf(385, 0), tf(499, 1), (tf(150, 0), tf(113, 1)),
                      sound_path='game_assets_f/sounds/button_click.wav')
name_sprites.add(n_res_button)
user_name = ''
text_input_rect = pygame.Rect(tf(460, 0), tf(295, 1), tf(140, 0), tf(32, 1))
bad_sound = pygame.mixer.Sound('game_assets_f/sounds/stuck_sound.mp3')
color_bad = pygame.Color(247, 70, 91)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('lightskyblue2')
color = color_passive
active = False

# Game Screen: #########################################################################################################
game_sprites = pygame.sprite.Group()
player = Player('game_assets_f/player', 0, tf(370, 0), tf(480, 1), (tf(129, 0), tf(97, 1)), 2, img_format='PNG')
npc_types = ["Favorite", "Hyper", "Aloof"]
random_type = randrange(0, 3)
# random_type = 2
chosen_npc = npc_types[random_type]
# chosen_npc = 'Aloof'
noopcie_pic = pygame.image.load('game_assets_f/Noopcie/{}/Noopcie_{}.png'.format(chosen_npc, random_type + 1))
noopcie_pic = pygame.transform.smoothscale(noopcie_pic, [tf(214, 0), tf(162, 1)])
FRIEND = "FRIEND"
npc = NPC('game_assets_f/Noopcie/{}'.format(chosen_npc), 0, tf(608, 0), tf(84, 1), (tf(82, 0), tf(65, 1)), 2, loc_offset=100, img_format='PNG',
          type=chosen_npc, friend_name=FRIEND)
sandbox_approaches = float(-1 * len(npc.texts[-1]) - 2) / 2 + 0.5
msg_button = Msg_Button('game_assets_f/Buttons/msg_button', 1, tf(400, 0), tf(200, 1), (tf(100, 0), tf(75, 1)), npc=npc, y_offset=-60,
                        sound_path='game_assets_f/sounds/button_click.wav')
text_sprites = pygame.sprite.Group()
next_button = Button('game_assets_f/Buttons/next_button', 1, tf(720, 0), tf(540, 1), (tf(107, 0), tf(81, 1)),
                     sound_path='game_assets_f/sounds/button_click.wav')
game_button = Button('game_assets_f/Buttons/next_button', 1, tf(720, 0), tf(540, 1), (tf(107, 0), tf(81, 1)),
                     sound_path='game_assets_f/sounds/button_click.wav')
door_button = Door('game_assets_f/Buttons/door_button', 1, tf(500, 0), tf(190, 1), (tf(300, 0), tf(185, 1)),
                   sound_path='game_assets_f/sounds/door_open.wav')

game_sprites.add([door_button, msg_button, npc, player])
text_sprites.add([next_button])

tool_sprites = pygame.sprite.Group()

candy_button = Button('game_assets_f/Tools/Candy', 1, tf(220, 0), tf(175, 1), (tf(112, 0), tf(81, 1)),
                      sound_path='game_assets_f/sounds/candy_sound.wav', tag='Candy')
fruit_button = Button('game_assets_f/Tools/Fruit', 1, tf(610, 0), tf(475, 1), (tf(112, 0), tf(81, 1)),
                      sound_path='game_assets_f/sounds/fruit_sound.wav', tag='Fruit')
money_button = Button('game_assets_f/Tools/Money', 1, tf(100, 0), tf(395, 1), (tf(90, 0), tf(64, 1)),
                      sound_path='game_assets_f/sounds/money_sound.wav', tag='Money')
trick_button = Button('game_assets_f/Tools/Trick', 1, tf(120, 0), tf(95, 1), (tf(112, 0), tf(82, 1)),
                      sound_path='game_assets_f/sounds/Lesh_laugh.wav', tag='Trick')

legend_button = Button('game_assets_f/Tools/Legend', 1, tf(394, 0), tf(44, 1), (tf(112, 0), tf(82, 1)),
                       sound_path='game_assets_f/sounds/button_click.wav')
available_tools = [candy_button]
tool_sprites.add([candy_button, fruit_button, money_button, trick_button, legend_button])

# Game Answer outcome
outcome = Outcome(X_sound_path='game_assets_f/sounds/wrong_sound.wav',
                  V_sound_path='game_assets_f/sounds/cheering_ppl.wav')

# Finish Screen: #######################################################################################################
finish_screen = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/finish_bg.png')
finish_buttons = pygame.sprite.Group()
finish_button = Button('game_assets_f/Buttons/quit_button', 1, tf(400, 0), tf(400, 1), (tf(215, 0), tf(162, 1)),
                       sound_path='game_assets_f/sounds/button_click.wav')
finish_buttons.add(finish_button)

# Legend Screen: #######################################################################################################
legend_screen = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/legend_bg.png')
legend_buttons = pygame.sprite.Group()
cont_button = Button('game_assets_f/Buttons/continue_button', 1, tf(400, 0), tf(500, 1), (tf(215, 0), tf(162, 1)),
                     sound_path='game_assets_f/sounds/button_click.wav')
legend_buttons.add(cont_button)
start_time = time.time()

# Phase-specific variables: ############################################################################################
bad_time = -8
knocked = False
last_talk_action = 0
done_talking_flag = 0
new_outcome = outcome
prev_screen = None
legend_const_action = 0
legend_last_talk_action = 0
visited_legend = False
################################################# GAME LOOP ############################################################
while running:
    core_surface.blit(curr_screen, (0, 0))
    # Main Menu Stuff
    if curr_screen == main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                for button in menu_sprites:
                    if button.coll_check(event.pos):
                        button.set_hovered()
                    else:
                        button.set_released()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.coll_check(event.pos):
                    quit_button.sound.play()
                    time.sleep(0.3)
                    running = False
                    pygame.quit()
                    sys.exit()
                elif play_button.coll_check(event.pos):
                    play_button.sound.play()
                    if not already_named:
                        curr_screen = name_screen
                        already_named = True
                    else:
                        curr_screen = level_0
        menu_sprites.draw(core_surface)
        menu_sprites.update()

    elif curr_screen == name_screen:
        if time.time() - bad_time > 0.5:
            bad_flag = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if n_res_button.coll_check(event.pos):
                    n_res_button.set_hovered()
                else:
                    n_res_button.set_released()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if n_res_button.coll_check(event.pos):
                    if len(user_name) >= 1:
                        n_res_button.sound.play()
                        npc.update_texts(player_name=user_name)
                        curr_screen = instruct_screen
                    else:
                        bad_flag = True
                        bad_time = time.time()
                        bad_sound.play()
                        break

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    user_name += event.unicode
        if bad_flag:
            color = color_bad
        elif active:
            color = color_active
        else:
            color = color_passive
        name_sprites.draw(core_surface)
        name_sprites.update()
        pygame.draw.rect(core_surface, color, text_input_rect)
        text_surface = basefont.render(user_name, True, (255, 255, 255))
        core_surface.blit(text_surface, (text_input_rect.x + 5, text_input_rect.y + 5))

    elif curr_screen == pause_screen:

        pygame.mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    p_res_button.set_hovered()
                    p_res_button.sound.play()
                elif event.key == pygame.K_l:
                    p_quit_button.set_hovered()
                    p_quit_button.sound.play()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_k:
                    p_res_button.set_released()
                    curr_screen = level_0
                    pygame.mixer.music.unpause()
                elif event.key == pygame.K_l:
                    p_quit_button.set_released()
                    running = False
                    pygame.quit()
                    sys.exit()

        pause_sprites.draw(core_surface)
        pause_sprites.update()

    elif curr_screen == instruct_screen:
        if prev_screen:
            pygame.mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    cont_button.sound.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_k:
                    start_time = time.time()
                    curr_screen = level_0
                    if prev_screen:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load("game_assets_f/sounds/game_theme_music.mp3")
                        pygame.mixer.music.set_volume(0.1)
                        pygame.mixer.music.play()

    # Game Screen Stuff
    elif curr_screen == level_0:
        if tut_phase == 0:
            knocked = knock_on_door(done_talking_flag == 3 and not knocked, knocked)
            if done_talking_flag == 3 and not knocked:
                door_button.set_hovered()
                knock_sound.play()
                knocked = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if npc.is_talking:
                    player.deltas = [0, 0]
                phase_0_if = done_talking_flag == 3 and not knocked
                msg_texts, last_talk_action = npc.npc_talk(msg_button, game_sprites, player, tut_phase,
                                                           [phase_0_if], [npc.resps["knock"]], event, next_button,
                                                           textfont)
                if done_talking_flag != 3:
                    done_talking_flag = last_talk_action
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        prev_screen = True
                        curr_screen = instruct_screen
                    if not npc.is_talking:
                        player.update_delts(event)
                    if event.key == pygame.K_k:
                        if not npc.is_talking and door_button.coll_check(player.rect.center) and not \
                                door_button.is_open and knocked:
                            knocked = False
                            door_button.is_open = True
                            door_button.sound.play()
                            curr_enemy = tut_enemies[tut_lvl]
                            tut_lvl += 1
                            game_enemy.add([curr_enemy])
                            enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))
                            tut_phase += 1
                            phase_0_if = False
                            if msg_button not in game_sprites:
                                game_sprites.add(msg_button)
                            break

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
            if time.time() - start_time > 2:
                update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                             text_sprites,
                             door_button)
            else:
                update_frame(player, None, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                             text_sprites,
                             door_button)

        elif 0 < tut_phase < 4 or 5 <= tut_phase <= 7:  # Before and After legend
            if tut_phase == 2 and fruit_button not in available_tools:
                available_tools.append(fruit_button)
            if tut_phase == 3 and money_button not in available_tools:
                available_tools.append(money_button)
            if tut_phase == 7 and trick_button not in available_tools:
                available_tools.append(trick_button)
            if time.time() - ts > 1 and not knocked:
                if tut_phase != 1:
                    knock_sound.play()
                knocked = True
            for event in pygame.event.get():
                if npc.is_talking:
                    player.deltas = [0, 0]

                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                cond = door_button.is_open and event.type == pygame.KEYDOWN and event.key == pygame.K_k \
                       and door_button.coll_check(player.rect.center)
                msg_texts, last_talk_action = npc.npc_talk(msg_button, game_sprites, player, tut_phase,
                                                           [new_outcome.wrong, new_outcome.right, not choice and cond],
                                                           [npc.resps['try'], npc.npc_good(), npc.resps["nothing"]],
                                                           event, next_button, textfont)
                if last_talk_action == 4:  # Finished responding
                    new_outcome.reset()
                    last_talk_action = 0
                    done_talking_flag = 0
                    npc.curr_response = None

                for button in tool_sprites:
                    if button in available_tools:
                        if door_button.is_open and button.coll_check(player.rect.center, x_offset=25, y_offset=25):
                            button.set_hovered()
                        else:
                            button.set_released()
                if door_button.coll_check(player.rect.center):
                    door_button.set_hovered()
                else:
                    door_button.set_released()
                if event.type == pygame.KEYDOWN:
                    if not npc.is_talking:
                        player.update_delts(event)
                    if event.key == pygame.K_ESCAPE:
                        prev_screen = True
                        curr_screen = instruct_screen

                    if event.key == pygame.K_k:
                        for button in tool_sprites:
                            if button in available_tools:
                                if door_button.is_open and \
                                        button.coll_check(player.rect.center, x_offset=25, y_offset=25):
                                    button.sound.play()
                                    if button.tag:
                                        choice = button.tag
                                    if choice is not None:
                                        player.change_sprite('game_assets_f/player_aux/player_{}.png'.format(choice))
                        if legend_button in available_tools and legend_button.coll_check(player.rect.center):
                            legend_button.sound.play()  # for hybrid, after legend is intro'd
                            curr_screen = legend_screen
                        if door_button.coll_check(player.rect.center):
                            if choice:
                                final_choice = choice
                                choice = None
                                player.change_sprite('game_assets_f/player/player.png')
                                new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                new_outcome.sound.play()
                                if new_outcome.right:
                                    game_enemy.remove([curr_enemy])
                                    door_button.is_open = not door_button.is_open
                                    ts = time.time()
                                    tut_phase += 1
                                    knocked = False
                                    if tut_phase == 8:
                                        sandbox_time = time.time()
                                        game_sprites.add(msg_button)
                                        # game_sprites.add(game_button) # Physical N button not really necessary
                                        last_talk_action, done_talking_flag = 0, 0
                                        break
                                    if tut_phase == 4:
                                        game_sprites.add(msg_button)
                                        available_tools.append(legend_button)
                                        break

                            elif not door_button.is_open and time.time() - ts > 1:
                                door_button.is_open = not door_button.is_open
                                door_button.sound.play()
                                if msg_button not in game_sprites:
                                    pop_sound.play()
                                    game_sprites.add(msg_button)
                                curr_enemy = tut_enemies[tut_lvl]
                                game_enemy.add([curr_enemy])
                                tut_lvl += 1
                                enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))

                    # if event.key == pygame.K_l:
                    #     msg_texts = npc_talk(npc, msg_button, game_sprites, player, tut_phase)

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
            update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                         text_sprites, door_button)


        elif tut_phase == 4:  # Legend
            door_button.set_released()
            for event in pygame.event.get():
                if legend_last_talk_action == 4:
                    tut_phase += 1
                    break
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                msg_texts, legend_last_talk_action = npc.npc_talk(msg_button, game_sprites, player, tut_phase,
                                                                  [legend_const_action == 3 and visited_legend],
                                                                  [npc.resps['legend']], event, next_button,
                                                                  textfont)
                if legend_const_action != 3:
                    legend_const_action = legend_last_talk_action
                if legend_button.coll_check(player.rect.center):
                    legend_button.set_hovered()
                else:
                    legend_button.set_released()
                if event.type == pygame.KEYDOWN:
                    if not npc.is_talking:
                        player.update_delts(event)
                    if event.key == pygame.K_ESCAPE:
                        prev_screen = True
                        curr_screen = instruct_screen
                    if event.key == pygame.K_k:
                        if legend_button.coll_check(player.rect.center):
                            legend_button.sound.play()
                            curr_screen = legend_screen
                    # if event.key == pygame.K_l:
                    #     msg_texts = npc_talk(npc, msg_button, game_sprites, player, tut_phase)

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
            update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                         text_sprites, door_button)

        elif tut_phase == 8:
            if time.time() - ts > 1 and not knocked:
                knock_sound.play()
                knocked = True

            for event in pygame.event.get():
                # nothing_cond = door_button.is_open and event.type == pygame.KEYDOWN and event.key == pygame.K_k \
                #                and door_button.coll_check(player.rect.center)
                ghost_cond = curr_enemy.title in ghost_opts and event.type == pygame.KEYDOWN and event.key == pygame.K_l \
                             and done_talking_flag == 3
                base_cond = curr_enemy.title in single_opts and event.type == pygame.KEYDOWN and event.key == pygame.K_l \
                            and done_talking_flag == 3
                hybrid_cond = curr_enemy.title not in single_opts and curr_enemy.title not in ghost_opts \
                              and event.type == pygame.KEYDOWN and event.key == pygame.K_l and done_talking_flag == 3
                msg_texts, last_talk_action = npc.npc_talk(msg_button, game_sprites, player, tut_phase,
                                                           [npc_flag, ghost_cond, base_cond,
                                                            hybrid_cond],
                                                           [npc.resps['done'], npc.resps["ghost"], npc.resps["base"],
                                                            npc.resps["hybrid"]],
                                                           event, next_button, textfont,
                                                           force_talk=done_talking_flag != 3)
                if last_talk_action == 3:
                    done_talking_flag = last_talk_action
                if last_talk_action == 4:  # Finished responding
                    new_outcome.reset()
                    last_talk_action = 0
                    npc.curr_response = None
                    if npc_flag:
                        FRIEND = npc.friend_name.replace(' ', '_')
                        game_sprites.remove(npc, msg_button)
                        if door_button.is_open:
                            game_enemy.remove([curr_enemy])
                            door_button.is_open = not door_button.is_open
                            knocked = False
                            choice = None
                        tut_phase = 10
                        tut_lvl = 0
                        all_game_time = time.time()
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load("game_assets_f/sounds/after_tut_music.mp3")
                        pygame.mixer.music.set_volume(0.1)
                        pygame.mixer.music.play()
                        break
                if npc.is_talking:
                    player.deltas = [0, 0]
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                for button in tool_sprites:
                    if button in available_tools:
                        if door_button.is_open and \
                                button.coll_check(player.rect.center, x_offset=25, y_offset=25):
                            button.set_hovered()
                        else:
                            button.set_released()
                if door_button.coll_check(player.rect.center):
                    door_button.set_hovered()
                else:
                    door_button.set_released()
                if npc.is_talking and event.type == pygame.MOUSEBUTTONDOWN and next_button.coll_check(event.pos):
                    sandbox_approaches += 0.5
                if event.type == pygame.KEYDOWN:
                    if not npc.is_talking:
                        player.update_delts(event)
                    if event.key == pygame.K_ESCAPE:
                        prev_screen = True
                        curr_screen = instruct_screen
                    if event.key == pygame.K_n:
                        npc_flag = True
                        sandbox_time = time.time() - sandbox_time
                        # break
                    if event.key == pygame.K_k:
                        for button in tool_sprites:
                            if button in available_tools:
                                if door_button.is_open and \
                                        button.coll_check(player.rect.center, x_offset=25, y_offset=25):
                                    button.sound.play()
                                    choice = button.tag
                                    if choice:
                                        player.change_sprite('game_assets_f/player_aux/player_{}.png'.format(choice))
                        if legend_button in available_tools and legend_button.coll_check(player.rect.center):
                            legend_button.sound.play()  # for hybrid, after legend is intro'd
                            curr_screen = legend_screen
                        if not npc.is_talking and door_button.coll_check(player.rect.center):
                            if choice:
                                final_choice = choice
                                choice = None
                                player.change_sprite('game_assets_f/player/player.png')
                                new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                new_outcome.sound.play()
                                if new_outcome.right:
                                    game_enemy.remove([curr_enemy])
                                    door_button.is_open = not door_button.is_open
                                    knocked = False
                                    tut_accumulative.append(round(time.time() - tut_ts, 2))  # For the learning curve
                                    ts = time.time()

                            elif not door_button.is_open and time.time() - ts > 1:
                                door_button.is_open = not door_button.is_open
                                door_button.sound.play()
                                curr_enemy_num = randrange(0, 28)
                                tut_ts = time.time()
                                curr_enemy = all_enemies[curr_enemy_num]
                                game_enemy.add(curr_enemy)
                                enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
                        sandbox_approaches += 0.5
                    if event.key == pygame.K_n:
                        next_button.set_released()
            update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                         text_sprites, door_button, done_talking_flag == 3 and not npc.is_talking)


        else:  # Not tutorial
            if time.time() - ts > 1 and not knocked:
                knock_sound.play()
                knocked = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                for button in tool_sprites:
                    if button in available_tools:
                        if door_button.is_open and button.coll_check(player.rect.center, x_offset=25, y_offset=25):
                            button.set_hovered()
                        else:
                            button.set_released()
                if door_button.coll_check(player.rect.center):
                    door_button.set_hovered()
                else:
                    door_button.set_released()
                if event.type == pygame.KEYDOWN:
                    player.update_delts(event)
                    if event.key == pygame.K_ESCAPE:
                        prev_screen = True
                        curr_screen = instruct_screen
                    if event.key == pygame.K_k:
                        for button in tool_sprites:
                            if button in available_tools:
                                if door_button.is_open and button.coll_check(player.rect.center, x_offset=25,
                                                                             y_offset=25):
                                    button.sound.play()
                                    choice = button.tag
                                    if choice:
                                        player.change_sprite('game_assets_f/player_aux/player_{}.png'.format(choice))
                        if legend_button in available_tools and legend_button.coll_check(player.rect.center):
                            legend_button.sound.play()  # for hybrid, after legend is intro'd
                            curr_screen = legend_screen
                        if door_button.coll_check(player.rect.center):  # TODO: Use Enemy coll check
                            if choice:
                                final_choice = choice
                                choice = None
                                player.change_sprite('game_assets_f/player/player.png')
                                new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                new_outcome.sound.play()
                                answered_correctly.append(new_outcome.right)
                                game_enemy.remove([curr_enemy])
                                door_button.is_open = not door_button.is_open
                                reaction_times.append(round(time.time() - perf_ts, 2))  # For the learning curve
                                ts = time.time()
                                knocked = False
                                if tut_lvl > len(game_enemies) - 1:
                                    curr_screen = finish_screen
                                    acc = accuracy(answered_correctly)
                                    times = avg_time(reaction_times)
                                    curr_score = score(answered_correctly, reaction_times)
                                    if curr_score > best_score:
                                        best_score = curr_score
                                    else:
                                        break
                                    break
                            elif not door_button.is_open and time.time() - ts > 1:
                                door_button.is_open = not door_button.is_open
                                door_button.sound.play()
                                curr_enemy = game_enemies[tut_lvl]
                                game_enemy.add([curr_enemy])
                                tut_lvl += 1
                                perf_ts = time.time()
                                enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))
                if event.type == pygame.KEYUP:
                    player.update_delts(event, down=False)

            update_frame(player, None, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                         text_sprites, door_button)

    elif curr_screen == legend_screen:
        visited_legend = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    curr_screen = level_0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_k:
                    cont_button.set_released()

    elif curr_screen == finish_screen:
        score_text = scorefont.render(str(curr_score), 1, (0, 0, 0))
        core_surface.blit(score_text, (400, 250))
        best_score_text = scorefont.render(str(best_score), 1, (0, 0, 0))
        core_surface.blit(best_score_text, (400, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    curr_screen = level_0
                    tut_phase = 10
                    tut_lvl = 0
                    all_game_time = time.time()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("game_assets_f/sounds/after_tut_music.mp3")
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.play()
                    answered_correctly = []
                    reaction_times = []
                    replays += 1
                    break

                if event.key == pygame.K_l:
                    report_performance_mail(acc, times, int(sandbox_approaches), tut_accumulative,
                                            answered_correctly, chosen_npc, FRIEND, best_score, replays)
                    finish_button.sound.play()
                    # time.sleep(0.2)
                    running = False
                    pygame.quit()
                    sys.exit()

    clock.tick()
    # print(clock.get_fps())
    pygame.display.update()  # TODO bad for perfomance, should keep a list of objects(rects/sprites) that are updated and only update them
