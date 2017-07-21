FILENAME = "grid10" 


M = 4
N = 5 

CORONA = 10

ROTATE = 30


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

ORIGIN_X = (CORONA - 1) * dX
ORIGIN_Y = (CORONA - 1) * dX
SVG_HT = (CORONA * 2 + 3) * dY

STROKEWIDTH = 100 
STROKE = "black"

CON_PT = [(1000, 0), (1750, 433), (1750, 1299), (1000, 1732), 
              (250, 1299), (250, 433)]
VERTEX = [(1500 - 250, 0 + 433), (2000 - 250, 866), (1500 - 250, 1732 - 433), (500 + 250, 1732 - 433), 
              (0 + 250, 866), (500 + 250, 0 + 433)]

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
        if(a[1] is not None): 
            t_str += "mask=\"url(#{})\" ".format(a[1])
        t_str += "/>\n" 
    t_str += "</g>\n\n"
    return t_str
                
def T1(x, y, phi = 6, stroke=STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None]]
    t1_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
#    t1_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + C_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "</g>\n\n"
    return t1_str 
    
    
def T2(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[0], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + CAT_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "</g>\n\n"
    return t_str

def T3(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[STRAIGHT_ARC[0], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + STRAIGHT_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "</g>\n\n"
    return t_str

def T4(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [C_ARC[0], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + C_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + C_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "</g>\n\n"
    return t_str

def T5(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [C_ARC[3], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + C_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + C_ARC[3] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "</g>\n\n"
    return t_str
    
def T6(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [STRAIGHT_ARC[0], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    

#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + C_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + STRAIGHT_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "</g>\n\n"
    return t_str

def T7(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [CAT_ARC[2], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    
    
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + C_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + CAT_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "</g>\n\n"
    return t_str

def T8(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[0], None], [CAT_ARC[3], None]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    

#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + CAT_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + CAT_ARC[3] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "</g>\n\n"
    return t_str

def T9(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[1], None], [STRAIGHT_ARC[0], "mCatArc1"]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)    

#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + CAT_ARC[1] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + STRAIGHT_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mCatArc1)\" "
#    t_str += "/>\n" +\
#                "</g>\n\n"
    return t_str 

def T10(x, y, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):  
    arcs = [[STRAIGHT_ARC[1], None], [STRAIGHT_ARC[2], "mStraightArc1"]]
    t_str = make_tile(x, y, arcs, phi, stroke, stroke_width)
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + STRAIGHT_ARC[1] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + STRAIGHT_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#m-straight-arc-1)\" "
#    t_str += "/>\n" +\
#                "</g>\n\n"
    return t_str 
    
def T11(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[STRAIGHT_ARC[2], None], [STRAIGHT_ARC[1], "mStraightArc2"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
        
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + STRAIGHT_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + STRAIGHT_ARC[1] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mStraightArc2)\" "
#    t_str += "/>\n" +\
#                "</g>\n\n"
    return t_str 

def T12(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[1], None], [CAT_ARC[2], "mCatArc1"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
    
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + CAT_ARC[1] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + CAT_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mCatArc1)\" "
#    t_str += "/>\n" +\
#                "</g>\n\n"
    return t_str 

def T13(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):   
    arcs = [[CAT_ARC[2], None], [CAT_ARC[1], "mCatArc2"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    

#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + CAT_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + CAT_ARC[1] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mCatArc2)\" "
#    t_str += "/>\n" +\
#                "</g>\n\n"
    return t_str 



def T14(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [C_ARC[3], None], [STRAIGHT_ARC[0], None]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    

#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + C_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + C_ARC[3] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + STRAIGHT_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "</g>\n\n"
    return t_str

def T15(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[C_ARC[0], None], [C_ARC[2], None], [C_ARC[4], None]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    

#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
#                "\t<path d=\"" + C_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + C_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "\t<path d=\"" + C_ARC[4] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n" +\
#                "</g>\n\n"
    return t_str

def T16(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[1], None], [CAT_ARC[2], "mCatArc1"], [C_ARC[5], None]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
#
#    t_str = "<g id=\"tile-{}-{}\" ".format(kappa, theta)
#    t_str += "transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
#    t_str += "\t<path d=\"" + CAT_ARC[1] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n"
#    t_str +=    "\t<path d=\"" + CAT_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mCatArc1)\" "
#    t_str += "/>\n" +\
#                "\t<path d=\"" + C_ARC[5] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n"
#    t_str += "</g>\n\n"
    return t_str

def T17(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[2], None], [CAT_ARC[1], "mCatArc2"], [C_ARC[5], None]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
#
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
#    t_str += "\t<path d=\"" + CAT_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n"
#    t_str +=    "\t<path d=\"" + CAT_ARC[1] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mCatArc2)\" "
#    t_str += "/>\n" +\
#                "\t<path d=\"" + C_ARC[5] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n"
#    t_str += "</g>\n\n"
    return t_str 
    
def T18(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    arcs = [[CAT_ARC[0], None], [CAT_ARC[3], None], [STRAIGHT_ARC[5], "mDoubleCatArc"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
#
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
#    t_str += "\t<path d=\"" + CAT_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n"
#    t_str +=    "\t<path d=\"" + CAT_ARC[3] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "/>\n" +\
#                "\t<path d=\"" + STRAIGHT_ARC[5] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mDoubleCatArc)\" "
#    t_str += "/>\n"
#    t_str += "</g>\n\n"
    return t_str

def T19(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    arcs = [[CAT_ARC[0], None], [CAT_ARC[3], "mStraightArc2"], [STRAIGHT_ARC[2], "mCatArc0"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
#
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
#    t_str += "\t<path d=\"" + CAT_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" " +\
#                "/>\n"
#    t_str +=    "\t<path d=\"" + CAT_ARC[3] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mStraightArc2)\" "
#    t_str += "/>\n" +\
#                "\t<path d=\"" + STRAIGHT_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mCatArc0)\" "
#    t_str += "/>\n"
#    t_str += "</g>\n\n"
    return t_str

def T20(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    arcs = [[TRIPLE_ARC[0], "mTripleArc2"], [TRIPLE_ARC[2], "mTripleArc4"], 
            [TRIPLE_ARC[4], "mTripleArc0"]] 
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
#
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
#    t_str += "\t<path d=\"" + TRIPLE_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mTripleArc2)\" "
#    t_str += "/>\n"
#    t_str +=    "\t<path d=\"" + TRIPLE_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mTripleArc4)\" "
#    t_str += "/>\n" +\
#                "\t<path d=\"" + TRIPLE_ARC[4] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mTripleArc0)\" "
#    t_str += "/>\n"
#    t_str += "</g>\n\n"
    return t_str

def T21(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    arcs = [[TRIPLE_ARC[0], "mTripleArc4"], 
            [TRIPLE_ARC[2], "mTripleArc0"], 
            [TRIPLE_ARC[4], "mTripleArc2"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
#    t_str += "\t<path d=\"" + TRIPLE_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mTripleArc4)\" "
#    t_str += "/>\n"
#    t_str +=    "\t<path d=\"" + TRIPLE_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mTripleArc0)\" "
#    t_str += "/>\n" +\
#                "\t<path d=\"" + TRIPLE_ARC[4] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mTripleArc2)\" "
#    t_str += "/>\n"
#    t_str += "</g>\n\n"
    return t_str 
    
def T22(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    arcs = [[TRIPLE_ARC[0], None], 
            [TRIPLE_ARC[2], "mDoubleTripleArc"], 
            [TRIPLE_ARC[4], "mTripleArc0"]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
#
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
#    t_str += "\t<path d=\"" + TRIPLE_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    #t_str += "mask=\"url(#m-triple-arc-2)\" "
#    t_str += "/>\n"
#    t_str +=    "\t<path d=\"" + TRIPLE_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mDoubleTripleArc)\" "
#    t_str += "/>\n" +\
#                "\t<path d=\"" + TRIPLE_ARC[4] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mTripleArc0)\" "
#    t_str += "/>\n"
#    t_str += "</g>\n\n"
    return t_str 
    
def T23(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    arcs = [[TRIPLE_ARC[0], "mTripleArc4"], 
            [TRIPLE_ARC[2], "mDoubleTripleArc"], 
            [TRIPLE_ARC[4], None]]
    t_str = make_tile(kappa, theta, arcs, phi, stroke, stroke_width)    
#
#    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
#                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
#    t_str += "\t<path d=\"" + TRIPLE_ARC[0] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mTripleArc4)\" "
#    t_str += "/>\n"
#    t_str +=    "\t<path d=\"" + TRIPLE_ARC[2] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    t_str += "mask=\"url(#mDoubleTripleArc)\" "
#    t_str += "/>\n" +\
#                "\t<path d=\"" + TRIPLE_ARC[4] + "\" " +\
#                "stroke=\"{}\" ".format(STROKE) +\
#                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
#                "fill=\"none\" "
#    #t_str += "mask=\"url(#m-double-triple-arc)\" "
#    t_str += "/>\n"
#    t_str += "</g>\n\n"
    return t_str

    
    
      

def draw_tile(file, x_pos = 0, y_pos = 0, stroke = "black", stroke_width = 30, 
              stroke_color = "black", scale = 0.10, fill = "none", 
              fill_opacity = 1.0): 
    file.write("<use xlink:href=\"#hextile\" ")
#    file.write("x=\"{}\" ".format(int(x_pos)))
#    file.write("y=\"{}\" ".format(int(y_pos))) 
    file.write("stroke=\"{}\" ".format(stroke)) 
    file.write("stroke-width=\"{}\" ".format(int(stroke_width))) 
    file.write("stroke-color=\"{}\" ".format(stroke_color)) 
    file.write("fill=\"{}\" ".format(fill)) 
    file.write("fill-opacity=\"{:.2f}\" ".format(fill_opacity)) 
    file.write("transform =\"translate({}, {})\" ".format(x_pos, y_pos))
    file.write(" />\n")
     
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



def svg_header(): 
    svgheader = "<?xml version=\"1.0\"?>\n" +\
            "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" " +\
            "width=\"800\" height=\"800\" viewBox=\"0 0 {0} {0}\" ".format(SVG_HT)
    if(ROTATE != 0): 
        svgheader += "transform=\"rotate({}, {}, {})\" ".format(ROTATE, 400, 400)
    svgheader += ">\n" +\
            "\n" +\
            "<defs>\n" +\
            "\t<polygon id=\"hextile\" stroke=\"black\" stroke-width=\"30\" " +\
            "points=\"500,0 1500,0 2000,866 1500,1732 500,1732 0,866\" />\n" +\
            "\n"
    return svgheader


def prep_file(file): 
    file.write(svg_header())
    write_mask_dfns(file) 
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

def blank_corona(file):     
    file.write("<use xlink:href=\"#hextile\" x=\"" + str(ORIGIN_X) + "\" y=\"" + str(ORIGIN_Y) +\
                  "\" fill=\"white\"  />\n")
    
    for k in range(CORONA):
        opacity = (k + 1) / (2 * CORONA)
        for t in range (6 * (k + 1)): 
            x_pos, y_pos = corona_coords(k + 1, t, dX, dY, ORIGIN_X, ORIGIN_Y)
            draw_tile(file, x_pos, y_pos, fill = "none", fill_opacity = opacity)

    
#def sat_hex(file): 
    


svgfile = open(FILENAME + ".svg", "w") 
prep_file(svgfile)

blank_corona(svgfile)

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

svgfile.write("</svg>\n") 
svgfile.close()


        