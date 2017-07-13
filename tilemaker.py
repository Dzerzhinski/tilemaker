FILENAME = "satpar-X" 


M = 4
N = 5 

CORONA = 3


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

ORIGIN_X = (CORONA + 2) * 1250 
ORIGIN_Y = (CORONA + 1) * dY 
SVG_HT = (CORONA * 2 + 3) * dY

STROKEWIDTH = 50 
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

           
def mask_dfn(arcs, mid): 
    m_str = "\t<mask id=\"{}\" maskUnits=\"userSpaceOnUse\" >\n".format(mid) 
    m_str += "\t\t<rect height=\"{}\" width=\"{}\" fill=\"white\" />\n".format(dX, dY)
    for a in arcs:
        m_str += "\t\t<path d=\"{}\" ".format(a) 
        m_str += "stroke=\"black\" fill=\"none\" "
        m_str += "stroke-width=\"{}\" />\n" .format(5 * STROKEWIDTH)
    m_str += "\t</mask>\n\n" 
    return m_str 
        
def write_mask_dfns(file): 
    for c in range(len(C_ARC)): 
        file.write(mask_dfn([C_ARC[c]], "m-c-arc-{}".format(c)))
    for c in range(len(CAT_ARC)): 
        file.write(mask_dfn([CAT_ARC[c]], "m-cat-arc-{}".format(c)))
    for c in range(len(STRAIGHT_ARC)): 
        file.write(mask_dfn([STRAIGHT_ARC[c]], "m-straight-arc-{}".format(c)))
    for c in range(len(TRIPLE_ARC)): 
        file.write(mask_dfn([TRIPLE_ARC[c]], "m-triple-arc-{}".format(c)))
    file.write(mask_dfn([CAT_ARC[0], CAT_ARC[3]], "m-double-cat-arc")) 
    file.write(mask_dfn([TRIPLE_ARC[0], TRIPLE_ARC[4]], "m-double-triple-arc"))

                
def T1(kappa, theta, phi = 6, stroke=STROKE, stroke_width = STROKEWIDTH): 
    t1_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
                "\t<path d=\"" + C_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "</g>\n\n"
    return t1_str
    
    
def T2(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
                "\t<path d=\"" + CAT_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "</g>\n\n"
    return t_str

def T3(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
                "\t<path d=\"" + STRAIGHT_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "</g>\n\n"
    return t_str

def T4(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
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

def T5(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
                "\t<path d=\"" + C_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + C_ARC[3] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "</g>\n\n"
    return t_str
    
def T6(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
                "\t<path d=\"" + C_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + STRAIGHT_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "</g>\n\n"
    return t_str

def T7(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
                "\t<path d=\"" + C_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + CAT_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "</g>\n\n"
    return t_str

def T8(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
                "\t<path d=\"" + CAT_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + CAT_ARC[3] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "</g>\n\n"
    return t_str

def T9(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
                "\t<path d=\"" + CAT_ARC[1] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + STRAIGHT_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-cat-arc-1)\" "
    t_str += "/>\n" +\
                "</g>\n\n"
    return t_str 

def T10(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):     
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
                "\t<path d=\"" + STRAIGHT_ARC[1] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + STRAIGHT_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-straight-arc-1)\" "
    t_str += "/>\n" +\
                "</g>\n\n"
    return t_str 
    
def T11(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):     
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
                "\t<path d=\"" + STRAIGHT_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + STRAIGHT_ARC[1] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-straight-arc-2)\" "
    t_str += "/>\n" +\
                "</g>\n\n"
    return t_str 

def T12(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):     
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
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

def T13(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):     
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
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



def T14(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
                "\t<path d=\"" + C_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + C_ARC[3] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "\t<path d=\"" + STRAIGHT_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "</g>\n\n"
    return t_str

def T15(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60) +\
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
                "\t<path d=\"" + C_ARC[4] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n" +\
                "</g>\n\n"
    return t_str

def T16(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
    t_str += "\t<path d=\"" + CAT_ARC[1] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n"
    t_str +=    "\t<path d=\"" + CAT_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-cat-arc-1)\" "
    t_str += "/>\n" +\
                "\t<path d=\"" + C_ARC[5] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n"
    t_str += "</g>\n\n"
    return t_str

def T17(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
    t_str += "\t<path d=\"" + CAT_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n"
    t_str +=    "\t<path d=\"" + CAT_ARC[1] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-cat-arc-2)\" "
    t_str += "/>\n" +\
                "\t<path d=\"" + C_ARC[5] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n"
    t_str += "</g>\n\n"
    return t_str 
    
def T18(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH): 
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
    t_str += "\t<path d=\"" + CAT_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n"
    t_str +=    "\t<path d=\"" + CAT_ARC[3] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "/>\n" +\
                "\t<path d=\"" + STRAIGHT_ARC[5] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-double-cat-arc)\" "
    t_str += "/>\n"
    t_str += "</g>\n\n"
    return t_str

def T19(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
    t_str += "\t<path d=\"" + CAT_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" " +\
                "/>\n"
    t_str +=    "\t<path d=\"" + CAT_ARC[3] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-straight-arc-2)\" "
    t_str += "/>\n" +\
                "\t<path d=\"" + STRAIGHT_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-cat-arc-0)\" "
    t_str += "/>\n"
    t_str += "</g>\n\n"
    return t_str

def T20(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
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

def T21(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
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
    
def T22(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
    t_str += "\t<path d=\"" + TRIPLE_ARC[0] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    #t_str += "mask=\"url(#m-triple-arc-2)\" "
    t_str += "/>\n"
    t_str +=    "\t<path d=\"" + TRIPLE_ARC[2] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-double-triple-arc)\" "
    t_str += "/>\n" +\
                "\t<path d=\"" + TRIPLE_ARC[4] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    t_str += "mask=\"url(#m-triple-arc-0)\" "
    t_str += "/>\n"
    t_str += "</g>\n\n"
    return t_str 
    
def T23(kappa, theta, phi = 6, stroke = STROKE, stroke_width = STROKEWIDTH):
    t_str = "<g transform=\"translate({}, {}) ".format(*corona_coords(kappa, theta)) +\
                "rotate({}, 1000, 866)\" >\n".format(phi * 60)
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
    t_str += "mask=\"url(#m-double-triple-arc)\" "
    t_str += "/>\n" +\
                "\t<path d=\"" + TRIPLE_ARC[4] + "\" " +\
                "stroke=\"{}\" ".format(STROKE) +\
                "stroke-width=\"{}\" ".format(STROKEWIDTH) +\
                "fill=\"none\" "
    #t_str += "mask=\"url(#m-double-triple-arc)\" "
    t_str += "/>\n"
    t_str += "</g>\n\n"
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
            "width=\"800\" height=\"800\" viewBox=\"0 0 {0} {0}\" >".format(SVG_HT) +\
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
            draw_tile(file, x_pos, y_pos, fill = "blue", fill_opacity = opacity)
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
    


svgfile = open(FILENAME + ".svg", "w") 
prep_file(svgfile)

sat_par_cross(svgfile) 

svgfile.write("</svg>\n") 
svgfile.close()


        