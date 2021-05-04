import pygame,sys,time,random

#目标提示线的颜色
target_line_color=pygame.Color(153,153,0)
#人类矩形和猪类矩形的颜色，和他们的尺寸（像素）
human_color=pygame.Color(0,191,255)
pig_color=pygame.Color(255,20,147)
size=5

#程序窗口大小，初始化整个地图列表，因为渲染出来的人类和猪有尺寸，所以列表的范围是程序窗口大小除以尺寸
#pygame的坐标系xy方向和二维列表的下标不一样，程序坐标均以列表为准，如[3,5] -> 第三行第五列 -> pygame x=5,y=3
#pygame：0----->x
#        |
#        ↓
#        y

width=1380  
height=750
field_width=width//size
field_height=height//size
field=[[0]*field_width for i in range(field_height)] #0:空地，1:人类，2:猪  

#统一管理猪和人类的列表，方便批量操作
pig_list = []
human_list = []

#初始化pygame，设置程序窗口和标题，窗口底部预留40像素的高度用来显示信息
pygame.init()
screen = pygame.display.set_mode((width, height+40))
pygame.display.set_caption("模拟抓猪 作者：幽蓝伊梦")

#人类
class Human:
    '''
    position：列表，初始坐标
    target：Pig对象，要抓的猪对象
    field_size：列表或元组，战场的尺寸（长，高）
    '''

    speed = 5 #移动速度

    def __init__(self,position,target,field_size):
        '''
        初始化方法，定义基本属性
        position：列表，初始坐标
        target：Pig对象，要抓的猪对象
        field_size：列表或元组，战场的尺寸（长，高）
        '''
        self.position = position
        self.target = target 
        self.field_width = field_size[0]
        self.field_height = field_size[1]

        field[position[0]][position[1]]=1 #在地图中将坐标值标记为1：人类

    def random_move(self):
        '''
        随机移动，并修改坐标
        '''
        while True:
            direction = random.randint(0,3)#0123，上下左右
            if direction == 0 and self.position[0]-1>=0 and field[self.position[0]-1][self.position[1]]==0: #如果向上有路可走
                self.position[0]-=1
                break
            elif direction == 1 and self.position[0]+1<self.field_height and field[self.position[0]+1][self.position[1]]==0: #如果向下有路可走
                self.position[0]+=1
                break
            elif direction == 2 and self.position[1]-1>=0 and field[self.position[0]][self.position[1]-1]==0: #如果向左有路可走
                self.position[1]-=1
                break
            elif direction == 3 and self.position[1]+1<self.field_width and field[self.position[0]][self.position[1]+1]==0: #如果向右有路可走
                self.position[1]+=1
                break

    def move(self):
        '''
        沿着目标猪的方向移动到新的地点，并修改自己的坐标。
        '''

        field[self.position[0]][self.position[1]]=0#当前的位置改为0：空地

        #先判断周围是否有空位置可走，且未超过边界
        if((self.position[0]+1<self.field_height and field[self.position[0]+1][self.position[1]]==0) or\
            (self.position[0]-1>=0 and field[self.position[0]-1][self.position[1]]==0) or\
            (self.position[1]+1<self.field_width and field[self.position[0]][self.position[1]+1]==0) or\
            (self.position[1]-1>=0 and field[self.position[0]][self.position[1]-1]==0)):
            
            #如果有位置可走，随机01来确定先横走还是竖走，1是横走
            if random.randint(0,1):  

                if self.position[1]==self.target.position[1]: #如果随机到横走，判断是否已经在同一列，如果在就没必要横走，直接竖走
                    #纵坐标相减判断是向上(>0)还是向下(<0)走，且要判断是否可走
                    if self.position[0]-self.target.position[0] > 0 and field[self.position[0]-1][self.position[1]]==0:
                        self.position[0]-=1 #更改坐标

                    elif self.position[0]-self.target.position[0] < 0 and field[self.position[0]+1][self.position[1]]==0:
                        self.position[0]+=1
                    #竖向也没得走，随机走一步
                    else:
                        self.random_move()

                #如果不在同一列，横坐标相减判断是向左(>0)还是向右(<0)走，且要判断是否可走
                elif self.position[1]-self.target.position[1] > 0 and field[self.position[0]][self.position[1]-1]==0:
                    self.position[1]-=1

                elif self.position[1]-self.target.position[1] < 0 and field[self.position[0]][self.position[1]+1]==0 : 
                    self.position[1]+=1

                #横向没得走，转向竖走，一样抄的上面的
                else:
                    if self.position[0]-self.target.position[0] > 0 and field[self.position[0]-1][self.position[1]]==0:
                        self.position[0]-=1
                    #纵坐标相减判断是向下(>0)还是向上(<0)走，且要判断是否可走
                    elif self.position[0]-self.target.position[0] < 0 and field[self.position[0]+1][self.position[1]]==0:
                        self.position[0]+=1
                    else:
                        self.random_move()

            #----------------------------------------------------------------------------------------------
            #如果随机到竖走，以下逻辑全部同上，仅修改方向
            else:
                if self.position[0]==self.target.position[0]: #如果随机到竖走，判断是否已经在同一行，如果在就没必要竖走，直接横走
                    #横坐标相减判断是向左(>0)还是向右(<0)走，且要判断是否可走
                    if self.position[1]-self.target.position[1] > 0 and field[self.position[0]][self.position[1]-1]==0:
                        self.position[1]-=1

                    elif self.position[1]-self.target.position[1] < 0 and field[self.position[0]][self.position[1]+1]==0 : 
                        self.position[1]+=1
                    else:
                        self.random_move()

                #如果不在同一行，纵坐标相减判断是向上(>0)还是向下(<0)走，且要判断是否可走
                elif self.position[0]-self.target.position[0] > 0 and field[self.position[0]-1][self.position[1]]==0:
                    self.position[0]-=1
                #纵坐标相减判断是向上(>0)还是向下(<0)走，且要判断是否可走
                elif self.position[0]-self.target.position[0] < 0 and field[self.position[0]+1][self.position[1]]==0:
                    self.position[0]+=1

                #竖向没得走，转向横走
                else:
                    if self.position[1]-self.target.position[1] > 0 and field[self.position[0]][self.position[1]-1]==0:
                        self.position[1]-=1
                    #横坐标相减判断是向左(>0)还是向右(<0)走，且要判断是否可走
                    elif self.position[1]-self.target.position[1] < 0 and field[self.position[0]][self.position[1]+1]==0:
                        self.position[1]+=1
                    else:
                        self.random_move()

        #将新修改的位置改为1：人类
        field[self.position[0]][self.position[1]]=1

    def check_target(self):
        '''
        检查目标猪是否已被抓获，如果已被抓获则重新选择目标。
        '''
        if self.target.flag :   #如果目标猪的flag为True，那么更换目标
            if len(pig_list):
                self.target=pig_list[random.randint(0,len(pig_list)-1)]#随机在pig_list里选一个
            else:
                print("猪抓完了")


#猪类
class Pig:
    '''
    position：列表，初始坐标
    num：整数，每头猪的编号
    field_size：列表或元组，战场的尺寸（长，高）
    '''

    count = 5000 #猪的数量
    speed = 1 #移动速度

    def __init__(self,position,num,field_size):
        '''
        初始化方法，定义基本属性
        position：列表，初始坐标
        num：整数，每头猪的编号
        field_size：列表或元组，战场的尺寸（长，高）
        '''
        self.position = position
        self.num = num 
        self.flag = False  #布尔值，猪被抓住的标志
        self.field_width = field_size[0]
        self.field_height = field_size[1]

        field[position[0]][position[1]]=2 #在地图中将坐标值标记为2：猪类

    def capture(self):
        '''
        判断自己是否被抓，当 周围的人类>=3 就认为被抓住，并且修改count的值
        '''
        human_num=0 #循环周围的格子，检查有多少人类
        for i in range(-1,2):
            for j in range(-1,2):
                if 0<=self.position[0]+i<field_height and 0<=self.position[1]+j<field_width and field[self.position[0]+i][self.position[1]+j]==1:
                    human_num+=1
        #大于等于三个人就认为猪被抓住了
        if human_num>=3:
            Pig.count-=1
            self.flag=True
            print("%d号猪被抓" % self.num)

    def move(self):
        '''
        随机移动到新的地点，并修改自己的坐标
        '''
        #先判断周围是否有空位置可走，且未超过边界
        if((self.position[0]+1<self.field_height and field[self.position[0]+1][self.position[1]]==0) or\
            (self.position[0]-1>=0 and field[self.position[0]-1][self.position[1]]==0) or\
            (self.position[1]+1<self.field_width and field[self.position[0]][self.position[1]+1]==0) or\
            (self.position[1]-1>=0 and field[self.position[0]][self.position[1]-1]==0)):
            
            field[self.position[0]][self.position[1]]=0#原来的位置改为0：空地

            while True:
                direction = random.randint(0,3)#0123，上下左右
                if direction == 0 and self.position[0]-1>=0 and field[self.position[0]-1][self.position[1]]==0: #如果向上有路可走
                    self.position[0]-=1
                    break
                elif direction == 1 and self.position[0]+1<self.field_height and field[self.position[0]+1][self.position[1]]==0: #如果向下有路可走
                    self.position[0]+=1
                    break
                elif direction == 2 and self.position[1]-1>=0 and field[self.position[0]][self.position[1]-1]==0: #如果向左有路可走
                    self.position[1]-=1
                    break
                elif direction == 3 and self.position[1]+1<self.field_width and field[self.position[0]][self.position[1]+1]==0: #如果向右有路可走
                    self.position[1]+=1
                    break

            field[self.position[0]][self.position[1]]=2#新的位置改为2：猪类


#程序开始前预先创建猪和人类对象，并添加进对应的列表
for i in range(100):
    for j in range(50):
        #相邻两头猪间隔为一个size
        pig_list.append(Pig([30+2*j,60+2*i] , i*10+j+1 , (field_width,field_height)))

for i in range(20):
    for j in range(50):
        #随机为每个人分配目标
        human_list.append(Human([20+2*j,10+2*i] , pig_list[random.randint(0,len(pig_list)-1)] , (field_width,field_height)))

#画出刚刚创建的猪和人类
for i in pig_list:
    #画布，颜色，矩形对象（坐标，尺寸），圆角半径
    pygame.draw.rect(screen,pig_color,pygame.Rect((i.position[1]*size,i.position[0]*size),(size,size)),border_radius=size//2)
for i in human_list:
    pygame.draw.rect(screen,human_color,pygame.Rect((i.position[1]*size,i.position[0]*size),(size,size)),border_radius=size//2)

pygame.display.update()  #更新屏幕
time.sleep(1)
frame=0#帧计数变量
draw_target_line=False#是否绘制目标线，默认不绘制

#主循环
#监听关闭事件和按键事件->时间计数+1 ->检查猪是否抓完->猪检查自己是否被抓，并删除已抓住的猪->人类检查目标状态并移动->猪移动->画出所有的猪和人
while True:
    for event in pygame.event.get():  #监听事件
        if event.type == pygame.QUIT: #如果关闭窗口则退出程序
            pygame.quit()
            sys.exit()
        #s键控制是否显示目标线
        if event.type == pygame.KEYDOWN and event.key == ord("s"):
            draw_target_line = not draw_target_line

    #背景覆盖
    screen.fill((0,0,0))

    #时间计数+1，并绘制提示文字
    frame+=1
    screen.blit(pygame.font.Font("SourceHanSansSC-Regular.otf",24).render("模拟时间%d分钟"%(frame*4),1,(64,255,212)),(350,2))
    screen.blit(pygame.font.Font("SourceHanSansSC-Regular.otf",22).render("蓝色：人类",1,human_color),(800,2))
    screen.blit(pygame.font.Font("SourceHanSansSC-Regular.otf",22).render("红色：猪",1,(255,92,201)),(950,2))

    #检查猪抓完没有，并绘制猪数量的提示文字
    if not len(pig_list):
        screen.blit(pygame.font.Font("SourceHanSansSC-Regular.otf",50).render("任务完成，全部的猪都抓到啦，耗时%d分钟"%(frame*4),1,(61,216,255)),(200,400))
        pygame.display.update()
        print(frame*4)
        time.sleep(3)
        pygame.quit()
        sys.exit()
    else:
        screen.blit(pygame.font.Font("SourceHanSansSC-Regular.otf",24).render("还剩%d只猪"%Pig.count,1,(255,92,201)),(580,2))

    #绘制是否开启目标线的提示文字
    if draw_target_line:
        screen.blit(pygame.font.Font("SourceHanSansSC-Regular.otf",22).render("按下S键显示目标线：已开启",1,(255,255,41)),(680,750))
    else:
        screen.blit(pygame.font.Font("SourceHanSansSC-Regular.otf",22).render("按下S键显示目标线：已隐藏",1,(255,255,41)),(680,750))

    #开始抓猪
    #把已经被抓住的猪从列表里删除
    for i in pig_list:
        i.capture()
        if i.flag:
            pig_list.remove(i)

    #所有人类检查自己的目标是否存活，并移动一步，画出对应猪和目标的提示线
    for i in human_list:
        i.check_target()
        i.move()
        if draw_target_line:
            pygame.draw.aaline(screen, target_line_color,(i.position[1]*size+size//2,i.position[0]*size+size//2),(i.target.position[1]*size+size//2,i.target.position[0]*size+size//2), 1)

    #计算人类和猪的移速比，时间到了所有的猪移动一步
    if frame%(Human.speed//Pig.speed)==0:
        for i in pig_list:
            i.move()

    #画出所有的人类和猪
    for i in human_list:
        pygame.draw.rect(screen , human_color ,pygame.Rect((i.position[1]*size,i.position[0]*size),(size,size)),border_radius=size//2)
    for i in pig_list:
        pygame.draw.rect(screen , pig_color ,pygame.Rect((i.position[1]*size,i.position[0]*size),(size,size)),border_radius=size//2)

    #底部签名及信息
    screen.blit(pygame.font.Font("SourceHanSansSC-Regular.otf",22).render("幽蓝伊梦",1,(92,255,255)),(1050,750))
    screen.blit(pygame.font.Font("SourceHanSansSC-Regular.otf",22).render("点个赞吧",1,(92,255,255)),(280,750))
    screen.blit(pygame.font.Font("SourceHanSansSC-Regular.otf",22).render("投个币吧(*^▽^*)",1,(92,255,255)),(430,750))

    #更新屏幕
    pygame.display.update()
    #运行速度
    pygame.time.Clock().tick(60)
