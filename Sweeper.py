from subprocess import PIPE, call
from time import sleep
from matplotlib import pyplot as plt
from numpy import where
from PIL.ImageGrab import grab
from win32con import MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP, KEYEVENTF_KEYUP
from cv2 import COLOR_BGR2GRAY, TM_CCOEFF_NORMED, cvtColor, imread, imwrite, matchTemplate, rectangle
from win32api import SetCursorPos, mouse_event, keybd_event
from win32gui import SetForegroundWindow, ShowWindow, EnumWindows, GetWindowText




#focus on program
def Focus(window):

    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, GetWindowText(hwnd)))

    top_windows = []
    EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if window in i[1].lower():
            ShowWindow(i[0],5)
            SetForegroundWindow(i[0])
            return




#dump process memory
def GetMem():
    cmd = "del mine.dmp"
    call(cmd,shell=True,stdout=PIPE)
    cmd = "procdump -ma Minesweeper.exe mine"
    call(cmd,shell=True,stdout=PIPE)


#scan memory for board and game mode
def FindBoard():
    #load memory
    with open("mine.dmp","rb") as dump:
        dump=dump.read()
        #scan for start of easy board
        target=dump.find((b"\x10"*11+b"\x0F"*21))
        if target!=-1:
            #if board set board and game mode
            result=dump[target:target+320]
            mode="easy"
        #scan for start of medium board
        target=dump.find((b"\x10"*18+b"\x0F"*14))
        if target!=-1:
            #if board set board and game mode
            result=dump[target:target+550]
            mode="medium"
        #scan for start of hard board
        target=dump.find((b"\x10"*33+b"\x0F"))
        if target!=-1:
            #if board set board and game mode
            result=dump[target:target+570]
            mode="hard"
        #return board and game mode
        return mode,result


#exploit easy game mode
def ExploitEasy(result,cords):
    times=0
    p=True
    board=[]
    #format board data
    for x in result:
        if times==10 and p==True:
            p=False
            times=0
        elif times==22 and p==False:
            times=0
            p=True
        #structure useful board data
        if p==True:
            if MapBoard(x)!="?":
                board.append(MapBoard(x))
        times+=1
    #return processed board data
    return board
    

#exploit meduim game mode
def ExploitMedium(result,cords):
    times=0
    p=True
    board=[]
    #format board data
    for x in result:
        if times==17 and p==True:
            p=False
            times=0
        elif times==15 and p==False:
            times=0
            p=True
        #structure useful board data
        if p==True:
            if MapBoard(x)!="?":
                board.append(MapBoard(x))
        times+=1
    #return processed board data
    return board

#exploit hard game mode
def ExploitHard(result,cords):
    board=[]
    for x in result:
        #structure useful board data
        if MapBoard(x)!="?":
            board.append(MapBoard(x))
    #return processed board data
    return board


#change hex to board pieces
def MapBoard(value):
    if value==143:return"B"
    elif value==15:return"X"
    else: return "?"


#play board
def Play(level,board,cords):
    #iterate through board coordinates and pieces
    for (space,location),data in zip(level.items(),board):
        #click every space that doesnt have a bomb
        if data!="B": Click((cords[0]+location[0],cords[1]+location[1]))


#easy board coordinates
easy={
      1: (18, 105),   2: (34, 105),   3: (50, 105),   4: (66, 105),   5: (82, 105),   6: (98, 105),   7: (114, 105),   8: (130, 105),   9: (146, 105), 
     31: (18, 121),  32: (34, 121),  33: (50, 121),  34: (66, 121),  35: (82, 121),  36: (98, 121),  37: (114, 121),  38: (130, 121),  39: (146, 121), 
     61: (18, 137),  62: (34, 137),  63: (50, 137),  64: (66, 137),  65: (82, 137),  66: (98, 137),  67: (114, 137),  68: (130, 137),  69: (146, 137), 
     91: (18, 153),  92: (34, 153),  93: (50, 153),  94: (66, 153),  95: (82, 153),  96: (98, 153),  97: (114, 153),  98: (130, 153),  99: (146, 153), 
    121: (18, 169), 122: (34, 169), 123: (50, 169), 124: (66, 169), 125: (82, 169), 126: (98, 169), 127: (114, 169), 128: (130, 169), 129: (146, 169), 
    151: (18, 185), 152: (34, 185), 153: (50, 185), 154: (66, 185), 155: (82, 185), 156: (98, 185), 157: (114, 185), 158: (130, 185), 159: (146, 185), 
    181: (18, 201), 182: (34, 201), 183: (50, 201), 184: (66, 201), 185: (82, 201), 186: (98, 201), 187: (114, 201), 188: (130, 201), 189: (146, 201), 
    211: (18, 217), 212: (34, 217), 213: (50, 217), 214: (66, 217), 215: (82, 217), 216: (98, 217), 217: (114, 217), 218: (130, 217), 219: (146, 217), 
    241: (18, 233), 242: (34, 233), 243: (50, 233), 244: (66, 233), 245: (82, 233), 246: (98, 233), 247: (114, 233), 248: (130, 233), 249: (146, 233), 
    }
    
#medium board coordinates
medium={
      1: (18, 105),   2: (34, 105),   3: (50, 105),   4: (66, 105),   5: (82, 105),   6: (98, 105),   7: (114, 105),   8: (130, 105),   9: (146, 105),  10: (162, 105),  11: (178, 105),  12: (194, 105),  13: (210, 105),  14: (226, 105),  15: (242, 105),  16: (258, 105), 
     31: (18, 121),  32: (34, 121),  33: (50, 121),  34: (66, 121),  35: (82, 121),  36: (98, 121),  37: (114, 121),  38: (130, 121),  39: (146, 121),  40: (162, 121),  41: (178, 121),  42: (194, 121),  43: (210, 121),  44: (226, 121),  45: (242, 121),  46: (258, 121), 
     61: (18, 137),  62: (34, 137),  63: (50, 137),  64: (66, 137),  65: (82, 137),  66: (98, 137),  67: (114, 137),  68: (130, 137),  69: (146, 137),  70: (162, 137),  71: (178, 137),  72: (194, 137),  73: (210, 137),  74: (226, 137),  75: (242, 137),  76: (258, 137), 
     91: (18, 153),  92: (34, 153),  93: (50, 153),  94: (66, 153),  95: (82, 153),  96: (98, 153),  97: (114, 153),  98: (130, 153),  99: (146, 153), 100: (162, 153), 101: (178, 153), 102: (194, 153), 103: (210, 153), 104: (226, 153), 105: (242, 153), 106: (258, 153), 
    121: (18, 169), 122: (34, 169), 123: (50, 169), 124: (66, 169), 125: (82, 169), 126: (98, 169), 127: (114, 169), 128: (130, 169), 129: (146, 169), 130: (162, 169), 131: (178, 169), 132: (194, 169), 133: (210, 169), 134: (226, 169), 135: (242, 169), 136: (258, 169), 
    151: (18, 185), 152: (34, 185), 153: (50, 185), 154: (66, 185), 155: (82, 185), 156: (98, 185), 157: (114, 185), 158: (130, 185), 159: (146, 185), 160: (162, 185), 161: (178, 185), 162: (194, 185), 163: (210, 185), 164: (226, 185), 165: (242, 185), 166: (258, 185), 
    181: (18, 201), 182: (34, 201), 183: (50, 201), 184: (66, 201), 185: (82, 201), 186: (98, 201), 187: (114, 201), 188: (130, 201), 189: (146, 201), 190: (162, 201), 191: (178, 201), 192: (194, 201), 193: (210, 201), 194: (226, 201), 195: (242, 201), 196: (258, 201), 
    211: (18, 217), 212: (34, 217), 213: (50, 217), 214: (66, 217), 215: (82, 217), 216: (98, 217), 217: (114, 217), 218: (130, 217), 219: (146, 217), 220: (162, 217), 221: (178, 217), 222: (194, 217), 223: (210, 217), 224: (226, 217), 225: (242, 217), 226: (258, 217), 
    241: (18, 233), 242: (34, 233), 243: (50, 233), 244: (66, 233), 245: (82, 233), 246: (98, 233), 247: (114, 233), 248: (130, 233), 249: (146, 233), 250: (162, 233), 251: (178, 233), 252: (194, 233), 253: (210, 233), 254: (226, 233), 255: (242, 233), 256: (258, 233), 
    271: (18, 249), 272: (34, 249), 273: (50, 249), 274: (66, 249), 275: (82, 249), 276: (98, 249), 277: (114, 249), 278: (130, 249), 279: (146, 249), 280: (162, 249), 281: (178, 249), 282: (194, 249), 283: (210, 249), 284: (226, 249), 285: (242, 249), 286: (258, 249), 
    301: (18, 265), 302: (34, 265), 303: (50, 265), 304: (66, 265), 305: (82, 265), 306: (98, 265), 307: (114, 265), 308: (130, 265), 309: (146, 265), 310: (162, 265), 311: (178, 265), 312: (194, 265), 313: (210, 265), 314: (226, 265), 315: (242, 265), 316: (258, 265), 
    331: (18, 281), 332: (34, 281), 333: (50, 281), 334: (66, 281), 335: (82, 281), 336: (98, 281), 337: (114, 281), 338: (130, 281), 339: (146, 281), 340: (162, 281), 341: (178, 281), 342: (194, 281), 343: (210, 281), 344: (226, 281), 345: (242, 281), 346: (258, 281), 
    361: (18, 297), 362: (34, 297), 363: (50, 297), 364: (66, 297), 365: (82, 297), 366: (98, 297), 367: (114, 297), 368: (130, 297), 369: (146, 297), 370: (162, 297), 371: (178, 297), 372: (194, 297), 373: (210, 297), 374: (226, 297), 375: (242, 297), 376: (258, 297), 
    391: (18, 313), 392: (34, 313), 393: (50, 313), 394: (66, 313), 395: (82, 313), 396: (98, 313), 397: (114, 313), 398: (130, 313), 399: (146, 313), 400: (162, 313), 401: (178, 313), 402: (194, 313), 403: (210, 313), 404: (226, 313), 405: (242, 313), 406: (258, 313), 
    421: (18, 329), 422: (34, 329), 423: (50, 329), 424: (66, 329), 425: (82, 329), 426: (98, 329), 427: (114, 329), 428: (130, 329), 429: (146, 329), 430: (162, 329), 431: (178, 329), 432: (194, 329), 433: (210, 329), 434: (226, 329), 435: (242, 329), 436: (258, 329), 
    451: (18, 345), 452: (34, 345), 453: (50, 345), 454: (66, 345), 455: (82, 345), 456: (98, 345), 457: (114, 345), 458: (130, 345), 459: (146, 345), 460: (162, 345), 461: (178, 345), 462: (194, 345), 463: (210, 345), 464: (226, 345), 465: (242, 345), 466: (258, 345)
    }

#hard board coordinates
hard={
      1: (18, 105),   2: (34, 105),   3: (50, 105),   4: (66, 105),   5: (82, 105),   6: (98, 105),   7: (114, 105),   8: (130, 105),   9: (146, 105),  10: (162, 105),  11: (178, 105),  12: (194, 105),  13: (210, 105),  14: (226, 105),  15: (242, 105),  16: (258, 105),  17: (274, 105),  18: (290, 105),  19: (306, 105),  20: (322, 105),  21: (338, 105),  22: (354, 105),  23: (370, 105),  24: (386, 105),  25: (402, 105),  26: (418, 105),  27: (434, 105),  28: (450, 105),  29: (466, 105),  30: (482, 105), 
     31: (18, 121),  32: (34, 121),  33: (50, 121),  34: (66, 121),  35: (82, 121),  36: (98, 121),  37: (114, 121),  38: (130, 121),  39: (146, 121),  40: (162, 121),  41: (178, 121),  42: (194, 121),  43: (210, 121),  44: (226, 121),  45: (242, 121),  46: (258, 121),  47: (274, 121),  48: (290, 121),  49: (306, 121),  50: (322, 121),  51: (338, 121),  52: (354, 121),  53: (370, 121),  54: (386, 121),  55: (402, 121),  56: (418, 121),  57: (434, 121),  58: (450, 121),  59: (466, 121),  60: (482, 121), 
     61: (18, 137),  62: (34, 137),  63: (50, 137),  64: (66, 137),  65: (82, 137),  66: (98, 137),  67: (114, 137),  68: (130, 137),  69: (146, 137),  70: (162, 137),  71: (178, 137),  72: (194, 137),  73: (210, 137),  74: (226, 137),  75: (242, 137),  76: (258, 137),  77: (274, 137),  78: (290, 137),  79: (306, 137),  80: (322, 137),  81: (338, 137),  82: (354, 137),  83: (370, 137),  84: (386, 137),  85: (402, 137),  86: (418, 137),  87: (434, 137),  88: (450, 137),  89: (466, 137),  90: (482, 137), 
     91: (18, 153),  92: (34, 153),  93: (50, 153),  94: (66, 153),  95: (82, 153),  96: (98, 153),  97: (114, 153),  98: (130, 153),  99: (146, 153), 100: (162, 153), 101: (178, 153), 102: (194, 153), 103: (210, 153), 104: (226, 153), 105: (242, 153), 106: (258, 153), 107: (274, 153), 108: (290, 153), 109: (306, 153), 110: (322, 153), 111: (338, 153), 112: (354, 153), 113: (370, 153), 114: (386, 153), 115: (402, 153), 116: (418, 153), 117: (434, 153), 118: (450, 153), 119: (466, 153), 120: (482, 153), 
    121: (18, 169), 122: (34, 169), 123: (50, 169), 124: (66, 169), 125: (82, 169), 126: (98, 169), 127: (114, 169), 128: (130, 169), 129: (146, 169), 130: (162, 169), 131: (178, 169), 132: (194, 169), 133: (210, 169), 134: (226, 169), 135: (242, 169), 136: (258, 169), 137: (274, 169), 138: (290, 169), 139: (306, 169), 140: (322, 169), 141: (338, 169), 142: (354, 169), 143: (370, 169), 144: (386, 169), 145: (402, 169), 146: (418, 169), 147: (434, 169), 148: (450, 169), 149: (466, 169), 150: (482, 169), 
    151: (18, 185), 152: (34, 185), 153: (50, 185), 154: (66, 185), 155: (82, 185), 156: (98, 185), 157: (114, 185), 158: (130, 185), 159: (146, 185), 160: (162, 185), 161: (178, 185), 162: (194, 185), 163: (210, 185), 164: (226, 185), 165: (242, 185), 166: (258, 185), 167: (274, 185), 168: (290, 185), 169: (306, 185), 170: (322, 185), 171: (338, 185), 172: (354, 185), 173: (370, 185), 174: (386, 185), 175: (402, 185), 176: (418, 185), 177: (434, 185), 178: (450, 185), 179: (466, 185), 180: (482, 185), 
    181: (18, 201), 182: (34, 201), 183: (50, 201), 184: (66, 201), 185: (82, 201), 186: (98, 201), 187: (114, 201), 188: (130, 201), 189: (146, 201), 190: (162, 201), 191: (178, 201), 192: (194, 201), 193: (210, 201), 194: (226, 201), 195: (242, 201), 196: (258, 201), 197: (274, 201), 198: (290, 201), 199: (306, 201), 200: (322, 201), 201: (338, 201), 202: (354, 201), 203: (370, 201), 204: (386, 201), 205: (402, 201), 206: (418, 201), 207: (434, 201), 208: (450, 201), 209: (466, 201), 210: (482, 201), 
    211: (18, 217), 212: (34, 217), 213: (50, 217), 214: (66, 217), 215: (82, 217), 216: (98, 217), 217: (114, 217), 218: (130, 217), 219: (146, 217), 220: (162, 217), 221: (178, 217), 222: (194, 217), 223: (210, 217), 224: (226, 217), 225: (242, 217), 226: (258, 217), 227: (274, 217), 228: (290, 217), 229: (306, 217), 230: (322, 217), 231: (338, 217), 232: (354, 217), 233: (370, 217), 234: (386, 217), 235: (402, 217), 236: (418, 217), 237: (434, 217), 238: (450, 217), 239: (466, 217), 240: (482, 217), 
    241: (18, 233), 242: (34, 233), 243: (50, 233), 244: (66, 233), 245: (82, 233), 246: (98, 233), 247: (114, 233), 248: (130, 233), 249: (146, 233), 250: (162, 233), 251: (178, 233), 252: (194, 233), 253: (210, 233), 254: (226, 233), 255: (242, 233), 256: (258, 233), 257: (274, 233), 258: (290, 233), 259: (306, 233), 260: (322, 233), 261: (338, 233), 262: (354, 233), 263: (370, 233), 264: (386, 233), 265: (402, 233), 266: (418, 233), 267: (434, 233), 268: (450, 233), 269: (466, 233), 270: (482, 233), 
    271: (18, 249), 272: (34, 249), 273: (50, 249), 274: (66, 249), 275: (82, 249), 276: (98, 249), 277: (114, 249), 278: (130, 249), 279: (146, 249), 280: (162, 249), 281: (178, 249), 282: (194, 249), 283: (210, 249), 284: (226, 249), 285: (242, 249), 286: (258, 249), 287: (274, 249), 288: (290, 249), 289: (306, 249), 290: (322, 249), 291: (338, 249), 292: (354, 249), 293: (370, 249), 294: (386, 249), 295: (402, 249), 296: (418, 249), 297: (434, 249), 298: (450, 249), 299: (466, 249), 300: (482, 249), 
    301: (18, 265), 302: (34, 265), 303: (50, 265), 304: (66, 265), 305: (82, 265), 306: (98, 265), 307: (114, 265), 308: (130, 265), 309: (146, 265), 310: (162, 265), 311: (178, 265), 312: (194, 265), 313: (210, 265), 314: (226, 265), 315: (242, 265), 316: (258, 265), 317: (274, 265), 318: (290, 265), 319: (306, 265), 320: (322, 265), 321: (338, 265), 322: (354, 265), 323: (370, 265), 324: (386, 265), 325: (402, 265), 326: (418, 265), 327: (434, 265), 328: (450, 265), 329: (466, 265), 330: (482, 265), 
    331: (18, 281), 332: (34, 281), 333: (50, 281), 334: (66, 281), 335: (82, 281), 336: (98, 281), 337: (114, 281), 338: (130, 281), 339: (146, 281), 340: (162, 281), 341: (178, 281), 342: (194, 281), 343: (210, 281), 344: (226, 281), 345: (242, 281), 346: (258, 281), 347: (274, 281), 348: (290, 281), 349: (306, 281), 350: (322, 281), 351: (338, 281), 352: (354, 281), 353: (370, 281), 354: (386, 281), 355: (402, 281), 356: (418, 281), 357: (434, 281), 358: (450, 281), 359: (466, 281), 360: (482, 281), 
    361: (18, 297), 362: (34, 297), 363: (50, 297), 364: (66, 297), 365: (82, 297), 366: (98, 297), 367: (114, 297), 368: (130, 297), 369: (146, 297), 370: (162, 297), 371: (178, 297), 372: (194, 297), 373: (210, 297), 374: (226, 297), 375: (242, 297), 376: (258, 297), 377: (274, 297), 378: (290, 297), 379: (306, 297), 380: (322, 297), 381: (338, 297), 382: (354, 297), 383: (370, 297), 384: (386, 297), 385: (402, 297), 386: (418, 297), 387: (434, 297), 388: (450, 297), 389: (466, 297), 390: (482, 297), 
    391: (18, 313), 392: (34, 313), 393: (50, 313), 394: (66, 313), 395: (82, 313), 396: (98, 313), 397: (114, 313), 398: (130, 313), 399: (146, 313), 400: (162, 313), 401: (178, 313), 402: (194, 313), 403: (210, 313), 404: (226, 313), 405: (242, 313), 406: (258, 313), 407: (274, 313), 408: (290, 313), 409: (306, 313), 410: (322, 313), 411: (338, 313), 412: (354, 313), 413: (370, 313), 414: (386, 313), 415: (402, 313), 416: (418, 313), 417: (434, 313), 418: (450, 313), 419: (466, 313), 420: (482, 313), 
    421: (18, 329), 422: (34, 329), 423: (50, 329), 424: (66, 329), 425: (82, 329), 426: (98, 329), 427: (114, 329), 428: (130, 329), 429: (146, 329), 430: (162, 329), 431: (178, 329), 432: (194, 329), 433: (210, 329), 434: (226, 329), 435: (242, 329), 436: (258, 329), 437: (274, 329), 438: (290, 329), 439: (306, 329), 440: (322, 329), 441: (338, 329), 442: (354, 329), 443: (370, 329), 444: (386, 329), 445: (402, 329), 446: (418, 329), 447: (434, 329), 448: (450, 329), 449: (466, 329), 450: (482, 329), 
    451: (18, 345), 452: (34, 345), 453: (50, 345), 454: (66, 345), 455: (82, 345), 456: (98, 345), 457: (114, 345), 458: (130, 345), 459: (146, 345), 460: (162, 345), 461: (178, 345), 462: (194, 345), 463: (210, 345), 464: (226, 345), 465: (242, 345), 466: (258, 345), 467: (274, 345), 468: (290, 345), 469: (306, 345), 470: (322, 345), 471: (338, 345), 472: (354, 345), 473: (370, 345), 474: (386, 345), 475: (402, 345), 476: (418, 345), 477: (434, 345), 478: (450, 345), 479: (466, 345), 480: (482, 345)
    }



#take screenshot
def Screenshot():
    # grab fullscreen
    im = grab()
    # save image file
    im.save('screen.png')



#board templates to scan for
class Icon():
    easy="easy.png"
    medium="medium.png"
    hard="hard.png"
    success="success2.png"
    incomplete="success.png"


#test scan for icon
def Scan(icon,threshold=0.8):
    #get screenshot
    Screenshot()
    #read screenshot
    img_rgb = imread('screen.png')
    #convert to grey
    img_gray = cvtColor(img_rgb, COLOR_BGR2GRAY)
    #read template
    template = imread(icon,0)
    #get dimensions of screen
    w, h = template.shape[::-1]
    #scan screen for template
    res = matchTemplate(img_gray,template,TM_CCOEFF_NORMED)
    #get location of match
    loc = where( res >= threshold)
    #get coordinates
    for pt in zip(*loc[::-1]):
        cords=pt[0],pt[1]
        #return coordinates
        return cords
    #return false if nothing found
    return False
    #first number is horizontal left to right
    #second number is vertical from top to bottom
    #exports upper left corner


#click mouse at coordinates
def Click(cords,times=1):
    for click in range(times):
        x=cords[0]
        y=cords[1]
        SetCursorPos((x,y))
        mouse_event(MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        mouse_event(MOUSEEVENTF_LEFTUP,x,y,0,0)


def Reset():
    keybd_event(0x71,0,0,0)    #F2
    sleep(0.1)
    keybd_event(0x71,0,KEYEVENTF_KEYUP,0) #F2 up

def Main():
    call("cls",shell=True)
    for x in range(1):
        #focus onto program
        Focus("Minesweeper")
        #reset program
        Reset()
        #dump process memory
        GetMem()
        #find board in dump
        mode,result=FindBoard()
        #get screen
        Screenshot()
        #find board on screen
        cords=Scan(Icon.easy)
        #check mode and exploit mode
        if mode=="easy":
            Play(easy,ExploitEasy(result,Scan(Icon.easy)),cords)
        elif mode=="medium":
            Play(medium,ExploitMedium(result,Scan(Icon.medium)),cords)
        elif mode=="hard":
            Play(hard,ExploitHard(result,Scan(Icon.hard)),cords)
        #get screen
        Screenshot()
        if Scan(Icon.success,0.99)!=False:print("Success!")
        elif Scan(Icon.incomplete,0.99)!=False:print("DNF")
        else: print("Failure")


if __name__=="__main__":
    Main()

"""
while True:
    try:
        GetMem()
        mode,result=Find()
        if mode=="easy":ExploitEasy(result)
        elif mode=="medium":ExploitMedium(result)
        elif mode=="hard":ExploitHard(result)
        else: sleep(5)
    except:exit()
"""
