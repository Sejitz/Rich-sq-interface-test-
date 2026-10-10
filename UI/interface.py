import sys
import tty
import termios
import os

from rich.console import Console, Group
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from rich.progress import Progress, BarColumn, TextColumn
from rich.live import Live

from menu import menu, draw_menu
from name import get_player_name

console = Console()



def main_ui(live):
    options = [
        "New Game",
        "Load Game",
        "Exit"
    ]

    # Main menu layout
    
    live.update(draw_menu(options, 0), refresh=True)

    return menu(options, live)

#Village Ui ---------------------------------------------------
def village_ui(live):
    options = [
        "Leaf",
        "Rain",
        "Sand"
    ]

    live.update(draw_menu(options, 0), refresh=True)

    return menu(options, live)

#Choice Ui ---------------------------------------------------
def choice_ui(live):
    options = [
        "Yes",
        "No"
    ]

    layout = Layout()

    layout.split_column(
        Layout(name="story", ratio=3),
        Layout(name="choice", ratio=2)
    )

    layout["story"].update(
        Panel(
            "Welcome to Shinobiquest! \n"
            "Here's your startup rewards"
            "for your exciting journey!"
        )
    )

    layout["choice"].update(
        draw_menu(options, 0)
    )

    live.update(layout, refresh=True)

    return menu(
        options,
        live,
        target=layout["choice"]
    )

#Interface Ui ---------------------------------------------------
def interface_ui(live):
    options = [
        "Search",
        "Inventory",
        "Shop",
        "Back"
    ]

    # Interface menu layout
    live.update(draw_menu(options, 0), refresh=True)

    return menu(options, live)

#Inventory Ui ---------------------------------------------------
def inventory_ui(live, potion_quantity = 0, kunai_quantity = 0):
    console.print(Align.center("[italic green]← Inventory →[/italic green]"))

    
    
    
    options = [
        f"Potions: {potion_quantity}",
        f"Kunai: {kunai_quantity}\n",
        "Back"
    ]

    live.update(draw_menu(options, 0), refresh=True)

    return menu(options, live)

#Shop Ui ---------------------------------------------------
def shop_ui(live, balance):
    console.print(Align.center("[italic green]← Shop →[/italic green]"))
    
    print(f"Balance: {balance}")

    potion_price = 70
    kunai_price = 40
    
    options = [
        f"Potion: {potion_price}",
        f"Kunai: {kunai_price}\n",
        "Back"
    ]

    live.update(draw_menu(options, 0), refresh=True)

    return menu(options, live)

#Battle Ui ---------------------------------------------------
def battle_ui(live):

    options = [
        "Attack",
        "Kunai",
        "Run"
    ]

    # HP / CHAKRA BARS

    player_hpbar = Progress(
        TextColumn("[bold]HP [/bold]"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%")
    )

    player_chbar = Progress(
        TextColumn("[bold]Chakra [/bold]"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%")
    )

    enemy_bar = Progress(
        TextColumn("[bold]HP [/bold]"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%")
    )

    player_hpbar.add_task(
        "HP ",
        total=100,
        completed=100
    )

    player_chbar.add_task(
        "Chakra ",
        total=100,
        completed=100
    )

    enemy_bar.add_task(
        "HP ",
        total=100,
        completed=100
    )

    # -----------------------------------------------------
    # MAIN BATTLE LAYOUT
    # -----------------------------------------------------

    layout = Layout()

    layout.split_column(
        Layout(name="info", ratio=3),
        Layout(name="log", ratio=2),
        Layout(name="battleui", ratio=2)
    )

    # -----------------------------------------------------
    # PLAYER / ENEMY
    # -----------------------------------------------------

    layout["info"].split_row(
        Layout(name="player"),
        Layout(name="enemy")
    )

    player_panel = Group(
        player_hpbar,
        player_chbar,
        "",
        "Ryo: 100"
    )

    enemy_panel = Group(
        "Name: Bandit",
        enemy_bar
    )

    layout["player"].update(
        Panel(
            player_panel,
            title="Player"
        )
    )

    layout["enemy"].update(
        Panel(
            enemy_panel,
            title="Enemy"
        )
    )

    # -----------------------------------------------------
    # BATTLE LOG
    # -----------------------------------------------------

    layout["log"].update(
        Panel(
            "Choose your action...",
            title="Battle Log"
        )
    )

    # -----------------------------------------------------
    # BATTLE MENU
    # -----------------------------------------------------

    layout["battleui"].update(
        draw_menu(options, 0),
    )

    # -----------------------------------------------------
    # UPDATE LIVE SCREEN
    # -----------------------------------------------------

    live.update(
        layout,
        refresh=True
    )

    # -----------------------------------------------------
    # GET PLAYER CHOICE
    # -----------------------------------------------------

    return menu(
        options,
        live,
        target=layout["battleui"]
    )


# =========================================================
# GAME UI
# =========================================================

def run_ui():

    old_settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin.fileno())

        console.print(
            Align.center(
                "[bold cyan]→ Shinobi Quest ←[/bold cyan]"
            )
        )


        with Live(
            "",
            console=console,
            auto_refresh=False
        ) as live:


            screen = "main"
            potion_amount = 4
            kunai_amount = 7
            balance = 0

            while True:
                if screen == "main":
                    choice = main_ui(live)
                    if choice == "New Game":
                        screen = "village"
                    elif choice == "Load Gamed":
                        screen = "Load"
                    elif choice == "Exit":
                        break
                        
                elif screen == "village":
                    name = get_player_name(live)
                    village = village_ui(live)
                    screen = "choice"
                    
                elif screen == "choice":
                    choice = choice_ui(live)
                    if choice == "No":
                        screen = "main"
                    elif choice == "Yes":
                        screen = "interface"
                        
                elif screen == "interface":
                    choice = interface_ui(live)
                    if choice == "Search":
                        screen = "battle"
                    elif choice == "Inventory":
                        screen = "inventory"
                    elif choice == "Shop":
                        screen = "shop"
                    elif choice == "Back":
                        screen = "main"
                        
                elif screen == "battle":
                    choice = battle_ui(live)
                    
                elif screen == "inventory":
                    choice = inventory_ui(live, potion_amount, kunai_amount)
                    if choice == "Back":
                        screen = "interface"

                elif screen == "shop":
                    choice = shop_ui(live, balance)
                    if choice == "Back":
                        screen = "interface"

                # elif screen == "inv_back":
                #     choice = interface_ui(live)

                # elif screen == "shop_back":
                #     choice = interface_ui(live)
                    
    
                elif choice == "Load Game":
                    console.print(
                        "\nLoad Game selected."
                    )
    
    
                elif choice == "Exit":
                    return




    finally:

        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            old_settings
        )
        