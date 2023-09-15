from importer import importer
importer("../../bitw/bitw", __file__)
from bitw import read_txt

def xor(m, x):
	(f, t) = x
	if t in m and f in m[t]:
		m[t].remove(f) # 2 directions countered
		if not m[t]:
			m.pop(t)
	else:
		if f not in m:
			m[f] = [t]
		else:
			assert t not in m[f]
			m[f].append(t)

def tsub(f, t):
	return (
		f[0] - t[0],
		f[1] - t[1],
	)

def pt(t):
	return f"{t[0]},{t[1]}"

def traceroute(edgemap, pos):
	visited = [pos]
	while True:
		targets = edgemap[pos]
		if len(targets) == 1:
			prev = pos
			edgemap.pop(pos)
			pos = targets[0]
		elif len(targets) == 2:
			if prev == None:
				choose_idx = 0
			else:
				# turn left
				for idx, pos2 in enumerate(targets):
					dp1 = tsub(pos, prev)
					dp2 = tsub(pos2, pos)
					cross = dp1[0] * dp2[1] - dp1[1] * dp2[0]
					if cross == -1:
						choose_idx = idx
						break
				else:
					raise Exception("cannot turn left")
			prev = pos
			pos = targets[choose_idx]
			del targets[choose_idx]
		else:
			print(targets)
			raise Exception("bad edgemap")
		if pos == visited[0]:
			return visited
			print("draw", visited)
		visited.append(pos)

def proc_glyph(array):
	routes = []
	edgemap = dict()
	for y, line in enumerate(array):
		for x, ch in enumerate(line):
			if ch == 0:
				continue
			# ccw winding
			xor(edgemap, ((x + 1, y), (x, y)))
			xor(edgemap, ((x, y), (x, y + 1)))
			xor(edgemap, ((x + 1, y + 1), (x + 1, y)))
			xor(edgemap, ((x, y + 1), (x + 1, y + 1)))

	while edgemap:
		pos = next(iter(edgemap))
		prev = None
		routes.append(traceroute(edgemap, pos))
	return routes

def bit2routes(txt_file):
	data, w, h = read_txt(txt_file)
	result = dict()
	for unicode, array in data.items():
		h, w = array.shape
		routes = proc_glyph(array)
		result[unicode] = routes
	return result, w, h
