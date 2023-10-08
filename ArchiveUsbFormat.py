# Software Name: Archive USB Format Free
# License: GPLv3
# Author: Bocaletto Luca

# Nome del Software: Archive USB Format Free
# Licenza: GPLv3
# Autore: Bocaletto Luca

# Importa le librerie necessarie
import tkinter as tk
import subprocess
import psutil

# Funzione per ottenere la lista delle unità USB collegate al computer
def get_usb_drives():
    usb_drives = []
    for partition in psutil.disk_partitions():
        if "removable" in partition.opts:
            usb_drives.append(partition.device)
    return usb_drives

# Funzione per formattare l'unità USB selezionata
def format_usb():
    selected_filesystem = filesystem_var.get()
    selected_drive = drive_var.get()

    # Verifica se è stata selezionata un'unità USB
    if not selected_drive:
        result_label.config(text="Seleziona una chiavetta USB.")
        return

    # Genera il comando di formattazione in base al sistema di file selezionato
    if selected_filesystem == "FAT32":
        cmd = f"format {selected_drive} /fs:FAT32 /q /y"
    elif selected_filesystem == "NTFS":
        cmd = f"format {selected_drive} /fs:NTFS /q /y"
    else:
        result_label.config(text="Seleziona un sistema di file valido.")
        return

    try:
        # Esegue il comando di formattazione
        subprocess.run(cmd, shell=True, check=True)
        result_label.config(text="Formattazione completata con successo.")
    except subprocess.CalledProcessError as e:
        result_label.config(text=f"Errore durante la formattazione: {e}")

# Crea la finestra principale dell'applicazione
root = tk.Tk()
root.title("Formatta Chiavetta USB")

# Etichetta per la selezione del sistema di file
filesystem_label = tk.Label(root, text="Seleziona il sistema di file:")
filesystem_label.pack()

# Variabile per la selezione del sistema di file
filesystem_var = tk.StringVar()
filesystem_var.set("FAT32")

# Menu a tendina per la selezione del sistema di file
filesystem_option_menu = tk.OptionMenu(root, filesystem_var, "FAT32", "NTFS")
filesystem_option_menu.pack()

# Etichetta per la selezione dell'unità USB
drive_label = tk.Label(root, text="Seleziona l'unità USB:")
drive_label.pack()

# Variabile per la selezione dell'unità USB
drive_var = tk.StringVar()

# Ottiene la lista delle unità USB collegate
drive_options = get_usb_drives()

# Verifica se sono presenti unità USB
if not drive_options:
    result_label = tk.Label(root, text="Nessuna chiavetta USB trovata. Collega una chiavetta USB e riprova.")
    result_label.pack()
else:
    # Menu a tendina per la selezione dell'unità USB
    drive_menu = tk.OptionMenu(root, drive_var, *drive_options)
    drive_menu.pack()

# Etichetta per il risultato dell'operazione di formattazione
result_label = tk.Label(root, text="")
result_label.pack()

# Pulsante per avviare la formattazione
format_button = tk.Button(root, text="Formatta", command=format_usb)
format_button.pack()

# Esegui l'applicazione
root.mainloop()
