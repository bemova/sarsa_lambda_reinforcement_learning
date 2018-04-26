import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


cell = 60
w_height = 6
w_width = 6


class MazeGrid(tk.Tk, object):
    def __init__(self):
        super(MazeGrid, self).__init__()
        self.action_space = ['up', 'down', 'left', 'right']
        self.n_actions = len(self.action_space)
        self.title('Intelligent Mouse')
        self.geometry('{0}x{1}'.format(w_height * cell, w_height * cell))
        self.make_env()

    def make_env(self):
        self.canvas = tk.Canvas(self, bg='white', height=w_height * cell, width=w_width * cell)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        for c in range(0, w_width * cell, cell):
            x0, y0, x1, y1 = c, 0, c, w_height * cell
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, w_height * cell, cell):
            x0, y0, x1, y1 = 0, r, w_height * cell, r
            self.canvas.create_line(x0, y0, x1, y1)

        trap1 = tk.PhotoImage(file='./images/trap.png')
        self.canvas.image3 = trap1
        self.trap_1 = self.canvas.create_image(cell * 2 + 1, cell + 1, image=trap1, anchor="nw")

        trap2 = tk.PhotoImage(file='./images/trap.png')
        self.canvas.image4 = trap2
        self.trap_2 = self.canvas.create_image(cell + 1, cell * 2 + 1, image=trap2, anchor="nw")

        trap3 = tk.PhotoImage(file='./images/trap.png')
        self.canvas.image5 = trap3
        self.trap_3 = self.canvas.create_image(cell * 4 + 1, cell * 2 + 1, image=trap3, anchor="nw")

        trap4 = tk.PhotoImage(file='./images/trap.png')
        self.canvas.image6 = trap4
        self.trap_4 = self.canvas.create_image(cell * 2 + 1, cell * 3 + 1, image=trap4, anchor="nw")

        trap5 = tk.PhotoImage(file='./images/trap.png')
        self.canvas.image7 = trap5
        self.trap_5 = self.canvas.create_image(cell * 3 + 1, cell * 4 + 1, image=trap5, anchor="nw")

        trap6 = tk.PhotoImage(file='./images/trap.png')
        self.canvas.image8 = trap6
        self.trap_6 = self.canvas.create_image(cell * 5 + 1, cell * 5 + 1, image=trap6, anchor="nw")

        trap7 = tk.PhotoImage(file='./images/trap.png')
        self.canvas.image9 = trap7
        self.trap_7 = self.canvas.create_image(1, 1, image=trap7, anchor="nw")

        trap8 = tk.PhotoImage(file='./images/trap.png')
        self.canvas.image10 = trap8
        self.trap_8 = self.canvas.create_image(cell * 5 + 1, 1, image=trap8, anchor="nw")

        cheese = tk.PhotoImage(file='./images/cheese.png')
        self.canvas.image = cheese
        self.cheese = self.canvas.create_image(cell * 2 + 1, cell * 2 + 1, image=cheese, anchor="nw")

        mouse = tk.PhotoImage(file='./images/mouse.png')
        self.canvas.image2 = mouse
        self.mouse = self.canvas.create_image(0, cell * 5, image=mouse, anchor="nw")

        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.mouse)
        mouse = tk.PhotoImage(file='./images/mouse.png')
        self.canvas.image2 = mouse
        self.mouse = self.canvas.create_image(0, cell * 5, image=mouse, anchor="nw")
        # return the state of the mouse
        return self.canvas.coords(self.mouse)

    def step(self, action):
        """
        :param action: could be 0, 1, 2, 3, 4 as up, down, right, and left respectively
        :return: nest state, current reward, and the the state of the game as 'done' which could be false or true
        """
        s = self.canvas.coords(self.mouse)
        base_action = np.array([0, 0])
        if action == 0:
            if s[1] > cell:
                base_action[1] -= cell
        elif action == 1:
            if s[1] < (w_height - 1) * cell:
                base_action[1] += cell
        elif action == 2:
            if s[0] < (w_width - 1) * cell:
                base_action[0] += cell
        elif action == 3:
            if s[0] > cell:
                base_action[0] -= cell

        # move the mouse(agent) to the nest state coordinate
        self.canvas.move(self.mouse, base_action[0], base_action[1])

        next_state = self.canvas.coords(self.mouse)

        done, reward, next_state= self.calculate_reward(next_state)

        return next_state, reward, done

    def calculate_reward(self, next_state):
        """
        calculates the reward in a case of moving to the next state
        reaching to the cheese reward is 100
        reaching to mouse traps reward are -100
        each movement has -1 reward in order to find fastest path.
        :param next_state: next state
        :return: done, reward, next_state
        """
        if [next_state[0] + 1, next_state[1] + 1] == self.canvas.coords(self.cheese):
            reward = 100
            done = True
            next_state = 'terminal'
        elif [next_state[0] + 1, next_state[1] + 1] in \
                [self.canvas.coords(self.trap_1), self.canvas.coords(self.trap_2), self.canvas.coords(self.trap_3),
                 self.canvas.coords(self.trap_4), self.canvas.coords(self.trap_5), self.canvas.coords(self.trap_6),
                 self.canvas.coords(self.trap_7), self.canvas.coords(self.trap_8)]:
            reward = -100
            next_state = 'terminal'
            done = True
        else:
            reward = -1
            done = False

        return done, reward, next_state

    def render(self):
        time.sleep(0.1)
        self.update()


def update():
    for t in range(10):
        env.reset()
        while True:
            env.render()
            a = 2
            s, r, done = env.step(a)
            if done:
                break


if __name__ == '__main__':
    env = MazeGrid()
    env.after(100, update)
    env.mainloop()