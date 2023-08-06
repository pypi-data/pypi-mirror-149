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
Menu.SimpleConsoleMenu(menuName,menuItems,autoAddQuit,onlyReturnNumber)
```

With these parameters :

    menuName - Required : name of the menu (Str)
    menuItems - Required : menu items, separated with ';' (Str)
    autoAddQuit - Optional : automatically add a quit option (Bool)
    onlyReturnNumber - Optional : only numbers are allowed to return (Bool)
