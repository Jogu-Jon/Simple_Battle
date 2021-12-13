import io
import random
import os
import sys
import socket


# 解决 Win32 终端转义失效 bug
os.system("")


class plyr:
    def __init__(self, nm, hp, atk, dfs, crt):
        self.nm = nm
        self.mx_hp = hp
        self.hp = hp
        self.atk = atk
        self.dfs = dfs
        self.crt = crt

    def atkd_by(self, atkr, target=sys.stdout):
        dmg = int(atkr.atk * 140 / (140 + self.dfs))
        if random.randint(1, 100) <= atkr.crt:
            dmg = int(dmg * max(2, 1 + atkr.crt / 100))
            print(atkr.nm, " deal ", dmg, " damages to ", self.nm, " critically!", file=target)
        else:
            print(atkr.nm, " deal ", dmg, " damages to ", self.nm, file=target)
        self.hp -= dmg

    def buff(self, knd, target=sys.stdout):
        if knd == buffs[0]:
            self.hp += hp_up
            print(self.nm, " get ", hp_up, " heart points!", file=target)
        elif knd == buffs[1]:
            self.atk += atk_up
            print(self.nm, " get ", atk_up, " attacks!", file=target)
        elif knd == buffs[2]:
            self.dfs += dfs_up
            print(self.nm, " get ", dfs_up, " defenses!", file=target)
        elif knd == buffs[3]:
            self.crt += crt_up
            print(self.nm, " get ", crt_up, " critical rates!", file=target)
        else:
            print("It's a bug! How could you do this!", file=target)

    def show(self, target=sys.stdout):
        print(f"* {self.nm}: ", end='', file=target)
        # 显示模式 38, 使用 256 色模式, 结尾 \033[m 切换回正常颜色
        # 红色——0——橙色——1/3——黄色——2/3——淡绿色——1——绿色
        if self.hp >= self.mx_hp:
            print(f"HP: \033[38;5;34m{self.hp}\033[0m", end="", file=target)
        elif self.hp * 3 >= self.mx_hp * 2:
            print(f"HP: \033[38;5;112m{self.hp}\033[0m", end="", file=target)
        elif self.hp * 3 >= self.mx_hp:
            print(f"HP: \033[38;5;184m{self.hp}\033[0m", end="", file=target)
        elif self.hp > 0:
            print(f"HP: \033[38;5;214m{self.hp}\033[0m", end="", file=target)
        else:
            print(f"HP: \033[38;5;196m{self.hp}\033[0m", end="", file=target)
        print(f" ATK: {self.atk}  DFS: {self.dfs}  CRT: {self.crt}", file=target)


def wnt_gt(lst, sy_wnt, sy_agn):
    while True:
        x = input(sy_wnt)
        if x in lst:
            break
        else:
            print(sy_agn)
    return x


# Basic statistics
hp_up = 700
atk_up = 80
dfs_up = 30
crt_up = 12
buffs = ['h', 'a', 'd', 'c']

print("Mission: kill the enemy and keep alive.")

print("Mode: 1.single player 2.online")
while True:
    s = input("Your option:")
    if s == "1":
        you = plyr("You  ", 7000, 800, 60, 20)
        enmy = plyr("Enemy ", 7000, 800, 60, 20)
        # The game starts!
        turn = 0
        while True:
            turn += 1
            you.show()
            enmy.show()
            print()
            if you.hp <= 0:
                print("You lose!")
                break
            elif enmy.hp <= 0:
                print("You win!")
                break
            else:
                you.buff(wnt_gt(buffs, f"Choose your buff kind {buffs}:", "There's no this kind of buff!"))
                enmy.buff(random.choice(buffs))
                print(f"——The {turn} turn——")
                enmy.atkd_by(you)
                you.atkd_by(enmy)
        # The game ends!
        print("press 'Enter' key to end")
        input()
        sys.exit(0)

    if s == "2":
        s = input("1.create a server  2.join a server:")
        if s == "1":
            s = socket.socket()
            s.bind(("0.0.0.0", 2333))
            print(f"server listening on {socket.gethostbyname(socket.gethostname())} port 2333")
            s.listen()
            c, addr = s.accept()
            print(f"player from {addr} connected!")
            print("Game starts! You are player1!")
            turn = 0

            local = plyr("Player1 ", 7000, 800, 60, 20)
            remote = plyr("Player2 ", 7000, 800, 60, 20)
            while True:
                turn += 1

                print(f"——The {turn} turn——")
                local.show()
                remote.show()
                print()

                temp = io.StringIO()
                print(f"——The {turn} turn——", file=temp)
                local.show(target=temp)
                remote.show(target=temp)
                print(file=temp)

                c.send(temp.getvalue().encode("utf-8"))

                if local.hp <= 0:
                    print("You lose!")
                    c.send("You win!|".encode("utf-8"))
                    c.close()
                    break
                elif remote.hp <= 0:
                    print("You win!")
                    c.send("You lose!|".encode("utf-8"))
                    c.close()
                    break
                else:
                    temp = io.StringIO()
                    local.buff(wnt_gt(buffs, f"Choose your buff kind {buffs}:", "There's no this kind of buff!"), target=temp)
                    remote.atkd_by(local, target=temp)

                    temp = temp.getvalue()
                    print(temp)
                    c.send(temp.encode("utf-8"))

                    c.send(f"Choose your buff kind {buffs}:".encode("utf-8"))

                    temp = io.StringIO()

                    while True:
                        remote_buf = c.recv(1024).decode("utf-8").strip()
                        if remote_buf in buffs:
                            remote.buff(remote_buf, target=temp)
                            break
                    local.atkd_by(remote, target=temp)

                    temp = temp.getvalue()
                    print(temp)
                    c.send(temp.encode("utf-8"))

        elif s == "2":
            s = socket.socket()
            addr = input("server addr:")
            s.connect((addr, 2333))
            print(f"connected to {addr} port 2333!")
            print("Game starts! You are player2!")

            while True:
                data = s.recv(40960)
                if len(data) > 0:
                    data = data.decode("utf-8")
                    flag = False
                    if f"Choose your buff kind {buffs}:" in data:
                        data = data.replace(f"Choose your buff kind {buffs}:", "")
                        flag = True
                    if "|" in data:
                        print(data.replace("|", ""))
                        break
                    print(data)
                    if flag:
                        buf = wnt_gt(buffs, f"Choose your buff kind {buffs}:", "There's no this kind of buff!")
                        s.send(buf.encode("utf-8"))

        else:
            print("Invalid input!")

        print("press 'Enter' key to end")
        input()
        sys.exit(0)
    print("Invalid input!")

# ccacdcchhhhhhhhhahhhhhchhcaahchhhhchchdhhhachhhaaadhhcdchccchahhahhchhhchcchchcchhdcahchhdhhhhhchhhhchdhhhcahhcdhchhccchhdhachdhhhhhchchcahhhhhhchhhhh
