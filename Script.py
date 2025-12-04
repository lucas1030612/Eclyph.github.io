import tkinter as tk
import random
import webbrowser
import os
import platform
import subprocess
import re
from threading import Thread
import ctypes
import urllib.request
import tempfile
import shutil
import time
from threading import Event
import math
print ("DeepVoid V0.2 - Iniciando...")


# ----------Terminal----------

def começa():
    abrir_abas()          # 🔥 abre várias abas igual ao outro código
   

# ---------- CONFIG ----------
POPUPS_TOTAL_CICLOS = 90      # quantos ciclos de pop-ups (cada ciclo cria POPUPS_POR_CICLO popups)
POPUPS_POR_CICLO = 6
POPUP_INTERVAL_MS = 25        # intervalo entre ciclos (ms)
POPUP_LIFETIME_MS = 400      # tempo que cada popup fica (ms)

NUM_FAKE_WINDOWS = 10  #mude aqui para mais janelas dizendo voce é idiota
FAKE_WINDOW_SIZE = (420, 220)
FAKE_ANIM_INTERVAL_MS = 100   # velocidade da animação das janelas falsas (ms)

# ---------- CONFIG EVENTO EXTRA (ABRIR ABAS) ----------
ABRIR_ABAS_HABILITADO = True  # ativar/desativar abertura de abas
NUM_VEZES_ABRIR_ABAS = 50      # quantas vezes abrir as abas

# ---------- CONFIG CRIAR PASTAS ----------
CRIAR_PASTAS_HABILITADO = True  # ativar/desativar criação de pastas
NUM_PASTAS_CRIAR = 50            # quantas pastas "arquivoX" criar na área de trabalho
# ----------------------------

# ---------- WALLPAPER CONFIG ----------
# Se quiser que o script altere o papel de parede ao iniciar, deixe True
CHANGE_WALLPAPER = True
# Se você quiser usar uma imagem local, coloque o arquivo `wallpaper.jpg`
# na mesma pasta do `Script.py`. Caso prefira baixar da web, defina
# WALLPAPER_URL = 'https://exemplo.com/imagem.jpg'
WALLPAPER_URL = None
WALLPAPER_FILENAME = "wallpaper.jpg"
# --------------------------------------

# ---------- CPU STRESS CONFIG ----------
# Habilite manualmente se realmente quiser forçar uso de CPU (padrão: False)
ENABLE_CPU_STRESS = False
# Percentual mínimo e máximo da CPU alvo (0-100)
CPU_MIN_PERCENT = 95
CPU_MAX_PERCENT = 100
# Cada quanto (s) o controlador escolhe um novo alvo dentro do intervalo
CPU_ADJUST_INTERVAL = 1
# Periodo de cada ciclo dos workers (segundos). Valores menores -> menor latência
CPU_WORKER_PERIOD = 0.1
# Quantas threads por núcleo (1 usa n_cores threads). Se quiser aumentar agressividade, aumente.
CPU_THREADS_PER_CORE = 1
# --------------------------------------

root = tk.Tk()
root.title("Simulador")
root.geometry("420x200")
root.configure(bg="black")
root.resizable(False, False)

# Texto principal
titulo = tk.Label(root, text="Simulador de Hacker", fg="white", bg="black", font=("Arial", 20, "bold"))
titulo.pack(pady=20)
status = tk.Label(root, text="Executando eventos...", fg="gray", bg="black", font=("Arial", 12))
status.pack()

# cores
cores_vivas = [
    "#ff0000", "#08FF08", "#ffffff", "#002ae7",
    "#171818", "#ee14bf", "#005716", "#4F038D", "#F7E70F"
]

# ---------- Função que cria um popup (Tkinter Toplevel) ----------
def criar_popup():
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.lift()
    popup.attributes("-topmost", True)

    largura = random.randint(160, 320)
    altura = random.randint(70, 140)

    # garante coordenadas válidas
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = random.randint(0, max(0, sw - largura))
    y = random.randint(0, max(0, sh - altura))

    popup.geometry(f"{largura}x{altura}+{x}+{y}")
    cor = random.choice(cores_vivas)
    popup.configure(bg=cor)

    label = tk.Label(popup, text="DeepVoid V0.2", fg="white", bg=cor, font=("Arial", 18, "bold"))
    label.pack(expand=True, fill="both")

    # fecha depois de POPUP_LIFETIME_MS
    popup.after(POPUP_LIFETIME_MS, popup.destroy)

# ---------- Evento 1: criar vários pop-ups em ciclos, depois chama evento 2 ----------
popup_ciclo_atual = 0

def ciclo_popups():
    global popup_ciclo_atual
    if popup_ciclo_atual >= POPUPS_TOTAL_CICLOS:
        # terminou os pop-ups -> iniciar evento das janelas falsas
        status.config(text="Evento 1 concluído. Iniciando evento 2...")
        root.after(500, iniciar_evento_falso)  # pequena pausa antes do próximo evento
        return

    # cria POPUPS_POR_CICLO popups agora
    for _ in range(POPUPS_POR_CICLO):
        criar_popup()

    popup_ciclo_atual += 1
    # agenda próximo ciclo
    root.after(POPUP_INTERVAL_MS, ciclo_popups)

def iniciar_evento_popups():
    status.config(text="Evento 1: GLITCH...")
    root.after(200, ciclo_popups)  # começa rapidinho

# ---------- EVENTO 2: Janelas "YOU ARE AN IDIOT (FAKE)" que mudam cor e se movem ----------
fake_windows = []

def animar_falsa_janela(win, label):
    # função que alterna cor e move a janela; usa root.after para agendar repetidamente
    def passo():
        # alterna cor de fundo e texto (preto <-> branco)
        current_bg = win.cget("bg")
        novo_bg = "white" if current_bg == "black" else "black"
        novo_fg = "black" if label.cget("fg") == "white" else "white"

        win.configure(bg=novo_bg)
        label.configure(bg=novo_bg, fg=novo_fg)

        # calcula nova posição aleatória (mantendo tamanho constante)
        largura, altura = FAKE_WINDOW_SIZE
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = random.randint(0, max(0, sw - largura))
        y = random.randint(0, max(0, sh - altura))

        try:
            win.geometry(f"{largura}x{altura}+{x}+{y}")
        except tk.TclError:
            # janela pode ter sido fechada; aborta animação
            return

        # reagenda
        win.after(FAKE_ANIM_INTERVAL_MS, passo)

    passo()

def abrir_falsa_janela(index):
    win = tk.Toplevel(root)
    win.title(f"Seu pc foi contaminado com DeepVoid{index+1}")
    win.overrideredirect(True)              # remove bordas (opcional)
    win.attributes("-topmost", True)        # 🔥 deixa sempre na frente
    
    largura, altura = FAKE_WINDOW_SIZE
    # posição inicial aleatória
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = random.randint(0, max(0, sw - largura))
    y = random.randint(0, max(0, sh - altura))

    win.geometry(f"{largura}x{altura}+{x}+{y}")
    win.configure(bg="black")

    # impedir fechar (opcional)
    win.protocol("WM_DELETE_WINDOW", lambda: None)

    label = tk.Label(win, text="VOCE È IDIOTA HAHAHAHA", fg="white", bg="black",
                     font=("Arial", 20, "bold"))
    label.pack(expand=True, fill="both")

    fake_windows.append(win)
    animar_falsa_janela(win, label)

def iniciar_evento_falso():
    status.config(text="Evento 2: Abrindo janelas")
    # cria janelas uma por vez com pequeno intervalo
    def criar_uma(i):
        if i >= NUM_FAKE_WINDOWS:
            status.config(text="Evento 2 em execução.")
            # reinicia o loop após 10 segundos
            root.after(10000, reiniciar_loop_eventos)
            return
        abrir_falsa_janela(i)
        root.after(300, lambda: criar_uma(i+1))

    criar_uma(0)

def reiniciar_loop_eventos():
    """Reinicia o loop de eventos - fecha janelas e volta ao evento 1"""
    global popup_ciclo_atual
    # fecha todas as janelas falsas
    for win in fake_windows:
        try:
            win.destroy()
        except Exception:
            pass
    fake_windows.clear()
    # reseta contador e reinicia
    popup_ciclo_atual = 0
    status.config(text="Reiniciando eventos...")
    root.after(1000, iniciar_evento_popups)

# ---------- Funções para trocar o papel de parede (Windows) ----------
def _download_image(url, dest_path):
    """Baixa imagem da URL. Retorna caminho se sucesso, None se falhar."""
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            with open(dest_path, 'wb') as f:
                shutil.copyfileobj(resp, f)
        return dest_path
    except Exception as e:
        # silencia erro e continua
        return None

def _set_wallpaper_windows(img_path):
    """Define wallpaper no Windows. Retorna True se sucesso, False caso contrário."""
    try:
        if not os.path.exists(img_path):
            return False
        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 0x1
        SPIF_SENDWININICHANGE = 0x2
        abs_path = os.path.abspath(img_path)
        # Tenta diretamente (Windows 10 aceita jpg/png)
        res = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, abs_path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
        return bool(res)
    except Exception as e:
        # falha silenciosamente -> retorna False
        return False

def _cmd_exists(cmd):
    return shutil.which(cmd) is not None

def _set_wallpaper_linux(img_path):
    """Tenta várias estratégias para definir o papel de parede no Linux.
    Retorna True se alguma estratégia teve sucesso, False caso contrário."""
    try:
        if not os.path.exists(img_path):
            return False
        abs_path = os.path.abspath(img_path)

        # 1) GNOME (gsettings)
        try:
            if _cmd_exists('gsettings'):
                uri = f"file://{abs_path}"
                # tenta setar picture-uri (GNOME)
                subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', uri], check=False, timeout=5)
                subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-options', 'scaled'], check=False, timeout=5)
                return True
        except Exception:
            pass

        # 2) feh (comum em ambientes leves)
        try:
            if _cmd_exists('feh'):
                subprocess.run(['feh', '--bg-scale', abs_path], check=False, timeout=5)
                return True
        except Exception:
            pass

        # 3) XFCE (xfconf-query) - tenta algumas chaves comuns
        try:
            if _cmd_exists('xfconf-query'):
                keys = [
                    '/backdrop/screen0/monitor0/image-path',
                    '/backdrop/screen0/monitor0/workspace0/last-image',
                    '/backdrop/screen0/monitor0/workspace0/last-image'
                ]
                for k in keys:
                    subprocess.run(['xfconf-query', '-c', 'xfce4-desktop', '-p', k, '-s', abs_path], check=False, timeout=5)
                return True
        except Exception:
            pass

        # 4) KDE Plasma via qdbus (plasmashell)
        try:
            if _cmd_exists('qdbus'):
                script = "var Desktops = desktops();for (i=0;i<Desktops.length;i++) {d = Desktops[i];d.wallpaperPlugin = 'org.kde.image';d.currentConfigGroup = Array('Wallpaper','org.kde.image','General');d.writeConfig('Image', 'file://%s'); }" % abs_path
                subprocess.run(['qdbus', 'org.kde.plasmashell', '/PlasmaShell', 'org.kde.PlasmaShell.evaluateScript', script], check=False, timeout=5)
                return True
        except Exception:
            pass

        # nenhuma estratégia funcionou
        return False
    except Exception:
        # falha silenciosamente
        return False

def change_wallpaper_if_requested():
    """Tenta trocar o wallpaper. Se falhar em qualquer etapa, continua silenciosamente."""
    try:
        if not CHANGE_WALLPAPER:
            return
        # determina caminho do arquivo alvo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(base_dir, WALLPAPER_FILENAME)

        # se houver URL configurada, tenta baixar
        if WALLPAPER_URL:
            tmp = None
            try:
                fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(WALLPAPER_URL)[-1])
                os.close(fd)
                downloaded = _download_image(WALLPAPER_URL, tmp)
                if downloaded and os.path.exists(downloaded):
                    if platform.system() == 'Windows':
                        _set_wallpaper_windows(downloaded)
                    else:
                        _set_wallpaper_linux(downloaded)
                    return
            except Exception:
                pass
            finally:
                if tmp and os.path.exists(tmp):
                    try:
                        os.remove(tmp)
                    except Exception:
                        pass

        # se existir arquivo local, usa
        if os.path.exists(target):
            try:
                if platform.system() == 'Windows':
                    _set_wallpaper_windows(target)
                else:
                    _set_wallpaper_linux(target)
            except Exception:
                pass
    except Exception:
        # falha silenciosamente - o programa continua independente disso
        pass

# ---------- Funções de estresse de CPU (seguro, controlável) ----------
# Implementação: threads de "busy-wait" que alternam busy/sleep para atingir
# uma carga alvo. A rotina principal escolhe aleatoriamente um alvo entre
# CPU_MIN_PERCENT e CPU_MAX_PERCENT a cada CPU_ADJUST_INTERVAL segundos.

cpu_stop_event = Event()
cpu_target_percent = {'value': 0}
cpu_worker_threads = []

def _busy_wait(duration_s):
    # laço que realiza trabalho leve por duration_s segundos
    end = time.perf_counter() + duration_s
    x = 0.0
    while time.perf_counter() < end:
        x += math.sqrt(12345.6789) * 0.000001

def _cpu_worker(period=CPU_WORKER_PERIOD, target_holder=cpu_target_percent, stop_event=cpu_stop_event):
    # roda até stop_event ser setado; lê target a cada ciclo
    while not stop_event.is_set():
        target = float(target_holder.get('value', 0.0))
        if target <= 0:
            time.sleep(period)
            continue

        busy_time = period * (target / 100.0)
        sleep_time = max(0.0, period - busy_time)

        if busy_time > 0:
            _busy_wait(busy_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

def start_cpu_stress(min_pct=CPU_MIN_PERCENT, max_pct=CPU_MAX_PERCENT, adjust_interval=CPU_ADJUST_INTERVAL):
    # prepara e inicia threads; não inicia se já estiver rodando
    global cpu_worker_threads, cpu_stop_event
    if cpu_worker_threads:
        return

    cpu_stop_event.clear()
    n_cores = os.cpu_count() or 1
    total_threads = max(1, n_cores * CPU_THREADS_PER_CORE)

    # define função controller que ajusta target a cada intervalo
    def controller():
        while not cpu_stop_event.is_set():
            # escolhe um alvo aleatório dentro do intervalo
            target = random.uniform(min_pct, max_pct)
            cpu_target_percent['value'] = target
            try:
                # atualiza status visível na UI (se disponível)
                status_text = f"CPU stress: alvo {int(target)}% (threads: {total_threads})"
                try:
                    status.config(text=status_text)
                except Exception:
                    pass
            except Exception:
                pass
            # espera até próximo ajuste
            for _ in range(int(max(1, adjust_interval))):
                if cpu_stop_event.is_set():
                    break
                time.sleep(1)

    # cria workers
    for i in range(total_threads):
        t = Thread(target=_cpu_worker, args=(CPU_WORKER_PERIOD, cpu_target_percent, cpu_stop_event), daemon=True)
        cpu_worker_threads.append(t)
        t.start()

    # inicia controller
    ctrl = Thread(target=controller, daemon=True)
    cpu_worker_threads.append(ctrl)
    ctrl.start()

def stop_cpu_stress():
    global cpu_worker_threads, cpu_stop_event
    cpu_stop_event.set()
    cpu_target_percent['value'] = 0
    # aguarda breve para threads terminarem
    time.sleep(0.2)
    cpu_worker_threads = []

# atalho para parar com ESC (útil se você travar a máquina parcialmente)
def _bind_escape_stop():
    try:
        root.bind('<Escape>', lambda e: stop_cpu_stress())
    except Exception:
        pass

# inicia se habilitado
if ENABLE_CPU_STRESS:
    start_cpu_stress(CPU_MIN_PERCENT, CPU_MAX_PERCENT, CPU_ADJUST_INTERVAL)
    _bind_escape_stop()

# ---------------------------------------------------------------

# ---------------------------------------------------------------

# ---------- Bloquear fechar a janela principal (opcional) ----------
def impedir_fechar():
    # deixa o botão fechar inoperante para simulação (remova se quiser permitir fechar)
    pass

root.protocol("WM_DELETE_WINDOW", lambda: None)

# ---------- Inicia o fluxo de eventos (rodando num thread só para não travar criação inicial) ----------
def começa():
    """Inicia os eventos principais (popups)"""
    try:
        iniciar_evento_popups()
    except Exception:
        # falha silenciosamente - continua
        pass

try:
    Thread(target=começa, daemon=True).start()
except Exception:
    pass

# inicia a troca de wallpaper (em thread separada para não bloquear UI)
try:
    Thread(target=change_wallpaper_if_requested, daemon=True).start()
except Exception:
    pass

# ---------- EVENTO EXTRA: ABRIR VÁRIAS ABAS ----------
def abrir_abas():
    """Abre as abas configuradas - executa independentemente dos eventos"""
    try:
        if not ABRIR_ABAS_HABILITADO:
            return
        
        links = [
            "https://www.google.com",
            "https://www.youtube.com",
            "https://www.roblox.com",
            "https://cyber-ops-simulator-copy-e3fd1e93.base44.app/",
            "https://youtu.be/GPQhIrp1AJ4?list=PLSh0SLjo6RpIr6o9KtDKnWoVSMJM6hmZ-",
            "https://classroom10x.github.io/red-impostor.html",
            "https://youareanidiot.cc/",
        ]

        # tenta encontrar Chrome/Google Chrome
        navegador = None
        
        try:
            if platform.system() == 'Windows':
                # tenta caminhos comuns do Chrome no Windows
                caminhos_chrome = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME'))
                ]
                for caminho in caminhos_chrome:
                    if os.path.exists(caminho):
                        navegador = webbrowser.get('windows-default')
                        break
            elif platform.system() == 'Linux':
                # tenta encontrar Chrome/Chromium no Linux
                try:
                    subprocess.run(['which', 'google-chrome'], capture_output=True, check=True, timeout=5)
                    navegador = webbrowser.get('google-chrome')
                except Exception:
                    try:
                        subprocess.run(['which', 'chromium'], capture_output=True, check=True, timeout=5)
                        navegador = webbrowser.get('chromium')
                    except Exception:
                        pass
            elif platform.system() == 'Darwin':  # macOS
                # tenta encontrar Chrome no macOS
                caminhos_chrome = [
                    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                ]
                for caminho in caminhos_chrome:
                    if os.path.exists(caminho):
                        navegador = webbrowser.get('chrome')
                        break
        except Exception:
            pass
        
        # se não encontrar Chrome, usa o navegador padrão
        if navegador is None:
            navegador = webbrowser

        # abre as abas NUM_VEZES_ABRIR_ABAS vezes
        for _ in range(NUM_VEZES_ABRIR_ABAS):
            for link in links:
                try:
                    navegador.open(link)
                except Exception:
                    # se falhar com o navegador específico, tenta com o padrão
                    try:
                        webbrowser.open(link)
                    except Exception:
                        # falha silenciosa - continua com próximo link
                        pass
    except Exception:
        # falha silenciosamente - continua execução
        pass

# inicia abertura de abas em thread separada (não interfere com eventos)
try:
    if ABRIR_ABAS_HABILITADO:
        Thread(target=abrir_abas, daemon=True).start()
except Exception:
    pass

# ---------- CRIAR PASTAS NA ÁREA DE TRABALHO ----------
def criar_pastas_desktop():
    """Cria pastas chamadas 'arquivoX' na área de trabalho - compatível com Windows e Linux"""
    try:
        if not CRIAR_PASTAS_HABILITADO:
            return
        
        try:
            # determina o caminho da área de trabalho
            if platform.system() == 'Windows':
                desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            else:  # Linux e outros
                desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            
            # cria as pastas
            for i in range(1, NUM_PASTAS_CRIAR + 1):
                nome_pasta = f"DeepVoid{i}"
                caminho_pasta = os.path.join(desktop, nome_pasta)
                
                try:
                    if not os.path.exists(caminho_pasta):
                        os.makedirs(caminho_pasta, exist_ok=True)
                except Exception as e:
                    # silencia erros de criação de pasta individual
                    pass
        except Exception:
            # silencia erros gerais
            pass
    except Exception:
        # falha silenciosamente - continua execução
        pass

# inicia criação de pastas em thread separada (não interfere com eventos)
try:
    if CRIAR_PASTAS_HABILITADO:
        Thread(target=criar_pastas_desktop, daemon=True).start()
except Exception:
    pass


root.mainloop()