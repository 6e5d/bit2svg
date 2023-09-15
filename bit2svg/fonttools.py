from fontTools import ttLib
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from pathlib import Path

from . import bit2routes

def un(ch):
	return f"gid{ch}"

def bit2ttf(txt_file, dpath):
	routes_table, w, h = bit2routes(txt_file)
	em = 1024 * w // h
	k = em // w
	ww = int(em * 0.2)
	ascent = 1024
	descent = 0
	def xk(x):
		return (x[0] * k, (h - x[1]) * k)

	fb = FontBuilder(em, isTTF = True)
	fb.setupGlyphOrder([])
	unicodes = list(routes_table.keys())
	cmap = {x: un(x) for x in unicodes}
	fb.setupCharacterMap(cmap)
	fb.setupGlyphOrder([".notdef", ".null"] + [un(x) for x in unicodes])
	family = Path(dpath).stem
	ns = {
		"familyName": family,
		"styleName": "Regular",
	}

	glyphs = dict()
	for unicode, routes in routes_table.items():
		pen = TTGlyphPen(None)
		for route in routes:
			pen.moveTo(xk(route[0]))
			for v in route[1:]:
				pen.lineTo(xk(v))
			pen.closePath()
		glyphs[un(unicode)] = pen.glyph()
	glyphs[".null"] = glyphs["gid32"]
	glyphs[".notdef"] = glyphs["gid63"]
	fb.setupGlyf(glyphs)
	table = fb.font["glyf"]
	metrics = {x: (table[x].xMax + ww, table[x].xMin) for x in glyphs}
	metrics["gid32"] = (em, 0)
	fb.setupHorizontalMetrics(metrics)
	fb.setupHorizontalHeader(ascent = ascent, descent = descent)
	fb.setupNameTable(ns)
	fb.setupPost()
	fb.save(dpath)
