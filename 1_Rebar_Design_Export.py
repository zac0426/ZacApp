import streamlit as st

import io

import math

import shelve
import pyodbc
import os
import pandas as pd

import ezdxf

import fun_column_section_rebar_design
import fun_column_exportDXF
import fun_column_exportMTOandREPORT

import fun_gogogo



def dictionary_remove_nan_values(dictionary):
    new_dictionary = {}

    for key, values in dictionary.items():
        if len(values) == 1:
            new_value = values[0]
            new_dictionary[key] = new_value
        
        else:
            new_valueList = []
            for value in values:
                if isinstance(value, str):
                    new_valueList.append(value)
                else:
                    if not math.isnan(value):
                        new_valueList.append(value)
            new_dictionary[key] = new_valueList
    
    return new_dictionary



@st.cache_data
def read_external_excel_sheet(gh_id):

    excel_sheets = pd.read_excel(f"https://docs.google.com/spreadsheets/export?id={gh_id}&format=xlsx", sheet_name=None)


    modelUnits_For      = ''
    modelUnits_Len      = ''

    dictGridLines       = ''
    dictStoryHeight     = ''
    dictStoryJoint      = ''
    dictPointXY         = ''
    dictLineCon_B       = ''
    dictLineCon_C       = ''
    dictLineAssign      = ''
    dictFrameSec        = ''
    dictBarArea         = ''
    dictBarDia          = ''
    dictBarWei          = ''
    listSpacing         = ''
    dictOverLapLen      = ''
    dictColCheckMode    = ''
    dictLineAssign2     = ''

    listColumnForce     = ''
    listBeamForce       = ''
    listStoryShear      = ''
    listStoryLayer      = ''
    tableColumDesign    = ''
    tableBeamsDesign    = ''


    for sheet_name, values in excel_sheets.items():
        if sheet_name == 'modelUnits_For':
            modelUnits_For = values.iat[0, 1]
            st.write(f"Get modelUnits_For")
            # st.write(f"{modelUnits_For}")

        elif sheet_name == 'modelUnits_Len':
            modelUnits_Len = values.iat[0, 1]
            st.write(f"Get modelUnits_Len")
            # st.write(f"{modelUnits_Len}")



        elif sheet_name == 'dictGridLines':
            dictGridLines = values.to_dict(orient='list')
            dictGridLines = dictionary_remove_nan_values(dictGridLines)
            st.write(f"Get dictGridLines")
            # st.write(f"{dictGridLines}")

        elif sheet_name == 'dictStoryHeight':
            dictStoryHeight = values.to_dict(orient='list')
            dictStoryHeight = dictionary_remove_nan_values(dictStoryHeight)
            st.write(f"Get dictStoryHeight")
            # st.write(f"{dictStoryHeight}")

        elif sheet_name == 'dictStoryJoint':
            dictStoryJoint = values.to_dict(orient='list')
            dictStoryJoint = dictionary_remove_nan_values(dictStoryJoint)
            st.write(f"Get dictStoryJoint")
            # st.write(f"{dictStoryJoint}")

        elif sheet_name == 'dictPointXY':
            dictPointXY = values.to_dict(orient='list')
            dictPointXY = dictionary_remove_nan_values(dictPointXY)
            st.write(f"Get dictPointXY")
            # st.write(f"{dictPointXY}")

        elif sheet_name == 'dictLineCon_B':
            dictLineCon_B = values.to_dict(orient='list')
            dictLineCon_B = dictionary_remove_nan_values(dictLineCon_B)
            st.write(f"Get dictLineCon_B")
            # st.write(f"{dictLineCon_B}")

        elif sheet_name == 'dictLineCon_C':
            dictLineCon_C = values.to_dict(orient='list')
            dictLineCon_C = dictionary_remove_nan_values(dictLineCon_C)
            st.write(f"Get dictLineCon_C")
            # st.write(f"{dictLineCon_C}")

        elif sheet_name == 'dictLineAssign':
            dictLineAssign = values.to_dict(orient='list')
            dictLineAssign = dictionary_remove_nan_values(dictLineAssign)
            st.write(f"Get dictLineAssign")
            # st.write(f"{dictLineAssign}")
            # print(dictLineAssign)

        elif sheet_name == 'dictFrameSec':
            dictFrameSec = values.to_dict(orient='list')
            dictFrameSec = dictionary_remove_nan_values(dictFrameSec)
            st.write(f"Get dictFrameSec")
            # st.write(f"{dictFrameSec}")

        elif sheet_name == 'dictBarArea':
            dictBarArea = values.to_dict(orient='list')
            dictBarArea = dictionary_remove_nan_values(dictBarArea)
            st.write(f"Get dictBarArea")
            # st.write(f"{dictBarArea}")

        elif sheet_name == 'dictBarDia':
            dictBarDia = values.to_dict(orient='list')
            dictBarDia = dictionary_remove_nan_values(dictBarDia)
            st.write(f"Get dictBarDia")
            # st.write(f"{dictBarDia}")

        elif sheet_name == 'dictBarWei':
            dictBarWei = values.to_dict(orient='list')
            dictBarWei = dictionary_remove_nan_values(dictBarWei)
            st.write(f"Get dictBarWei")
            # st.write(f"{dictBarWei}")

        elif sheet_name == 'listSpacing':
            listSpacing = values.to_dict(orient='list')
            listSpacing = dictionary_remove_nan_values(listSpacing)
            st.write(f"Get listSpacing")
            # st.write(f"{listSpacing}")

        elif sheet_name == 'dictOverLapLen':
            dictOverLapLen = values.to_dict(orient='list')
            dictOverLapLen = dictionary_remove_nan_values(dictOverLapLen)
            st.write(f"Get dictOverLapLen")
            # st.write(f"{dictOverLapLen}")

        elif sheet_name == 'dictColCheckMode':
            dictColCheckMode = values.to_dict(orient='list')
            dictColCheckMode = dictionary_remove_nan_values(dictColCheckMode)
            st.write(f"Get dictColCheckMode")
            # st.write(f"{dictColCheckMode}")

        elif sheet_name == 'dictLineAssign2':
            dictLineAssign2 = values.to_dict(orient='list')
            dictLineAssign2 = dictionary_remove_nan_values(dictLineAssign2)
            st.write(f"Get dictLineAssign2")
            # st.write(f"{dictLineAssign2}")
            # print(dictLineAssign2)



        elif sheet_name == 'listColumnForce':
            listColumnForce = values.values.tolist()
            st.write(f"Get listColumnForce")
            # st.write(f"{listColumnForce}")

        elif sheet_name == 'listBeamForce':
            listBeamForce = values.values.tolist()
            st.write(f"Get listBeamForce")
            # st.write(f"{listBeamForce}")

        elif sheet_name == 'listStoryShear':
            listStoryShear = values.values.tolist()
            listStoryShear = [data[0] for data in listStoryShear]
            st.write(f"Get listStoryShear")
            # st.write(f"{listStoryShear}")

        elif sheet_name == 'listStoryLayer':
            listStoryLayer = values.values.tolist()
            listStoryLayer = [data[0] for data in listStoryLayer]
            st.write(f"Get listStoryLayer")
            # st.write(f"{listStoryLayer}")

        elif sheet_name == 'tableColumDesign':
            tableColumDesign = values.values.tolist()
            st.write(f"Get tableColumDesign")
            # st.write(f"{tableColumDesign}")

        elif sheet_name == 'tableBeamsDesign':
            tableBeamsDesign = values.values.tolist()
            st.write(f"Get tableBeamsDesign")
            # st.write(f"{tableBeamsDesign}")


    export_data = [
        modelUnits_For, 
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
        ]

    # Fetch data from URL here, and then clean it up.
    return export_data



def get_etabs_col_axial_maxload(LoadData, Story, ColName, LoadCase):
    if ColName:
        AxialLoadList = []
        for index, element in enumerate(LoadData):            
            tmpCondition1 = (Story == element[0])
            tmpCondition2 = (ColName == element[1])
            tmpCondition3 = (LoadCase in element[2])
            if tmpCondition1 and tmpCondition2 and tmpCondition3:
                AxialLoadList.append(element[4])

        maxAxialLoad = max(AxialLoadList)
        minAxialLoad = min(AxialLoadList)

    if minAxialLoad < 0.0:
        return abs(minAxialLoad)
    else:
        return 0.0















st.set_page_config(page_title='Zac\'s Blog', page_icon=":+1:", layout="wide",)
st.title(':green[Rebar Design Export App]')

if not st.session_state.user_state['logged_in']:
    # Create login form
    st.sidebar.write('Please login')
    
elif st.session_state.user_state['logged_in']:
    st.sidebar.write('Welcome to the app')
    st.sidebar.write('You are logged in as:', st.session_state.user_state['mail_adress'])
    st.sidebar.write('You are a:', st.session_state.user_state['user_type'])
    st.sidebar.write('Your fixed user message:', st.session_state.user_state['fixed_user_message'])
    
    # start function
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['資料讀取', 'RC柱鋼筋設計', 'RC梁鋼筋設計', '極限層剪力設計', '平面圖輸出'])
    
    with tab1:
        st.header('設計參數')
        # url = st.secrets["project_data_url"]
        # st.write(f'Download and update project data [link]({url}).')


        # argProInfo           
        # argGirderBarMinus    
        # argBeamBarMinus      
        # argTieGirderBarMinus 
        # argTieBeamBarMinus   
        # argColumnBarMinus    
        # argGBRebarDWGScale

        argProInfo = st.radio("專案顯示選擇", ("Code112_mm_ShowCrossSection", "Code112_cm_ShowCrossSection", "Code112_mm_DontShowCrossSection", "Code112_cm_DontShowCrossSection"))
        st.write("您選擇了：", argProInfo)
        st.markdown('\n')

        argGirderBarMinus = st.number_input("大梁主筋根數需減少幾根", min_value=0, max_value=10, value=0)
        st.write(f"大梁主筋根數減少：{argGirderBarMinus} 根")
        st.markdown('\n')

        argBeamBarMinus = st.number_input("小梁主筋根數需減少幾根", min_value=0, max_value=10, value=0)
        st.write(f"小梁主筋根數減少：{argBeamBarMinus} 根")
        st.markdown('\n')

        argColumnBarMinus = st.number_input("柱主筋根數需減少幾根", min_value=0, max_value=10, value=0)
        st.write(f"柱主筋根數減少：{argColumnBarMinus} 根")
        st.markdown('\n')

        argGBRebarDWGScale = st.number_input("梁鋼筋詳圖輸出比例(30 or 50)", min_value=30, max_value=50, value=30)
        st.write(f"梁鋼筋詳圖輸出比例：{argGBRebarDWGScale}")
        st.markdown('\n'*3)

        proj_arguments = [argProInfo, argGirderBarMinus, argBeamBarMinus, argColumnBarMinus, argGBRebarDWGScale]

        
        gh_link = st.text_input("貼上google-docs模型資料分享連結:", value="https://docs.google.com/spreadsheets/d/1KqAmkQZTkYmeyrPQyvp11f-A-blqHLJS/edit?us")

        if gh_link:

            bool_read_model_data = False

            # 在d/與/edit之間為文件ID
            # tmpS = gh_link.find('d/')
            # tmpE = gh_link.find('/edit')
            #  gh_id = gh_link[tmpS+2:tmpE]
            gh_id = gh_link[(gh_link.find('d/') + 2):(gh_link.find('/edit'))]

            st.write("模型資料google-docs連結ID為:   ", gh_id)
            st.markdown('***')

            st.write(f"<<<模型資料讀取中，請等待>>>")

            model_data_all = read_external_excel_sheet(gh_id)

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

            st.write(f"<<<模型資料讀取完畢, 可進行設計>>>")

            bool_read_model_data = True
            
    with tab2:
        if bool_read_model_data:
            
# ==========================================================================================================================================================
            checkbox_step01 = st.checkbox(':blue[1. 設定RC柱群組: Col_Out01_ColList]')
            
            if checkbox_step01:

                for floor in listStoryLayer:
                    column = []
                    for tmp in dictLineAssign[floor]:
                        # print(tmp)
                        tmpLabel = tmp.split(':')[0]
                        if floor + '-' + tmpLabel in dictLineCon_C:
                            column.append(tmpLabel)
                    
                    # tmpStr = f'樓層{floor}柱桿件編號:'
                    # st.write(f"{tmpStr}")

                    tmpStr = ''
                    for tmp in column:
                        tmpStr = tmpStr + f'{tmp}/'
                    
                    st.write(f"樓層{floor}柱桿件編號:{tmpStr}")

                with st.form(key="form_story_group"):
                    # st.write("Inside the form")
                    st.write(f"[Story Group]")

                    tmpdict = {'story_group_name':["MyFloor1", "MyFloor2", "MyFloor3"], 'story_group_list':['1F/2F/3F', '4F/5F/6F', '7F/8F/9F']}
                    dict_story_group = pd.DataFrame(st.data_editor(data=tmpdict, num_rows="dynamic"))

                    # Every form must have a submit button.
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        st.write("Updated!")
                # st.write(dict_story_group)


                with st.form(key="form_column_group"):
                    # st.write("Inside the form")
                    st.write(f"[Column Group]")

                    tmpdict = {'column_group_name':["MyColumn1", "MyColumn2", "MyColumn3"], 'column_group_list':['C1/C2/C3', 'C4/C5/C6', 'C7/C8/C9']}
                    dict_column_group = pd.DataFrame(st.data_editor(data=tmpdict, num_rows="dynamic"))

                    # Every form must have a submit button.
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        st.write("Updated!")
                # st.write(dict_column_group)

            
            

# ==========================================================================================================================================================
            st.markdown('***')
            checkbox_step02 = st.checkbox(':blue[2. 設定(樓層-柱)群組設計參數: CF02_GetGroup]')
            if checkbox_step02:

                with st.form(key="form_storycolumngroup_designparameter"):
                    st.write(f"[Story & Column Group Design Parameter]")

                    tmpDictColumn = ['story_group','column_group','xlocation','ylocation','rebar_type','cover_mm','mainbar_mark','Dx_mm','Dy_mm','fc\'_kg/cm2','fys_kg/cm2','column_List_model']
                    
                    tmpDictList = []
                    for index1, row1 in dict_story_group.iterrows():
                        sgn, sgl = row1
                        sgl = sgl.split('/')

                        for index2, row2 in dict_column_group.iterrows():
                            cgn, cgl = row2
                            cgl = cgl.split('/')

                        # # for index2, (cgn, cgl) in enumerate(zip(dict_column_group['column_group_name'], dict_column_group['column_group_list'])):
                        #     cgl = cgl.split('/')

                            argStoryGroupName   = sgn
                            argColumnGroupName  = cgn                        
                            
                            argLocationX = index2
                            argLocationY = index1
                            argColumnSizeDx = 0.0
                            argColumnSizeDy = 0.0

                            argColumnListModel = ''

                            for storyname in sgl:
                                for columnname in cgl:
                                    for linedata in dictLineAssign[storyname]:
                                        tmpLabel, tmpSection = linedata.split(':')
                                        if tmpLabel == columnname:
                                            argColumnSizeDx, argColumnSizeDy, argColumnShape = dictFrameSec[tmpSection]

                                            # '''得到GROUP裡每根柱的(樓層_編號_最大軸壓力),其中軸壓力須配合ETABS裡USDENVE的包絡載重組合'''
                                            tmpMaxAxialLoad = get_etabs_col_axial_maxload(listColumnForce, storyname, columnname, 'USDENVE')
                                            argColumnListModel += f'{storyname}_{columnname}_{tmpMaxAxialLoad:.2f}  '
                            
                            if argColumnListModel:
                                tmpDictList.append([argStoryGroupName, argColumnGroupName, argLocationX, argLocationY, '1', '40', '#8', argColumnSizeDx, argColumnSizeDy, '280', '4200', argColumnListModel])
                            
                    # 須轉置
                    tmpdict = dict(zip(tmpDictColumn, list(zip(*tmpDictList))))
                    
                    dict_column_design_parameter = pd.DataFrame(st.data_editor(data=tmpdict, num_rows="dynamic"))

                    # Every form must have a submit button.
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        st.write("Updated!")
                # st.write(dict_column_design_parameter)



# ==========================================================================================================================================================
            st.markdown('***')
            checkbox_step03 = st.checkbox(':blue[3. 柱斷面鋼筋配置結果: CF03_GetColRebar]')
            if checkbox_step03:

                with st.form(key="form_storycolumngroup_rebardesign"):
                    st.write(f"[Story & Column Group Section Rebar Design]")

                    reqSecBarDesign, reqExportRectangularSectionData, reqExportCircleSectionData = fun_column_section_rebar_design.main(dict_column_design_parameter, model_data_all, proj_arguments)
                    
                    dict_column_rebar_design = st.data_editor(data=reqSecBarDesign, num_rows="dynamic")

                    # Every form must have a submit button.
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        st.write("Updated!")
                # st.write(dict_column_rebar_design)


                if isinstance(reqExportRectangularSectionData, pd.DataFrame):
                    st.download_button("[REF] download column check data for rectangular section", reqExportRectangularSectionData.to_csv(index=False).encode('utf-8'), "ColumnCheckData_Rectangular.csv", "text/csv", key='download-csv')

                if isinstance(reqExportCircleSectionData, pd.DataFrame):
                    st.download_button("[REF] download column check data for circle section", reqExportCircleSectionData.to_csv(index=False).encode('utf-8'), "ColumnCheckData_Circle.csv", "text/csv", key='download-csv')





# ==========================================================================================================================================================
            st.markdown('***')
            checkbox_step04 = st.checkbox(':blue[4. 柱斷面DXF/MTO/REPORT輸出: CF04_ColSecMtoReport]')
            if checkbox_step04:

                # DXF & USS
                dxf_to_string, df_ColData2USS = fun_column_exportDXF.main(dict_column_rebar_design, dict_story_group['story_group_name'], dict_column_group['column_group_name'], model_data_all, proj_arguments)
                st.download_button('Download ColumnRebarSection.dxf', dxf_to_string, file_name='ColumnRebarSection.dxf')

                if isinstance(df_ColData2USS, pd.DataFrame):
                    st.download_button("[REF] download column data to USS check", df_ColData2USS.to_csv(index=False).encode('utf-8'), "ColData2USS.csv", "text/csv")



                # MTO & REPORT
                report_string, mto1_string, mto2_string = fun_column_exportMTOandREPORT.main(dict_column_rebar_design, reqExportRectangularSectionData, reqExportCircleSectionData, model_data_all, proj_arguments)
                st.download_button('Download ColumnRebarDesignReport.csv', report_string, file_name='ColumnRebarDesignReport.csv')
                st.download_button('Download ColumnMTOsummary1.csv', mto1_string, file_name='ColumnMTOsummary1.csv')
                st.download_button('Download ColumnMTOsummary2.csv', mto2_string, file_name='ColumnMTOsummary2.csv')
                







                # # create a new DXF document
                # doc = ezdxf.new("R2000", setup=True)    # 透過參數setup設為來ezdxf.new()建立一些標準資源，例如線型和文字樣式

                # doc.units = ezdxf.units.MM
                # doc.layers.add(name="Default", color=1, linetype="Continuous")
                # doc.layers.add(name="Concrete", color=13, linetype="Continuous")
                # doc.layers.add(name="Dimension", color=1, linetype="Continuous")

                # tmpDXFdata = to_binary_data(doc)

                # st.download_button('Download Zip', tmpDXFdata, file_name='archive.dxf')








        else:
            st.header('請先讀取資料')

























        
    with tab3:
        pass



    with tab4:
        pass

    with tab5:
        number_a = st.number_input("A", min_value=0, max_value=10, value=0)
        number_b = st.number_input("B", min_value=0, max_value=10, value=0)
        st.write(fun_gogogo.plluus(number_a,number_b))

        


