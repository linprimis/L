from tkinter import *

class draw_polyline:
    def __init__(self,canvas,vertical):
        self.lines_list = []
        self.canvas = canvas
        self.vertical = vertical
        self.click_num = 0
        pass
    def get_diagonal_coords(self):
        self.x_list,self.y_list = [],[]
        for i in self.lines_list:

            coord = self.canvas.coords(i)
            self.x_list.append(coord[0])
            self.x_list.append(coord[2])
            self.y_list.append(coord[1])
            self.y_list.append(coord[3])
        self.x_min = min(self.x_list)
        self.y_min = min(self.y_list)
        self.x_max = max(self.x_list)
        self.y_max = max(self.y_list)

    def start_draw_line(self,event):
        x1,y1,x,y = event.x,event.y,event.x,event.y
        if self.click_num  == 0:
            if self.vertical:
                self.lines_list.append(self.canvas.create_line(x1,y1,x1,y))
            else:
                self.lines_list.append(self.canvas.create_line(x1,y1,x,y1))

        else:

            l = self.lines_list[self.click_num-1]
            coords = self.canvas.coords(l)
            if self.vertical:
                self.lines_list.append(self.canvas.create_line(coords[2],coords[3],coords[2],y+5))
            else:
                self.lines_list.append(self.canvas.create_line(coords[2],coords[3],x+5,coords[3]))

        canvas.bind("<B1-Motion>", self.move_and_draw)
        canvas.bind("<ButtonRelease-1>", self.onrelease_handler)

    def onrelease_handler(self,event):
        self.vertical = not self.vertical
        self.click_num+=1

    def in_the_range(self,l,coord):
        coords = self.canvas.coords(l)
        x_min,x_max = min(coords[0],coords[2]),max(coords[0],coords[2])
        y_min,y_max = min(coords[1],coords[3]),max(coords[1],coords[3])
        x_in_range = coord[0]>x_min-3 and coord[0]<x_max+3
        y_in_range = coord[1]>y_min-3 and coord[1]<y_max+3
        return x_in_range and y_in_range

    def start_draw_line_1(self,event):
        self.start = (event.x,event.y)
        x1,y1,x,y = event.x,event.y,event.x,event.y
        if self.click_num  == 0:
            if self.vertical:
                self.lines_list.append(self.canvas.create_line(x1,y1,x1,y+5,arrow = 'last',arrowshape=(8,15,3)))
            else:
                self.lines_list.append(self.canvas.create_line(x1,y1,x+5,y1,arrow = 'last',arrowshape=(8,15,3)))
        canvas.bind("<B1-Motion>", self.move_and_draw_1)
        # canvas.bind("<ButtonRelease-1>", self.onrelease_handler)

    def move_and_draw_1(self,event):
        l = self.lines_list[-1]
        coords = self.canvas.coords(l)
        x_in_range = event.x < canvas.winfo_width()-10 and event.x>10
        y_in_range = event.y < canvas.winfo_height()-10 and event.y > 10
        # print(l)
        x0,y0,x,y = coords[0],coords[1],event.x,event.y

        if event.x > canvas.winfo_width()-10:
            x = canvas.winfo_width()-10
        elif event.x<10:
            x = 10
        if event.y > canvas.winfo_height()-10:
            y = canvas.winfo_height()-10
        elif event.y < 10:
            y = 10

        if self.vertical:
            if abs(y-y0)>20 or len(self.lines_list)==1:
                self.canvas.coords(l,x0,y0,x0,y)
                coords = self.canvas.coords(l)
                if abs(x-x0)>20:
                    self.vertical = not self.vertical
                    self.canvas.itemconfig(l, arrow='')
                    self.lines_list.append(self.canvas.create_line(coords[2],coords[3],x,coords[3],arrow = 'last',arrowshape=(8,15,3)))
            elif abs(y-y0)<20:
                self.canvas.delete(l)
                self.lines_list.pop(-1)
                self.canvas.itemconfig(self.lines_list[-1], arrow = 'last',arrowshape=(8,15,3))
                # print('delete')
                self.vertical = not self.vertical

        elif not self.vertical:
            if abs(x-x0)>20 or len(self.lines_list)==1:
                self.canvas.coords(l,x0,y0,x,y0)
                coords = self.canvas.coords(l)
                if abs(y-y0)>20:
                    self.vertical = not self.vertical
                    self.canvas.itemconfig(l, arrow='')
                    self.lines_list.append(self.canvas.create_line(coords[2],coords[3],coords[2],y,arrow = 'last',arrowshape=(8,15,3)))

            elif abs(x-x0)<20:
                self.canvas.delete(l)
                self.lines_list.pop(-1)
                self.canvas.itemconfig(self.lines_list[-1], arrow = 'last',arrowshape=(8,15,3))
                # print('delete')
                self.vertical = not self.vertical
    

    def move_and_draw(self,event):
        if len(self.lines_list)>0:
            l = self.lines_list[self.click_num]
            coords = self.canvas.coords(l)
            x1,y1,x,y = coords[0],coords[1],event.x,event.y
            if self.vertical:
                if y-y1<5:
                    y = int(y+5*abs(y-y1)/((y-y1)+1e-9))
                self.canvas.coords(l,x1,y1,x1,y)
            else:
                if x-x1<5:
                    x = int(x+5*abs(x-x1)/((x-x1)+1e-9))

                self.canvas.coords(l,x1,y1,x,y1)

    def onclick_handler(self,event):
        self.canvas.bind("<Button-1>", self.start_draw_line)
    def start_draw(self):
        self.canvas.bind("<Button-1>", self.start_draw_line_1)


if __name__=='__main__':
    print("Hello")
    master = Tk()
    canvas = Canvas(master, width=500, height=500)
    canvas.pack()
    p =  draw_polyline(canvas = canvas,vertical=True)
    p.start_draw()
    master.mainloop()