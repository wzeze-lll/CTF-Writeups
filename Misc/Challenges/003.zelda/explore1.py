import game, time
g = game.Game()
def c(x, q=0.45):
    print(">>>", x)
    out = g.cmd(x, q)
    print(out)
    return out
try:
    c("battle")
    for i in range(6):
        c("attack")
    c("inv list")
    c("mw show")
    c("shop list")
except Exception as e:
    print("[err]", e)
g.close()
