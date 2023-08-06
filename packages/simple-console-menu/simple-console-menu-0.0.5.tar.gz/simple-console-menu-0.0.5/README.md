# Simple console menu

This is a simple console menu

## SimpleConsoleMenu
---
The first (and only) menu is the `SimpleConsoleMenu`. <br>
You can use it by first importing the right file: 
```python
from simple_console_menu import Menu
```

And if you want to use it you can do this:
```python
menu = Menu.SimpleConsoleMenu(menuName,menuItems,autoAddQuit,onlyReturnNumber, allowedCharacters = '')
```

With these parameters :

    menuName           - Required : name of the menu (Str)
    menuItems          - Required : menu items, separated with ';' (Str)
    autoAddQuit        - Optional : automatically add a quit option (Bool)
    onlyReturnNumber   - Optional : only numbers are allowed to return (Bool)
    allowedCharacters  - Optional  : specifier which character(s) are allowed if onlyReturnNumber is False, separated with ';' (str)

full example:
```python
from simple_console_menu import Menu

menuNumber = Menu.SimpleConsoleMenu('menu','item1;item2;item3;item4;item5',True)

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
