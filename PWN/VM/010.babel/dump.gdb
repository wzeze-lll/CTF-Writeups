set pagination off
set confirm off
starti
python
import gdb, struct
maps = gdb.execute("info proc mappings", to_string=True)
base = None
for line in maps.splitlines():
    if "babel_239" in line and "r-xp" not in line:
        parts = line.split()
        try:
            a = int(parts[0], 16)
        except Exception:
            continue
        if a & 0xfff == 0:
            base = a
            break
print("BASE", hex(base))
inf = gdb.selected_inferior()
gdb.execute("break *%d" % (base + 0xdb80))
gdb.execute("continue")
mem = inf.read_memory(base + 0x75f60, 256).tobytes()
print("MAP_HEX", mem.hex())
tb = inf.read_memory(base + 0x76060, 512).tobytes()
ptrs = struct.unpack("<64Q", tb)
print("TABLE", " ".join(hex(p - base) for p in ptrs))
# also dump the 16 resources at 0x75e40 and core regs 0x75ec0
res = inf.read_memory(base + 0x75e40, 0x100).tobytes()
print("RES", res.hex())
core = struct.unpack("<16Q", inf.read_memory(base + 0x75ec0, 0x80).tobytes())
print("CORE", " ".join(hex(x) for x in core))
print("HEAPBASE", hex(struct.unpack("<Q", inf.read_memory(base+0x76260, 8).tobytes())[0]))
print("HEAPTOP", struct.unpack("<I", inf.read_memory(base+0x76268, 4).tobytes())[0])
print("REGION2", hex(struct.unpack("<Q", inf.read_memory(base+0x76270, 8).tobytes())[0]))
print("SP", struct.unpack("<Q", inf.read_memory(base+0x97288, 8).tobytes())[0])
end
quit
