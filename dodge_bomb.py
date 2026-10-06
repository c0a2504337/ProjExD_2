import os
import random
import sys
import pygame as pg



WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def check_bound(rect:pg.Rect) -> tuple[bool,bool]:
    yoko,tate = True,True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko,tate


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def draw_time(screen: pg.Surface, tmr: int) -> None:
    font = pg.font.Font(None,77)
    score = tmr // 50  
    txt_img = font.render(f"Time: {score}", True, (1, 0, 0))
    screen.blit(txt_img, (1, 1))



def gameover(screen: pg.Surface) -> None:
    gameover_bg = pg.Surface((WIDTH, HEIGHT))
    gameover_bg.set_alpha(200)
    gameover_bg.fill((0, 0, 0))
    screen.blit(gameover_bg, (0, 0))

    font = pg.font.Font(None, 100)
    txt_img = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt_img.get_rect()
    txt_rct.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(txt_img, txt_rct)

    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    
    kk_rct_l = kk_img.get_rect()
    kk_rct_l.center = (WIDTH // 2 - 300, HEIGHT // 2)
    screen.blit(kk_img, kk_rct_l)
    
    kk_rct_r = kk_img.get_rect()
    kk_rct_r.center = (WIDTH // 2 + 300, HEIGHT // 2)
    screen.blit(kk_img, kk_rct_r)

    # 4. 画面を更新
    pg.display.update()

    start_time = pg.time.get_ticks()
    clock = pg.time.Clock()

    while pg.time.get_ticks() - start_time < 5000:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        clock.tick(60)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct =bb_img.get_rect()
    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.centerx = (random.randint(0,WIDTH))
    bb_rct.centery = (random.randint(0,HEIGHT))
    vx,vy =+5,+5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0] #横方向移動量
                sum_mv[1] += tpl[1] #縦方向移動量
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True): #どこかにはみでる
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)

        idx = min(tmr // 200, 20)
        
        # 加速後の移動量を計算
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        
        # 現在の段階に対応する爆弾Surfaceの取得とサイズ更新
        bb_img = bb_imgs[idx]
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        bb_rct.move_ip(avx,avy)
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        draw_time(screen, tmr)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
