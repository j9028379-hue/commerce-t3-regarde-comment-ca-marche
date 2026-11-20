"""Témoin technique : quatre mires, son uniquement en S2, aucune donnée de client."""

from pathlib import Path as P
import subprocess as sp, json, shutil, sys

J = lambda p: json.loads(P(p).read_text())
cmd = lambda *a: sp.run(a, check=True)
if sys.argv[1] == "preparer":
    P("work").mkdir(exist_ok=True)
    for i, (d, c) in enumerate(
        zip([6, 8, 7, 9], ["navy", "green", "maroon", "teal"]), 1
    ):
        args = [
            "ffmpeg",
            "-v",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={c}:s=360x640:r=30:d={d}",
        ]
        args += (
            ["-f", "lavfi", "-i", f"sine=frequency=350:duration={d}", "-c:a", "aac"]
            if i == 2
            else ["-an"]
        )
        cmd(*(args + ["-c:v", "libx264", "-pix_fmt", "yuv420p", f"work/S{i}.mp4"]))
else:
    dest = P("verification")
    src = dest / "entree"
    src.mkdir(parents=True)
    shutil.copy("livraison/job.json", src / "job.json")
    j = J(src / "job.json")
    assert j["reponses"] == J("qc/temoin.json") and j["ecrans"] == list(range(1, 13))
    for i in range(1, 5):
        shutil.copy(f"work/S{i}.mp4", src)
    sys.path.insert(0, "render")
    from marchand import run

    out = dest / "sorties"
    db = dest / "test.sqlite"
    r = run(src, out, db)
    assert r["status"] == "COMPLETED", r
    assert r["music_id"] == 1
    d = out / r["run_id"]
    ctrl = J(d / "controle.json")
    assert not ctrl["prix_affiche"] and ctrl["frames"] == 900
    assert J(d / "audio.json")["scenes_audio"] == ["S2"]
    titles = J(d / "titres.json")
    assert (
        titles["prix"] == ""
        and j["reponses"]["quartier"] in titles["boutique"]
        and titles["contact"].endswith(j["reponses"]["whatsapp"])
    )
    assert all(
        titles[k]
        == ("WhatsApp\n" if k == "contact" else "")
        + "\n".join(j["reponses"][name] for name in keys)
        for k, keys in J("montage/partition.json")["texte"]["liaison_champs"].items()
    )
    assert run(src, out, db) == r
    with (src / "S1.mp4").open("ab") as f:
        f.write(b"x")
    assert run(src, out, db)["status"] == "FAILED"
    print(
        "PASS job navigateur alternatif, prix absent, audio S2 uniquement, MP4 crédité, idempotence et rejet prise altérée"
    )
