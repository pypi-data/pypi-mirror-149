# Simple console menu

This is a simple console menu

## SimpleConsoleMenu
---
The first menu is the `SimpleConsoleMenu`. <br>
You can use it by first importing the right file: 
```python
from simple_console_menu import Menu
```

And if you want to use it you can do this:
```python
menu = Menu.SimpleConsoleMenu(menuName,menuItems,inputQuestion,autoAddQuit,onlyReturnNumber, allowedCharacters = '', acceptedQuitCharacters = '')
```

With these parameters :

    menuName               - Required : name of the menu (Str)
    menuItems              - Required : menu items, separated with ';' (Str)
    inputQuestion          - Required : Question input (Str)
    autoAddQuit            - Optional : automatically add a quit option (Bool)
    onlyReturnNumber       - Optional : only numbers are allowed to return (Bool)
    allowedCharacters      - Optional  : specifier which character(s) are allowed if onlyReturnNumber is False, separated with ';' (str)
    acceptedQuitCharacters - Optional  : specifier which character is allowed if onlyReturnNumber is False for quit (str)

full example:
```python
from simple_console_menu import Menu

menuNumber = Menu.SimpleConsoleMenu('menu','item1;item2;item3;item4;item5',"Number:",True)

if menuNumber == 1:
    print('item1')
elif menuNumber == 2:
    print('item2')
elif menuNumber == 3:
    print('item3')
elif menuNumber == 4:
    print('item4')
elif menuNumber == 5:
    print('item5')
```

And this wil display

```
----------------------------------- menu -----------------------------------
1. item1
2. item2
3. item3
4. item4
5. item5
6. Quit
----------------------------------------------------------------------------
Number:1
item1
```

There is also `SimpleConsoleMenuBlock` which works the same as `SimpleConsoleMenu` but looks like this:

```
╭────────────────────────────────── menu ──────────────────────────────────╮
│1. item1                                                                  │
│2. item2                                                                  │
│3. item3                                                                  │
│4. item4                                                                  │
│5. item5                                                                  │
│6. Quit                                                                   │
╰──────────────────────────────────────────────────────────────────────────╯
Number:
```