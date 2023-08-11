import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psycopg2
import base64
from PIL import Image
import io
import re
import os

conn = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        password = 'Nlgangster@7',
                        port = 4540,
                        database = 'bizcard')
cursor = conn.cursor()


st.set_page_config(page_title= "BizCardX",
                   page_icon= '💼',
                   layout= "wide",)


text = 'BizCardX'   
st.markdown(f"<h2 style='color: white; text-align: center;'>{text} </h2>", unsafe_allow_html=True)



st.markdown(f""" <style>.stApp {{
                    background: url('https://mcdn.wallpapersafari.com/medium/51/43/YZuGTL.jpg');   
                    background-size: cover}}
                 </style>""",unsafe_allow_html=True)


def image_to_text(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    details =[]
    for i in range(len(result)):
        details.append(result[i][1])
    name = []
    designation = []
    contact =[]
    email =[]
    website = []
    street =[]
    city =[]
    state =[]
    pincode=[]
    company =[]
    
    for i in range(len(details)):
        match1 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+). ([a-zA-Z]+)',details[i])    
        match2 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+)', details[i])
        match3 = re.findall('^[E].+[a-z]',details[i])
        match4 = re.findall('([A-Za-z]+) ([0-9]+)',details[i])
        match5 = re.findall('([0-9]+ [a-zA-z]+)',details[i])    
        match6 = re.findall('.com$' , details[i])
        match7 = re.findall('([0-9]+)',details[i])
        if details[i] == details[0]:
            name.append(details[i])        
        elif details[i] == details[1]:
            designation.append(details[i])
        elif '-' in details[i]:
            contact.append(details[i])
        elif '@' in details[i]:
            email.append(details[i])
        elif "www " in details[i].lower() or "www." in details[i].lower():
            website.append(details[i])
        elif "WWW" in details[i]:
            website.append(details[i] +"." + details[i+1])
        elif match6:
            pass
        elif match1:
            street.append(match1[0][0])
            city.append(match1[0][1])
            state.append(match1[0][2])
        elif match2:
            street.append(match2[0][0])
            city.append(match2[0][1])
        elif match3:
            city.append(match3[0])
        elif match4:
            state.append(match4[0][0])
            pincode.append(match4[0][1])
        elif match5:
            street.append(match5[0]+' St,')
        elif match7:
            pincode.append(match7[0])
        else:
            company.append(details[i])
    if len(company)>1:
        comp = company[0]+' '+company[1]
        print(comp)
    else:
        comp = company[0]
    if len(contact) >1:
        contact_number = contact[0]
        alternative_number = contact[1]
    else:
        contact_number = contact[0]
        alternative_number = None
    
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    # Convert the binary image data to a base64 encoded string
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    
    image_details = {'name':name[0],'designation':designation[0],'company_name':comp,
                     'contact':contact_number,'alternative':alternative_number,'email':email[0],
                     'website':website[0],'street':street[0],'city':city[0],'state':state[0],
                     'pincode':pincode[0], 'image': encoded_image}
        
    return image_details





col1,col2 = st.columns([1,4])
with col1:
    menu = option_menu("Menu", ["Home","Upload","Database"], 
                    icons=["house",'cloud-upload', "list-task"],
                    menu_icon="cast",
                    default_index=0,
                    styles={"icon": {"color": "orange", "font-size": "20px"},
                            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px", "--hover-color": "#FFFFFF"},
                            "nav-link-selected": {"background-color": "#225154"}})
    if menu == 'Upload':
        upload_menu = option_menu("Upload", ['Predefined','Undefined'],                        
                        menu_icon='cloud-upload',
                        default_index=0,
                        styles={"icon": {"color": "orange", "font-size": "20px"},
                                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px", "--hover-color": "#FFFFFF"},
                                "nav-link-selected": {"background-color": "#225154"}})
    
    if menu == 'Database':
        Database_menu = option_menu("Database", ['Modify','Delete'], 
                        
                        menu_icon="list-task",
                        default_index=0,
                        styles={"icon": {"color": "orange", "font-size": "20px"},
                                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#FFFFFF"},
                                "nav-link-selected": {"background-color": "#225154"}})

with col2:
    if menu == 'Home':
        col3,col4 = st.columns([3,2])
        with col3:
            st.header('Welcome to business card application')
            st.subheader(':orange[About the App:]')
            home_text = (f'''In this Streamlit web app, you can upload an image of a business 
                         card and extract relevant information from it using EasyOCR. You can view, 
                         modify, or delete the extracted data in this app. Additionally, the app would 
                         allow users to save the extracted information into a database alongside the 
                         uploaded business card image. The database would be capable of storing multiple 
                         entries, each with its own business card image and the extracted information.''')
                         
            st.markdown(f"<h4 text-align: left;'>{home_text} </h4>", unsafe_allow_html=True)
            st.subheader(":orange[Technologies Used:]")
            tech_text =('  EasyOCR, Python, SQL, Streamlit')
            st.markdown(f"<h4 text-align: left;'>{tech_text} </h4>", unsafe_allow_html=True)
        with col4:
            home_image = Image.open('C:/Users/Gowtham/Datascience/bizcard/dataset/OCR.png')
            st.write('')
            st.write('')
            st.image(home_image)
        
    if menu == 'Upload':
        
        path = False
        if upload_menu == 'Predefined':
            col3,col4 = st.columns([2,2])
            with col3:
                uploaded_file = st.file_uploader("**Choose a file**", type=["jpg", "png", "jpeg"])
                extract = st.button("Extract and Upload")
                if uploaded_file is not None:
                    image_path = os.getcwd()+ "\\"+"dataset"+"\\"+ uploaded_file.name
                    image = Image.open(image_path)
                    col3.image(image)
                    path = True
                
            with col4:
                st.write('')
                st.write('')
                st.info(f'''i) Kindly upload the image in JPG, PNG, or JPEG format.       
                        ii) Click the "**Extract and Upload**" button to extract text from the image and upload the extracted text details to the database.''', icon="ℹ️")
                if path:                
                    image_details = image_to_text(image_path)
                    if extract:
                        img = cv2.imread(image_path)
                        reader = easyocr.Reader(['en'])
                        result = reader.readtext(image_path)
                        for detection in result:    
                            top_left =tuple([int(val) for val in detection[0][0]])
                            bottom_right =tuple([int(val) for val in detection[0][2]])
                            text = detection[1]
                            font =cv2.FONT_HERSHEY_SIMPLEX
                            img = cv2.rectangle(img, top_left, bottom_right, (0,255,0), 2)
                            img = cv2.putText(img, text, top_left, font, 1, (255,0,0),1, cv2.LINE_AA)
                            plt.figure(figsize=(20,20))
                            
                        st.write("")
                        st.write("")
                        st.subheader("Extracted Text")
                        st.image(img)            
                        
                    with col3:
                        if extract:
                            st.write('**Name** :',image_details['name'])
                            st.write('**Designation** :', image_details['designation'])
                            st.write('**Company Name** :', image_details['company_name'])
                            st.write('**Contact Number** :', image_details['contact'])
                            st.write('**Alternative Number** :', image_details['alternative'])
                            st.write('**E-mail** :', image_details['email'])
                    with col4:
                        if extract:
                            st.write('**Website** :', image_details['website'])
                            st.write('**Street** :', image_details['street'])
                            st.write('**City** :', image_details['city'])
                            st.write('**State** :', image_details['state'])
                            st.write('**Pincode** :', image_details['pincode'])
                            try:
                                query = f"SELECT email FROM bizcard WHERE email = '{image_details['email']}';"
                                cursor.execute(query)
                                conn.commit()
                                df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
                                x=df.values.tolist()                        
                                k=x[0][0]                        
                                if image_details['email'] ==k:                    
                                    st.warning("Duplicate Data, Data already exists", icon ="⚠")
                                else:
                                    pass
                            except:
                                df =pd.DataFrame(image_details, index= np.arange(1))
                                li = df.values.tolist()
                                query = "insert into bizcard values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                cursor.executemany(query,li)
                                conn.commit()   
                                col4.success('Data uploaded successfully', icon="✅")
                        
        if upload_menu == 'Undefined':
            path = False            
            col3, col4 =st.columns([2,2])
            with col3:
                uploaded_file = st.file_uploader("**Choose a file**", type=["jpg", "png", "jpeg"])
                extract = st.button("Extract Text")
                if uploaded_file is not None:
                    image_path = os.getcwd()+ "\\"+"dataset"+"\\"+ uploaded_file.name
                    image = Image.open(image_path)
                    col3.image(image)
                    path = True
            with col4:
                st.write('')
                st.write('')
                st.info(f'''i) Kindly upload the image in JPG, PNG, or JPEG format.       
                            ii) Click the "**Extract Text**" button to extract text from the image ''', icon="ℹ️")
                if path:
                    if extract:
                        img = cv2.imread(image_path)
                        reader = easyocr.Reader(['en'])#,gpu=False)
                        result = reader.readtext(image_path)
                        for detection in result:    
                            top_left =tuple([int(val) for val in detection[0][0]])
                            bottom_right =tuple([int(val) for val in detection[0][2]])
                            text = detection[1]
                            font =cv2.FONT_HERSHEY_SIMPLEX
                            img = cv2.rectangle(img, top_left, bottom_right, (0,255,0), 2)
                            img = cv2.putText(img, text, top_left, font, 1, (255,0,0),1, cv2.LINE_AA)
                            plt.figure(figsize=(20,20))
                        
                        st.write("")
                        st.write("")
                        st.write("")
                        st.subheader("Extracted Text")
                        st.image(img)
                        
                        reader = easyocr.Reader(['en'])
                        result = reader.readtext(image_path)
                        details =[]
                        for i in range(len(result)):
                            details.append(result[i][1])
                        join = " ".join(details)
                        st.markdown(f"<h3 style='color: white; text-align: left;'>{join} </h3>", unsafe_allow_html=True)
                        st.success("Data Extracted successfully", icon ='✅')

    if menu == 'Database':
        query = "SELECT * FROM bizcard;"
        cursor.execute(query)
        conn.commit()
        df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
        st.header("Database")                    
        st.dataframe(df)
        st.button('Show Changes')
     
        
        if Database_menu == 'Modify':
            modify_col,display = st.columns([1,1])
            with modify_col:
                names= ['','name','designation','email','company_name']
                selected = st.selectbox('**Select Categories**',names)
                try:
                    if selected != '':
                        select = df[selected]
                        select_detail = st.selectbox('**Select Details**', select)
                        st.header('Select the modify details')
                        df1 = df[df[selected] == select_detail]
                        df1 = df1.reset_index()
                        select_modify = st.selectbox('**Select categories**', df.columns)
                        a = df1[select_modify][0]            
                        st.write(f'Do you want to change {select_modify}: **{a}** ?')
                        modified = st.text_input(f'**Enter the {select_modify}**')
                        if modified:
                            st.write(f'{select_modify} **{a}** changed as **{modified}**')
                        if st.button("Commit Changes"):
                            cursor.execute(f"update bizcard set {select_modify} = '{modified}' where {selected} = '{select_detail}' ;")
                            conn.commit()
                            st.success("Data successfully updated", icon ='✅')
                    else:
                        select_detail = st.selectbox('**Select details**', "")
                    
                        st.header('Select the modify details')
                        select_modify = st.selectbox('**Select categories**', '')
                        modified = st.text_input('')
                except KeyError:
                    pass
                try:
                    with display:
                         if selected != '':
                            image_data = df[df[selected] == select_detail]
                            image_data = image_data.reset_index()
                            encoded_image = image_data['image'][0] # Get the base64 encoded image data from the DataFrame
                            convert = base64.b64decode(encoded_image) # Decode the base64 encoded image data back to binary
                            image = Image.open(io.BytesIO(convert)) # Open the image using PIL
                            st.image(image)
                except KeyError:
                    pass
                        
        if Database_menu == 'Delete':
            names= ['','name','email']
            delete_selected = st.selectbox('**Select Name**',names) 
            if delete_selected != '':
                
                select = df[delete_selected]
                delete_select_detail = st.selectbox('**Select Details**', select)
                st.write(f'Do you want to delete **{delete_select_detail}** card details ?')
                col5,col6,col7 =st.columns([1,1,5])
                delete = col5.button('Yes')
                delete1 = col6.button('No')
                if delete:
                    delete_query = f"delete from bizcard where {delete_selected} = '{delete_select_detail}'"
                    cursor.execute(delete_query)
                    conn.commit()
                    st.success("Data Deleted successfully", icon ='✅')
            else:
                st.selectbox('**Select Details**', ' ')
                
            
            
                
        
            
            
                
        
            