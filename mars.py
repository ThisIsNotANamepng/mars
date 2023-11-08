#  Works: Changing allegiance, Basic GUI, Writing to ShipRegister.txt
#  Todo: Change name, ID, and class, Adjust GUI for long ship names, When cursor is on the far left and gets a left arrow, go to other side (Same with up and down), assign battlegroup leaders (used in the deploy() call)

import sys,os
import curses
import requests

def changeAllegiance(id, newAllegiance):
    # Change the allegiance in register.txt

    with open("ShipRegister.txt", 'r') as file:
        lines = file.readlines()

    lines[lines.index(id+"\n")+3]=newAllegiance+"\n"


    with open("ShipRegister.txt", 'w') as file:
        file.writelines(lines)

def deploy(id, lead):
    print("Deploy")
    # Delete the ship from ShipRegister.txt and send the informaton back to the ship to deploy it
    allegiances=["Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Unknown"]
    allegiancesCommunicationPorts=[5002, 5003, 5004, 5005, 5006, 5007] # Need the ship's allegiance

    with open("ShipRegister.txt", 'r') as file:
        lines = file.readlines()

    allegiance=(lines[lines.index(id+"\n")+3])[:-2]
    address=lines[lines.index(id+"\n")+4]

    lines.pop(lines.index(id+"\n")+4)
    lines.pop(lines.index(id+"\n")+3)
    lines.pop(lines.index(id+"\n")+2)
    lines.pop(lines.index(id+"\n")+1)
    lines.pop(lines.index(id+"\n"))

    with open("ShipRegister.txt", 'w') as file:
        file.writelines(lines)

    

def draw_menu(stdscr):
    k = 0
    #cursor_x = 0
    #cursor_y = 1

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)


    curses.curs_set(0)  # Hide the cursor
    selected_index = 0
    selected_category = 0
    deployNum=0
    allegiances=["Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Unknown"]

    # Loop where k is the last character pressed
    while (k != ord('q')):
        if deployNum==1:deployNum=0
        if deployNum==2:deployNum=1
        f = open("ShipRegister.txt", "r")
        shipIDs=[]
        shipTypes=[]
        shipNames=[]
        shipAllegiances=[]

        num=0
        for x in f:
            if num%5==0:
                shipIDs.append(x[:len(x)-1])
            elif num%5==1:
                shipTypes.append(x[:len(x)-1])
            elif num%5==2:
                shipNames.append(x[:len(x)-1])
            elif num%5==3:
                shipAllegiances.append(x[:len(x)-1])

            num+=1
        f.close()

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN and selected_index < len(shipNames) - 1:
            selected_index += 1
        elif k == curses.KEY_UP and selected_index > 0:
            selected_index -= 1
        elif k == curses.KEY_RIGHT and selected_category < 3:
            selected_category +=1
        elif k == curses.KEY_LEFT and selected_category > 0:
            selected_category -=1
        elif k == 10:
            #Enter key
            leadShip=False
            if deployNum==0:
                shipAllegiances[selected_index]="Deploy?"
                selected_category=3
                deployNum=2 # deployNum is originally set to 0, when enter is hit it goes up by two, every main loop if deployNum is 2 it gets set to 1. If deployNum is 1 at this point the ship is deployed and deploy is set back to 0
            if deployNum==1:
                deploy(shipIDs[selected_index], leadShip)
                deployNum=0
                
        elif k == 32:
            # We can add editing names, IDs, and types later
            #Get index of current allegiance, make new allegiance index up
            if shipAllegiances[selected_index]=="Unknown":
                newAllegiance="Red"
                changeAllegiance(shipIDs[selected_index], "Red")
            else:
                # This doesn't work -------
                currentAllegiance=shipAllegiances[selected_index]
                newAllegianceIndex=allegiances.index(currentAllegiance)+1

                newAllegiance=allegiances[newAllegianceIndex]
                changeAllegiance(shipIDs[selected_index], newAllegiance)

            shipAllegiances[selected_index]=newAllegiance


        # Draw objects
        for i, obj in enumerate(shipNames):
            if i == selected_index and selected_category == 0:
                stdscr.attron(curses.color_pair(3))
            elif obj=="NAME":
                stdscr.attron(curses.color_pair(3))
            else:
                stdscr.attron(curses.color_pair(1))
            stdscr.addstr(2 + i, 2, obj)
            stdscr.attroff(curses.color_pair(1))
            stdscr.attroff(curses.color_pair(2))

        for i, obj in enumerate(shipIDs):
            if i == selected_index and selected_category == 1:
                stdscr.attron(curses.color_pair(3))
            elif obj=="ID":
                stdscr.attron(curses.color_pair(3))
            else:
                stdscr.attron(curses.color_pair(1))
            stdscr.addstr(2 + i, int(width // 6), obj)
            stdscr.attroff(curses.color_pair(1))
            stdscr.attroff(curses.color_pair(2))

        for i, obj in enumerate(shipTypes):
            if i == selected_index and selected_category == 2:
                stdscr.attron(curses.color_pair(3))
            elif obj=="TYPE":
                stdscr.attron(curses.color_pair(3))
            else:
                stdscr.attron(curses.color_pair(1))
            stdscr.addstr(2 + i, int(width // 3), obj)
            stdscr.attroff(curses.color_pair(1))
            stdscr.attroff(curses.color_pair(2))

        for i, obj in enumerate(shipAllegiances):
            if i == selected_index and selected_category == 3:
                stdscr.attron(curses.color_pair(3))
            elif obj=="ALLEGIANCE":
                stdscr.attron(curses.color_pair(3))
            else:
                stdscr.attron(curses.color_pair(1))
            stdscr.addstr(2 + i, int(width // 2 + width // 3), obj)
            stdscr.attroff(curses.color_pair(1))
            stdscr.attroff(curses.color_pair(2))


        # Declaration of strings
        #title = str(shipNames)[:width-1]
        #subtitle = "Written by Clay McLeod"[:width-1]
        #keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "    MARS Command Shell v0.9"

        # Centering calculations
        #start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        #start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        #start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        #start_y = int((height // 2) - 2)

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(0, 0, statusbarstr)
        stdscr.addstr(0, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        #stdscr.attron(curses.color_pair(2))
        #stdscr.attron(curses.A_BOLD)

        # Rendering title
        #stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        #stdscr.attroff(curses.color_pair(2))
        #stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        #stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        #stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        #stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        #stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()