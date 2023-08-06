import math


def SimpleConsoleMenu(menuName,menuItems,autoAddQuit = False,onlyReturnNumber = True, allowedCharacters = ''):
    """
    Makes a menu

    parameters:
        menuName          - Required  : name of the menu (Str)
        menuItems         - Required  : menu items, separated with ';' (Str)
        autoAddQuit       - Optional  : automatically add a quit option (Bool)
        onlyReturnNumber  - Optional  : only numbers are allowed to return (Bool)
        allowedCharacters - Optional  : specifier which character(s) are allowed if onlyReturnNumber is False, separated with ';' (str)
    """
    chooseLoop = True
    menuItemsList = []
    allowedCharactersList = []
    menuItemsList = str(menuItems).split(';')
    if allowedCharacters != '':
        allowedCharactersList = str(allowedCharacters).split(';')
    if autoAddQuit:
        menuItemsList.append('Quit')
    menuNumber = 1
    chooseAmount = 0
    menuNameLength = len(menuName) + 2
    menuNameLength = 76 - menuNameLength
    menuNameLength /= 2
    if (menuNameLength % 2) == 0:
        #even
        print(int(menuNameLength)*'-',menuName,int(menuNameLength)*'-')
    else:
        #uneven
        menuNameLength1 = round(menuNameLength)
        menuNameLength2 = int(math.ceil(menuNameLength))
        print(int(menuNameLength1)*'-',menuName,int(menuNameLength2)*'-')
    for x in menuItemsList:
        print(f'{menuNumber}. {x}')
        menuNumber += 1
    print(76*'-')
    while chooseLoop:
        choose = input(f'Enter a number:')
        if onlyReturnNumber:
            if choose.isdigit():
                chooseLoop = False
        else:
            if choose != '' and choose in allowedCharactersList:
                chooseLoop = False
        if chooseAmount >= 20 and chooseLoop:
            menuNumber = 1
            if (menuNameLength % 2) == 0:
                #even
                print(int(menuNameLength)*'-',menuName,int(menuNameLength)*'-')
            else:
                #uneven
                menuNameLength1 = round(menuNameLength)
                menuNameLength2 = int(math.ceil(menuNameLength))
                print(int(menuNameLength1)*'-',menuName,int(menuNameLength2)*'-')
            for x in menuItemsList:
                print(f'{menuNumber}. {x}')
                menuNumber += 1
            print(76*'-')
            chooseAmount = 1
        chooseAmount += 1
    if int(choose) == menuNumber-1:
        quit()
    else:
        if onlyReturnNumber:
            return int(choose)
        else:
            if allowedCharacters != '':
                if choose in allowedCharactersList:
                    return choose
                    