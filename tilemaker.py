FILENAME = "shaded-k6torus" 

M = 4
N = 5 

CORONA = 6

ROTATE = 30

SHADE_LIST = [("yellow", 0.5), ("red", 0.25), 
              ("green", 0.25), ("navy", 0.25)]

dX = 2000 
X_OFFSET = 1000
dY = 1732
Y_OFFSET = 866

X_MIDEDGE_1 = 250
X_MIDEDGE_2 = 1000
X_MIDEDGE_3 = 1750

Y_MIDEDGE_1 = 0
Y_MIDEDGE_2 = 433
Y_MIDEDGE_3 = 1299
Y_MIDEDGE_4 = 1732 

ORIGIN_X = (CORONA + 1) * dX
ORIGIN_Y = (CORONA) * dX
SVG_HT = (CORONA * 2 + 3) * dY

STROKEWIDTH = 100 
STROKE = "black"

CON_PT = [(1000, 0), (1750, 433), (1750, 1299), (1000, 1732), 
              (250, 1299), (250, 433)]
              
CON_VECT = [(0, -1), (0.866, -0.5), (0.866, 0.5), (0, 1), (-0.866, 0.5), (-0.866, -0.5)] 


             
VERTEX = [(1500 - 250, 0 + 433), (2000 - 250, 866), (1500 - 250, 1732 - 433), (500 + 250, 1732 - 433), 
              (0 + 250, 866), (500 + 250, 0 + 433)]
              
REAL_VERT = [(1500, 0), (2000, 866), (1500, 1732), (500, 1732), (0, 866), 
             (500, 0)] 
VERT_VECT = [(0.5, -0.866), (1, 0), (0.5, 0.866), (-0.5, 0.866), (-1, 0), (-0.5, -0.866)]

def trans_coord_str(x, y, dx, dy, scale = STROKEWIDTH): 
    return "{} {}".format(int(x + dx * 2.5 * scale), int(y + dy * 2.5 * scale))
    
def clip_path_catarc(i, normal): 
    p_str = "M"    
    if(normal > 0): 
        p_str += trans_coord_str(*CON_PT[(i + 1) % 6], *CON_VECT[(i + 2) % 6])
        p_str += " Q" 
        p_str += trans_coord_str(1000, 866, *CON_VECT[(i + 2) % 6]) 
        p_str += " "
        p_str += trans_coord_str(*CON_PT[(i + 3) % 6], *CON_VECT[(i + 2) % 6])
        p_str += " "
        for j in range(2): 
            p_str += "L"
            p_str += trans_coord_str(*REAL_VERT[(i + 2 - j) % 6], 0, 0)
            p_str += " "
    elif(normal < 0): 
        p_str += trans_coord_str(*CON_PT[(i + 1) % 6], *CON_VECT[(i + 5) % 6])
        p_str += " Q" 
        p_str += trans_coord_str(1000, 866, *CON_VECT[(i + 5) % 6]) 
        p_str += " "
        p_str += trans_coord_str(*CON_PT[(i + 3) % 6], *CON_VECT[(i + 5) % 6])
        p_str += " "
        for j in range(4): 
            p_str += "L"
            p_str += trans_coord_str(*REAL_VERT[(i + 3 + j) % 6], 0, 0)
            p_str += " "
    p_str += "Z"
    
    return p_str
    
        
def clip_path_straight(i, normal): 
    c_str = "M" 
    if(normal > 0): 
        c_str += trans_coord_str(*CON_PT[(i)], *VERT_VECT[(i + 1) % 6])
        c_str += " L" 
        c_str += trans_coord_str(*CON_PT[(i + 3) % 6], *VERT_VECT[(i + 1) % 6]) 
        for j in range(3):         
            c_str += " L"
            c_str += trans_coord_str(*REAL_VERT[(i + 2 - j) % 6], 0, 0) 
    if(normal < 0): 
        c_str += trans_coord_str(*CON_PT[(i)], *VERT_VECT[(i + 4) % 6])
        c_str += " L" 
        c_str += trans_coord_str(*CON_PT[(i + 3) % 6], *VERT_VECT[(i + 4) % 6]) 
        for j in range(3):         
            c_str += " L"
            c_str += trans_coord_str(*REAL_VERT[(i + 3 + j) % 6], 0, 0) 
    c_str += " Z" 
    return c_str 
    
def clip_path_triple(i, normal): 
    p_str = "M" 
    if(normal > 0): 
        p_str += trans_coord_str(*CON_PT[i], *VERT_VECT[(i + 1) % 6]) 
        p_str += " Q" 
        p_str += trans_coord_str(*VERTEX[(i - 2) % 6], *VERT_VECT[(i + 1) % 6])
        p_str += " "
        p_str += trans_coord_str(*CON_PT[(i + 3) % 6], *VERT_VECT[(i + 1) % 6])
        for j in range(3): 
            p_str += " L"
            p_str += trans_coord_str(*REAL_VERT[(i + 2 - j) % 6], 0, 0)
    if(normal < 0): 
        p_str += trans_coord_str(*CON_PT[i], *VERT_VECT[(i + 4) % 6]) 
        p_str += " Q" 
        p_str += trans_coord_str(*VERTEX[(i - 2) % 6], *VERT_VECT[(i + 4) % 6])
        p_str += " "
        p_str += trans_coord_str(*CON_PT[(i + 3) % 6], *VERT_VECT[(i + 4) % 6])
        for j in range(3): 
            p_str += " L"
            p_str += trans_coord_str(*REAL_VERT[(i + 3 + j) % 6], 0, 0)
    p_str += " Z"
    return p_str
        
        
def clip_dfn(paths, clip_id): 
    c_str = "\t<clipPath id=\"{}\" ".format(clip_id) 
    c_str += "clipPathUnits=\"userSpaceOnUse\" "
    c_str += "clip-rule=\"evenodd\" " 
    c_str += ">\n"
    for p in paths: 
        c_str += "\t\t<path d=\"{}\" />\n".format(p)
    c_str += "\t</clipPath>\n\n"
    return c_str 
    
def write_clip_dfns(file): 
    for c in range(len(CAT_ARC)): 
        file.write(clip_dfn([clip_path_catarc(c, 1), 
                             clip_path_catarc(c, -1)], 
                             "clipCatArc{}".format(c)))
    for c in range(len(STRAIGHT_ARC)): 
        file.write(clip_dfn([clip_path_straight(c, 1), 
                             clip_path_straight(c, -1)], 
                             "clipStraightArc{}".format(c)))
    for c in range(len(TRIPLE_ARC)): 
        file.write(clip_dfn([clip_path_triple(c, 1), 
                             clip_path_triple(c, -1)], 
                             "clipTripleArc{}".format(c)))
    file.write(clip_dfn([clip_path_catarc(0, 1), 
                         clip_path_catarc(0, -1), 
                         clip_path_catarc(3, 1), 
                            clip_path_catarc(3, -1)], 
                            "clipDoubleCatArc"))
    file.write(clip_dfn([clip_path_triple(0, 1), 
                         clip_path_triple(0, -1), 
                            clip_path_triple(4, 1), 
                            clip_path_triple(4, -1)], 
                            "ClipDoubleTripleArc"))


def coord_str(pt): 
    return "{} {}".format(CON_PT[pt][0], CON_PT[pt][1])
    
def vertex_str(pt): 
    return "{} {}".format(VERTEX[pt][0] , VERTEX[pt][1])

C_ARC = ["M" + coord_str((i + 1) % 6) + " Q1000 866, " +\
            coord_str((i + 2) % 6) for i in range(6)]
            

CAT_ARC = ["M" + coord_str((i + 1) % 6) + " Q1000 866, " +\
            coord_str((i + 3) % 6) for i in range(6)] 
            

STRAIGHT_ARC = ["M" + coord_str((i) % 6) + " L" +\
                coord_str((i + 3) % 6) for i in range(6)] 
                
TRIPLE_ARC = ["M" + coord_str(i) + " Q" + vertex_str((i - 2) % 6) +\
                ", " + coord_str((i + 3) % 6) for i in range(6)]

def mask_dfn_proto(arcs, mid): 
    m_str = "\t<mask id=\"{}Proto\" ".format(mid)
    m_str += "maskUnits=\"userSpaceOnUse\" " 
    m_str += "mask-type=\"alpha\" >\n" 
    m_str += "\t\t<rect x=\"0\" y=\"0\" "
    m_str += "height=\"{}\" width=\"{}\" ".format(dY, dX) 
    m_str += "fill=\"white\" fill-opacity=\"0.0\" "
    m_str += "/>\n"
    for a in arcs:
        m_str += "\t\t<path d=\"{}\" ".format(a) 
        m_str += "stroke=\"black\" stroke-opacity=\"1.0\" "
        m_str += "stroke-width=\"{}\" ".format(5 * STROKEWIDTH) 
        m_str += "/>\n" 
    m_str += "\t</mask>\n\n" 
    return m_str

           
def mask_dfn(arcs, mid):     
    m_str = "\t<mask id=\"{}\" maskUnits=\"userSpaceOnUse\" ".format(mid)
    m_str += "x=\"0\" y=\"0\" height=\"{}\" width=\"{}\" ".format(dY, dX) 
    m_str += "mask-type=\"luminance\" >\n"
    m_str += "\t\t<rect height=\"{}\" width=\"{}\" fill=\"#ffffff\" ".format(dY, dX)
    m_str += "fill-opacity=\"1.0\" "
    m_str += "/>\n"
    for a in arcs:
        m_str += "\t\t<path d=\"{}\" ".format(a) 
        m_str += "stroke=\"#000000\" "
        m_str += "stroke-opacity=\"1.0\" fill=\"none\" "
        m_str += "stroke-width=\"{}\" />\n" .format(3 * STROKEWIDTH)
    m_str += "\t\t</mask>\n\n"
    return m_str
    

        
def write_mask_dfns(file): 
    for c in range(len(C_ARC)): 
        file.write(mask_dfn([C_ARC[c]], "mCArc{}".format(c)))
    for c in range(len(CAT_ARC)): 
        file.write(mask_dfn([CAT_ARC[c]], "mCatArc{}".format(c)))
    for c in range(len(STRAIGHT_ARC)): 
        file.write(mask_dfn([STRAIGHT_ARC[c]], "mStraightArc{}".format(c)))
    for c in range(len(TRIPLE_ARC)): 
        file.write(mask_dfn([TRIPLE_ARC[c]], "mTripleArc{}".format(c)))
    file.write(mask_dfn([CAT_ARC[0], CAT_ARC[3]], "mDoubleCatArc")) 
    file.write(mask_dfn([TRIPLE_ARC[0], TRIPLE_ARC[4]], "mDoubleTripleArc"))

def make_tile(x, y, arcs, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g id=\"tileK{}T{}\" ".format(x, y)
    t_str += "transform=\"translate({}, {}) ".format(*cor_axis_coords(x, y))
    t_str += "rotate({}, 1000, 866)\" >\n".format(phi * 60) 
    for a in arcs: 
        t_str += "\t<path d=\"" + a[0] + "\" "
        t_str += "stroke=\"{}\" ".format(stroke) 
        t_str += "stroke-width=\"{}\" ".format(stroke_width) 
        t_str += "fill=\"none\" "
        if(len(a) > 2): 
            t_str += "clip-path=\"url(#{})\" ".format(a[2])
            t_str += "stroke-linecap=\"round\" "
        if(a[1] is not None): 
            t_str += "mask=\"url(#{})\" ".format(a[1])
        t_str += "/>\n" 
    t_str += "</g>\n\n"
    return t_str 
 
def make_tile_stretched(x, y, arcs, phi = 6, stroke=STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g id=\"tileK{}T{}\" ".format(x, y)
    t_str += "transform=\"translate({}, {}) ".format(*stretched_coords(x, y))
    t_str += "rotate({}, 1000, 866)\" >\n".format(phi * 60) 
    for a in arcs: 
        t_str += "\t<path d=\"" + a[0] + "\" "
        t_str += "stroke=\"{}\" ".format(stroke) 
        t_str += "stroke-width=\"{}\" ".format(stroke_width) 
        t_str += "fill=\"none\" "
        if(len(a) > 2): 
            t_str += "clip-path=\"url(#{})\" ".format(a[2])
            t_str += "stroke-linecap=\"round\" "
        if(a[1] is not None): 
            t_str += "mask=\"url(#{})\" ".format(a[1])
        t_str += "/>\n" 
    t_str += "</g>\n\n"
    return t_str 
    
                
def T1(x, y, phi = 6, stroke=STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None]]
    t1_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
    return t1_str 
    
    
def T2(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[0], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
    return t_str

def T3(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[STRAIGHT_ARC[0], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
    return t_str

def T4(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [C_ARC[2], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
    return t_str

def T5(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [C_ARC[3], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
    return t_str
    
def T6(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [STRAIGHT_ARC[0], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
    return t_str

def T7(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [CAT_ARC[2], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
    return t_str

def T8(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[0], None], [CAT_ARC[3], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
    return t_str

def T9(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
#    arcs = [[CAT_ARC[1], None], [STRAIGHT_ARC[0], "mCatArc1"]]
    arcs = [[CAT_ARC[1], None], [STRAIGHT_ARC[0], None, "clipCatArc1"]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
    return t_str 

def T10(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):  
    arcs = [[STRAIGHT_ARC[1], None], [STRAIGHT_ARC[2], None, "clipStraightArc1"]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)
    return t_str 
    
def T11(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[STRAIGHT_ARC[2], None], [STRAIGHT_ARC[1], None, "clipStraightArc2"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
        
    return t_str 

def T12(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[1], None], [CAT_ARC[2], None, "clipCatArc1"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str 

def T13(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):   
    arcs = [[CAT_ARC[2], None], [CAT_ARC[1], None, "clipCatArc2"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str 



def T14(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [C_ARC[3], None], [STRAIGHT_ARC[0], None]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str

def T15(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [C_ARC[2], None], [C_ARC[4], None]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    

    return t_str

def T16(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[1], None], [CAT_ARC[2], None, "clipCatArc1"], [C_ARC[5], None]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str

def T17(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[2], None], [CAT_ARC[1], None, "clipCatArc2"], [C_ARC[5], None]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str 
    
def T18(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[0], None], 
            [CAT_ARC[3], None], 
            [STRAIGHT_ARC[5], None, "clipDoubleCatArc"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str

def T19(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    arcs = [[CAT_ARC[0], None], 
            [CAT_ARC[3], None, "clipStraightArc2"], 
            [STRAIGHT_ARC[2], None, "clipCatArc0"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str

def T20(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    arcs = [[TRIPLE_ARC[0], None, "clipTripleArc2"], 
            [TRIPLE_ARC[2], None, "clipTripleArc4"], 
            [TRIPLE_ARC[4], None, "clipTripleArc0"]] 
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str

def T21(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    arcs = [[TRIPLE_ARC[0], None, "clipTripleArc4"], 
            [TRIPLE_ARC[2], None, "clipTripleArc0"], 
            [TRIPLE_ARC[4], None, "clipTripleArc2"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str 
    
def T22(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    arcs = [[TRIPLE_ARC[0], None], 
            [TRIPLE_ARC[2], None, "clipDoubleTripleArc"], 
            [TRIPLE_ARC[4], None, "clipTripleArc0"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str 
    
def T23(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    arcs = [[TRIPLE_ARC[0], None, "clipTripleArc4"], 
            [TRIPLE_ARC[2], None, "clipDoubleTripleArc"], 
            [TRIPLE_ARC[4], None]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str

    
    
      

def draw_tile(file, x_pos = 0, y_pos = 0, stroke = "black", stroke_width = 30, 
              stroke_color = "black", scale = 0.10, fill = "none", 
              fill_opacity = 1.0): 
    file.write("<use xlink:href=\"#hextile\" ")
    file.write("stroke=\"{}\" ".format(stroke)) 
    file.write("stroke-width=\"{}\" ".format(int(stroke_width))) 
    file.write("stroke-color=\"{}\" ".format(stroke_color)) 
    file.write("fill=\"{}\" ".format(fill)) 
    file.write("fill-opacity=\"{:.2f}\" ".format(fill_opacity)) 
    file.write("transform =\"translate({}, {})\" ".format(x_pos, y_pos))
    file.write(" />\n")
    
def draw_tile_str(x_pos = 0, y_pos = 0, stroke = "black", stroke_width = 30, 
              stroke_color = "black", scale = 0.10, fill = "none", 
              fill_opacity = 1.0): 
    t_str = "<use xlink:href=\"#hextile\" "
    t_str += "stroke=\"{}\" ".format(stroke)
    t_str += "stroke-width=\"{}\" ".format(int(stroke_width))
    t_str += "stroke-color=\"{}\" ".format(stroke_color)
    t_str += "fill=\"{}\" ".format(fill)
    t_str += "fill-opacity=\"{:.2f}\" ".format(fill_opacity)
    t_str += "transform =\"translate({}, {})\" ".format(x_pos, y_pos)
    t_str += " />\n"
    return t_str
     
def p_tile(m, n, fill = "none", fill_opacity = 1.0): 
    t_str = "<use xlink:href=\"#hextile\" " 
    t_str += "transform=\"translate({}, {}) ".format(*par_coords(m, n))
    t_str += "rotate(30, 1000, 866)\" " 
    t_str += "fill=\"{}\" ".format(fill) 
    t_str += "fill-opacity=\"{:.2f}\" ".format(fill_opacity) 
    t_str += "/>\n" 
    return t_str
    
def cor_axis_coords(x, y, x_ht = dX, y_ht = dY, origin_x = ORIGIN_X, 
                    origin_y = ORIGIN_Y): 
    dx = origin_x 
    dy = origin_y
    dx += (x) * 1500
    dy += -(x * Y_OFFSET + y * dY)
    return dx, dy
    
def corona_coords(kappa, theta, x_ht = dX, y_ht = dY, 
                  origin_x = ORIGIN_X, origin_y = ORIGIN_Y): 
    dx = origin_x
    dy = origin_y
    if(kappa == 0): 
        return dx, dy
    y_off = int(y_ht / 2)
    x_off = int((3 * x_ht) / 4)
    sextant = theta // kappa 
    s = theta % kappa
    if(sextant == 0): 
        dy = origin_y - (y_ht * (kappa)) + (s * y_off) 
        dx = origin_x + (s * x_off)
    elif(sextant == 1): 
        dy = origin_y - (y_off * (kappa)) + (s * y_ht) 
        dx = origin_x + ((kappa) * x_off)
    elif(sextant == 2): 
        dy = origin_y + (y_off * (kappa)) + (s * y_off) 
        dx = origin_x + ((kappa - s) * x_off)
    elif(sextant == 3): 
        dy = origin_y + (y_ht * (kappa)) - (s * y_off) 
        dx = origin_x - (s * x_off)
    elif(sextant == 4): 
        dy = origin_y + (y_off * (kappa)) - (s * dY) 
        dx = origin_x - ((kappa) * x_off)
    elif(sextant == 5): 
        dy = origin_y - (y_off * (kappa)) - (s * y_off) 
        dx = origin_x - ((kappa - s) * x_off)
    return dx, dy
    
def par_coords(m, n, x_ht = dY, y_ht = dX): 
    dx = dY    
    dy = dX
    dx += (m - 1) * Y_OFFSET 
    dx += n * dY 
    dy += m * 1500 
    return dx, dy



def svg_header(corona = CORONA, m = None, n = None): 
    svgheader = "<?xml version=\"1.0\"?>\n" +\
            "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" " +\
            "width=\"1000\" height=\"1000\" "
    if((m is not None) and (n is  not None)):
        svgheader += "viewBox=\"0 0 {0} {1}\" ".format((n + 4) * dY, 
                                                        (2 * m + 2) * dY)
    else: 
       svgheader += "viewBox=\"0 0 {0} {1}\" ".format((2 * corona + 2) * dX, 
                                                        (2 * corona + 2) * dY)        
    if(ROTATE != 0): 
        svgheader += "transform=\"rotate({}, {}, {})\" ".format(ROTATE, 400, 400)
    svgheader += ">\n" +\
            "\n" +\
            "<defs>\n" +\
            "\t<polygon id=\"hextile\" stroke=\"black\" stroke-width=\"30\" " +\
            "points=\"500,0 1500,0 2000,866 1500,1732 500,1732 0,866\" />\n" +\
            "\n"
    return svgheader


def prep_file(file, corona = CORONA, m = None, n = None): 
    file.write(svg_header(corona = corona, m = m, n = n))
    write_mask_dfns(file) 
    write_clip_dfns(file)
    file.write("</defs>\n\n")

    
def sat_corona(file):     
    file.write("<use xlink:href=\"#hextile\" x=\"" + str(ORIGIN_X) + "\" y=\"" + str(ORIGIN_Y) +\
                  "\" fill=\"white\"  />\n")
    file.write(T20(0, 0))
    
    for k in range(CORONA):
        opacity = (k + 1) / (2 * CORONA)
        for t in range (6 * (k + 1)): 
            x_pos, y_pos = corona_coords(k + 1, t, dX, dY, ORIGIN_X, ORIGIN_Y)
            draw_tile(file, x_pos, y_pos, fill = "none", fill_opacity = opacity)
            if(k + 1 < CORONA): 
                file.write(T20(k + 1, t)) 
            else: 
                if(t // (k + 1) % 2 > 0): 
                    file.write(T1(k + 1, t, t // (k + 1) + 2)) 
                elif(t % (k + 1) > 0): 
                    file.write(T4(k + 1, t, t // (k + 1) + 1))
                else: 
                    file.write(T1(k + 1, t, t // (k + 1) + 1))
        


def T20p(m, n, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH, flip = False):
    t_str = "<g transform=\"translate({}, {}) ".format(*par_coords(m, n)) +\
                "rotate({}, 1000, 866)".format(phi * 60 + 30)
    if(flip): 
        t_str += " scale(1, -1)"
    t_str += "\" >\n"
    t_str += "\t<path d=\"" + TRIPLE_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-triple-arc-2)\" "
    t_str += "/>\n"
    t_str +=    "\t<path d=\"" + TRIPLE_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-triple-arc-4)\" "
    t_str += "/>\n" +\
                "\t<path d=\"" + TRIPLE_ARC[4] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-triple-arc-0)\" "
    t_str += "/>\n"
    t_str += "</g>\n\n"
    return t_str
    
def T21p(m, n, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    t_str = "<g transform=\"translate({}, {}) ".format(*par_coords(m, n)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60 + 30)
    t_str += "\t<path d=\"" + TRIPLE_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-triple-arc-4)\" "
    t_str += "/>\n"
    t_str +=    "\t<path d=\"" + TRIPLE_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-triple-arc-0)\" "
    t_str += "/>\n" +\
                "\t<path d=\"" + TRIPLE_ARC[4] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-triple-arc-2)\" "
    t_str += "/>\n"
    t_str += "</g>\n\n"
    return t_str 

    
def T1p(m, n, phi = 6, stroke=STROKE, stroke_width = STROKEWIDTH): 
    t1_str = "<g transform=\"translate({}, {}) ".format(*par_coords(m, n)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60 + 30) +\
                "\t<path d=\"" + C_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "</g>\n\n"
    return t1_str

def T4p(m, n, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*par_coords(m, n)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60 + 30) +\
                "\t<path d=\"" + C_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + C_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "</g>\n\n"
    return t_str

def T12p(m, n, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):     
    t_str = "<g transform=\"translate({}, {}) ".format(*par_coords(m, n)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60 + 30) +\
                "\t<path d=\"" + CAT_ARC[1] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + CAT_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-cat-arc-1)\" "
    t_str += "/>\n" +\
                "</g>\n\n"
    return t_str 

def T13p(m, n, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):     
    t_str = "<g transform=\"translate({}, {}) ".format(*par_coords(m, n)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60 + 30) +\
                "\t<path d=\"" + CAT_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + CAT_ARC[1] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-cat-arc-2)\" "
    t_str += "/>\n" +\
                "</g>\n\n"
    return t_str 



def sat_par_basic(file): 
    for j in range(N - 1): 
        file.write(p_tile(0, j + 1))
        file.write(p_tile(M - 1, j))
    for i in range(M - 2): 
        for j in range(N): 
            if((i < M - 2) and (j > 0) and (j < N - 1)):
                file.write(p_tile(i + 1, j, fill = "blue", fill_opacity = 0.3))
            else:
                file.write(p_tile(i + 1, j))
    for i in range(M - 2): 
        for j in range(N - 2): 
            file.write(T21p(i + 1, j + 1, 3))
        
def sat_par(file): 
    sat_par_basic(file)
    # legit version
        
    for j in range(N - 3): 
        file.write(T4p(0, j + 2, 0))
    for i in range(M - 3): 
        file.write(T4p(i + 2, 0, 4))
        
    for j in range(N - 1): 
        file.write(T1p(M - 1, j, 4))
        
    for j in range(M - 1): 
        file.write(T1p(j, N - 1, 2))
    file.write(T1p(1, 0, 0))
    file.write(T1p(0, 1, 0))
            
def sat_par_R1(file): 
    sat_par_basic(file)
    # R1 moves
    for j in range(N - 1): 
        file.write(T1p(0, j + 1, 1))
    for i in range(M - 3): 
        file.write(T4p(i + 1, N - 1, 1))
    for i in range(M - 1): 
        file.write(T1p(i + 1, 0, 5))
    for j in range(N - 3): 
        file.write(T4p(M - 1, j + 1, 3))
    file.write(T1p(M - 2, N - 1, 3))
    file.write(T1p(M - 1, N - 2, 3))

def sat_par_cross(file):
    # cross
    sat_par_basic(file)
    for j in range(N - 3): 
        file.write(T12p(0, j + 2, 5))
    for j in range(N - 1): 
        file.write(T1p(M - 1, j, 4))
    for i in range(M - 1): 
        file.write(T1p(i, N - 1, 2))   
    for i in range(M - 3): 
        file.write(T12p(i + 2, 0, 3))
    file.write(T1p(0, 1, 0))
    file.write(T1p(1, 0, 0))

def blank_corona(file, opacity = 1.0, corona = CORONA):     
#    file.write("<use xlink:href=\"#hextile\" x=\"" + str(ORIGIN_X) + "\" y=\"" + str(ORIGIN_Y) +\
#                  "\" fill=\"white\"  />\n")
    
    for k in range(corona):
        if(opacity is None):
            shade = (k + 1) / (2 * corona)
        else: 
            shade = opacity
        for t in range (6 * (k + 1)): 
            x_pos, y_pos = corona_coords(k + 1, t, dX, dY, ORIGIN_X, ORIGIN_Y)
            draw_tile(file, x_pos, y_pos, fill = "none", fill_opacity = shade)

    
#def sat_hex(file): 
    


#svgfile = open(FILENAME + ".svg", "w") 
#prep_file(svgfile)

#blank_corona(svgfile)

#svgfile.write(T15(0, 0))
#
## A, 5
##svgfile.write(T19(1, 0, 5))
##svgfile.write(T1(2, 0, 2))
##svgfile.write(T1(2, 1, 2))
#
#
## A1, 5
##svgfile.write(T16(1, 0, 4))
##svgfile.write(T1(2, 0, 2))
##svgfile.write(T1(2, 1, 2))
#
## A2, 5
#svgfile.write(T4(1, 0, 1))
#svgfile.write(T2(2, 0, 1))
#svgfile.write(T2(2, 1, 2))
#
#
## C
##svgfile.write(T13(1, 1, 1))
##svgfile.write(T1(2, 3, 2))
#
## C1
#svgfile.write(T6(1, 1, 3))
#svgfile.write(T1(2, 3, 2))
#
#
## B, 4
#svgfile.write(T19(1, 5, 5))
#svgfile.write(T4(2, 11, 0))
#svgfile.write(T1(2, 10, 0))
#
## A, 1
#svgfile.write(T19(1, 2, 1))
#svgfile.write(T1(2, 4, 4))
#svgfile.write(T1(2, 5, 4))
#
## B, 2
#svgfile.write(T19(1, 3, 3))
#svgfile.write(T4(2, 7, 4))
#svgfile.write(T1(2, 6, 4))
#
#
## A, 3
#svgfile.write(T19(1, 4, 3))
##svgfile.write(T1(2, 8, 0))
#svgfile.write(T1(2, 9, 0))
#
#svgfile.write(T2(9, 46, 1))
#svgfile.write(T2(9, 45, 0))
#svgfile.write(T2(9, 44, 5))
#svgfile.write(T1(9, 43, 0))
#svgfile.write(T10(8, 39, 0))
#svgfile.write(T10(8, 38, 0))
#svgfile.write(T10(8, 37, 0))
#
#svgfile.write(T10(8, 34, 0))
#svgfile.write(T10(8, 33, 0))
#svgfile.write(T2(9, 37, 0))
#svgfile.write(T2(9, 36, 5))
#svgfile.write(T2(9, 35, 4))
#svgfile.write(T1(8, 32, 0))
#svgfile.write(T11(8, 31, 0))
##svgfile.write(T1(7, 29, 3))
#svgfile.write(T1(7, 28, 3))
#svgfile.write(T1(7, 27, 2))
#
#svgfile.write(T2(8, 24, 4))
#svgfile.write(T2(7, 21, 1))
#svgfile.write(T11(8, 23, 0))
#svgfile.write(T1(9, 25, 4))
#
#svgfile.write(T10(8, 14, 0))
#svgfile.write(T10(8, 15, 0))
#svgfile.write(T10(8, 13, 0))
#svgfile.write(T2(9, 19, 4))
#svgfile.write(T2(9, 18, 3))
#svgfile.write(T2(9, 17, 2))
#svgfile.write(T1(9, 16, 3))  
#svgfile.write(T1(8, 16, 3))
##svgfile.write(T1(7, 29, 3))
#svgfile.write(T1(7, 14, 0))
#svgfile.write(T1(7, 13, 0))
#
#svgfile.write(T10(8, 9, 0))
#svgfile.write(T10(8, 10, 0))
#svgfile.write(T11(8, 7, 0))
#svgfile.write(T2(9, 10, 3))
#svgfile.write(T2(9, 9, 2))
#svgfile.write(T2(9, 8, 1))
#svgfile.write(T1(9, 16, 3))
#svgfile.write(T1(8, 16, 3))
##svgfile.write(T1(7, 29, 3))
#svgfile.write(T1(7, 14, 0))
#svgfile.write(T1(7, 13, 0)) 

def draw_cat1(file): 
    file.write(T11(-(CORONA - 1), 7, 5))
    file.write(T2(-(CORONA - 1), (CORONA - 1)))
    file.write(T2(-(CORONA - 2), (CORONA - 2), 3))
    
    file.write(T2(-9, 1, 0))
    file.write(T2(-9, 0, 5))
    file.write(T2(-8, -1, 4))
    file.write(T1(-8, 0, 5))
    file.write(T1(-7, 0, 2))
    file.write(T10(-7, -1, 2))
    file.write(T1(-7, -2, 5))
    file.write(T1(-6, -1, 2))
    file.write(T10(-6, -2, 2))
    file.write(T10(-5, -3, 2))
    
    file.write(T10(-2, -6, 2))
    file.write(T10(-1, -7, 2))
    file.write(T2(-1, -8, 5))
    file.write(T2(0, -9, 4))
    file.write(T1(0, -7, 2)) 
    file.write(T1(0, -8, 5))
    file.write(T2(1, -9, 3))
    file.write(T11(1, -8, 5))
    file.write(T1(1, -7, 1))
    
    file.write(T2(8, -8, 3))
    file.write(T2(7, -7, 0))
    file.write(T11(8, -7, 2))
    file.write(T1(9, -7, 3))
    
    file.write(T2(9, -1, 3))
    file.write(T2(9, 0, 2))
    file.write(T1(8, 0, 2))
    file.write(T2(8, 1, 1))
    file.write(T1(7, 0, 5))
    file.write(T10(7, 1, 2))
    file.write(T10(6, 2, 2))
    file.write(T1(7, 2, 2))
    file.write(T10(5, 3, 2))
    
    file.write()
    
#draw_cat1(svgfile)
    
def draw_AB_clusters(file, shades = None): 
    prep_file(file, corona = 6)
    if(shades is not None): 
        s_list = shades 
    else: 
        s_list = 4 * [(None, 1.0)] 
    for i in range(3): 
        file.write(draw_A_cluster(-6 + 2 * i, 4 - 4 * i, rotation = 1, 
                                  sub = i, shading = s_list[1][0], 
                              opacity = s_list[1][1]))
        file.write(draw_B_cluster(-1 + 2 * i, 4 - 4 * i, rotation = 1, 
                                   sub = i, shading = s_list[0][0], 
                                    opacity = s_list[0][1]))                     
    
def draw_clusters(file): 
    draw_tile(file, *cor_axis_coords(-9, 7))
    draw_tile(file, *cor_axis_coords(-8, 7))
    draw_tile(file, *cor_axis_coords(-8, 6))
    file.write(T1(-9, 7, 1))
    file.write(T1(-8, 7, 1))
    file.write(T19(-8, 6, 4))
    
    
    draw_tile(file, *cor_axis_coords(-7, 3))
    draw_tile(file, *cor_axis_coords(-6, 3))
    draw_tile(file, *cor_axis_coords(-6, 2))
    file.write(T1(-7, 3, 1))
    file.write(T1(-6, 3, 1))
    file.write(T16(-6, 2, 3))
    
    draw_tile(file, *cor_axis_coords(-5, -1))
    draw_tile(file, *cor_axis_coords(-4, -1))
    draw_tile(file, *cor_axis_coords(-4, -2))
    file.write(T2(-5, -1, 0))
    file.write(T2(-4, -1, 1))
    file.write(T4(-4, -2, 0))
    
    draw_tile(file, *cor_axis_coords(-4, 7))
    draw_tile(file, *cor_axis_coords(-3, 7))
    draw_tile(file, *cor_axis_coords(-3, 6))
    file.write(T1(-4, 7, 0))
    file.write(T4(-3, 7, 0))
    file.write(T19(-3, 6, 5))
    
    draw_tile(file, *cor_axis_coords(-2, 3))
    draw_tile(file, *cor_axis_coords(-1, 3))
    draw_tile(file, *cor_axis_coords(-1, 2))
    file.write(T1(-2, 3, 0))
    file.write(T4(-1, 3, 0))
    file.write(T16(-1, 2, 4))
    
    draw_tile(file, *cor_axis_coords(0, -1))
    draw_tile(file, *cor_axis_coords(1, -1))
    draw_tile(file, *cor_axis_coords(1, -2))
    file.write(T1(0, -1, 0))
    file.write(T4(1, -1, 0))
    file.write(T15(1, -2, 1))
    
def draw_CD_clusters(): 
    file = open("CDclusters.svg", "w") 
    prep_file(file, corona = 4) 
    file.write(draw_C_cluster(-2, 0, rotation = 1, 
                   shading = SHADE_LIST[3][0], 
                    opacity = SHADE_LIST[3][1]))
    file.write(draw_D_cluster(1, 0, rotation = 1, 
                   shading = SHADE_LIST[2][0], 
                    opacity = SHADE_LIST[2][1]))
    file.write("</svg>") 
    file.close()
    
    
    
def edge_clusters(file): 
    draw_tile(file, *cor_axis_coords(-9, 7))
    draw_tile(file, *cor_axis_coords(-9, 6))
    draw_tile(file, *cor_axis_coords(-8, 5))
    file.write(T4(-9, 7, 0))
    file.write(T19(-9, 6, 5))
    file.write(T1(-8, 5, 4))
    
    draw_tile(file, *cor_axis_coords(-4, 7))
    draw_tile(file, *cor_axis_coords(-4, 6)) 
    draw_tile(file, *cor_axis_coords(-3, 5))
    file.write(T1(-4, 7, 1))
    file.write(T19(-4, 6, 2))
    file.write(T4(-3, 5, 3))

def draw_base_torus(file): 
    blank_corona(file) 
    file.write(T1(-2, 2, 1))
    file.write(T1(-1, 2, 1))
    file.write(T19(-1, 1, 4))

    file.write(T1(-1, -1, 5))
    file.write(T1(0, -2, 5))
    file.write(T19(0, -1, 2))

    file.write(T1(2, 0, 3))
    file.write(T1(2, -1, 3))
    file.write(T19(1, 0, 0))
    
    file.write(T1(0, 2, 1))
    file.write(T4(1, 1, 1))
    file.write(T19(0, 1, 0))

    file.write(T1(2, -2, 3))
    file.write(T4(1, -2, 3))
    file.write(T19(1, -1, 2))

    file.write(T1(-2, 0, 5))
    file.write(T4(-2, 1, 5))
    file.write(T19(-1, 0, 4))
    
    file.write(T15(0, 0, 1))

    
def draw_n3_torus(file): 
    blank_corona(file) 
    # A vertex
    file.write(T1(-3, 3, 1))
    file.write(T1(-2, 3, 1))
    file.write(T19(-2, 2, 4))

    # A vertex
    file.write(T1(-1, -2, 5))
    file.write(T1(0, -3, 5))
    file.write(T19(0, -2, 2))

    # A vertex
    file.write(T1(3, 0, 3))
    file.write(T1(3, -1, 3))
    file.write(T19(2, 0, 0))
    
    # B vertex
    file.write(T1(0, 3, 1))
    file.write(T4(1, 2, 1))
    file.write(T19(0, 2, 0))

    # B vertex
    file.write(T1(3, -3, 3))
    file.write(T4(2, -3, 3))
    file.write(T19(2, -2, 2))

    # B vertex
    file.write(T1(-3, 0, 5))
    file.write(T4(-3, 1, 5))
    file.write(T19(-2, 0, 4))
    
    file.write(T1(-1, 3, 1))
    file.write(T19(-1, 2, 2))
    file.write(T4(0, 1, 3))    
    
    
    file.write(T4(2, 1, 1))
    file.write(T19(1, 1, 0))
    file.write(T4(1, 0, 5))

    file.write(T1(3, -2, 3))
    file.write(T19(2, -1, 4))
    file.write(T4(1, -1, 5))    

    file.write(T4(1, -3, 3))
    file.write(T19(1, -2, 2))
    file.write(T4(0, -1, 1))

    file.write(T1(-2, -1, 5))
    file.write(T19(-1, -1, 0))
    file.write(T4(-1, 0, 1))    

    file.write(T4(-3, 2, 5))
    file.write(T19(-2, 1, 4))
    file.write(T4(-1, 1, 3))

def draw_torus_edge(file): 
    #blank_corona(file)    
        
    for i in range(CORONA + 1): 
        draw_tile(file, *cor_axis_coords(-CORONA + i, CORONA))
    for i in range(CORONA + 2): 
        draw_tile(file, *cor_axis_coords(-CORONA + i, CORONA - 1))
    for i in range(CORONA + 3): 
        draw_tile(file, *cor_axis_coords(-CORONA + i, CORONA - 2))
    
    for i in range(CORONA + 1): 
        draw_tile(file, *cor_axis_coords(-CORONA + 2 + i, CORONA - 4))
    for i in range(CORONA + 2): 
        draw_tile(file, *cor_axis_coords(-CORONA + 2 + i, CORONA - 5))
    for i in range(CORONA + 3): 
        draw_tile(file, *cor_axis_coords(-CORONA + 2 + i, CORONA - 6))
    
    
    # A cluster
    file.write(T1(-CORONA, CORONA, 1))
    file.write(T1(-(CORONA - 1), CORONA, 1))
    file.write(T19(-(CORONA - 1), (CORONA - 1), 4))
    
    # B cluster
    file.write(T1(0, CORONA, 1))
    file.write(T4(1, CORONA - 1, 1))
    file.write(T19(0, CORONA - 1, 0))
    
    # D cluster
    for i in range(CORONA - 2): 
        file.write(T1(-1 - i, CORONA, 1))
        file.write(T19(-1 - i, CORONA - 1, 2))
        file.write(T4(0 - i, CORONA - 2, 3))    
    
    # B cluster
    file.write(T1(-CORONA + 2, CORONA  - 4))
    file.write(T4(-CORONA + 2 + 1, CORONA - 4 , 0))
    file.write(T19(-CORONA + 2 + 1, CORONA - 4 - 1, 5))

    # A cluster
    file.write(T1(0 + 2, CORONA - 4, 2))
    file.write(T1(0 + 2 + 1, CORONA - 4 - 1, 2))
    file.write(T19(0 + 2, CORONA - 4 - 1, 5))

    for i in range(CORONA - 2):
        file.write(T4(-CORONA + 4 + i, CORONA - 4, 0))
        file.write(T19(-CORONA + 4 + i, CORONA - 5, 5))
        file.write(T1(- CORONA + 5 + i, CORONA - 6, 4))



    
#edge_clusters(svgfile)
#draw_n3_torus(svgfile)
#draw_torus_edge(svgfile) 
    
def shaded_corona(file, color): 
    draw_tile(file, *cor_axis_coords(0, 0), fill = color, fill_opacity = 0.0) 
    for k in range(CORONA + 1): 
        for t in range(6 * k): 
            draw_tile(file, *corona_coords(k, t), fill = color, fill_opacity = 0.5 * (k / CORONA))
    
def draw_k2_trefoil(file): 
    prep_file(file) 
    shaded_corona(file, "blue")
    file.write(T2(-1, 2, 0))
    file.write(T2(0, 2, 1))
    file.write(T2(1, 1, 2))
    
    file.write(T2(2, -1, 2))
    file.write(T2(2, -2, 3))
    file.write(T2(1, -2, 4))

    file.write(T2(-2, 1, 0))
    file.write(T2(-2, 0, 5))
    file.write(T2(-1, -1, 4))
    
    file.write(T2(0, 1, 1))
    file.write(T2(1, -1, 3))
    file.write(T2(-1, 0, 5))
    
    file.write(T11(1, 0, 1))
    file.write(T11(-1, 1, 5))
    file.write(T11(0, -1, 3)) 
    
def draw_k1_trefoil(file): 
    prep_file(file) 
    shaded_corona(file, "blue") 
    file.write(T20(0, 0, 0))
    file.write(T1(0, 1, 1)) 
    file.write(T1(1, 0, 3)) 
    file.write(T1(0, -1, 5)) 
    file.write(T1(1, -1, 3)) 
    file.write(T1(-1, 0, 5)) 
    file.write(T1(-1, 1, 1)) 
    
def draw_k1_unknot(file): 
    prep_file(file) 
    shaded_corona(file, "blue") 
    file.write(T21(0, 0, 1))
    file.write(T1(0, 1, 1)) 
    file.write(T1(1, 0, 3)) 
    file.write(T1(0, -1, 5)) 
    file.write(T1(1, -1, 3)) 
    file.write(T1(-1, 0, 5)) 
    file.write(T1(-1, 1, 1)) 
    

    
    





    
def stretched_coords(x, y, m = M, n = N): 
    origin_x = dX 
    if(m > n): 
        origin_y = (m + n) * dy
    else: 
        origin_y = (m) * dY 
    x_pos = origin_x + (x * 1500) 
    y_pos = origin_y - (x * Y_OFFSET) - y * dY 
    
    return x_pos, y_pos
    
def T4s(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [C_ARC[2], None]]
    t_str = make_tile_stretched(x, y, arcs, phi, stroke, stroke_width)    
    return t_str
    
    
def T1s(x, y, phi = 6, stroke=STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None]]
    t1_str = make_tile_stretched(x, y, arcs, phi, stroke, stroke_width)    
    return t1_str 
    
def T20s(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    arcs = [[TRIPLE_ARC[0], None, "clipTripleArc2"], 
            [TRIPLE_ARC[2], None, "clipTripleArc4"], 
            [TRIPLE_ARC[4], None, "clipTripleArc0"]] 
    t_str = make_tile_stretched(kappa, theta, arcs, phi, stroke, stroke_width)    
    return t_str


    
def stretched_hexagon(file, m, n):     
    if(m > n): 
        CORONA = m
    else: 
        CORONA = n
    
    prep_file(file, m = m, n = n) 

    for i in range(m): 
        for j in range(n + i): 
            draw_tile(file, *stretched_coords(j, m - i - 1)) 
            if((i < m - 1) and (j > 0) and (j < n + m - 2)): 
                file.write(T20s(j, m  -i - 2))
            
    for i in range(n): 
        file.write(T1s(i, m - 1, 1))
    for i in range(m - 2): 
        file.write(T4s(0, i + 1, 5))
        file.write(T4s(m + n - (i + 1) - 2, i + 1, 1))
        
                
    for i in range(m - 1): 
        for j in range(n + (m - i - 2)): 
            draw_tile(file, *stretched_coords(j + i + 1, -i - 1)) 
            if((i < m - 2) and (j > 0) and (j < n + m - i - 3)): 
                file.write(T20s(j + i + 1, -i - 1))
            
    for i in range(m): 
        file.write(T1s(i, -(i), 5))
        file.write(T1s(m + n - 2, -(i), 3))
    for i in range(n - 2): 
        file.write(T4s(i + m, -m + 1, 3))

def sextant(x, y): 
    rot = 0   
    if((x < 0) and (y > 0) and (x + y >= 0)): 
        rot = 1
    if((x < 0) and (y >= 0) and (x + y < 0)): 
        rot = 2 
    if((x <= 0) and (y < 0) and (x + y < 0)): 
        rot = 3 
    if((x > 0) and (y < 0) and (x + y <= 0)): 
        rot = 4 
    if((x > 0) and (y <= 0) and (x + y > 0)): 
        rot = 5 
        
    return rot
    

    
def rot_cluster(rot): 
    dx = 0
    dy = 0
    if((rot == 1) or (rot == 2)): 
        dx = -1
    if((rot % 3 == 0)): 
        dx = 0 
    if((rot == 4) or (rot == 5)): 
        dx = 1 
    if((rot == 0) or (rot == 1)): 
        dy = 1 
    if((rot == 2) or (rot == 5)): 
        dy = 0 
    if((rot == 3) or (rot == 4)): 
        dy = -1 
    return dx, dy 
    


        
    
def draw_A_cluster(x, y, rotation = None, sub = 0, color = STROKE, 
                   shading = None, opacity = 1.0): 
    if(rotation is not None): 
        rot = rotation
    else: 
       rot = sextant(x, y) 
    t2 = list(rot_cluster((rot + 4) % 6)) 
    t3 = list(rot_cluster((rot + 3) % 6))  
    t4 = list(rot_cluster((rot + 3) % 6))
    
    tile_str = ""
    if(shading is not None): 
        tile_str += draw_tile_str(*cor_axis_coords(x, y), 
                    fill = shading, fill_opacity = opacity)
        tile_str += draw_tile_str(*cor_axis_coords(x + t2[0], y + t2[1]), 
                    fill = shading, fill_opacity = opacity)
        tile_str += draw_tile_str(*cor_axis_coords(x + t3[0], y + t3[1]), 
                    fill = shading, fill_opacity = opacity)

    if(sub == 1): 
        tile_str += T1(x, y, 2 - rot, ) 
        tile_str += T1(x + t2[0], y + t2[1], 2 - rot, stroke = color)
        tile_str += T16(x + t3[0], y + t3[1], 4 - rot, stroke = color) 
    elif(sub == 2): 
        tile_str += T2(x, y, 1 - rot, stroke = color) 
        tile_str += T2(x + t2[0], y + t2[1], 2 - rot, stroke = color)
        tile_str += T4(x + t3[0], y + t3[1], 1 - rot, stroke = color) 
    else:
        tile_str += T1(x, y, 2 - rot, stroke = color) 
        tile_str += T1(x + t2[0], y + t2[1], 2 - rot, stroke = color)
        tile_str += T19(x + t3[0], y + t3[1], 5 - rot, stroke = color) 
    tile_str += T1(x + t3[0] + t4[0], y + t3[1] + t4[1], 0 - rot, stroke = color)
    return tile_str
    
def draw_B_cluster(x, y, rotation = None, sub = 0, color = STROKE, 
                   shading = None, opacity = 1.0): 
    if(rotation is not None): 
        rot = rotation
    else: 
       rot = sextant(x, y) 
    t2 = list(rot_cluster((rot + 4) % 6)) 
    t3 = list(rot_cluster((rot + 3) % 6))  
    
    tile_str = "" 
    if(shading is not None): 
        tile_str += draw_tile_str(*cor_axis_coords(x, y), 
                    fill = shading, fill_opacity = opacity)
        tile_str += draw_tile_str(*cor_axis_coords(x + t2[0], y + t2[1]), 
                    fill = shading, fill_opacity = opacity)
        tile_str += draw_tile_str(*cor_axis_coords(x + t3[0], y + t3[1]), 
                    fill = shading, fill_opacity = opacity)
    if(sub == 1): 
        tile_str += T1(x, y, 1 - rot, stroke = color)
        tile_str += T4(x + t2[0], y + t2[1], 1 - rot, stroke = color)
        tile_str += T16(x + t3[0], y + t3[1], 5 - rot, stroke = color) 
    elif(sub == 2): 
        tile_str += T1(x, y, 1 - rot, stroke = color)
        tile_str += T4(x + t2[0], y + t2[1], 1 - rot, stroke = color)
        tile_str += T15(x + t3[0], y + t3[1], 0 - rot, stroke = color) 
    else: 
        tile_str += T1(x, y, 1 - rot, stroke = color)
        tile_str += T4(x + t2[0], y + t2[1], 1 - rot, stroke = color)
        tile_str += T19(x + t3[0], y + t3[1], 0 - rot, stroke = color) 
    
    return tile_str
    
def draw_C_cluster(x, y, rotation = None, color = STROKE, 
                   shading = None, opacity = 1.0): 
    if(rotation is not None): 
        rot = rotation
    else: 
       rot = sextant(x, y) 
    t2 = list(rot_cluster((rot + 2) % 6)) 
    t3 = list(rot_cluster((rot + 3) % 6))  
    
    t_str = "" 
    if(shading is not None): 
        t_str += draw_tile_str(*cor_axis_coords(x, y), 
                    fill = shading, fill_opacity = opacity)
        t_str += draw_tile_str(*cor_axis_coords(x + t2[0], y + t2[1]), 
                    fill = shading, fill_opacity = opacity)
        t_str += draw_tile_str(*cor_axis_coords(x + t2[0] + t3[0], y + t2[1] + t3[1]), 
                    fill = shading, fill_opacity = opacity)
    t_str += T1(x, y, 2 - rot, stroke = color) 
    t_str += T19(x + t2[0], y + t2[1], 3 - rot, stroke = color) 
    t_str += T4(x + t2[0] + t3[0], y + t2[1] + t3[1], 4 - rot, stroke = color)
    
    return t_str

def draw_D_cluster(x, y, rotation = None, color = STROKE,
                   shading = None, opacity = 1.0): 
    if(rotation is not None): 
        rot = rotation
    else: 
       rot = sextant(x, y) 
    t2 = list(rot_cluster((rot + 2) % 6)) 
    t3 = list(rot_cluster((rot + 3) % 6))  
    
    t_str = "" 
    if(shading is not None): 
        t_str += draw_tile_str(*cor_axis_coords(x, y), 
                    fill = shading, fill_opacity = opacity)
        t_str += draw_tile_str(*cor_axis_coords(x + t2[0], y + t2[1]), 
                    fill = shading, fill_opacity = opacity)
        t_str += draw_tile_str(*cor_axis_coords(x + t2[0] + t3[0], y + t2[1] + t3[1]), 
                    fill = shading, fill_opacity = opacity)
    t_str += T4(x, y, 1 - rot, stroke = color) 
    t_str += T19(x + t2[0], y + t2[1], 0 - rot, stroke = color) 
    t_str += T1(x + t2[0] + t3[0], y + t2[1] + t3[1], 5 - rot, stroke = color)
    
    return t_str 
    
def draw_X_over(x, y, rotation = None, color = STROKE, 
                   shading = None, opacity = 1.0): 
    if(rotation is not None): 
        rot = rotation
    else: 
       rot = sextant(x, y) 
    t01 = list(rot_cluster((rot + 2) % 6)) 
    t10 = list(rot_cluster((rot + 4) % 6))  
    t11 = list(rot_cluster((rot + 3) % 6)) 
    tx = list(rot_cluster((rot + 2) % 6)) 
    ty = list(rot_cluster((rot + 4) % 6)) 
    
    t_str = "" 
    if(shading is not None): 
        t_str += draw_tile_str(*cor_axis_coords(x, y), 
                    fill = shading, fill_opacity = opacity)
        t_str += draw_tile_str(*cor_axis_coords(x + t01[0], y + t01[1]), 
                    fill = shading, fill_opacity = opacity)
        t_str += draw_tile_str(*cor_axis_coords(x + t10[0], y + t10[1]), 
                    fill = shading, fill_opacity = opacity)

    t_str += T1(x, y, 2 - rot, stroke = color)
    t_str += T4(x + t01[0], y + t01[1], 0 - rot, stroke = color)
    
    t_str += T1(x + t10[0], y + t10[1], 2 - rot, stroke = color)
    t_str += T19(x + t11[0], y + t11[1], 5 - rot, stroke = color)
    t_str += T19(x + t11[0] + tx[0], y + t11[1] + tx[1], 5 - rot, stroke = color)
    
    t_str += T1(x + (2 * ty[0]), y + (2 * ty[1]), 2 - rot, stroke = color)
    t_str += T17(x + tx[0] + (2 * ty[0]), y + tx[1] + (2 * ty[1]), 1 - rot, stroke = color)
    t_str += T14(x + (2 * tx[0]) + (2 * ty[0]), 
                 y + (2 * tx[1]) + (2 * ty[1]), 1 - rot, stroke = color)
    
    t_str += T1(x + (3 * ty[0]), y + (3 * ty[1]), 2 - rot, stroke = color) 
    t_str += T19(x + tx[0] + (3 * ty[0]), 
                 y + tx[1] + (3 * ty[1]), 5 - rot, stroke = color)
    t_str += T23(x + (2 * tx[0]) + (3 * ty[0]), 
                 y + (2 * tx[1]) + (3 * ty[1]), 1 - rot, stroke = color)
    t_str += T23(x + (3 * tx[0]) + (3 * ty[0]), 
                 y + (3 * tx[1]) + (3 * ty[1]), 3 - rot, stroke = color)
    t_str += T4(x + (2 * tx[0]) + (4 * ty[0]), 
                y + (2 * tx[1]) + (4 * ty[1]), 4 - rot, stroke = color)
    t_str += T4(x + (4 * tx[0]) + (4 * ty[0]), 
                y + (4 * tx[1]) + (4 * ty[1]), 4 - rot, stroke = color)    
    print("crap")
    return t_str
    
    

    
def draw_torus(file, corona = CORONA, loop = None, color = STROKE, 
               shade_list = None, 
               corner_list = None, sub_list = None): 
    if(shade_list is None): 
        shade_list = [(None, None), (None, None), (None, None), (None, None)]
        
    if(corner_list is None): 
        corner_list = list(range(6)) 
    if(sub_list is None): 
        sub_list = 6 * [0]             

    for i in range(corona - 2): 
        file.write(draw_D_cluster(-i - 1, corona, color = color, 
                                  shading = shade_list[2][0], 
                                opacity = shade_list[2][1])) 
        file.write(draw_D_cluster(-corona + i + 1, 0 - i - 1, color = color, 
                                  shading = shade_list[2][0], 
                                    opacity = shade_list[2][1])) 
        file.write(draw_D_cluster(corona, -i - 2, color = color, 
                              shading = shade_list[2][0], 
                                opacity = shade_list[2][1])) 
                             
        file.write(draw_C_cluster(corona - 1 - i, i + 1, color = color, 
                              shading = shade_list[3][0], 
                                opacity = shade_list[3][1]))                                   
        file.write(draw_C_cluster(-corona, i + 2, color = color, 
                              shading = shade_list[3][0], 
                                opacity = shade_list[3][1]))                                   
        file.write(draw_C_cluster(i + 1, -corona, color = color, 
                              shading = shade_list[3][0], 
                                opacity = shade_list[3][1])) 
                                  
    for c in corner_list: 
        if(c == 1):                 
            file.write(draw_B_cluster(-corona, corona, color = color, 
                                  shading = shade_list[0][0], 
                                    opacity = shade_list[0][1], 
                                    sub = sub_list[c])) 
        elif(c == 3):                            
            file.write(draw_B_cluster(0, -corona, color = color, 
                                  shading = shade_list[0][0], 
                                    opacity = shade_list[0][1], 
                                    sub = sub_list[c])) 

        elif(c == 5): 
            file.write(draw_B_cluster(corona, 0, color = color, 
                                  shading = shade_list[0][0], 
                                    opacity = shade_list[0][1], 
                                    sub = sub_list[c])) 

        
        elif(c == 0): 
            file.write(draw_A_cluster(0, corona, color = color, 
                                  shading = shade_list[1][0], 
                                    opacity = shade_list[1][1], 
                                    sub = sub_list[c])) 
        elif(c == 2): 
            file.write(draw_A_cluster(-corona, 0, color = color, 
                                  shading = shade_list[1][0], 
                                    opacity = shade_list[1][1], 
                                    sub = sub_list[c])) 

        elif(c == 4): 
            file.write(draw_A_cluster(corona, -corona, color = color, 
                                  shading = shade_list[1][0], 
                                    opacity = shade_list[1][1], 
                                    sub = sub_list[c])) 


    


#    file.write(draw_A_cluster(-CORONA, CORONA, sub = 1))
#    file.write(draw_B_cluster(0, CORONA, sub = 2))
#    file.write(draw_D_cluster(-1, CORONA)) 
#    file.write(draw_D_cluster(2, 1))

def draw_simple_torus(file, corona = CORONA, shade_list = None, 
                      corner_list = None, sub_list = None): 
    prep_file(file, corona) 
    blank_corona(file, corona = corona)
    draw_torus(file, corona = corona, shade_list = shade_list, 
               corner_list = corner_list, 
               sub_list = sub_list)

def draw_nested_torii(file, corona = CORONA, colors = None, shading_l = None): 
    prep_file(file) 
    blank_corona(file, opacity = 1.0) 
    if(colors is not None): 
        draw_torus(file, corona, color = colors[0]) 
        draw_torus(file, corona - 2, color = colors[1]) 
    else: 
        draw_torus(file, corona, shade_list = shading_l) 
        draw_torus(file, corona - 2, shade_list = shading_l) 
        

def draw_looped_torii(file, corona = CORONA): 
    prep_file(file) 
    blank_corona(file) 
#    draw_torus(file, corona) 
#    draw_torus(file, corona - 2) 
    draw_outer_looped_torus(file, corona)
    draw_inner_looped_torus(file, corona)
    file.write(draw_X_over(0, corona))
    
def draw_outer_looped_torus(file, corona = CORONA, loop = 0): 
#    file.write(draw_X_over(0, corona)) 
    file.write(draw_A_cluster(-corona, 0)) 
    file.write(draw_A_cluster(corona, -corona)) 
    
    file.write(draw_B_cluster(-corona, corona)) 
    file.write(draw_B_cluster(0, -corona)) 
    file.write(draw_B_cluster(corona, 0)) 
    
    for i in range(corona - 3): 
        file.write(draw_D_cluster(-2 - i, corona))
        
    for i in range(corona - 4): 
        file.write(draw_C_cluster(corona - i - 1, i + 1))
        
    for i in range(corona - 2): 
        file.write(draw_C_cluster(-corona, i + 2))
        file.write(draw_C_cluster(i + 1, -corona)) 
        file.write(draw_D_cluster(-corona + i + 1, -i - 1)) 
        file.write(draw_D_cluster(corona, -corona + i + 1)) 
        
def draw_inner_looped_torus(file, corona = CORONA, loop = 0): 
    k = corona - 2    
    file.write(draw_A_cluster(-k, 0)) 
    file.write(draw_A_cluster(k, -k))
    file.write(draw_B_cluster(-k, k)) 
    file.write(draw_B_cluster(0, -k)) 
    file.write(draw_B_cluster(k, 0)) 
    for i in range(k - 2): 
        file.write(draw_D_cluster(-i - 1, k)) 
        file.write(draw_D_cluster(-k + i + 1, -i - 1)) 
        file.write(draw_D_cluster(k, -k + i + 1))
        file.write(draw_C_cluster(-k, k - 1 - i)) 
        file.write(draw_C_cluster(i + 1, -k)) 
        file.write(draw_C_cluster(k - i - 1, i + 1))
    
    

    
def draw_loop(file, corona = CORONA, loops = 2): 
    prep_file(file) 
    blank_corona(file) 
    draw_outer_looped_torus(file)

def draw_torus_Xover(file): 
    prep_file(file)
    for i in range(2): 
        draw_tile(file, *cor_axis_coords(-1 + i, 1))
    for i in range(3): 
        draw_tile(file, *cor_axis_coords(-1 + i, 0))
        draw_tile(file, *cor_axis_coords(i, -1))        
    for i in range(4): 
        draw_tile(file, *cor_axis_coords(i, -2))
    for i in range(5): 
        draw_tile(file, *cor_axis_coords(i, -3))
    file.write(draw_X_over(0, 1))

def draw_k2_torus_series():  
    for i in range(6): 
        fname = "k2-torus-{}.svg".format(i)
        file_i = open(fname, "w")
    
        draw_simple_torus(file_i, shade_list = SHADE_LIST, 
                        corner_list = list(range(i + 1)), 
                        sub_list = [0, 0, 1, 1, 2, 2])
        file_i.write("</svg>\n") 
        file_i.close()
        
def draw_k3_torus_series(): 
    for i in range(7): 
        fname = "k3-torus-{}.svg".format(i) 
        file_i = open(fname, "w") 
        
        prep_file(file_i, corona = 3) 
        blank_corona(file_i, corona = 3)
        
        file_i.write(draw_A_cluster(0, 3, 0, shading = SHADE_LIST[0][0], 
                                  opacity = SHADE_LIST[0][1]))
        file_i.write(draw_A_cluster(-3, 0, 2, 
                                    sub = 1, 
                                    shading = SHADE_LIST[0][0], 
                                    opacity = SHADE_LIST[0][1]))
        file_i.write(draw_A_cluster(3, -3, 4, sub = 2, 
                                    shading = SHADE_LIST[0][0], 
                                    opacity = SHADE_LIST[0][1]))
        file_i.write(draw_B_cluster(-3, 3, 1, shading = SHADE_LIST[1][0], 
                                    opacity = SHADE_LIST[1][1])) 
        file_i.write(draw_B_cluster(0, -3, 3, sub = 1, 
                                    shading = SHADE_LIST[1][0], 
                                    opacity = SHADE_LIST[1][1])) 
        file_i.write(draw_B_cluster(3, 0, 5, sub = 2, 
                                    shading= SHADE_LIST[1][0], 
                                    opacity = SHADE_LIST[1][1])) 
        for j in range(i): 
            if(j == 0): 
                file_i.write(draw_D_cluster(-1, 3, shading = SHADE_LIST[2][0],
                                                opacity = SHADE_LIST[2][1]))
            if(j == 1): 
                file_i.write(draw_C_cluster(-3, 2, shading = SHADE_LIST[3][0],
                                                opacity = SHADE_LIST[3][1]))

            if(j == 2): 
                file_i.write(draw_D_cluster(-2, -1, shading = SHADE_LIST[2][0],
                                                opacity = SHADE_LIST[2][1]))
            if(j == 3): 
                file_i.write(draw_C_cluster(1, -3, shading = SHADE_LIST[3][0],
                                                opacity = SHADE_LIST[3][1]))
            if(j == 4): 
                file_i.write(draw_D_cluster(3, -2, shading = SHADE_LIST[2][0],
                                                opacity = SHADE_LIST[2][1]))
            if(j == 5): 
                file_i.write(draw_C_cluster(2, 1, shading = SHADE_LIST[3][0],
                                                opacity = SHADE_LIST[3][1]))
                                    
        file_i.write("</svg>")
        file_i.close()

def draw_nested_shaded(file, corona = CORONA, shade_l = SHADE_LIST): 
    prep_file(file) 
    blank_corona(file, opacity = 1.0) 
    if(colors is not None): 
        draw_torus(file, corona, color = colors[0]) 
        draw_torus(file, corona - 2, color = colors[1]) 
    else: 
        draw_torus(file, corona) 
        draw_torus(file, corona - 2) 

    
    
def test(file): 
    #prep_file(file) 
    #draw_tile(file, *cor_axis_coords(0, 0)) 
    draw_simple_torus(file, corona = 5, shade_list = SHADE_LIST)
    
    
svgfile = open(FILENAME + ".svg", "w") 
# draw_AB_clusters(svgfile, shades = SHADE_LIST)
#draw_simple_torus(svgfile, corona = 3, shade_list = SHADE_LIST)

#draw_k1_unknot(svgfile)
M = 2
N = 5
#stretched_hexagon(svgfile, M + 1, N + 1)
#draw_looped_torii(svgfile, corona = 6)

#draw_looped_torii(svgfile, corona = 6)

draw_simple_torus(svgfile, shade_list = SHADE_LIST)

svgfile.write("</svg>\n") 
svgfile.close()

#draw_k2_torus_series()

        