import struct, sys

LUMP_ENTITIES = 0
LUMP_PLANES = 1
LUMP_TEXTURES = 2
LUMP_VERTICES = 3
LUMP_VISIBILITY = 4
LUMP_NODES = 5
LUMP_TEXINFO = 6
LUMP_FACES = 7
LUMP_LIGHTING = 8
LUMP_CLIPNODES = 9
LUMP_LEAVES = 10
LUMP_MARKSURFACES = 11
LUMP_EDGES = 12
LUMP_SURFEDGES = 13
LUMP_MODELS = 14
HEADER_LUMPS = 15

with open("msvc/rsc.bsp", "rb") as f:
	header = f.read(4)
	version = struct.unpack('i', header)[0]
	
	if version != 30:
		print("unexpected BSP version %s" % version)
		sys.exit()
	
	lump_names = ['ENTITIES', 'PLANES', 'TEXTURES', 'VERTICES', 'VISIBILITY', 'NODES', 'TEXINFO', 'FACES', 'LIGHTING',
		'CLIPNODES', 'LEAVES', 'MARKSURFACES', 'EDGES', 'SURFEDGES', 'MODELS']
	lump_info = []
	for name in lump_names:
		offset = struct.unpack('i', f.read(4))[0]
		length = struct.unpack('i', f.read(4))[0]
		
		lump_info.append({
			'offset': offset,
			'length': length
		})
		print("LUMP_%s offset=%i, size=%i" % (name, offset, length))
	
	
	print("TOTAL NODES: %s " % int(lump_info[LUMP_NODES]['length'] / 24))
	print("TOTAL CLIPNODES: %s " % int(lump_info[LUMP_CLIPNODES]['length'] / 8))
	
	model_lump = lump_info[LUMP_MODELS]
	num_models = int(model_lump['length'] / 64)
	
	for modelIdx in range(0, num_models):
		f.seek(model_lump['offset'] + modelIdx*64 + 4*(3 + 3 + 3))
		
		head_nodes = [0, 0, 0, 0]
		for idx in range(0, 4):
			bytes = f.read(4)
			headNode = struct.unpack('i', bytes)[0]
			print("Model %s node %s = %s (offset: %s, bytes: %s)" % (modelIdx, idx, headNode, f.tell()-4, bytes))
	