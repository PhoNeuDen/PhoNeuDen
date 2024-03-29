#=======what is python libraries=====
#Python library refers to a collection of modules and functions that extend the capabilities of the Python programming language. 
#These libraries are pre-written code that you can use to perform common tasks without having to write the code from scratch. 
#They are designed to be reusable and can save you time and effort in your development process.

# import  libraries
from cmath import nan
from fpdf import FPDF
import lasio
import numpy as np 
from numpy.core.fromnumeric import mean
import missingno as ms
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns    
import pathlib
import pandas as pd
import plotly.express as px
from PIL import Image
import tempfile
from tempfile import NamedTemporaryFile
import streamlit as st
import streamlit.components.v1 as components
import streamlit_antd_components as sac
import striplog
from striplog import Legend, Lexicon, Interval, Component, Decor


#importing images
img1 = Image.open('logo.png')
img1 = img1.resize([int(img1.width/3),int(img1.height/3.5)])
st.image(img1)

st.markdown("<h1 style='text-align: center; theme-font: harlow solid italic; font-size: 100px'> PHONEUDEN", unsafe_allow_html=True)
st.write('---')

tab1, tab2 , tab3 , tab4 = st.tabs(['THE PROJECT', 'ABOUT THE AUTHORS', 'INTRODUCTION', 'PHONEUDEN'])

with tab1:
  st.write()
  st.markdown("<h2 style='text-align: center; color: whitegrey; font-size: 30px'> Development of Python-based Web Application Program for the Visualization and Interpretation of Neutron-Density Well Logs for Lithology Determination", unsafe_allow_html=True)
  st.write('---')
with tab2: 
  st.text('Batangas State University "The National Engineering University" \n  Bachelor of Science in Petroleum Engineering \n\n created by: \n Carlvin C. Manjares \n Andre Lorenzo A. Añonuevo \n Rome Erwin M. Festin')

  st.write('---')
with tab3:
  st.markdown("<h1 style='text-align: center; text-size: 16px;'> INTRODUCTION", unsafe_allow_html=True)
  st.markdown("<p style='text-align: justify;'>   Well logging is a technique used to obtain the properties of a geological structure. It is commonly used in the field of geology, petroleum engineering, and hydrogeology. To understand the composition and structure of the formation, it measures the physical properties of rocks and fluids in the formation. Well logging is commonly used in the oil and gas industry to provide valuable data including geological formation evaluation, hydrocarbon exploration, reservoir management, environmental studies, and geotechnical engineering. The process of well logging involves different tools and sensors that can measure various properties. To determine the properties of the formation, they use different types such as Spontaneous Potential Log, Gamma Ray Log, Porosity Log, Resistivity Log, and Magnetic Resonance Imaging Log." , unsafe_allow_html=True)

  st.write('---')

with tab4:

  litho='b'
  limestone_strip = Decor({'component': Component({'hatch':litho}), 'hatch': litho, 'colour': '#eeeeee'}).plot(fmt="{hatch}")


  mode = st.selectbox(
      "Select Option",
      ('Upload File', 'Use Example File')
  )

  if mode == 'Upload File':
      file = st.file_uploader('Upload the LAS file')
      if file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(file.read())
        las_file = lasio.read(tfile.name)
        las_df=las_file.df()

        

  if mode == 'Use Example File':
      file = '15-101-22527.las'
      las_file = lasio.read(file)
      las_df=las_file.df()   
 


  if file:  
    las_df.insert(0, 'DEPT', las_df.index)
    las_df.replace(['1.00000', 1.00000], np.nan, inplace=True)
    las_df.replace(['999.2500', 999.2500], np.nan, inplace=True)
    las_df.reset_index(drop=True, inplace=True)   

    try:
      well_name =  las_file.header['Well'].WELL.value
      start_depth = las_df['DEPT'].min()
      stop_depth = las_df['DEPT'].max()
      step = abs(las_file.header['Well'].STEP.value)
      company_name =  las_file.header['Well'].COMP.value
      date =  las_file.header['Well'].DATE.value
      curvename = las_file.curves
    except:
      well_name =  'unknown'
      start_depth = 0.00
      stop_depth = 10000.00
      step = abs(las_df['DEPT'][1]-las_df['DEPT'][0])
      company_name =  'unknown'
      date =  'unknown'
      curvename = las_file.curves

    st.subheader('Well Information')
    st.text(f'================================================\nWell Name : {well_name}')
    st.text(f'Start Depth : {start_depth}')
    st.text(f'Stop Depth : {stop_depth}')
    st.text(f'Step : {step}')
    st.text(f'Company : {company_name}')
    st.text(f'Logging Date : {date}')
    
    st.subheader('Curve Information')
    st.text(f'================================================\n{curvename}')

    st.subheader('Curve Data Overview')
    st.markdown(f'The value on the left figure is number of rows. White space in each column of curve is a missing value rows/data. Expand to see more details')
    st.pyplot(ms.matrix(las_df, sparkline=False, labels=100).figure)

    # for item in las_file.well:
    #   st.text(f"{item.descr} ({item.mnemonic} {item.unit}): {item.value}")
    
    well_df = las_df
    well_df.replace(-999.2500, np.nan, inplace=True)
    well_df.replace(1.0000, np.nan, inplace=True)
    curve_list = las_df.columns.values
    curve_names = curve_list

    plot_h = 17
    plot_w = 10

    title_size = 12
    title_height = 1.0
    line_width = 0.7
    alpha = 0.8
    
    if file:
      curves = las_df.columns.values
      if 'PE' in curves:
        pe_col = las_df.columns.get_loc('PE')
      else:
        pe_col = 0
      if 'RHOB' in curves:
        den_col = las_df.columns.get_loc('RHOB')
      else:
        den_col = 0
      if 'NPHI' in curves:
        neu_col = las_df.columns.get_loc('NPHI')
      else:
        neu_col = 0
      pe_curve = las_df['PE']
      den_curve = las_df['RHOB']
      neu_curve = las_df['NPHI']

      curve_list = [pe_curve, den_curve, neu_curve]
      pe_log=las_df['PE']
      den_log=las_df['RHOB']
      neu_log=las_df['NPHI']

      
    #====================sidebar settings=======================
      st.sidebar.title('Plot Setting')
      well_name = st.sidebar.text_input('Well Name',value =(well_name))
      top_depth = st.sidebar.number_input('Top Depth', min_value=0.00, value=(start_depth), step=100.00)
      bot_depth = st.sidebar.number_input('Bottom Depth', min_value=0.00, value=(stop_depth), step=100.00)
    #====================sidebar settings End=======================  
      #-------------Pe settings---------------------------------------------------------------------------
      st.sidebar.title('Photoelectric Factor Log')
      pe_left = st.sidebar.number_input('PE Minimum Value', min_value=0.0, value=0.0, step=0.5)
      pe_right = st.sidebar.number_input('PE Maximum Value', max_value=10.0, value=10.0, step=0.5)
      #-------------Pe settings end-----------------------------------------------------------------------

      #-------------Density settings----------------------------------------------------------------------
      st.sidebar.title('Bulk Density Log')
      den_left = st.sidebar.number_input('RHOB Minimum Value', min_value=0.00, value=1.95, step=0.05)
      den_right = st.sidebar.number_input('RHOB Maximum Value', max_value=3.00, value=2.95, step=0.05)
      #-------------Density settings end------------------------------------------------------------------

      #-------------Neutron settings----------------------------------------------------------------------
      st.sidebar.title('Neutron Porosity Log')
      neu_mean = np.nanmean(las_df['NPHI'])
      if neu_mean < 1 :
        neu_left = st.sidebar.number_input('NPHI Minimum Value', min_value=-50.00, value=0.45)
        neu_right = st.sidebar.number_input('NPHI Maximum Value', min_value=-50.00, value=-0.15)
      if neu_mean > 1:
        neu_left = st.sidebar.number_input('NPHI Minimum Value', min_value=-50.00, value=45.00)
        neu_right = st.sidebar.number_input('NPHI Maximum Value', min_value=-50.00, value=-15.00)
      den_neu_div = st.sidebar.radio('Number of Division:',[4,5])
      dn_xover = st.sidebar.radio('Hydrocarbon Bearing',['Yellow','Gold','None'])
      dn_sep = st.sidebar.radio('N-D Colour',['Lightgray','Green', 'None'])

      #-------------Neutron settings end------------------------------------------------------------------

      
      #-------------Formation Evaluation settings---------------------------------------------------------
      st.sidebar.write('---')
      st.sidebar.title('Formation Evaluation Settings')
      
      denmat = st.sidebar.number_input('Matrix-Density', min_value=1.0, value=2.71, step=0.1)
      denfl = st.sidebar.number_input('Fluid-Density', min_value=0.0, value=1.0, max_value=1.5, step=0.1)
      dphi = (denmat - den_log)/(denmat-denfl)
      den_shale = st.sidebar.number_input('Density at 100% Shale', min_value=1.0, value=2.71, step=0.1)
      dphi_shale = (den_shale - den_log)/(den_shale-denfl)
      dphi_shale = np.clip(dphi_shale, 0, 1)
      neu_shale = st.sidebar.number_input('Neutron at 100% Shale', min_value=0.0, value=0.35, step=0.1)
      neu_mean = neu_log.mean()
      
      #-------------Volume of Shle settings ------------------------------------------------------------
      vsh_log = (neu_log - dphi)/(neu_shale-dphi_shale) *100
      vsh_log = np.clip(vsh_log, 0, 100)
      vsh_color = 'black'
      well_df['VSH'] = vsh_log
      shale_shading = st.sidebar.radio('Shale Shading',['Gray','Green'])
      vsh_trackname = f'Volume of shale (%)'
      #-------------Volume of Shle settings End------------------------------------------------------------
      
      #-------------sidebar-porosity settings------------------------------------------------------------
      st.sidebar.title('Porosity')
      mode = st.sidebar.radio(
        "Choose the Porosity Method",
        ('Density-Neutron', 'Density')
        )
      
      #-------------Density-Porosity settings------------------------------------------------------------
      if mode == 'Density':
        density_mat = st.sidebar.number_input('Matrix Density', min_value=1.0, value=2.71, step=0.1)
        density_fluid = st.sidebar.number_input('Fluid Density', min_value=0.0, value=1.0, max_value=1.5, step=0.1)
        dphi_log = (density_mat - den_log)/(density_mat-density_fluid)
          
        tpor_log = dphi_log  
        tpor_log = np.clip(tpor_log, 0.001, 1)
        
        epor_log = tpor_log*(1-vsh_log/100)
        epor_log = np.clip(epor_log, 0.001, 1)
      #-------------Density-Porosity settings end--------------------------------------------------------
      
      #-------------Density-Neutron-porosity settings----------------------------------------------------
      if mode == 'Density-Neutron':
        density_mat = st.sidebar.number_input('Matrix Density', min_value=1.0, value=2.71, step=0.1)
        density_fluid = st.sidebar.number_input('Fluid Density', min_value=0.0, value=1.0, max_value=1.5, step=0.1)
        dphi_log = (density_mat - den_log)/(density_mat-density_fluid)
        dnphi_log = ((dphi_log**2 + neu_log**2)/2)**0.5
          
        tpor_log = dnphi_log
        tpor_log = np.clip(tpor_log, 0.001, 1)
        
        epor_log = tpor_log*(1-vsh_log/100)
        epor_log = np.clip(epor_log, 0.001, 1)
        
      por_left = st.sidebar.number_input('Left Scale', min_value=0, max_value=100, value=35, step=10)
      por_right = st.sidebar.number_input('Right Scale', min_value=0, max_value=100, value=0, step=10)
      por_grid = st.sidebar.number_input('Number of Grids', min_value = 0, value=8, step =1)
      por_color = 'black'
      por_shading = st.sidebar.radio('Total Porosity Shading',['Aqua','None'])
      #-------------Density-Neutron-porosity settings end------------------------------------------------

      #-------------Porosity to Display settings------------------------------------------------------------
      mode = st.sidebar.radio(
        "Porosity to Display",
        ('Effective Porosity', 'Total Porosity')
      )
      if mode == 'Total Porosity':
        por_log = tpor_log*100
        por_trackname = f'Total Porosity(p.u.)\n'
      if mode == 'Effective Porosity':
        por_log = epor_log*100
        por_trackname = f'Effective Porosity(p.u.)\n'
      #-------------Porosity to Display settings end--------------------------------------------------------
      #print total porosity & effective porosity
        
      well_df['TPOR'] = tpor_log
      well_df['EPOR'] = epor_log


      # litholofy algorithms 

      sandstone =np.where(( 0.06<=neu_log) & (neu_log <=0.27 ) & (1.8<=den_log) & (den_log<= 2.65), 1, 0)
      dolomite = np.where( ( 0.01<=neu_log) & (neu_log <=0.18 ) & (2.3<=den_log) & (den_log<= 2.8), 1, 0)
      shale = np.where(( 0.28<=neu_log) & (neu_log <=0.39 ) & (1.6<=den_log) & (den_log<= 2.9), 1, 0)
      limestone = np.where(( 0.00<=neu_log) & (neu_log <=0.10 ) & (2.2<=den_log) & (den_log<= 2.71), 1, 0)
      anhydrite = np.where(( 4.80<=pe_log) & (pe_log <=5.15 ) & (2.91<=den_log) & (den_log<= 2.99), 1, 0)
      halite = np.where(( 3.8<=pe_log) & (pe_log <=4.7 ) & (1.90<=den_log) & (den_log<= 2.19), 1, 0)
      oil = np.where(( 0.8<=pe_log) & (pe_log <=0.15 ) & (0.4<=den_log) & (den_log<= 0.12), 1, 0)
      #-------------Formation Evaluation settings end----------------------------------------------------
#-------------Scatter Plot settings-----------------------------------------------------------------
      st.sidebar.write('---')
      st.sidebar.title('Scatter Plot')
      st.write('---')
      st.sidebar.header("Scatter Plot Axis")
      
      x_curve =st.sidebar.selectbox('Select Curve for X-axis  ', las_df.columns.values)
      y_curve = st.sidebar.selectbox('Select Curve for Y-axis', las_df.columns.values)
      z_curve = st.sidebar.selectbox('Select Curve for Z-axis', las_df.columns.values)
      st.sidebar.write('---')

      scale_x_left = st.sidebar.number_input ('Left Scale X-axis', value= well_df[x_curve].min())
      scale_x_right = st.sidebar.number_input ('Right Scale X-axis', value = well_df[x_curve].max())
      agreex = st.sidebar.checkbox('Logarithmic Scale on X')
      if agreex:
        log_valuex = True
      else:
        log_valuex=False
      scale_y_upper = st.sidebar.number_input ('Upper Scale Y-axis', value= well_df[y_curve].min())
      scale_y_bottom = st.sidebar.number_input ('Bottom Scale Y-axis', value = well_df[y_curve].max())
      agreey = st.sidebar.checkbox('Logarithmic Scale on Y')
      if agreey:
        log_valuey = True
      else:
        log_valuey=False

      scale_z_left = st.sidebar.number_input ('Upper Scale Z-axis', value= well_df[z_curve].min())
      scale_z_right = st.sidebar.number_input ('Bottom Scale Z-axis', value = well_df[z_curve].max())
      st.write('---')
      #-------------Scatter Plot settings end-------------------------------------------------------------
      #=========================================================
      st.markdown("<h1 style='text-align: center; text-size: 16px;'> CHOOSE A PLOT", unsafe_allow_html=True)

      st.write('---')
      st.markdown("<h1 style='text-align: center; text-size: 16px;'> Triple Combo Plot", unsafe_allow_html=True)
      st.markdown("<p style='text-align: center; text-size: 12px;'> ========================================================================================", unsafe_allow_html=True)
      st.markdown("<p style='text-align: justify; text-size: 12px;'> Triple Combo Plot: Shows the graphical representation of the curves Photoelectric Factor, Bulk Density and Neutron Porosity, proportional to their depth.", unsafe_allow_html=True)
      st.markdown("<p style='text-align: center; text-size: 12px;'> ========================================================================================", unsafe_allow_html=True)
      TCP = st.button("Triple Combo Plot");
      #=================== triple combo tracks==========================================
      if TCP:
        
    
        st.title('Triple Combo Plot')
            #====================
      
        pe_color = 'green'
        a_trackname = 'Photoelectric Factor (PEF) \n (b/e)'
        
        if pe_right == 10:
          pe_div = 6
        else:
          pe_div=5
        
        den_color = 'red'
        b_trackname = 'Bulk Density (RHOB) \n (g/cc)'
        
        
        neu_color = 'blue'
        c_trackname = 'Neutron Porosity (NPHI) \n (decp)'

        #fig, ax = plt.subplots(figsize=(plot_w,plot_h))
        fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(plot_w,plot_h), sharey=True)
        fig.suptitle(f"Triple Combo Plot\n===================\nWell: {well_name}\n(Interval: {top_depth} - {bot_depth})",
                    size=title_size, y=title_height)
        
        #General setting for all axis
        for axes in ax:
          axes.set_ylim (top_depth,bot_depth)
          axes.invert_yaxis()
          axes.yaxis.grid(True)
          axes.get_xaxis().set_visible(False)
        
        #================================== Photoelectric effect track============================================================
        ax1=ax[0].twiny()
        ax1.get_xaxis().set_visible(True)
        ax1.plot( pe_log,"DEPT",  data = well_df, color = pe_color, lw=line_width,alpha=alpha)
        ax1.set_xlim(pe_left, pe_right)
        ax1.set_xlabel(a_trackname)
        ax1.xaxis.label.set_color(pe_color)
        ax1.tick_params(axis='x', colors=pe_color)
        ax1.spines["top"].set_edgecolor(pe_color)
        ax1.spines["top"].set_position(("axes", 1.02))
        ax1.set_xticks(list(np.linspace(pe_left, pe_right, num = pe_div)))
        ax1.grid(which='major', color='silver', linestyle='-')
        ax1.grid(which='minor', color='lightgrey', linestyle=':', axis='y')


      #===================================== Density track=======================================================================
        ax11=ax[1].twiny()
        ax11.plot(den_log, "DEPT", data = well_df, color = den_color, lw=line_width,alpha=alpha)
        ax11.set_xlabel(b_trackname)
        ax11.minorticks_on()
        ax11.set_xlim(den_left, den_right)
        ax11.xaxis.label.set_color(den_color)
        ax11.tick_params(axis='x', colors=den_color)
        ax11.spines["top"].set_edgecolor(den_color)
        ax11.spines["top"].set_position(("axes", 1.02))
        ax11.set_xticks(list(np.linspace(den_left, den_right, num = (den_neu_div+1))))
        ax11.grid(which='major', color='silver', linestyle='-')
        ax11.grid(which='minor', color='lightgrey', linestyle=':', axis='y')
        ax11.xaxis.set_ticks_position("top")
        ax11.xaxis.set_label_position("top")

      #===================================== Neutron track=======================================================================
        ax21=ax[2].twiny()
        ax21.plot(neu_log, "DEPT", data = well_df, color = neu_color, lw=line_width, alpha=alpha)
        ax21.set_xlabel(c_trackname)
        ax21.minorticks_on()
        ax21.xaxis.label.set_color(neu_color)
        ax21.set_xlim(neu_left, neu_right)
        ax21.tick_params(axis='x', colors=neu_color)
        ax21.spines["top"].set_position(("axes", 1.02))
        ax21.spines["top"].set_edgecolor(neu_color)
        ax21.set_xticks(list(np.linspace(neu_left, neu_right, num = (den_neu_div+1))))
        ax21.grid(which='major', color='silver', linestyle='-')
        ax21.grid(which='minor', color='lightgrey', linestyle=':', axis='y')
        ax21.xaxis.set_ticks_position("top")
        ax21.xaxis.set_label_position("top")
       
      #==========================Combination of Tracks=======================================================
        # Density track
        ax31=ax[3].twiny()
        ax31.plot(den_log, "DEPT", data = well_df, color = den_color, lw=line_width, alpha=alpha)
        ax31.set_xlabel(b_trackname)
        ax31.minorticks_on()
        ax31.set_xlim(den_left, den_right)
        ax31.xaxis.label.set_color(den_color)
        ax31.tick_params(axis='x', colors=den_color)
        ax31.spines["top"].set_edgecolor(den_color)
        ax31.spines["top"].set_position(("axes", 1.02))
        ax31.set_xticks(list(np.linspace(den_left, den_right, num = (den_neu_div+1))))
        ax31.grid(which='major', color='silver', linestyle='-')
        ax31.grid(which='minor', color='lightgrey', linestyle=':', axis='y')
        ax31.xaxis.set_ticks_position("top")
        ax31.xaxis.set_label_position("top")

        # Neutron trak placed ontop of density track
        ax32=ax[3].twiny()
        ax32.plot(neu_log, "DEPT", data = well_df, color = neu_color, lw=line_width, alpha=alpha)
        ax32.set_xlabel(c_trackname)
        ax32.minorticks_on()
        ax32.xaxis.label.set_color(neu_color)
        ax32.set_xlim(neu_left, neu_right)
        ax32.tick_params(axis='x', colors=neu_color)
        ax32.spines["top"].set_position(("axes", 1.08))
        ax32.spines["top"].set_visible(True)
        ax32.spines["top"].set_edgecolor(neu_color)
        ax32.set_xticks(list(np.linspace(neu_left, neu_right, num = (den_neu_div+1))))
        ax32.grid(which='major', color='silver', linestyle='-')
        ax32.grid(which='minor', color='lightgrey', linestyle=':', axis='y')
        ax32.xaxis.set_ticks_position("top")
        ax32.xaxis.set_label_position("top")

        #shading between density and neutron
        x1=den_log
        x2=neu_log

        x = np.array(ax31.get_xlim())
        z = np.array(ax32.get_xlim())

        nz=((x2-np.max(z))/(np.min(z)-np.max(z)))*(np.max(x)-np.min(x))+np.min(x)

        ax31.fill_betweenx(well_df['DEPT'], x1, nz, where=x1>=nz, interpolate=True, color=dn_sep, linewidth=0, alpha=0.8)
        ax31.fill_betweenx(well_df['DEPT'], x1, nz, where=x1<=nz, interpolate=True, color=dn_xover, linewidth=0, alpha=0.8)

        plt.tight_layout()
        plt.show() 
        st.pyplot(fig)

               
      #=================== download feature ================================================
        #exporting as pdf
        pdf = FPDF()
        pdf.add_page()
        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
          fig.savefig(tmpfile.name)
          pdf.image(tmpfile.name, 10, 10, (plot_w*16), (plot_h*16))
        st.download_button(
          "Download Triple Combo Plot as PDF",
          data=pdf.output(dest='S').encode('latin-1'),
          file_name=f"{well_name}_triple_combo.pdf",
        )
      #=================== triple combo plot end==========================================
      st.write('---')
      st.markdown("<h1 style='text-align: center; text-size: 16px;'> Formation Evaluation", unsafe_allow_html=True)
      st.markdown("<p style='text-align: center; text-size: 12px;'> ========================================================================================", unsafe_allow_html=True)
      st.markdown("<p style='text-align: justify; text-size: 12px;'> Formation Evaluation: This function shows the possible prediction of lithologies in the well. It shows the following results such as the Volume of Shale, the Total Porosity and the Effective Porosity. It can also download the results as a CSV file", unsafe_allow_html=True)
      st.markdown("<p style='text-align: center; text-size: 12px;'> ========================================================================================", unsafe_allow_html=True)

      form_eval = st.button("Formation Evaluation");
        
      
      if form_eval:
      #=================== Formation Evaluation ==========================================
        
        #=====================Formation Evaluation Plot=========================  
        
      
        lithology_numbers = {30000: {'lith':'Sandstone', 'lith_num':1, 'hatch': '..', 'color':'#ffff00'},
                        65000: {'lith':'Shale', 'lith_num':2, 'hatch':'--', 'color':'#bebebe'},
                        74000: {'lith':'Dolomite', 'lith_num':3, 'hatch':'-/', 'color':'#8080ff'},
                        70000: {'lith':'Limestone', 'lith_num':4, 'hatch':'+', 'color':'#80ffff'},
                        88000: {'lith':'Halite','lith_num':6,'hatch':'XXXXX','color':'#7ddfbe'},
                        86000: {'lith':'Anhydrite','lith_num':7,'hatch':'x','color':'#ff80ff'},}
                        
        y = [0, 1]
        x = [1, 1]

        fig, axes = plt.subplots(ncols=3,nrows=2, sharex=True, sharey=True,
                                figsize=(10,2), subplot_kw={'xticks': [], 'yticks': []})

        for ax, key in zip(axes.flat, lithology_numbers.keys()):
            ax.plot(x, y)
            ax.fill_betweenx(y, 0, 1, facecolor=lithology_numbers[key]['color'], hatch=lithology_numbers[key]['hatch'])
            ax.set_xlim(0, 0.1)
            ax.set_ylim(0, 1)
            ax.set_title(str(lithology_numbers[key]['lith']))

        plt.tight_layout()

        plt.show()
        st.pyplot(fig)
        
        #fig, ax = plt.subplots(figsize=(10,20), sharex=True, sharey=True)
        fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(plot_w,plot_h), sharey=True)
        fig.suptitle(f"Formation Evaluation Plot\n===================\nWell: {well_name}\n(Interval: {top_depth} - {bot_depth})",
                    size=title_size, y=title_height)
        for axes in ax:
          axes.get_xaxis().set_visible(False)
        
        #================Set up the plot axes========================
        ax1 = plt.subplot2grid((1,3), (0,0), rowspan=2, colspan = 1)
        ax2 = plt.subplot2grid((1,3), (0,1), rowspan=2, colspan = 1)
        ax3 = plt.subplot2grid((1,3), (0,2), rowspan=2, colspan = 1)
        
        ax4 = ax1.twiny()
        ax4.xaxis.set_visible(False)
        ax4 = ax2.twiny()
        ax4.xaxis.set_visible(False)
        ax4 = ax3.twiny()
        ax4.xaxis.set_visible(False)
        ax5 = ax3.twiny()
        ax5.xaxis.set_visible(False)
        ax6 = ax3.twiny()
        ax6.xaxis.set_visible(False)
        ax7 = ax3.twiny()
        ax7.xaxis.set_visible(False)
        ax8 = ax3.twiny()
        ax8.xaxis.set_visible(False)
        ax9 = ax3.twiny()
        ax9.xaxis.set_visible(False)

        
        
        #===========================Volume of shale track================================
        ax1.plot(vsh_log, "DEPT", data = well_df, color = vsh_color, lw=line_width)
        ax1.set_xlabel(vsh_trackname)
        ax1.minorticks_on()
        ax1.set_xlim(0, 100)
        ax1.set_ylim(bot_depth, top_depth)
        ax1.xaxis.label.set_color(vsh_color)
        ax1.tick_params(axis='x', colors=vsh_color)
        ax1.spines["top"].set_edgecolor(vsh_color)
        ax1.spines["top"].set_position(("axes", 1.02))
        ax1.set_xticks(list(np.linspace(0, 100, num = 5)))
        ax1.grid(which='major', color='grey', linestyle='--')
        ax1.grid(which='minor', color='lightgrey', linestyle='-.', axis='y')
        ax1.xaxis.set_ticks_position("top")
        ax1.xaxis.set_label_position("top")
        #===========================Volume of shale track end================================
        #area-fill sand and shale for VSH
        ax1.fill_betweenx(well_df['DEPT'], 0, vsh_log, interpolate=False, color = shale_shading, linewidth=0, alpha=0.5, hatch = '--')
        
        #==================================total/effective Porosity track====================================
        ax2.plot(por_log, "DEPT", data = well_df, color = por_color, lw=line_width)
        ax2.set_xlabel(por_trackname)
        ax2.minorticks_on()
        ax2.set_xlim(por_left, por_right)
        ax2.set_ylim(bot_depth, top_depth)
        ax2.xaxis.label.set_color(por_color)
        ax2.tick_params(axis='x', colors=por_color)
        ax2.spines["top"].set_edgecolor(por_color)
        ax2.spines["top"].set_position(("axes", 1.02))
        ax2.set_xticks(list(np.linspace(por_left, por_right, num = int(por_grid))))
        ax2.grid(which='major', color='grey', linestyle='--')
        ax2.grid(which='minor', color='lightgrey', linestyle='-.', axis='y')
        ax2.xaxis.set_ticks_position("top")
        ax2.xaxis.set_label_position("top")
        if por_shading == 'Aqua':
          ax2.fill_betweenx(well_df['DEPT'], por_log, 0, interpolate=True, color = 'aqua', linewidth=0, alpha=0.5)
        
        #==================================total/effective Porosity track====================================

        ##area-fill tpor and epor
        
          
        ax3.plot(shale, "DEPT", data = well_df, color = '#bebebe', lw=0.8)
        ax3.set_xlabel('Lithology')
        ax3.minorticks_off()
        ax3.set_xlim(1, 0)
        ax3.set_ylim(bot_depth, top_depth)
        ax3.xaxis.set_label_position("top")
        ax3.xaxis.set_ticks_position("top")
        ax3.spines["top"].set_position(("axes", 1.02))
        ax3.spines["top"].set_visible(True)
        ax3.spines["top"].set_edgecolor('black')
        ax3.set_xticks(list(np.linspace(1, 0, num = 2)))
        ax3.fill_betweenx(well_df['DEPT'], shale, 0, interpolate=False, facecolor = '#bebebe', linewidth=0.8, alpha=0.8, hatch = '--')

        ax4.plot(sandstone, "DEPT", data = well_df, lw=0.8)
        ax4.set_xlim(1, 0)
        ax4.set_ylim(bot_depth, top_depth)
        ax4.fill_betweenx(well_df['DEPT'], sandstone, 0, interpolate=False, facecolor = '#ffff00', linewidth=0.8, alpha=0.8, hatch = '..')

        ax5.plot(dolomite, "DEPT", data = well_df, lw=0.8)
        ax5.set_xlim(1, 0)
        ax5.set_ylim(bot_depth, top_depth)
        ax5.fill_betweenx(well_df['DEPT'], dolomite, 0, interpolate=False, facecolor = '#8080ff', linewidth=0.8, alpha=0.8, hatch = '-/')

        ax6.plot(limestone, "DEPT", data = well_df, lw=0.8)
        ax6.set_xlim(1, 0)
        ax6.set_ylim(bot_depth, top_depth)
        ax6.fill_betweenx(well_df['DEPT'], limestone, 0, interpolate=False, facecolor = '#80ffff', linewidth=0.8, alpha=0.8, hatch = '+')
        
        ax7.plot(anhydrite, "DEPT", data = well_df, lw=0.8)
        ax7.set_xlim(1, 0)
        ax7.set_ylim(bot_depth, top_depth)
        ax7.fill_betweenx(well_df['DEPT'], anhydrite, 0, interpolate=False, facecolor = '#ff80ff', linewidth=0.8, alpha=0.8, hatch = 'x')

        ax8.plot(halite, "DEPT", data = well_df, lw=0.8)
        ax8.set_xlim(1, 0)
        ax8.set_ylim(bot_depth, top_depth)
        ax8.fill_betweenx(well_df['DEPT'], halite, 0, interpolate=False, facecolor = '#7ddfbe', linewidth=0.8, alpha=0.8, hatch = 'XXXXX')

         
        
        plt.tight_layout()

        plt.show() 
        st.pyplot(fig)

        #exporting as pdf
        pdf = FPDF()
        pdf.add_page()
        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
          fig.savefig(tmpfile.name)
          pdf.image(tmpfile.name, 10, 10, (plot_w*16), (plot_h*16))
        st.download_button(
          "Download Formation Evaluation Plot as PDF",
          data=pdf.output(dest='S').encode('latin-1'),
          file_name=f"{well_name}_Formation_Eval.pdf",
        )

        well_df= well_df.query(f"`DEPT` >= {top_depth} and `DEPT` <= {bot_depth}")
        st.markdown('**Final Result, Expand to See Full Data.**')
        st.text('VSH, TPOR, and EPOR are in the Last Right 3 Columns')
        well = well_df[['DEPT','PE','RHOB','NPHI','VSH','EPOR','TPOR']]

        st.write (well)
        

        st.title('Downloading Final Result as CSV')
        st.markdown('**REMARKS**: _The CSV file will include input LAS data (Photoelectric effect, Bulk Density, and Neutron Porosity)_ **AND** _Formation Evaluation Result: Volume of Shale (%), Porosity (dec) at the above depth interval_')

        #exporting as CSV
        @st.cache_data
        def convert_df(df):
          return df.to_csv().encode('utf-8')


        csv = convert_df(well_df)

        st.download_button(
          "Download the Formation Evaluation CSV file",
          csv,
          f"{well_name}_Formation_Evaluation.csv",
          "text/csv",
          key='download-csv'
        )
    #=================== Formation Evaluation end==========================================
      #=================== Scatter Plot ==========================================
      st.write('---')
      st.markdown("<h1 style='text-align: center; text-size: 16px;'> Cross Plot", unsafe_allow_html=True)
      st.markdown("<p style='text-align: center; text-size: 12px;'> ========================================================================================", unsafe_allow_html=True)
      st.markdown("<p style='text-align: justify; text-size: 12px;'> Cross Plot: Present the cross plot of Neutron Porosity as the X-axis and Bulk Density as the Y-axis, for the Z-axis it will be the depth of the well. In the Cross Plot Settings you can choose different curves as there are many types of cross plotting. (Note: It is for future development of the program)", unsafe_allow_html=True)
      st.markdown("<p style='text-align: center; text-size: 12px;'> ========================================================================================", unsafe_allow_html=True)

      st.markdown("<h3 style='text-align: justify; text-size: 16px;'> Choose a Dimension for Cross Plot", unsafe_allow_html=True)

      demi2 = st.button('2D Cross Plot')

      demi3 = st.button('3D Cross Plot')
      if demi2:

        st.title('Cross Plot')
        
        fig=px.scatter(well_df, x=x_curve, y=y_curve,log_y=log_valuey,log_x = log_valuex,
                      color = z_curve, range_x=[scale_x_left, scale_x_right], range_y = [scale_y_bottom, scale_y_upper],
                      color_continuous_scale=px.colors.sequential.Jet)
        st.plotly_chart(fig)


        
        lsX = np.linspace(0,0.45,46)
        ssCnlX = np.empty((np.size(lsX),0), float)
        dolCnlX = np.empty((np.size(lsX),0), float)

        for n in np.nditer(lsX):

            ssCnlX = np.append(ssCnlX, np.roots([0.222, 1.021, 0.039 - n])[1])
            dolCnlX = np.append(dolCnlX, np.roots([1.40, 0.389, -0.01259 - n])[1])
        denLs = (1 - 2.71) * lsX + 2.71
        denSs = (1 - 2.65) * lsX + 2.65  
        denDol = (1 - 2.87) * lsX + 2.87    
        fig, ax = plt.subplots()
        x = las_df['NPHI']
        y = las_df['RHOB']
        cbar=las_df['DEPT']
        ax1 = plt.subplot2grid((1,1), (0,0), rowspan=2, colspan = 2)
        ax1.scatter(x,y,c=cbar,cmap='jet', alpha=0.5)
        ax1.set_title("ND Crossplot")
        ax1.set_xlabel("Neutron Porosity [v.v]")
        ax1.set_ylabel("Density g/cc")
        ax1.set_xlim(-0.15, 0.5)
        ax1.set_ylim(3, 1.6)
        ax1.grid(True)
        ax1.plot(ssCnlX, denSs, '.-', color='blue', label = 'Sandstone')
        ax1.plot(lsX, denLs, '.-', color='black', label = 'Limestone')
        ax1.plot(dolCnlX, denDol, '.-', color='red', label = 'Dolomite')
        ax1.legend(loc='best')
        fig.subplots_adjust(wspace = 0.6)
        fig.subplots_adjust(hspace = 0.8)

        plt.tight_layout()
        plt.show() 
        st.pyplot(fig)

        #exporting as pdf
        pdf = FPDF()
        pdf.add_page()
        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
          fig.savefig(tmpfile.name)
          pdf.image(tmpfile.name, 10, 10, (plot_w*20), (plot_h*16))
        st.download_button(
          "Download 2D Cross Plot as PDF",
          data=pdf.output(dest='S').encode('latin-1'),
          file_name=f"{well_name}_2D_Cross_Plot.pdf",
        )
      if demi3:
        from mpl_toolkits.mplot3d import Axes3D
        cbar = (las_df[z_curve])
        fig = plt.figure(figsize=(5,5))
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(las_df[x_curve], las_df[y_curve], las_df[z_curve], alpha= 0.7, c=cbar, cmap='jet')
        plt.tight_layout()
        plt.show() 
        st.pyplot(fig)
        #exporting as pdf
        pdf = FPDF()
        pdf.add_page()
        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
          fig.savefig(tmpfile.name)
          pdf.image(tmpfile.name, 10, 10, (plot_w*16), (plot_h*16))
        st.download_button(
          "Download 3D Cross Plot as PDF",
          data=pdf.output(dest='S').encode('latin-1'),
          file_name=f"{well_name}_3D_Cross_Plot.pdf",
        ) 
      #=================== Scatter Plot end==========================================
            
  st.write('---')


