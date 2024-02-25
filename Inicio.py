import streamlit as st
from PIL import Image
import io
import base64



st.set_page_config(page_title="La Liga",
                   layout='centered',
                   page_icon=":soccer:",
                   #    layout="wide"
                   )

st.markdown("""
        <style>
        @font-face {
            font-family: 'LALIGAText-Regular';
            src: url('https://assets.laliga.com/assets/public/fonts/LALIGAText-Regular.woff2') format('woff2');
        }

        *  {
            font-family: 'LALIGAText-Regular', sans-serif;
        }
        </style>
        """, unsafe_allow_html=True)
# st.sidebar.header('Menú')


# Cargar la imagen
imagen = Image.open('ui/laliga_logo.png')

# Convertir la imagen a bytes
img_bytes = io.BytesIO()
imagen.save(img_bytes, format='PNG')
img_bytes = img_bytes.getvalue()

# Convertir bytes a base64
img_str = base64.b64encode(img_bytes).decode()

# Mostrar la imagen centrada y más pequeña
st.markdown(
    f'<div style="display: flex; justify-content: center;">'
    f'<img src="data:image/png;base64,{img_str}" style="max-width: 50%; height: auto;" />'
    f'</div>',
    unsafe_allow_html=True
)

st.divider()
st.markdown(
    '''
        <div style="text-align: justify">
        Esta aplicación está diseñada para obtener el máximo de información sobre  
        los resultados históricos de La Liga. En el menú de la izquierda podrás   
        aprender al interactuar con representaciones visuales de los datos desde 1928.  
        </div>
    ''', unsafe_allow_html=True
)
st.divider()
st.markdown(
    '''
    Hemos dividido la información en 4 páginas:

    1. **Resumen:** Contiene información general de los equipos con más participaciones en la liga (más de 20). Podrás explorar sus ubicaciones geográficas el número de trofeos de La Liga y cuándo los obtuvieron.

    2. **Históricos:** Con estadísticas históricas para los equipos que quieras ver. Podrás hacer comparaciones de equipos a través de los años y enfocarte en los periodos de tiempo y los datos que más te interesen.

    3. **Temporadas:** Esta página está diseñada para darte un resumen de lo que ha pasado cada temporada de La Liga. Podrás escoger el año que te interese y descubrir los detalles más interesantes.

    4. **Equipos:** Y para conocer más sobre tu equipo favorito o aprender un poco sobre algún equipo rival podrás visitar esta página.
    ''')




