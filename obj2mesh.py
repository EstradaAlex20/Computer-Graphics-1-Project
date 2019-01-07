import os
import array
import sys

def convert(fname):
    fnorms = []
    fpos = []
    ftex = []
    ffaces = {}
    materials = {}
    with open(fname) as fp:
        for line in fp:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith("#"):
                continue
            lst = line.split()
            if lst[0] == "v":
                fpos.append([float(q) for q in lst[1:]])
            elif lst[0] == "vt":
                ftex.append([float(q) for q in lst[1:]])

                #added this myself no clue if its right
            elif lst[0] == "vn":
                fnorms.append([float(q) for q in lst[1:]])


            elif lst[0]=="usemtl":
                currmtl = lst[1]
            elif lst[0] == "f":
                if len(lst) != 4:
                    raise RuntimeError("Non-Triangles!")
                for vspec in lst[1:]:
                    tmp = vspec.split('/')
                    vi = int(tmp[0]) - 1
                    if len(tmp) != 3 or len(tmp[1])==0:
                        raise RuntimeError("Bad obj")
                    ti = int(tmp[1])-1
                    ni = int(tmp[2])-1
                    if currmtl not in ffaces:
                        ffaces[currmtl] = []
                    ffaces[currmtl].append((vi,ti,ni))
            elif lst[0] == "mtllib":
                ParseMtl(lst[1], os.path.dirname(fname), materials)
    vmap = {}
    numv = 0
    idata = []
    pdata=[]
    tdata = []
    ndata = []
    for mtl in ffaces:
        materials[mtl].first = len(idata)
        for vi,ti,ni in ffaces[mtl]:
            if (vi, ti, ni) not in vmap:
                vmap[(vi,ti,ni)] = numv
                numv += 1
                pdata += fpos[vi]
                tdata += ftex[ti]
                ndata += fnorms[ni]
            idata.append(vmap[(vi,ti,ni)])
            materials[mtl].count+=1
    with open(fname + ".mesh", "wb") as fp:
        fp.write(b"mesh 0\n")
        fp.write(b"num_materials %d\n" % len(ffaces.keys()))
        for mtlname in ffaces:
            M = materials[mtlname]
            fp.write(b"material %s\n" % mtlname.encode())
            fp.write(b"kd %s\n" % M.kd.encode())
            fp.write(b"ks %s\n" % M.ks.encode())
            fp.write(b"ns %s\n" % M.ns.encode())
            if M.map_kd:
                fp.write(b"map_kd %s\n" % M.map_kd.encode())
            fp.write(b"first and count %d %d\n" % (M.first, M.count))
        writeBlob(fp, "f", pdata, "position")
        writeBlob(fp, "f", tdata, "texcoord")
        writeBlob(fp, "f", ndata, "normal")
        writeBlob(fp, "I", idata, "Indicies")
        fp.write(b"end\n")



def writeBlob(fp, fmt, data, name):
    A = array.array(fmt, data)
    B = A.tobytes()
    fp.write(b"%s %d\n" % (name.encode(), len(B)))
    fp.write(B)
    fp.write(b"\n")

def ParseMtl(mtlFile, pfx, material):
    with open(os.path.join(pfx, mtlFile)) as fp:
        for line in fp:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith("#"):
                continue
            lst = line.split(" ", 1)
            if lst[0] == "newmtl":
                currmtl = lst[1]
                material[currmtl] = Material()
            elif lst[0] == "Kd":
                material[currmtl].kd = lst[1]
            elif lst[0] == "map_Kd":
                print(lst[0], lst)
                material[currmtl].map_kd = lst[1]
            elif lst[0] == "Ks":
                material[currmtl].ks = lst[1]
            elif lst[0] == "Ns":
                material[currmtl].ns = lst[1]


class Material:
    def __init__(self):
        self.kd = None
        self.map_kd = None
        self.first = None
        self.count = 0
        self.tex = None
        self.ks = None
        self.ns = None

if __name__ == "__main__":
	convert("assets/asteroid.obj")