# import os
# import re
import math
# import shelve
import pandas as pd

# import SoftwareLicense

# from ctypes import c_int, WINFUNCTYPE, windll
# from ctypes.wintypes import HWND, LPCWSTR, UINT

# def message_box(title, text):
#     #   ctypes.windll.user32.MessageBoxW(0, text, title, style)    
#     prototype = WINFUNCTYPE(c_int, HWND, LPCWSTR, LPCWSTR, UINT)
#     paramflags = (1, "hwnd", 0), (1, "text", text), (1, "caption", title), (1, "flags", 0)
#     MessageBox = prototype(("MessageBoxW", windll.user32), paramflags)   
#     MessageBox()


def seismic_shear_design_formula_1(Ag, Ach, fc, fyt):
    return 0.3 * (Ag / Ach - 1) * (fc / fyt)


def seismic_shear_design_formula_2(fc, fyt):
    return 0.09 * (fc / fyt)


def seismic_shear_design_formula_3(Pu, Ach, fc, fyt, nl):
    kf = max(1.0, fc/1750 + 0.6)
    kn = nl/(nl-2)
    return 0.2 * kf * kn * Pu / (Ach / 100 * fyt / 1000)

def seismic_shear_design_formula_C1(Ag, Ach, fc, fyt):
    return 0.45 * (Ag / Ach - 1) * (fc / fyt)


def seismic_shear_design_formula_C2(fc, fyt):
    return 0.12 * (fc / fyt)


def seismic_shear_design_formula_C3(Pu, Ach, fc, fyt):
    kf = max(1.0, fc/1750 + 0.6)
    return 0.35 * kf * Pu / (Ach / 100 * fyt / 1000)


def get_CR_ShearBarSpace(Dx, Dy, hx, hy, fyt, db):
    value1 = max(0.25 * Dx, 100.0)
    value2 = max(0.25 * Dy, 100.0)
    value3 = 100 + (350 - hx) / 3
    value4 = 100 + (350 - hy) / 3

    if abs((fyt - 4200)) / 4200 < 0.01:
        value5 = 6 * db
    elif abs((fyt - 5000)) / 5000 < 0.01:
        value5 = 5.5 * db
    elif abs((fyt - 5600)) / 5600 < 0.01:
        value5 = 5 * db
    else:
        value5 = 5 * db

    value6 = 150.0

    GovernedValue = min(value1, value2, value3, value4, value5, value6)

    return GovernedValue, 100.0


def get_TieBarNumber(MB_Number, C2C, MB_Dia, TB_Dia):
    tmpN1 = 0
    tmpN2 = 0

    # 隔一箍一
    if (MB_Number - 2) % 2 == 0:
        tmpN1 = (MB_Number - 2) / 2
    else:
        tmpN1 = (MB_Number - 2 - 1) / 2

    # 350mm限制
    for j in range(1, MB_Number - 2):
        if (MB_Number - 2 + 1) % (j + 1) == 0:
            arg_hy = (MB_Number - 2 + 1) / (j + 1) * C2C
            if arg_hy < 350.0:
                tmpN2 = j
                break
        else:
            arg_hy = (MB_Number - 2 + 1) // (j + 1 + 1) * C2C
            if arg_hy < 350.0:
                tmpN2 = j
                break

    return int(max(tmpN1, tmpN2))


def get_outCS(Datas, Floor, ColumnID, ColumnH, out_unit):
    # read data
    listSta = []
    listAtl = []
    listAs2 = []
    listAs3 = []
    listPMM = []

    for tmp in Datas:
        if tmp[0] == Floor and tmp[1] == ColumnID:
            listSta.append(tmp[2])
            listAtl.append(tmp[3])
            listAs2.append(tmp[4])
            listAs3.append(tmp[5])
            listPMM.append(tmp[6])


    # Bottom
    tmpH1 = 0.00* ColumnH
    tmpH2 = 0.25 * ColumnH
          
    intS = 0
    intE = 0
    intN = len(listSta)
    for i in range(len(listSta)):
        if listSta[i] > tmpH1:
            intS = i
            break
    for i in range(len(listSta)):
        if listSta[i] > tmpH2:
            intE = i
            break

    if intS == 0:
        listSta.append(tmpH1)
        listAtl.append(listAtl[intS])
        listAs2.append(listAs2[intS])
        listAs3.append(listAs3[intS])
    else:
        listSta.append(tmpH1)
        listAtl.append(((listAtl[intS] - listAtl[intS - 1]) / (listSta[intS] - listSta[intS - 1])) * (tmpH1 - listSta[intS - 1]) + listAtl[intS - 1])
        listAs2.append(((listAs2[intS] - listAs2[intS - 1]) / (listSta[intS] - listSta[intS - 1])) * (tmpH1 - listSta[intS - 1]) + listAs2[intS - 1])
        listAs3.append(((listAs3[intS] - listAs3[intS - 1]) / (listSta[intS] - listSta[intS - 1])) * (tmpH1 - listSta[intS - 1]) + listAs3[intS - 1])


    if intE == intN:
        listSta.append(tmpH2)
        listAtl.append(listAtl[intE-1])
        listAs2.append(listAs2[intE-1])
        listAs3.append(listAs3[intE-1])
    else:
        listSta.append(tmpH2)
        listAtl.append(((listAtl[intE] - listAtl[intE - 1]) / (listSta[intE] - listSta[intE - 1])) * (tmpH2 - listSta[intE - 1]) + listAtl[intE - 1])
        listAs2.append(((listAs2[intE] - listAs2[intE - 1]) / (listSta[intE] - listSta[intE - 1])) * (tmpH2 - listSta[intE - 1]) + listAs2[intE - 1])
        listAs3.append(((listAs3[intE] - listAs3[intE - 1]) / (listSta[intE] - listSta[intE - 1])) * (tmpH2 - listSta[intE - 1]) + listAs3[intE - 1])
    
    
    for i in range(len(listSta)):
        if i < intS and i > intE and i != len(listSta)-1 and i != len(listSta)-2:
            listSta.pop(i)
            listAtl.pop(i)
            listAs2.pop(i)
            listAs3.pop(i)

    Bot_Atl = max(listAtl)
    Bot_As2 = max(listAs2)
    Bot_As3 = max(listAs3)
        
    # Center
    tmpH1 = 0.25* ColumnH
    tmpH2 = 0.75 * ColumnH
         
    intS = 0
    intE = 0
    intN = len(listSta)
    for i in range(len(listSta)):
        if listSta[i] > tmpH1:
            intS = i
            break
    for i in range(len(listSta)):
        if listSta[i] > tmpH2:
            intE = i
            break

    if intS == 0:
        listSta.append(tmpH1)
        listAtl.append(listAtl[intS])
        listAs2.append(listAs2[intS])
        listAs3.append(listAs3[intS])
    else:
        listSta.append(tmpH1)
        listAtl.append(((listAtl[intS] - listAtl[intS - 1]) / (listSta[intS] - listSta[intS - 1])) * (tmpH1 - listSta[intS - 1]) + listAtl[intS - 1])
        listAs2.append(((listAs2[intS] - listAs2[intS - 1]) / (listSta[intS] - listSta[intS - 1])) * (tmpH1 - listSta[intS - 1]) + listAs2[intS - 1])
        listAs3.append(((listAs3[intS] - listAs3[intS - 1]) / (listSta[intS] - listSta[intS - 1])) * (tmpH1 - listSta[intS - 1]) + listAs3[intS - 1])


    if intE == intN:
        listSta.append(tmpH2)
        listAtl.append(listAtl[intE-1])
        listAs2.append(listAs2[intE-1])
        listAs3.append(listAs3[intE-1])
    else:
        listSta.append(tmpH2)
        listAtl.append(((listAtl[intE] - listAtl[intE - 1]) / (listSta[intE] - listSta[intE - 1])) * (tmpH2 - listSta[intE - 1]) + listAtl[intE - 1])
        listAs2.append(((listAs2[intE] - listAs2[intE - 1]) / (listSta[intE] - listSta[intE - 1])) * (tmpH2 - listSta[intE - 1]) + listAs2[intE - 1])
        listAs3.append(((listAs3[intE] - listAs3[intE - 1]) / (listSta[intE] - listSta[intE - 1])) * (tmpH2 - listSta[intE - 1]) + listAs3[intE - 1])
    
    
    for i in range(len(listSta)):
        if i < intS and i > intE and i != len(listSta)-1 and i != len(listSta)-2:
            listSta.pop(i)
            listAtl.pop(i)
            listAs2.pop(i)
            listAs3.pop(i)

    Cen_Atl = max(listAtl)
    Cen_As2 = max(listAs2)
    Cen_As3 = max(listAs3)
        
    # End
    tmpH1 = 0.75 * ColumnH
    tmpH2 = 1.00 * ColumnH
          
    intS = 0
    intE = 0
    intN = len(listSta)
    for i in range(len(listSta)):
        if listSta[i] > tmpH1:
            intS = i
            break
    for i in range(len(listSta)):
        if listSta[i] > tmpH2:
            intE = i
            break

    if intS == 0:
        listSta.append(tmpH1)
        listAtl.append(listAtl[intS])
        listAs2.append(listAs2[intS])
        listAs3.append(listAs3[intS])
    else:
        listSta.append(tmpH1)
        listAtl.append(((listAtl[intS] - listAtl[intS - 1]) / (listSta[intS] - listSta[intS - 1])) * (tmpH1 - listSta[intS - 1]) + listAtl[intS - 1])
        listAs2.append(((listAs2[intS] - listAs2[intS - 1]) / (listSta[intS] - listSta[intS - 1])) * (tmpH1 - listSta[intS - 1]) + listAs2[intS - 1])
        listAs3.append(((listAs3[intS] - listAs3[intS - 1]) / (listSta[intS] - listSta[intS - 1])) * (tmpH1 - listSta[intS - 1]) + listAs3[intS - 1])


    if intE == intN:
        listSta.append(tmpH2)
        listAtl.append(listAtl[intE-1])
        listAs2.append(listAs2[intE-1])
        listAs3.append(listAs3[intE-1])
    else:
        listSta.append(tmpH2)
        listAtl.append(((listAtl[intE] - listAtl[intE - 1]) / (listSta[intE] - listSta[intE - 1])) * (tmpH2 - listSta[intE - 1]) + listAtl[intE - 1])
        listAs2.append(((listAs2[intE] - listAs2[intE - 1]) / (listSta[intE] - listSta[intE - 1])) * (tmpH2 - listSta[intE - 1]) + listAs2[intE - 1])
        listAs3.append(((listAs3[intE] - listAs3[intE - 1]) / (listSta[intE] - listSta[intE - 1])) * (tmpH2 - listSta[intE - 1]) + listAs3[intE - 1])
    
    
    for i in range(len(listSta)):
        if i < intS and i > intE and i != len(listSta)-1 and i != len(listSta)-2:
            listSta.pop(i)
            listAtl.pop(i)
            listAs2.pop(i)
            listAs3.pop(i)

    End_Atl = max(listAtl)
    End_As2 = max(listAs2)
    End_As3 = max(listAs3)

        
    return [Bot_Atl, Bot_As2, Bot_As3, Cen_Atl, Cen_As2, Cen_As3, End_Atl, End_As2, End_As3, max(listPMM)]

    
def main(dict_column_design_parameter, model_data_all, proj_arguments):
    
    # read
    # with shelve.open(db_file) as db:
    #     # modelUnits_For      =   db['modelUnits_For']   
    #     modelUnits_Len      =   db['modelUnits_Len']     
    #     # listStoryLayer      =   db['listStoryLayer']  
    #     dictStoryHeight     =   db['dictStoryHeight']
    #     # dictStoryJoint      =   db['dictStoryJoint']     
    #     # dictPointXY         =   db['dictPointXY']        
    #     # dictLineCon_B       =   db['dictLineCon_B']      
    #     # dictLineCon_C       =   db['dictLineCon_C']      
    #     # dictLineAssign      =   db['dictLineAssign']     
    #     # dictFrameSec        =   db['dictFrameSec']       
    #     tableColumDesign    =   db['tableColumDesign']   
    #     # tableBeamsDesign    =   db['tableBeamsDesign']   

    #     dictBarArea         =   db['dictBarArea']        
    #     dictBarDia          =   db['dictBarDia']    
    #     # dictBarWei          =   db['dictBarWei'] 
    #     # listSpacing         =   db['listSpacing']
    #     # dictOverLapLen      =   db['dictOverLapLen']
    
    #     dictColCheckMode    =   db['dictColCheckMode']
    #     dictLineAssign2     =   db['dictLineAssign2']
    #     argColumnBarMinus   =   db['argColumnBarMinus'] #   計算出來的最大根數減少的根數

    # file_full_name = os.path.join(file_folder, 'ColumnDesign', 'Col_Out02_GroupingList.txt')
    # dxfI = [line.strip() for line in open(file_full_name, "r") if line[:1] != '*']

    # # write
    # outfile = open(os.path.join(file_folder, 'ColumnDesign', 'Col_Out03_ColSecInput.txt'), 'w')
    # outfile.write('{0:<10}{1:<10}{2:<10}{3:<10}{4:<10}{5:<10}{6:<10}{7:<10}{8:<10}{9:<10}{10:<10}{11:<10}{12:<10}{13:<10}{14:<10}{15:<10}{16:<10}\n'
    #             .format("*Floor", "Column","Location","Location", "RebarType", "Cover", "Main-Bar", "Sti-Bar", "Tie-Bar", "CR", "Non-CR", "Dx", "Dy", "Nx", "Ny", "TNx", "TNy"))
    # outfile.write('{0:<10}{1:<10}{2:<10}{3:<10}{4:<10}{5:<10}{6:<10}{7:<10}{8:<10}{9:<10}{10:<10}{11:<10}{12:<10}{13:<10}{14:<10}{15:<10}{16:<10}\n'
    #             .format("*", "", "X-Dir.","Y-Dir.", "", "", "Dia.", "Dia.", "Dia.", "TieSpace", "TieSpace", "", "", "", "", "", ""))
    # outfile.write('*' + '='*162 + ' All Units: mm\n')



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





    reqSecBarDesign = []

    reqExportRectangular = []
    reqExportCircle      = []
    for index, row in dict_column_design_parameter.iterrows():
        arg_FloorGroup, arg_ColumnGroup, arg_X0, arg_Y0, arg_RebarType, arg_Cover, arg_MB_Name, arg_Dx, arg_Dy, arg_fc, arg_fys, arg_ModelColumnList = row

        arg_FloorGroup      =   str(arg_FloorGroup) 
        arg_ColumnGroup     =   str(arg_ColumnGroup)
        arg_X0              =   int(arg_X0)         
        arg_Y0              =   int(arg_Y0)         
        arg_RebarType       =   int(arg_RebarType)  
        arg_Cover           = float(arg_Cover)    
        arg_MB_Name         =   str(arg_MB_Name)    
        arg_Dx              = float(arg_Dx)       
        arg_Dy              = float(arg_Dy)       
        arg_fc              = float(arg_fc)       
        arg_fys             = float(arg_fys)
        arg_ModelColumnList =   str(arg_ModelColumnList)
        
        # print(row)

    # # for i in range(len(dxfI)):
    #     arg_FloorGroup = dxfI[i].split()[0]
    #     arg_ColumnGroup = dxfI[i].split()[1]
    #     arg_X0 = int(dxfI[i].split()[2])
    #     arg_Y0 = int(dxfI[i].split()[3])
    #     arg_RebarType = int(dxfI[i].split()[4])
    #     arg_Cover = float(dxfI[i].split()[5])        
    #     arg_MB_Name = dxfI[i].split()[6]
    #     arg_Dx = float(dxfI[i].split()[7])
    #     arg_Dy = float(dxfI[i].split()[8])        
    #     arg_fc = float(dxfI[i].split()[9])
    #     arg_fys = float(dxfI[i].split()[10])

    #     # print(arg_FloorGroup, arg_ColumnGroup)

        # ====================================================================================================================== get required re-bar
        arg_MainBar     = []
        arg_As2_CR      = []
        arg_As2_nCR     = []
        arg_As3_CR      = []
        arg_As3_nCR     = []
        arg_PMM         = []
        arg_N3          = []
        arg_N2          = []
        arg_RB          = []
        arg_ColShape    = []
        
        arg_ModelMemberList = ''
        arg_MaxAxialLoad  =   []
        # for tmp in dxfI[i].split()[11:]:
        for tmp in arg_ModelColumnList.split():
            modelFloor, modelColumn, modelmaxAxialLoad = tmp.split('_')
            modelmaxAxialLoad = float(modelmaxAxialLoad)

            modelColH = float(dictStoryHeight[modelFloor])

            rebarInfo = get_outCS(tableColumDesign, modelFloor, modelColumn, modelColH, modelUnits_Len)
            # return [Bot_Atl, Bot_As2, Bot_As3, Cen_Atl, Cen_As2, Cen_As3, End_Atl, End_As2, End_As3, max(listPMM)] 
            
            arg_MainBar.append(rebarInfo[0])
            arg_MainBar.append(rebarInfo[3])
            arg_MainBar.append(rebarInfo[6])
            arg_As2_CR.append(rebarInfo[1])
            arg_As2_CR.append(rebarInfo[7])
            arg_As3_CR.append(rebarInfo[2])
            arg_As3_CR.append(rebarInfo[8])
            arg_As2_nCR.append(rebarInfo[4])
            arg_As3_nCR.append(rebarInfo[5])
            arg_PMM.append(rebarInfo[9])
            arg_N3.append(dictColCheckMode[dictLineAssign2[modelFloor+'-'+modelColumn]][0])
            arg_N2.append(dictColCheckMode[dictLineAssign2[modelFloor+'-'+modelColumn]][1])
            arg_RB.append(dictColCheckMode[dictLineAssign2[modelFloor+'-'+modelColumn]][2])
            arg_ColShape.append(dictColCheckMode[dictLineAssign2[modelFloor+'-'+modelColumn]][3])

            arg_ModelMemberList = arg_ModelMemberList + modelFloor + '-' + modelColumn + ' '
            arg_MaxAxialLoad.append(modelmaxAxialLoad)
            
        arg_Pu = max(arg_MaxAxialLoad)
        arg_ColShape = list(set(arg_ColShape))[0]

        if arg_ColShape == 'Rectangular':
            arg_Ag = arg_Dx * arg_Dy
        elif arg_ColShape == 'Circle':
            arg_Ag = 0.25 * math.pi * arg_Dx * arg_Dx

        # ====================================================================================================================== for check mode main bar
        if arg_ColShape == 'Rectangular':

            # 主筋設計放大值--目前沒使用 固定1.0
            main_bar_application = 1.0
            arg_MainBar_req = max(arg_MainBar) * main_bar_application

            # 斷面性質
            arg_MB_Dia = dictBarDia[arg_MB_Name]    # 需確認ETABS名稱一致
            arg_MB_Area = dictBarArea[arg_MB_Name]

            arg_SB_Dia = 19.0   # 主筋間距在計算時，箍筋採D19保守計算
            arg_TB_Dia = 19.0   # 主筋間距在計算時，箍筋採D19保守計算

            # 最小鋼筋間距
            arg_RebarC2C = max(1.5*arg_MB_Dia + 1.145*arg_MB_Dia, 40+arg_MB_Dia, 1.33*25+arg_MB_Dia)

            # 計算X向鋼筋配置(N1第一層,N2第二層)
            arg_Nx = max(arg_N2)
            max_BarNo = int(math.floor((arg_Dx - 2*arg_Cover - 2*arg_SB_Dia - arg_MB_Dia) / (arg_RebarC2C)) + 1 - argColumnBarMinus)    #   計算出來的最大根數減少輸入根數
            if arg_Nx <= max_BarNo:
                arg_Nx1 = int(arg_Nx)
                arg_Nx2 = 0
            else:
                arg_Nx1 = max_BarNo
                arg_Nx2 = int(arg_Nx - max_BarNo)

            # 計算Y向鋼筋配置(N1第一層,N2第二層)
            arg_Ny = max(arg_N3)
            max_BarNo = int(math.floor((arg_Dy - 2*arg_Cover - 2*arg_SB_Dia - arg_MB_Dia) / (arg_RebarC2C)) + 1 - argColumnBarMinus)    #   計算出來的最大根數減少輸入根數
            if arg_Ny <= max_BarNo:
                arg_Ny1 = int(arg_Ny)
                arg_Ny2 = 0
            else:
                arg_Ny1 = max_BarNo
                arg_Ny2 = int(arg_Ny - max_BarNo)

            # 紀錄總鋼筋量
            arg_MainBar_total = arg_Nx * 2 + arg_Ny * 2 - 4
            arg_MainBar_pro = arg_MainBar_total * arg_MB_Area
            arg_MainBar_PMMRatio = max(arg_PMM)

            # # 主筋淨間距(不須檢核，計算N1 & N2時已考慮)
            # arg_NetSpace_x = (arg_Dx - 2*arg_Cover - 2*arg_SB_Dia - arg_MB_Dia) / (arg_Nx1 - 1) - arg_MB_Dia
            # arg_NetSpace_y = (arg_Dy - 2*arg_Cover - 2*arg_SB_Dia - arg_MB_Dia) / (arg_Ny1 - 1) - arg_MB_Dia


            # ====================================================================================================================== for shear bar design 剪力鋼筋計算
            # 軸力檢核
            tmpCondition1 = (arg_Pu > 0.3*(arg_Ag/10/10)*arg_fc/1000)
            tmpCondition2 = (arg_fc > 700)

            # tmpSB_Name_List = ['#3', '#4', '#5', '#6'] if '#' in arg_MB_Name else ['D10', 'D13', 'D16', 'D19']
            tmpSB_Name_List = ['#4', '#5', '#6', '#7'] if '#' in arg_MB_Name else ['D13', 'D16', 'D19', 'D22']
            tmpSB_Space_List = [150.0, 120.0, 100.0]        
            

            # 先判斷是否為大軸力柱
            if tmpCondition1 or tmpCondition2:
                # 每根都要箍筋
                arg_TNx = arg_Ny1 - 2
                arg_TNy = arg_Nx1 - 2

                for tmp1 in tmpSB_Name_List:
                    # 箍繫筋資訊
                    arg_SB_Name = tmp1
                    arg_TB_Name = tmp1        
                    arg_SB_Dia = dictBarDia[arg_SB_Name]
                    arg_TB_Dia = dictBarDia[arg_TB_Name]
                    arg_SB_Area = dictBarArea[arg_SB_Name]
                    arg_TB_Area = dictBarArea[arg_TB_Name]
                    
                    arg_Space_CR = False
                    arg_Space_nCR = False

                    arg_Ach = (arg_Dx - 2 * arg_Cover + 2 * arg_SB_Dia)* (arg_Dy - 2 * arg_Cover + 2 * arg_SB_Dia)
                    arg_C2C_y = (arg_Dy - 2 * arg_Cover - 2 * arg_SB_Dia - arg_MB_Dia) / (arg_Ny1 - 1)
                    arg_C2C_x = (arg_Dx - 2 * arg_Cover - 2 * arg_SB_Dia - arg_MB_Dia) / (arg_Nx1 - 1)

                    # ============================================================== 圍束區
                    # X向耐震需求推算間距
                    arg_As2_CR_Ash1 = (arg_Dy - 2 * arg_Cover - arg_SB_Dia) * seismic_shear_design_formula_1(arg_Ag, arg_Ach, arg_fc, arg_fys)
                    arg_As2_CR_Ash2 = (arg_Dy - 2 * arg_Cover - arg_SB_Dia) * seismic_shear_design_formula_2(arg_fc, arg_fys)
                    arg_As2_CR_Ash3 = (arg_Dy - 2 * arg_Cover - arg_SB_Dia) * seismic_shear_design_formula_3(arg_Pu, arg_Ach, arg_fc, arg_fys, (arg_TNx + arg_TNy +4))
                    arg_As2_CR_Reqd = max(arg_As2_CR)       
                    
                    # X向推算間距-圍束區
                    arg_As2_CR_governed = max(arg_As2_CR_Ash1, arg_As2_CR_Ash2, arg_As2_CR_Ash3, arg_As2_CR_Reqd)
                    arg_Space_CR_X = (2 * arg_SB_Area + arg_TNx * arg_TB_Area) / arg_As2_CR_governed
                    arg_hy = 1.0 * arg_C2C_y + arg_MB_Dia + arg_TB_Dia

                    # Y向耐震需求推算間距
                    arg_As3_CR_Ash1 = (arg_Dx - 2 * arg_Cover - arg_SB_Dia) * seismic_shear_design_formula_1(arg_Ag, arg_Ach, arg_fc, arg_fys)
                    arg_As3_CR_Ash2 = (arg_Dx - 2 * arg_Cover - arg_SB_Dia) * seismic_shear_design_formula_2(arg_fc, arg_fys)
                    arg_As3_CR_Ash3 = (arg_Dx - 2 * arg_Cover - arg_SB_Dia) * seismic_shear_design_formula_3(arg_Pu, arg_Ach, arg_fc, arg_fys, (arg_TNx + arg_TNy +4))
                    arg_As3_CR_Reqd = max(arg_As3_CR)

                    # Y向推算間距-圍束區
                    arg_As3_CR_governed = max(arg_As3_CR_Ash1, arg_As3_CR_Ash2, arg_As3_CR_Ash3, arg_As3_CR_Reqd)
                    arg_Space_CR_Y = (2 * arg_SB_Area + arg_TNy * arg_TB_Area) / arg_As3_CR_governed
                    arg_hx = 1.0 * arg_C2C_x + arg_MB_Dia + arg_TB_Dia

                    # 間距計算
                    arg_MaxSpace_CR, arg_MinSpace_CR = get_CR_ShearBarSpace(arg_Dx, arg_Dy, arg_hx, arg_hy, arg_fys, arg_MB_Dia)
                    arg_Space_CR_required = 1.0 if min(arg_Space_CR_X, arg_Space_CR_Y,  arg_MaxSpace_CR) < arg_MinSpace_CR else min(arg_Space_CR_X, arg_Space_CR_Y,  arg_MaxSpace_CR)

                    for tmp2 in tmpSB_Space_List:
                        if (tmp2 < arg_Space_CR_required) or (abs(tmp2-arg_Space_CR_required) < 1):
                            arg_Space_CR = tmp2
                            break
                    
                    if arg_Space_CR == False:   #   要上升一個號數，不然會低於100mm
                        continue

                    # ============================================================== 非圍束區
                    # X向推算間距-非圍束區
                    arg_As2_nCR_governed = max(arg_As2_nCR)
                    arg_Space_nCR_X = (2 * arg_SB_Area + arg_TNx * arg_TB_Area) / arg_As2_nCR_governed if arg_As2_nCR_governed > 0.0001 else 150

                    # Y向推算間距-非圍束區
                    arg_As3_nCR_governed = max(arg_As3_nCR)
                    arg_Space_nCR_Y = (2 * arg_SB_Area + arg_TNy * arg_TB_Area) / arg_As3_nCR_governed if arg_As3_nCR_governed > 0.0001 else 150

                    arg_MaxSpace_nCR, arg_MinSpace_nCR = min(6*arg_MB_Dia, 150), 100.0
                    arg_Space_nCR_required = 1.0 if min(arg_Space_nCR_X, arg_Space_nCR_Y, arg_MaxSpace_nCR) < arg_MinSpace_nCR else min(arg_Space_nCR_X, arg_Space_nCR_Y, arg_MaxSpace_nCR)

                    for tmp2 in tmpSB_Space_List:
                        if (tmp2 < arg_Space_nCR_required) or (abs(tmp2-arg_Space_nCR_required) < 1):
                            arg_Space_nCR = tmp2
                            break
                    
                    if arg_Space_nCR == False:   #   要上升一個號數，不然會低於100mm
                        continue

                    # ============================================================== 確認離開
                    if arg_Space_CR and arg_Space_nCR:
                        break


            else:

                for tmp1 in tmpSB_Name_List:
                    # 箍繫筋資訊
                    arg_SB_Name = tmp1
                    arg_TB_Name = tmp1        
                    arg_SB_Dia = dictBarDia[arg_SB_Name]
                    arg_TB_Dia = dictBarDia[arg_TB_Name]
                    arg_SB_Area = dictBarArea[arg_SB_Name]
                    arg_TB_Area = dictBarArea[arg_TB_Name]

                    arg_Space_CR = False
                    arg_Space_nCR = False

                    arg_Ach = (arg_Dx - 2 * arg_Cover + 2 * arg_SB_Dia)* (arg_Dy - 2 * arg_Cover + 2 * arg_SB_Dia)
                    arg_C2C_y = (arg_Dy - 2 * arg_Cover - 2 * arg_SB_Dia - arg_MB_Dia) / (arg_Ny1 - 1)
                    arg_C2C_x = (arg_Dx - 2 * arg_Cover - 2 * arg_SB_Dia - arg_MB_Dia) / (arg_Nx1 - 1)

                    # ============================================================== 繫筋數計算
                    # 隔一箍一與350mm檢查
                    # def get_TieBarNumber(MB_Number, C2C, MB_Dia, TB_Dia)
                    arg_TNx = get_TieBarNumber(arg_Ny1, arg_C2C_y, arg_MB_Dia, arg_TB_Dia)
                    arg_TNy = get_TieBarNumber(arg_Nx1, arg_C2C_x, arg_MB_Dia, arg_TB_Dia)

                                            # # X向 隔一箍一與350mm檢查
                                            # arg_TNx_1 = 0
                                            # arg_TNx_2 = 0
                                            # # 隔一箍一
                                            # if (arg_Ny1 - 2) % 2 == 0:
                                            #     arg_TNx_1 = (arg_Ny1 - 2) / 2
                                            # else:
                                            #     arg_TNx_1 = (arg_Ny1 - 2 - 1) / 2

                                            # # 350mm限制
                                            # for j in range(1, arg_Ny1 - 2):
                                            #     if (arg_Ny1 - 2 + 1) % (j + 1) == 0:
                                            #         arg_hy = (arg_Ny1 - 2 + 1) / (j + 1) * arg_C2C_y + arg_MB_Dia + arg_TB_Dia
                                            #         if arg_hy < 350.0:
                                            #             arg_TNx_2 = j
                                            #             break
                                            #     else:
                                            #         arg_hy = (arg_Ny1 - 2 + 1) // (j + 1 + 1) * arg_C2C_y + arg_MB_Dia + arg_TB_Dia
                                            #         if arg_hy < 350.0:
                                            #             arg_TNx_2 = j
                                            #             break

                                            # arg_TNx = int(max(arg_TNx_1, arg_TNx_2))


                                            # # y向 隔一箍一與350mm檢查
                                            # arg_TNy_1 = 0
                                            # arg_TNy_2 = 0
                                            # # 隔一箍一
                                            # if (arg_Nx1 - 2) % 2 == 0:
                                            #     arg_TNy_1 = (arg_Nx1 - 2) / 2
                                            # else:
                                            #     arg_TNy_1 = (arg_Nx1 - 2 - 1) / 2

                                            # # 350mm限制
                                            # for j in range(1, arg_Nx1 - 2):
                                            #     if (arg_Nx1 - 2 + 1) % (j + 1) == 0:
                                            #         arg_hx = (arg_Nx1 - 2 + 1) / (j + 1) * arg_C2C_x + arg_MB_Dia + arg_TB_Dia
                                            #         if arg_hx < 350.0:
                                            #             arg_TNy_2 = j
                                            #             break
                                            #     else:
                                            #         arg_hx = (arg_Nx1 - 2 + 1) // (j + 1 + 1) * arg_C2C_x + arg_MB_Dia + arg_TB_Dia
                                            #         if arg_hx < 350.0:
                                            #             arg_TNy_2 = j
                                            #             break
                                            
                                            # arg_TNy = int(max(arg_TNy_1, arg_TNy_2))

                    # ============================================================== 圍束區
                    # X向耐震需求推算間距
                    arg_As2_CR_Ash1 = (arg_Dy - 2 * arg_Cover - arg_SB_Dia) * seismic_shear_design_formula_1(arg_Ag, arg_Ach, arg_fc, arg_fys)
                    arg_As2_CR_Ash2 = (arg_Dy - 2 * arg_Cover - arg_SB_Dia) * seismic_shear_design_formula_2(arg_fc, arg_fys)
                    arg_As2_CR_Ash3 = 0.0
                    arg_As2_CR_Reqd = max(arg_As2_CR)
                    
                    # X向推算間距-圍束區
                    arg_As2_CR_governed = max(arg_As2_CR_Ash1, arg_As2_CR_Ash2, arg_As2_CR_Ash3, arg_As2_CR_Reqd)
                    arg_Space_CR_X = (2 * arg_SB_Area + arg_TNx * arg_TB_Area) / arg_As2_CR_governed
                    arg_hy = 2.0 * arg_C2C_y + arg_MB_Dia + arg_TB_Dia

                    # Y向耐震需求推算間距
                    arg_As3_CR_Ash1 = (arg_Dx - 2 * arg_Cover - arg_SB_Dia) * seismic_shear_design_formula_1(arg_Ag, arg_Ach, arg_fc, arg_fys)
                    arg_As3_CR_Ash2 = (arg_Dx - 2 * arg_Cover - arg_SB_Dia) * seismic_shear_design_formula_2(arg_fc, arg_fys)
                    arg_As3_CR_Ash3 = 0.0
                    arg_As3_CR_Reqd = max(arg_As3_CR)

                    # Y向推算間距-圍束區
                    arg_As3_CR_governed = max(arg_As3_CR_Ash1, arg_As3_CR_Ash2, arg_As3_CR_Ash3, arg_As3_CR_Reqd)
                    arg_Space_CR_Y = (2 * arg_SB_Area + arg_TNy * arg_TB_Area) / arg_As3_CR_governed
                    arg_hx = 2.0 * arg_C2C_x + arg_MB_Dia + arg_TB_Dia

                    # 間距計算
                    arg_MaxSpace_CR, arg_MinSpace_CR = get_CR_ShearBarSpace(arg_Dx, arg_Dy, arg_hx, arg_hy, arg_fys, arg_MB_Dia)
                    arg_Space_CR_required = 1.0 if min(arg_Space_CR_X, arg_Space_CR_Y,  arg_MaxSpace_CR) < arg_MinSpace_CR else min(arg_Space_CR_X, arg_Space_CR_Y,  arg_MaxSpace_CR)

                    for tmp2 in tmpSB_Space_List:
                        if (tmp2 < arg_Space_CR_required) or (abs(tmp2-arg_Space_CR_required) < 1):
                            arg_Space_CR = tmp2
                            break
                    
                    if arg_Space_CR == False:   #   要上升一個號數，不然會低於100mm
                        continue

                    # ============================================================== 非圍束區
                    # X向推算間距-非圍束區
                    arg_As2_nCR_governed = max(arg_As2_nCR)
                    arg_Space_nCR_X = (2 * arg_SB_Area + arg_TNx * arg_TB_Area) / arg_As2_nCR_governed if arg_As2_nCR_governed > 0.0001 else 150

                    # Y向推算間距-非圍束區
                    arg_As3_nCR_governed = max(arg_As3_nCR)
                    arg_Space_nCR_Y = (2 * arg_SB_Area + arg_TNy * arg_TB_Area) / arg_As3_nCR_governed if arg_As3_nCR_governed > 0.0001 else 150

                    arg_MaxSpace_nCR, arg_MinSpace_nCR = min(6*arg_MB_Dia, 150), 100.0
                    arg_Space_nCR_required = 1.0 if min(arg_Space_nCR_X, arg_Space_nCR_Y, arg_MaxSpace_nCR) < arg_MinSpace_nCR else min(arg_Space_nCR_X, arg_Space_nCR_Y, arg_MaxSpace_nCR)

                    for tmp2 in tmpSB_Space_List:
                        if (tmp2 < arg_Space_nCR_required) or (abs(tmp2-arg_Space_nCR_required) < 1):
                            arg_Space_nCR = tmp2
                            break
                    
                    if arg_Space_nCR == False:   #   要上升一個號數，不然會低於100mm
                        continue

                    # ============================================================== 確認離開
                    if arg_Space_CR and arg_Space_nCR:
                        break
            
            arg_As2_CR_pro = (2 * arg_SB_Area + arg_TNx * arg_TB_Area) / arg_Space_CR
            arg_As2_nCR_pro = (2 * arg_SB_Area + arg_TNx * arg_TB_Area) / arg_Space_nCR
            
            arg_As3_CR_pro = (2 * arg_SB_Area + arg_TNy * arg_TB_Area) / arg_Space_CR
            arg_As3_nCR_pro = (2 * arg_SB_Area + arg_TNy * arg_TB_Area) / arg_Space_nCR


            string_Nx1Nx2 = f'{arg_Nx1}+{arg_Nx2}'
            string_Ny1Ny2 = f'{arg_Ny1}+{arg_Ny2}'

            arg_warning = 'Tie bar number exceed main bar numbe!' if arg_TNx>(arg_Ny1-2) or arg_TNy>(arg_Nx1-2) else '---'

            # reqSecBarDesign
            reqSecBarDesign.append([arg_FloorGroup, arg_ColumnGroup, arg_X0, arg_Y0, arg_RebarType, arg_Cover, arg_MB_Name, arg_SB_Name, arg_TB_Name, arg_Space_CR, arg_Space_nCR, arg_Dx, arg_Dy, arg_fc, arg_fys, string_Nx1Nx2, string_Ny1Ny2, arg_TNx, arg_TNy, arg_warning, arg_ModelColumnList])
            
            # export for check
            reqExportRectangular.append([
                                arg_FloorGroup, arg_ColumnGroup, arg_RebarType, arg_Dx, arg_Dy, arg_MB_Name, arg_SB_Name, arg_TB_Name, arg_Space_CR, arg_Space_nCR, arg_MainBar_total, arg_MainBar_pro, arg_MainBar_PMMRatio, 
                                arg_As2_CR_Ash1, arg_As2_CR_Ash2, arg_As2_CR_Ash3, arg_As2_CR_Reqd, arg_As2_nCR_governed, arg_TNx, arg_As2_CR_pro,arg_As2_nCR_pro,
                                arg_As3_CR_Ash1, arg_As3_CR_Ash2, arg_As3_CR_Ash3, arg_As3_CR_Reqd, arg_As3_nCR_governed, arg_TNy, arg_As3_CR_pro,arg_As3_nCR_pro, arg_Pu, arg_fc, arg_ModelMemberList
            ])



        elif arg_ColShape == 'Circle':

            # 主筋設計放大值--目前沒使用 固定1.0
            main_bar_application = 1.0
            arg_MainBar_req = max(arg_MainBar) * main_bar_application

            # 斷面性質
            arg_MB_Dia = dictBarDia[arg_MB_Name]    # 需確認ETABS名稱一致
            arg_MB_Area = dictBarArea[arg_MB_Name]

            # 最小鋼筋間距
            arg_RebarC2C = max(1.5*arg_MB_Dia + 1.145*arg_MB_Dia, 40+arg_MB_Dia, 1.33*25+arg_MB_Dia)

            # 計算主要鋼筋配置(N1第一層,N2第二層)
            arg_Na = max(arg_N3)

            # max_BarNo = int(math.floor((arg_Dy - 2*arg_Cover - 2*arg_SB_Dia - arg_MB_Dia) / (arg_RebarC2C)) + 1 - argColumnBarMinus)    #   計算出來的最大根數減少輸入根數
            max_BarNo = int(math.floor((math.pi * (arg_Dx - 2*40 - 2*arg_SB_Dia - arg_MB_Dia) / arg_RebarC2C) / 4) * 4)

            arg_N1 = max_BarNo
            arg_N2 = arg_Na - arg_N1
            

            # 紀錄總鋼筋量
            arg_MainBar_total = arg_Na
            arg_MainBar_pro = arg_MainBar_total * arg_MB_Area
            arg_MainBar_PMMRatio = max(arg_PMM)

            # # 主筋淨間距(不須檢核，計算N1 & N2時已考慮)

            # ====================================================================================================================== for shear bar design 剪力鋼筋計算
            arg_Ach = (0.25 * math.pi * (arg_Dx - 2*40)**2)
            arg_C2C = math.pi * (arg_Dx - 2*40 - arg_SB_Dia) / max_BarNo

            # 軸力檢核
            tmpAxialLoadCondition1 = (arg_Pu > 0.3*(arg_Ag/10/10)*arg_fc/1000)
            tmpAxialLoadCondition2 = (arg_fc > 700)


            # ============================================================== 圍束區
            tmpSBCondition = []
            if '#' in arg_MB_Name:
                for tmpSB in ['#4', '#5', '#6']:
                    for tmpNo in [1, 2]:                
                        for tmpSS in [150.0, 125.0, 100.0]:
                            tmpSBCondition.append([tmpNo, tmpSB, tmpSS])
            else:
                for tmpSB in ['D13', 'D16', 'D19']:
                    for tmpNo in [1, 2]:                
                        for tmpSS in [150.0, 125.0, 100.0]:
                            tmpSBCondition.append([tmpNo, tmpSB, tmpSS])


            for sbc in tmpSBCondition:
                tmpNo, tmpSB, tmpSS = sbc

                # 箍繫筋資訊
                arg_SB_Name = tmpSB
                arg_TB_Name = tmpSB
                arg_SB_Dia = dictBarDia[arg_SB_Name]
                arg_TB_Dia = dictBarDia[arg_TB_Name]
                arg_SB_Area = dictBarArea[arg_SB_Name]
                arg_TB_Area = dictBarArea[arg_TB_Name]
                
                # X向耐震需求
                arg_As2_CR_Ash1 = seismic_shear_design_formula_C1(arg_Ag, arg_Ach, arg_fc, arg_fys)
                arg_As2_CR_Ash2 = seismic_shear_design_formula_C2(arg_fc, arg_fys)

                if tmpAxialLoadCondition1 or tmpAxialLoadCondition2:
                    arg_As2_CR_Ash3 = seismic_shear_design_formula_C3(arg_Pu, arg_Ach, arg_fc, arg_fys)
                else:
                    arg_As2_CR_Ash3 = 0.0


                # X向剪力筋需求
                arg_As2_CR_Reqd = max(arg_As2_CR)                    


                # Y向耐震需求推算間距
                arg_As3_CR_Ash1 = seismic_shear_design_formula_C1(arg_Ag, arg_Ach, arg_fc, arg_fys)
                arg_As3_CR_Ash2 = seismic_shear_design_formula_C2(arg_fc, arg_fys)                

                if tmpAxialLoadCondition1 or tmpAxialLoadCondition2:
                    arg_As3_CR_Ash3 = seismic_shear_design_formula_C3(arg_Pu, arg_Ach, arg_fc, arg_fys)
                else:
                    arg_As3_CR_Ash3 = 0.0


                # Y向剪力筋需求
                arg_As3_CR_Reqd = max(arg_As3_CR)

                # 檢核
                arg_Ratio_X1 = ((arg_Ach * tmpSS) * max(arg_As2_CR_Ash1, arg_As2_CR_Ash2, arg_As2_CR_Ash3)) / (tmpNo * arg_SB_Area * math.pi * (arg_Dx - 2*40 - arg_SB_Dia))
                arg_Check_X1 = True if arg_Ratio_X1 < 1.0 else False

                arg_Ratio_X2 = (arg_As2_CR_Reqd) / (tmpNo * (2*arg_SB_Area) / tmpSS)
                arg_Check_X2 = True if arg_Ratio_X2 < 1.0 else False

                arg_Ratio_Y1 = ((arg_Ach * tmpSS) * max(arg_As3_CR_Ash1, arg_As3_CR_Ash2, arg_As3_CR_Ash3)) / (tmpNo * arg_SB_Area * math.pi * (arg_Dx - 2*40 - arg_SB_Dia))
                arg_Check_Y1 = True if arg_Ratio_Y1 < 1.0 else False

                arg_Ratio_Y2 = (arg_As3_CR_Reqd) / (tmpNo * (2*arg_SB_Area) / tmpSS)
                arg_Check_Y2 = True if arg_Ratio_Y2 < 1.0 else False

                if arg_Check_X1 and arg_Check_X2 and arg_Check_Y1 and arg_Check_Y2:
                    arg_SBno_CR     = tmpNo
                    arg_SB_CR       = tmpSB
                    arg_SBSpace_CR  = tmpSS
                    break

            # ============================================================== 非圍束區
            tmpSBCondition = []
            if '#' in arg_SB_CR:
                for tmpNo in [1, 2]:                
                    for tmpSS in [150.0, 125.0, 100.0]:
                        tmpSBCondition.append([tmpNo, arg_SB_CR, tmpSS])
            else:
                for tmpNo in [1, 2]:                
                    for tmpSS in [150.0, 125.0, 100.0]:
                        tmpSBCondition.append([tmpNo, arg_SB_CR, tmpSS])


            for sbc in tmpSBCondition:
                tmpNo, tmpSB, tmpSS = sbc

                # 箍繫筋資訊
                arg_SB_Name = tmpSB
                arg_TB_Name = tmpSB
                arg_SB_Dia = dictBarDia[arg_SB_Name]
                arg_TB_Dia = dictBarDia[arg_TB_Name]
                arg_SB_Area = dictBarArea[arg_SB_Name]
                arg_TB_Area = dictBarArea[arg_TB_Name]

                # X向剪力筋需求
                arg_As2_nCR_Reqd = max(arg_As2_nCR)
                
                # Y向剪力筋需求
                arg_As3_nCR_Reqd = max(arg_As3_nCR)

                arg_Ratio_X3 = (arg_As2_nCR_Reqd) / (tmpNo * (2*arg_SB_Area) / tmpSS)
                arg_Check_X3 = True if arg_Ratio_X3 < 1.0 else False

                arg_Ratio_Y3 = (arg_As3_nCR_Reqd) / (tmpNo * (2*arg_SB_Area) / tmpSS)
                arg_Check_Y3 = True if arg_Ratio_Y3 < 1.0 else False

                if arg_Check_X3 and arg_Check_Y3:
                    arg_SBno_nCR    = tmpNo
                    arg_SB_nCR      = tmpSB
                    arg_SBSpace_nCR = tmpSS
                    break


            string_Nx1Nx2 = f'{arg_N1}+{arg_N2}'
            string_Ny1Ny2 = f'0'

            arg_warning = '---'


            # reqSecBarDesign
            reqSecBarDesign.append([arg_FloorGroup, arg_ColumnGroup, arg_X0, arg_Y0, arg_RebarType, arg_Cover, arg_MB_Name, arg_SB_CR, arg_SB_CR, arg_SBSpace_CR, arg_SBSpace_nCR, 'Circle', arg_Dx, arg_fc, arg_fys, string_Nx1Nx2, string_Ny1Ny2, arg_SBno_CR, arg_SBno_nCR, arg_warning, arg_ModelColumnList])

            # export for check
            reqExportCircle.append([
                                arg_FloorGroup, arg_ColumnGroup, arg_RebarType, arg_Dx, arg_MB_Name, arg_SB_CR, arg_SBSpace_CR, arg_SBSpace_nCR, arg_SBno_CR, arg_SBno_nCR, arg_MainBar_total, arg_MainBar_pro, arg_MainBar_PMMRatio, 
                                arg_As2_CR_Ash1, arg_As2_CR_Ash2, arg_As2_CR_Ash3, arg_As2_CR_Reqd, arg_As2_nCR_Reqd, 
                                arg_As3_CR_Ash1, arg_As3_CR_Ash2, arg_As3_CR_Ash3, arg_As3_CR_Reqd, arg_As3_nCR_Reqd, 
                                arg_Pu, arg_fc, arg_Ach, arg_ModelMemberList
            ])





    # Export Required Section Bar Design
    if reqSecBarDesign:
        tmpColumns = [
            'story_group','column_group','xlocation','ylocation','rebar_type','cover_mm',
            'mainbar_mark','stirrupbar_mark','tiebar_mark','CR_tiespace','nonCR_tiespace',
            'Dx_mm','Dy_mm','fc\'_kg/cm2','fys_kg/cm2','Nx','Ny','TNx','TNy','warning','ModelColumnList'
            ]
        df_reqSecBarDesign = pd.DataFrame(reqSecBarDesign, columns=tmpColumns)


    # Export Required for Regular
    if reqExportRectangular:
        tmpColumns = [
            'FloorGroup', 'ColumnGroup', 'RebarType', 'Dx', 'Dy', 'MB_Name', 'SB_Name', 'TB_Name', 'Space_CR', 'Space_nCR', 'MBtotal', 'MBpro', 'PMMRatio',
            'As2_CR_Ash1', 'As2_CR_Ash2', 'As2_CR_Ash3', 'As2_CR_Reqd', 'As2_nCR_Reqd', 'TNx', 'As2_CR_pro', 'As2_nCR_pro',
            'As3_CR_Ash1', 'As3_CR_Ash2', 'As3_CR_Ash3', 'As3_CR_Reqd', 'As3_nCR_Reqd', 'TNy', 'As3_CR_pro', 'As3_nCR_pro', 'Pu', 'fc', 'ModelMemberList'
        ]
        df_reqExportRectangular = pd.DataFrame(reqExportRectangular, columns=tmpColumns)

    else:
        df_reqExportRectangular = ''


    # Export Required for Circle
    if reqExportCircle:
        tmpColumns = [
            'FloorGroup', 'ColumnGroup', 'RebarType', 'Dia', 'MB_Name', 'SB_Name', 'SBSpace_CR', 'SBSpace_nCR', 'SBno_CR', 'SBno_nCR', 'MainBar_total', 'MainBar_pro', 'MainBar_PMMRatio', 
            'As2_CR_Ash1', 'As2_CR_Ash2', 'As2_CR_Ash3', 'As2_CR_Reqd', 'As2_nCR_Reqd', 
            'As3_CR_Ash1', 'As3_CR_Ash2', 'As3_CR_Ash3', 'As3_CR_Reqd', 'As3_nCR_Reqd', 
            'Pu', 'fc', 'Ach', 'ModelMemberList'
        ]
        df_reqExportCircle = pd.DataFrame(reqExportCircle, columns=tmpColumns)

    else:
        df_reqExportCircle = ''





    return(df_reqSecBarDesign, df_reqExportRectangular, df_reqExportCircle)


# if __name__ == '__main__':
#         main()