import random
import os

'''
更新内容;
·修改了伤害公式，并调整了各项属性初始值和提升值
·增加了血条颜色会随血量而改变的机制
·增加了回合计数器
'''

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

    def atkd_by(self, atkr):
        dmg = int(atkr.atk * 140 / (140 + self.dfs) )
        if random.randint(1, 100) <= atkr.crt:
            dmg = int(dmg * max(2, 1 + atkr.crt / 100))
            print(atkr.nm, " deal ", dmg, " damages to ", self.nm, " critically!")
        else:
            print(atkr.nm, " deal ", dmg, " damages to ", self.nm)
        self.hp -= dmg

    def buff(self, knd):
        if knd == buffs[0]:
            self.hp += hp_up
            print(self.nm, " get ", hp_up, " heart points!")
        elif knd == buffs[1]:
            self.atk += atk_up
            print(self.nm, " get ", atk_up, " attacks!")
        elif knd == buffs[2]:
            self.dfs += dfs_up
            print(self.nm, " get ", dfs_up, " defenses!")
        elif knd == buffs[3]:
            self.crt += crt_up
            print(self.nm, " get ", crt_up, " critical rates!")
        else:
            print("It's a bug! How could you do this!")

    def show(self):
        print(f"* {self.nm}: ", end = '')
        # 显示模式 38, 使用 256 色模式, 结尾 \033[m 切换回正常颜色
        # 红色——0——橙色——1/3——黄色——2/3——淡绿色——1——绿色
        if self.hp >= self.mx_hp:
            print(f"HP: \033[38;5;34m{self.hp}\033[0m", end = "")
        elif self.hp * 3 >= self.mx_hp * 2:
            print(f"HP: \033[38;5;112m{self.hp}\033[0m", end = "")
        elif self.hp * 3 >= self.mx_hp:
            print(f"HP: \033[38;5;184m{self.hp}\033[0m", end = "")
        elif self.hp > 0:
            print(f"HP: \033[38;5;214m{self.hp}\033[0m", end = "")
        else:
            print(f"HP: \033[38;5;196m{self.hp}\033[0m", end = "")
        print(f" ATK: {self.atk}  DFS: {self.dfs}  CRT: { self.crt}")

def wnt_gt(lst, sy_wnt, sy_agn):
    while True:
        x = input(sy_wnt)
        if x in lst:
            break
        else:
            print(sy_agn)
    return x

#Basic statistics
you = plyr("You  ", 7000, 800, 60, 20)
enmy = plyr("Enemy", 7000, 800, 60, 20)
hp_up = 700
atk_up = 80
dfs_up = 30
crt_up = 12
buffs = ['h', 'a', 'd', 'c']

print("Mission: kill the enemy and keep alive.")
#The game starts!
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
#The game ends!
print("press 'Enter' key to end")
input()

#ccacdcchhhhhhhhhahhhhhchhcaahchhhhchchdhhhachhhaaadhhcdchccchahhahhchhhchcchchcchhdcahchhdhhhhhchhhhchdhhhcahhcdhchhccchhdhachdhhhhhchchcahhhhhhchhhhh