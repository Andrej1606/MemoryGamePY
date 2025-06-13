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

        for i in range(self.ukupan_broj_kartica):
            dugme = tk.Button(
                self.okvir_karte,
                text=" ",
                width=sirina,
                height=visina,
                font=font,
                relief="raised",
                bg="#ffffff",
                fg="#333",
                bd=3,
                command=lambda idx=i: self.okreni_karticu(idx)
            )
            dugme.grid(row=i // velicina, column=i % velicina, padx=4, pady=4)
            self.dugmad.append(dugme)

        self.dugme_nazad = tk.Button(self.root, text="⬅️ Nazad na izbor nivoa", font=("Helvetica", 12),
                                  bg="#e0e0e0", command=self.odabir_nivoa)
        self.dugme_nazad.pack(pady=10)

        if self.hard_mode or self.blind_mode:
            self.prikazi_sve_karte()

    def prikazi_sve_karte(self):
        for i, dugme in enumerate(self.dugmad):
            dugme.config(text=str(self.vrijednosti[i]), state="disabled", bg="#E8F5E9")
        self.root.after(3000, self.sakrij_karte)

    def sakrij_karte(self):
        for i, dugme in enumerate(self.dugmad):
            dugme.config(text=" ", state="normal", bg="#ffffff")

    def okreni_karticu(self, idx):
        if idx in self.okrenute or self.drugi_izabrani is not None:
            return

        if self.blind_mode:
            if self.prvi_izabrani is None:
                self.prvi_izabrani = idx
            elif self.prvi_izabrani != idx and self.drugi_izabrani is None:
                self.drugi_izabrani = idx
                self.root.after(400, self.provjeri_poklapanje)
            return

        dugme = self.dugmad[idx]
        dugme.config(text=str(self.vrijednosti[idx]), state="disabled", disabledforeground="black", bg="#BBDEFB")

        if self.prvi_izabrani is None:
            self.prvi_izabrani = idx
        elif self.prvi_izabrani != idx and self.drugi_izabrani is None:
            self.drugi_izabrani = idx
            self.root.after(400, self.provjeri_poklapanje)

    def provjeri_poklapanje(self):
        self.broj_pokusaja += 1
        self.oznaka_pokusaja.config(text=f"Pokušaji: {self.broj_pokusaja}")

        vrijednost_prve = self.vrijednosti[self.prvi_izabrani]
        vrijednost_druge = self.vrijednosti[self.drugi_izabrani]

        if vrijednost_prve == vrijednost_druge:
            self.okrenute.extend([self.prvi_izabrani, self.drugi_izabrani])
            self.broj_uklopljenih += 1

            if self.blind_mode:
                self.dugmad[self.prvi_izabrani].config(text=str(vrijednost_prve), state="disabled", bg="#C8E6C9")
                self.dugmad[self.drugi_izabrani].config(text=str(vrijednost_druge), state="disabled", bg="#C8E6C9")

            if self.broj_uklopljenih == self.ukupan_broj_kartica // 2:
                messagebox.showinfo("Čestitamo!", f"Pobijedili ste za {self.broj_pokusaja} pokušaja!")
                self.odabir_nivoa()
        else:
            if not self.blind_mode:
                self.dugmad[self.prvi_izabrani].config(text=" ", state="normal", bg="#ffffff")
                self.dugmad[self.drugi_izabrani].config(text=" ", state="normal", bg="#ffffff")

        if self.blind_mode and vrijednost_prve != vrijednost_druge:
            pass  # sve ostaje skriveno

        self.prvi_izabrani = None
        self.drugi_izabrani = None

    def azuriraj_tajmer(self):
        if not self.hard_mode:
            return
        self.preostalo_vrijeme -= 1
        if self.oznaka_tajmera:
            self.oznaka_tajmera.config(text=f"⏱️ Vrijeme: {self.preostalo_vrijeme}s")
        if self.preostalo_vrijeme == 0:
            messagebox.showwarning("⏰ Vrijeme isteklo", "Nažalost, isteklo je vrijeme.")
            self.odabir_nivoa()
        else:
            self.root.after(1000, self.azuriraj_tajmer)

    def obrisi_sve(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x700")
    root.resizable(False, False)
    igra = IgraPamćenja(root)
    root.mainloop()

