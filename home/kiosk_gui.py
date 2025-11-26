#!/usr/bin/env python3
import subprocess
import subprocess as sp
import tkinter as tk
from tkinter import messagebox
import os
import time
import threading
import pyudev
import psutil
from threading import Thread

USB_MOUNT_POINT = "/media/usb"

EXT_IMAGENES = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
EXT_VIDEOS   = {".mp4", ".mkv", ".avi", ".mov"}
EXT_MUSICA   = {".mp3", ".flac", ".wav", ".ogg"}

CHROMIUM = "/usr/bin/chromium" 
VLC      = "/usr/bin/vlc"

# Rutas locales por defecto
LOCAL_VIDEO_DIR    = "/home/pi/videos"
LOCAL_PICTURES_DIR = "/home/pi/pictures"
LOCAL_MUSIC_DIR    = "/home/pi/media_local/music"

# Ruta que se usara para las fotos (puede cambiar a USB)
pictures_path = LOCAL_PICTURES_DIR

# ----------------- URLS de servicios en linea -----------------
NETFLIX_URL     = "https://www.netflix.com/browse"
YOUTUBE_URL     = "https://www.youtube.com"
DISNEY_URL      = "https://www.disneyplus.com"
HBO_URL         = "https://play.max.com"   
SPOTIFY_URL     = "https://open.spotify.com"
APPLE_MUSIC_URL = "https://music.apple.com"
AMAZON_MUSIC_URL= "https://music.amazon.com"


def launch_and_wait(cmd):
    print("[INFO] Ejecutando:", " ".join(cmd))
    root.withdraw()
    try:
        proc = subprocess.Popen(cmd)
        proc.wait()
    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar:\n{e}")
    finally:
        # Al terminar, mostramos de nuevo el menu
        root.deiconify()
        restore_mouse_cursor()


# ----------------- Lanzadores de servicios online -----------------
def open_chromium_kiosk(url):
    cmd = [
        CHROMIUM,
        "--kiosk",
        "--noerrdialogs",
        "--disable-infobars",
        "--start-maximized",
        "--window-position=0,0",
        "--window-size=1920,1080",
        url
    ]
    launch_and_wait(cmd)

def open_netflix():
    open_chromium_kiosk(NETFLIX_URL)

def open_youtube():
    open_chromium_kiosk(YOUTUBE_URL)

def open_disney():
    open_chromium_kiosk(DISNEY_URL)

def open_hbo():
    open_chromium_kiosk(HBO_URL)

def open_spotify_web():
    open_chromium_kiosk(SPOTIFY_URL)

def open_apple_music():
    open_chromium_kiosk(APPLE_MUSIC_URL)

def open_amazon_music():
    open_chromium_kiosk(AMAZON_MUSIC_URL)


# ----------------- Contenido local -----------------
def play_local_videos():
    if not os.path.isdir(LOCAL_VIDEO_DIR):
        messagebox.showwarning("Aviso", f"No existe la carpeta:\n{LOCAL_VIDEO_DIR}")
        return
    cmd = [
        VLC,
        "--fullscreen",
        "--no-video-title-show",
        "--mouse-hide-timeout=0",
        LOCAL_VIDEO_DIR
    ]
    launch_and_wait(cmd)

def get_images(path):
    """Devuelve lista de imagenes .jpg y .png en la ruta dada"""
    if not os.path.exists(path):
        return []
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.lower().endswith(".jpg") or f.lower().endswith(".png")
    ]

def slideshow_photos():
    """Presentacion de flista de imagenes"""
    global pictures_path
    path = LOCAL_PICTURES_DIR

    images = get_images(path)
    if not images:
        tk.messagebox.showinfo(
            "Sin imágenes",
            f"No se encontraron imágenes en:\n{path}"
        )
        return

    cmd = [
        VLC,
        "--fullscreen",
        "--no-video-title-show",
        "--mouse-hide-timeout=0",
        "--loop",
        "--image-duration=3"
    ]
    cmd.extend(images)
    launch_and_wait(cmd)

def play_local_music():
    if not os.path.isdir(LOCAL_MUSIC_DIR):
        messagebox.showwarning("Aviso",
                               f"No existe la carpeta:\n{LOCAL_MUSIC_DIR}")
        return

    cmd = [
        VLC,
        "--fullscreen",
        "--no-video-title-show",
        "--mouse-hide-timeout=0",
        "--loop",
        LOCAL_MUSIC_DIR
    ]
    launch_and_wait(cmd)



def quit_app():
    cmd = [
            "sudo",
            "shutdown",
            "now",
    ]
    launch_and_wait(cmd)

def restore_mouse_cursor():
    os.system("xsetroot -cursor_name left_ptr")
    os.system("xinput --disable 'pointer:Virtual core pointer'")
    time.sleep(0.2)
    os.system("xinput --enable 'pointer:Virtual core pointer'")
    


# ----------------- Interfaz grafica -----------------
root = tk.Tk()
root.title("Centro Multimedia - Miguel Lozano")

# Fuerza tamano y escala
root.geometry("1920x1080+0+0")
root.tk.call('tk', 'scaling', 1.0)

# Pantalla completa
root.attributes("-fullscreen", True)
root.configure(bg="#101820")  # fondo oscuro

# Configurar para ocupar toda la pantalla
root.rowconfigure(0, weight=1)   # fila de titulo
root.rowconfigure(1, weight=4)   # fila de botones
root.rowconfigure(2, weight=1)   # fila salir
root.columnconfigure(0, weight=1)

# -------- TITULO  --------
title = tk.Label(
    root,
    text="Centro Multimedia - Lozano & Galvan",
    fg="#FFFFFF",
    bg="#101820",
    font=("Helvetica", 46, "bold")
)
title.grid(row=0, column=0, pady=40, sticky="n")

#-------- FRAME DE BOTONES --------
button_frame = tk.Frame(root, bg="#101820")
button_frame.grid(row=1, column=0, sticky="nsew")
button_frame.columnconfigure(0, weight=1)

btn_style = {
    "height": 2,
    "font": ("Helvetica", 26),
    "bg": "#1F6FEB",
    "fg": "#FFFFFF",
    "activebackground": "#1150AA",
    "activeforeground": "#FFFFFF",
    "bd": 0
}

# Botones de servicios
btn1 = tk.Button(button_frame, text="Netflix",       command=open_netflix,      **btn_style)
btn2 = tk.Button(button_frame, text="YouTube",       command=open_youtube,      **btn_style)
btn3 = tk.Button(button_frame, text="Disney+",       command=open_disney,       **btn_style)
btn4 = tk.Button(button_frame, text="HBO Max",       command=open_hbo,          **btn_style)
btn5 = tk.Button(button_frame, text="Spotify Web",  command=open_spotify_web,  **btn_style)
btn6 = tk.Button(button_frame, text="Apple Music",  command=open_apple_music,  **btn_style)
btn7 = tk.Button(button_frame, text="Amazon Music", command=open_amazon_music, **btn_style)
btn8 = tk.Button(button_frame, text="Videos locales",                 command=play_local_videos, **btn_style)
btn9 = tk.Button(button_frame, text="Presentación de fotos locales",command=slideshow_photos,  **btn_style)



btn1.grid(row=0, column=0, sticky="ew", padx=40, pady=10)
btn2.grid(row=1, column=0, sticky="ew", padx=40, pady=10)
btn3.grid(row=2, column=0, sticky="ew", padx=40, pady=10)
btn4.grid(row=3, column=0, sticky="ew", padx=40, pady=10)
btn5.grid(row=4, column=0, sticky="ew", padx=40, pady=10)
btn6.grid(row=5, column=0, sticky="ew", padx=40, pady=10)
btn7.grid(row=6, column=0, sticky="ew", padx=40, pady=10)
btn8.grid(row=7, column=0, sticky="ew", padx=40, pady=10)
btn9.grid(row=8, column=0, sticky="ew", padx=40, pady=10)


# -------- BOTON SALIR --------
btn_exit = tk.Button(
    root,
    text="Apagar",
    command=quit_app,
    width=12,
    height=1,
    font=("Helvetica", 24),
    bg="#444444",
    fg="#FFFFFF",
    activebackground="#666666",
    activeforeground="#FFFFFF",
    bd=0
)
btn_exit.grid(row=2, column=0, pady=40)

# ---------- NAVEGACION CON TECLAS ----------
menu_buttons = [btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn_exit]
selected_index = 0

def highlight_button(index):
    global selected_index
    selected_index = index
    for i, b in enumerate(menu_buttons):
        if i == selected_index:
            b.configure(bg="#2B88FF" if i < 9 else "#666666")
            b.focus_set()
        else:
            if i < 9:
                b.configure(bg="#1F6FEB")
            else:
                b.configure(bg="#444444")

def activate_selected():
    menu_buttons[selected_index].invoke()

def handle_key(event):
    global selected_index
    k = event.keysym

    if k in ("Down", "KP_Down"):
        highlight_button((selected_index + 1) % len(menu_buttons))
    elif k in ("Up", "KP_Up"):
        highlight_button((selected_index - 1) % len(menu_buttons))
    elif k in ("Return", "KP_Enter", "space"):
        activate_selected()
    elif k in ("Escape", "q", "Q"):
        quit_app()
    # Atajos numéricos
    elif k in ("1", "KP_1"):
        btn1.invoke()
    elif k in ("2", "KP_2"):
        btn2.invoke()
    elif k in ("3", "KP_3"):
        btn3.invoke()
    elif k in ("4", "KP_4"):
        btn4.invoke()
    elif k in ("5", "KP_5"):
        btn5.invoke()
    elif k in ("6", "KP_6"):
        btn6.invoke()
    elif k in ("7", "KP_7"):
        btn7.invoke()
    elif k in ("8", "KP_8"):
        btn8.invoke()
    elif k in ("9", "KP_9"):
        btn9.invoke()

root.bind("<Key>", handle_key)
highlight_button(0)


# ----------------- Logica de USB / escaneo de contenido -----------------
def auto_mount(path):
    """Monta la particion USB usando udisksctl"""
    args = ["udisksctl", "mount", "-b", path]
    sp.run(args)

def get_mount_point(path):
    """Obtiene el punto de montaje de la particion."""
    args = ["findmnt", "-unl", "-S", path]
    cp = sp.run(args, capture_output=True, text=True)
    out = cp.stdout.strip().split(" ")[0] if cp.stdout.strip() else ""
    return out if out else None

def scan_usb_content(base_path):
    """Escanea la USB y cuenta imagenes videos y música, y devuelve listas de rutas"""
    images = []
    videos = []
    music  = []
    for root_dir, dirs, files in os.walk(base_path):
        for fname in files:
            f_lower = fname.lower()
            _, ext = os.path.splitext(f_lower)
            full_path = os.path.join(root_dir, fname)
            if ext in EXT_IMAGENES:
                images.append(full_path)
            elif ext in EXT_VIDEOS:
                videos.append(full_path)
            elif ext in EXT_MUSICA:
                music.append(full_path)
    return images, videos, music

def play_usb_photos(base_path, images=None):
    """Presentacion de fotos desde la USB usando solo imagenes validos."""
    if images is None:
        images, _, _ = scan_usb_content(base_path)

    if not images:
        messagebox.showinfo("Fotos", "No se encontraron imágenes en la USB.")
        return

    cmd = [
        VLC,
        "--fullscreen",
        "--no-video-title-show",
        "--image-duration=3",
        "--mouse-hide-timeout=0",
        "--loop",
    ]
    cmd.extend(images)
    root.withdraw()
    launch_and_wait(cmd)

def play_usb_music(base_path, music=None):
    """Reproduccion de musica desde la USB en bucle."""
    if music is None:
        _, _, music = scan_usb_content(base_path)

    if not music:
        messagebox.showinfo("Música", "No se encontraron pistas de música en la USB.")
        return

    cmd = [
        VLC,
        "--fullscreen",
        "--no-video-title-show",
        "--mouse-hide-timeout=0",
        "--loop",
    ]
    cmd.extend(music)   # solo archivos de audio
    launch_and_wait(cmd)


def play_usb_videos_slideshow(base_path, videos=None):
    """Videos de la USB uno tras otro"""
    if videos is None:
        _, videos, _ = scan_usb_content(base_path)

    if not videos:
        messagebox.showinfo("Videos", "No se encontraron videos en la USB.")
        return

    cmd = [
        VLC,
        "--fullscreen",
        "--no-video-title-show",
        "--mouse-hide-timeout=0",
        "--loop",
    ]
    cmd.extend(videos)   #solo archivos de video
    launch_and_wait(cmd)


def play_single_video(video_path):
    """Reproducir un solo video"""
    cmd = [
        VLC,
        "--fullscreen",
        "--no-video-title-show",
        "--mouse-hide-timeout=0",
        video_path
    ]
    launch_and_wait(cmd)

def choose_video_and_play(videos):
    """Muestra una lista de videos y deja elegir uno para reproducir"""
    if not videos:
        messagebox.showinfo("Videos", "No se encontraron videos en la USB.")
        return

    win = tk.Toplevel(root)
    win.title("Seleccionar película")
    win.geometry("1920x1080")
    win.configure(bg="#101820")

    label = tk.Label(
        win,
        text="Seleccione una película:",
        fg="#FFFFFF",
        bg="#101820",
        font=("Helvetica", 20, "bold")
    )
    label.pack(pady=10)

    frame_list = tk.Frame(win, bg="#101820")
    frame_list.pack(expand=True, fill="both", padx=20, pady=20)

    scrollbar = tk.Scrollbar(frame_list)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(
        frame_list,
        font=("Helvetica", 16),
        bg="#182030",
        fg="#FFFFFF",
        selectbackground="#2B88FF",
        selectforeground="#FFFFFF",
        yscrollcommand=scrollbar.set
    )
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    for v in videos:
        listbox.insert("end", os.path.basename(v))

    def on_play():
        sel = listbox.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione una película primero.")
            return
        idx = sel[0]
        video_path = videos[idx]
        win.destroy()
        play_single_video(video_path)

    btn_play = tk.Button(
        win,
        text="Reproducir",
        command=on_play,
        font=("Helvetica", 16),
        bg="#1F6FEB",
        fg="#FFFFFF",
        activebackground="#1150AA",
        activeforeground="#FFFFFF",
        bd=0,
        width=12,
        height=1
    )
    btn_play.pack(pady=10)

    btn_cancel = tk.Button(
        win,
        text="Cancelar",
        command=win.destroy,
        font=("Helvetica", 14),
        bg="#444444",
        fg="#FFFFFF",
        activebackground="#666666",
        activeforeground="#FFFFFF",
        bd=0,
        width=10,
        height=1
    )
    btn_cancel.pack(pady=5)

def handle_usb_media(base_path):
    """Decide que hacer segun el contenido de la USB."""
    global pictures_path
    images, videos, music = scan_usb_content(base_path)
    n_imgs = len(images)
    n_vids = len(videos)
    n_mus  = len(music)

    print(f"[USB] Contenido: {n_imgs} imágenes, {n_vids} videos, {n_mus} pistas de música")

    if n_imgs == 0 and n_vids == 0 and n_mus == 0:
        messagebox.showinfo("USB", "No se encontró contenido multimedia soportado en la USB.")
        return

    tipos = sum(1 for x in (n_imgs, n_vids, n_mus) if x > 0)

    # Solo fotos
    if tipos == 1 and n_imgs > 0:
        pictures_path = base_path
        messagebox.showinfo("USB", "Se detectaron solo imágenes.\nIniciando presentación.")
        play_usb_photos(base_path, images)
        return

    # Solo música
    if tipos == 1 and n_mus > 0:
        messagebox.showinfo("USB", "Se detectaron solo pistas de música.\nIniciando reproducción en bucle.")
        play_usb_music(base_path, music)
        return

    # Solo videos
    if tipos == 1 and n_vids > 0:
        resp = messagebox.askyesno(
            "Videos en USB",
            "Se detectaron solo videos.\n\n¿Reproducir todos en modo presentación?"
        )
        if resp:
            play_usb_videos_slideshow(base_path, videos)
        else:
            choose_video_and_play(videos)
        return

    # Contenido mixto
    msg = (
        "Se detectó contenido mixto en la USB:\n\n"
        f"- Imágenes: {n_imgs}\n"
        f"- Videos:   {n_vids}\n"
        f"- Música:   {n_mus}\n\n"
        "¿Qué desea reproducir?"
    )

    win = tk.Toplevel(root)
    win.title("Contenido mixto en USB")
    win.geometry("1920x1080")
    win.configure(bg="#101820")
    win.attributes("-fullscreen", True)
    win.attributes("-topmost", True)

    label = tk.Label(
        win,
        text=msg,
        fg="#FFFFFF",
        bg="#101820",
        font=("Helvetica", 20)
    )
    label.pack(pady=40)

    def choose_photos():
        win.destroy()
        if n_imgs > 0:
            pictures_path = base_path
            play_usb_photos(base_path, images)
        else:
            messagebox.showinfo("Fotos", "No hay fotos disponibles en la USB.")

    def choose_videos():
        win.destroy()
        if n_vids > 0:
            resp2 = messagebox.askyesno(
                "Videos en USB",
                "¿Reproducir todos los videos en modo presentación?"
            )
            if resp2:
                play_usb_videos_slideshow(base_path, videos)
            else:
                choose_video_and_play(videos)
        else:
            messagebox.showinfo("Videos", "No hay videos disponibles en la USB.")

    def choose_music():
        win.destroy()
        if n_mus > 0:
            play_usb_music(base_path, music)
        else:
            messagebox.showinfo("Música", "No hay música disponible en la USB.")

    btn_frame = tk.Frame(win, bg="#101820")
    btn_frame.pack(pady=20)

    btn_fotos = tk.Button(
        btn_frame, text="Fotos", command=choose_photos,
        font=("Helvetica", 18), bg="#1F6FEB", fg="#FFFFFF",
        activebackground="#1150AA", activeforeground="#FFFFFF",
        bd=0, width=10, height=2
    )
    btn_videos = tk.Button(
        btn_frame, text="Videos", command=choose_videos,
        font=("Helvetica", 18), bg="#1F6FEB", fg="#FFFFFF",
        activebackground="#1150AA", activeforeground="#FFFFFF",
        bd=0, width=10, height=2
    )
    btn_musica = tk.Button(
        btn_frame, text="Música", command=choose_music,
        font=("Helvetica", 18), bg="#1F6FEB", fg="#FFFFFF",
        activebackground="#1150AA", activeforeground="#FFFFFF",
        bd=0, width=10, height=2
    )

    btn_fotos.grid(row=0, column=0, padx=20, pady=10)
    btn_videos.grid(row=0, column=1, padx=20, pady=10)
    btn_musica.grid(row=0, column=2, padx=20, pady=10)

    btn_cerrar = tk.Button(
        win,
        text="Cerrar",
        command=win.destroy,
        font=("Helvetica", 16),
        bg="#444444",
        fg="#FFFFFF",
        activebackground="#666666",
        activeforeground="#FFFFFF",
        bd=0,
        width=10,
        height=2
    )
    btn_cerrar.pack(pady=30)

    # Navegacion con teclado
    botones = [btn_fotos, btn_videos, btn_musica, btn_cerrar]
    estado = {"idx": 0}
    botones[0].focus_set()

    def on_key(event):
        if event.keysym in ("Right", "Down"):
            estado["idx"] = (estado["idx"] + 1) % len(botones)
            botones[estado["idx"]].focus_set()
        elif event.keysym in ("Left", "Up"):
            estado["idx"] = (estado["idx"] - 1) % len(botones)
            botones[estado["idx"]].focus_set()
        elif event.keysym in ("Return", "KP_Enter", "space"):
            botones[estado["idx"]].invoke()

    win.bind("<Key>", on_key)


def usb_monitor():
    """Hilo que detecta insercion y retiro de USB y llama a handle_usb_media"""
    global pictures_path
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="block", device_type="partition")

    print("[USB] Monitor iniciado...")
    for action, device in monitor:
        dev_path = "/dev/" + device.sys_name
        print(f"[USB] Evento: {action} en {dev_path}")

        if action == "add":
            print(f"[USB] USB detectada en {dev_path}, montando...")
            auto_mount(dev_path)
            mp = get_mount_point(dev_path)
            if mp:
                print(f"[USB] Punto de montaje: {mp}")
                root.after(0, handle_usb_media, mp)

        elif action == "remove":
            print(f"[USB] USB retirada: {dev_path}")
            pictures_path = LOCAL_PICTURES_DIR
            root.after(0, lambda: messagebox.showinfo(
                "USB retirada",
                "Se ha retirado la memoria USB.\nSe regresa a contenido local."
            ))


# Lanzar monitor de USB en segundo plano
usb_thread = Thread(target=usb_monitor, daemon=True)
usb_thread.start()

root.mainloop()
