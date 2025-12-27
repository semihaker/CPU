import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import sys
import os
import math

# =============================================================================
# [BÖLÜM 1] VERİ YAPILARI (İŞLEM/SÜREÇ)
# =============================================================================
class ServerProcess:
    def __init__(self, pid, arrival_time, burst_time, memory):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.memory = memory             
        self.remaining_time = burst_time 
        self.finish_time = -1            

# =============================================================================
# [BÖLÜM 2] ALGORİTMA MOTORU
# =============================================================================
def solve_logic(data, mode, q, cs_cost):
    procs_exec = [ServerProcess(*p) for p in data]
    curr = 0      
    completed = 0 
    n = len(procs_exec)
    
    def get_ready_queue(current_time):
        return [p for p in procs_exec if p.arrival_time <= current_time and p.remaining_time > 0]

    last_pid = None 

    if mode == "FCFS":
        while completed < n:
            arrived = get_ready_queue(curr)
            if not arrived:
                curr += 1
                continue
            target = min(arrived, key=lambda x: x.arrival_time)
            if last_pid is not None and target.pid != last_pid and cs_cost > 0:
                curr += cs_cost
            curr += target.burst_time
            target.remaining_time = 0
            target.finish_time = curr
            completed += 1
            last_pid = target.pid

    else: # RR ve SRTF
        rr_queue = []; rr_added = set(); current_proc = None; q_timer = 0
        while completed < n:
            ready_candidates = get_ready_queue(curr)
            if not ready_candidates:
                curr += 1; last_pid = None; continue
            target = None
            if mode == "SRTF": target = min(ready_candidates, key=lambda x: x.remaining_time)
            elif mode == "RR":
                new_arrivals = [p for p in ready_candidates if p.pid not in rr_added]
                new_arrivals.sort(key=lambda x: x.arrival_time)
                for p in new_arrivals: rr_queue.append(p); rr_added.add(p.pid)
                if current_proc and current_proc.remaining_time > 0 and q_timer == 0: rr_queue.append(current_proc)
                if not rr_queue: target = current_proc 
                else: target = rr_queue[0]
            
            if last_pid is not None and target.pid != last_pid and cs_cost > 0:
                curr += cs_cost
            
            target.remaining_time -= 1; curr += 1; last_pid = target.pid
            
            if mode == "RR":
                current_proc = target; q_timer += 1
                if target.remaining_time == 0: 
                    rr_queue.pop(0); q_timer = 0; current_proc = None; target.finish_time = curr; completed += 1
                elif q_timer == q: rr_queue.pop(0); q_timer = 0
            else: # SRTF
                if target.remaining_time == 0: target.finish_time = curr; completed += 1

    return procs_exec

def solve_logic_visual(data, mode, q, cs_cost):
    procs_exec = [ServerProcess(*p) for p in data]
    timeline = [] 
    curr = 0      
    completed = 0 
    n = len(procs_exec)
    
    def get_ready_queue(current_time):
        return [p for p in procs_exec if p.arrival_time <= current_time and p.remaining_time > 0]

    last_pid = None 
    
    if mode == "FCFS":
        while completed < n:
            arrived = get_ready_queue(curr)
            if not arrived:
                timeline.append((curr, "IDLE", -1, []))
                curr += 1
                continue
            target = min(arrived, key=lambda x: x.arrival_time)
            if last_pid is not None and target.pid != last_pid and cs_cost > 0:
                for _ in range(cs_cost):
                    timeline.append((curr, "CS", -1, [p.pid for p in arrived]))
                    curr += 1
            dur = target.burst_time
            for _ in range(dur):
                others = [p.pid for p in get_ready_queue(curr) if p.pid != target.pid]
                timeline.append((curr, "ACTIVE", target.pid, others))
                curr += 1
            target.remaining_time = 0
            target.finish_time = curr
            completed += 1
            last_pid = target.pid
    else: 
        rr_queue = []; rr_added = set(); current_proc = None; q_timer = 0
        while completed < n:
            ready_candidates = get_ready_queue(curr)
            if not ready_candidates:
                timeline.append((curr, "IDLE", -1, []))
                curr += 1; last_pid = None; continue
            target = None
            if mode == "SRTF": target = min(ready_candidates, key=lambda x: x.remaining_time)
            elif mode == "RR":
                new_arrivals = [p for p in ready_candidates if p.pid not in rr_added]
                new_arrivals.sort(key=lambda x: x.arrival_time)
                for p in new_arrivals: rr_queue.append(p); rr_added.add(p.pid)
                if current_proc and current_proc.remaining_time > 0 and q_timer == 0: rr_queue.append(current_proc)
                if not rr_queue: target = current_proc 
                else: target = rr_queue[0]
            is_switch = (last_pid is not None) and (target.pid != last_pid)
            if is_switch and cs_cost > 0:
                for _ in range(cs_cost):
                    others_cs = [p.pid for p in ready_candidates]
                    timeline.append((curr, "CS", -1, others_cs))
                    curr += 1
            others = [p.pid for p in get_ready_queue(curr) if p.pid != target.pid]
            timeline.append((curr, "ACTIVE", target.pid, others))
            target.remaining_time -= 1; curr += 1; last_pid = target.pid
            if mode == "RR":
                current_proc = target; q_timer += 1
                if target.remaining_time == 0: rr_queue.pop(0); q_timer = 0; current_proc = None; target.finish_time = curr; completed += 1
                elif q_timer == q: rr_queue.pop(0); q_timer = 0
            else: 
                if target.remaining_time == 0: target.finish_time = curr; completed += 1
    return timeline, procs_exec

# =============================================================================
# [BÖLÜM 3] BİLİMSEL TEST PENCERESİ (3'lü Karşılaştırma)
# =============================================================================
class HypothesisWindow:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Çoklu Hipotez Testi Modülü (ANOVA/T-Testi)")
        self.win.geometry("700x650")
        self.win.configure(bg="#2d2d2d")
        
        ttk.Label(self.win, text="3 Algoritma Karşılaştırmalı Test", font=("Arial", 14, "bold"), background="#2d2d2d", foreground="#f1c40f").pack(pady=10)
        
        info_text = "Monte Carlo Simülasyonu (N=30) ile 3 farklı algoritmayı aynı veri setlerinde yarıştırır.\nEn iyi performansı göstereni belirler ve istatistiksel anlamlılık testi yapar."
        ttk.Label(self.win, text=info_text, background="#2d2d2d", foreground="white", justify="center").pack(pady=5)
        
        frame_sel = tk.Frame(self.win, bg="#2d2d2d")
        frame_sel.pack(pady=15)
        
        # Algoritma A Seçimi
        ttk.Label(frame_sel, text="Algoritma A:", background="#2d2d2d", foreground="white").grid(row=0, column=0, padx=5)
        self.algo_a = ttk.Combobox(frame_sel, values=["FCFS", "SRTF", "RR"], state="readonly", width=10)
        self.algo_a.set("FCFS")
        self.algo_a.grid(row=0, column=1, padx=5)
        
        # Algoritma B Seçimi
        ttk.Label(frame_sel, text="Algoritma B:", background="#2d2d2d", foreground="white").grid(row=0, column=2, padx=5)
        self.algo_b = ttk.Combobox(frame_sel, values=["FCFS", "SRTF", "RR"], state="readonly", width=10)
        self.algo_b.set("RR")
        self.algo_b.grid(row=0, column=3, padx=5)

        # Algoritma C Seçimi (YENİ)
        ttk.Label(frame_sel, text="Algoritma C:", background="#2d2d2d", foreground="white").grid(row=0, column=4, padx=5)
        self.algo_c = ttk.Combobox(frame_sel, values=["FCFS", "SRTF", "RR"], state="readonly", width=10)
        self.algo_c.set("SRTF")
        self.algo_c.grid(row=0, column=5, padx=5)
        
        tk.Button(self.win, text="🧪 3'LÜ ANALİZİ BAŞLAT", command=self.run_test, bg="#27ae60", fg="white", font=("Arial", 11, "bold")).pack(pady=10)
        
        self.txt_output = tk.Text(self.win, height=20, width=80, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
        self.txt_output.pack(pady=10, padx=10)

    def run_test(self):
        names = [self.algo_a.get(), self.algo_b.get(), self.algo_c.get()]
        
        # Aynı algoritmayı seçme uyarısı (İsteğe bağlı)
        if len(set(names)) < 2:
             self.txt_output.insert(tk.END, "Uyarı: Benzer algoritmalar seçildi, yine de test ediliyor...\n")

        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, f"Monte Carlo Simülasyonu (N=30) Başlatılıyor...\n")
        self.txt_output.insert(tk.END, "-"*60 + "\n")
        
        results = {names[0]: [], names[1]: [], names[2]: []}
        
        # 30 Kez Simülasyon
        for i in range(30):
            test_data = []
            for pid in range(1, 6):
                at = random.randint(0, 5)
                bt = random.randint(2, 10) 
                mem = 512
                test_data.append((pid, at, bt, mem))
            
            # 3 Algoritmayı da aynı veriyle çalıştır
            for algo_name in names:
                res = solve_logic(test_data, algo_name, q=2, cs_cost=1)
                wait = sum((p.finish_time - p.arrival_time - p.burst_time) for p in res) / len(res)
                results[algo_name].append(wait)
        
        # İstatistik Hesapla
        stats = []
        for name in list(set(names)): # Unique isimler üzerinden git
            data_pts = results[name]
            mean = sum(data_pts) / 30
            var = sum((x - mean) ** 2 for x in data_pts) / 29
            stats.append({"name": name, "mean": mean, "var": var, "data": data_pts})
        
        # Performans Sıralaması (Küçük olan iyi)
        stats.sort(key=lambda x: x["mean"])
        
        self.txt_output.insert(tk.END, ">>> PERFORMANS SIRALAMASI (Düşük Daha İyi) <<<\n")
        for i, s in enumerate(stats):
            self.txt_output.insert(tk.END, f"{i+1}. {s['name']} \t| Ort. Bekleme: {s['mean']:.2f} ms\n")
        
        self.txt_output.insert(tk.END, "\n>>> KRİTİK KARŞILAŞTIRMA (1. vs 2.) <<<\n")
        
        # En iyi (Winner) ve İkinci (Runner-up) arasında T-Testi
        best = stats[0]
        second = stats[1]
        
        std_err = math.sqrt((best['var']/30) + (second['var']/30))
        if std_err == 0: t_score = 0
        else: t_score = (second['mean'] - best['mean']) / std_err # Pozitif çıksın diye ters aldım
        
        self.txt_output.insert(tk.END, f"Karşılaştırılan: {best['name']} vs {second['name']}\n")
        self.txt_output.insert(tk.END, f"Fark: {second['mean'] - best['mean']:.2f} ms\n")
        self.txt_output.insert(tk.END, f"T-Skoru: {t_score:.4f}\n")
        
        if abs(t_score) > 2.04:
            self.txt_output.insert(tk.END, f"SONUÇ: {best['name']} istatistiksel olarak ANLAMLI derecede daha iyi.\n")
            self.txt_output.insert(tk.END, "(P < 0.05, Şans faktörü elendi.)\n")
        else:
            self.txt_output.insert(tk.END, f"SONUÇ: {best['name']} daha iyi görünüyor ama fark ANLAMLI DEĞİL.\n")
            self.txt_output.insert(tk.END, "(İki algoritma benzer performans sergiliyor.)\n")

# =============================================================================
# [BÖLÜM 4] ANA ARAYÜZ (GUI - TÜRKÇE)
# =============================================================================
class CPULabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("İşlem Zamanlama Analiz Aracı (Process Scheduling Analysis Tool)") 
        self.root.geometry("1600x950")
        self.root.configure(bg="#1e1e1e")
        
        # --- SENARYOLAR ---
        self.scenarios = {
            "Normal / Dengeli Senaryo": [
                (1, 0, 8, 512), 
                (2, 2, 4, 1024), 
                (3, 4, 9, 256), 
                (4, 5, 5, 2048)
            ],
            "Konvoy Etkisi (FCFS Hatası)": [
                (1, 0, 40, 4096), 
                (2, 1, 2, 256), 
                (3, 2, 2, 512), 
                (4, 3, 2, 256)
            ],
            # 30'luk Büyük Veri Seti (Vize Projesi Stres Testi)
            "Büyük Test (30 İşlem - Yüksek Yük)": [
                (1, 5, 3, 2048), (2, 5, 7, 256), (3, 12, 2, 2048), (4, 14, 20, 2048), (5, 1, 20, 256),
                (6, 9, 2, 256), (7, 6, 6, 256), (8, 4, 3, 2048), (9, 11, 11, 2048), (10, 11, 18, 4096),
                (11, 10, 20, 1024), (12, 4, 16, 256), (13, 4, 7, 512), (14, 3, 12, 512), (15, 5, 12, 1024),
                (16, 13, 3, 1024), (17, 15, 19, 2048), (18, 13, 20, 1024), (19, 4, 19, 4096), (20, 9, 13, 4096),
                (21, 14, 15, 4096), (22, 9, 8, 2048), (23, 6, 10, 512), (24, 3, 12, 2048), (25, 3, 7, 2048),
                (26, 11, 12, 512), (27, 14, 18, 1024), (28, 12, 15, 1024), (29, 7, 18, 2048), (30, 4, 16, 4096)
            ]
        }
        
        self.colors = {1: "#3498db", 2: "#2ecc71", 3: "#f1c40f", 4: "#e74c3c", 5: "#9b59b6", 6: "#16a085", -1: "#34495e"}
        self.comparison_history = {"Algo": [], "Wait": []}
        self.anim_job = None 
        
        self.setup_ui()
        
        # AÇILIŞTA DİREKT 30'LUK LİSTEYİ YÜKLE
        self.combo_scenario.set("Büyük Test (30 İşlem - Yüksek Yük)")
        self.load_scenario() 

    def setup_ui(self):
        ctrl = tk.Frame(self.root, bg="#2d2d2d", pady=10)
        ctrl.pack(fill=tk.X)
        
        # --- Sol Taraf ---
        grp_data = tk.LabelFrame(ctrl, text=" Veri Yönetimi ", fg="#ecf0f1", bg="#2d2d2d", padx=5)
        grp_data.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(grp_data, text="Senaryo:", background="#2d2d2d", foreground="#f1c40f").pack(side=tk.LEFT)
        self.combo_scenario = ttk.Combobox(grp_data, values=list(self.scenarios.keys()), width=30, state="readonly")
        self.combo_scenario.pack(side=tk.LEFT, padx=5)
        self.combo_scenario.bind("<<ComboboxSelected>>", self.load_scenario)
        
        ttk.Label(grp_data, text="| PID:", background="#2d2d2d", foreground="white").pack(side=tk.LEFT, padx=(10, 0))
        self.e_pid = ttk.Entry(grp_data, width=3); self.e_pid.pack(side=tk.LEFT, padx=2)
        ttk.Label(grp_data, text="Geliş(AT):", background="#2d2d2d", foreground="white").pack(side=tk.LEFT)
        self.e_at = ttk.Entry(grp_data, width=3); self.e_at.pack(side=tk.LEFT, padx=2)
        ttk.Label(grp_data, text="Süre(BT):", background="#2d2d2d", foreground="white").pack(side=tk.LEFT)
        self.e_bt = ttk.Entry(grp_data, width=3); self.e_bt.pack(side=tk.LEFT, padx=2)
        tk.Button(grp_data, text="+", command=self.add_p, bg="#3498db", fg="white", width=3).pack(side=tk.LEFT, padx=5)

        # --- Orta Taraf ---
        grp_sim = tk.Frame(ctrl, bg="#2d2d2d")
        grp_sim.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(grp_sim, text="Algoritma:", background="#2d2d2d", foreground="white").pack(side=tk.LEFT)
        self.algo_box = ttk.Combobox(grp_sim, values=["FCFS", "SRTF", "RR"], width=8, state="readonly")
        self.algo_box.set("RR"); self.algo_box.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(grp_sim, text="Kuantum(Q):", background="#2d2d2d", foreground="white").pack(side=tk.LEFT)
        self.ent_q = ttk.Entry(grp_sim, width=3); self.ent_q.insert(0,"2"); self.ent_q.pack(side=tk.LEFT)

        ttk.Label(grp_sim, text="CS Maliyeti:", background="#2d2d2d", foreground="#e74c3c").pack(side=tk.LEFT, padx=(10,0))
        self.ent_cs = ttk.Entry(grp_sim, width=3); self.ent_cs.insert(0,"1"); self.ent_cs.pack(side=tk.LEFT)
        
        tk.Button(ctrl, text="▶ BAŞLAT", command=self.start_sim, bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=10).pack(side=tk.LEFT, padx=15)
        tk.Button(ctrl, text="⟳ Yeniden Başlat", command=self.restart_program, bg="#c0392b", fg="white").pack(side=tk.LEFT)
        
        tk.Button(ctrl, text="🧪 Bilimsel Test", command=self.open_hypothesis, bg="#8e44ad", fg="white").pack(side=tk.LEFT, padx=15)

        # --- Görsel Alanlar ---
        mid_panel = tk.Frame(self.root, bg="#1e1e1e")
        mid_panel.pack(fill=tk.BOTH, expand=True)
        left_viz = tk.Frame(mid_panel, bg="#1e1e1e")
        left_viz.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.hw_canvas = tk.Canvas(left_viz, width=950, height=160, bg="#1e1e1e", highlightthickness=0)
        self.hw_canvas.pack(pady=5)
        self.draw_hardware_static()

        self.fig, self.ax = plt.subplots(figsize=(8, 4), facecolor='#1e1e1e')
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=left_viz)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.ax.set_facecolor('#1e1e1e')

        right_stats = tk.Frame(mid_panel, bg="#252526", width=480)
        right_stats.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        lbl_t = tk.Label(right_stats, text="İşlem Listesi (Metadata)", bg="#252526", fg="white", font=("Arial", 10, "bold"))
        lbl_t.pack(pady=5)
        self.proc_tree = ttk.Treeview(right_stats, columns=("P","A","B","M"), show="headings", height=8)
        self.proc_tree.heading("P", text="İşlem No (PID)"); self.proc_tree.column("P", width=80, anchor="center")
        self.proc_tree.heading("A", text="Varış (AT)"); self.proc_tree.column("A", width=80, anchor="center")
        self.proc_tree.heading("B", text="Süre (BT)"); self.proc_tree.column("B", width=80, anchor="center")
        self.proc_tree.heading("M", text="Hafıza (MB)"); self.proc_tree.column("M", width=100, anchor="center")
        self.proc_tree.pack(fill=tk.X, padx=5)

        lbl_r = tk.Label(right_stats, text="Simülasyon Sonuçları", bg="#252526", fg="white", font=("Arial", 10, "bold"))
        lbl_r.pack(pady=(15,5))
        self.res_tree = ttk.Treeview(right_stats, columns=("M","W","T"), show="headings", height=4)
        self.res_tree.heading("M", text="Algoritma"); self.res_tree.column("M",width=90, anchor="center")
        self.res_tree.heading("W", text="Ort. Bekleme"); self.res_tree.column("W",width=110, anchor="center")
        self.res_tree.heading("T", text="Ort. Dönüş"); self.res_tree.column("T",width=110, anchor="center")
        self.res_tree.pack(fill=tk.X, padx=5)

        lbl_g = tk.Label(right_stats, text="Performans Karşılaştırması", bg="#252526", fg="#f1c40f", font=("Arial", 10, "bold"))
        lbl_g.pack(pady=(15,5))
        self.fig_bar, self.ax_bar = plt.subplots(figsize=(4, 3), facecolor='#252526')
        self.canvas_bar = FigureCanvasTkAgg(self.fig_bar, master=right_stats)
        self.canvas_bar.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.ax_bar.set_facecolor('#252526')

    def open_hypothesis(self):
        HypothesisWindow(self.root)

    def draw_hardware_static(self):
        self.hw_canvas.create_rectangle(420, 30, 620, 130, outline="#00ff00", width=3, tags="cpu_box")
        self.hw_canvas.create_text(520, 145, text="MERKEZİ İŞLEM BİRİMİ (CPU)", fill="#00ff00", font=("Consolas", 10))
        self.hw_canvas.create_line(270, 80, 410, 80, fill="#f1c40f", arrow=tk.LAST, width=3)
        self.hw_canvas.create_text(320, 65, text="Hazır Kuyruğu", fill="#f1c40f", font=("Arial", 9))
        self.hw_canvas.create_line(630, 80, 770, 80, fill="#e74c3c", arrow=tk.LAST, width=3)
        self.hw_canvas.create_text(720, 65, text="Tamamlananlar", fill="#e74c3c", font=("Arial", 9))

    def load_scenario(self, event=None):
        selected = self.combo_scenario.get()
        if selected in self.scenarios:
            self.stop_animation()
            self.ax.clear()
            self.canvas_plot.draw()
            self.raw_data = list(self.scenarios[selected])
            self.refresh_proc_list()
            self.comparison_history = {"Algo": [], "Wait": []}
            self.ax_bar.clear()
            self.canvas_bar.draw()

    def add_p(self):
        try:
            pid = int(self.e_pid.get())
            at = int(self.e_at.get())
            bt = int(self.e_bt.get())
            possible_mems = [256, 512, 1024, 2048, 4096]
            mem = random.choice(possible_mems)
            self.raw_data.append((pid, at, bt, mem))
            self.refresh_proc_list()
        except: pass

    def stop_animation(self):
        if self.anim_job is not None:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None

    def restart_program(self):
        self.root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def refresh_proc_list(self):
        for i in self.proc_tree.get_children(): self.proc_tree.delete(i)
        for p in sorted(self.raw_data): 
            display_values = (p[0], f"{p[1]} ms", f"{p[2]} ms", f"{p[3]} MB")
            self.proc_tree.insert("", "end", values=display_values)

    def start_sim(self):
        if not self.raw_data: return
        try:
            q_val = int(self.ent_q.get())
            if q_val < 1:
                messagebox.showerror("Hata", "Kuantum süresi (Q) en az 1 olmalıdır!")
                return
        except ValueError:
            messagebox.showerror("Hata", "Lütfen Q değeri için geçerli bir sayı giriniz.")
            return

        self.stop_animation() 
        self.ax.clear()
        
        algo = self.algo_box.get()
        q = q_val
        cs = int(self.ent_cs.get())
        
        self.timeline, self.p_results = solve_logic_visual(self.raw_data, algo, q, cs)
        
        pids = sorted([p[0] for p in self.raw_data])
        self.ax.set_yticks(pids)
        self.ax.set_yticklabels([f"İşlem {p}" for p in pids], color='white', fontsize=10) 
        self.ax.set_xlabel("Zaman Birimi (ms)", color="white")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.grid(True, linestyle='--', alpha=0.1)
        
        self.step = 0
        self.animate()
        
        total_wait = sum((p.finish_time - p.arrival_time - p.burst_time) for p in self.p_results)
        avg_wait = total_wait / len(self.p_results)
        avg_turn = sum((p.finish_time - p.arrival_time) for p in self.p_results) / len(self.p_results)
        
        self.res_tree.insert("", 0, values=(algo, f"{avg_wait:.2f} ms", f"{avg_turn:.2f} ms"))
        self.update_comparison_chart(algo, avg_wait)

    def update_comparison_chart(self, algo_name, avg_wait):
        self.comparison_history["Algo"].append(algo_name)
        self.comparison_history["Wait"].append(avg_wait)
        self.ax_bar.clear()
        colors = ['#e74c3c', '#2ecc71', '#f1c40f', '#3498db', '#9b59b6']
        bars = self.ax_bar.bar(self.comparison_history["Algo"], self.comparison_history["Wait"], color=colors[:len(self.comparison_history["Algo"])])
        self.ax_bar.set_title("Ortalama Bekleme Süresi Karşılaştırması", color="white", fontsize=9)
        self.ax_bar.tick_params(colors='white', labelsize=8)
        self.ax_bar.spines['bottom'].set_color('white')
        self.ax_bar.spines['left'].set_color('white')
        self.ax_bar.spines['top'].set_visible(False)
        self.ax_bar.spines['right'].set_visible(False)
        self.ax_bar.set_ylabel("Zaman (ms)", color="white", fontsize=8)
        for bar in bars:
            height = bar.get_height()
            self.ax_bar.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f} ms', ha='center', va='bottom', color='white', fontsize=8)
        self.canvas_bar.draw()

    def animate(self):
        if self.step < len(self.timeline):
            t, state, pid, queue = self.timeline[self.step]
            self.hw_canvas.delete("anim_obj")
            if state == "ACTIVE":
                color = self.colors.get(pid, "white")
                self.hw_canvas.create_oval(490, 50, 550, 110, fill=color, tags="anim_obj")
                self.hw_canvas.create_text(520, 80, text=f"P{pid}", fill="black", font=("Arial", 12, "bold"), tags="anim_obj")
                self.hw_canvas.create_text(520, 100, text="ÇALIŞIYOR", fill="white", font=("Arial", 8), tags="anim_obj")
                self.ax.barh(pid, 1, left=t, color=color, edgecolor='black', alpha=0.9)
            elif state == "CS":
                self.hw_canvas.create_rectangle(470, 50, 570, 110, fill="#7f8c8d", outline="white", tags="anim_obj")
                self.hw_canvas.create_text(520, 80, text="GEÇİŞ", fill="white", font=("Arial", 10, "bold"), tags="anim_obj")
                self.hw_canvas.create_text(520, 95, text="Maliyet", fill="#bdc3c7", font=("Arial", 8), tags="anim_obj")
                self.ax.axvspan(t, t+1, color='#7f8c8d', alpha=0.5, hatch='///')
            elif state == "IDLE":
                self.hw_canvas.create_text(520, 80, text="BOŞTA", fill="#95a5a6", font=("Arial", 14), tags="anim_obj")
            for i, q_pid in enumerate(queue[:6]):
                qx = 370 - (i * 40)
                q_color = self.colors.get(q_pid, "white")
                self.hw_canvas.create_rectangle(qx, 70, qx+30, 90, fill=q_color, tags="anim_obj")
                self.hw_canvas.create_text(qx+15, 80, text=f"P{q_pid}", fill="black", font=("Arial", 8), tags="anim_obj")
            self.ax.set_xlim(0, max(self.step + 5, 20))
            self.canvas_plot.draw()
            self.step += 1
            self.anim_job = self.root.after(12, self.animate)
        else:
            self.anim_job = None

if __name__ == "__main__":
    root = tk.Tk()
    app = CPULabApp(root)
    root.mainloop()