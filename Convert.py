import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread

# Drapeau pour vérifier si l'annulation a été demandée
cancel_flag = False

def video_to_images(video_path, output_folder):
    global cancel_flag
    cancel_flag = False  # Réinitialiser le drapeau d'annulation

    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)
    
    # Vérifier si la vidéo a été ouverte correctement
    if not cap.isOpened():
        messagebox.showerror("Erreur", "Impossible d'ouvrir la vidéo.")
        return
    
    # S'assurer que le dossier de sortie existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Compteur pour nommer les images
    frame_count = 0
    
    # Boucle à travers chaque frame de la vidéo
    while True:
        if cancel_flag:
            break
        
        ret, frame = cap.read()
        
        # Vérifier si la frame a été lue correctement
        if not ret:
            break
        
        # Redimensionner l'image à 1920x1080 (Full HD)
        frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_AREA)
        
        # Enregistrer la frame sous forme d'image avec une meilleure qualité
        image_path = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 100 est le meilleur taux de qualité
        
        # Incrémenter le compteur de frame
        frame_count += 1
    
    # Fermer la vidéo
    cap.release()
    
    if cancel_flag:
        messagebox.showinfo("Annulé", "Conversion annulée.")
    else:
        messagebox.showinfo("Terminé", f"Conversion terminée. {frame_count} images ont été créées.")

def select_video():
    video_path = filedialog.askopenfilename(title="Sélectionner une vidéo", filetypes=[("Fichiers vidéo", "*.mp4 *.avi *.mov")])
    video_entry.delete(0, tk.END)
    video_entry.insert(0, video_path)

def select_output_folder():
    output_folder = filedialog.askdirectory(title="Sélectionner un dossier de sortie")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_folder)

def start_conversion():
    video_path = video_entry.get()
    output_folder = output_entry.get()
    if not video_path or not output_folder:
        messagebox.showwarning("Attention", "Veuillez sélectionner une vidéo et un dossier de sortie.")
        return
    # Lancer la conversion dans un thread séparé
    conversion_thread = Thread(target=video_to_images, args=(video_path, output_folder))
    conversion_thread.start()

def cancel_conversion():
    global cancel_flag
    cancel_flag = True

# Configuration de l'interface graphique
root = tk.Tk()
root.title("SANOU Bakary - Extraction d'images dans une Vidéo")

tk.Label(root, text="Vidéo:").grid(row=0, column=0, padx=10, pady=10)
video_entry = tk.Entry(root, width=50)
video_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Sélectionner", command=select_video).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Dossier de sortie:").grid(row=1, column=0, padx=10, pady=10)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Sélectionner", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Convertir", command=start_conversion).grid(row=2, column=0, padx=10, pady=20)
tk.Button(root, text="Annuler", command=cancel_conversion).grid(row=2, column=1, padx=10, pady=20)

root.mainloop()
