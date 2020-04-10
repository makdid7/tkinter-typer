import sys
from random import choice
from time import time
from tkinter import Entry, Button, Tk, Label

from easy_words import easy_words
from easy_words_est import easy_words_est
from hard_words import hard_words
from hard_words_est import hard_words_est
from medium_words import medium_words
from medium_words_est import medium_words_est

# TODO: separate scores_file for every difficulty and language
# TODO: make name restrictions (reason: commas in names mess up scores_file)
# TODO: add a pause / resume option
# TODO: add more estonian words

rand_words = easy_words + medium_words + hard_words
rand_words_est = easy_words_est + medium_words_est + hard_words_est

root = Tk()
root.title("SpeedTyping Game - Maksim Didenko's Creative Project")
root.geometry('500x500')
root['background'] = '#37474F'
root.resizable(False, False)
root.iconbitmap('AppIcon.ico')

# Difficulty choosing menu widgets:
dif_choose_lb = Label(text='\nChoose your difficulty:',
                      font=("Times New Roman", 20),
                      bg='#37474F',
                      fg='white')

easy_btn = Button(text='\nEasy',
                  font=("Times New Roman", 15),
                  command=lambda dif='easy': start_game(dif),
                  bg='#37474F',
                  fg='white')

easy_lb = Label(text='-- Short, 4-letter words',
                font=('Times New Roman', 14),
                bg='#37474F',
                fg='white')

medium_btn = Button(text='\nMedium',
                    font=("Times New Roman", 15),
                    command=lambda dif='med': start_game(dif),
                    bg='#37474F',
                    fg='white')

medium_lb = Label(text='-- Medium, 7-letter words',
                  font=("Times New Roman", 15),
                  bg='#37474F',
                  fg='white')

hard_btn = Button(text='\nHard',
                  font=("Times New Roman", 15),
                  command=lambda dif='hard': start_game(dif),
                  bg='#37474F',
                  fg='white')

hard_lb = Label(text='-- Long, 12+ letter words',
                font=('Times New Roman', 14),
                bg='#37474F',
                fg='white')

rand_btn = Button(text='\nRandom',
                  font=('Times New Roman', 15),
                  command=lambda dif='rand': start_game(dif),
                  bg='#37474F',
                  fg='white')

rand_lb = Label(text='-- Words with random length',
                font=('Times New Roman', 15),
                bg='#37474F',
                fg='white')

# Language choosing menu widgets:

welc_lb = Label(text='Welcome!',
                font=("Times New Roman", 30),
                bg='#37474F',
                fg='white')

choose_lang_lb = Label(text='Choose a language:',
                       font=('Times New Roman', 20),
                       bg='#37474F',
                       fg='white')

eng_btn = Button(text='\nEnglish',
                 font=('Times New Roman', 14),
                 command=lambda lang='eng': choose_difficulty_menu(
                     lang),
                 bg='#37474F',
                 fg='white')

eng_lb = Label(text='-- Type English words',
               font=('Times New Roman', 14),
               bg='#37474F',
               fg='white')

est_btn = Button(text='\nEesti keel',
                 font=('Times New Roman', 14),
                 command=lambda lang='est': choose_difficulty_menu(
                     lang),
                 bg='#37474F',
                 fg='white')

est_lb = Label(text='-- Trüki sõnu eesti keeles',
               font=('Times New Roman', 14),
               bg='#37474F',
               fg='white')

instructions = Label(text=(
    'How to play:\nType the word that will be shown\nthen press Enter!'),
    font=("Times New Roman", 15),
    bg='#37474F',
    fg='white',
    justify='left')

# Widgets for displaying countdown & average time:

countdown_lb = Label(font=("Times New Roman", 17),
                     bg='#37474F',
                     fg='white')

all_time_avg_lb = Label(font=("Times New Roman", 16),
                        bg='#37474F',
                        fg='white')

time_display = Label(font=("Times New Roman", 16),
                     bg='#37474F',
                     fg='white')
time_display.pack()

# Name requesting widgets:
name_lb = Label(text="What's your first name?",
                font=("Times New Roman", 17),
                bg='#37474F',
                fg='white')

name_ask_btn = Button(text='Save name',
                      font=("Times New Roman", 13),
                      command=lambda: show_leaderboard(name_ask.get()),
                      bg='#37474F',
                      fg='white')

name_ask = Entry(font=("Times New Roman", 17),
                 insertbackground='white',
                 bg='#37474F',
                 fg='white')

# Main game widgets:
user_input = Entry(font=("Times New Roman", 30),
                   bg='#37474F',
                   fg='white',
                   justify='center',
                   width=15,
                   insertbackground='white')

word_display = Label(font=("Times New Roman", 40),
                     bg='#37474F',
                     fg='white')

a = Label(text='\n\n\nYour word is...',
          font=("Times New Roman", 20),
          bg='#37474F',
          fg='white')

b = Label(text='Quickly, type it in!\n',
          font=("Times New Roman", 20),
          bg='#37474F',
          fg='white')

# Retrieving leaderboard:  # here
with open('scores_file.txt') as file:
    text = file.read()
    scores = text.split(' ')
    scores.pop()
    for i in range(len(scores)):
        scores[i] = scores[i].split(',')

# Assigning variables
last_10_times = []
all_times = []
first_time = True
wordCount = 0
countdown_time = 121  # here
all_time_avg = '--'


def show_leaderboard(name):
    name_lb.destroy()
    name_ask_btn.destroy()
    name_ask.destroy()

    if _lang == 'eng':
        if wordCount == 1:
            countdown_lb.config(text=(
                f'''\nTime is up!\n\nYou have typed 1 word.
                \nAverage time: {all_time_avg} seconds\n\nTop 5 scores:'''))
        else:
            countdown_lb.config(text=(
                f'''\nTime is up!\n\nYou have typed {wordCount} words.
                \nAverage time: {all_time_avg} seconds\n\nTop 5 scores:'''))

    elif _lang == 'est':
        if wordCount == 1:
            countdown_lb.config(text=(
                f'''\nAeg on läbi!\n\nTe trükisite 1 sõna.
                \nKeskmine aeg: {all_time_avg} sekundit\n\n5 Parimat:'''))
        else:
            countdown_lb.config(text=(
                f'''\nAeg on läbi!\n\nTe trükisite {wordCount} sõnu.
                \nKeskmine aeg: {all_time_avg} sekundit\n\n5 Parimat:'''))

    # Updating leaderboard:
    scores.append([name, wordCount])
    if len(scores) > 5:
        scores.sort(reverse=False, key=lambda data: int(data[1]))
        del scores[0]
    scores.sort(reverse=True, key=lambda data: int(data[1]))

    # Saving leaderboard to file:
    # here
    with open('scores_file.txt', 'w') as file:
        for i in scores:
            file.write(i[0] + ',' + str(i[1]) + ' ')

    # Displaying leaderboard and 'exit' button:
    y = 240
    for num, i in enumerate(scores, start=1):
        if _lang == 'eng':
            Label(text=(str(num) + '. ' + i[0] + ', ' + str(i[1]) + ' words'),
                  font=("Times New Roman", 16),
                  bg='#37474F',
                  fg='#f1c40f').place(x=150, y=y)

        elif _lang == 'est':
            Label(text=(str(num) + '. ' + i[0] + ', ' + str(i[1]) + ' sõnu'),
                  font=("Times New Roman", 16),
                  bg='#37474F',
                  fg='#f1c40f').place(x=150, y=y)
        y += 50

    Button(text='Exit',
           font=("Times New Roman", 14),
           width=10,
           command=lambda: sys.exit(),
           bg='#37474F',
           fg='#c0392b').place(x=350, y=430)


def game_end():
    global name_ask, name_ask_btn, name_lb, countdown_time
    root.unbind_all('<Return>')

    user_input.pack_forget()
    word_display.pack_forget()
    a.pack_forget()
    b.pack_forget()
    time_display.pack_forget()

    if _lang == 'eng':
        if wordCount == 0:
            countdown_lb.config(
                text="\nTime is up!\n\nYou didn't type any words.")
        elif wordCount == 1:
            countdown_lb.config(
                text='\nTime is up!\n\nYou have typed 1 word.')
        elif wordCount > 1:
            countdown_lb.config(
                text=f'\nTime is up!\n\nYou have typed {wordCount} words')

    elif _lang == 'est':
        name_lb.config(text="Mis on teie eesnimi?")
        name_ask_btn.config(text='Salvesta nimi')

        if wordCount == 0:
            countdown_lb.config(text='\nAeg on läbi!\n\nTe ei trükinud sõnu.')
        elif wordCount == 1:
            countdown_lb.config(text='\nAeg on läbi!\n\nTe trükisite 1 sõna.')
        elif wordCount > 1:
            countdown_lb.config(
                text=f'\nAeg on läbi!\n\nTe trükisite {wordCount} sõnu.')

    name_lb.place(x=140, y=270)
    name_ask.place(x=140, y=310)
    name_ask_btn.place(x=140, y=340)

    countdown_lb.pack(side='top')
    name_ask.focus()


def countdown():
    global countdown_time

    if countdown_time == 0:
        game_end()
        return

    countdown_time -= 1

    if _lang == 'eng':
        countdown_lb.config(text=f'{countdown_time} secs left\n')
    elif _lang == 'est':
        countdown_lb.config(text=f'{countdown_time} sekundit jäänud\n')

    countdown_lb.pack(side='bottom')

    root.after(1000, countdown)


def choose_language_menu():
    welc_lb.pack()
    choose_lang_lb.pack()
    eng_btn.place(x=120, y=140)
    eng_lb.place(x=190, y=165)
    est_btn.place(x=120, y=220)
    est_lb.place(x=210, y=245)
    instructions.place(x=40, y=400)


def choose_difficulty_menu(lang):
    global _lang
    _lang = lang

    welc_lb.destroy()
    choose_lang_lb.destroy()
    eng_btn.destroy()
    eng_lb.destroy()
    est_btn.destroy()
    est_lb.destroy()
    instructions.destroy()

    if lang == 'est':
        dif_choose_lb.config(text='\nVali raskus')

        easy_btn.config(text='\nLihtne')
        easy_lb.config(text='-- Lühikesed, 4-tähe sonad')

        medium_btn.config(text='\nKeskmine')
        medium_lb.config(text='-- 7-tähe sõnad')

        hard_btn.config(text='\nRaske')
        hard_lb.config(text='-- Pikad, 12+ täht sõnas')

        rand_btn.config(text='\nJuhuslik')
        rand_lb.config(text='-- Sõnad juhusliku pikkusega')

    dif_choose_lb.pack()
    easy_btn.place(x=120, y=130)
    easy_lb.place(x=188, y=160)
    medium_btn.place(x=120, y=210)
    medium_lb.place(x=215, y=238)
    hard_btn.place(x=120, y=290)
    hard_lb.place(x=185, y=316)
    rand_btn.place(x=120, y=370)
    rand_lb.place(x=215, y=394)


def hide_menus():
    welc_lb.destroy()
    dif_choose_lb.destroy()
    easy_btn.destroy()
    easy_lb.destroy()
    medium_btn.destroy()
    medium_lb.destroy()
    hard_btn.destroy()
    hard_lb.destroy()
    rand_btn.destroy()
    rand_lb.destroy()


def start_game(dif):
    global first_time, word, start_time, _dif, countdown_time
    _dif = dif

    hide_menus()

    if _lang == 'est':
        a.config(text='\n\n\nSõna on...')
    a.pack()

    try:
        if dif == 'easy' and _lang == 'eng':
            word = choice(easy_words)
            easy_words.remove(word)

        elif dif == 'easy' and _lang == 'est':
            word = choice(easy_words_est)
            easy_words_est.remove(word)

        elif dif == 'med' and _lang == 'eng':
            word = choice(medium_words)
            medium_words.remove(word)

        elif dif == 'med' and _lang == 'est':
            word = choice(medium_words_est)
            medium_words_est.remove(word)

        elif dif == 'hard' and _lang == 'eng':
            word = choice(hard_words)
            hard_words.remove(word)

        elif dif == 'hard' and _lang == 'est':
            word = choice(hard_words_est)
            hard_words_est.remove(word)

        elif dif == 'rand' and _lang == 'eng':
            word = choice(rand_words)
            rand_words.remove(word)

        elif dif == 'rand' and _lang == 'est':
            word = choice(rand_words_est)
            rand_words_est.remove(word)

    except IndexError:
        countdown_time = 0
        game_end()

    word_display.config(text=word)

    if first_time:
        countdown()

    first_time = False

    word_display.pack()
    start_time = time()

    if _lang == 'est':
        b.config(text='Kirjuta kiiresti!\n')
    b.pack()

    user_input.pack()
    user_input.focus()
    root.bind_all('<Return>', lambda event: check_input())


def check_input():
    global wordCount, all_time_avg

    if user_input.get() == word:
        finish_time = time()
        time_difference = round(finish_time - start_time, 3)

        all_times.append(time_difference)
        all_time_avg = round(sum(all_times) / len(all_times), 3)

        last_10_times.append(time_difference)
        if len(last_10_times) > 10:
            del last_10_times[0]
        avg_time = round(sum(last_10_times) / len(last_10_times), 3)

        if _lang == 'eng':
            time_display.config(
                text=f'Avg. time (last 10 words): {avg_time} seconds')
        elif _lang == 'est':
            time_display.config(
                text=f'Keskmine aeg (viimased 10 sõnu): {avg_time} sekundit')

        user_input.delete(0, 'end')
        user_input.pack_forget()
        word_display.pack_forget()
        a.pack_forget()
        b.pack_forget()

        wordCount += 1
        start_game(_dif)


choose_language_menu()

root.mainloop()

# Special letters:
# Õ õ
# Ü ü
# Ö ö
# Ä ä
