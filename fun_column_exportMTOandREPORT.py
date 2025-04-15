# coding=UTF-8
# import os
import math
# import Draw as Draw
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


def get_Total_ReBar(StringData):
    V1, V2 = StringData.split('+')
    return int(int(V1)+int(V2))


def  exportREPORT_Rectangular(dict_column_rebar_design, reqExportRectangularSectionData, dictBarArea):

    exportString = ''

    for index1, row1 in reqExportRectangularSectionData.iterrows():
        FloorGroup, ColumnGroup, RebarType, Dx, Dy, MB_Name, SB_Name, TB_Name, Space_CR, Space_nCR, MBtotal, MBpro, PMMRatio, \
        As2_CR_Ash1, As2_CR_Ash2, As2_CR_Ash3, As2_CR_Reqd, As2_nCR_Reqd, TNx, As2_CR_pro, As2_nCR_pro, \
        As3_CR_Ash1, As3_CR_Ash2, As3_CR_Ash3, As3_CR_Reqd, As3_nCR_Reqd, TNy, As3_CR_pro, As3_nCR_pro, arg_Pu, arg_fc, arg_ModelMemberList = row1

        # for index2, row2 in dict_column_rebar_design.iterrows():
        # # for datas in final_rebar:
        #     if FloorGroup == datas[0] and ColumnGroup == datas[1]:
        #         SB_Name     = datas[7]
        #         TB_Name     = datas[8]
        #         Space_CR    = float(datas[9])
        #         Space_nCR   = float(datas[10])

        #         As2_CR_pro  = (dictBarArea[SB_Name]*2+dictBarArea[TB_Name]*TNx) / Space_CR
        #         As3_CR_pro  = (dictBarArea[SB_Name]*2+dictBarArea[TB_Name]*TNy) / Space_CR
        #         As2_nCR_pro = (dictBarArea[SB_Name]*2+dictBarArea[TB_Name]*TNx) / Space_nCR
        #         As3_nCR_pro = (dictBarArea[SB_Name]*2+dictBarArea[TB_Name]*TNy) / Space_nCR

        #         break

            

        # write for report
        tmpWidth = 7
        tmpPrecision = 3

        exportString += '========================================================================================================\n'
        exportString += f'@FloorGroup: {FloorGroup}    @ColGroup: {ColumnGroup}    @Section: {Dx:.0f}X{Dy:.0f}\n'


        exportString += f'@Model Floor-Label: '
        for index, tmp in enumerate(arg_ModelMemberList.split()):
            tmpV1, tmpV2 = divmod(index, 7)

            if tmpV2 == 0 and index != 0:
                exportString += f'{tmp}  \n                    '
            else:
                exportString += f'{tmp}  '
        if index % 7 == 0:                
            exportString += '\n'
        else:
            exportString += '\n'
            exportString += '\n'


        tmpRebarAssignMB            = str(MBtotal) + '-' + str(MB_Name)
        tmpRebarAssignStirTieX_CR   = '(' + str(SB_Name)+' Sti.+ '+ str(TNx) + '-' + str(TB_Name) + ' Tie)@' + f'{Space_CR:<.0f}'
        tmpRebarAssignStirTieY_CR   = '(' + str(SB_Name)+' Sti.+ '+ str(TNy) + '-' + str(TB_Name) + ' Tie)@' + f'{Space_CR:<.0f}'
        tmpRebarAssignStirTieX_nCR  = '(' + str(SB_Name)+' Sti.+ '+ str(TNx) + '-' + str(TB_Name) + ' Tie)@' + f'{Space_nCR:<.0f}'
        tmpRebarAssignStirTieY_nCR  = '(' + str(SB_Name)+' Sti.+ '+ str(TNy) + '-' + str(TB_Name) + ' Tie)@' + f'{Space_nCR:<.0f}'

        tmpRebarCheckMB             = 'OK' if PMMRatio < 1.0 else 'NG'

        tmpBigAxialLoadCheck      = True if ( arg_Pu > (0.3 * Dx * Dy * arg_fc / 100000)) or (arg_fc > 700) else False

        tmpRebarCheckStirTieX_CR    = 'OK' if As2_CR_pro  > max(As2_CR_Ash1, As2_CR_Ash2, As2_CR_Ash3, As2_CR_Reqd) else 'NG'
        tmpRebarCheckStirTieY_CR    = 'OK' if As3_CR_pro  > max(As3_CR_Ash1, As3_CR_Ash2, As3_CR_Ash3, As3_CR_Reqd) else 'NG'
        tmpRebarCheckStirTieX_nCR   = 'OK' if As2_nCR_pro > As2_nCR_Reqd else 'NG'
        tmpRebarCheckStirTieY_nCR   = 'OK' if As3_nCR_pro > As3_nCR_Reqd else 'NG'
        

        exportString += f'(A) For Main Bar Check:\n'
        exportString += f'{"    Main-Rebar":<{tmpWidth*4}} = {tmpRebarAssignMB:<{tmpWidth}}\n'
        exportString += f'{"    Max.PMM Ratio":<{tmpWidth*4}} = {PMMRatio:<{tmpWidth}.{tmpPrecision}f}\n'
        exportString += f'{"    Check":<{tmpWidth*4}} = {tmpRebarCheckMB:<{tmpWidth}}\n'
        exportString += '\n'


        exportString += f'(B) Confined Regin Check: (unit: mm2/mm)\n'
        tmpString = '    Pu'
        exportString += f'{tmpString:<{tmpWidth*4}} = {arg_Pu:<{tmpWidth}.{tmpPrecision}f} tonf\n'
        tmpString = '    0.3Agfc\''
        exportString += f'{tmpString:<{tmpWidth*4}} = {(0.3 * Dx * Dy * arg_fc / 100000):<{tmpWidth}.{tmpPrecision}f} tonf\n'
        tmpString = '    fc\''
        exportString += f'{tmpString:<{tmpWidth*4}} = {arg_fc:<{tmpWidth}.0f} kg/cm2\n'
        if tmpBigAxialLoadCheck:
            tmpString = '    Check Pu>0.3Agfc\' or fc\'>700 kg/cm2 --- Yes, Av,req3 should be considered.\n'
        else:
            tmpString = '    Check Pu>0.3Agfc\' or fc\'>700 kg/cm2 --- No, Av,req3 should NOT be considered (Use Av,req3 = 0.000).\n'
        exportString += f'{tmpString:<{tmpWidth*6}}\n'


        tmpString = "    [X-Dir]                                             [Y-Dir]"
        exportString += f'{tmpString}'
        exportString += '\n'
        tmpString = "    -------------------------------------------------   ------------------------------------------------"
        exportString += f'{tmpString}'
        exportString += '\n'

        tmpString = f'{"    Stirrup & Tie = ":<{tmpWidth*3}}{tmpRebarAssignStirTieX_CR:<{tmpWidth*4}}   '
        exportString += f'{tmpString}'
        tmpString = f'{"    Stirrup & Tie = ":<{tmpWidth*3}}{tmpRebarAssignStirTieY_CR:<{tmpWidth*4}}   '
        exportString += f'{tmpString}'
        exportString += '\n'*2

        tmpString = f'{"    (Av/s)req1 = bc*0.3*fc/fy*(Ag/Ach-1)":<{tmpWidth*6}} = {As2_CR_Ash1:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        tmpString = f'{"    (Av/s)req1 = bc*0.3*fc/fy*(Ag/Ach-1)":<{tmpWidth*6}} = {As3_CR_Ash1:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        exportString += '\n'

        tmpString = f'{"    (Av/s)req2 = bc*0.09*fc/fy":<{tmpWidth*6}} = {As2_CR_Ash2:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        tmpString = f'{"    (Av/s)req2 = bc*0.09*fc/fy":<{tmpWidth*6}} = {As3_CR_Ash2:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        exportString += '\n'

        tmpString = f'{"    (Av/s)req3 = bc*0.2*kf*kn*Pu/fyt/Ach":<{tmpWidth*6}} = {As2_CR_Ash3:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        tmpString = f'{"    (Av/s)req3 = bc*0.2*kf*kn*Pu/fyt/Ach":<{tmpWidth*6}} = {As3_CR_Ash3:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        exportString += '\n'

        tmpString = f'{"    (Av/s)req4 = requiredment from model":<{tmpWidth*6}} = {As2_CR_Reqd:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        tmpString = f'{"    (Av/s)req4 = requiredment from model":<{tmpWidth*6}} = {As3_CR_Reqd:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        exportString += '\n'

        tmpString = f'{"    (Av/s)pro":<{tmpWidth*6}} = {As2_CR_pro:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        tmpString = f'{"    (Av/s)pro":<{tmpWidth*6}} = {As3_CR_pro:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        exportString += '\n'

        tmpString = f'{"    Check (Av/s)pro > (Av/s)req":<{tmpWidth*6}} = {tmpRebarCheckStirTieX_CR:<{tmpWidth}}'
        exportString += f'{tmpString}'
        tmpString = f'{"    Check (Av/s)pro > (Av/s)req":<{tmpWidth*6}} = {tmpRebarCheckStirTieY_CR:<{tmpWidth}}'
        exportString += f'{tmpString}'
        exportString += '\n'*2


        exportString += f'(C) Non-Confined Regin Check: (unit: mm2/mm)\n'

        tmpString = "    [X-Dir]                                             [Y-Dir]"
        exportString += f'{tmpString}'
        exportString += '\n'
        tmpString = "    -------------------------------------------------   ------------------------------------------------"
        exportString += f'{tmpString}'
        exportString += '\n'

        tmpString = f'{"    Stirrup & Tie = ":<{tmpWidth*3}}   {tmpRebarAssignStirTieX_nCR:<{tmpWidth*4}}'
        exportString += f'{tmpString}'
        tmpString = f'{"    Stirrup & Tie = ":<{tmpWidth*3}}   {tmpRebarAssignStirTieY_nCR:<{tmpWidth*4}}'
        exportString += f'{tmpString}'
        exportString += '\n'*2
        # out_report.write(f'{"Arrangement = ":>{tmpWidth}}{tmpRebarAssignStirTieX_nCR:<{tmpWidth}}{"Arrangement = ":>{tmpWidth}}{tmpRebarAssignStirTieY_nCR:<{tmpWidth}}\n')
        # out_report.write('\n')

        tmpString = f'{"    (Av/s)req = requiredment from model":<{tmpWidth*6}} = {As2_nCR_Reqd:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        tmpString = f'{"    (Av/s)req = requiredment from model":<{tmpWidth*6}} = {As3_nCR_Reqd:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        exportString += '\n'
        # out_report.write(f'{"Av,req = ":>{tmpWidth}}{"required from model":<{tmpWidth}}{"Av,req = ":>{tmpWidth}}{"required from model":<{tmpWidth}}\n')
        # out_report.write(f'{"= ":>{tmpWidth}}{As2_nCR_Reqd:<{tmpWidth}.{tmpPrecision}f}{"= ":>{tmpWidth}}{As3_nCR_Reqd:<{tmpWidth}.{tmpPrecision}f}\n')
        # out_report.write('\n')

        tmpString = f'{"    (Av/s)pro":<{tmpWidth*6}} = {As2_nCR_pro:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        tmpString = f'{"    (Av/s)pro":<{tmpWidth*6}} = {As3_nCR_pro:<{tmpWidth}.{tmpPrecision}f}'
        exportString += f'{tmpString}'
        exportString += '\n'
        # out_report.write(f'{"Av,pro = ":>{tmpWidth}}{As2_nCR_pro:<{tmpWidth}.{tmpPrecision}f}{"Av,pro = ":>{tmpWidth}}{As3_nCR_pro:<{tmpWidth}.{tmpPrecision}f}\n')
        # out_report.write('\n')

        tmpString = f'{"    Check (Av/s)pro > (Av/s)req":<{tmpWidth*6}} = {tmpRebarCheckStirTieX_nCR:<{tmpWidth}}'
        exportString += f'{tmpString}'
        tmpString = f'{"    Check (Av/s)pro > (Av/s)req":<{tmpWidth*6}} = {tmpRebarCheckStirTieY_nCR:<{tmpWidth}}'
        exportString += f'{tmpString}'
        exportString += '\n'
        # out_report.write(f'{"Check = ":>{tmpWidth}}{tmpRebarCheckStirTieX_nCR:<{tmpWidth}}{"Check = ":>{tmpWidth}}{tmpRebarCheckStirTieY_nCR:<{tmpWidth}}\n')
        # out_report.write('\n')


    return exportString


def exportREPORT_Circle(file_folder, tmpREPORTData, dictBarDia, dictBarArea, final_rebar):
    # out_report = open(os.path.join(file_folder, 'ColumnDesign', 'Col_Out04c_Report_ColDesign_Circle.txt'), 'w')

    # for tmp in tmpREPORTData:
    #     index, FloorGroup, ColumnGroup, RebarType, Dia, MB_Name, SB_Name, SBSpace_CR, SBSpace_nCR, SBno_CR, SBno_nCR, MBtotal, MBpro, PMMRatio, \
    #     As2_CR_Ash1, As2_CR_Ash2, As2_CR_Ash3, As2_CR_Reqd, As2_nCR_Reqd, \
    #     As3_CR_Ash1, As3_CR_Ash2, As3_CR_Ash3, As3_CR_Reqd, As3_nCR_Reqd, \
    #     arg_Pu, arg_fc, arg_Ach, arg_ModelMemberList = tmp


    #     for datas in final_rebar:
    #         if FloorGroup == datas[0] and ColumnGroup == datas[1]:
    #             SB_Name     = datas[7]
    #             SBSpace_CR    = float(datas[9])
    #             SBSpace_nCR   = float(datas[10])
    #             break

    #     arg_SB_Area = dictBarArea[SB_Name]
    #     arg_SB_Dia  = dictBarDia[SB_Name]

    #     # write for report
    #     tmpWidth = 7
    #     tmpPrecision = 3

    #     out_report.write('========================================================================================================\n')
    #     out_report.write(f'@FloorGroup: {FloorGroup}    @ColGroup: {ColumnGroup}    @Section: Dia. {Dia:.0f}\n')

    #     out_report.write(f'@Model Floor-Label: ')
    #     for index, tmp in enumerate(arg_ModelMemberList.split()):
    #         tmpV1, tmpV2 = divmod(index, 7)

    #         if tmpV2 == 0 and index != 0:
    #             out_report.write(f'{tmp}  \n                    ')
    #         else:
    #             out_report.write(f'{tmp}  ')
    #     if index % 7 == 0:                
    #         out_report.write('\n')
    #     else:
    #         out_report.write('\n')
    #         out_report.write('\n')


    #     tmpRebarAssignMB        = str(MBtotal) + '-' + str(MB_Name)
    #     tmpRebarAssignStir_CR   = '(' + str(SBno_CR) + '-' + str(SB_Name)+' Sti. + ' + str(SB_Name) + ' Tie)@' + f'{SBSpace_CR:<.0f}'
    #     tmpRebarAssignStir_nCR  = '(' + str(SBno_nCR) + '-' + str(SB_Name)+' Sti. + ' + str(SB_Name) + ' Tie)@' + f'{SBSpace_nCR:<.0f}'

    #     tmpRebarCheckMB         = 'OK' if PMMRatio < 1.0 else 'NG'

    #     tmpBigAxialLoadCheck    = True if ( arg_Pu > (0.3 * (0.25*math.pi*Dia*Dia) * arg_fc / 100000)) or (arg_fc > 700) else False

    #     tmpRebarStirCheckX1     = 'OK' if (SBno_CR * arg_SB_Area * math.pi * (Dia - 2*40 - arg_SB_Dia)) > ((arg_Ach * SBSpace_CR) * max( As2_CR_Ash1, As2_CR_Ash2, As2_CR_Ash3))    else 'NG'
    #     tmpRebarStirCheckX2     = 'OK' if (SBno_CR * (2*arg_SB_Area) / SBSpace_CR)                      > (As2_CR_Reqd)                                                             else 'NG'
    #     tmpRebarStirCheckX3     = 'OK' if (SBno_nCR * (2*arg_SB_Area) / SBSpace_nCR)                    > (As2_nCR_Reqd)                                                            else 'NG'

    #     tmpRebarStirCheckY1     = 'OK' if (SBno_CR * arg_SB_Area * math.pi * (Dia - 2*40 - arg_SB_Dia)) > ((arg_Ach * SBSpace_CR) * max( As3_CR_Ash1, As3_CR_Ash2, As3_CR_Ash3))    else 'NG'
    #     tmpRebarStirCheckY2     = 'OK' if (SBno_CR * (2*arg_SB_Area) / SBSpace_CR)                      > (As3_CR_Reqd)                                                             else 'NG'
    #     tmpRebarStirCheckY3     = 'OK' if (SBno_nCR * (2*arg_SB_Area) / SBSpace_nCR)                    > (As3_nCR_Reqd)                                                            else 'NG'



    #     out_report.write(f'(A) For Main Bar Check:\n')
    #     out_report.write(f'{"    Main-Rebar":<{tmpWidth*4}} = {tmpRebarAssignMB:<{tmpWidth}}\n')
    #     out_report.write(f'{"    Max.PMM Ratio":<{tmpWidth*4}} = {PMMRatio:<{tmpWidth}.{tmpPrecision}f}\n')
    #     out_report.write(f'{"    Check":<{tmpWidth*4}} = {tmpRebarCheckMB:<{tmpWidth}}\n')
    #     out_report.write('\n')


    #     out_report.write(f'(B) Confined Regin Check: (unit: mm2/mm)\n')
    #     tmpString = '    Pu'
    #     out_report.write(f'{tmpString:<{tmpWidth*4}} = {arg_Pu:<{tmpWidth}.{tmpPrecision}f} tonf\n')
    #     tmpString = '    0.3Agfc\''
    #     out_report.write(f'{tmpString:<{tmpWidth*4}} = {(0.3 * (0.25*math.pi*Dia*Dia) * arg_fc / 100000):<{tmpWidth}.{tmpPrecision}f} tonf\n')
    #     tmpString = '    fc\''
    #     out_report.write(f'{tmpString:<{tmpWidth*4}} = {arg_fc:<{tmpWidth}.0f} kg/cm2\n')
    #     if tmpBigAxialLoadCheck:
    #         tmpString = '    Check Pu>0.3Agfc\' or fc\'>700 kg/cm2 --- Yes, ρs,req3 should be considered.\n'
    #     else:
    #         tmpString = '    Check Pu>0.3Agfc\' or fc\'>700 kg/cm2 --- No, ρs,req3 should NOT be considered (Use ρs,req3 = 0.000).\n'
    #     out_report.write(f'{tmpString:<{tmpWidth*6}}\n')


    #     tmpString = "    [X-Dir]                                             [Y-Dir]"
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')
    #     tmpString = "    -------------------------------------------------   ------------------------------------------------"
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')

    #     tmpString = f'{"    Stirrup & Tie = ":<{tmpWidth*3}}{tmpRebarAssignStir_CR:<{tmpWidth*4}}   '
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    Stirrup & Tie = ":<{tmpWidth*3}}{tmpRebarAssignStir_CR:<{tmpWidth*4}}   '
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n'*2)

    #     tmpString = f'{"    ρs,req1 = 0.45*fc/fy*(Ag/Ach-1)":<{tmpWidth*6}} = {As2_CR_Ash1:<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    ρs,req1 = 0.45*fc/fy*(Ag/Ach-1)":<{tmpWidth*6}} = {As3_CR_Ash1:<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')

    #     tmpString = f'{"    ρs,req2 = 0.12*fc/fy":<{tmpWidth*6}} = {As2_CR_Ash2:<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    ρs,req2 = 0.12*fc/fy":<{tmpWidth*6}} = {As3_CR_Ash2:<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')

    #     tmpString = f'{"    ρs,req3 = 0.35*kf*Pu/fyt/Ach":<{tmpWidth*6}} = {As2_CR_Ash3:<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    ρs,req3 = 0.35*kf*Pu/fyt/Ach":<{tmpWidth*6}} = {As3_CR_Ash3:<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')

    #     tmpString = f'{"    Center RC Volume * max(ρs) (CRCV)":<{tmpWidth*6}} = {((arg_Ach * SBSpace_CR) * max( As2_CR_Ash1, As2_CR_Ash2, As2_CR_Ash3)):<{tmpWidth}.1e}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    Center RC Volume * max(ρs) (CRCV)":<{tmpWidth*6}} = {((arg_Ach * SBSpace_CR) * max( As2_CR_Ash1, As2_CR_Ash2, As2_CR_Ash3)):<{tmpWidth}.1e}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')

    #     tmpString = f'{"    Closed Stirrup Volumn (CSV)":<{tmpWidth*6}} = {(SBno_CR * arg_SB_Area * math.pi * (Dia - 2*40 - arg_SB_Dia)):<{tmpWidth}.1e}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    Closed Stirrup Volumn (CSV)":<{tmpWidth*6}} = {(SBno_CR * arg_SB_Area * math.pi * (Dia - 2*40 - arg_SB_Dia)):<{tmpWidth}.1e}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')


    #     tmpString = f'{"    Check CSV > CRCV":<{tmpWidth*6}} = {tmpRebarStirCheckX1:<{tmpWidth}}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    Check CSV > CRCV":<{tmpWidth*6}} = {tmpRebarStirCheckY1:<{tmpWidth}}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')
    #     out_report.write('\n')


    #     tmpString = f'{"    (Av/s)req = requiredment from model":<{tmpWidth*6}} = {As2_CR_Reqd:<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    (Av/s)req = requiredment from model":<{tmpWidth*6}} = {As3_CR_Reqd:<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')

    #     tmpString = f'{"    (Av/s)pro":<{tmpWidth*6}} = {(SBno_CR * (2*arg_SB_Area) / SBSpace_CR):<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    (Av/s)pro":<{tmpWidth*6}} = {(SBno_CR * (2*arg_SB_Area) / SBSpace_CR):<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')

    #     tmpString = f'{"    Check (Av/s)pro > (Av/s)req":<{tmpWidth*6}} = {tmpRebarStirCheckX2:<{tmpWidth}}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    Check (Av/s)pro > (Av/s)req":<{tmpWidth*6}} = {tmpRebarStirCheckY2:<{tmpWidth}}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')
    #     out_report.write('\n')



    #     out_report.write(f'(C) Non-Confined Regin Check: (unit: mm2/mm)\n')

    #     tmpString = "    [X-Dir]                                             [Y-Dir]"
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')
    #     tmpString = "    -------------------------------------------------   ------------------------------------------------"
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')

    #     tmpString = f'{"    Stirrup & Tie = ":<{tmpWidth*3}}   {tmpRebarAssignStir_nCR:<{tmpWidth*4}}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    Stirrup & Tie = ":<{tmpWidth*3}}   {tmpRebarAssignStir_nCR:<{tmpWidth*4}}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n'*2)
        

    #     tmpString = f'{"    (Av/s)req = requiredment from model":<{tmpWidth*6}} = {As2_nCR_Reqd:<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    (Av/s)req = requiredment from model":<{tmpWidth*6}} = {As3_nCR_Reqd:<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')
    #     # out_report.write(f'{"Av,req = ":>{tmpWidth}}{"required from model":<{tmpWidth}}{"Av,req = ":>{tmpWidth}}{"required from model":<{tmpWidth}}\n')
    #     # out_report.write(f'{"= ":>{tmpWidth}}{As2_nCR_Reqd:<{tmpWidth}.{tmpPrecision}f}{"= ":>{tmpWidth}}{As3_nCR_Reqd:<{tmpWidth}.{tmpPrecision}f}\n')
    #     # out_report.write('\n')

    #     tmpString = f'{"    (Av/s)pro":<{tmpWidth*6}} = {(SBno_nCR * (2*arg_SB_Area) / SBSpace_nCR):<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    (Av/s)pro":<{tmpWidth*6}} = {(SBno_nCR * (2*arg_SB_Area) / SBSpace_nCR):<{tmpWidth}.{tmpPrecision}f}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')
    #     # out_report.write(f'{"Av,pro = ":>{tmpWidth}}{As2_nCR_pro:<{tmpWidth}.{tmpPrecision}f}{"Av,pro = ":>{tmpWidth}}{As3_nCR_pro:<{tmpWidth}.{tmpPrecision}f}\n')
    #     # out_report.write('\n')

    #     tmpString = f'{"    Check (Av/s)pro > (Av/s)req":<{tmpWidth*6}} = {tmpRebarStirCheckX3:<{tmpWidth}}'
    #     out_report.write(f'{tmpString}')
    #     tmpString = f'{"    Check (Av/s)pro > (Av/s)req":<{tmpWidth*6}} = {tmpRebarStirCheckY3:<{tmpWidth}}'
    #     out_report.write(f'{tmpString}')
    #     out_report.write('\n')
    #     # out_report.write(f'{"Check = ":>{tmpWidth}}{tmpRebarCheckStirTieX_nCR:<{tmpWidth}}{"Check = ":>{tmpWidth}}{tmpRebarCheckStirTieY_nCR:<{tmpWidth}}\n')
    #     # out_report.write('\n')

    # out_report.write('========================================================================================================\n')
    # out_report.write('End of File.')
    # out_report.close()

    return None


def exportMTO1(tmpMTOData):
    #   使用鋼筋搭接續接，採錯層搭接

    # Export MTO
    tmpColumns = [
        'Floor', 'ColSec', 'ModelMember', 'SecInfo(mm)', 'fc', 'ConcreteVol(m3)', 'Form(m2)', 'MainBar', 'MainBarNumbers', 'MainBarWeight(ton)',
        'StirBar', 'StirBarNumbers', 'StirBarWeight(ton)' , 'TieBar', 'TieBarXNumbers', 'TieBarYNumbers', 'TieBarWeight(ton)', 'OverLapNumbers', 'OverLapWeight(ton)'
    ]

    df_MTO = pd.DataFrame(tmpMTOData, columns=tmpColumns)
    
    exportstring = ''

    # for concrete
    list_conc = ['210', '245', '280', '350', '420']

    for tmp in list_conc:
        try:
            tmpqurryTEXT = f'fc ==  \'{tmp}\''
            tmpdf = df_MTO.query(tmpqurryTEXT).copy()
            tmpConVol = tmpdf['ConcreteVol(m3)'].sum()
            if tmpConVol > 0.0:
                exportstring += f'Concrete Volumn for fc\' {tmp} = {tmpConVol:.3f} m3\n'
        except:
            pass
        

    # for Form
    exportstring += f'\n\n'
    tmpFormArea = df_MTO['Form(m2)'].sum()
    exportstring += f'Total Form Area = {tmpFormArea:>10.3f} m2\n'



    # for rebars
    exportstring += f'\n\n'

    factor_for_OverLapNo = 0.5  #   採錯層搭接

    tmpRebarWeight = df_MTO['MainBarWeight(ton)'].sum() + df_MTO['StirBarWeight(ton)'].sum() + df_MTO['TieBarWeight(ton)'].sum() + df_MTO['OverLapWeight(ton)'].sum() * factor_for_OverLapNo
    exportstring += f'Total Rebar Weight = {tmpRebarWeight:>10.3f} ton\n'

    exportstring += f'    (A)Summary by Application:\n'

    tmpRebarWeight = df_MTO['MainBarWeight(ton)'].sum()
    exportstring += f'        Total MainBarWeight = {tmpRebarWeight:>10.3f} ton\n'
    
    tmpRebarWeight = df_MTO['StirBarWeight(ton)'].sum()
    exportstring += f'        Total StriBarWeight = {tmpRebarWeight:>10.3f} ton\n'
    
    tmpRebarWeight = df_MTO['TieBarWeight(ton)'].sum()
    exportstring += f'        Total TieBarWeight  = {tmpRebarWeight:>10.3f} ton\n'
    
    tmpRebarWeight = df_MTO['OverLapWeight(ton)'].sum() * factor_for_OverLapNo
    exportstring += f'        Total OverLapWeight = {tmpRebarWeight:>10.3f} ton\n'
    exportstring += f'        (HALF OVERLAP FOR EACH FLOOR)\n'


    exportstring += f'\n'
    exportstring += f'    (B)Summary by Size:\n'
    # ===============================================================================
    list_RebarName = ['#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11', '#12', '#14', '#18', 'D10', 'D13', 'D16', 'D19', 'D22', 'D25', 'D29', 'D32', 'D36', 'D39', 'D43', 'D57']

    for tmp in list_RebarName:            

        tmpRebarName = tmp
        tmpRebarWeight = 0
        for index, element in enumerate(tmpMTOData):
            if tmpRebarName in element[7]:
                tmpRebarWeight += element[9]
            if tmpRebarName in element[10]:
                tmpRebarWeight += element[12]
            if tmpRebarName in element[13]:
                tmpRebarWeight += element[16]
            if tmpRebarName in element[7]:
                tmpRebarWeight += element[18] * factor_for_OverLapNo
        if tmpRebarWeight > 0.001:
            exportstring += f'        Total {tmpRebarName}   = {tmpRebarWeight:>10.3f} ton\n'


    return exportstring


def exportMTO2(tmpMTOData):
    #   使用續接器續接

    # Export MTO
    tmpColumns = [
        'Floor', 'ColSec', 'ModelMember', 'SecInfo(mm)', 'fc', 'ConcreteVol(m3)', 'Form(m2)', 'MainBar', 'MainBarNumbers', 'MainBarWeight(ton)',
        'StirBar', 'StirBarNumbers', 'StirBarWeight(ton)' , 'TieBar', 'TieBarXNumbers', 'TieBarYNumbers', 'TieBarWeight(ton)', 'Couplers'
    ]

    df_MTO = pd.DataFrame(tmpMTOData, columns=tmpColumns)

    exportstring = ''
    

    # for concrete
    list_conc = ['210', '245', '280', '350', '420']

    for tmp in list_conc:
        try:
            tmpqurryTEXT = f'fc ==  \'{tmp}\''
            tmpdf = df_MTO.query(tmpqurryTEXT).copy()
            tmpConVol = tmpdf['ConcreteVol(m3)'].sum()
            if tmpConVol > 0.0:
                exportstring += f'Concrete Volumn for fc\' {tmp} = {tmpConVol:.3f} m3\n'
        except:
            pass


    # for Form
    exportstring += f'\n\n'
    tmpFormArea = df_MTO['Form(m2)'].sum()
    exportstring += f'Total Form Area = {tmpFormArea:>10.3f} m2\n'



    # for rebars
    exportstring += f'\n\n'

    tmpRebarWeight = df_MTO['MainBarWeight(ton)'].sum() + df_MTO['StirBarWeight(ton)'].sum() + df_MTO['TieBarWeight(ton)'].sum()
    exportstring += f'Total Rebar Weight = {tmpRebarWeight:>10.3f} ton\n'

    exportstring += f'    (A)Summary by Application:\n'

    tmpRebarWeight = df_MTO['MainBarWeight(ton)'].sum()
    exportstring += f'        Total MainBarWeight = {tmpRebarWeight:>10.3f} ton\n'
    
    tmpRebarWeight = df_MTO['StirBarWeight(ton)'].sum()
    exportstring += f'        Total StriBarWeight = {tmpRebarWeight:>10.3f} ton\n'
    
    tmpRebarWeight = df_MTO['TieBarWeight(ton)'].sum()
    exportstring += f'        Total TieBarWeight  = {tmpRebarWeight:>10.3f} ton\n'
    

    exportstring += f'\n'
    exportstring += f'    (B)Summary by Size:\n'
    # ===============================================================================
    list_RebarName = ['#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11', '#12', '#14', '#18', 'D10', 'D13', 'D16', 'D19', 'D22', 'D25', 'D29', 'D32', 'D36', 'D39', 'D43', 'D57']

    for tmp in list_RebarName:            

        tmpRebarName = tmp
        tmpRebarWeight = 0
        for index, element in enumerate(tmpMTOData):
            if tmpRebarName in element[7]:
                tmpRebarWeight += element[9]
            if tmpRebarName in element[10]:
                tmpRebarWeight += element[12]
            if tmpRebarName in element[13]:
                tmpRebarWeight += element[16]
            # if tmpRebarName in element[7]:
            #     tmpRebarWeight += element[18]
        if tmpRebarWeight > 0.001:
            exportstring += f'        Total {tmpRebarName}   = {tmpRebarWeight:>10.3f} ton\n'


    # for couplers
    exportstring += f'\n\n'

    for tmp in list_RebarName:            

        tmpRebarName = tmp
        tmpRebarNos = 0
        for index, element in enumerate(tmpMTOData):
            if tmpRebarName in element[7]:
                tmpRebarNos += int(element[17])
        if tmpRebarNos > 0.001:
            exportstring += f'Couplers for {tmpRebarName:<3}   = {tmpRebarNos:>6.0f} SETs\n'
            

    return exportstring


def main(dict_column_rebar_design, reqExportRectangularSectionData, reqExportCircleSectionData, model_data_all, proj_arguments):

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




#================================================================================================================================================ REPORT
    if isinstance(reqExportRectangularSectionData, pd.DataFrame):
        report_rectangular_to_string = exportREPORT_Rectangular(dict_column_rebar_design, reqExportRectangularSectionData, dictBarArea)
        
    # 圓型的檢核尚未完成!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # if isinstance(reqExportCircleSectionData, pd.DataFrame):
    #     exportREPORT_Circle(file_folder, chexk_report_Data_Circle, dictBarDia, dictBarArea, dxfI)
        



    
#================================================================================================================================================ MTO
    tmpMTOData1 = []
    tmpMTOData2 = []

    for index, row in dict_column_rebar_design.iterrows():
        argShape = row[11]

        if argShape == 'Circle':
            # 圓形斷面
            argFloor        = str(row[0])
            argColumn       = str(row[1])

            # argX0           = float(row[2]) * argBoxWid * 1
            # argY0           = float(row[3]) * (argBoxDep + 750/dwg_scale) * -1

            argRebarType    = int(row[4])
            argCover        = float(row[5])

            argMBName       = str(row[6])
            argSBName       = str(row[7])
            argTBName       = str(row[8])

            argMBDia        = float(dictBarDia[argMBName])
            argSBDia        = float(dictBarDia[argSBName])
            argTBDia        = float(dictBarDia[argTBName])

            argSS_CR        = float(row[9])
            argSS_nCR       = float(row[10])

            argDia          = float(row[12])

            argfc           = float(row[13])
            argfy           = float(row[14])

            argNa           = get_Total_ReBar(row[15])
            
            argSN_CR        = float(row[17])
            argSN_nCR       = float(row[18])

            argModelColumnList  = str(row[20]).split()

            argTotalMainBar = argNa

            for tmp3 in argModelColumnList:
                modelFloor = tmp3.split('_')[0]
                modelColumn = tmp3.split('_')[1]
                modelColH = float(dictStoryHeight[modelFloor])

                arg_hook_90 = math.pi * (4 * argSBDia) / 4 + 6 * argSBDia
                arg_hook_135 = math.pi * (4 * argSBDia) / 2 + max(75, 6 * argSBDia)

                arg_len_tie_x = (argDia - 2*argCover) + arg_hook_90 + arg_hook_135
                arg_len_tie_y = (argDia - 2*argCover) + arg_hook_90 + arg_hook_135
                arg_len_stirr = math.pi*(argDia - 2*argCover) + 2*arg_hook_135

                tmpSecInfo =  f'{argDia:.0f}Diameter*{modelColH:.0f}H'
                
                tmpVOL = (0.25*math.pi*argDia*argDia*modelColH)/1000/1000/1000
                tmpFOR = (math.pi*argDia*modelColH)/1000/1000

                if modelFloor == listStoryLayer[-1]:
                    #   最底部的柱考慮1500mm的伸展長度
                    modelColH = modelColH + 1500

                tmpNumber1  = math.ceil(modelColH/2/argSS_CR)
                tmpNumber2  = math.ceil(modelColH/2/argSS_nCR)
                tmpNumber   = tmpNumber1 + tmpNumber2

                tmpMBW = dictBarWei[argMBName]/1000*argTotalMainBar*modelColH/1000
                tmpStW = dictBarWei[argSBName]/1000*(tmpNumber1*argSN_CR+tmpNumber2*argSN_nCR)*arg_len_stirr/1000
                tmpTxW = dictBarWei[argTBName]/1000*tmpNumber*1*arg_len_tie_x/1000
                tmpTyW = dictBarWei[argTBName]/1000*tmpNumber*1*arg_len_tie_y/1000

                tmpOverLapNumber = argTotalMainBar

                # tmpOLW = dictBarWei[argMBName]/1000 * dictOverLapLen[f'{argfy:.0f}-{argfc:.0f}-{argMBName}']/1000 * tmpOverLapNumber
                tmpOLW = dictBarWei[argMBName]/1000 * 1.5 * tmpOverLapNumber

                tmpMTOData1.append([argFloor, argColumn, tmp3, tmpSecInfo, f'{argfc:.0f}', tmpVOL, tmpFOR, argMBName, argTotalMainBar, tmpMBW, argSBName, (tmpNumber1*argSN_CR+tmpNumber2*argSN_nCR), tmpStW, argTBName, (tmpNumber*1), (tmpNumber*1), (tmpTxW+tmpTyW), tmpOverLapNumber, tmpOLW])
                tmpMTOData2.append([argFloor, argColumn, tmp3, tmpSecInfo, f'{argfc:.0f}', tmpVOL, tmpFOR, argMBName, argTotalMainBar, tmpMBW, argSBName, (tmpNumber1*argSN_CR+tmpNumber2*argSN_nCR), tmpStW, argTBName, (tmpNumber*1), (tmpNumber*1), (tmpTxW+tmpTyW), tmpOverLapNumber])

        else:
            # 矩形斷面
            argFloor = str(row[0])
            argColumn = str(row[1])

            # argX0 = float(row[2]) * argBoxWid * 1
            # argY0 = float(row[3]) * (argBoxDep + 750/dwg_scale) * -1

            argRebarType = int(row[4])
            argCover = float(row[5])

            argMBName = str(row[6])
            argSBName = str(row[7])
            argTBName = str(row[8])

            argMBDia = float(dictBarDia[argMBName])
            argSBDia = float(dictBarDia[argSBName])
            argTBDia = float(dictBarDia[argTBName])

            argSBSpace1 = float(row[9])
            argSBSpace2 = float(row[10])
            argDx = float(row[11])
            argDy = float(row[12])

            argfc = float(row[13])
            argfy = float(row[14])
            
            argNx = get_Total_ReBar(row[15])
            argNy = get_Total_ReBar(row[16])

            argTNx = int(row[17])
            argTNy = int(row[18])

            argTotalMainBar = int(2 * (argNx + argNy) - 4)

            argModelColumnList = str(row[20]).split()
            

            for tmp3 in argModelColumnList:
                modelFloor = tmp3.split('_')[0]
                modelColumn = tmp3.split('_')[1]
                modelColH = float(dictStoryHeight[modelFloor])

                arg_hook_90 = math.pi * (4 * argTBDia) / 4 + 6 * argTBDia
                arg_hook_135 = math.pi * (4 * argTBDia) / 2 + max(75, 6 * argTBDia)
                arg_E2C = argCover+argSBDia+0.5*argMBDia

                arg_len_tie_x = argDx - 2*arg_E2C + arg_hook_90 + arg_hook_135
                arg_len_tie_y = argDy - 2*arg_E2C + arg_hook_90 + arg_hook_135
                arg_len_stirr = (argDx - 2*arg_E2C + argMBDia)*2 + (argDy - 2*arg_E2C + argMBDia)*2 + 2*arg_hook_135

                tmpSecInfo =  f'{argDx:.0f}B*{argDy:.0f}D*{modelColH:.0f}H'
                
                tmpVOL = (argDx*argDy*modelColH)/1000/1000/1000
                tmpFOR = (argDx*modelColH + argDy*modelColH)*2/1000/1000

                if modelFloor == listStoryLayer[-1]:
                    #   最底部的柱考慮1500mm的伸展長度
                    modelColH = modelColH + 1500

                tmpNumber=math.ceil(modelColH/argSBSpace1/2+modelColH/argSBSpace2/2)

                tmpMBW = dictBarWei[argMBName]/1000*argTotalMainBar*modelColH/1000
                tmpStW = dictBarWei[argSBName]/1000*tmpNumber*arg_len_stirr/1000
                tmpTxW = dictBarWei[argTBName]/1000*tmpNumber*argTNx*arg_len_tie_x/1000
                tmpTyW = dictBarWei[argTBName]/1000*tmpNumber*argTNy*arg_len_tie_y/1000

                tmpOverLapNumber = argTotalMainBar

                # tmpOLW = dictBarWei[argMBName]/1000 * dictOverLapLen[f'{argfy:.0f}-{argfc:.0f}-{argMBName}']/1000 * tmpOverLapNumber
                tmpOLW = dictBarWei[argMBName]/1000 * 1.5 * tmpOverLapNumber

                tmpMTOData1.append([argFloor, argColumn, tmp3, tmpSecInfo, f'{argfc:.0f}', tmpVOL, tmpFOR, argMBName, argTotalMainBar, tmpMBW, argSBName, tmpNumber, tmpStW, argTBName, (tmpNumber*argTNx), (tmpNumber*argTNy), (tmpTxW+tmpTyW), tmpOverLapNumber, tmpOLW])
                tmpMTOData2.append([argFloor, argColumn, tmp3, tmpSecInfo, f'{argfc:.0f}', tmpVOL, tmpFOR, argMBName, argTotalMainBar, tmpMBW, argSBName, tmpNumber, tmpStW, argTBName, (tmpNumber*argTNx), (tmpNumber*argTNy), (tmpTxW+tmpTyW), tmpOverLapNumber])


    return report_rectangular_to_string, exportMTO1(tmpMTOData1), exportMTO2(tmpMTOData2)


if __name__ == '__main__':
        main(r'D:\@Programing\Python\EtabsOutputToAutoCad\@202404_ToEXE\Sample\ModelData\ModelData', r'D:\@Programing\Python\EtabsOutputToAutoCad\@202404_ToEXE\Sample')