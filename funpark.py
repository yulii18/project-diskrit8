import heapq
from collections import deque

# --- Data model ---
# Nodes: lokasi di taman
NODES = {
    'Pintu Masuk', 'Lobby', 'RollerCoaster', 'Kincir Angin', 'Rumah Hantu',
    'KidsZone', 'FoodCourt', 'AquaticShow', 'VRCenter'
}

# Peta koneksi dua arah.
GRAPH = {
    'Pintu Masuk':     {'Lobby': 50},
    'Lobby':        {'Pintu Masuk':50, 'RollerCoaster':120, 'Kincir Angin':80, 'FoodCourt':60},
    'RollerCoaster':{'Lobby':120, 'Rumah Hantu':150},
    'Kincir Angin':  {'Lobby':80, 'KidsZone':100},
    'Rumah Hantu': {'RollerCoaster':150, 'VRCenter':70},
    'KidsZone':     {'Kincir Angin':100, 'AquaticShow':140},
    'FoodCourt':    {'Lobby':60, 'AquaticShow':90},
    'AquaticShow':  {'FoodCourt':90, 'KidsZone':140},
    'VRCenter':     {'Rumah Hantu':70}
}

# wahana detaildata: kategori (set), estimated thrill (1-10), node mapping
wahana = {
    'RollerCoaster': {'node':'RollerCoaster', 'kategori': {'ekstrem'}, 'thrill':9},
    'Kincir Angin':   {'node':'Kincir Angin', 'kategori': {'keluarga','pemandangan'}, 'thrill':3},
    'Rumah Hantu':  {'node':'Rumah Hantu', 'kategori': {'horor','ekstrem'}, 'thrill':7},
    'KidsZone':      {'node':'KidsZone', 'kategori': {'anak','edu'}, 'thrill':2},
    'AquaticShow':   {'node':'AquaticShow', 'kategori': {'pertunjukan','keluarga'}, 'thrill':2},
    'VRCenter':      {'node':'VRCenter', 'kategori': {'virtual','edu'}, 'thrill':5}
}

# Status Operasional (Penggunaan Aljabar Boolean)
STATUS = {
    'RollerCoaster': True,
    'Kincir Angin': True,
    'Rumah Hantu': False,   # contoh: sedang maintenance
    'KidsZone': True,
    'AquaticShow': True,
    'VRCenter': True
}

# --- Algoritma Graph ---
def dijkstra(mulai, tujuan):
    """Mengembalikan jarak dan rute terpendek menggunakan algoritma Dijkstra. Jika tidak ditemukan jalur, mengembalikan (inf, [])."""
    if mulai not in GRAPH or tujuan not in GRAPH:
        return float('inf'), []
    pq = [(0, mulai, [mulai])]
    seen = {}
    while pq:
        jarak, node, jalur = heapq.heappop(pq)
        if node == tujuan:
            return jarak, jalur
        if node in seen and seen[node] <= jarak:
            continue
        seen[node] = jarak
        for nb, w in GRAPH.get(node, {}).items():
            nd = jarak + w
            if nb not in seen or nd < seen.get(nb, float('inf')):
                heapq.heappush(pq, (nd, nb, jalur + [nb]))
    return float('inf'), []

def bfs(mulai):
    """Mengembalikan urutan node yang dikunjungi melalui algoritma BFS."""
    q = deque([mulai])
    visited = {mulai}
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in GRAPH.get(u, {}):
            if v not in visited:
                visited.add(v)
                q.append(v)
    return order

# Filter Wahana (Logika Predikat) ---
def filter_wahana(nama_wahana, category=None, min_thrill=0):
    """Mengembalikan True jika wahana tersedia, beroperasi, sesuai kategori (jika diberikan), dan memenuhi nilai minimum thrill."""
    if nama_wahana not in wahana:
        return False
    r = wahana[nama_wahana]
    kondisi_operasional = STATUS.get(nama_wahana, False)           # Boolean
    kategori_kondisi = True if category is None else (category in r['kategori'])
    kondisi_thrill = r['thrill'] >= min_thrill
    return kondisi_operasional and kategori_kondisi and kondisi_thrill

# --- FITUR ---
def daftar_wahana(show_all=False):
    print("\nDaftar Wahana:")
    for name, detail in wahana.items():
        stat = 'Open' if STATUS.get(name, False) else 'Closed'
        cats = ','.join(sorted(detail['kategori']))
        if show_all or STATUS.get(name, False):
            print(f"- {name} (Lokasi: {detail['node']}) | Cat: {cats} | Thrill: {detail['thrill']} | {stat}")

def rekomendasi_terdekat(mulai_node, category=None, min_thrill=0):
    """Mencari wahana terdekat dari mulai_node yang memenuhi kondisi (filterisasi) tertentu."""
    best = (float('inf'), None, None)  # (jarak, nama_wahana, jalur)
    for nama_wahana, detail in wahana.items():
        if not filter_wahana(nama_wahana, category, min_thrill):
            continue
        node = detail['node']
        jarak, jalur = dijkstra(mulai_node, node)
        if jarak < best[0]:
            best = (jarak, nama_wahana, jalur)
    if best[1] is None:
        print("\nTidak ditemukan wahana yang memenuhi kriteria.")
    else:
        jarak, ride, jalur = best
        print(f"\nRekomendasi terdekat: {ride} (jarak {jarak})")
        print("Rute:", " -> ".join(jalur))

def toggle_status(nama_wahana):
    if nama_wahana not in STATUS:
        print("Wahana tidak ditemukan.")
        return
    STATUS[nama_wahana] = not STATUS[nama_wahana]
    print(f"Status {nama_wahana} sekarang: {'Open' if STATUS[nama_wahana] else 'Closed'}")

def tampilan_menu():
    print("""
=== FunPark Navigator ===
1) List wahana (Yang Beroperasi)
2) List semua wahana
3) Rute terpendek antara 2 lokasi wahana
4) Rekomendasi wahana terdekat (filter kategori / thrill)
5) Toggle status wahana (open/close) [admin]
6) BFS traversal dari node
0) Keluar
""")

# --- Main loop ---
def main():
    print("Selamat datang di FunPark Navigator")
    while True:
        tampilan_menu()
        pilihan = input("Pilih menu: ").strip()
        if pilihan == '1':
            daftar_wahana(show_all=False)
            input("\nTekan ENTER untuk kembali...")
        elif pilihan == '2':
            daftar_wahana(show_all=True)
            input("\nTekan ENTER untuk kembali...")
        elif pilihan == '3':
            a = input("Dari node: ").strip()
            b = input("Ke node: ").strip()
            jarak, jalur = dijkstra(a, b)
            if jalur:
                print(f"Jarak terpendek: {jarak}. Rute: {' -> '.join(jalur)}")
            else:
                print("Rute tidak tersedia / node tidak ditemukan.")
            input("\nTekan ENTER untuk kembali...")   
        elif pilihan == '4':
            mulai = input("Posisi pengunjung (node): ").strip()
            cat = input("Kategori (kosong untuk semua): ").strip() or None
            try:
                mt = int(input("Min thrill (0-10): ").strip() or "0")
            except ValueError:
                mt = 0
            rekomendasi_terdekat(mulai, category=cat, min_thrill=mt)
            input("\nTekan ENTER untuk kembali...")
        elif pilihan == '5':
            r = input("Nama wahana untuk toggle status: ").strip()
            toggle_status(r)
            input("\nTekan ENTER untuk kembali...")
        elif pilihan == '6':
            s = input("Mulai BFS dari node: ").strip()
            if s not in GRAPH:
                print("Node tidak ditemukan.")
            else:
                order = bfs(s)
                print("Urutan BFS:", " -> ".join(order))
            input("\nTekan ENTER untuk kembali...")    
        elif pilihan == '0':
            print("Terima Kasih telah Mengunjungi FUN PARK! Sampai jumpa!")
            break
        else:
            print("Perintah tidak dikenal. Pilih menu yang tersedia.")

if __name__ == '__main__':
    main()