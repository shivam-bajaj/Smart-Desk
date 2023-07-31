from tkinter import *
import time
import RPi.GPIO as IO



'''
Colors used
 
#2b2d2f = Grey Background

#90EE90 = Light Green

#0078D4 = Light blue

'''



IO.setmode(IO.BCM)
root = Tk()
root.title("Project")
root.configure(bg="#2b2d2f")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#root.geometry("1024x600+30+30")
# pin number 10 and 11 are dummy pins used for error handling
s1_relay = 10
s2_relay = 17
s3_relay = 16
s4_relay = 11
wc_relay = 14
up_relay = 17
down_relay = 18

IO.setup(s1_relay,IO.OUT)
IO.setup(s2_relay,IO.OUT)
IO.setup(s3_relay,IO.OUT)
IO.setup(s4_relay,IO.OUT)
IO.setup(wc_relay,IO.OUT)
IO.setup(up_relay,IO.OUT)
IO.setup(down_relay,IO.OUT)



table_memory=1
previous_table_memory=0

height= 48
up_total_time=22
down_total_time=18
current_distance = 0
next_distance =0
levels_distance ={1:0,2:16,3:32,4:48}
up_down_start_time=0

up_velocity=height/up_total_time
down_velocity = height/down_total_time

s1_button_status = True
s2_button_status = True
s3_button_status = True
s4_button_status = True
wc_button_status = True

print(f" Up Velocity   -> {up_velocity}cm/sec")
print(f" Down Velocity -> {down_velocity}cm/sec")





up_icon = PhotoImage(file = "icons8-scroll-up-72.png")
up_icon_press = PhotoImage(file = "icons8-scroll-up-72 (1).png")

down_icon = PhotoImage(file = "icons8-scroll-down-72.png")
down_icon_press = PhotoImage(file ="icons8-scroll-down-72 (1).png")

m1_icon = PhotoImage(file = "icons8-1-60.png")
m1_icon_press = PhotoImage(file = "icons8-1-60 (2).png")

m2_icon = PhotoImage(file = "icons8-2-60.png")
m2_icon_press = PhotoImage(file = "icons8-2-60 (1).png")

m3_icon = PhotoImage(file = "icons8-3-60.png")
m3_icon_press = PhotoImage(file = "icons8-3-60 (1).png")

m4_icon = PhotoImage(file = "icons8-4-60.png")
m4_icon_press = PhotoImage(file = "icons8-4-60 (1).png")

toggle_icon_on = PhotoImage(file = "icons8-toggle-on-48 (1).png")
toggle_icon_off = PhotoImage(file = "icons8-toggle-off-48 (1).png" )


screen_top = Frame(root,width=1024, height=40, bg="#2b2d2f")
screen_top.pack(side=TOP,fill=BOTH)

company_label = Label(screen_top,text="XO",font=("Comic Sans ms", 32, "bold"), anchor=N, fg='#90EE90', bd=0, bg="#2b2d2f")
company_label.grid(row=0,column=0,padx=50,pady=5)

user_label = Label(screen_top,text="Jarvis",font=("Comic Sans ms", 32, "bold"), anchor=N, fg='#90EE90', bd=0, bg="#2b2d2f")
user_label.grid(row=0,column=1,padx=50,pady=5)

time_label = Label(screen_top,text="04:40 pm",font=("Comic Sans ms", 32, "bold"), anchor=N, fg='#90EE90', bd=0, bg="#2b2d2f")
time_label.grid(row=0,column=2,padx=50,pady=5)



screen_mid = Frame(root,width=1024,height=250, bg="#2b2d2f")
screen_mid.pack(side=TOP,fill=BOTH,expand=True)


def relay_switch_on(relay):
    IO.output(relay,IO.LOW)


def relay_switch_off(relay):
    IO.output(relay,IO.HIGH)

relay_switch_off(up_relay)
relay_switch_off(down_relay)


def update_current_distance(up_down_time,up_or_down):
    global current_distance
    if up_or_down==1:
        up_distance= up_velocity*up_down_time
        current_distance=current_distance+up_distance
        print(f"current distance -> {current_distance}")
    if up_or_down==0:
        down_distance= down_velocity*up_down_time
        current_distance=current_distance-down_distance
        print(f"current distance -> {current_distance}")


def up_press(event):
    global up_down_start_time
    up_button.config(image=up_icon_press)
    up_down_start_time = time.perf_counter()
    relay_switch_on(up_relay)


def up_release(event):
    global up_down_start_time
    up_button.config(image=up_icon)
    relay_switch_off(up_relay)
    end = time.perf_counter()
    up_time=end-up_down_start_time
    update_current_distance(up_time,1)



up_button = Button(screen_mid,image=up_icon,height=68,width=68,bd=0,highlightthickness=0)

up_button.bind("<ButtonPress>", up_press)
up_button.bind("<ButtonRelease>", up_release)

up_button.grid(row=0,column=0,padx=50,pady=30)


up_label = Label(screen_mid,text="UP",font=("Comic Sans ms", 32, "bold"), anchor=N, fg='#90EE90', bd=0, bg="#2b2d2f")
up_label.grid(row=1,column=0)


def down_press(event):
    global up_down_start_time
    down_button.config(image=down_icon_press)
    up_down_start_time = time.perf_counter()
    relay_switch_on(down_relay)

def down_release(event):
    global up_down_start_time
    down_button.config(image=down_icon)
    relay_switch_off(down_relay)
    end = time.perf_counter()
    down_time=end-up_down_start_time
    update_current_distance(down_time,0)

down_button = Button(screen_mid,image=down_icon,height=68,width=68,bd=0,highlightthickness=0)
down_button.bind("<ButtonPress>", down_press)
down_button.bind("<ButtonRelease>", down_release)

down_button.grid(row=0,column=1,padx=50,pady=30)


down_label = Label(screen_mid,text="DOWN",font=("Comic Sans ms", 32, "bold"), anchor=N, fg='#90EE90', bd=0, bg="#2b2d2f")
down_label.grid(row=1,column=1)

def previous_memory_delete():
    global previous_table_memory
    global table_memory
    previous_table_memory=table_memory
    print(f"prevous_memory -> {previous_table_memory}")
    if previous_table_memory==1:
        m1_button.config(image=m1_icon)
    if previous_table_memory==2:
        m2_button.config(image=m2_icon)
    if previous_table_memory==3:
        m3_button.config(image=m3_icon)
    if previous_table_memory==4:
        m4_button.config(image=m4_icon)

def current_memory_call():
    global table_memory
    print(f"Current_memory -> {table_memory}")
    if table_memory==1:
        m1_button.config(image=m1_icon_press)
    if table_memory==2:
        m2_button.config(image=m2_icon_press)
    if table_memory==3:
        m3_button.config(image=m3_icon_press)
    if table_memory==4:
        m4_button.config(image=m4_icon_press)

def change_distance(level):
    global current_distance
    next_distance=current_distance-levels_distance[level]
    if next_distance > 0:
        t=abs(next_distance)/up_velocity
        print(f"Time to reach the level      ->  {t} sec")
        print(f"Distance to reach the level  ->  {abs(next_distance)} cm")
        relay_switch_on(up_relay)
        time.sleep(t)
        relay_switch_off(up_relay)
        current_distance=current_distance+abs(next_distance)

    if next_distance > 0:
        print(f"Time to reach the level      ->  {t} sec")
        print(f"Distance to reach the level  ->  {abs(next_distance)} cm")
        relay_switch_on(down_relay)
        time.sleep(t)
        relay_switch_off(down_relay)
        current_distance=current_distance+abs(next_distance)

    print(f"Current Distance -> {current_distance}")



def m1():
    previous_memory_delete()
    global table_memory
    table_memory=1
    current_memory_call()
    change_distance(table_memory)



m1_button = Button(screen_mid,image=m1_icon,height=55,width=55,bd=0,highlightthickness=0,command=lambda: m1())
m1_button.grid(row=0,column=2,padx=50,pady=30)

def m2():
    previous_memory_delete()
    global table_memory
    table_memory=2
    current_memory_call()
    change_distance(table_memory)


m2_button = Button(screen_mid,image=m2_icon,height=55,width=55,bd=0,highlightthickness=0,command=lambda: m2())
m2_button.grid(row=0,column=3,padx=50,pady=30)

def m3():
    previous_memory_delete()
    global table_memory
    table_memory=3
    current_memory_call()
    change_distance(table_memory)

m3_button = Button(screen_mid,image=m3_icon,height=55,width=55,bd=0,highlightthickness=0,command=lambda: m3())
m3_button.grid(row=0,column=4,padx=50,pady=30)


def m4():
    previous_memory_delete()
    global table_memory
    table_memory=4
    current_memory_call()
    change_distance(table_memory)

m4_button = Button(screen_mid,image=m4_icon,height=55,width=55,bd=0,highlightthickness=0,command=lambda: m4())
m4_button.grid(row=0,column=5)

memory_label = Label(screen_mid,text="Memory",font=("Comic Sans ms", 32, "bold"), anchor=N, fg='#90EE90', bd=0, bg="#2b2d2f")
memory_label.grid(row=1,column=3)


screen_bottom_left = Frame(root,width=700,height=310, bg="#2b2d2f")
screen_bottom_left.pack(side=LEFT)


relay_switch_off(s1_relay)
relay_switch_off(s2_relay)
relay_switch_off(s3_relay)
relay_switch_off(s4_relay)
relay_switch_off(wc_relay)


def s1(relay):
    global s1_button_status

    if s1_button_status:
        s1_button.config(image=toggle_icon_on)
        s1_button_status=False
        relay_switch_on(relay)

    else:
        s1_button.config(image=toggle_icon_off)
        s1_button_status = True
        relay_switch_off(relay)

def s2(relay):
    global s2_button_status

    if s2_button_status:
        s2_button.config(image=toggle_icon_on)
        s2_button_status=False
        relay_switch_on(relay)

    else:
        s2_button.config(image=toggle_icon_off)
        s2_button_status = True
        relay_switch_off(relay)


def s3(relay):
    global s3_button_status

    if s3_button_status:
        s3_button.config(image=toggle_icon_on)
        s3_button_status=False
        relay_switch_on(relay)

    else:
        s3_button.config(image=toggle_icon_off)
        s3_button_status = True
        relay_switch_off(relay)

def s4(relay):
    global s4_button_status

    if s4_button_status:
        s4_button.config(image=toggle_icon_on)
        s4_button_status=False
        relay_switch_on(relay)

    else:
        s4_button.config(image=toggle_icon_off)
        s4_button_status = True
        relay_switch_off(relay)

def wc(relay):
    global wc_button_status

    if wc_button_status:
        wc_button.config(image=toggle_icon_on)
        wc_button_status=False
        relay_switch_on(relay)

    else:
        wc_button.config(image=toggle_icon_off)
        wc_button_status = True
        relay_switch_off(relay)

s1_button = Button(screen_bottom_left,image=toggle_icon_off,bd=0,highlightthickness=0,height=44,width=44, command= lambda: s1(s1_relay) )
s1_button.grid(row=0,column=0,padx=50,pady=30)

switch_label1 = Label(screen_bottom_left,text="S1",font=("Comic Sans ms", 32, "bold"), anchor=N, fg='#90EE90', bd=0, bg="#2b2d2f")
switch_label1.grid(row=1,column=0,padx=50,pady=5)


s2_button = Button(screen_bottom_left,image=toggle_icon_off,bd=0,highlightthickness=0,height=44,width=44, command= lambda: s2(s2_relay))
s2_button.grid(row=0,column=1,padx=50,pady=30)

switch_label2 = Label(screen_bottom_left,text="S2",font=("Comic Sans ms", 32, "bold"), anchor=N, fg='#90EE90', bd=0, bg="#2b2d2f")
switch_label2.grid(row=1,column=1,padx=50,pady=5)



s3_button = Button(screen_bottom_left,image=toggle_icon_off,bd=0,highlightthickness=0,height=44,width=44, command= lambda: s3(s3_relay))
s3_button.grid(row=0,column=2,padx=50,pady=30)

switch_label3 = Label(screen_bottom_left,text="S3",font=("Comic Sans ms", 32, "bold"), anchor=N, fg='#90EE90', bd=0, bg="#2b2d2f")
switch_label3.grid(row=1,column=2,padx=50,pady=5)


s4_button = Button(screen_bottom_left,image=toggle_icon_off,bd=0,highlightthickness=0,height=44,width=44,command= lambda: s4(s4_relay))
s4_button.grid(row=0,column=3,padx=50,pady=30)

switch_label4 = Label(screen_bottom_left,text="S4",font=("Comic Sans ms", 32, "bold"), anchor=N, fg='#90EE90', bd=0, bg="#2b2d2f")
switch_label4.grid(row=1,column=3,padx=50,pady=5)


wc_button = Button(screen_bottom_left,image=toggle_icon_off,bd=0,highlightthickness=0,height=44,width=44, command= lambda: wc(wc_relay))
wc_button.grid(row=0,column=4,padx=50,pady=30)

wc_label = Label(screen_bottom_left,text="WC",font=("Comic Sans ms", 32, "bold"), anchor=N, fg='#90EE90', bd=0, bg="#2b2d2f")
wc_label.grid(row=1,column=4,padx=50,pady=5)



screen_bottom_right = Frame(root,width=324,height=310, relief=RAISED,bg="#2b2d2f")
screen_bottom_right.pack(side=RIGHT)

user = Button(screen_bottom_right,bg="#2b2d2f",width=12,height=1,text="User",font=("Comic Sans ms",20, "bold"),fg='#90EE90',bd=4,highlightbackground="#90EE90")
user.grid(row=0,column=0)

setting = Button(screen_bottom_right,bg="#2b2d2f",width=12,height=1,text="Settings",font=("Comic Sans ms",20, "bold"),fg='#90EE90',bd=4,highlightbackground="#90EE90")
setting.grid(row=1,column=0)

music_player = Button(screen_bottom_right,bg="#2b2d2f",width=12,height=1,text="Music Player",font=("Comic Sans ms",20, "bold"),fg='#90EE90',bd=4,highlightbackground="#90EE90")
music_player.grid(row=2,column=0)

notes = Button(screen_bottom_right,bg="#2b2d2f",width=12,height=1,text="notes",font=("Comic Sans ms",20, "bold"),fg='#90EE90',bd=4,highlightbackground="#90EE90")
notes.grid(row=3,column=0)

logout = Button(screen_bottom_right,bg="#2b2d2f",width=12,height=1,text="Log Out",font=("Comic Sans ms",20, "bold"),fg='#90EE90',bd=4,highlightbackground="#90EE90")
logout.grid(row=4,column=0)

root.wm_attributes('-fullscreen','True')
root.config(cursor="none")
root.mainloop()
