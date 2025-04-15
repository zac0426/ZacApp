import streamlit as st
import pandas as pd
import requests as rs



def home():

    st.set_page_config(page_title='Zac\'s Blog', page_icon=":+1:", layout="wide",)
    st.title(':rainbow[Zac\'s Blog]')
    st.markdown('***')

    st.header(':blue[:material/Home_App_Logo:] __WELCOME__')

    # st.markdown('''
    #             - python 
    #             - java 
    #             - C
    #             ''')

    # st.markdown("## :material/Download:")

    # st.markdown('***')

    # st.markdown(":material/Download:")

    # st.markdown("*Streamlit* is **really** ***cool***.")
    # st.markdown('''
    #     :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    #     :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
    # st.markdown("Here's a bouquet &mdash;\
    #             :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

    # multi = '''If you end a line with two spaces,
    # a soft return is used for the next line.

    # Two (or more) newline characters in a row will result in a hard return.
    # '''
    # st.markdown(multi)


    # read user data
    sheet_csv = "https://docs.google.com/spreadsheets/d/1lEaiW6AZxlx0DV1-pG7cDOqMl6n0FCI-qoe5f0tszkI/export?format=csv"
    # sheet_csv = st.secrets["user_database_url"]
    res = rs.get(url=sheet_csv)
    open('user_database.csv', 'wb').write(res.content)
    user_database = pd.read_csv('user_database.csv', header=0)


    # Create user_state
    if 'user_state' not in st.session_state:
        st.session_state.user_state = {
            'name_surname': '',
            'password': '',
            'logged_in': False,
            'user_type': '',
            'mail_adress': '',
            'fixed_user_message': ''
        }

    if not st.session_state.user_state['logged_in']:
        # Create login form
        st.write('Please login')
        mail_adress = st.text_input('E-Mail',value='zac0426@gmail.com')
        password = st.text_input('Password', type='password',value='a6185a6185')
        login_button = st.button('Login')

        # Check if user is logged in
        if login_button:
            user_ = user_database[user_database['mail_adress'] == mail_adress].copy()
            if len(user_) == 0:
                st.error('User not found')
            else:
                if user_['mail_adress'].values[0] == mail_adress and user_['password'].values[0] == password:
                    st.session_state.user_state['mail_adress'] = mail_adress
                    st.session_state.user_state['password'] = password
                    st.session_state.user_state['logged_in'] = True
                    st.session_state.user_state['user_type'] = user_['user_type'].values[0]
                    st.session_state.user_state['mail_adress'] = user_['mail_adress'].values[0]
                    st.session_state.user_state['fixed_user_message'] = user_['fixed_user_message'].values[0]
                    st.write('You are logged in')

                    # application should run again according to the new user state. 
                    # the information about the user is not lost because it is stored in session_state.
                    st.rerun()
                else:
                    st.write('Invalid username or password')
    elif st.session_state.user_state['logged_in']:
        st.write('Welcome to the app')
        st.write('You are logged in as:', st.session_state.user_state['mail_adress'])
        st.write('You are a:', st.session_state.user_state['user_type'])
        st.write('Your fixed user message:', st.session_state.user_state['fixed_user_message'])
        if st.session_state.user_state['user_type'] == 'admin':
            st.write('You have admin rights. Here is the database')
            st.table(user_database)

        # logout function
        logout_button = st.button('logout')
        if logout_button:
            st.session_state.user_state['logged_in'] = False
            st.rerun()
            # st.stop()

if __name__ == "__main__":
    home()



# if not st.session_state.user_state['logged_in']:
#     # Create login form
#     st.sidebar.write('Please login')
#     mail_adress = st.sidebar.text_input('E-Mail')
#     password = st.sidebar.text_input('Password', type='password')
#     login_button = st.sidebar.button('Login')

#     # Check if user is logged in
#     if login_button:
#         user_ = database[database['mail_adress'] == mail_adress].copy()
#         if len(user_) == 0:
#             st.error('User not found')
#         else:
#             if user_['mail_adress'].values[0] == mail_adress and user_['password'].values[0] == password:
#                 st.session_state.user_state['mail_adress'] = mail_adress
#                 st.session_state.user_state['password'] = password
#                 st.session_state.user_state['logged_in'] = True
#                 st.session_state.user_state['user_type'] = user_['user_type'].values[0]
#                 st.session_state.user_state['mail_adress'] = user_['mail_adress'].values[0]
#                 st.session_state.user_state['fixed_user_message'] = user_['fixed_user_message'].values[0]
#                 st.write('You are logged in')

#                 # application should run again according to the new user state. 
#                 # the information about the user is not lost because it is stored in session_state.
#                 st.rerun()
#             else:
#                 st.sidebar.write('Invalid username or password')
# elif st.session_state.user_state['logged_in']:
#     st.sidebar.write('Welcome to the app')
#     st.sidebar.write('You are logged in as:', st.session_state.user_state['mail_adress'])
#     st.sidebar.write('You are a:', st.session_state.user_state['user_type'])
#     st.sidebar.write('Your fixed user message:', st.session_state.user_state['fixed_user_message'])
#     if st.session_state.user_state['user_type'] == 'admin':
#         st.sidebar.write('You have admin rights. Here is the database')
#         st.sidebar.table(database)

#     # logout function
#     logout_button = st.sidebar.button('logout')
#     if logout_button:
#         st.session_state.user_state['logged_in'] = False
#         st.rerun()
#         # st.stop()



# if st.session_state.user_state['logged_in'] :
#     # text_contents = '''This is some text'''
#     # st.download_button("Download some text", text_contents)

#     url = "https://drive.google.com/file/d/1vENJ9IEg3oiVunFe51trEKYJ_FGYMOoZ/view?usp=sharing"
#     st.write(f'Download and update project database [link]({url}).')
