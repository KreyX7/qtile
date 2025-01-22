

# Importaciones
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.config import Key
import os 

# Configuración de mod y terminal
mod = "mod4"
terminal = guess_terminal()

# Configuración de las teclas
keys = [
    # Navegar entre las ventanas
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Mover ventanas entre columnas y apilar
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Ajustar tamaño de las ventanas
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Alternar entre diseños
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    # Comandos de ventana
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    
    # Captura de pantalla guardado en ~/screenshot
    Key([mod, "shift"], "Print", lazy.spawn("scrot /home/enzo/screenshot/%Y-%m-%d-%T-screenshot.png")),   
    
    # Recarga y apagado
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    
    # Comando rápido
    Key([mod], "r", lazy.spawn("bash /home/enzo/rofi/files/launchers/type-4/launcher.sh"), desc="Abrir lanzador"),
    # Key([mod], "r", lazy.spawncmd("bash /home/enzo/rofi/files/launchers/type-1/launcher.sh", desc="Spawn a command using a prompt widget"),
]

# Cambiar de VT en Wayland
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# Definición de grupos
groups = [Group(f"{i}", label=f" ●") for i in "123456789"]


for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Switch to group {i.name}"),
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc=f"Switch to & move focused window to group {i.name}"),
        ]
    )

# Configuración de layouts
layouts = [
    layout.MonadTall(margin=8, border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=0),
    layout.Max(),
]

# Configuración de widgets
widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# Definición de pantallas
screens = [
    Screen(
        top=bar.Bar(
            [
             
                # Sección izquierda
                widget.Image(
                filename="~/.config/qtile/logo.png",  # Ruta a la imagen
                margin=4,  # Cambia el tamaño 
                ), 
                
                widget.GroupBox(
                        highlight_method="text",         # Resalta solo el texto (para mantener los círculos simples)
                        rounded=True,                    # Crea esquinas redondeadas (círculos)
                        inactive="#666666",              # Color para grupos inactivos
                        active="#979af7",                # Color para grupos activos
                        this_current_screen_border="#fff09e",  # Amarillo para el grupo activo en la pantalla actual
                        other_current_screen_border="#1E3A5F", # Azul marino para los ocupados en otras pantallas
                        this_screen_border="#FFD700",          # Amarillo para el grupo activo en pantallas no actuales
                        other_screen_border="#1E3A5F",         # Azul marino para ocupados
                        urgent_border="#FF00FF",               # Magenta para grupos urgentes
                        highlight_color=["f7f7f5"], # Fondo para el grupo activo
                        disable_drag=True,               # Desactiva arrastrar grupos con el mouse
                        fontsize=14,                     # Tamaño de la fuente para el círculo
                        margin_y=3,                      # Espaciado vertical
                        margin_x=1,                      # Espaciado horizontal
                        padding=5,                       # Espaciado interno del círculo
                        use_mouse_wheel=False,  
                    
                ),
                widget.Prompt(),              
      
                # Separador para el centro
                widget.Spacer(length=bar.STRETCH),
                widget.TextBox("", fontsize=34, padding=-1, foreground="#171717", background="#0b0e0f"),
                widget.WindowName(foreground="#808080", background="#171717", padding=-1, font="Fira Code Nerd Font"),
                widget.Systray(foreground="#ffffff", background="#171717", font=""),      
                widget.TextBox("", fontsize=34, padding=-1, foreground="#171717", background="#0b0e0f"),

                # Sección central
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),

                # Separador para la derecha
                widget.Spacer(length=bar.STRETCH),

                # Sección derecha

                
                widget.TextBox("", fontsize=34, padding=1, foreground="#2e2e2e", background="#0b0e0f"),
                widget.Battery(format=" {percent:2.0%} ", background="#2e2e2e", font="Fira Code Nerd Font", foreground="#ffffff"),

                widget.TextBox("", fontsize=34, padding=1, foreground="#171717", background="#2e2e2e"),
                widget.Clock(format=" %I:%M ", background="#171717", font="Fira Code Nerd Font"),

                widget.TextBox("", fontsize=34, padding=1, foreground="#000000", background="#171717"),
                widget.Clock(format=" %d/%m/%Y  ", background="#000000", font="Fira Code Nerd Font"),
                
                
            ],
            34,  # Altura de la barra
            background="#0b0e0f",
            margin=[5, 5, 0, 5],  # Márgenes
            border_width=[2, 2, 2, 2],  # Bordes de la barra
            opacity=0.8,
            border_color="",  # Color de los bordes
            border_radius=25,
        ),
    ),
]


# Configuración de mouse (drag and click)
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]



floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    border_focus="#",  # Color del borde para ventanas enfocadas
    border_normal="#",  # Color del borde para ventanas no enfocadas
    border_width=0,  # Ancho del borde en píxeles
)

# Configuración adicional
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

# Configuración de Wayland
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24

# Nombre de la ventana del WM
wmname = "LG3D"

autostart = [
   # "bash ~/.screenlayout/resolution.sh" 
   "picom &"
   "nitrogen --restore &",
   
   
]

for x in autostart:
    os.system(x)