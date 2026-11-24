# CS2-közvetítések képi elemzése – bemutató oldal

Streamlit-oldal egy bemutató videóval, amelyen a játékosdetektor, a minimap-olvasó, a HUD-olvasó és a takaró él
működése látszik, mellette a leírás, a mért pontosság és a támogatott közvetítések listája.

Ez a mappa **önállóan kitehető**: nincs benne a projekt kódja, modellje vagy adata (a fő repó privát), csak az oldal
(`app.py`) és a kész videó (`media/bemutato.mp4`).

## A videó elkészítése (a fő repóban, GPU-s gépen)

```
python scripts/showcase_video.py                      # -> outputs/visualizations/showcase_<dátum>.mp4
copy outputs\visualizations\showcase_<dátum>.mp4 showcase\media\bemutato.mp4
```

A videó a fő repóban nem kerül gitbe (`*.mp4` a `.gitignore`-ban), a nyilvános repóba viszont igen. A GitHub
fájlonként legfeljebb 100 MB-ot enged: a videó maradjon jóval ez alatt (a mostani, 57 s-os videó 30,7 MB).

## Helyi futtatás

```
pip install -r requirements.txt
streamlit run app.py
```

## Közzététel: Streamlit Community Cloud (ingyenes)

1. Új, **nyilvános** GitHub-repó (pl. `cs2-kepi-elemzes-bemutato`), és ennek a mappának a tartalma a gyökerébe:
   `app.py`, `requirements.txt`, `.streamlit/config.toml`, `media/bemutato.mp4`, `README.md`.
2. <https://share.streamlit.io> → bejelentkezés GitHubbal → **Create app** → a repó, az ág (`main`) és a fájl
   (`app.py`) → **Deploy**. Az oldal címe `<név>.streamlit.app` lesz.
3. Frissítés: új push a repóba, és az oldal magától újraindul.

Az ingyenes alkalmazás néhány nap használatlanság után elalszik. Ilyenkor az első látogatónak egy „wake up” gombot
kell megnyomnia, és ~1 percet várnia. A védés előtt érdemes egyszer megnyitni.

## Alternatíva: Hugging Face Spaces

Új Space → SDK: *Streamlit* (vagy Docker + Streamlit) → ugyanezek a fájlok. A Space lehet nyilvános úgy, hogy a
fájljai is nyilvánosak. Akkor jó választás, ha később élő kipróbálás is kerül az oldalra (több RAM-ot ad).

## Jogok

A videó egy IEM-közvetítés rövid részletein készült (© ESL FACEIT Group), kutatási bemutató céljára, forrásmegjelöléssel.
