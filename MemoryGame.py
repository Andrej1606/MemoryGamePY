import tkinter as tk
import random
from tkinter import messagebox


class IgraPamćenja:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Igra Pamćenja")
        self.root.configure(bg="#f0f0f0")

        self.nivoi = {
            "🟢 Lako (2x2)": 2,
            "🟡 Srednje (4x4)": 4,
            "🔴 Teško (6x6)": 6,
            "🔥 Hard Mode (4x4 + tajmer)": 4,
            "🕶️ Blind Mode (4x4 memorija)": 4
        }

        self.prvi_izabrani = None
        self.drugi_izabrani = None
        self.dugmad = []
        self.vrijednosti = []
        self.okrenute = []
        self.broj_pokusaja = 0
        self.oznaka_tajmera = None
        self.preostalo_vrijeme = 30
        self.hard_mode = False
        self.blind_mode = False

        self.prikazi_pocetak()

    def prikazi_pocetak(self):
        self.obrisi_sve()

        okvir = tk.Frame(self.root, bg="#f0f0f0")
        okvir.pack(expand=True)

        naslov = tk.Label(okvir, text="Igra Pamćenja", font=("Helvetica", 32, "bold"), fg="#333", bg="#f0f0f0")
        naslov.pack(pady=30)

        dugme_pocni = tk.Button(okvir, text="Počni igru", font=("Helvetica", 16), bg="#4CAF50", fg="white",
                              activebackground="#45a049", padx=20, pady=10, command=self.odabir_nivoa)
        dugme_pocni.pack(pady=20)

    def odabir_nivoa(self):
        self.obrisi_sve()
        self.hard_mode = False
        self.blind_mode = False

        okvir = tk.Frame(self.root, bg="#f0f0f0")
        okvir.pack(expand=True)

        labela = tk.Label(okvir, text="Odaberi nivo težine:", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#333")
        labela.pack(pady=20)

        for nivo, velicina in self.nivoi.items():
            dugme = tk.Button(okvir, text=nivo, width=30, font=("Helvetica", 14),
                            bg="#2196F3", fg="white", activebackground="#1976D2",
                            command=lambda n=nivo, v=velicina: self.pocetak_igre(v, n))
            dugme.pack(pady=8)

    def pocetak_igre(self, velicina, ime_nivoa):
        self.velicina = velicina
        self.ukupan_broj_kartica = velicina * velicina
        self.obrisi_sve()

        self.prvi_izabrani = None
        self.drugi_izabrani = None
        self.dugmad = []
        self.vrijednosti = []
        self.okrenute = []
        self.broj_pokusaja = 0
        self.broj_uklopljenih = 0
        self.preostalo_vrijeme = 60

        self.hard_mode = "Hard Mode" in ime_nivoa
        self.blind_mode = "Blind Mode" in ime_nivoa

        brojevi = list(range(1, self.ukupan_broj_kartica // 2 + 1)) * 2
        random.shuffle(brojevi)
        self.vrijednosti = brojevi

        self.okvir_info = tk.Frame(self.root, bg="#f0f0f0")
        self.okvir_info.pack(pady=10)

        self.oznaka_pokusaja = tk.Label(self.okvir_info, text="🔁 Pokušaji: 0", font=("Helvetica", 12), bg="#f0f0f0", fg="#555")
        self.oznaka_pokusaja.pack(side=tk.LEFT, padx=10)

        if self.hard_mode:
            self.oznaka_tajmera = tk.Label(self.okvir_info, text=f"⏱️ Vrijeme: {self.preostalo_vrijeme}s", font=("Helvetica", 12), bg="#f0f0f0", fg="#c62828")
            self.oznaka_tajmera.pack(side=tk.RIGHT, padx=10)
            self.azuriraj_tajmer()

        self.okvir_karte = tk.Frame(self.root, bg="#f0f0f0")
        self.okvir_karte.pack(pady=20)

        if velicina == 6:
            sirina = 8
            visina = 4
            font = ("Helvetica", 10, "bold")
        elif velicina == 4:
            sirina = 6
            visina = 3
            font = ("Helvetica", 14, "bold")
        else:
            sirina = 8
            visina = 4
            font = ("Helvetica", 16, "bold")

