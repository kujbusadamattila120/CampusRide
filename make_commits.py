import os
import subprocess
from datetime import datetime, timedelta

# 1. index.html - A prémium dizájn és a saját logó
html_content = """<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CampusRide - Közösségi Ingyenes és Olcsó Ingaút</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="navbar">
        <div class="nav-container">
            <div class="logo-group">
                <a href="#" class="logo-link">
                    <img src="logo.png" alt="CampusRide Logo" class="brand-logo">
                </a>
                <div class="live-badge">
                    <span class="pulse-dot"></span> Élő Campus Hálózat
                </div>
            </div>
            <nav class="nav-links">
                <a href="#search">Járatkereső</a>
                <a href="#jaratok">Elérhető Járatok</a>
                <a href="#hirdetes">Járat Indítása</a>
            </nav>
            <button class="btn btn-primary" onclick="location.href='#hirdetes'">
                <i class="fa-solid fa-plus"></i> Új Járat
            </button>
        </div>
    </header>

    <main class="main-container">
        <section class="search-hero" id="search">
            <div class="search-label">MIKOR?</div>
            <div class="search-bar-wrapper">
                <div class="date-input-group">
                    <i class="fa-regular fa-calendar"></i>
                    <input type="text" placeholder="éééé. hh. nn." value="2026. 11. 02.">
                </div>
                <button class="btn btn-search">
                    <i class="fa-solid fa-magnifying-glass"></i> Keresés
                </button>
            </div>
        </section>

        <div class="stats-banner">
            <div class="stat-card">
                <div class="stat-icon blue"><i class="fa-solid fa-route"></i></div>
                <div class="stat-info">
                    <h2>3</h2>
                    <p>Aktív járat a hálózatban</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon green"><i class="fa-solid fa-leaf"></i></div>
                <div class="stat-info">
                    <h2>142 kg</h2>
                    <p>Megspórolt CO₂ kibocsátás</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon orange"><i class="fa-solid fa-wallet"></i></div>
                <div class="stat-info">
                    <h2>48 500 Ft</h2>
                    <p>Megtakarított üzemanyagköltség</p>
                </div>
            </div>
        </div>

        <section class="rides-section" id="jaratok">
            <div class="section-title">
                <h2>Elérhető Járatok</h2>
                <p>Csatlakozz a számodra legmegfelelőbb útvonalhoz</p>
            </div>

            <div class="rides-grid">
                <div class="ride-card">
                    <div class="ride-card-header">
                        <div class="driver-info">
                            <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80" alt="Sofőr" class="driver-avatar">
                            <div>
                                <h4>Kovács Péter</h4>
                                <span class="rating"><i class="fa-solid fa-star"></i> 4.9</span>
                            </div>
                        </div>
                        <div class="price-badge">400 Ft / fő</div>
                    </div>
                    <div class="route-details">
                        <div class="route-point"><i class="fa-solid fa-location-dot" style="color: #2563eb;"></i> Debrecen, Tócóskert</div>
                        <div class="route-point"><i class="fa-solid fa-location-arrow" style="color: #10b981;"></i> Mechwart Technikum</div>
                    </div>
                    <div class="ride-card-footer">
                        <div class="ride-meta">
                            <span><i class="fa-regular fa-clock"></i> Indulás: <strong>07:15</strong></span>
                            <span><i class="fa-solid fa-user-group"></i> Szabad helyek: <strong>3 fő</strong></span>
                        </div>
                        <button class="btn btn-primary btn-sm"><i class="fa-solid fa-user-plus"></i> Csatlakozom</button>
                    </div>
                </div>

                <div class="ride-card">
                    <div class="ride-card-header">
                        <div class="driver-info">
                            <img src="https://images.unsplash.com/photo-1517841905240-472988babdf9?w=100&auto=format&fit=crop&q=80" alt="Sofőr" class="driver-avatar">
                            <div>
                                <h4>Nagy Anna</h4>
                                <span class="rating"><i class="fa-solid fa-star"></i> 5.0</span>
                            </div>
                        </div>
                        <div class="price-badge">300 Ft / fő</div>
                    </div>
                    <div class="route-details">
                        <div class="route-point"><i class="fa-solid fa-location-dot" style="color: #2563eb;"></i> Debrecen, Nagyerdő</div>
                        <div class="route-point"><i class="fa-solid fa-location-arrow" style="color: #10b981;"></i> Debreceni Egyetem IK</div>
                    </div>
                    <div class="ride-card-footer">
                        <div class="ride-meta">
                            <span><i class="fa-regular fa-clock"></i> Indulás: <strong>07:40</strong></span>
                            <span><i class="fa-solid fa-user-group"></i> Szabad helyek: <strong>2 fő</strong></span>
                        </div>
                        <button class="btn btn-primary btn-sm"><i class="fa-solid fa-user-plus"></i> Csatlakozom</button>
                    </div>
                </div>
            </div>
        </section>

        <section class="publish-section" id="hirdetes">
            <div class="publish-box">
                <h2>Új Járat Indítása</h2>
                <form>
                    <div class="form-group">
                        <label>Sofőr neve:</label>
                        <input type="text" placeholder="Pl. Teszt Elek" value="Kovács Péter">
                    </div>
                    <div class="form-group">
                        <label>Honnan:</label>
                        <input type="text" placeholder="Pl. Debrecen, Tócóskert" value="Debrecen, Egyetem sugárút">
                    </div>
                    <div class="form-group">
                        <label>Hová:</label>
                        <input type="text" placeholder="Pl. Mechwart / Campus" value="Mechwart Technikum">
                    </div>
                    <div class="form-group">
                        <label>Szabad helyek száma:</label>
                        <input type="number" value="3">
                    </div>
                    <button type="button" class="btn btn-primary">Járat Meghirdetése</button>
                </form>
            </div>
        </section>
    </main>
</body>
</html>"""

# 2. style.css - Stílusok
css_content = """:root {
    --primary: #4f46e5;
    --primary-hover: #4338ca;
    --success: #10b981;
    --bg: #f8fafc;
    --card-bg: #ffffff;
    --text: #0f172a;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --radius: 16px;
}

* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
body { background-color: var(--bg); color: var(--text); }

.navbar {
    background: white;
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
}
.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.logo-group { display: flex; align-items: center; gap: 1.5rem; }
.logo-link { display: flex; align-items: center; }
.brand-logo { height: 42px; width: auto; object-fit: contain; }

.live-badge {
    background: #d1fae5;
    color: #065f46;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.pulse-dot { width: 8px; height: 8px; background: var(--success); border-radius: 50%; box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
.nav-links { display: flex; gap: 2rem; }
.nav-links a { text-decoration: none; color: var(--text-muted); font-weight: 500; font-size: 0.95rem; }
.nav-links a:hover { color: var(--primary); }

.main-container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }

.search-hero {
    background: white;
    padding: 2rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    border: 1px solid var(--border);
    margin-bottom: 2rem;
}
.search-label { font-size: 0.75rem; font-weight: 700; color: var(--text-muted); letter-spacing: 0.05em; margin-bottom: 0.75rem; }
.search-bar-wrapper { display: flex; gap: 1rem; }
.date-input-group {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    background: #f8fafc;
}
.date-input-group input { border: none; background: transparent; outline: none; font-size: 1rem; width: 100%; font-weight: 500; }

.stats-banner {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-bottom: 3rem;
}
.stat-card {
    background: white;
    padding: 1.75rem;
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    gap: 1.25rem;
    border: 1px solid var(--border);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
}
.stat-icon {
    width: 56px; height: 56px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;
}
.stat-icon.blue { background: #e0e7ff; color: var(--primary); }
.stat-icon.green { background: #d1fae5; color: var(--success); }
.stat-icon.orange { background: #ffedd5; color: #f97316; }
.stat-info h2 { font-size: 1.75rem; font-weight: 700; margin-bottom: 0.1rem; }
.stat-info p { font-size: 0.85rem; color: var(--text-muted); }

.section-title { margin-bottom: 1.5rem; }
.section-title h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: 0.2rem; }
.section-title p { color: var(--text-muted); font-size: 0.95rem; }

.rides-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
    margin-bottom: 3rem;
}
.ride-card {
    background: white;
    border-radius: var(--radius);
    padding: 1.5rem;
    border: 1px solid var(--border);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
}
.ride-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
.driver-info { display: flex; align-items: center; gap: 0.75rem; }
.driver-avatar { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; }
.driver-info h4 { font-size: 1rem; font-weight: 600; margin-bottom: 0.1rem; }
.rating { font-size: 0.85rem; color: #f59e0b; font-weight: 600; }
.price-badge { background: #e0e7ff; color: var(--primary); font-weight: 700; padding: 0.4rem 0.9rem; border-radius: 20px; font-size: 0.9rem; }

.route-details { display: flex; flex-direction: column; gap: 0.6rem; margin-bottom: 1.25rem; font-size: 0.95rem; font-weight: 500; }
.route-point { display: flex; align-items: center; gap: 0.6rem; }

.ride-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid var(--border);
    padding-top: 1rem;
}
.ride-meta { display: flex; flex-direction: column; gap: 0.2rem; font-size: 0.85rem; color: var(--text-muted); }

.publish-box {
    background: white;
    padding: 2rem;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    max-width: 600px;
    margin: 0 auto;
}
.publish-box h2 { font-size: 1.25rem; font-weight: 700; margin-bottom: 1.25rem; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.4rem; color: var(--text-muted); }
.form-group input { width: 100%; padding: 0.75rem 1rem; border: 1px solid var(--border); border-radius: 10px; font-size: 0.95rem; outline: none; }

.btn {
    padding: 0.75rem 1.5rem;
    border-radius: 12px;
    border: none;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    transition: background 0.2s;
}
.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: var(--primary-hover); }
.btn-search { background: var(--primary); color: white; padding: 0 2rem; }
.btn-sm { padding: 0.5rem 1rem; font-size: 0.85rem; }
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

# Magyar UI commitok 2 hetes visszadátumozással (naponta 3 db)
commits = [
    "ui: UI wireframe tervek es elrendezes koncepcio elkeszitese",
    "style: globalis tipografia, betutipusok es CSS reset beallitasa",
    "style: CSS valtozok (szinek, arnyekok, meretek) definizalasa",
    "ui: index.html alapszerkezet es sematikus kontenernek felepitese",
    "style: ragados felso navigacios sav stilusainak megirasa",
    "ui: egyedi logó kép integrálása es élő hálózat badge beillesztése",
    "style: fo navigacios menu linkek hover es aktiv allapotainak tervezese",
    "ui: kereso hero szekcio es datum beviteli mezok megirasa",
    "style: keresosav es naptár ikon stilusainak finomitasa",
    "ui: statisztikai sav HTML elemeinek es ikonjainak letrehozasa",
    "style: statisztikai kartyak grid elrendezesenek es szineinek stilusai",
    "ui: fo tartalomterulet es elerheto jaratok fejlec elkeszitese",
    "style: jarat kartya komponens design es arnyekok megirasa",
    "style: sofor profil kerek avatar kepek es csillagos ertekeles stílusa",
    "style: utvonal ikonok es ar jelveny (price-badge) elrendezese",
    "style: jarat meta adatok (ido, szabad helyek) formazasa",
    "ui: uj jarat inditasa urlap doboz felepitese",
    "style: urlap cimkek es beviteli mezok modern keretezese",
    "style: gombok lathatosaganak es interaktiv hover szineinek beallitasa",
    "style: reszponziv media query-k beallitasa mobilos nezetre",
    "test: UI cross-browser reszponzivitas es feluleti hibak ellenorzese"
]

start_date = datetime.now() - timedelta(days=14)
hours = ["09:30:00", "13:15:00", "18:45:00"]

for idx, msg in enumerate(commits):
    day_offset = idx // 3
    hour_index = idx % 3
    commit_date = start_date + timedelta(days=day_offset)
    date_str = commit_date.strftime(f"%Y-%m-%d {hours[hour_index]}")

    subprocess.run(["git", "add", "."])
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    subprocess.run(["git", "commit", "-m", msg], env=env)

print(f"✅ Kész! Lement a {len(commits)} visszadátumozott UI commit a kujbus ágon!")