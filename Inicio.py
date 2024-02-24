import streamlit as st 


st.set_page_config(page_title= "La Liga",
                   layout='centered',
                   page_icon= ":soccer:",
                #    layout="wide"
                )
st.sidebar.image('data/LOGO.jpg')

st.title('Historia de La Liga Española')
st.divider()
st.markdown(
    '''
        Esta aplicación está diseñada para obtener el máximo de información sobre  
        los resultados históricos de La Liga. En el menú de la izquierda podrás   
        aprender al interactuar con representaciones visuales de los datos desde 1928.  
    '''
)
st.divider()  
st.markdown(
    '''    
         ### Hemos dividido la información en 4 páginas:
            1.Resumen:     
                        Contiene información general de los equipos con más participaciones  
                        más participaciones en la liga (más de 20). Podrás explorar sus   
                        úbicaciones geográficas el número de trofeos de La Liga y cuándo los  
                        obtuvieron.   
            2.Hisóricos:   
                        Con estádisticas historicas para los equipos que quieras ver. Podrás  
                        hacer comparaciones de equipos a través de los años y enfocarte en  
                        los periodos de tiempo y los datos que más te interesen.   
                           
            3.Temporadas:   
                        Esta página esta diseñada para date un resumen de lo que ha pasado  
                        cada temporada de La Liga. Podrás escoger el año que te interese y  
                        descubrir los detalles más interesantes.   
            4.Equipos:   
                        Y para conocer más sobre tu equipo favorito o aprender un poco sobre  
                        algún equipo rival podrás visitar esta página.   
     '''                       
    
)
css="""
<style>
    [data-testid="stMarkdown"] {
        background: LightBlue;
    }
</style>
"""
st.write(css, unsafe_allow_html=True)

st.markdown("""     
            <style>         
                     
            [class='st-emotion-cache-k4gfp0 eczjsme5] {             
            color: white; 
                     
            }     
            </style> """, 
            unsafe_allow_html=True)
