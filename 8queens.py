import matplotlib.pyplot as plt
import numpy as np
import pandas

from matplotlib.table import Table
from matplotlib.text import Text

cnt=0
lst=pandas.DataFrame()
lst_dup=pandas.DataFrame()
dct={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
aa=['a','b','c','d','e','f','g','h']

def checkerboard_table(data, text, fmt='{:.0f}', bkg_colors=['black', 'white']):
   # plt.style.use('seaborn-colorblind')
   # print(type(data),data)
    fig, ax = plt.subplots()
    ax.set_axis_off()
    fig.suptitle(text)
    tb = Table(ax, bbox=[0,0,1,1])
   # print(tb.Cell.properties())

    nrows, ncols = data.shape
    width, height = 1.0 / ncols, 1.0 / nrows
    # Add cells
    for (i,j), val in np.ndenumerate(data):
        # Index either the first or second item of bkg_colors based on
        # a checker board pattern
        idx = [j % 2, (j + 1) % 2][i % 2]
        color = bkg_colors[idx]
        color1 = ['white', 'blue'][idx]
        if val==0:
            txt=""
        else:
#            txt=fmt.format(val)
            txt='♛'
        tb.add_cell(i, j, width, height, text=txt, 
                    loc='center', facecolor=color1)

    # Row Labels...
    for i, label in enumerate(data.index):
        tb.add_cell(i, -1, width, height, text=label, loc='right', 
                    edgecolor='none', facecolor='none')
    # Column Labels...
    for j, label in enumerate(data.columns):
        tb.add_cell(-1, j, width, height/2, text=label, loc='center', 
                           edgecolor='none', facecolor='none')
    ax.add_table(tb)
    return fig

def main():
    global cnt, lst
#    image = np.zeros(64).reshape((8,8))
#    for i in range(0,8):
#        for j in range(0,8):
#            if (i%2==j%2):
   #             image[i*8+j]=1
#                image[i][j]=1
    img0 = np.zeros(64).reshape((8,8))
    print('try_for(00):',try_for((0,0),0,img0))
    img0 = np.zeros(64).reshape((8,8))
    print('try_for(01):',try_for((0,1),0,img0))
    img0 = np.zeros(64).reshape((8,8))
    print('try_for(02):',try_for((0,2),0,img0))
    img0 = np.zeros(64).reshape((8,8))
    print('try_for(03):',try_for((0,3),0,img0))
#    print(lst)
#    print('lst_dup:',lst_dup)
    n=0
    for idx,x in lst.iterrows():
        n+=1
        print('solution', n, ':', x[0])
        img = np.zeros(64).reshape((8,8))
        for i in range(8):
            img[i][dct[x[0][i:i+1]]]=8
#            img[i][dct[x[0][i:i+1]]]='♛'
        data = pandas.DataFrame(img, 
                columns=['a','b','c','d','e','f','g','h'])
#    df['age'] = df['age'].apply(lambda x: 1 if 25 <=  x <= 35 else 0)
#                data = data.apply(lambda x,y: x,y in enumerate(data) if data[y][x]==8 else 0)
        checkerboard_table(data, f"solution{n}:{x[0]}")
        plt.show()

def set_img(root,img):
    for (i,j) in enumerate(img):
        for k in range(0,8):
            if (i==root[0]):
                if (k==root[1]):
                    j[k]=8
                else:
                    j[k]=1
            else:
                if k==root[1]:
                    j[k]=1
                if i-root[0]==k-root[1]:
                    j[k]=1
                if k==root[1]-i+root[0]:
                    j[k]=1

def copy(im):
    im1=np.zeros(64).reshape((8,8))
    for i1 in range(0,8):
        for j1 in range(0,8):
            im1[i1][j1]=im[i1][j1]
    return im1

def mirror(str):
    new_str=""
    for i in range(8):
        new_str += str[7-i]
    return new_str
        
def found_str(str):
#    print('found_str',str)
    for idx, x in lst.iterrows():
#        print('x:', x[0], x[1], str)
        for y in range(4):
            if (x[y]==str) | (x[y]==mirror(str)):
#            print('x:', x[0], x[1], x[2], x[3], x[4], str)
                return True
    return False

def rotate(str):
    global aa, dct
    new_str=['a','b','c','d','e','f','g','h']
    for i in range(8):
        j=dct[str[i:i+1]]
        new_str[j] = aa[7-i]
    return ''.join(new_str)

def flip(str):
    global aa, dct
    new_str=['a','b','c','d','e','f','g','h']
    for i in range(8):
        j=dct[str[i:i+1]]
        new_str[7-i] = aa[7-j]
    return ''.join(new_str)

def store_str(str):
    global lst, lst_dup, cnt
    if lst.empty:
        cnt += 1
        lst = pandas.DataFrame([[str,flip(str),rotate(str),flip(rotate(str))]])
#        rotate_str(str)
    else:
        if found_str(str):
            if lst_dup.empty:
                lst_dup = pandas.DataFrame([[str]])
            else:
#                lst_dup = lst_dup.append([[str]])
                lst_dup = pandas.concat([lst_dup, pandas.DataFrame([[str]])])
        else:
            cnt +=1
#            lst = lst.append([[str,flip(str),rotate(str),flip(rotate(str))]])
            lst = pandas.concat([lst, pandas.DataFrame(
                [[str,flip(str),rotate(str),flip(rotate(str))]])])

def try_for(spot,layer,img):
    global cnt, lst, aa, dct
    if img[spot[0]][spot[1]]==0:
        set_img(spot,img)
        img_sav=copy(img)
        rtn=0
        for jj in range(0,8):
            if rtn==-2:
#                print('-2',layer,spot)
                img=copy(img_sav)
            if spot[0]<7:
                rtn=try_for((spot[0]+1,jj),layer+1,img)
            else:
#                print('success')
#                print(img)
                str=""
                for x in range(0,8):
                    for y in range(0,8):
                        if img[x][y]==8:
#                        if img[x][y]=='♛':
                            str += aa[y]
                store_str(str)
                return 0
        if rtn==-2:
            return -2
    else:
        if spot[1]==7:
            return -2
        else:
            return -1

if __name__ == '__main__':
    main()
