# coding=UTF-8
import io
import os
import math
# import Draw
import shelve

import pandas as pd

import ezdxf

# import SoftwareLicense

# from ctypes import c_int, WINFUNCTYPE, windll
# from ctypes.wintypes import HWND, LPCWSTR, UINT

# def message_box(title, text):
#     #   ctypes.windll.user32.MessageBoxW(0, text, title, style)    
#     prototype = WINFUNCTYPE(c_int, HWND, LPCWSTR, LPCWSTR, UINT)
#     paramflags = (1, "hwnd", 0), (1, "text", text), (1, "caption", title), (1, "flags", 0)
#     MessageBox = prototype(("MessageBoxW", windll.user32), paramflags)   
#     MessageBox()


def get_Total_ReBarshear(StringData):
    V1, V2 = StringData.split('+')
    return int(int(V1)+int(V2))


def to_binary_data(doc):
    '''
    1. 需將DXF檔案寫入文字流,使用StringIO物件將其寫入字串。StringIO.getvalue()傳回一個 unicode 字串
    2. DXF R2007 (AC1021)及更高版本的文字編碼始終為'utf8'，對於舊版 DXF,所需編碼儲存在中Drawing.encoding
    3. https://stackoverflow.com/questions/59363895/how-can-i-offer-an-ezdxf-download-in-a-flask-app
    4. doc為ezdxf的產物 
    '''

    stream = io.StringIO()
    doc.write(stream)
    dxf_data = stream.getvalue()
    stream.close()
    enc = 'utf-8' if doc.dxfversion >= 'AC1021' else doc.encoding
    return dxf_data.encode(enc)


def drawing_Rectangular(ID, Name, X0, Y0, RebarType, Cover, MBDia, SBDia, TBDia, MBName, SBName, TBName, SBSpace1, SBSpace2, Dx, Dy, Nx, Ny, TNx, TNy, BoxWid, BoxDep, Scale, msp):

    Nx1 =  int(Nx.split('+')[0])
    Nx2 =  int(Nx.split('+')[1])

    Ny1 =  int(Ny.split('+')[0])
    Ny2 =  int(Ny.split('+')[1])


    # strTEXT = ''

    if TNy > (Nx1-2) or TNx > (Ny1-2):

        msp.add_text(
            'nx < tny Or ny < tnx, Please check input data',
            height=50/Scale,
            dxfattribs={"style": "Standard", "layer": "Default"}
        ).set_placement((0, -10), align=ezdxf.enums.TextEntityAlignment.MIDDLE_LEFT)

    else:
        #   RC Column

        points = []
        # （x, y, start_width, end_width, bulge）
        points.append((X0 - 0.5 * Dx, Y0 - 0.5 * Dy, 0, 0, 0))
        points.append((X0 + 0.5 * Dx, Y0 - 0.5 * Dy, 0, 0, 0))
        points.append((X0 + 0.5 * Dx, Y0 + 0.5 * Dy, 0, 0, 0))
        points.append((X0 - 0.5 * Dx, Y0 + 0.5 * Dy, 0, 0, 0))
        msp.add_lwpolyline(points, dxfattribs={"layer": "Concrete"}).close(state=True)
        

        #   Stirrup
        anchor_factor = 6.0

        points = []
        # （x, y, start_width, end_width, bulge）
        points.append((X0 - 0.5 * Dx + Cover + SBDia + 0.5 * MBDia, Y0 - 0.5 * Dy + Cover + 0.5 * SBDia, 0, 0, 0))
        points.append((X0 + 0.5 * Dx - Cover - SBDia - 0.5 * MBDia, Y0 - 0.5 * Dy + Cover + 0.5 * SBDia, 0, 0, math.tan(math.pi / 180 * 90 / 4)))
        points.append((X0 + 0.5 * Dx - Cover - 0.5 * SBDia, Y0 - 0.5 * Dy + Cover + SBDia + 0.5 * MBDia, 0, 0, 0))
        points.append((X0 + 0.5 * Dx - Cover - 0.5 * SBDia, Y0 + 0.5 * Dy - Cover - SBDia - 0.5 * MBDia, 0, 0, math.tan(math.pi / 180 * 90 / 4)))
        points.append((X0 + 0.5 * Dx - Cover - SBDia - 0.5 * MBDia, Y0 + 0.5 * Dy - Cover - 0.5 * SBDia, 0, 0, 0))
        points.append((X0 - 0.5 * Dx + Cover + SBDia + 0.5 * MBDia, Y0 + 0.5 * Dy - Cover - 0.5 * SBDia, 0, 0, math.tan(math.pi / 180 * 90 / 4)))
        points.append((X0 - 0.5 * Dx + Cover + 0.5 * SBDia, Y0 + 0.5 * Dy - Cover - SBDia - 0.5 * MBDia, 0, 0, 0))
        points.append((X0 - 0.5 * Dx + Cover + 0.5 * SBDia, Y0 - 0.5 * Dy + Cover + SBDia + 0.5 * MBDia + 0.707 * SBDia, 0, 0, 0))
        points.append((X0 - 0.5 * Dx + Cover + 0.5 * SBDia + SBDia * anchor_factor * 0.707, Y0 - 0.5 * Dy + Cover + SBDia + 0.5 * SBDia + 0.707 * SBDia + SBDia * anchor_factor * 0.707, 0, 0, 0))
        points.append((X0 - 0.5 * Dx + Cover + 0.5 * SBDia, Y0 - 0.5 * Dy + Cover + SBDia + 0.5 * MBDia + 0.707 * SBDia, 0, 0, 0))
        points.append((X0 - 0.5 * Dx + Cover + 0.5 * SBDia, Y0 - 0.5 * Dy + Cover + SBDia + 0.5 * MBDia, 0, 0, math.tan(math.pi / 180 * 90 / 4)))
        points.append((X0 - 0.5 * Dx + Cover + SBDia + 0.5 * MBDia, Y0 - 0.5 * Dy + Cover + 0.5 * SBDia, 0, 0, 0))
        points.append((X0 - 0.5 * Dx + Cover + SBDia + 0.5 * MBDia + 0.707 * SBDia, Y0 - 0.5 * Dy + Cover + 0.5 * SBDia, 0, 0, 0))
        points.append((X0 - 0.5 * Dx + Cover + SBDia + 0.5 * MBDia + 0.707 * SBDia + SBDia * anchor_factor * 0.707, Y0 - 0.5 * Dy + Cover + 0.5 * SBDia + SBDia * anchor_factor * 0.707, 0, 0, 0))
        msp.add_lwpolyline(points, dxfattribs={"layer": "Stirrup"}).close(state=False)
        


        #   Main Bar
        if RebarType == 1:
            for i in range(Nx1):
                tmpX = (X0 - 0.5 * Dx + Cover + SBDia + MBDia / 2) + (i) * (Dx - 2 * Cover - 2 * SBDia - MBDia) / (Nx1 - 1)
                tmpY = Y0 - 0.5 * Dy + Cover + SBDia + MBDia / 2
                points = []
                for j in range(48):
                    P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
                    P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
                    points.append((P1x, P1y))
                hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
                hatch.paths.add_polyline_path(points, is_closed=True)
                

                tmpX = (X0 - 0.5 * Dx + Cover + SBDia + MBDia / 2) + (i) * (Dx - 2 * Cover - 2 * SBDia - MBDia) / (Nx1 - 1)
                tmpY = Y0 + 0.5 * Dy - Cover - SBDia - MBDia / 2
                points = []
                for j in range(48):
                    P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
                    P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
                    points.append((P1x, P1y))
                hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
                hatch.paths.add_polyline_path(points, is_closed=True)


            for i in range(Nx2):
                tmpX = (X0 - 0.5 * Dx + Cover + SBDia + MBDia / 2) + round((i+1)*Nx1/(Nx2+1)) * (Dx - 2 * Cover - 2 * SBDia - MBDia) / (Nx1 - 1)
                tmpY = Y0 - 0.5 * Dy + Cover + SBDia + MBDia / 2  + MBDia
                points = []
                for j in range(48):
                    P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
                    P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
                    points.append((P1x, P1y))
                hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
                hatch.paths.add_polyline_path(points, is_closed=True)


                tmpX = (X0 - 0.5 * Dx + Cover + SBDia + MBDia / 2) + round((i+1)*Nx1/(Nx2+1)) * (Dx - 2 * Cover - 2 * SBDia - MBDia) / (Nx1 - 1)
                tmpY = Y0 + 0.5 * Dy - Cover - SBDia - MBDia / 2  - MBDia
                points = []
                for j in range(48):
                    P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
                    P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
                    points.append((P1x, P1y))
                hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
                hatch.paths.add_polyline_path(points, is_closed=True)





            for i in range(1, Ny1 - 1):
                tmpX = (X0 - 0.5 * Dx + Cover + SBDia + MBDia / 2)
                tmpY = (Y0 - 0.5 * Dy + Cover + SBDia + MBDia / 2) + i * (Dy - 2 * Cover - 2 * SBDia - MBDia) / (Ny1 - 1)
                points = []
                for j in range(48):
                    P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
                    P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
                    points.append((P1x, P1y))
                hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
                hatch.paths.add_polyline_path(points, is_closed=True)


                tmpX = (X0 + 0.5 * Dx - Cover - SBDia - MBDia / 2)
                tmpY = (Y0 - 0.5 * Dy + Cover + SBDia + MBDia / 2) + i * (Dy - 2 * Cover - 2 * SBDia - MBDia) / (Ny1 - 1)
                points = []
                for j in range(48):
                    P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
                    P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
                    points.append((P1x, P1y))
                hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
                hatch.paths.add_polyline_path(points, is_closed=True)


            for i in range(Ny2):
                tmpX = (X0 - 0.5 * Dx + Cover + SBDia + MBDia / 2 + MBDia)
                tmpY = (Y0 - 0.5 * Dy + Cover + SBDia + MBDia / 2) + round((i+1)*Ny1/(Ny2+1)) * (Dy - 2 * Cover - 2 * SBDia - MBDia) / (Ny1 - 1)
                points = []
                for j in range(48):
                    P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
                    P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
                    points.append((P1x, P1y))
                hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
                hatch.paths.add_polyline_path(points, is_closed=True)


                tmpX = (X0 + 0.5 * Dx - Cover - SBDia - MBDia / 2 - MBDia)
                tmpY = (Y0 - 0.5 * Dy + Cover + SBDia + MBDia / 2) + round((i+1)*Ny1/(Ny2+1)) * (Dy - 2 * Cover - 2 * SBDia - MBDia) / (Ny1 - 1)
                points = []
                for j in range(48):
                    P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
                    P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
                    points.append((P1x, P1y))
                hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
                hatch.paths.add_polyline_path(points, is_closed=True)


        #   Tie Bar for Dir-X
        tmpCen = (Ny1 + 1) / 2
        tmpMN = (Ny1 - 2)
        tmpTN = TNx
        tmpSS = (Dy - 2 * Cover - 2 * SBDia - MBDia) / (Ny1 - 1)
        tmpDelta = (tmpMN + 1) / (tmpTN + 1)

        for i in range(tmpTN):
            tmpN1 = round(1 + (i + 1) * tmpDelta)
            
            if tmpN1 <= tmpCen:
                if i % 2 == 0:
                    tmpType = 1
                else:
                    tmpType = 2
            elif tmpN1 > tmpCen:
                if i % 2 == 0:
                    tmpType = 3
                else:
                    tmpType = 4

            tmpX1 = X0 - 0.5 * Dx + Cover + SBDia + MBDia / 2
            tmpY1 = Y0 - 0.5 * Dy + Cover + SBDia + MBDia / 2 + (tmpN1 - 1) * tmpSS
            tmpX2 = X0 + 0.5 * Dx - Cover - SBDia - MBDia / 2
            tmpY2 = Y0 - 0.5 * Dy + Cover + SBDia + MBDia / 2 + (tmpN1 - 1) * tmpSS

            points = draw_Tie_Bar(tmpType, tmpX1, tmpY1, tmpX2, tmpY2, MBDia, TBDia)
            # （x, y, start_width, end_width, bulge）
            msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)


        #   Tie Bar for Dir-Y
        tmpCen = (Nx1 + 1) / 2
        tmpMN = (Nx1 - 2)
        tmpTN = TNy
        tmpSS = (Dx - 2 * Cover - 2 * SBDia - MBDia) / (Nx1 - 1)
        tmpDelta = (tmpMN + 1) / (tmpTN + 1)

        for i in range(tmpTN):
            tmpN1 = round(1 + (i + 1) * tmpDelta)
            
            if tmpN1 <= tmpCen:
                if i % 2 == 0:
                    tmpType = 5
                else:
                    tmpType = 6
            elif tmpN1 > tmpCen:
                if i % 2 == 0:
                    tmpType = 7
                else:
                    tmpType = 8

            tmpX1 = X0 - 0.5 * Dx + Cover + SBDia + MBDia / 2 + (tmpN1 - 1) * tmpSS
            tmpY1 = Y0 - 0.5 * Dy + Cover + SBDia + MBDia / 2
            tmpX2 = X0 - 0.5 * Dx + Cover + SBDia + MBDia / 2 + (tmpN1 - 1) * tmpSS
            tmpY2 = Y0 + 0.5 * Dy - Cover - SBDia - MBDia / 2

            points = draw_Tie_Bar(tmpType, tmpX1, tmpY1, tmpX2, tmpY2, MBDia, TBDia)
            # （x, y, start_width, end_width, bulge）
            msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)
            



        #   Sec. Infomation
        msp.add_text(
            '{0}X{1}'.format(round(Dx), round(Dy)),
            height=90/Scale,
            dxfattribs={"style": "Standard", "layer": "Text"}
        ).set_placement((X0, Y0 - BoxDep / 2 - 75/Scale), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)


        tmpX = X0 - 450/Scale
        tmpY = Y0 - BoxDep / 2 - 225/Scale
        points = []
        for j in range(48):
            P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
            P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
            points.append((P1x, P1y))
        hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
        hatch.paths.add_polyline_path(points, is_closed=True)


        msp.add_text(
            '{0}-{1}'.format(round((Nx1+Nx2) * 2 + (Ny1+Ny2) * 2 - 4), MBName),
            height=90/Scale,
            dxfattribs={"style": "Standard", "layer": "Text"}
        ).set_placement((X0, Y0 - BoxDep / 2 - 225/Scale), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)



        points = []
        # （x, y, start_width, end_width, bulge）
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 375/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale + 45/Scale                        , Y0 - BoxDep / 2 - 375/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale + 45/Scale                        , Y0 - BoxDep / 2 - 375/Scale + 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 375/Scale + 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 375/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale             , Y0 - BoxDep / 2 - 375/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale + 15/Scale  , Y0 - BoxDep / 2 - 375/Scale - 45/Scale + 15/Scale             , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale             , Y0 - BoxDep / 2 - 375/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 375/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 375/Scale - 45/Scale + 15/Scale             , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale             , Y0 - BoxDep / 2 - 375/Scale - 45/Scale + 15/Scale + 15/Scale  , 0, 0, 0))
        msp.add_lwpolyline(points, dxfattribs={"layer": "Stirrup"}).close(state=False)
        points = []
        # （x, y, start_width, end_width, bulge）
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 525/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale + 45/Scale                        , Y0 - BoxDep / 2 - 525/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale + 45/Scale                        , Y0 - BoxDep / 2 - 525/Scale + 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 525/Scale + 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 525/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale             , Y0 - BoxDep / 2 - 525/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale + 15/Scale  , Y0 - BoxDep / 2 - 525/Scale - 45/Scale + 15/Scale             , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale             , Y0 - BoxDep / 2 - 525/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 525/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 525/Scale - 45/Scale + 15/Scale             , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale             , Y0 - BoxDep / 2 - 525/Scale - 45/Scale + 15/Scale + 15/Scale  , 0, 0, 0))
        msp.add_lwpolyline(points, dxfattribs={"layer": "Stirrup"}).close(state=False)
        points = []
        # （x, y, start_width, end_width, bulge）
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 675/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale + 45/Scale                        , Y0 - BoxDep / 2 - 675/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale + 45/Scale                        , Y0 - BoxDep / 2 - 675/Scale + 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 675/Scale + 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 675/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale             , Y0 - BoxDep / 2 - 675/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale + 15/Scale  , Y0 - BoxDep / 2 - 675/Scale - 45/Scale + 15/Scale             , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale             , Y0 - BoxDep / 2 - 675/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 675/Scale - 45/Scale                        , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale                        , Y0 - BoxDep / 2 - 675/Scale - 45/Scale + 15/Scale             , 0, 0, 0))
        points.append((X0 - 175/Scale - 45/Scale + 15/Scale             , Y0 - BoxDep / 2 - 675/Scale - 45/Scale + 15/Scale + 15/Scale  , 0, 0, 0))
        msp.add_lwpolyline(points, dxfattribs={"layer": "Stirrup"}).close(state=False)




        points = []
        # （x, y, start_width, end_width, bulge）
        points.append((X0 - 175/Scale + 440/Scale - 15/Scale    , Y0 - BoxDep / 2 - 375/Scale + 45/Scale            , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale               , Y0 - BoxDep / 2 - 375/Scale + 45/Scale            , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale               , Y0 - BoxDep / 2 - 375/Scale - 45/Scale            , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale - 15/Scale    , Y0 - BoxDep / 2 - 375/Scale - 45/Scale + 15/Scale , 0, 0, 0))
        msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)
        points = []
        # （x, y, start_width, end_width, bulge）
        points.append((X0 - 175/Scale + 440/Scale - 15/Scale    , Y0 - BoxDep / 2 - 525/Scale + 45/Scale            , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale               , Y0 - BoxDep / 2 - 525/Scale + 45/Scale            , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale               , Y0 - BoxDep / 2 - 525/Scale - 45/Scale            , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale - 15/Scale    , Y0 - BoxDep / 2 - 525/Scale - 45/Scale + 15/Scale , 0, 0, 0))
        msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)
        points = []
        # （x, y, start_width, end_width, bulge）
        points.append((X0 - 175/Scale + 440/Scale - 15/Scale    , Y0 - BoxDep / 2 - 675/Scale + 45/Scale            , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale               , Y0 - BoxDep / 2 - 675/Scale + 45/Scale            , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale               , Y0 - BoxDep / 2 - 675/Scale - 45/Scale            , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale - 15/Scale    , Y0 - BoxDep / 2 - 675/Scale - 45/Scale + 15/Scale , 0, 0, 0))
        msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)





        points = []
        # （x, y, start_width, end_width, bulge）
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 375/Scale - 15/Scale    , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 375/Scale               , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale + 45/Scale            , Y0 - BoxDep / 2 - 375/Scale               , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale + 45/Scale - 15/Scale , Y0 - BoxDep / 2 - 375/Scale - 15/Scale    , 0, 0, 0))
        msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)
        points = []
        # （x, y, start_width, end_width, bulge）
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 525/Scale - 15/Scale    , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 525/Scale               , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale + 45/Scale            , Y0 - BoxDep / 2 - 525/Scale               , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale + 45/Scale - 15/Scale , Y0 - BoxDep / 2 - 525/Scale - 15/Scale    , 0, 0, 0))
        msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)
        points = []
        # （x, y, start_width, end_width, bulge）
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 675/Scale - 15/Scale    , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 675/Scale               , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale + 45/Scale            , Y0 - BoxDep / 2 - 675/Scale               , 0, 0, 0))
        points.append((X0 - 175/Scale + 440/Scale + 440/Scale + 45/Scale - 15/Scale , Y0 - BoxDep / 2 - 675/Scale - 15/Scale    , 0, 0, 0))
        msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)




        string_info = [
            [X0 - 550/Scale , Y0 - BoxDep / 2 - 375/Scale, '{0}@{1} ('.format(SBName, round(SBSpace1))], 
            [X0 +  30/Scale , Y0 - BoxDep / 2 - 375/Scale, '+{0:>2}'.format(round(TNy))               ], 
            [X0 + 450/Scale , Y0 - BoxDep / 2 - 375/Scale, '+{0:>2}'.format(round(TNx))               ], 
            [X0 + 830/Scale , Y0 - BoxDep / 2 - 375/Scale, ')'                                        ], 
            [X0 - 550/Scale , Y0 - BoxDep / 2 - 525/Scale, '{0}@{1} ('.format(SBName, round(SBSpace2))], 
            [X0 +  30/Scale , Y0 - BoxDep / 2 - 525/Scale, '+{0:>2}'.format(round(TNy))               ], 
            [X0 + 450/Scale , Y0 - BoxDep / 2 - 525/Scale, '+{0:>2}'.format(round(TNx))               ], 
            [X0 + 830/Scale , Y0 - BoxDep / 2 - 525/Scale, ')'                                        ], 
            [X0 - 550/Scale , Y0 - BoxDep / 2 - 675/Scale, '{0}@{1} ('.format(SBName, round(SBSpace1))], 
            [X0 +  30/Scale , Y0 - BoxDep / 2 - 675/Scale, '+{0:>2}'.format(round(TNy))               ], 
            [X0 + 450/Scale , Y0 - BoxDep / 2 - 675/Scale, '+{0:>2}'.format(round(TNx))               ], 
            [X0 + 830/Scale , Y0 - BoxDep / 2 - 675/Scale, ')'                                        ]
        ]

        for element in string_info:
            msp.add_text(
                element[2],
                height=90/Scale,
                dxfattribs={"style": "Standard", "layer": "Text"}
            ).set_placement((element[0], element[1]), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    return msp



def drawing_Circle(ID, Name, X0, Y0, RebarType, Cover, MBDia, SBDia, TBDia, MBName, SBName, TBName, SS_CR, SS_nCR, Dia, RBNo, SN_CR, SN_nCR, BoxWid, BoxDep, Scale, msp):
# (ID, Name, X0, Y0, RebarType, Cover, MBDia, SBDia, TBDia, MBName, SBName, TBName, SBSpace1, SBSpace2, Dx, Dy, Nx, Ny, TNx, TNy, BoxWid, BoxDep, Scale)

    RN1, RN2 = RBNo.split('+')
    RN1 = int(RN1)
    RN2 = int(RN2)

    # strTEXT = ''

    #   RC Column
    target_point = ezdxf.math.Vec2(X0, Y0)
    msp.add_circle(
        target_point, radius=Dia/2, dxfattribs={"layer": "Concrete"}
    )
    
    #   Stirrup
    target_point = ezdxf.math.Vec2(X0, Y0)
    msp.add_circle(
        target_point, radius=(Dia-2*Cover-SBDia)/2, dxfattribs={"layer": "Stirrup"}
    )

    #   Main Bar
    radius1 = (Dia-2*Cover-2*SBDia-MBDia)/2
    radius2 = (Dia-2*Cover-2*SBDia-2*MBDia-MBDia)/2

    if RN1:
        deltaThita1 = 2*math.pi / RN1
        for i in range(RN1):
            tmpThita = 0 + i * deltaThita1
            tmpX = X0 + radius1 * math.cos(tmpThita)
            tmpY = Y0 + radius1 * math.sin(tmpThita)
            points = []
            for j in range(48):
                P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
                P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
                points.append((P1x, P1y))
            hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
            hatch.paths.add_polyline_path(points, is_closed=True)

    if RN2:
        deltaThita2 = 2*math.pi / RN2
        for i in range(RN2):

            tmpThita = 0 + round(i * deltaThita2 / deltaThita1) * deltaThita1
            tmpX = X0 + radius2 * math.cos(tmpThita)
            tmpY = Y0 + radius2 * math.sin(tmpThita)
            points = []
            for j in range(48):
                P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
                P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
                points.append((P1x, P1y))
            hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
            hatch.paths.add_polyline_path(points, is_closed=True)


    #   Tie Bar for Dir-X
    tmpX1 = X0 - radius1
    tmpY1 = Y0
    tmpX2 = X0 + radius1
    tmpY2 = Y0

    points = draw_Tie_Bar(1, tmpX1, tmpY1, tmpX2, tmpY2, MBDia, TBDia)
    # （x, y, start_width, end_width, bulge）
    msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)


    #   Tie Bar for Dir-Y
    tmpX1 = X0
    tmpY1 = Y0 - radius1
    tmpX2 = X0
    tmpY2 = Y0 + radius1

    points = draw_Tie_Bar(5, tmpX1, tmpY1, tmpX2, tmpY2, MBDia, TBDia)
    # （x, y, start_width, end_width, bulge）
    msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)




    #   Sec. Infomation
    msp.add_text(
        'D={0}'.format(round(Dia)),
        height=90/Scale,
        dxfattribs={"style": "Standard", "layer": "Text"}
    ).set_placement((X0, Y0 - BoxDep / 2 - 75/Scale), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)


    tmpX = X0 - 450/Scale
    tmpY = Y0 - BoxDep / 2 - 225/Scale
    points = []
    for j in range(48):
        P1x = tmpX + float(MBDia/2) * math.cos(j * 360/48 * math.pi / 180)
        P1y = tmpY + float(MBDia/2) * math.sin(j * 360/48 * math.pi / 180)
        points.append((P1x, P1y))
    hatch = msp.add_hatch(color=-1, dxfattribs={"layer": "MainBar"})
    hatch.paths.add_polyline_path(points, is_closed=True)


    msp.add_text(
        '{0}-{1}'.format(RN1 + RN2, MBName),
        height=90/Scale,
        dxfattribs={"style": "Standard", "layer": "Text"}
    ).set_placement((X0, Y0 - BoxDep / 2 - 225/Scale), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)




    target_point = ezdxf.math.Vec2((X0 - 175/Scale - 45/Scale + 200/Scale), (Y0 - BoxDep / 2 - 375/Scale))
    msp.add_circle(target_point, radius=(60/Scale), dxfattribs={"layer": "Stirrup"})

    target_point = ezdxf.math.Vec2((X0 - 175/Scale - 45/Scale + 200/Scale), (Y0 - BoxDep / 2 - 525/Scale))
    msp.add_circle(target_point, radius=(60/Scale), dxfattribs={"layer": "Stirrup"})

    target_point = ezdxf.math.Vec2((X0 - 175/Scale - 45/Scale + 200/Scale), (Y0 - BoxDep / 2 - 675/Scale))
    msp.add_circle(target_point, radius=(60/Scale), dxfattribs={"layer": "Stirrup"})
    



    points = []
    # （x, y, start_width, end_width, bulge）
    points.append((X0 - 175/Scale + 590/Scale - 15/Scale    , Y0 - BoxDep / 2 - 375/Scale + 45/Scale            , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale               , Y0 - BoxDep / 2 - 375/Scale + 45/Scale            , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale               , Y0 - BoxDep / 2 - 375/Scale - 45/Scale            , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale - 15/Scale    , Y0 - BoxDep / 2 - 375/Scale - 45/Scale + 15/Scale , 0, 0, 0))
    msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)
    points = []
    # （x, y, start_width, end_width, bulge）
    points.append((X0 - 175/Scale + 590/Scale - 15/Scale    , Y0 - BoxDep / 2 - 525/Scale + 45/Scale            , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale               , Y0 - BoxDep / 2 - 525/Scale + 45/Scale            , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale               , Y0 - BoxDep / 2 - 525/Scale - 45/Scale            , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale - 15/Scale    , Y0 - BoxDep / 2 - 525/Scale - 45/Scale + 15/Scale , 0, 0, 0))
    msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)
    points = []
    # （x, y, start_width, end_width, bulge）
    points.append((X0 - 175/Scale + 590/Scale - 15/Scale    , Y0 - BoxDep / 2 - 675/Scale + 45/Scale            , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale               , Y0 - BoxDep / 2 - 675/Scale + 45/Scale            , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale               , Y0 - BoxDep / 2 - 675/Scale - 45/Scale            , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale - 15/Scale    , Y0 - BoxDep / 2 - 675/Scale - 45/Scale + 15/Scale , 0, 0, 0))
    msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)




    points = []
    # （x, y, start_width, end_width, bulge）
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 375/Scale - 15/Scale    , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 375/Scale               , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale + 45/Scale            , Y0 - BoxDep / 2 - 375/Scale               , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale + 45/Scale - 15/Scale , Y0 - BoxDep / 2 - 375/Scale - 15/Scale    , 0, 0, 0))
    msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)
    points = []
    # （x, y, start_width, end_width, bulge）
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 525/Scale - 15/Scale    , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 525/Scale               , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale + 45/Scale            , Y0 - BoxDep / 2 - 525/Scale               , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale + 45/Scale - 15/Scale , Y0 - BoxDep / 2 - 525/Scale - 15/Scale    , 0, 0, 0))
    msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)
    points = []
    # （x, y, start_width, end_width, bulge）
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 675/Scale - 15/Scale    , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale - 45/Scale            , Y0 - BoxDep / 2 - 675/Scale               , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale + 45/Scale            , Y0 - BoxDep / 2 - 675/Scale               , 0, 0, 0))
    points.append((X0 - 175/Scale + 590/Scale + 440/Scale + 45/Scale - 15/Scale , Y0 - BoxDep / 2 - 675/Scale - 15/Scale    , 0, 0, 0))
    msp.add_lwpolyline(points, dxfattribs={"layer": "Tie"}).close(state=False)



    string_info = [
        [X0 - 550/Scale , Y0 - BoxDep / 2 - 375/Scale, '{0}-{1}@{2} ( {3}'.format(SN_CR, SBName, round(SS_CR), SN_CR)   ], 
        [X0 +  30/Scale + 150/Scale , Y0 - BoxDep / 2 - 375/Scale, '+{0:>2}'.format(round(1))                           ], 
        [X0 + 450/Scale + 150/Scale , Y0 - BoxDep / 2 - 375/Scale, '+{0:>2}'.format(round(1))                           ], 
        [X0 + 830/Scale + 150/Scale , Y0 - BoxDep / 2 - 375/Scale, ')'                                                  ], 
        [X0 - 550/Scale , Y0 - BoxDep / 2 - 525/Scale, '{0}-{1}@{2} ( {3}'.format(SN_nCR, SBName, round(SS_nCR), SN_nCR)], 
        [X0 +  30/Scale + 150/Scale , Y0 - BoxDep / 2 - 525/Scale, '+{0:>2}'.format(round(1))                           ], 
        [X0 + 450/Scale + 150/Scale , Y0 - BoxDep / 2 - 525/Scale, '+{0:>2}'.format(round(1))                           ], 
        [X0 + 830/Scale + 150/Scale , Y0 - BoxDep / 2 - 525/Scale, ')'                                                  ], 
        [X0 - 550/Scale , Y0 - BoxDep / 2 - 675/Scale, '{0}-{1}@{2} ( {3}'.format(SN_CR, SBName, round(SS_CR), SN_CR)   ], 
        [X0 +  30/Scale + 150/Scale , Y0 - BoxDep / 2 - 675/Scale, '+{0:>2}'.format(round(1))                           ], 
        [X0 + 450/Scale + 150/Scale , Y0 - BoxDep / 2 - 675/Scale, '+{0:>2}'.format(round(1))                           ], 
        [X0 + 830/Scale + 150/Scale , Y0 - BoxDep / 2 - 675/Scale, ')'                                                  ]
    ]

    for element in string_info:
        msp.add_text(
            element[2],
            height=90/Scale,
            dxfattribs={"style": "Standard", "layer": "Text"}
        ).set_placement((element[0], element[1]), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)


    return msp




def table(BoxWid, BoxDep, FloorList, ColumnList, Scale, msp):

    FloorNo = len(FloorList)
    ColumnNo = len(ColumnList)

    X1 = 0 - BoxWid / 2 - 700/Scale
    Y1 = 0 + BoxDep / 2 + 400/Scale
    X2 = (ColumnNo - 0.5) * BoxWid
    Y2 = 0 + BoxDep / 2 + 400/Scale
    msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

    X1 = 0 - BoxWid / 2 - 700/Scale
    Y1 = 0 + BoxDep / 2
    X2 = (ColumnNo - 0.5) * BoxWid
    Y2 = 0 + BoxDep / 2
    msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

    X1 = 0 - BoxWid / 2 - 700/Scale
    Y1 = 0 + BoxDep / 2 + 400/Scale
    X2 = 0 - BoxWid / 2 - 700/Scale
    Y2 = 0 + BoxDep / 2 - FloorNo * (BoxDep + 750/Scale)
    msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

    X1 = 0 - BoxWid / 2
    Y1 = 0 + BoxDep / 2 + 400/Scale
    X2 = 0 - BoxWid / 2
    Y2 = 0 + BoxDep / 2 - FloorNo * (BoxDep + 750/Scale)
    msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

    X1 = 0 - BoxWid / 2 - 700/Scale
    Y1 = 0 + BoxDep / 2 + 400/Scale
    X2 = 0 - BoxWid / 2
    Y2 = 0 + BoxDep / 2
    msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

    X1 = 0 - BoxWid / 2 - 250/Scale
    Y1 = 0 + BoxDep / 2 + 300/Scale
    msp.add_text(
        '柱',
        height=90/Scale,
        dxfattribs={"style": "Standard", "layer": "Text"}
    ).set_placement((X1, Y1), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    X1 = 0 - BoxWid / 2 - 450/Scale
    Y1 = 0 + BoxDep / 2 + 100/Scale
    msp.add_text(
        '樓層',
        height=90/Scale,
        dxfattribs={"style": "Standard", "layer": "Text"}
    ).set_placement((X1, Y1), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)


    for i in range(ColumnNo):
        X1 = 0 + BoxWid * (i + 0.5)
        Y1 = 0 + BoxDep / 2 + 400/Scale
        X2 = 0 + BoxWid * (i + 0.5)
        Y2 = 0 + BoxDep / 2 - FloorNo * (BoxDep + 750/Scale)
        msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

        X1 = 0 + BoxWid * i
        Y1 = 0 + BoxDep / 2 + 200/Scale
        msp.add_text(
            ColumnList[i],
            height=90/Scale,
            dxfattribs={"style": "Standard", "layer": "Text"}
        ).set_placement((X1, Y1), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)


    for i in range(FloorNo):
        X1 = 0 - BoxWid / 2 - 350/Scale
        Y1 = 0 - (BoxDep + 750/Scale) * i
        msp.add_text(
            FloorList[i],
            height=90/Scale,
            dxfattribs={"style": "Standard", "layer": "Text"}
        ).set_placement((X1, Y1), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

        X1 = 0 - BoxWid / 2 - 350/Scale
        Y1 = 0 - (BoxDep + 750/Scale) * i - BoxDep / 2 - 75/Scale
        msp.add_text(
            '斷面',
            height=90/Scale,
            dxfattribs={"style": "Standard", "layer": "Text"}
        ).set_placement((X1, Y1), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

        X1 = 0 - BoxWid / 2 - 350/Scale
        Y1 = 0 - (BoxDep + 750/Scale) * i - BoxDep / 2 - 225/Scale
        msp.add_text(
            '鋼筋',
            height=90/Scale,
            dxfattribs={"style": "Standard", "layer": "Text"}
        ).set_placement((X1, Y1), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

        X1 = 0 - BoxWid / 2 - 350/Scale
        Y1 = 0 - (BoxDep + 750/Scale) * i - BoxDep / 2 - 375/Scale
        msp.add_text(
            '圍束區',
            height=90/Scale,
            dxfattribs={"style": "Standard", "layer": "Text"}
        ).set_placement((X1, Y1), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

        X1 = 0 - BoxWid / 2 - 350/Scale
        Y1 = 0 - (BoxDep + 750/Scale) * i - BoxDep / 2 - 525/Scale
        msp.add_text(
            '中央區',
            height=90/Scale,
            dxfattribs={"style": "Standard", "layer": "Text"}
        ).set_placement((X1, Y1), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

        X1 = 0 - BoxWid / 2 - 350/Scale
        Y1 = 0 - (BoxDep + 750/Scale) * i - BoxDep / 2 - 675/Scale
        msp.add_text(
            '接頭區',
            height=90/Scale,
            dxfattribs={"style": "Standard", "layer": "Text"}
        ).set_placement((X1, Y1), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

        X1 = 0 - BoxWid / 2 - 700/Scale
        Y1 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 0
        X2 = (ColumnNo - 0.5) * BoxWid
        Y2 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 0
        msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

        X1 = 0 - BoxWid / 2 - 700/Scale
        Y1 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 150/Scale
        X2 = (ColumnNo - 0.5) * BoxWid
        Y2 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 150/Scale
        msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

        X1 = 0 - BoxWid / 2 - 700/Scale
        Y1 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 300/Scale
        X2 = (ColumnNo - 0.5) * BoxWid
        Y2 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 300/Scale
        msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

        X1 = 0 - BoxWid / 2 - 700/Scale
        Y1 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 450/Scale
        X2 = (ColumnNo - 0.5) * BoxWid
        Y2 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 450/Scale
        msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

        X1 = 0 - BoxWid / 2 - 700/Scale
        Y1 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 600/Scale
        X2 = (ColumnNo - 0.5) * BoxWid
        Y2 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 600/Scale
        msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

        X1 = 0 - BoxWid / 2 - 700/Scale
        Y1 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 750/Scale
        X2 = (ColumnNo - 0.5) * BoxWid
        Y2 = 0 - (BoxDep) * (i + 0.5) - 750/Scale * i - 750/Scale
        msp.add_line((X1, Y1), (X2, Y2), dxfattribs={"layer": "Default"})

    return msp


def draw_Tie_Bar(Type, X1, Y1, X2, Y2, MBDia, TBDia, F1=1.5, F2=6):

    C2C = math.sqrt((X1 - X2)**2 + (Y1 - Y2)**2)

    Point = []
    Point.append([X1 - 0.5 * MBDia - F1 * TBDia, Y1 - 0.5 * MBDia - F1 * TBDia + F2 * TBDia, 0])
    Point.append([X1 - 0.5 * MBDia - F1 * TBDia, Y1, math.tan(math.pi / 180 * 90 / 4)])
    Point.append([X1, Y1 - 0.5 * MBDia - F1 * TBDia, 0])
    Point.append([X1 + C2C, Y1 - 0.5 * MBDia - F1 * TBDia, math.tan(math.pi / 180 * 135 / 4)])
    Point.append([X1 + C2C + (0.5 * MBDia + F1 * TBDia) * (1 / math.sqrt(2)), Y1 - 0.5 * MBDia - F1 * TBDia + (0.5 * MBDia + F1 * TBDia) * (1 + (1 / math.sqrt(2))), 0])
    Point.append([X1 + C2C + (0.5 * MBDia + F1 * TBDia) * (1 / math.sqrt(2)) - F2 * TBDia * (1 / math.sqrt(2)), Y1 - 0.5 * MBDia - F1 * TBDia + (0.5 * MBDia + F1 * TBDia) * (1 + (1 / math.sqrt(2))) + F2 * TBDia * (1 / math.sqrt(2)), 0])

    tmpPoint = []
    DXFpoint = []
    delta_X = 0.0
    delta_Y = 0.0

    if Type == 1:
        for i in range(len(Point)):
            tmpPoint.append([Point[i][0], Point[i][1], 1 * Point[i][2]])
            DXFpoint.append((tmpPoint[i][0], tmpPoint[i][1], 0, 0, tmpPoint[i][2]))

    elif Type == 2:
        for i in range(len(Point)):
            delta_X = 2 * ((X1 + C2C / 2) - Point[i][0])
            tmpPoint.append([Point[i][0] + delta_X, Point[i][1], -1 * Point[i][2]])
            DXFpoint.append((tmpPoint[i][0], tmpPoint[i][1], 0, 0, tmpPoint[i][2]))

    elif Type == 3:
        for i in range(len(Point)):
            delta_Y = 2 * (Y1 - Point[i][1])
            tmpPoint.append([Point[i][0], Point[i][1] + delta_Y, -1 * Point[i][2]])
            DXFpoint.append((tmpPoint[i][0], tmpPoint[i][1], 0, 0, tmpPoint[i][2]))

    elif Type == 4:
        for i in range(len(Point)):
            delta_X = 2 * ((X1 + C2C / 2) - Point[i][0])
            delta_Y = 2 * (Y1 - Point[i][1])
            tmpPoint.append([Point[i][0] + delta_X, Point[i][1] + delta_Y, 1 * Point[i][2]])
            DXFpoint.append((tmpPoint[i][0], tmpPoint[i][1], 0, 0, tmpPoint[i][2]))

    elif Type == 5:  # type 4 rotate 90
        for i in range(len(Point)):
            delta_X = 2 * ((X1 + C2C / 2) - Point[i][0])
            delta_Y = 2 * (Y1 - Point[i][1])
            tmpPoint.append([Point[i][0] + delta_X, Point[i][1] + delta_Y, 1 * Point[i][2]])

            tmpX1 = tmpPoint[i][0] - X1
            tmpY1 = tmpPoint[i][1] - Y1
            tmpX2 = -tmpY1 + X1
            tmpY2 = tmpX1 + Y1
            DXFpoint.append((tmpX2, tmpY2, 0, 0, tmpPoint[i][2]))

    elif Type == 6:  # type 3 rotate 90
        for i in range(len(Point)):
            delta_Y = 2 * (Y1 - Point[i][1])
            tmpPoint.append([Point[i][0], Point[i][1] + delta_Y, -1 * Point[i][2]])

            tmpX1 = tmpPoint[i][0] - X1
            tmpY1 = tmpPoint[i][1] - Y1
            tmpX2 = -tmpY1 + X1
            tmpY2 = tmpX1 + Y1
            DXFpoint.append((tmpX2, tmpY2, 0, 0, tmpPoint[i][2]))

    elif Type == 7:  # type 2 rotate 90
        for i in range(len(Point)):
            delta_X = 2 * ((X1 + C2C / 2) - Point[i][0])
            tmpPoint.append([Point[i][0] + delta_X, Point[i][1], -1 * Point[i][2]])

            tmpX1 = tmpPoint[i][0] - X1
            tmpY1 = tmpPoint[i][1] - Y1
            tmpX2 = -tmpY1 + X1
            tmpY2 = tmpX1 + Y1
            DXFpoint.append((tmpX2, tmpY2, 0, 0, tmpPoint[i][2]))

    elif Type == 8:  # type 1 rotate 90
        for i in range(len(Point)):
            tmpPoint.append([Point[i][0], Point[i][1], 1 * Point[i][2]])

            tmpX1 = tmpPoint[i][0] - X1
            tmpY1 = tmpPoint[i][1] - Y1
            tmpX2 = -tmpY1 + X1
            tmpY2 = tmpX1 + Y1
            DXFpoint.append((tmpX2, tmpY2, 0, 0, tmpPoint[i][2]))

    return DXFpoint


def main(dict_column_rebar_design, list_story_group, list_column_group, model_data_all, proj_arguments):

    [modelUnits_For, 
    modelUnits_Len,
    dictGridLines,
    dictStoryHeight,
    dictStoryJoint,
    dictPointXY,
    dictLineCon_B,
    dictLineCon_C,
    dictLineAssign,
    dictFrameSec,
    dictBarArea,
    dictBarDia,
    dictBarWei,
    listSpacing,
    dictOverLapLen,
    dictColCheckMode,
    dictLineAssign2,

    listColumnForce,
    listBeamForce,
    listStoryShear,
    listStoryLayer,
    tableColumDesign,
    tableBeamsDesign
    ] = model_data_all

    argProInfo, argGirderBarMinus, argBeamBarMinus, argColumnBarMinus, argGBRebarDWGScale = proj_arguments


    # # read
    # with shelve.open(db_file) as db:
    #     # dictBarArea       =   db['dictBarArea']
    #     argProInfo              =   db['argProInfo']        
    #     dictBarDia        =   db['dictBarDia']

    # # get files
    # file_full_name = os.path.join(file_folder, 'ColumnDesign', 'Col_Out01_ColList.txt')
    # groupList = [line.rstrip() for line in open(file_full_name, "r") if line[:1] != '*' and line[:1] != ' ' and line[:1] != '\n']

    # file_full_name = os.path.join(file_folder, 'ColumnDesign', 'Col_Out02_GroupingList.txt')
    # ColI = [line.rstrip() for line in open(file_full_name, "r") if line[:1] != '*']

    # file_full_name = os.path.join(file_folder, 'ColumnDesign', 'Col_Out03_ColSecInput.txt')
    # dxfI = [line.rstrip() for line in open(file_full_name, "r") if line[:1] != '*' and line[:1] != ' ']

    # tmpStart = groupList.index('$ Floor Name      List')
    # tmpEnd = groupList.index('$ Column Name     List')
    # groupFloor = [groupList[i].split()[0] for i in range(tmpStart, tmpEnd + 1) if groupList[i][:1] != '$']

    # tmpStart = groupList.index('$ Column Name     List')
    # tmpEnd = groupList.index('$ End of File')
    # groupColumn = [groupList[i].split()[0] for i in range(tmpStart, tmpEnd + 1) if groupList[i][:1] != '$']
    # groupList = []

    
    #============================================================================== To DXF

    dwg_scale = 1    #   1 == mm, 10 == cm
    if argProInfo == 'Code112_mm_ShowCrossSection':
        dwg_scale = 1    #   1 == mm, 10 == cm

    elif argProInfo == 'Code112_cm_ShowCrossSection':
        dwg_scale = 10    #   1 == mm, 10 == cm

    elif argProInfo == 'Code112_mm_DontShowCrossSection':
        dwg_scale = 1    #   1 == mm, 10 == cm

    elif argProInfo == 'Code112_cm_DontShowCrossSection':
        dwg_scale = 10    #   1 == mm, 10 == cm


    argBoxWid = 2000.0/dwg_scale    # please adjust! 可自行調整，但要2000以上
    argBoxDep = 1500.0/dwg_scale    # please adjust! 可自行調整


    # create a new DXF document
    doc = ezdxf.new('R2010', setup=True)    # 透過參數setup設為來ezdxf.new()建立一些標準資源，例如線型和文字樣式

    # 定義單位
    if dwg_scale == 1:
        doc.units = ezdxf.units.MM
    elif dwg_scale == 10:
        doc.units = ezdxf.units.CM

    # define modelspace
    msp = doc.modelspace()

    # define layer
    doc.layers.add(name="Default", color=1, linetype="Continuous")
    doc.layers.add(name="Concrete", color=13, linetype="Continuous")
    doc.layers.add(name="Dimension", color=1, linetype="Continuous")
    doc.layers.add(name="MainBar", color=1, linetype="Continuous")
    doc.layers.add(name="Stirrup", color=4, linetype="Continuous")
    doc.layers.add(name="Tie", color=3, linetype="Continuous")
    doc.layers.add(name="Text", color=2, linetype="Continuous")


    # add DXF Entities
    for index, row in dict_column_rebar_design.iterrows():
        argShape = row[11]

        if argShape == 'Circle':
            # 圓形斷面
            argFloor        = str(row[0])
            argColumn       = str(row[1])

            argX0           = float(row[2]) * argBoxWid * 1
            argY0           = float(row[3]) * (argBoxDep + 750/dwg_scale) * -1

            argRebarType    = int(row[4])
            argCover        = float(row[5])/dwg_scale

            argMBName       = str(row[6])
            argSBName       = str(row[7])
            argTBName       = str(row[8])

            argMBDia        = float(dictBarDia[argMBName])/dwg_scale
            argSBDia        = float(dictBarDia[argSBName])/dwg_scale
            argTBDia        = float(dictBarDia[argTBName])/dwg_scale

            argSS_CR        = float(row[9])/dwg_scale
            argSS_nCR       = float(row[10])/dwg_scale

            argDia          = float(row[12])/dwg_scale

            argNa           = str(row[15])
            
            argSN_CR        = int(row[17])
            argSN_nCR       = int(row[18])

            tmpNumber = index
            

            drawing_Circle(
                tmpNumber, argFloor + '_' + argColumn, argX0, argY0, argRebarType, argCover, argMBDia, argSBDia, argTBDia, argMBName, argSBName, argTBName, 
                argSS_CR, argSS_nCR, argDia, argNa, argSN_CR, argSN_nCR, 
                argBoxWid, argBoxDep, dwg_scale, msp
            )
                

        else:
            # 矩形斷面
            argFloor = str(row[0])
            argColumn = str(row[1])

            argX0 = float(row[2]) * argBoxWid * 1
            argY0 = float(row[3]) * (argBoxDep + 750/dwg_scale) * -1

            argRebarType = int(row[4])
            argCover = float(row[5])/dwg_scale

            argMBName = str(row[6])
            argSBName = str(row[7])
            argTBName = str(row[8])

            argMBDia = float(dictBarDia[argMBName])/dwg_scale
            argSBDia = float(dictBarDia[argSBName])/dwg_scale
            argTBDia = float(dictBarDia[argTBName])/dwg_scale

            argSBSpace1 = float(row[9])/dwg_scale
            argSBSpace2 = float(row[10])/dwg_scale
            argDx = float(row[11])/dwg_scale
            argDy = float(row[12])/dwg_scale

            argNx = str(row[15])
            argNy = str(row[16])

            argTNx = int(row[17])
            argTNy = int(row[18])

            tmpNumber = index
            

            drawing_Rectangular(
                tmpNumber, argFloor + '_' + argColumn, argX0, argY0, argRebarType, argCover, argMBDia, argSBDia, argTBDia, argMBName, argSBName, argTBName, 
                argSBSpace1, argSBSpace2, argDx, argDy, argNx, argNy, argTNx, argTNy, 
                argBoxWid, argBoxDep, dwg_scale, msp
            )
            


    table(argBoxWid, argBoxDep, list_story_group, list_column_group, dwg_scale, msp)


    #   Output
    dxf_to_string = to_binary_data(doc)
    



#============================================================================== To USS Column Section
    list_uss_data = []

    for index, row in dict_column_rebar_design.iterrows():
        argShape = row[11]
        if not argShape == 'Circle':

            argFloor = str(row[0])
            argColumn = str(row[1])

            argX0 = float(row[2]) * argBoxWid * 1
            argY0 = float(row[3]) * (argBoxDep + 750/dwg_scale) * -1

            argRebarType = int(row[4])
            argCover = float(row[5])/dwg_scale

            argMBName = str(row[6])
            argSBName = str(row[7])
            argTBName = str(row[8])

            argMBDia = float(dictBarDia[argMBName])/dwg_scale
            argSBDia = float(dictBarDia[argSBName])/dwg_scale
            argTBDia = float(dictBarDia[argTBName])/dwg_scale

            argSBSpace1 = float(row[9])/dwg_scale
            argSBSpace2 = float(row[10])/dwg_scale
            argDx = float(row[11])/dwg_scale
            argDy = float(row[12])/dwg_scale

            argfc = str(row[13])
            argfy = str(row[14])


            argNx = str(row[15])
            argNy = str(row[16])

            argTNx = int(row[17])
            argTNy = int(row[18])

            argModelMemberList = row[20].split()

            for value in argModelMemberList:
                argModelStory, argModelLabel, argAxialForce = value.split('_')

                list_uss_data.append([argModelStory, argModelLabel, argfc, argfy, argDx, argDy, argRebarType, argCover, argMBName, argSBName, argNx, argNy])
                # ("*ModelStory", "ModelLabel", "fc", "fy", "Dx(mm)", "Dy(mm)", "MBType", "Cover", "MB", "SB", "Nx", "Ny")


    if list_uss_data:
        tmpColumns = ["ModelStory", "ModelLabel", "fc", "fy", "Dx(mm)", "Dy(mm)", "MBType", "Cover", "MB", "SB", "Nx", "Ny"]
        df_ColData2USS = pd.DataFrame(list_uss_data, columns=tmpColumns)





    return dxf_to_string, df_ColData2USS










    # members = []
    # for tmp in ColI:
    #     tmpStoryGroup = tmp.split()[0]
    #     tmpColGroup = tmp.split()[1]
    #     tmpColMBType = tmp.split()[4]
    #     tmpColCo = tmp.split()[5]
    #     tmpColMB = tmp.split()[6]
    #     # tmpColSB = tmp.split()[7]        
    #     tmpfc = tmp.split()[9]
    #     tmpfy = tmp.split()[10]
        
    #     tmpList = tmp.split()[11:]
    #     for tmp2 in tmpList:
    #         tmpModelStory = tmp2.split('_')[0]
    #         tmpModelLabel = tmp2.split('_')[1]
    #         members.append((tmpModelStory, tmpModelLabel, tmpStoryGroup, tmpColGroup, tmpColMBType, tmpColCo, tmpColMB, tmpfc,tmpfy))

    # sections = []
    # for tmp in dxfI:
    #     tmpStoryGroup = tmp.split()[0]
    #     tmpColGroup = tmp.split()[1]
    #     tmpColSB = tmp.split()[7]
    #     tmpDx = tmp.split()[11]
    #     tmpDy = tmp.split()[12]
    #     tmpNx = tmp.split()[13]
    #     tmpNy = tmp.split()[14]
    #     # tmpNx = get_Total_ReBarshear(tmp.split()[13])
    #     # tmpNy = get_Total_ReBarshear(tmp.split()[14])
    #     sections.append((tmpStoryGroup, tmpColGroup, tmpColSB, tmpDx, tmpDy, tmpNx, tmpNy))

    # #   Output
    # secInfo = open(os.path.join(file_folder, 'ColumnDesign', 'Col_Out04b_ColData2USS.txt'), 'w')
    # secInfo.write('{0:<15}{1:<15}{2:<10}{3:<10}{4:<10}{5:<10}{6:<10}{7:<10}{8:<10}{9:<10}{10:<10}{11:<10}\n'.format("*ModelStory", "ModelLabel", "fc", "fy", "Dx(mm)", "Dy(mm)", "MBType", "Cover", "MB", "SB", "Nx", "Ny"))

    # secInfo.write('*' + '=' * 129 + '\n')

    # for tmp1 in members:
    #     tmpMBType = tmp1[4]
    #     tmpCo = tmp1[5]
    #     tmpMB = tmp1[6]
        
    #     tmpfc = tmp1[7]
    #     tmpfy = tmp1[8]
    #     tmpSB = ''
    #     tmpDx = ''
    #     tmpDy = ''
    #     tmpNx = ''
    #     tmpNy = ''
    #     for tmp2 in sections:
    #         if tmp1[2] + '_' + tmp1[3] == tmp2[0] + '_' + tmp2[1]:
    #             tmpSB = tmp2[2]
    #             tmpDx = tmp2[3]
    #             tmpDy = tmp2[4]
    #             tmpNx = tmp2[5]
    #             tmpNy = tmp2[6]
    #             break

    #     secInfo.write('{0:<15}{1:<15}{2:<10}{3:<10}{4:<10}{5:<10}{6:<10}{7:<10}{8:<10}{9:<10}{10:<10}{11:<10}\n'.format(tmp1[0], tmp1[1], tmpfc, tmpfy, tmpDx, tmpDy, tmpMBType, tmpCo, tmpMB, tmpSB, tmpNx, tmpNy))
    # secInfo.close()
#============================================================================== EOF
    # message_box('Message', 'Job Done')
    
    

if __name__ == '__main__':
        main(r'D:\@Programing\Python\EtabsOutputToAutoCad\@202404_ToEXE\Sample\ModelData\ModelData', r'D:\@Programing\Python\EtabsOutputToAutoCad\@202404_ToEXE\Sample')