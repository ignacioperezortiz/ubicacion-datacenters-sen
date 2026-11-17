"""Reemplaza los marcadores {{EQn}} que deja build.js por ecuaciones nativas y editables de PowerPoint.

Uso: python ecuaciones.py deck.pptx deck.pptx.eqs.json
Cada marcador es un run propio (a:r); se sustituye en su lugar por OMML (a14:m) generado con omml.py
(LaTeX -> MathML -> MML2OMML.XSL de Office). Funciona en cuadros de texto y en celdas de tablas.
"""
import json
import re
import sys
from pathlib import Path

from lxml import etree
from pptx import Presentation

sys.path.insert(0, str(Path(__file__).parent))
import omml  # noqa: E402

A = omml.A
MARK = re.compile(r"\{\{EQ(\d+)\}\}")


def main(pptx_path, eqs_path):
    eqs = json.loads(Path(eqs_path).read_text(encoding="utf-8"))
    prs = Presentation(pptx_path)
    done = 0
    for slide in prs.slides:
        for r in list(slide._element.iter(f"{{{A}}}r")):
            t = r.find(f"{{{A}}}t")
            m = MARK.fullmatch(t.text or "") if t is not None else None
            if not m:
                continue
            e = eqs[m.group(1)]
            math_el = omml._styled(e["latex"], e["size"], e["color"])
            p = r.getparent()
            alone = not any((n.text or "").strip() for x in p.iter(f"{{{A}}}r") if x is not r for n in x.iter(f"{{{A}}}t"))
            if alone:
                # una ecuación sola en su párrafo PowerPoint la trata como de display y la centra:
                # se envuelve en oMathPara con la alineación del párrafo
                ppr = p.find(f"{{{A}}}pPr")
                algn = ppr.get("algn") if ppr is not None else None
                para = etree.Element(f"{{{omml.M}}}oMathPara")
                etree.SubElement(etree.SubElement(para, f"{{{omml.M}}}oMathParaPr"), f"{{{omml.M}}}jc",
                                 {f"{{{omml.M}}}val": {"ctr": "centerGroup", "r": "right"}.get(algn, "left")})
                para.append(math_el)
                math_el = para
            ac = omml._wrap(math_el, e["latex"])
            r.addprevious(ac)
            r.getparent().remove(r)
            done += 1
    left = [n for s in prs.slides for n in s._element.iter(f"{{{A}}}t") if n.text and MARK.search(n.text)]
    if done != len(eqs) or left:
        raise SystemExit(f"ecuaciones: {done} reemplazadas de {len(eqs)}; marcadores sin reemplazar: {len(left)}")
    prs.save(pptx_path)
    print(f"ecuaciones: {done} reemplazadas")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
