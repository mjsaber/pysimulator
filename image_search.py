import argparse
import pyautogui as pg
import time
import random

normal_cnt = 0
mystery_cnt = 0


def wait():
    time.sleep(random.uniform(0.5, 1))


def click_if_found(step, loc):
    if not loc:
        print("not found: ", step)
        return
    print(step, loc)
    pg.click(loc.x/2, loc.y/2)
    wait()


def buy(loc, bookmark):
    if not loc:
        return
    # move x-axis right 500 pixels, y-axis down 30 pixels
    print("found bookmark", bookmark, loc)
    pg.click(loc.x/2+500, loc.y/2+30)
    wait()
    if bookmark == "normal":
        loc = pg.locateCenterOnScreen('material/buy_normal.png', confidence=0.9)
        if loc:
            pg.click(loc.x/2, loc.y/2)
            global normal_cnt
            normal_cnt += 1
        wait()
    elif bookmark == "mystery":
        loc = pg.locateCenterOnScreen('material/buy_mystery.png', confidence=0.9)
        if loc:
            pg.click(loc.x/2, loc.y/2)
            global mystery_cnt
            mystery_cnt += 1
        wait()


def buy_bookmark():
    loc = pg.locateCenterOnScreen('material/normal_bookmark.png', confidence=0.9)
    buy(loc, "normal")
    loc = pg.locateCenterOnScreen('material/mystery_bookmark.png', confidence=0.9)
    buy(loc, "mystery")
    pg.scroll(-1)
    wait()
    loc = pg.locateCenterOnScreen('material/normal_bookmark.png', confidence=0.9)
    buy(loc, "normal")
    loc = pg.locateCenterOnScreen('material/mystery_bookmark.png', confidence=0.9)
    buy(loc, "mystery")


def search(rounds):
    # click middle of screen to switch window
    click_if_found("start", pg.Point(1460, 900))
    print("start searching: ", rounds)
    for i in range(rounds):
        buy_bookmark()

        loc = pg.locateCenterOnScreen('material/refresh.png', confidence=0.9)
        click_if_found("refresh", loc)

        loc = pg.locateCenterOnScreen('material/confirm_refresh.png', confidence=0.9)
        click_if_found("confirm_refresh", loc)


def confirm_boss(boss):
    if boss == 1:
        found = False
        for i in range(3):
            loc = pg.locateCenterOnScreen('material/executor.png', confidence=0.9)
            if loc is not None:
                found = True
            if found:
                return True
            time.sleep(1)
        return False


def farm(boss):
    # click middle of screen to switch window
    click_if_found("start", pg.Point(1460, 900))
    # click_if_found("move west", pg.Point(115*2, 515*2))
    # if confirm_boss(1):
    #     return
    # loc = pg.locateCenterOnScreen('material/treasure.png', confidence=0.9)
    # click_if_found("treasure", loc)
    # click_if_found("move west", pg.Point(115*2, 515*2))
    # fight
    # click_if_found("move south", pg.Point(1035*2, 520*2))
    # fight
    # click_if_found("move west", pg.Point(115*2, 515*2))
    # fight
    # click_if_found("move north", pg.Point(110*2, 285*2))
    # fight
    # click_if_found("move west", pg.Point(115*2, 515*2))
    # fight
    # click_if_found("move east", pg.Point(1035*2, 287*2))
    # fight
    # click_if_found("move east", pg.Point(1035*2, 287*2))
    # fight
    click_if_found("move north", pg.Point(110*2, 285*2))


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('rounds', type=int, help='number of round searching shop')
    # args = parser.parse_args()
    # search(args.rounds)
    # print("normal: ", normal_cnt, "mystery: ", mystery_cnt)
    farm(1)
