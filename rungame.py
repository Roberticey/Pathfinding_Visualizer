import pygame
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
FPS = 30
blockSize = 20  # Set the size of the grid block
flagSource = 0
flagDest = 0
source = [-1,-1]
dest = [-1,-1]
wall = []

def main():
    global win, clock, flagSource
    pygame.init()
    pygame.display.set_caption("First Game")
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    win.fill(BLACK)
    clock = pygame.time.Clock()

    run = True
    ran = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not ran:
                x, y = event.pos
                print(x, y)
                global flagSource, flagDest, source, dest
                if x % blockSize == 0 or y % blockSize == 0:
                    pass
                elif flagSource == 0:
                    source = [x/blockSize,y/blockSize]
                    flagSource = 1
                elif flagDest == 0:
                    if [x/blockSize,y/blockSize] != source:
                        dest = [x/blockSize,y/blockSize]
                        flagDest = 1
                else:
                    global wall
                    temp = [x/blockSize,y/blockSize]
                    if temp!=source and temp!=dest and temp not in wall:
                        wall+= [[x/blockSize,y/blockSize]]

            elif event.type == pygame.KEYDOWN and not ran:
                if event.key == pygame.K_SPACE:
                    findPath()
                    ran = True

        drawGrid()
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

def drawGrid():

    for x in range(0,WINDOW_WIDTH,blockSize):
        for y in range(0,WINDOW_HEIGHT,blockSize):
            rect = pygame.Rect(x, y,blockSize, blockSize)
            pygame.draw.rect(win, WHITE, rect, 1)
    global source,dest
    if source[0]!=-1 :
        rect = pygame.Rect(source[0]*blockSize, source[1]*blockSize, blockSize-2, blockSize-2)
        pygame.draw.rect(win, (0,255,0), rect)
    if dest[0]!=-1 :
        rect = pygame.Rect(dest[0]*blockSize, dest[1]*blockSize, blockSize-2, blockSize-2)
        pygame.draw.rect(win, (0,0,255), rect)
    for tuple in wall:
        rect = pygame.Rect(tuple[0]*blockSize, tuple[1]*blockSize, blockSize-2, blockSize-2)
        pygame.draw.rect(win, WHITE, rect)

def findPath():
    print('')
    print(source)
    print(dest)
    print(wall)

    hsize = int(WINDOW_WIDTH/blockSize)
    vsize = int(WINDOW_HEIGHT/blockSize)


    visited = []
    prev = []
    dist = []
    queue = []

    for i in range(hsize):
        temp = []
        temp2 = []
        temp3 = []
        # temp4 = []
        for j in range(vsize):
            temp += [0]
            temp2 += [(-1,-1)]
            temp3 += [100000.50]
            queue += [[i,j]]
        visited += [temp]
        prev += [temp2]
        dist += [temp3]

    for pair in wall:
        # print(visited[pair[0]][pair[1]])
        visited[pair[0]][pair[1]] = 1



    # queue.append(source)
    dist[source[0]][source[1]] = 0.0
    found = False
    while queue:
        # x,y = queue.pop(0)
        dmin = 100000.50
        xmin = -1
        ymin = -1
        ind = -1
        ctr = 0
        for coord in queue:
            x = coord[0]
            y = coord[1]
            if dist[x][y] < dmin:
                dmin = dist[x][y]
                xmin = x
                ymin = y
                ind = ctr
            ctr += 1
        queue.pop(ind)
        x = xmin
        y = ymin
        if x == dest[0] and y == dest[1]:
            found = True
            break
        if dmin == 100000.50:
            return

        # visited[x][y] = 1
        for i in  range(8):
            xn, yn = x, y
            if i==0:
                xn += 1
            elif i == 1:
                xn -= 1
            elif i == 2:
                yn += 1
            elif i == 3:
                yn -= 1
            elif i == 4:
                xn += 1
                yn += 1
            elif i == 5:
                xn -= 1
                yn += 1
            elif i == 6:
                xn += 1
                yn -= 1
            elif i == 7:
                xn -= 1
                yn -= 1

            len = 1
            if i>=4:
                len=1.414

            if xn<0 or yn<0 or xn>=hsize or yn>=vsize:
                continue
            if [xn,yn] in wall:
                continue
            if visited[xn][yn] == 1:
                continue
            if dist[x][y]+len < dist[xn][yn]:
                dist[xn][yn] = dist[x][y]+len
                prev[xn][yn] = (x, y)
                if [xn,yn]==dest:
                    continue
                rect = pygame.Rect(xn * blockSize, yn * blockSize, blockSize - 2, blockSize - 2)
                pygame.draw.rect(win, (255, 255, 0), rect)
                pygame.display.update()

        clock.tick(50)

    prex, prey = dest[0], dest[1]

    while found:
        (prex,prey) = prev[prex][prey]
        if [prex,prey]==source:
            break
        rect = pygame.Rect(prex * blockSize, prey * blockSize, blockSize - 2, blockSize - 2)
        pygame.draw.rect(win, (255, 0, 0), rect)
        pygame.display.update()
        clock.tick(50)



    # print('exitting')

    # print(prev[0][4])

    # flag = 0
    # while(source[0] != dest[0] or source[1] != dest[1]):
    #     if flag:
    #         rect = pygame.Rect(source[0]*blockSize, source[1]*blockSize, blockSize-2, blockSize-2)
    #         pygame.draw.rect(win, (255,0,0), rect)
    #         pygame.display.update()
    #     clock.tick(5)
    #     if(source[0]<dest[0]):
    #         source[0]+=1
    #     elif(source[0]>dest[0]):
    #         source[0]-=1
    #     elif(source[1]<dest[1]):
    #         source[1]+=1
    #     elif(source[1]>dest[1]):
    #         source[1]-=1
    #     flag=1
    #
    #

main()
