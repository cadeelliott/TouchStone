import os
from pathlib import Path
import platform
from playsound3 import playsound
import pygetwindow
import random
import shutil
import subprocess
from time import sleep

if platform.system() == 'Windows': #Sizes the terminal window so the text and ascii art is displayed properly on Windows
   win = pygetwindow.getWindowsWithTitle(str(shutil.which("py")))[0]
   win.size = (1200, 700)
   sleep(1)
elif platform.system() == 'Darwin': #Sizes the terminal window so the text and ascii art is displayed properly on Mac
   def resize_terminal(columns=100, rows=30):
      applescript = f'''
      tell application "Terminal"
         set bounds of front window to {{100, 100, {100 + columns*7}, {100 + rows*14}}}
      end tell
      '''
      subprocess.run(["osascript", "-e", applescript])

   resize_terminal(130, 33)

def beginGame(): #This is the game start function that displays the first "screen" the player should see
   if platform.system() == 'Darwin': #This clears out the initial text in the terminal window that is in the way of the game experience
      os.system("clear")
   #Welcome to
   print('                                           ___       __   __         ___    ___  __  \n                                     |  | |__  |    /  ` /  \\  |\\/| |__      |  /  \\ \n                                     |/\\| |___ |___ \\__, \\__/  |  | |___     |  \\__/ \n')
   #Invasion Crisis
   print('::::::.    :::.:::      .::.:::.     .::::::. :::    ...   :::.    :::.      .,-::::: :::::::..   ::: .::::::. ::: .::::::. ')
   print(';;;`;;;;,  `;;;\';;,   ,;;;\' ;;`;;   ;;;`    ` ;;; .;;;;;;;.`;;;;,  `;;;    ,;;;\'````\' ;;;;``;;;;  ;;;;;;`    ` ;;;;;;`    ` ')
   print('[[[  [[[[[. \'[[ \\[[  .[[/  ,[[ \'[[, \'[==/[[[[,[[[,[[     \\[[,[[[[[. \'[[    [[[         [[[,/[[[\'  [[[\'[==/[[[[,[[[\'[==/[[[[,')
   print('$$$  $$$ \"Y$c$$  Y$c.$$\"  c$$$cc$$$c         $$$$$$$,     $$$$$$ \"Y$c$$    $$$         $$$$$$c    $$$         $$$$         $')
   print('888  888    Y88   Y88P     888   888,88b    dP888\"888,_ _,88P888    Y88    `88bo,__,o, 888b \"88bo,888 88b    dP888 88b    dP')
   print('MMM  MMM     YM    MP      YMM   \"\"`  \"YMmMY" MMM  \"YMMMMMP\" MMM     YM      \"YUMMMMMP\"MMMM   \"W\" MMM  \"YMmMY\" MMM  \"YMmMY\" ')
   sleep(3)
   print('\nThere is an invasion happening and the last line of defense is all that is left...\n') #Lore
   sleep(3)
   print('Player 1, only one stronghold stands in the way of victory. \nAdvance your units through the upcoming 4 sections using any of the 3 trenches to win!\n') #Game instruction for Player 1
   sleep(3)
   print('Player 2, this is the final wave of the invasion. \nAnticipate Player 1\'s positioning and use your 2 ordinances per section to hold them off and win the war!\n') #Game instruction for Player 2
   sleep(7)

beginGame()

#Set variables to be accessed later
ordinance1Loc = 0
ordinanceCount = 1
troopCount = 3
trench1Count = 0
trench2Count = 0
trench3Count = 0

def secretBonus():
   print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣵⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡙⢛⡿⢿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣵⠟⢋⣤⣴⣿⣯⣿⡿⡿⠿⡿⡿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢻⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⠃⡼⢋⣴⢿⡿⢛⣯⢭⢾⣱⣾⢏⣌⢇⣞⣽⣟⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⡟⡐⠰⣿⣧⣾⣷⢧⣿⠏⣼⣷⣴⡍⡣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠘⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⡇⡇⣴⣿⣿⡿⠟⣿⣷⣾⡿⢿⣪⣬⣾⡿⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢺⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⠋⠁⢘⣿⣿⣿⣱⣿⡟⣿⣿⣳⢻⣿⢟⣯⣾⣿⡟⣿⡿⣫⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣄⠨⢨⠞⣴⢿⡟⣻⣿⢿⣿⣳⣿⣭⢿⣾⡿⣫⣶⣿⡾⣫⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⡇⢸⢿⣿⣾⣿⣿⠟⣱⣏⢘⠋⣅⡺⣁⣸⣿⣿⣿⣶⣿⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢻⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⡇⡟⣸⣿⣿⡿⠋⣘⣥⣶⣶⣶⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⢣⢃⡿⢋⡥⠞⠛⢛⣛⣉⣉⣩⣭⣭⣭⣭⡉⣉⣉⣉⠉⢭⣭⣍⠉⣍⡉⣩⣭⣍⣉⣭⣭⣭⣩⣉⣭⣙⠛⠛⠿⢿⣿⡇⢹⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⠏⠡⠸⠀⢊⠄⢀⣚⣿⣿⡿⠿⠿⠻⠿⢿⣿⣧⡈⠙⠿⠿⠀⠀⣿⡀⠘⡯⢀⣈⡻⠿⠿⠟⠻⠿⣿⣿⣿⣿⣿⡈⣆⠊⣷⡀⢻⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⠋⠐⢡⠖⢡⡎⣠⣿⣿⡏⢀⣠⣤⣤⣤⣤⣄⣀⣀⣀⣀⠄⠀⠀⢀⣇⣇⠀⠀⠉⢁⣤⣶⣶⣤⣴⣤⣤⣤⣀⠨⢽⡇⠸⡇⣿⣷⡝⢿⣿⣿⣿\n⣿⣿⣿⡿⠣⢊⣀⡩⠴⢋⣰⣿⣿⣿⡿⠟⢿⡉⢉⡀⠀⣀⣀⠀⡉⠙⠀⠀⠀⠈⣁⣙⠀⢠⣟⠀⢀⡉⢁⣀⡠⢈⠀⠊⠉⠓⣺⡇⢰⣧⠹⣿⣿⣿⣿⣿⣿\n⣿⣿⡟⠕⠘⢉⡄⠀⢰⣿⢻⣿⣹⣿⣿⣶⣾⠓⢀⡉⠒⠀⠒⠚⠃⢠⠴⠀⠀⠀⣿⡿⣷⣄⠹⠒⠈⠙⠒⠲⠒⠊⠡⢶⣶⣿⣿⡇⢺⡇⣰⣬⢙⠿⣿⣿⣿\n⣿⠋⣤⣽⠗⠀⢳⡀⠀⢢⠀⣿⣿⣿⣿⠋⣩⣥⣶⣶⣶⣦⡖⠂⢀⣠⣦⢀⡆⢤⣿⢣⣿⣿⣷⣦⣭⡓⠲⣶⣶⣶⣶⣶⣬⡙⣿⠇⠼⢁⣿⠇⣼⣿⣮⠻⣿\n⡏⡆⣿⠀⠀⠀⠈⢱⡀⠀⣅⠈⢿⣿⣷⠂⢿⣿⣿⣿⣿⠿⢿⣿⣿⣿⡏⣼⡀⢸⣿⢸⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣿⣿⣿⡷⠘⠀⢡⣟⡝⣰⣿⣿⣿⢧⢸\n⣇⠇⣏⠀⠀⠀⠀⠀⡧⠀⠈⠄⠨⣿⣯⣶⣄⠛⠟⢿⣿⣶⣿⣿⣻⣿⠀⣿⡇⠀⣿⡼⣿⣿⣿⣿⣍⣽⡭⠵⣿⣟⣿⣿⠟⣡⠂⢀⠎⡾⢠⣿⣿⣿⡿⠌⣼\n⣿⡄⠈⣇⡀⠀⠀⠀⢣⠘⠀⠘⡀⢹⣿⣿⣿⣶⣆⠀⠈⠻⣿⣿⣿⣿⠇⠘⠁⢀⣿⣷⣍⢻⣿⣿⣿⢟⣿⣿⠾⠓⠀⠀⠂⠀⠀⠎⣼⣁⣿⣿⣿⣿⠝⣴⣿\n⣿⣿⣆⡳⢿⣿⣦⡀⠈⢳⣀⠀⢡⠈⣿⣿⣿⣿⣿⣆⠈⠲⢆⣼⡿⠁⣼⡇⠀⣿⣿⣹⣿⠶⢻⡝⣿⡿⠘⢿⡴⠀⢠⣼⠇⠀⡘⢰⣿⣿⣿⣿⠟⣫⣾⣿⣿\n⣿⣿⣿⣿⣶⣭⣙⡻⠖⠀⠻⢷⡀⢣⠸⣿⣿⣿⣿⣿⡀⠀⣽⣿⡇⠀⠀⠀⠀⠛⠯⡛⡟⠉⠘⠇⣸⣷⡌⠺⣗⠄⣾⣿⠀⠀⠁⠿⢛⣛⣭⣴⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⠘⣷⠈⠆⢻⣿⣿⣿⣿⠀⠸⣿⣿⡇⠀⠈⠁⠀⠀⠀⢠⣿⣿⣷⣾⣿⣿⣧⠀⢿⣿⣿⠏⢀⠀⠘⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⡏⢇⠘⡈⣿⣿⣿⣿⠀⢰⣿⣿⣾⣆⠀⠀⠀⢰⢇⣟⢿⣿⣿⣿⣿⡟⢿⣇⢸⣿⡛⠀⠂⣴⡎⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣦⠀⢣⠘⣿⣿⠀⠀⣿⡿⠛⠋⠙⠛⡐⠂⢁⣼⣿⠘⣋⣉⡿⠛⠷⠈⣻⡄⢻⠁⠀⠰⡏⢰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣿⣿⣧⡀⠢⠸⡇⠀⢹⣶⣶⠿⠟⠀⠰⠁⢠⣿⣿⣿⣼⣿⣿⣿⣿⣶⣿⠿⠇⠀⡄⠀⡆⢀⣾⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣴⢀⣿⢿⣿⣿⣄⠀⠁⠒⠌⠫⠖⠀⠀⠀⠀⣠⣿⣿⣿⠋⠀⢀⣒⠒⠊⠋⢀⣤⠎⡜⠀⣼⠇⣿⣉⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⡏⢰⡿⠈⣿⡄⣿⣿⣿⣾⣄⠀⠠⠀⠀⠀⠀⠀⢐⡤⣽⣿⢣⣿⣿⣿⣿⣷⣦⣀⠘⠋⠘⢀⣴⣿⠀⠿⠇⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⠇⠸⣇⢁⠘⣇⢻⣿⣿⣿⣿⣑⠄⠀⠀⠀⡈⠐⣪⣼⣿⢡⣿⣿⣿⣿⣿⡿⠟⠉⠀⠀⣰⣿⣿⡜⠀⣴⣄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣏⠰⠀⣿⡄⢢⡈⢿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠒⣿⣿⣿⡏⡤⠙⠏⢀⠭⠙⠀⠀⠀⠀⣠⣿⣿⣻⠋⡀⢸⣿⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⡔⢄⠀⣿⠈⢷⡌⢍⣿⣿⣿⣿⣻⠚⠠⠀⣼⢿⣿⣿⠁⠀⣂⡒⠀⠀⠀⠀⠀⠀⣴⣿⣿⡟⣻⣷⡇⢸⣿⡇⣸⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠙⠀⡈⢿⣆⠁⠘⢿⡿⠋⠠⢀⣾⡏⡜⣿⡏⣰⣿⣿⢷⣤⡶⠀⠀⢀⣾⣿⣿⣿⣿⣿⡟⠀⣼⣿⠑⣸⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣷⡹⣇⠂⠀⢳⡈⢿⣿⣆⠐⠏⠀⢀⣝⣛⠋⢙⡈⠃⠛⠛⠛⠓⢋⣀⠢⠲⠟⢛⡛⢿⣿⡿⠉⠀⣼⣿⡟⡀⣽⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡍⢶⠰⠀⣇⢸⡏⢻⠂⠀⢐⠿⠿⠿⣟⢟⡿⢿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣛⠿⣷⢹⢁⢊⣼⣿⡿⠐⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡘⢧⡈⠻⢸⡇⣤⠁⠘⢂⡀⠀⡑⣌⡳⢮⣕⣈⡩⠟⠛⠻⢿⡿⠿⢿⣿⣷⣮⡸⣷⣿⣿⣿⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡠⡻⣦⡉⠇⢠⢀⡐⢸⠀⠀⠞⡛⠿⣟⢻⣿⣿⣿⣿⣷⣶⣶⣮⡀⠘⠻⣿⣷⡝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⢝⠿⣶⡌⠘⠀⠘⠀⠄⠀⠀⢠⣿⣷⣝⠿⠿⣿⣿⣿⣿⣿⣿⣆⠁⠨⢿⣯⡈⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡳⢾⡇⢸⣷⠀⠀⠀⠀⠈⠀⣿⣿⣿⣿⣷⣶⣶⣤⣬⣝⢻⣿⣆⢠⡂⠀⠳⠝⢘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⠡⡄⣿⣴⣆⠀⣄⢐⠀⠈⢹⣿⣿⡟⣿⣿⣿⢿⣿⣇⢻⣿⡇⣿⣿⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣷⣷⣶⡂⠀⣈⣿⠿⠟⡈⠿⠋⣾⣿⣿⠘⣿⣿⢘⣿⣿⣷⣭⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠨⡻⣦⡐⠀⢀⣬⣭⣽⡏⣤⡈⠿⠮⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣍⡙⠀⠈⣿⡿⢟⣥⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣥⣆⣤⣴⣾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿')

def tankImage(): #Icon for Player 2
   print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠠⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⡀⠠⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠊⠴⠨⢀⠠⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠤⠀⠠⠀⠀⠀⠼⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠛⠿⠿⠛⠿⠿⠿⢃⣀⣀⣀⣀⣀⣀⣀⠨⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⠛⠛⠛⠿⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⢤⣠⡠⢶⣶⡶⠂⠖⢀⣄⡀⡺⢿⣿⠿⣯⣿⣿⣄⠀⢉⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣶⣶⣶⣶⣶⣤⣤⣤⣤⣤⣄⣀⣀⣀⣀⡀⠀⠉⠀⠈⠐⠈⠉⠀⠀⠀⠐⡚⣿⣽⠺⣟⡎⣿⣾⡸⣯⢭⣿⣄⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠳⢮⣵⣿⡿⣦⣹⣿⣟⣿⣲⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⠶⡆⢈⠛⠋⠁⠘⠁⠀⠈⠛⠻⠿⠟⠻⡛⠛⠛⠻⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⣩⠍⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡤⡤⣠⡔⠠⠀⠈⠤⠄⠰⠁⢀⡠⣀⣴⠖⠀⠀⠀⠀⢀⣠⠀⢸⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠈⠀⢀⣤⣀⣀⡀⢀⣈⠓⠀⣠⣶⣿⣾⣿⠇⠈⠁⢀⡡⣄⡠⠶⠿⠿⣎⣹⣿⣽⠤⣀⠀⠀⠀⠀⠐⢶⣿⣿⣿\n⣿⣿⡿⠛⢛⣛⣛⡛⠛⠉⠀⠀⠂⠀⠀⠀⡀⠤⠿⡿⣛⣛⣛⠟⠃⠡⠾⢛⡋⠍⣁⣠⠆⠠⠀⠠⢿⢟⣻⠻⠟⠛⠀⠀⠉⠉⠁⠀⠀⠀⠀⠐⠀⠀⠉⠉⣙\n⣿⠟⣤⣿⣿⣿⡟⠁⠀⠀⠴⠀⠀⢠⠦⠄⠀⠼⠀⠀⢡⠈⠉⠀⣰⣿⣿⣿⣷⣿⠏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡐⠀⢀⢀⡀⠄⠀⠘\n⣯⣤⠌⠉⠉⠉⠀⠀⣀⣾⣿⣶⣤⣤⣤⣤⣤⣀⣄⣀⣀⣀⡀⠾⠿⠿⠿⠿⠿⠁⠀⠀⠐⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠠⠀⠉⠀⢠⠀⠀⠀⠂⠀⠀⠈⠀⠀\n⣿⣿⠀⠀⡀⠀⠀⠀⠀⠀⠀⠰⠤⠤⡄⢤⢨⠬⠭⠍⠎⢭⣉⡁⠀⠀⠀⠀⠀⠀⣀⠀⠀⠈⠁⠀⠀⠀⡀⢀⡀⠀⠀⠀⢠⡄⠀⠀⣲⠄⠠⡁⠃⠀⠀⠀⢀\n⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠀⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⡍⠀⠀⡆⢨⡇⠀⠀⡆⠘⠃⠀⠀⠀⠘⠁⠀⠀⠀⠀⡆⠁⠀⠀⠀⢠⣿\n⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠃⠀⠃⠁⠀⠀⡀⠀⠘⢀⡄⠀⠘⠴⠞⠀⠀⠁⣀⣴⣿⣿\n⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⠣⠴⠂⠀⠀⠁⠋⠀⠀⣀⣀⣀⣤⣴⣴⣶⣶⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣶⣾⣶⣶⣶⣶⣶⣶⣶⣦⣦⣀⣄⣀⣀⣀⣠⣤⣤⣴⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n')

def tankImageNegative(): #Old image version, currently not in use
   print('   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣟⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⢿⣟⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣵⣋⣗⡿⣟⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣛⣿⣟⣿⣿⣿⣃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣤⣀⣀⣤⣀⣀⣀⡼⠿⠿⠿⠿⠿⠿⠿⣗⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n   ⣶⣶⣤⣤⣤⣤⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡛⠟⢟⡉⠉⢉⣽⣩⡿⠻⢿⢅⡀⠀⣀⠐⠀⠀⠻⣿⡶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n   ⠀⠀⠉⠉⠉⠉⠉⠉⠛⠛⠛⠛⠛⠻⠿⠿⠿⠿⢿⣿⣶⣿⣷⣯⣷⣶⣿⣿⣿⣯⢥⠀⠂⣅⠠⢱⠀⠁⢇⠐⡒⠀⠻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣌⡑⠊⠀⢀⠙⠆⠀⠠⠀⠍⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⣉⢹⡷⣤⣴⣾⣧⣾⣿⣷⣤⣄⣀⣠⣄⢤⣤⣤⣄⠀⠀⠀\n   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠖⣲⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢛⢛⠟⢫⣟⣿⣷⣛⣻⣏⣾⡿⢟⠿⠋⣩⣿⣿⣿⣿⡿⠟⣿⡇⠀⠀\n   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣷⣿⡿⠛⠿⠿⢿⡿⠷⣬⣿⠟⠉⠀⠁⠀⣸⣷⣾⡿⢞⠻⢟⣉⣀⣀⠱⠆⠀⠂⣛⠿⣿⣿⣿⣿⣯⡉⠀⠀⠀\n   ⠀⠀⠀⠀⠀⢀⣤⡤⠤⠤⢤⣤⣶⣿⣿⣽⣿⣿⣿⢿⣛⣀⢀⠤⠤⠤⣠⣼⣞⣁⡤⢴⣲⠾⠟⣹⣟⣿⣟⡀⡠⠄⣄⣠⣤⣿⣿⣶⣶⣾⣿⣿⣿⣿⣯⣿⣿⣶⣶⠦\n   ⠀⠀⠀⠀⣠⠛⠀⠀⠀⢠⣾⣿⣿⣋⣿⣿⡟⣙⣻⣿⣃⣿⣿⡞⣷⣶⣿⠏⠀⠀⠀⠈⠀⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢯⣿⡿⡿⢿⣻⣿⣧\n   ⠀⠀⠀⠐⠛⣳⣶⣶⣶⣿⣿⠿⠁⠀⠉⠛⠛⠛⠛⠛⠿⠻⠿⠿⠿⢿⣁⣀⣀⣀⣀⣀⣾⣿⣿⣯⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣟⣿⣶⣿⡟⣿⣿⣿⣽⣿⣿⣷⣿⣿\n   ⠀⠀⠀⠀⠀⣿⣿⢿⣿⣿⣿⣿⣿⣿⣏⣛⣛⢻⡛⡗⣓⣒⣲⣱⡒⠶⢾⣿⣿⣿⣿⣿⣿⠿⣿⣿⣷⣾⣿⣿⣿⢿⡿⢿⣿⣿⣿⡟⢻⣿⣿⠍⣻⣟⢾⣼⣿⣿⣿⡿\n   ⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣷⣿⣾⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⢲⣿⣿⢹⡗⢸⣿⣿⢹⣧⣼⣿⣿⣿⣧⣾⣿⣿⣿⣿⢹⣾⣿⣿⣿⡟⠀\n   ⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣼⣿⣼⣾⣿⣿⢿⣿⣧⡿⢻⣿⣧⣋⣡⣿⣿⣾⠿⠋⠀⠀\n   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢷⣜⣋⣽⣿⣿⣾⣴⣿⣿⠿⠿⠿⠛⠋⠋⠉⠉⠀⠀⠀⠀⠀⠀\n   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⠉⠁⠉⠉⠉⠉⠉⠉⠉⠙⠙⠿⠻⠿⠿⠿⠟⠛⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')

def tankDestroyedImage(): #Player 1 Victory/Player 2 Loss icon
   print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣊⣒⠀⠍⠈⠐⠁⠈⠐⠩⠀⠺⢟⣿⣿⣿⣛⢟⡻⠑⡄⠀⠈⠠⠰⠞⡙⡧⢹\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠐⠄⠰⠀⠈⢀⠀⠠⠠⠂⠠⢃⣿⢿⢿⢭⢰⢠⠀⢀⡂⠀⡆⠀⠀⠀⠈⠏⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡽⠬⠀⠀⢀⠂⠀⠀⠀⠠⠀⠀⠐⢀⢧⣻⡼⢎⢂⠁⠁⠀⠀⠀⢘⠀⢀⢠⢀⣼⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣧⡠⠀⠄⣂⠀⠀⠀⠀⠀⠠⢀⠀⠘⣿⣿⣷⣽⠌⠠⠠⠄⢀⠀⠁⡠⢔⠱⣽⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⡝⢰⡿⢸⠶⠤⠀⠀⠀⠀⠀⠐⠀⢸⣿⣿⣿⢵⡿⠃⠀⠀⠑⠀⡡⠔⣶⣞⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠛⠭⠭⠈⠄⠁⠈⢀⣀⣀⣀⣀⣀⣀⣀⠨⢹⣿⣿⣿⠑⠀⢥⡄⠠⢀⠀⢠⡺⣿⣽⣿⣿⣿\n⣻⣿⣿⡿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⢤⣠⡠⢶⣶⡶⠂⠖⢀⣄⡀⡺⢿⣿⠿⣯⣿⣿⣄⠀⢉⣽⣟⣾⠋⠀⠀⠃⠀⠤⢨⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣟⣿⡯⠏⠉⠀⠈⠐⠈⠉⠀⠀⠀⠐⡚⣿⣽⠺⣟⡎⣿⣾⡸⣯⢭⣿⣄⠘⡿⡯⡖⠀⢂⢀⠀⠀⢀⣺⠋⢻⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠉⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠳⢮⣵⣿⡿⣦⣹⣿⣟⣿⣲⠱⡻⢣⠀⠈⠀⠀⠀⢀⠂⣠⣸⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠀⠀⣀⣤⣴⣶⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⠶⡆⢈⠛⠋⠁⠘⠁⠀⠀⠊⠀⠨⠁⠘⠐⠚⠛⠻⣿⣿⣿\n⣿⣿⠿⠟⠋⠁⠀⢀⣀⣠⣤⣶⣿⣿⠿⠛⣩⠍⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡤⡤⣠⡔⠠⠀⠈⠤⠄⠰⠁⢀⡠⣀⣴⠖⠀⠀⠀⠀⢀⣠⠀⢸⣿⣿\n⠁⢀⣠⣤⣶⣶⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠈⠀⢀⣤⣀⣀⡀⢀⣈⠓⠀⣠⣶⣿⣾⣿⠇⠈⠁⢀⡡⣄⡠⠶⠿⠿⣎⣹⣿⣽⠤⣀⠀⠀⠀⠀⠐⢶⣿⣿⣿\n⣿⣿⡿⠛⢛⣛⣛⡛⠛⠉⠀⠀⠂⠀⠀⠀⡀⠤⠿⡿⣛⣛⣛⠟⠃⠡⠾⢛⡋⠍⣁⣠⠆⠠⠀⠠⢿⢟⣻⠻⠟⠛⠀⠀⠉⠉⠁⠀⠀⠀⠀⠐⠀⠀⠉⠉⣙\n⣿⠟⣤⣿⣿⣿⡟⠁⠀⠀⠴⠀⠀⢠⠦⠄⠀⠼⠀⠀⢡⠈⠉⠀⣰⣿⣿⣿⣷⣿⠏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡐⠀⢀⢀⡀⠄⠀⠘\n⣯⣤⠌⠉⠉⠉⠀⠀⣀⣾⣿⣶⣤⣤⣤⣤⣤⣀⣄⣀⣀⣀⡀⠾⠿⠿⠿⠿⠿⠁⠀⠀⠐⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠠⠀⠉⠀⢠⠀⠀⠀⠂⠀⠀⠈⠀⠀\n⣿⣿⠀⠀⡀⠀⠀⠀⠀⠀⠀⠰⠤⠤⡄⢤⢨⠬⠭⠍⠎⢭⣉⡁⠀⠀⠀⠀⠀⠀⣀⠀⠀⠈⠁⠀⠀⠀⡀⢀⡀⠀⠀⠀⢠⡄⠀⠀⣲⠄⠠⡁⠃⠀⠀⠀⢀\n⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠀⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⡍⠀⠀⡆⢨⡇⠀⠀⡆⠘⠃⠀⠀⠀⠘⠁⠀⠀⠀⠀⡆⠁⠀⠀⠀⢠⣿\n⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠃⠀⠃⠁⠀⠀⡀⠀⠘⢀⡄⠀⠘⠴⠞⠀⠀⠁⣀⣴⣿⣿\n⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⠣⠴⠂⠀⠀⠁⠋⠀⠀⣀⣀⣀⣤⣴⣴⣶⣶⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣶⣾⣶⣶⣶⣶⣶⣶⣶⣦⣦⣀⣄⣀⣀⣀⣠⣤⣤⣴⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n')

def soldierImage(): #Player 1 icon
   print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢛⣩⣭⣭⡍⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⡟⢠⣾⣿⡿⠛⣩⣴⣾⣿⣦⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⡿⢁⣼⣿⡯⠉⠛⠋⣠⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠉⢻⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⠀⣀⣀⣀⣉⠙⠋⣁⣾⣿⣿⠿⢃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠃⠀⠀⠘⣿⡿⠿⠿⠛⠛⠙\n⣿⣿⣿⣿⣿⣿⣿⣿⠀⢿⣿⣿⣿⡿⠿⠛⢋⡭⣶⠀⠛⠛⠛⣉⣉⣭⣥⠉⠿⠿⠛⠋⢉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣶⣶⣶⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠉⠉⠀⢀⣠⡄⠚⢛⡈⠀⠀⢰⣛⣛⣫⣭⣤⠶⠚⠁⡄⡄⣾⠀⣿⠀⠀⠀⠀⠀⠸⣿⣶⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⠖⠀⠀⠙⢛⢛⣛⢩⣿⣶⣶⣿⡏⠉⠉⠀⠀⠀⢀⠀⡇⣿⣸⣤⣇⠀⣶⣿⣿⠆⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⠿⠋⠁⣴⣶⣾⣿⣿⡆⠛⠋⠀⠙⠛⠛⠛⠋⠁⠀⠀⠀⠀⢿⣇⠻⣿⣿⣟⠱⢰⣿⣿⡟⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⠿⢃⠀⠀⠀⠈⠉⠉⠀⠀⠀⢀⣴⣥⣴⡶⢞⣋⡅⠀⢤⣴⡆⡆⢫⡙⠀⠺⠿⠟⠀⠙⣿⣿⠃⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⡿⠃⠀⣿⣀⡄⠀⠀⠀⠀⠀⢠⣾⡿⢻⣿⠈⣿⣿⡭⠄⠀⠀⢻⣿⡰⡈⢿⠂⠀⠐⠾⠂⣤⠸⡟⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⠃⣴⣿⣿⣿⡇⠀⣠⣴⣶⠰⡄⢻⡇⠿⠿⠇⠙⠛⣓⣀⠶⠄⠈⢿⣧⡳⠈⣼⣷⣤⡰⣾⣿⡇⠁⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⡿⢰⣿⣿⠟⣡⣶⣿⣿⣿⣿⣧⠹⡄⠀⢴⣶⣠⣦⣼⣿⣏⠀⡆⠀⢈⣩⣴⣾⣿⣿⣿⣧⣿⣸⡇⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⡇⢸⡿⢃⣾⣿⣿⣿⣿⣿⣿⠿⠓⣀⠀⠹⣿⡿⣿⣿⣿⣿⠀⠀⠀⠀⠉⢹⣿⣿⣿⣿⣿⡿⠹⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⠃⣼⣿⣿⣿⣿⣿⣿⣿⠏⡀⢸⣿⣿⣧⠀⢹⣿⣬⣍⠉⠡⠐⠀⠀⠀⠀⠈⢛⣛⣭⣭⣴⣶⣾⡇⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣧⠐⣿⣿⣿⣿⣿⣿⠟⠁⠚⠁⠈⣿⣿⣿⣷⡀⢠⣤⣶⣶⣿⣷⣶⡆⠀⠀⠀⠘⣿⣿⣿⣿⣿⡿⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣦⣌⣙⡻⠿⠟⡁⠀⣿⣿⡇⢻⣿⣿⣿⣿⣷⡄⠹⣿⠿⠿⠿⠟⠃⠀⠸⠿⠓⠸⠿⣿⣿⣿⠇⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⠿⠟⣋⣥⠤⠘⣛⣋⢸⣿⣿⣿⣿⣿⣿⣄⠹⣾⣿⣿⣿⠀⢀⣤⡈⠿⣿⣷⢸⣿⡟⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⡏⢰⣿⠿⢃⣀⡀⠻⣿⡎⣿⣿⣿⣿⣿⣿⣿⣦⠘⠋⠉⠒⣀⣸⣿⢟⠂⣟⣛⢸⡟⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣷⡄⢡⣾⣿⣿⣿⣆⠉⠀⠙⣛⣛⣉⠉⠛⠛⠛⠓⣦⠐⣦⣍⣛⠗⠹⢃⣿⡏⠚⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⡇⢸⠀⠹⡿⠟⣋⣤⡙⢿⣿⡿⠟⠁⠀⠀⠀⣀⠛⠀⣿⣿⡇⣙⣀⣈⡉⢠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣧⠀⢦⣀⠀⠰⡿⠿⠇⠀⠰⠞⠻⢀⡀⠻⣿⣿⣠⣷⠌⠛⣁⣉⢉⠉⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣧⡈⠿⣷⡄⠿⠿⢦⠄⠀⠛⢿⣿⣿⢀⣿⣿⣿⠁⢰⣾⠟⢃⣼⣿⠌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣴⣿⠋⣴⡆⣦⣼⣿⣿⠈⣩⣤⣾⣷⠀⣡⣾⣿⣿⡅⢛⠷⣬⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣷⢹⣿⣿⣿⡄⢻⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣉⣛⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n')

def p1LImage(): #Player 2 Victory/Player 1 Loss icon (Thousand Yard Stare)
   print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠄⡀⠘⠂⠅⠌⠛⠛⠿⠿⠿⣿⣿⣷⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠗⣿⠀⠀⡿⣻⠁⢈⣼⣻⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠤⠃⠓⢈⠑⢂⠀⠀⠀⠀⠀⠈⠙⣋⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡛⠿⡶⠰⣹⣿⠉⣿⣿⢿⣟⡿⠿⠿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠒⢿⣼⣷⡒⠄⠨⠜⠀⠀⠀⠀⡀⢱⠈⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢸⡇⣠⢟⢋⢠⣿⢟⢈⣿⡽⣻⡟\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠗⢼⠚⣉⣵⣣⠖⣡⢫⠐⠁⢀⢃⠄⠆⠄⢠⢻⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⠀⢈⡗⠽⠀⢠⠏⠁⠆⠉⣙⢨⠰⠶\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢧⠄⠄⠃⢠⡿⠺⡛⢱⠁⠆⠈⠀⣨⠂⠀⠸⠀⠀⠁⠉⢸⠻⣯⣿⣿⣯⣷⣮⣿⣿⣿⣿⣿⣿⣿⣿⢫⠞⠽⣻⡿⠏⠁⠀⠂⠀⣰⡏⠀⣼⠅⢀⠂⡈⠔⡠\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⡛⢿⣿⠏⠀⢀⠎⠀⠈⣴⡏⡆⡏⣶⠶⢀⠜⣁⢡⠞⢃⠀⠀⢀⣴⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢧⠊⠀⡄⠀⠤⢌⠠⠀⠁⠙⠀⣠⡟⠀⡂⠜⠉⠈⠀\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣻⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢛⡉⡴⣣⣬⣜⠉⠀⠠⠠⢖⣀⢀⡿⢼⣱⠀⠥⣂⠐⢒⡁⣤⠏⢀⠀⠤⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣀⣡⣈⣾⣿⣿⣿⣯⠀⠘⣤⣴⡀⠄⠀⣠⢴⠄\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢃⡾⠃⠋⠀⠒⢳⣽⠿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⠃⡔⢸⡕⣿⢿⢻⡇⢸⠔⢀⠺⠀⣾⢃⠂⣴⡯⡀⠁⠸⢉⢉⠁⡱⢤⢘⣰⣿⣿⣿⣿⣿⢏⠣⢘⠘⠮⣝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠈⠹⠀⠀⠄⡀⠾⠴\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣠⢿⡶⣶⠄⠀⢶⣛⢿⣷⣸⣿⣿⣿⣿⣿⠇⣾⣛⡽⠀⢛⣴⠃⢻⠈⢸⣿⠀⡹⡼⢀⠈⠛⣠⢈⡌⢉⢷⢎⢞⢩⣋⠖⡈⢒⡶⣹⣾⣿⣿⣿⣿⢊⡅⢲⣌⢳⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠒⠃⡸⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣹⠇⣿⡇⡟⢠⣅⡾⢡⣉⠿⣇⡿⣿⣿⡟⠀⠄⢰⡏⣀⠀⢺⣌⣠⣶⢸⠈⡞⠀⠀⢧⠋⡔⢸⣓⣄⣠⣌⠞⣨⠖⡟⢀⢊⠜⢡⠐⣹⣿⣿⣿⣿⣧⣏⡜⡡⣞⣽⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠤⡤⠉⡽\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢡⣼⡟⣸⡁⣄⠊⢁⣯⣮⠟⢤⠀⠸⠟⡃⡞⣠⠿⢰⣇⡀⣼⣹⢫⣟⣼⠲⢁⠀⡐⠊⠠⡀⠞⢉⣼⡿⡽⢫⠃⢀⠠⢁⠂⡄⢃⡂⢹⣛⣿⣿⣿⡷⣚⠴⡱⢮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⣴⠁⢸⠢⣜⢎⡕\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡘⣸⣹⠛⣅⡰⢣⢶⣋⣈⣡⠁⠈⡎⠀⠀⠘⠠⠏⠀⣾⣿⡟⢿⢻⢸⣯⣧⣿⣿⠇⠀⠡⠌⡀⡜⢺⡟⡥⡱⡁⡐⠈⠄⠁⡙⠄⡞⡐⠦⣓⣞⣿⣿⢿⡘⣜⡱⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⡀⠤⠾⠙⢩⠄\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣥⠐⣏⣿⢳⡜⡱⣲⠋⣱⣅⣹⠒⡀⠸⠄⢰⠭⠿⣿⠃⣴⡿⢯⠁⠁⣤⣷⠺⣶⣤⣾⣻⡤⠀⠘⢰⠡⣏⢔⠚⢁⠰⢀⠍⡀⠆⠀⡘⡜⠥⠓⡀⠎⠼⡹⢯⣛⠶⡱⣏⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣀⡶⢈⡿⠴⢦⡂⣀\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡯⡗⡀⢉⣻⠸⣷⡽⢫⣭⡽⠎⣿⠀⢋⠆⠄⠠⡌⠔⢿⡇⢸⢿⣵⠋⠎⣽⡟⡱⠚⢬⠟⢫⠞⡄⢘⢃⡜⠀⡀⠘⣠⠁⢊⡜⡠⠀⡔⠐⠈⠁⡀⠌⠘⠠⠑⡈⠡⢻⣕⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢠⠏⠁⠀⠜⠋⢶⣔⡈\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣀⡜⠈⡠⣅⡞⣷⣬⡟⠄⢑⣺⣌⣡⠹⠀⢇⡂⢤⣡⠝⣰⡀⢜⠈⣰⠟⣵⣿⣿⣿⣳⢼⣭⣾⣥⠂⢠⡋⢆⣈⠒⠀⠔⠁⡋⡞⢰⢁⠠⡀⠤⠐⢀⠠⢁⢄⡐⠀⠁⠂⢄⢻⣿⡳⣟⣻⢿⣻⣏⠿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡄⡀⠂⠀⠀⠈⢲⢽⡥\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⡾⣾⣿⣿⣿⣿⣿⣿⡿⠛⣿⣿⣿⣿⠅⣩⢬⢇⠢⢄⣣⡎⣽⣶⣿⣳⠃⢤⡘⡿⠿⡧⡄⢨⣶⢸⣻⢏⣰⡷⠄⢠⣡⣌⠁⡼⠛⠟⠯⢾⡟⣾⢏⡴⢋⡀⠠⢄⣂⣌⣤⣥⣷⣶⣶⣶⣶⣶⣤⣭⣂⣱⠊⠀⠌⠕⠪⠔⣠⣤⢻⠱⣭⠎⢃⠧⡘⠳⡜⣻⣟⣿⢿⣿⣿⣿⣿⣿⣿⡟⣇⡄⠀⡀⡀⣠⠼⡮⠄⠀\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣣⠄⠀⢹⡿⠏⠀⣧⣼⣾⣷⣊⣽⣯⡿⠛⢳⣿⣿⣦⣿⣤⢇⣳⡷⣬⣟⣯⡭⣞⣫⠁⣀⣿⣻⡿⠐⢠⠸⢑⢋⣂⣽⡉⠾⣛⣥⣶⣿⣿⣿⣿⣿⣿⡿⠿⠿⠻⠿⠿⠿⠿⣿⣿⣿⣿⣶⣬⣂⢝⣲⣿⣷⣙⡐⠈⠆⢌⡑⠣⢌⡑⢎⣿⣏⣽⣿⣿⣿⡿⢏⣐⣣⠄⠂⠰⢃⠐⣀⢢⡶⡼\n⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣍⠡⠠⢀⠔⣥⣿⢛⡮⡝⣿⣟⡽⣼⣿⣿⣸⣿⣿⡿⠓⢫⣀⢈⠣⢀⢛⣽⠃⠃⠀⣹⢿⢐⡛⣁⣦⡺⠞⢁⣮⣵⣿⣿⣿⣿⡟⠋⠉⠂⠁⠀⠀⠀⠀⠀⠀⠁⠂⠀⠈⠻⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣷⣌⡀⠠⠁⠂⡜⢢⣼⣿⣿⣿⣿⣿⣿⣏⡾⣣⡍⢀⡇⢆⠞⢭⣞⡧⡏\n⠋⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢾⣿⣋⢭⢾⣻⡵⣟⢷⣿⠛⣱⣿⣿⣻⠇⣴⣦⣬⣥⣶⣶⣿⣿⣽⡟⢄⠢⠙⣀⠛⡛⢛⣩⣽⣿⣿⡿⠿⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠹⣳⡄⠠⢉⠻⠿⣿⣿⣿⣿⣿⡇⠄⠂⠰⢈⠷⣿⣿⣿⣿⠿⣉⣻⣼⡟⢭⣌⠸⠁⠁⡐⡾⢻⠔⡣\n⢂⠠⢘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢠⣾⣿⣽⣏⠘⢙⣦⣿⣿⣴⣾⣿⡿⣉⣷⠿⣟⣓⡿⣹⠟⣋⣩⣷⡏⢄⠈⡆⡑⡻⣰⢟⣾⣿⣿⡟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡛⠂⠀⠀⠀⠈⠈⠻⣿⡻⣿⡼⠬⢄⠱⡈⠼⣯⢿⣿⣿⣷⣬⡭⢋⠲⠨⠍⠊⠴⠀⠙⠣⢂⡀⣁\n⢀⡢⣳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⡇⠿⢿⢷⣷⣳⣿⢯⢆⡉⣿⢁⣿⠿⣽⠿⣴⣥⣿⡿⣳⣿⢦⣽⣿⢦⣰⣿⣿⠟⠁⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣖⠡⢉⠀⢂⡜⣽⢯⣿⣿⣿⣿⣿⣭⡅⠋⠂⠀⢀⠀⢀⠀⠀⡼⠋⠉\n⣠⠶⣍⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢰⣀⣿⣿⣿⣿⣷⣦⣻⣴⣿⣿⣠⣾⣿⡻⢿⣿⣋⣽⣋⣵⢿⣿⡧⣶⣿⢏⠂⡀⠀⠀⠀⠁⠀⠀⠀⠀⠠⠀⠀⠁⠠⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣆⢂⠘⢠⠘⣯⣿⣼⣿⣿⣿⣿⡧⣘⠂⣁⠂⢠⢂⠀⡀⠛⠀⢠⡔\n⢼⢿⣖⣦⢭⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣿⣿⣿⣿⣟⣼⣿⣿⣱⣚⣯⣿⡻⢿⣽⣴⣿⠞⡛⢸⢸⣥⡿⢿⣏⡿⢅⠊⠀⠀⠀⠀⠀⠀⠀⠀⡀⠂⠀⢈⠐⡀⢀⠀⠀⠠⠀⡀⠄⠠⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⠊⢤⢛⣲⣿⣿⣿⣿⣿⣿⠴⣃⣞⣤⣫⣿⠰⡆⣸⣞⣣⣦⣜\n⣾⣷⡇⠙⠊⠚⡿⡿⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣾⣷⣿⣿⣷⣤⣝⣱⠟⠀⢢⢁⡰⢻⣘⣹⢧⡞⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠂⡄⠒⠀⠠⢀⠒⡀⡀⠀⠌⡐⡂⠬⡐⢂⠀⡐⡄⠀⠄⠂⢀⠈⠀⠀⠀⠀⠀⠀⠀⠑⣦⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣇⠩⣬⢸⣼⣋\n⣿⣿⣿⣥⣺⣭⣁⢏⣍⣻⣿⣿⣿⣿⣟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣦⣽⠜⣮⣗⣶⣿⢿⣿⠐⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠂⠈⠠⡀⠥⢈⠆⡑⠨⣁⠤⢁⠉⢂⡍⡄⢧⡐⢂⠡⠔⡰⠅⠚⡀⠂⠐⡀⠂⡀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⢿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢀⠃⠤⢘⠢⢱⢊⢓⠂⡅⠆⡔⠊⢤⡘⣘⠴⣉⡯⠭⠽⠘⠧⠧⠴⠬⡥⢥⠒⡘⠐⠢⠄⣀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣶⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡁⠠⠐⠂⡄⠲⠌⠃⣂⡍⣬⣶⠞⠟⢃⡛⣉⣉⣤⠤⣔⠦⢒⣀⣀⠤⠤⠄⠄⠒⠒⠒⠒⠒⠒⠊⠺⢽⣿⣿⣿⣿⣍⣻⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣿⣿\n⣿⣿⣿⡷⢻⣿⡗⣿⣿⣿⣿⣿⡿⣟⢹⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠙⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⢀⠰⢀⢣⠐⡁⢃⠽⢒⣩⠥⡴⠶⠞⣛⣙⠧⠜⠒⠛⠂⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠪⣙⢿⣙⠧⡭⣴⡿⢿⣟⣿⣿⣿⣿⣿⠿⢇⣽⣿⣿\n⣿⠿⣻⡃⠉⠸⢎⢡⣾⣿⣯⣍⢳⡩⢘⡋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣝⣿⣿⣿⣿⣿⣿⡹⣿⣯⢰⣠⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⡀⠂⠠⠐⡄⠒⠌⢐⣨⠔⠲⣚⣃⠭⠕⠒⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡫⣷⣦⢿⢷⢿⣶⣾⣺⣿⣿⣿⣿⣧⠿⣿⣿⣿\n⠟⢛⠛⠋⠀⢈⠙⣚⠜⡟⣧⣋⢧⠓⡼⣹⡴⡭⣿⣿⣿⣿⡿⠯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⡿⢿⡺⢋⡿⣿⣿⣿⡇⠀⠀⠀⠀⠀⡐⡈⠆⠃⠈⢀⣐⠎⠁⠒⠉⠁⠀⠂⠂⠐⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠁⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣟⣧⡜⣛⢶⣵⣯⣭⡿⢿⣿⡿⣉⢻⡿⢿⣏\n⡞⠠⠠⣄⣆⠀⢎⠅⢊⠔⣢⡙⠊⠡⢆⡡⢟⡇⢿⡏⣠⡿⣳⣳⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣏⣿⣿⣏⣿⣿⣿⡟⣥⡖⣸⡖⣭⣐⣾⣿⣿⣿⣿⠀⠀⠀⠀⠄⠁⢀⡠⠔⠂⠉⣠⠤⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⡀⠀⢀⠀⠠⠤⠴⠶⢦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠿⡿⣿⡞⣽⣷⣿⣽⣟⡿⢿⣤⢸⣷⡿⡇\n⠃⠒⠃⠐⠀⠉⠄⣊⠤⡚⠥⡜⢣⣃⠪⣜⣿⡿⡌⣚⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⣷⣭⣿⣿⣿⢏⣽⢪⣗⣟⣿⢱⣿⣿⣿⣿⣿⡄⠀⠀⣀⠔⠂⠀⠀⠀⣤⠝⠁⣠⡆⠀⠀⢰⡄⠀⠀⠀⠀⠀⠸⠿⣿⠟⠀⠀⣰⠊⠀⠀⢶⡈⠙⢿⣇⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣱⣿⣧⠛⢫⣿⢩⣿⣿⣿⣿⡎⣿⣿⡜\n⠤⠄⣀⠀⠀⢰⢨⣥⣒⠩⢔⣱⡆⡌⣄⢻⣿⣿⣶⣾⣶⡿⢿⣿⣿⣿⡻⠛⠻⣿⣿⣿⣿⢰⣿⣿⣿⡿⣿⣿⣯⣿⠿⣻⣿⡿⠏⣿⣿⣿⣿⣿⣿⡧⠪⠊⠀⠀⠀⠀⠀⠀⠈⠀⠀⢿⣧⣤⢤⢾⣫⣥⠀⠀⠀⠀⠐⠡⠀⠀⠰⣈⠿⣧⣤⣤⡿⢃⠀⠐⠻⠖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⢋⣿⣿⣿⣧⠚⣿⢋⣿⣿⢤⣿⠇⣿⣿⣟\n⠀⢊⠐⠠⡰⣘⢚⠒⢛⡓⢚⠃⠓⡙⢴⡿⠉⣻⣿⣿⣿⣷⡟⣿⣿⣿⣷⡀⠱⡝⢿⣟⢛⣠⣥⣴⣦⣴⣶⣽⢗⢻⡗⡿⣿⡇⣾⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⣨⣽⢯⣻⠛⠁⠀⠀⠀⠐⡯⠐⠄⠀⠀⠀⠿⣷⣶⣷⡯⣙⠄⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⡧⣿⣿⣿⡌⠿⣿⣿⣾⡞⠿⣹⣿⡿\n⠜⠁⠀⠬⡅⠂⢩⡐⣮⠴⣉⡀⠰⣈⢚⣿⣾⣿⣿⣿⣿⣿⢱⣿⡇⠛⠛⠁⠀⠘⡈⣿⣷⡟⠛⠛⠙⠉⠀⢀⣬⣿⢸⡿⣿⣍⣿⣿⣿⣿⣿⣿⠅⠀⠀⠀⠀⠀⠀⠀⠀⠤⢨⠕⡳⠰⡠⠌⠁⠀⠀⠀⠀⠀⠀⢸⠳⡈⠄⠀⠀⠀⠈⠙⠻⣋⡛⣥⣞⢫⡓⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣻⣷⣿⣿⡏⣿⡿⣻⣥⣀⢹⣿⡟⢨⣰⣿⣿⣾\n⢀⢪⡉⣹⣍⠺⡷⢈⠥⢘⠠⣐⡀⢂⢮⢽⣿⣿⣿⣿⣿⣿⣎⢯⣷⠄⡀⠀⠀⠀⡃⢡⠐⠃⢀⣀⣤⣴⣶⣾⣯⣿⠸⣏⣿⡇⣿⣟⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠘⠎⢥⠓⠁⠀⠐⠀⠄⠀⠀⠀⠀⠨⡑⠌⠀⠀⠀⠂⠁⠶⢀⠀⠉⡚⢬⡭⠙⠀⠀⠀⠀⠀⢀⣠⠆⠀⢠⣿⢼⣿⢸⣼⡟⣿⣽⢿⣧⣿⠈⠡⠰⢹⣿⣽⣿⣿\n⠾⠶⠿⠧⠞⠃⠈⢃⠚⢨⠱⢠⣘⠣⣜⣳⣿⣿⣿⣿⣿⣿⡟⠓⠙⠒⠒⣈⠐⠂⠁⢀⣤⣶⣿⣿⣿⣿⣿⣿⡿⣽⢰⢳⣯⡷⣹⣿⢼⣿⣿⡃⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠂⠈⠀⡐⡎⣄⠂⠀⢀⡴⣶⣦⡆⠀⠀⢂⠴⡈⡀⢃⠈⠁⠀⠀⠈⠀⠀⠀⠀⢂⢀⣿⣿⡆⠀⣾⣿⣿⣿⣿⣿⡗⣿⡿⣾⣹⣿⡃⠄⡇⣿⡟⡿⣿⡿\n⡀⠀⠀⠀⠀⠀⠀⢀⠈⡀⠬⠐⠦⠛⠶⠟⠛⠛⠛⠛⠛⠛⠓⠛⠛⣅⠀⠀⢀⢠⣾⣿⣿⣟⣿⣿⣿⣿⣷⣿⣿⡟⣸⣽⣿⣞⣡⢻⡾⣿⣿⣇⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠢⡝⢶⣝⠀⡰⠀⠘⣿⡿⠟⠀⣀⠀⡿⣍⢷⡀⠄⠀⠂⠀⠀⠀⠀⠀⡀⠂⣼⣿⣿⣗⠀⣹⣿⣿⢿⣻⣿⣿⣟⣗⣿⣿⣿⡇⠸⢹⣿⣷⢸⣻⣿\n⠐⠊⠒⠂⢒⡀⢧⣤⡀⢔⣐⢓⠲⣀⠂⠀⠀⠀⡆⠉⠁⠀⠀⠘⢸⣵⣄⣠⣾⣷⣿⡿⣿⣇⣿⣿⣿⣿⣿⣿⣿⡗⣱⣿⣿⣍⣽⣿⢿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠌⠱⢬⡍⣋⠈⠁⠀⠀⠀⠀⠁⠀⠀⠀⠊⡅⢮⡑⣀⠂⠀⠀⠀⠂⠠⡌⢀⣾⣿⣿⣿⣿⠀⣾⣿⣿⡆⣿⣿⢸⣿⡿⣿⣿⣻⡇⢼⣹⣿⡇⡼⣼⣿\n⣅⠈⠀⡆⠈⠿⠆⢻⡿⢀⢪⠍⠵⣈⠀⠀⠀⢀⠧⣬⡇⡀⢀⢸⢸⣿⡿⠋⢭⣟⣋⡿⠈⢙⢿⣿⣿⣿⣿⡧⣟⡇⡞⣯⣿⣸⣿⣿⣏⣿⣿⣿⣿⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⣡⠒⠌⠀⠀⠀⠀⠀⢠⠀⡀⠀⠀⠀⠀⠉⢂⠍⠖⡄⠀⠀⠀⢀⠀⠐⣸⣿⣿⣿⣿⣿⡄⣿⣿⣿⡇⣿⣿⣯⣿⢾⣿⣿⣻⠇⣾⣸⣿⡇⡐⣹⣿\n⠈⠆⠀⠀⠀⠀⠀⠈⠇⣀⠒⠬⠠⠌⠀⠤⠀⢆⡞⣿⡷⢃⡰⢈⢸⡏⠀⠰⡜⢍⡿⠒⠄⣀⡉⠯⣉⠙⣉⣃⡉⢒⡏⣿⣏⢹⣿⢿⡦⣿⣿⣿⣿⡆⠀⢰⣦⣤⣤⣀⣀⣀⠀⠀⠀⠀⠢⠀⠀⠀⠀⠀⠀⣀⣄⡀⢀⡁⢄⡀⠀⠀⠀⠀⠘⠬⠀⠃⠀⠀⣀⣠⣴⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣲⣿⣿⣻⣿⣗⣿⣿⣼⢈⡇⣟⣿⡇⠇⣿⠏\n⠤⠬⠤⠤⠤⠴⠤⠦⠶⠶⠛⠂⠰⠒⠲⠖⠂⠒⠒⠒⠒⠒⠒⠚⠚⠛⠒⠒⠒⠛⠓⠒⠒⠓⠒⠓⠓⠒⠓⠒⠒⠚⡏⣿⣿⠰⣿⡺⡗⣿⣻⣿⣿⡇⣴⣾⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⢀⠀⠀⠤⠐⠁⠀⠀⠈⠀⠀⠀⠈⠄⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⡟⡏⢿⣿⣿⣿⡇⣿⣿⣿⣼⡟⣿⣯⣿⣿⡟⣿⡋⢌⣴⢺⣿⡇⡇⣯⢀\n⠚⠚⠀⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠈⠁⠈⠀⠉⠀⠈⢀⠀⠀⠀⢄⣿⡇⣹⠠⣿⡓⡽⣿⣘⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⢠⠀⠄⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠋⣸⢾⣿⣿⡇⢟⣿⣿⠟⢟⣘⣿⡟⠼⣳⣏⠃⢸⡞⡸⣿⢣⣆⣿⠢\n⠂⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⢠⣘⣮⠇⣡⠐⡏⢱⠢⣟⣝⠻⣾⢿⡛⠻⣿⣞⣿⣿⣿⣿⣿⣷⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣷⡋⠘⣧⡟⣿⣿⡇⡿⢟⣫⢼⡌⢹⣯⣰⡏⡹⡿⢀⡏⣯⣷⢈⢘⣹⡀⠁\n⠈⠌⠀⠀⠀⠀⠄⠀⡀⠂⠀⠂⠀⠀⢀⠈⠀⠀⠀⠀⠀⠀⠀⠄⠁⠆⠂⠞⠠⠀⢀⠂⠀⡇⠀⠀⠀⠂⠀⠀⠀⢩⣜⠿⢆⠱⢸⠣⡐⡙⠁⠀⣸⠘⢋⠀⣿⣯⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⡀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠘⡿⠿⣿⠟⢁⡵⠿⠳⠈⠇⣸⣣⣽⠀⡿⠇⠠⣟⡗⡋⠌⢠⠿⣑⡀\n⠠⢉⠀⠀⠀⠀⡀⠈⢀⠁⠁⠠⠘⡀⢨⠀⡁⠡⠀⠀⠂⠡⢠⠐⢍⠂⢈⠐⢈⠀⡋⠄⡀⠂⢀⠀⠀⠀⠀⠀⠀⢪⣴⣬⡌⢸⢘⣧⣵⡊⣀⣵⣟⡆⠀⢀⡘⢿⠿⣟⣻⣿⣿⣿⠀⠀⠀⠀⠀⠀⡀⠐⠂⠔⠈⠠⠙⠀⢈⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠿⢿⡻⡿⠁⣼⣗⣋⣥⡗⠨⢟⣉⣋⣖⠸⢿⡿⠏⡼⣿⠄⠠⣟⠎⠵⠀⢸⡛⡻⣳\n⠀⠈⠀⠀⠀⠀⠌⠓⠄⡈⠐⠂⡄⢡⠸⠀⠈⡀⠀⢀⠀⠡⡐⠀⠌⠀⠾⡜⢼⠂⠁⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠼⠭⢁⡅⣸⡿⠿⠱⣯⢼⣿⠆⠑⢢⣂⡜⠋⢑⡩⣿⠿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡼⠛⣷⣤⣹⡯⠭⣟⡃⣴⡿⣟⢿⣙⡿⣯⣴⠁⢠⣈⠀⢰⢻⠆⠂⠈⠀⣇⣓⡈\n⠀⠐⠀⠈⠄⠈⠄⠃⠠⠀⠁⠌⡄⢃⠰⠀⠹⠀⠄⠀⠆⠔⡐⠛⠥⡙⠆⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⢀⣭⣯⡼⢿⣤⠠⢭⠖⢹⠟⠗⠂⠁⠙⠉⠙⠋⢃⣹⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⠊⢿⠋⢻⡍⠭⠉⠉⠀⠀⠀⠁⠀⠀⠀⢀⠰⠡⠀⠀⣘⢾⡆⠈⠀⡁⠘⠉⣣\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠈⠉⠉⠈⠹⡟⣛⣚⠁⠥⠧⠲⠔⠹⢳⠀⢠⠀⣠⠜⢂⣴⣟⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢀⠁⠀⠀⠀⠀⠀⠂⠀⠜⣿⣷⣄⠀⠀⠀⠤⠄⠐⠸⢂⡇⠀⠀⠀⠀⣠⠸⢋⠁⠀⠀⠰⠾⠁\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢺⣿⣿⡃⠀⣐⠲⠰⠒⢹⣿⡀⠠⠇⠁⢠⣾⣿⡟⠀⠀⢠⡎⠀⢀⠂⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⡠⡄⢔⡠⠂⠁⠀⡀⠆⠀⠀⠀⠀⠀⠐⠀⠀⠀⠐⢻⠟⠗⢢⣩⣷⣮⣽⡗⠮⣏⠀⠀⠀⠰⠃⣳⠈⣫⣤⣄⡒⠛⠈\n⠀⠠⠀⠀⠀⢀⠠⠐⠀⢁⠂⠐⠀⠂⠀⠄⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡀⠀⠐⠒⠀⠀⠀⠀⢸⣿⠻⣤⣈⠙⠀⠋⠂⣾⡿⡿⢀⣴⣾⣿⣿⠋⠀⡄⠀⠈⠀⠀⠀⠂⠌⠀⠐⠀⠀⠠⡉⠜⡬⢃⡳⠘⡤⠂⠄⠒⡠⠔⡠⠀⠀⠀⠀⠀⠀⣼⠂⠀⣀⠞⠀⣠⣄⠄⠤⠀⠴⠂⠤⢧⡷⠩⠄⢠⡊⠉⠙⠃⡀⠙⣈⣉⣅\n⠀⠈⠄⠀⠀⠈⠀⢂⠐⠀⠠⠀⢂⠁⢀⠘⣉⠻⠂⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠙⠆⠀⡴⢸⢩⡱⠀⠰⣸⠁⢋⣼⣾⠿⠛⣿⣿⠇⣠⠟⠀⠀⠀⠀⠀⠀⠈⠄⡈⠀⠀⠀⠀⠀⠉⠰⠋⠔⡱⠠⠉⡐⠠⠑⡈⠀⠀⠀⠀⠀⠄⠀⠀⡤⠶⠊⢀⡀⠈⠻⣷⣦⣄⡀⠐⠒⠀⠈⠁⠈⢄⠌⠉⠑⠀⠀⠘⠃⠊⠈\n⠀⢂⠀⠄⠀⠁⠀⠀⠀⠠⠀⠀⠐⠄⠂⠀⠩⡠⣗⣦⣅⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠠⣤⠜⠠⢠⠞⡰⠆⢰⣃⣴⣾⣿⠯⠄⣴⡟⠃⠐⠟⢀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⡀⠀⠀⢀⡈⠆⢠⢀⠡⠠⢃⠥⠀⠀⠀⠀⠀⠀⠈⠂⠀⣀⠡⡄⠀⠀⠀⠀⠈⣿⣿⠹⣿⣦⡀⠀⠀⠤⠀⠀⠀⠀⠀⠀⠀⢀⠈⡀\n⠀⠀⠀⠀⠀⠀⠀⠂⠈⠀⠀⠀⢁⠀⠀⠀⠴⣶⡿⢿⣽⢸⣿⣶⣄⠀⡀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⢀⠈⢠⠶⠋⠁⣣⣴⣿⣿⡿⠯⠁⢊⡾⣛⣡⡼⠄⢂⡕⡀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠠⠀⡀⠂⠄⠃⠄⢂⠐⡡⠎⠀⠀⠀⠀⠀⠀⠀⠀⠡⢈⠈⠳⣕⡀⠀⢀⠀⠀⠈⢿⣇⠈⠝⠻⡄⡤⣄⣤⢆⡄⠀⠀⠀⠉⠀⠐⠄\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠡⢈⣤⡴⡸⡾⡵⣿⣿⣷⡀⠄⠀⠀⠀⢀⠀⠀⠀⠒⠀⠀⠈⠉⠁⠀⣠⣴⣿⣿⡿⣉⠁⠀⠄⢃⡾⠿⠗⢾⡇⠚⠉⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⢀⠠⠀⢂⠘⠀⠂⠀⡐⠠⠉⠀⠀⠀⠀⢀⠀⠀⠐⢂⠀⠀⠀⡐⢁⠈⣤⠂⠀⠀⠈⣿⣄⠀⠀⠀⢰⡟⡁⠀⠉⠀⠀⡀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⣀⠰⡀⠆⡄⡄⠀⠀⠀⣆⢠⡑⣿⡿⢲⡇⠀⡀⣿⣷⢟⡇⠀⠐⠀⠆⠀⠀⠀⠀⠀⠀⠀⢀⢀⣴⣿⣿⢟⣈⢀⡁⠀⡀⠀⠀⠪⡄⠀⠀⠀⠙⢤⢠⠂⠁⠀⠀⠀⡀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠂⠀⠀⣠⠜⠁⠀⡀⢀⢠⠀⠆⠀⠀⠸⢀⠀⠀⣰⠁⠂⢰⣺⣟⡀⠀⠀⠸⢼⡤⠀⠀⠙⡇⢁⣀⡀⠀⠀⠁⠀⠀⠀⠀\n⠀⠀⣀⡀⠆⠻⣦⠀⣷⢈⢃⠇⢀⣸⣼⠏⠷⣸⠀⠃⢼⠀⠀⠙⢍⣽⣵⠀⠀⣀⢠⠘⠕⠄⠀⠀⣠⣴⣾⣿⣏⠃⠐⠀⠒⠻⡠⠀⠀⠀⠀⡉⠀⠰⠄⠀⠀⢨⠀⠉⠀⢠⠰⡄⠁⡄⢀⠀⠀⣀⠠⣷⡀⠈⠀⠄⠀⢀⣰⢋⡄⡄⣤⢨⣰⣆⡸⣔⣦⠀⠈⡈⠅⠀⡽⢸⣃⠀⠘⢹⡇⠀⠂⠀⢡⠒⡅⠀⠀⢱⣿⣿⣟⢟⡳⠛⢶⣦⣀⠀\n⠀⠀⠀⡀⢣⢂⡏⠶⠉⠃⠈⢢⣖⢮⡙⡄⠀⣼⢿⣅⠈⠃⠀⣶⣤⡬⣽⣁⣉⠍⠅⠀⢀⣬⣶⣿⡏⣉⠓⢢⣘⢧⡀⠀⠀⠀⠈⠀⠀⠀⣈⠀⠄⢓⠠⢀⢦⠠⡀⠀⡀⠂⢃⠘⡡⠐⡍⢌⠳⣌⠻⣳⢟⢧⡣⠔⡊⡜⢂⠣⠜⡩⢐⢋⠮⠙⡜⠩⠘⠀⠐⡐⡆⢸⡇⠈⠃⢒⠀⠆⠀⠐⠀⠀⢠⠁⠀⠈⠀⠝⢨⣝⡁⠀⠀⡄⠂⠈⠻⣷\n⠀⣀⡀⠉⢀⡈⢦⠀⠀⠃⠀⢀⣧⣻⡇⢸⡵⠤⣤⡄⠀⢠⣾⣯⣏⢹⠟⠀⠪⠉⠠⠶⠽⡦⠙⡋⠃⠈⠛⡄⠙⠆⠀⠀⠀⠀⡀⠈⠄⠀⢒⢈⡑⠀⠀⠀⡸⣆⠀⡅⡃⠈⠄⠂⡁⢒⠈⡌⢲⠠⢃⢥⡋⠷⢬⡑⢢⠘⢠⠃⡜⢠⠃⡌⠒⡜⢀⠡⠀⠀⢈⡽⢑⣾⠀⠀⠘⠂⣈⠄⠀⠀⠀⠀⠀⠁⠀⢀⠑⣸⠀⢄⣉⠆⠀⠈⢰⣀⠂⠈\n⠛⢿⠁⠀⠀⠇⠄⠧⠰⠄⠀⢀⢿⡿⠇⢺⣵⣿⡇⠀⣰⣟⢿⠋⣥⡆⢀⠏⣂⠄⠐⢂⠀⠡⠀⢳⠀⠀⠈⠀⠀⠲⠀⢀⠀⠀⠀⠀⠡⠀⠀⠀⠐⢠⡀⠀⠀⢻⡀⢿⡇⠐⠠⡁⠄⢡⢂⠙⣤⠃⡍⠦⡙⣎⠳⠘⠤⡉⢆⠣⡘⢄⠣⣈⠁⡐⠠⠂⠀⠀⠠⠚⢘⡟⠀⠀⠀⣃⠠⠀⠀⠐⠀⠀⠘⠀⠀⡄⢢⠘⡀⠈⠽⠇⠀⠸⠀⢸⠒⡀\n⠀⠐⢦⣤⡀⣌⠢⢈⠠⠔⢠⣖⡟⡶⠿⠿⠉⠀⢠⡾⢿⠏⢀⢀⡿⠃⠀⡴⡇⠀⢀⡀⠐⠀⠁⠈⠆⢀⣆⠀⠀⠀⡀⠀⠀⠀⠀⠀⢂⠁⠀⠀⠀⢎⢠⠀⠀⠄⣧⠸⡇⠈⠄⠡⠘⡄⠚⡴⠀⡻⢌⡕⣣⡌⢇⡘⢄⠃⡌⠰⡁⢎⡔⠀⠆⡁⡅⡐⠀⠀⠐⠄⣿⠇⠀⠀⠀⢸⡀⠄⠀⠀⠀⠀⠉⠀⠶⠐⡀⢋⣀⡀⠀⠃⠀⠀⠀⠀⡀⠁\n⢈⠀⠀⠉⠁⠀⢊⢡⣥⣬⣭⣤⡬⢝⣩⠛⠀⠠⡀⠈⡏⠀⠀⠀⠀⠀⣘⣿⠋⠀⠀⠀⠀⠂⠀⠀⠠⠐⠸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠈⠠⠀⠀⠀⢮⠹⡀⠀⠘⡇⡂⢧⠐⡈⠄⡡⢂⢣⠸⡥⠑⢪⡜⣡⠞⡠⠜⡠⢍⡴⠱⡘⢤⠉⡘⠠⠐⠀⡄⠀⠀⠹⡘⡟⠀⠀⠀⠀⠈⠧⠀⠀⠀⠀⠀⠰⠂⠄⠀⠁⠀⢣⠅⠀⠠⠀⠀⠀⠀⠀⠁\n⠆⠀⠁⠀⠈⠐⢌⠀⠈⡞⠿⢕⠾⠋⠀⠀⢶⣿⠤⠄⠀⠀⠀⠀⢀⠤⡙⠖⠁⠠⡃⠀⠀⠀⠁⠀⠀⠧⠈⢒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠸⡆⠀⠦⠀⠸⡁⢸⠀⣘⠨⢄⡡⢆⠳⡘⢧⠃⡘⢥⠚⡄⢣⠡⢎⠐⣇⡙⠦⠡⢀⠣⣈⠰⠀⠀⠀⠹⣡⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠠⠥⠀⠀⠀⠌⠀⠻⠄⠂⠄⠀⠀⠀⠀⠀\n⢠⡠⡀⡀⠀⠀⢈⠴⠆⣈⣀⠀⠠⠀⠀⢀⠚⠿⠀⠀⠂⠀⠀⢀⠎⡴⡥⠀⢀⠐⠃⠀⠀⠠⠀⠀⠀⠀⢠⠈⠀⠀⠀⠀⠂⡀⠀⠀⠀⠀⡠⠀⠀⠀⡒⠀⡰⠀⠤⠁⠀⡆⣡⢊⠔⠩⣔⣢⢙⡢⡕⢨⢊⡵⣈⠆⣃⠧⣙⢄⢫⠅⢰⢃⠲⣀⠆⡁⠀⠀⡇⠅⠀⠀⠀⠀⠀⠐⡀⢠⠀⡀⠀⠀⢠⣬⡀⠀⠁⠐⠨⢉⠃⢀⠀⠂⠀⠀⠀⠀')

def inputCheck(prompt): #Checks for invalid input that is a negative number or text
   while True:
      userInput = input(prompt)
      if userInput.isdigit():
         return int(userInput)
      print('Invalid input, try again.')

def p1turn(): #Player 1's turn function
    soldierImage()
    global trench1Count #Tracks the count of units in each location (Trench)
    global trench2Count
    global trench3Count
    trench1Count = inputCheck('Player 1, you have {} units. How many units in trench 1 of 3? '.format(troopCount)) #First input prompt
    while trench1Count > troopCount: #Checks if the input is more than the available units
      print('Commander we don\'t have {} units, we have {} available\n'.format(trench1Count,troopCount)) #Print the input vs the actual available units
      trench1Count = inputCheck('Player 1, you have {} units. How many units in trench 1? '.format(troopCount)) #Second input prompt (if the first input is invalid)

    #Start of Trench 2 - Check for remaining available units
    if troopCount - trench1Count > 0: #If Player 1 has not placed all the available units in the previous trench then proceed to the following trench
      trench2Count = inputCheck('Player 1, you have {} units. How many units in trench 2 of 3? '.format(troopCount - trench1Count)) #First input prompt
      while trench2Count > troopCount - trench1Count: #Checks if the input is more than the available units
         print('Commander we don\'t have {} units, we have {} available\n'.format(trench2Count,troopCount - trench1Count)) #Print the input and vs the actual available units
         trench2Count = inputCheck('Player 1, you have {} units. How many units in trench 2? '.format(troopCount - trench1Count)) #Second input prompt (if the first input is invalid)
      
    #Start of Trench 3 - Check for remaining available units
    if troopCount - trench1Count -trench2Count > 0: #If Player 1 has not placed all the available units in the previous 2 trenches then proceed to the following trench
      trench3Count = inputCheck('Player 1, you have {} units. How many units in trench 3 of 3? '.format(troopCount - trench1Count - trench2Count)) #First input prompt
      while trench3Count > troopCount - trench1Count - trench2Count: #Checks if the input is more than the available units
         print('Commander we don\'t have {} units, we have {} available\n'.format(trench3Count,troopCount - trench1Count - trench2Count)) #Print the input vs the actual available units
         trench3Count = inputCheck('Player 1, you have {} units. How many units in trench 3? '.format(troopCount - trench1Count - trench2Count)) #Second input prompt (if the first input is invalid)
    while troopCount != trench1Count + trench2Count + trench3Count: #If the total does not add up to what is available, then the turn should reset
       print('All units must be placed commander! We have {} available not {}!'.format(troopCount,trench1Count+trench2Count+trench3Count)) #Print that not all units have been placed
       p1turn() #Reset the turn
    else: 
       def conf(): #This function allows the player to confirm (yes/no) their inputs
        global trench1Count #Reference to inputs
        global trench2Count
        global trench3Count
        confirm = input('Confirm? y/n ') #input "y" or "n"
        if confirm == 'n': #This should reset the turn and allow the player to redo their turn
            trench1Count = 0 #reset the variables
            trench2Count = 0
            trench3Count = 0
            p1turn() #call back to the turn function to reset
        elif confirm == 'y': #This should end the turn and perform some "aesthetic" tasks to signify the end of the turn
            print('Good luck commander!')
            if platform.system() == 'Windows': #Play a random audio clip from the Player 1 (Sarge) files - formatted for Windows
               try:
                  playsound(str(Path(__file__).resolve().parent)+'\\Audio\\Sarge{}.mp3'.format(random.randrange(0,8)),False)
               except:
                  pass
            elif platform.system() == 'Darwin': #Play a random audio clip from the Player 1 (Sarge) files - formatted for Mac
               try:
                  playsound(str(Path(__file__).resolve().parent)+'/Audio/Sarge{}.mp3'.format(random.randrange(0,8)),False)
               except:
                  pass
            else:
               pass #If not running on Windows or Mac then the audio playing is skipped
            sleep(3)            
        else:
          print('{} is not y/n'.format(confirm)) #if "y" or "n" are not the input then reset the prompt
          conf()
       conf() #call the defined function

def p2turn(): #Player 2's turn
   tankImage() #prints the icon for player 2
   global ordinance1Loc #using the previously defined variables
   global ordinanceCount
   ordinanceDict = {1:'first', 2:'second', 3:'third'} #this dictionary allows for dynamic sentence structure later
   ordinance1Loc = inputCheck('Player 2, {} ordinance to which trench? '.format(ordinanceDict[ordinanceCount])) #ask player for input
   while 4 <= ordinance1Loc or ordinance1Loc <= 0: #This is to ensure the number is within the acceptable range
      print('{} is an invalid trench selection. Choose 1, 2, or 3.'.format(ordinance1Loc))
      ordinance1Loc = inputCheck('Player 2, first ordinance to which trench? ')
   ordinanceCount = ordinanceCount + 1 #adds one to track Player 2's available turns
   if platform.system() == 'Windows': #Plays a random audio clip for player 2, formatted for Windows
      try:
         playsound(str(Path(__file__).resolve().parent)+'\\Audio\\Artillery{}.mp3'.format(random.randrange(0,3)),False)
      except:
         pass
   elif platform.system() == 'Darwin': #plays a random audio clip for player 2, formatted for Mac
      try:
         playsound(str(Path(__file__).resolve().parent)+'/Audio/Artillery{}.mp3'.format(random.randrange(0,3)),False)
      except:
         pass
   else: #If neither Mac nor Windows the audio function is skipped
      pass

def turnCheck(): #This should analyze the turn outcome and verify if there is a win for Player 2
   global troopCount #access necessary variables
   global trench1Count
   global trench2Count
   global trench3Count
   trenchMap = {1:trench1Count,2:trench2Count,3:trench3Count} #numbers each trench
   troopCount = trench1Count + trench2Count + trench3Count - trenchMap[int(ordinance1Loc)] #Adds all the units in the trenches, subtracts the units in the attacked trench
   trench1Count = 0 #reset the trenches for the next turn
   trench2Count = 0
   trench3Count = 0
   if troopCount == 0: #This should trigger the win for player 2
      print('Units remaining...')
      sleep(6)
      print(troopCount)
      sleep(3)
      if platform.system() == 'Windows': #terminal resize to better show the Player 2 win screen, formatted for Windows
         win = pygetwindow.getWindowsWithTitle(str(shutil.which("py")))[0]
         win.size = (1200, 900)
         sleep(1)
      elif platform.system() == 'Darwin': #terminal resize to better show the Player 2 win screen, formatted for Mac
         resize_terminal(130,99)
      else: #If neither Windows nor Mac, the resizing is passed
         pass
      p1LImage()
      print('Player 2 wins!')
      sleep(7)
      os._exit(0) #should close the program

def clearScreen(): #Screen wipe to keep Player 2 from seeing Player 1's inputs
   for val in range(0,33):
      print('\n')

#Below is the chronological process of calling functions to walk proceed through the game
p1turn() #Round 1 Begins
clearScreen()
p2turn()
turnCheck()

print('Units remaining...')
sleep(6)
print(troopCount)
sleep(3) #Round 1 Ends

p1turn() #Round 2 Begins
clearScreen()
p2turn()
turnCheck()

print('Units remaining...')
sleep(6)
print(troopCount)
sleep(3) #Round 2 Ends

ordinanceCount = 1 #reset for player 2's turn count
troopCount += 2 #bonus units for player 1

print('Section 1 of 4 cleared. 2 units gained. Total {} units.'.format(troopCount)) #First section cleared notice
sleep(6)

p1turn() #Round 3 Begins
clearScreen()
p2turn()
turnCheck()

print('Units remaining...')
sleep(6)
print(troopCount)
sleep(3) #Round 3 Ends

p1turn() #Round 4 Begins
clearScreen()
p2turn()
turnCheck()

print('Units remaining...')
sleep(6)
print(troopCount)
sleep(3) #Round 4 Ends

ordinanceCount = 1 #reset for player 2's turn count
troopCount += 1 #bonus unit for player 1

print('Section 2 of 4 cleared. 1 unit gained. Total {} units.'.format(troopCount)) #Second section cleared notice
sleep(6)

p1turn() #Round 5 Begins
clearScreen()
p2turn()
turnCheck()

print('Units remaining...')
sleep(6)
print(troopCount)
sleep(3) #Round 5 Ends

p1turn() #Round 6 Begins
clearScreen()
p2turn()
turnCheck()

print('Units remaining...')
sleep(6)
print(troopCount)
sleep(3) #Round 6 Ends

ordinanceCount = 1 #reset player 2's turn count
troopCount += 1 #bonus unit for player 1

print('Section 3 of 4 cleared. 1 unit gained. Total {} units.'.format(troopCount)) #Third section cleared notice
sleep(6)

p1turn() #Round 7 Begins
clearScreen()
p2turn()
turnCheck()

print('Units remaining...')
sleep(6)
print(troopCount)
sleep(3) #Round 7 Ends

p1turn() #Round 8 Begins
clearScreen()
p2turn()
turnCheck() 

print('Units remaining...')
sleep(6)
print(troopCount)
sleep(3) #Round 8 Ends

print('Section 4 of 4 cleared. Player 1 wins!') #Victory message for player 1
tankDestroyedImage() #Victory icon for player 1
sleep(5)
os._exit(0) #should exit the program