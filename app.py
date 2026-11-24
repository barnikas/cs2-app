"""Nyilvános bemutató oldal (Streamlit) – CS2-közvetítések képi elemzése (2026-11-24).

Csak a kész bemutató videót és a leírást tartalmazza: a projekt kódja, modelljei és adatai NEM kerülnek ide (a fő repó
privát). A videó: scripts/showcase_video.py (a fő repóban) -> media/bemutato.mp4.

Helyi futtatás:
    pip install -r requirements.txt
    streamlit run app.py
Közzététel: README.md (Streamlit Community Cloud vagy Hugging Face Spaces).
"""

from pathlib import Path

import streamlit as st

HERE = Path(__file__).resolve().parent
VIDEO = HERE / "media" / "bemutato.mp4"
VIDEO_URL = ""                  # ha a videó nem a repóban van (pl. GitHub release / YouTube): az URL-je

st.set_page_config(page_title="CS2-közvetítések képi elemzése", page_icon="🎯", layout="wide")

st.title("Counter-Strike 2 közvetítések elemzése – csak a képből")
st.markdown(
    "Szakdolgozati projekt (2026). A rendszer **kizárólag a közvetítés képét** használja: "
    "demófájl, játék-API vagy szerveroldali adat nélkül olvassa ki a HUD-ot és a minimapot, "
    "ismeri fel a játékosokat, és keresi meg a részben takart játékos melletti fal élét."
)

# ---------------------------------------------------------------- videó
if VIDEO.exists():
    st.video(str(VIDEO))
elif VIDEO_URL:
    st.video(VIDEO_URL)
else:
    st.warning("A bemutató videó hiányzik (media/bemutato.mp4).")
st.caption(
    "IEM Cologne Major 2026, MOUZ–FUT, Ancient – ezt a meccset a modellek tanítása nem látta. "
    "Minden, ami a videón megjelenik, képkockánként, csak a képből számolódik. "
    "A közvetítés képe © ESL FACEIT Group; kutatási bemutató céljára, rövid részletként."
)

# ---------------------------------------------------------------- a négy modul
st.header("Mit látsz a videón?")
c1, c2 = st.columns(2)
with c1:
    st.subheader("1. Játékosdetektor")
    st.markdown(
        "- **Vastag keret:** a játékos *látható* része (kék = CT, narancs = T).\n"
        "- **Szaggatott keret:** a teljes alak (*outline*), a falon át látszó kontúrral együtt.\n"
        "- Négyosztályos YOLO-modell (`ct`, `t`, `ct_outline`, `t_outline`), 1280 px-es bemenet."
    )
    st.markdown(
        "**Mérés** (IEM Rio 2026, Gentle Mates–G2 – a tanításban nem szerepelt meccs, 852 kézzel ellenőrzött kép): "
        "látható rész pontosság **89,3%**, felidézés **84,7%**; teljes alak 94,0% / 96,9%. "
        "Gyenge pont: a részben takart (felidézés 63,6%) és a kicsi, 60 px-nél alacsonyabb alakok (36,8%)."
    )
    st.subheader("3. HUD-olvasó")
    st.markdown(
        "A jobb oldali táblázat: állás, a 10 játékoskártya (név, élet, páncél / sisak, pénz, kill / halál), "
        "a figyelt játékos (►), és hogy **élő-e** az adat. Visszajátszás (replay) és timeout alatt az adat "
        "*nem élő* – így is jelöljük."
    )
    st.markdown(
        "**Mérés** (IEM, a demóból kinyert igazsághoz): élet 98,7%, kill 98,9%, halál 96,1%, pénz 90,3%, "
        "állás 98,4%, páncél 99,3%, sisak 99,7%, él-e + oldal 97,9%, figyelt játékos 94,7%."
    )
with c2:
    st.subheader("2. Minimap-olvasó")
    st.markdown(
        "A nagyított minimapon a felismert jelek: kör = játékos (kék CT, narancs T, zöld a figyelt játékos), "
        "vonal = nézési irány, szám = a játékoskártya sorszáma (ki kicsoda)."
    )
    st.markdown(
        "**Mérés** (nem látott pályán, ESL és EWC közvetítésen): felidézés **98,0%**, pontosság **99,5%**, "
        "helyzethiba 0,37 px, irányhiba medián 2,3°; a jelben lévő szám 96,9%."
    )
    st.subheader("4. Takaró él")
    st.markdown(
        "Ha egy játékos csak részben látszik (a teljes alak oldalt túlnyúlik a láthatón), a takaró fal élét "
        "egy erre tanított élkereső háló (PiDiNet) keresi meg a levágott oldalon – **lila vonal**. "
        "Ebből mérhető, hogy a lövő mennyire tartotta előre a célkeresztet a fal széléhez képest, "
        "és mekkorát lépett ki a támadó."
    )
    st.markdown(
        "**Mérés:** a részben látszó képkockákon a kézzel jelölt élhez képest 10 px-en belül **90%** "
        "(medián 0,9 px; kis minta, 86 képkocka). A videón képkockánként, követés nélkül fut; "
        "a teljes, időben követett lánc a kézi éles képkockák ~45–55%-án ad helyes élt."
    )

# ---------------------------------------------------------------- támogatott HUD-ok
st.header("Milyen közvetítéseken működik?")
st.markdown(
    "A HUD minden tornán más (elhelyezés, betűtípus, színek), ezért a kiolvasó tornánként készül. "
    "A **játékosdetektor és a takaró él** a játék képén dolgozik, így HUD-tól függetlenül működik."
)
st.markdown(
    """
| Torna / közvetítés | HUD-olvasó | Minimap-olvasó | Megjegyzés |
|---|:---:|:---:|---|
| **IEM** (ESL FACEIT Group) | ✅ | ✅ | fő profil, kill feed is; a videó ilyen |
| **ESL Pro League** | ✅ | ✅ | fő profil, kill feed is |
| **BLAST** | ✅ | ❌ | a minimap itt arcképes, nagyító – folyamatban |
| Esports World Cup | ❌ | 🟡 | a minimap a tanításban szerepel, külön nem mérve |
| PGL, StarLadder, Fissure | ❌ | ❌ | nem támogatott |
"""
)

# ---------------------------------------------------------------- korlátok, technika
st.header("Korlátok és technika")
st.markdown(
    "- **Csak kép:** nincs demófájl, nincs játék-API. A demót kizárólag a mérésekhez (igazságként) használtuk.\n"
    "- **Becsületes mérés:** a mérőmeccsek a tanításban nem szerepelnek (meccsenkénti felosztás).\n"
    "- **Sebesség:** a teljes lánc egy RTX 5080-on ~5 kép/s (offline elemzés); a detektor + minimap + követés "
    "képkockánként ~33 ms, a valós idő határán. GPU-memória: ~3,2 GB.\n"
    "- **Modellek:** YOLO26m (detektor), YOLO26n-pose (minimap), PiDiNet (élkereső), Depth Anything V2 "
    "(távolság), saját számjegy-felismerő a HUD-hoz.\n"
    "- A forráskód nem nyilvános (szakdolgozat); érdeklődés esetén a szerzőnél."
)
