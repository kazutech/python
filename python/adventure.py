import tkinter

def decode_line(event):
    global current_line, bgimg, lcharimg, ccharimg, rcharimg
    if current_line >= len(scenario):
        return;

    line = scenario[current_line]
    current_line = current_line + 1

    line = line.replace("\\n","\n").strip()

    params = line.split(" ")

    if line[0] != "#":
        message["text"] = line
        return
    elif params[0] == "#back":
        canvas.delete("all")
        bgimg = tkinter.PhotoImage(file=params[1])
        canvas.create_image(450, 230, image=bgimg)
    elif params[0] == "#putChar":
        if params[2] == "L":
            canvas.delete("left")
            lcharimg = tkinter.PhotoImage(file=params[1])
            canvas.create_image(200,160,image=lcharimg,tag="left")
        elif params[2] == "R":
            canvas.delete("right")
            rcharimg = tkinter.PhotoImage(file=params[1])
            canvas.create_image(700,160,image=rcharimg,tag="right")
        else:
            canvas.delete("center")
            ccharimg = tkinter.PhotoImage(file=params[1])
            canvas.create_image(450,160,image=ccharimg,tag="center")
    elif params[0] == "#branch":
        message.unbind("<Button-1>")
        btn = tkinter.Button(text=params[2],width=20)
        branch.append(btn)
        btn["command"] = lambda : jump_to_line(int(params[1])-1)
        btn.place(x=300, y=60+int(params[1])*60)
        jumplabel.append(params[3])
        if params[4] == "n":
            return
    elif params[0] == "#jump":
        label = params[1].strip()

        for l in range(len(scenario)):
            if scenario[l].strip() == "## " + label:
                current_line = l
                decode_line(None)
                return
    elif params[0].strip() == "#end":
        message["text"] = "終わり"
        message.unbind("<Button-1>")
        current_line = 999999999

    decode_line(None)

def jump_to_line(branchID):
    global current_line

    for btn in branch:
        btn.place_forget()
        btn.destroy()
    branch.clear()
    label = jumplabel[branchID]
    jumplabel.clear()
    message.bind("<Button-1>",decode_line)

    for l in range(len(scenario)):
        if scenario[l].strip() == "## " + label:
            current_line = l
            decode_line(None)
            return

root = tkinter.Tk()
root.title("よろしくアドベンチャー")
root.minsize(900,460)
root.option_add("*font",["メイリオ",14])

canvas = tkinter.Canvas(width=900, height=460)
canvas.place(x=0,y=0)

message = tkinter.Label(width=70, height=5, wraplength=840,
                        bg="white", justify="left", anchor="nw")

message.place(x=28,y=284)
message["text"] = "クリックしてスタート"

scenario = []
file = open("img8/scenario.txt","r",encoding="utf-8")
while True:
    line = file.readline()
    scenario.append(line)
    if not line:
        file.close()
        break

current_line = 0

message.bind("<Button-1>",decode_line)

bgimg = None
lcharimg = None
ccharimg = None
rcharimg = None

branch = []
jumplabel = []
root.mainloop()
