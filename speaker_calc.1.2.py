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
    calc_type = v.get()
    speaker_type = lb1.curselection()[0]
    if calc_type == 1 or calc_type == 2:
        floor_length = float(e1.get())
        hor = int(e3.get())
    vert = int(e4.get())
    height = float(e6.get())
    xc = float(e7.get())
    yc = float(e8.get())

    # For coord calcs, get floor length and angles
    if calc_type == 3 or calc_type == 4:
        floor_length = float(floor_length_calc(xc, yc))
        hor = hor_angle(xc, yc)

    # Path and loss calcs
    path = path_length(floor_length,height)
    loss = path_loss(path)
    axis_loss_val = axis_loss(hor, vert, speaker_type)

    # SPL calcs
    if calc_type == 1 or calc_type ==3: # Calculate speaker SPL
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

def clear():
    e1.delete(0, 20)
    e2.delete(0, 20)
    e2["fg"] = "black"
    e3.delete(0, 20)
    e4.delete(0, 20)
    e5.delete(0, 20)
    e5["fg"] = "black"
    e6.delete(0, 20)
    e6.insert(0,2)
    Label(master, text="               ").grid(row=3, column=1, sticky=W, padx=4)
    Label(master, text="               ").grid(row=3, column=3, sticky=W, padx=4)
    Label(master, text="                    ").grid(row=4, column=1, sticky=W, padx=4)
    Label(master, text="                    ").grid(row=5, column=1, sticky=W, padx=4)


master = Tk()
master.title("Assembly Speaker SPL Calculator")
# Speaker type selection
Label(master, text="Speaker Type:").grid(row=0, sticky=W)
lb1 = Listbox(master, height=2)
lb1.insert(1, "Evid 4.2")
lb1.insert(2, "Evid 6.2")
lb1.grid(row=0, column=1)
lb1.activate(0)
lb1.selection_set(0)
Label(master, text="Speaker Output (dB-SPL):").grid(row=0, column=2, sticky=W)
# Get speaker SPL
e5 = Entry(master)
e5.grid(row=0, column=3, padx=4)
Label(master, text="Speaker HAL(m):").grid(row=0, column=4, sticky=W)
# Get speaker height, defaults to 2m
e6 = Entry(master)
e6.grid(row=0, column=5, padx=4)
e6.insert(0,2)

# Co-ordinate Entry
e7 = Entry(master)
e7.grid(row=7, column=1, padx=4)
e8 = Entry(master)
e8.grid(row=7, column=3, padx=4)
e9 = Entry(master)
e9.grid(row=7, column=5, padx=4)


Label(master, text="Floor Length (m):").grid(row=1, sticky=W)
Label(master, text="Target Seat SPL:").grid(row=1, column=2, sticky=W)
Label(master, text="Horizontal Off-Axis Angle:").grid(row=2, sticky=W)
Label(master, text="Vertical Off-Axis Angle:").grid(row=2, column=2, sticky=W)
Label(master, text="Path Length:").grid(row=3, sticky=W)
Label(master, text="Input Power:").grid(row=3, column=2, sticky=W)
Label(master, text="Path Loss:").grid(row=4, sticky=W)
Label(master, text="Off-Axis Loss:").grid(row=4, column=2, sticky=W)
Label(master, text="Speaker X Coord:").grid(row=7, sticky=W)
Label(master, text="Speaker Y Coord:").grid(row=7, column=2, sticky=W)
Label(master, text="Speaker Aim Angle:").grid(row=7, column=4, sticky=W)

#Floor length
e1 = Entry(master)
e1.grid(row=1, column=1, padx=4)
#Seat SPL
e2 = Entry(master)
e2.grid(row=1, column=3, padx=4)
#Horiz. angle
e3 = Entry(master)
e3.grid(row=2, column=1, padx=4)
#Vert. angle
e4 = Entry(master)
e4.grid(row=2, column=3, padx=4)

v = IntVar()
v.set(1)
Radiobutton(master, text="Calculate Speaker SPL", padx=5, variable=v, value=1).grid(row=6)
Radiobutton(master, text="Calculate Seat SPL", padx=5, variable=v, value=2).grid(row=6, column=1)
Radiobutton(master, text="Speaker SPL (Coord Mode)", padx=5, variable=v, value=3).grid(row=6, column=2)
Radiobutton(master, text="Seat SPL (Coord Mode)", padx=5, variable=v, value=4).grid(row=6, column=3)

Button(master, text='Quit', command=master.quit).grid(row=8, column=0, pady=4)
Button(master, text='Calculate', command=calculate).grid(row=8, column=1, pady=4)
Button(master, text='Clear', command=clear).grid(row=8, column=2, pady=4)

mainloop( )
