import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Generar datos de ejemplo
np.random.seed(0)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
central_options = ['Central A', 'Central B', 'Central C']
area_operativa_options = ['Prelavado', 'Clasificación', 'Empaquetado']
turno_options = ['Mañana', 'Tarde', 'Noche']
proveedor_options = ['Proveedor X', 'Proveedor Y', 'Proveedor Z']
rubro_options = ['Rubro1', 'Rubro2', 'Rubro3']
tipo_insumo_options = ['Tipo1', 'Tipo2']
cliente_options = ['Cliente1', 'Cliente2', 'Cliente3']
instrumento_options = ['Instrumento1', 'Instrumento2', 'Instrumento3']
IMS_options = ['IMS1', 'IMS2']
tipo_proceso_options = ['Proceso1', 'Proceso2']
tipo_orden_options = ['Orden1', 'Orden2']

# Crear DataFrame de ejemplo
df = pd.DataFrame({
    'Fecha': np.random.choice(dates, 1000),
    'Central': np.random.choice(central_options, 1000),
    'Área Operativa': np.random.choice(area_operativa_options, 1000),
    'Turno': np.random.choice(turno_options, 1000),
    'Proveedor': np.random.choice(proveedor_options, 1000),
    'Rubro': np.random.choice(rubro_options, 1000),
    'Tipo de insumo': np.random.choice(tipo_insumo_options, 1000),
    'Cliente': np.random.choice(cliente_options, 1000),
    'Instrumento': np.random.choice(instrumento_options, 1000),
    'IMS': np.random.choice(IMS_options, 1000),
    'Tipo de proceso': np.random.choice(tipo_proceso_options, 1000),
    'Tipo de orden': np.random.choice(tipo_orden_options, 1000)
})

# Agregar columnas de métricas de ejemplo
df['Tiempos Inactivos'] = np.random.uniform(0, 120, size=len(df))  # minutos/horas
df['Vacantes No Cubiertas'] = np.random.randint(0, 10, size=len(df))
df['Días Inventario Insumos'] = np.random.uniform(1, 30, size=len(df))
df['Incidencias Cliente y Central'] = np.random.randint(0, 20, size=len(df))
df['Estado y Etapa IMS'] = np.random.uniform(0, 100, size=len(df))
df['Capacidad Utilización'] = np.random.uniform(50, 100, size=len(df))
df['Tiempo Entrega Equipos'] = np.random.uniform(1, 10, size=len(df))  # días/horas
df['Volumen Consumido Monto'] = np.random.uniform(1000, 10000, size=len(df))
df['Porcentaje Abastecimiento'] = np.random.uniform(70, 100, size=len(df))

# Definir un esquema de colores uniforme
COLOR_PALETTE = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
TEMPLATE = "plotly_white"  # Usar un template limpio y profesional

# Streamlit app layout
st.title("Dashboard de Operaciones - Healthic")
st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Tiempos Inactivos", 
    "Vacantes No Cubiertas", 
    "Días Inventario de Insumos",
    "Incidencias por Cliente y Central",
    "Estado y Etapa de Instrumentos en IMS",
    "Capacidad de Utilización de Centrales",
    "Tiempo de Entrega de Equipos",
    "Volumen Consumido en Monto",
    "Porcentaje de Abastecimiento"
])

# Tab 1: Tiempos Inactivos
with tab1:
    st.subheader("Tiempos Inactivos")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("Filtros")
        central = st.selectbox("Central", options=central_options, key="central_tiempo")
        area = st.selectbox("Área Operativa", options=area_operativa_options, key="area_tiempo")
        start_date, end_date = st.date_input("Fecha", [dates.min(), dates.max()], key="date_tiempo")
    
    with col2:
        # Filter data based on selections
        dff = df[(df['Central'] == central) & (df['Área Operativa'] == area) &
                (df['Fecha'] >= pd.to_datetime(start_date)) & (df['Fecha'] <= pd.to_datetime(end_date))]
        
        # Create histogram
        fig = px.histogram(dff, x="Tiempos Inactivos", nbins=20, 
                          title="Distribución de Tiempos Inactivos",
                          color_discrete_sequence=[COLOR_PALETTE[0]],
                          template=TEMPLATE)
        
        fig.update_layout(
            xaxis_title="Tiempo Inactivo (minutos)",
            yaxis_title="Frecuencia",
            bargap=0.1,
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Add density line
        fig.add_trace(
            go.Scatter(
                x=dff["Tiempos Inactivos"].sort_values(),
                y=np.linspace(0, dff["Tiempos Inactivos"].count() * 0.15, len(dff)),
                mode='lines',
                name='Densidad',
                line=dict(color=COLOR_PALETTE[1], width=3)
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Tab 2: Vacantes No Cubiertas
with tab2:
    st.subheader("Vacantes No Cubiertas")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("Filtros")
        central = st.selectbox("Central", options=central_options, key="central_vacantes")
        area = st.selectbox("Área Operativa", options=area_operativa_options, key="area_vacantes")
        start_date, end_date = st.date_input("Fecha", [dates.min(), dates.max()], key="date_vacantes")
    
    with col2:
        # Filter data based on selections
        dff = df[(df['Central'] == central) & (df['Área Operativa'] == area) &
                (df['Fecha'] >= pd.to_datetime(start_date)) & (df['Fecha'] <= pd.to_datetime(end_date))]
        
        # Create bar chart
        fig = px.bar(dff.groupby('Turno')['Vacantes No Cubiertas'].mean().reset_index(), 
                     x='Turno', y='Vacantes No Cubiertas',
                     title="Promedio de Vacantes No Cubiertas por Turno",
                     color_discrete_sequence=[COLOR_PALETTE[2]],
                     template=TEMPLATE)
        
        fig.update_layout(
            xaxis_title="Turno",
            yaxis_title="Promedio de Vacantes No Cubiertas",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Tab 3: Días Inventario de Insumos
with tab3:
    st.subheader("Días Inventario de Insumos")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("Filtros")
        central = st.selectbox("Central", options=central_options, key="central_inventario")
        tipo_insumo = st.selectbox("Tipo de Insumo", options=tipo_insumo_options, key="tipo_insumo")
        proveedor = st.selectbox("Proveedor", options=proveedor_options, key="proveedor_inventario")
    
    with col2:
        # Filter data based on selections
        dff = df[(df['Central'] == central) & (df['Tipo de insumo'] == tipo_insumo) & (df['Proveedor'] == proveedor)]
        
        # Create time series chart
        dff_agg = dff.groupby('Fecha')['Días Inventario Insumos'].mean().reset_index()
        
        fig = px.line(dff_agg, x='Fecha', y='Días Inventario Insumos',
                     title="Tendencia de Días de Inventario",
                     color_discrete_sequence=[COLOR_PALETTE[3]],
                     template=TEMPLATE)
        
        fig.update_layout(
            xaxis_title="Fecha",
            yaxis_title="Días de Inventario",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Add reference line for target inventory days
        fig.add_hline(y=15, line_dash="dash", line_color="red", annotation_text="Objetivo")
        
        st.plotly_chart(fig, use_container_width=True)

# Tab 4: Incidencias por Cliente y Central
with tab4:
    st.subheader("Incidencias por Cliente y Central")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("Filtros")
        cliente = st.selectbox("Cliente", options=cliente_options, key="cliente_incidencias")
        start_date, end_date = st.date_input("Fecha", [dates.min(), dates.max()], key="date_incidencias")
    
    with col2:
        # Filter data based on selections
        dff = df[(df['Cliente'] == cliente) &
                (df['Fecha'] >= pd.to_datetime(start_date)) & (df['Fecha'] <= pd.to_datetime(end_date))]
        
        # Create heatmap
        pivot = dff.pivot_table(index='Central', columns='Área Operativa', 
                               values='Incidencias Cliente y Central', aggfunc='mean')
        
        fig = px.imshow(pivot, text_auto=True, aspect="auto",
                       title="Mapa de Calor de Incidencias por Central y Área",
                       color_continuous_scale=px.colors.sequential.Blues,
                       template=TEMPLATE)
        
        fig.update_layout(
            xaxis_title="Área Operativa",
            yaxis_title="Central",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Tab 5: Estado y Etapa de Instrumentos en IMS
with tab5:
    st.subheader("Estado y Etapa de Instrumentos en IMS")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("Filtros")
        ims = st.selectbox("IMS", options=IMS_options, key="ims_estado")
        instrumento = st.selectbox("Instrumento", options=instrumento_options, key="instrumento_estado")
    
    with col2:
        # Filter data based on selections
        dff = df[(df['IMS'] == ims) & (df['Instrumento'] == instrumento)]
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = dff['Estado y Etapa IMS'].mean(),
            title = {'text': f"Estado Promedio en {ims}"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': COLOR_PALETTE[5]},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 70], 'color': "gray"},
                    {'range': [70, 100], 'color': "darkgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(template=TEMPLATE)
        
        st.plotly_chart(fig, use_container_width=True)

# Tab 6: Capacidad de Utilización de Centrales
with tab6:
    st.subheader("Capacidad de Utilización de Centrales")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("Filtros")
        start_date, end_date = st.date_input("Fecha", [dates.min(), dates.max()], key="date_capacidad")
    
    with col2:
        # Filter data based on selections
        dff = df[(df['Fecha'] >= pd.to_datetime(start_date)) & (df['Fecha'] <= pd.to_datetime(end_date))]
        
        # Create radar chart
        dff_agg = dff.groupby('Central')['Capacidad Utilización'].mean().reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=dff_agg['Capacidad Utilización'],
            theta=dff_agg['Central'],
            fill='toself',
            name='Capacidad Utilización',
            line_color=COLOR_PALETTE[6]
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="Capacidad de Utilización por Central",
            template=TEMPLATE
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Tab 7: Tiempo de Entrega de Equipos
with tab7:
    st.subheader("Tiempo de Entrega de Equipos")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("Filtros")
        central = st.selectbox("Central", options=central_options, key="central_entrega")
        tipo_proceso = st.selectbox("Tipo de Proceso", options=tipo_proceso_options, key="proceso_entrega")
        tipo_orden = st.selectbox("Tipo de Orden", options=tipo_orden_options, key="orden_entrega")
    
    with col2:
        # Filter data based on selections
        dff = df[(df['Central'] == central) & 
                (df['Tipo de proceso'] == tipo_proceso) & 
                (df['Tipo de orden'] == tipo_orden)]
        
        # Create box plot
        fig = px.box(dff, x='Área Operativa', y='Tiempo Entrega Equipos',
                    title="Distribución de Tiempos de Entrega por Área",
                    color='Área Operativa',
                    color_discrete_sequence=COLOR_PALETTE,
                    template=TEMPLATE)
        
        fig.update_layout(
            xaxis_title="Área Operativa",
            yaxis_title="Tiempo de Entrega (días)",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Tab 8: Volumen Consumido en Monto
with tab8:
    st.subheader("Volumen Consumido en Monto")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("Filtros")
        central = st.selectbox("Central", options=central_options, key="central_volumen")
        rubro = st.selectbox("Rubro", options=rubro_options, key="rubro_volumen")
        start_date, end_date = st.date_input("Fecha", [dates.min(), dates.max()], key="date_volumen")
    
    with col2:
        # Filter data based on selections
        dff = df[(df['Central'] == central) & (df['Rubro'] == rubro) &
                (df['Fecha'] >= pd.to_datetime(start_date)) & (df['Fecha'] <= pd.to_datetime(end_date))]
        
        # Create pie chart
        dff_agg = dff.groupby('Proveedor')['Volumen Consumido Monto'].sum().reset_index()
        
        fig = px.pie(dff_agg, values='Volumen Consumido Monto', names='Proveedor',
                    title="Distribución de Volumen Consumido por Proveedor",
                    color_discrete_sequence=COLOR_PALETTE,
                    template=TEMPLATE)
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig, use_container_width=True)

# Tab 9: Porcentaje de Abastecimiento
with tab9:
    st.subheader("Porcentaje de Abastecimiento")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("Filtros")
        central = st.selectbox("Central", options=central_options, key="central_abastecimiento")
        proveedor = st.selectbox("Proveedor", options=proveedor_options, key="proveedor_abastecimiento")
        start_date, end_date = st.date_input("Fecha", [dates.min(), dates.max()], key="date_abastecimiento")
    
    with col2:
        # Filter data based on selections
        dff = df[(df['Central'] == central) & (df['Proveedor'] == proveedor) &
                (df['Fecha'] >= pd.to_datetime(start_date)) & (df['Fecha'] <= pd.to_datetime(end_date))]
        
        # Create time series with target line
        dff_agg = dff.groupby('Fecha')['Porcentaje Abastecimiento'].mean().reset_index()
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=dff_agg['Fecha'], 
                y=dff_agg['Porcentaje Abastecimiento'],
                mode='lines+markers',
                name='% Abastecimiento',
                line=dict(color=COLOR_PALETTE[9], width=3)
            )
        )
        
        # Add target line
        fig.add_trace(
            go.Scatter(
                x=dff_agg['Fecha'],
                y=[95] * len(dff_agg),
                mode='lines',
                name='Objetivo (95%)',
                line=dict(color='red', width=2, dash='dash')
            )
        )
        
        fig.update_layout(
            title="Tendencia de Porcentaje de Abastecimiento",
            xaxis_title="Fecha",
            yaxis_title="Porcentaje de Abastecimiento",
            template=TEMPLATE,
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)

