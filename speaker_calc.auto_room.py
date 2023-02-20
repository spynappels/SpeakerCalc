#!/usr/bin/python3
from math import sqrt, log, atan, degrees
from tkinter import *
import evid42_2k
import evid62_2k


# path length function
def path_length(fl,hght):
    floor = float(fl)
    height = float(hght)
    path = sqrt((floor**2)+(height**2))
    return(path)

# relative coordinate calcs
def rel_coord(seat_x, seat_y):
    speaker_x = sp1x.get()
    speaker_y = sp1y.get()
    seat_rel_x = abs(speaker_x - seat_x)
    seat_rel_y = abs(speaker_y - seat_y)
    return(seat_rel_x, seat_rel_y)

# path loss function
def path_loss(path):
    loss = abs(20*log(1/path,10))
    return(loss)

# floor length function
def floor_length_calc(x, y):
    length = sqrt((x**2)+(y**2))
    return(length)

# horizontal angle cal
def hor_angle(x, y):
    hor = int(degrees(atan(y/x)))
    return(hor)

# Off-axis loss calculation
def axis_loss(horangle, vertangle, speaker_type):
    hor = int(horangle)
    if hor < 0:
        raw_ha = 360+hor
    else:
        raw_ha = hor
    rem = (raw_ha % 2.5)
    if rem == 0:
        hor_ang = raw_ha
    elif rem < 1.25:
        hor_ang = raw_ha-rem
    else:
        hor_ang = raw_ha+(2.5-rem)
    if speaker_type == 0:
        horizontal_loss = abs(evid42_2k.horizontal[hor_ang])
    elif speaker_type == 1:
        horizontal_loss = abs(evid62_2k.horizontal[hor_ang])
    vert = int(vertangle)
    if vert < 0:
        raw_va = 360+vert
    else:
        raw_va = vert
    rem = (raw_va % 2.5)
    if rem == 0:
        vert_ang = raw_va
    elif rem < 1.25:
        vert_ang = raw_va-rem
    else:
        vert_ang = raw_va+(2.5-rem)
    if speaker_type == 0:
        vertical_loss = abs(evid42_2k.vertical[vert_ang])
    elif speaker_type == 1:
        vertical_loss = abs(evid62_2k.vertical[vert_ang])
    loss = (horizontal_loss+vertical_loss)
    return(loss)

def calculate():
    #Get entered values
    speaker_type = lb1.curselection()[0]
    for letter in [ "a", "b", "c", "d" ]:
        seat_x, seat_y = rel_coord(letter)
        print(seat_, seat_y)
        floor_length = float(floor_length_calc(seat_x, seat_y))
        print(floor_length)
        hor = hor_angle(seat_x, seat_y)
        # Path and loss calcs
        path = path_length(floor_length,height)
        loss = path_loss(path)
        axis_loss_val = axis_loss(hor, vert, speaker_type)
        if letter=="a" :
            seat_spl = int(e2.get())
        speaker_spl = seat_spl + (loss + axis_loss_val)
        e2["fg"] = "black"
        e5["fg"] = "red"
        e5.insert(0, f"{speaker_spl:.1f}")
        
    else: # Calculate seat SPL
        speaker_spl = float(e5.get())
        seat_spl = (speaker_spl - loss) - axis_loss_val
        e5["fg"] = "black"
        e2["fg"] = "red"
        e2.insert(0, f"{seat_spl:.1f}")
    
    # Calculate Input Power
    if speaker_type == 0:
        sensitivity = evid42_2k.sensitivity
    elif speaker_type == 1:
        sensitivity = evid62_2k.sensitivity
    power = int(10 ** ((speaker_spl - sensitivity)/10))
    
    # Display of output
    Label(master, text="               ").grid(row=3, column=1, sticky=W, padx=4)
    Label(master, text="               ").grid(row=3, column=3, sticky=W, padx=4)
    Label(master, text="                    ").grid(row=4, column=1, sticky=W, padx=4)
    Label(master, text="                    ").grid(row=5, column=1, sticky=W, padx=4)
    Label(master, text=f"{path:.2f}m").grid(row=3, column=1, sticky=W, padx=4)
    Label(master, text=f"{loss:.1f}dB-SPL").grid(row=4, column=1, sticky=W, padx=4)
    Label(master, text=f"{axis_loss_val:.1f}dB-SPL").grid(row=4, column=3, sticky=W, padx=4)
    Label(master, fg="red", text=f"{power}W").grid(row=3, column=3, sticky=W, padx=4)
    lb1.activate(speaker_type)



master = Tk()
master.title("Assembly Room Speaker Plan Calculator")
# Block 1
Label(master, text="Block 1").grid(row=0, sticky=W)
Label(master, text="Speaker Type:").grid(row=1, sticky=W)
lb1 = Listbox(master, height=2)
lb1.insert(1, "Evid 4.2")
lb1.insert(2, "Evid 6.2")
lb1.grid(row=1, column=1)
lb1.activate(0)
lb1.selection_set(0)
# Speaker 1 X
Label(master, text="Speaker X Coordinate:").grid(row=1, column=2, sticky=W)
sp1x = Entry(master)
sp1x.grid(row=1, column=3, padx=4)
# Speaker 1 Y
Label(master, text="Speaker Y Coordinate:").grid(row=1, column=4, sticky=W)
sp1y = Entry(master)
sp1y.grid(row=1, column=5, padx=4)
# Speaker 1 HAL
Label(master, text="Speaker HAL:").grid(row=1, column=6, sticky=W)
sp1z = Entry(master)
sp1z.grid(row=1, column=7, padx=4)
sp1z.insert(0,2)


# Block 1 Seat Coordinate Entry
# Front Right
Label(master, text="Front Right Seat:").grid(row=2, column=0, sticky=W)
Label(master, text="X Coordinate:").grid(row=2, column=1, sticky=W)
ax = Entry(master)
ax.grid(row=2, column=2, padx=4)
Label(master, text="Y Coordinate:").grid(row=2, column=3, sticky=W)
ay = Entry(master)
ay.grid(row=2, column=4, padx=4)

# Rear Right
Label(master, text="Rear Right Seat:").grid(row=3, column=0, sticky=W)
Label(master, text="X Coordinate:").grid(row=3, column=1, sticky=W)
bx = Entry(master)
bx.grid(row=3, column=2, padx=4)
Label(master, text="Y Coordinate:").grid(row=3, column=3, sticky=W)
by = Entry(master)
by.grid(row=3, column=4, padx=4)

# Rear Left
Label(master, text="Rear Left Seat:").grid(row=4, column=0, sticky=W)
Label(master, text="X Coordinate:").grid(row=4, column=1, sticky=W)
cx = Entry(master)
cx.grid(row=4, column=2, padx=4)
Label(master, text="Y Coordinate:").grid(row=4, column=3, sticky=W)
cy = Entry(master)
cy.grid(row=4, column=4, padx=4)

# Front Left
Label(master, text="Front Left Seat:").grid(row=5, column=0, sticky=W)
Label(master, text="X Coordinate:").grid(row=5, column=1, sticky=W)
dx = Entry(master)
dx.grid(row=5, column=2, padx=4)
Label(master, text="Y Coordinate:").grid(row=5, column=3, sticky=W)
dy = Entry(master)
dy.grid(row=5, column=4, padx=4)


Button(master, text='Quit', command=master.quit).grid(row=10, column=0, pady=4)
Button(master, text='Calculate', command=calculate).grid(row=10, column=1, pady=4)

mainloop( )
