import streamlit as st
import pandas as pd
import numpy as np
import textwrap
import matplotlib.pyplot as plt
import base64
import io
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Simulador de ações municipais",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CARGA DE DADOS E DEFINIÇÃO DE CAMINHOS UNIVERSAIS
pasta_raiz = os.path.dirname(__file__)


@st.cache_data
def carregar_dados():
    caminho = os.path.join(pasta_raiz, 'dados_simulador.xlsx')
    df_mun = pd.read_excel(caminho, sheet_name='Municipios')
    df_at = pd.read_excel(caminho, sheet_name='Atual')
    df_pr = pd.read_excel(caminho, sheet_name='Proposta')
    return df_mun, df_at, df_pr


def get_base64_image(nome_arquivo):
    try:
        caminho_img = os.path.join(pasta_raiz, nome_arquivo)
        with open(caminho_img, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""


# Carregamento dos dados e logos
df_mun, df_inic_atual, df_inic_prop = carregar_dados()
logo_sebrae = get_base64_image("logo_sebrae.png")
logo_pp = get_base64_image("logo_politicas_publicas.png")

# 3. INTERFACE E ESTILIZAÇÃO CSS
st.markdown(f'''
    <style>
        .stApp {{ margin-top: 70px; }}
        .full-header {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 90px;
            background-color: #0054A6;
            display: flex; align-items: center; justify-content: space-between;
            padding: 0 40px; z-index: 999999; color: white;
            border-bottom: 2px solid #0054A6;
        }}
        [data-testid="stSidebar"] {{ padding-top: 0rem !important; }}
        .header-title {{ text-align: center; flex-grow: 1; }}
        [data-testid="stTable"] th {{ background-color: #0054A6 !important;
            color: white !important;
            text-align: center !important;
        }}
        [data-testid="stTable"] tr:nth-child(even) {{ background-color: #f8f9fa; }}
        [data-testid="stTable"] tr:hover {{ background-color: #eef2f6 !important; }}
        
        .skew-btn:focus, .skew-btn:active, .skew-btn:visited {{
            outline: none !important;
            border-radius: 0px !important;
            box-shadow: none !important;
            color: white !important;
        }}
        
        /* Garante que o container do Streamlit não force bordas redondas */
        [data-testid="stMarkdownContainer"] a:focus {{
            border-radius: 0px !important;
        }}

        @media print {{
            .stApp {{ margin-top: 0; }}
            .full-header {{ position: static; height: auto; }}
            [data-testid="stSidebar"] {{ display: none !important; }}
            button, .stDownloadButton, [data-testid="stFileUploadDropzone"] {{ display: none !important; }}
        }}        
    </style>

    <div class="full-header">
        <img src="data:image/png;base64,{logo_sebrae}" height="75">
        <div class="header-title">
            <h1 style="margin:0; font-size: 2rem; color: white; line-height: 0.8;">SIMULADOR DE AÇÕES MUNICIPAIS</h1>
            <p style="margin:0; font-size: 1.2rem; font-weight: 400; margin-top: -8px;">AMBIENTE DE NEGÓCIOS</p>
        </div>
        <img src="data:image/png;base64,{logo_pp}" height="70">
    </div>
''', unsafe_allow_html=True)


def formata_reais(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


ref_atual = df_inic_atual.set_index('INICIATIVA')['VALOR'].to_dict()
pd.set_option('future.no_silent_downcasting', True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f'''
        <style>
            .portfolio-container {{
                background-color: #f0f2f6; 
                padding: 20px; 
                border-radius: 1px; 
                border: 0px solid #0054A6; 
                text-align: center;
                margin-bottom: 5px;
                position: relative;
                z-index: 10;
            }}
            .skew-btn {{
                display: inline-block;
                background-color: #0054A6;
                padding: 10px 50px;
                transform: skewX(-27deg);
                text-decoration: none !important;
                transition: background-color 0.3s;
                border: none;
                cursor: pointer;
            }}
            .skew-btn:hover {{
                background-color: #003d7a;
            }}
            .btn-text {{
                display: block;
                transform: skewX(27deg);
                color: white !important;
                font-weight: bold;
                font-size: 0.9rem;
                text-transform: uppercase;
            }}
        </style>

        <div class="portfolio-container">
            <p style="margin: 0 0 10px 0; font-size: 0.7rem; color: #555; font-weight: bold;"></p>
            <a href="https://sebraepr.sharepoint.com/:f:/s/pr_uan/IgBb_9qODkNhR4N6uGmaTzWAAZAcx99HqjJITLFLMeAZYpQ" target="_blank" class="skew-btn">
                <span class="btn-text">Acesse o portfólio</span>
            </a>
        </div>
    ''', unsafe_allow_html=True)

    st.title('Município')
    municipios = df_mun['MUN'].unique()
    options = st.selectbox('Selecione', municipios, index=None, placeholder='Selecione o município',
                           label_visibility='collapsed')

    if options:
        selec = df_mun[df_mun['MUN'] == options]
        st.markdown(f'''
            <div style='line-height: 0.7; margin-bottom: 10px;'>
                <strong>Regional:</strong> {selec['REG'].iloc[0]} <br><br>
                <strong>Território:</strong> {selec['TER'].iloc[0]}
            </div>
        ''', unsafe_allow_html=True)

        st.title('IDAN-M 2025')
        for _, linha in selec.iterrows():
            col_n, col_v = st.columns([3, 1])
            col_n.markdown(f"<div style='line-height: 1; margin-bottom: 2px;'>{linha['EIXO']}</div>",
                           unsafe_allow_html=True)
            col_v.markdown(
                f"<div style='line-height: 1; margin-bottom: 2px; text-align: right;'>{linha['PERCENTUAL']:.1%}</div>",
                unsafe_allow_html=True)

        c_tot1, c_tot2 = st.columns([3, 1])
        c_tot1.markdown(f"<div style='font-size: 1.15rem; text-align: left;'><strong>TOTAL IDAN-M</strong></div>",
                        unsafe_allow_html=True)
        c_tot2.markdown(
            f"<div style='font-size: 1.15rem; text-align: right;'><strong>{selec['IDAN-M'].iloc[0]:.2f}</strong></div>",
            unsafe_allow_html=True)

        st.markdown(
            "<br><div style='font-size: 1.2rem; font-weight: bold; margin-top: -20px;margin-bottom: 5px;'>OPORTUNIDADES</div>",
            unsafe_allow_html=True)
        eixos_zero = selec[selec['PERCENTUAL'] == 0]
        oportunidades = eixos_zero if len(eixos_zero) > 2 else selec.nsmallest(2, 'PERCENTUAL')

        for _, linha in oportunidades.iterrows():
            col_op_n, col_op_v = st.columns([3, 1])
            col_op_n.markdown(f"<div style='line-height: 1; margin-bottom: 2px;'>{linha['EIXO']}</div>",
                              unsafe_allow_html=True)
            col_op_v.markdown(
                f"<div style='line-height: 1; margin-bottom: 2px; text-align: right;'>{linha['PERCENTUAL']:.1%}</div>",
                unsafe_allow_html=True)

        st.markdown('---')

        # GRÁFICO DE RADAR
        categorias = selec['EIXO'].tolist()
        valores = selec['PERCENTUAL'].tolist()
        n = len(categorias)
        angulos = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
        valores += valores[:1];
        angulos += angulos[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        fig.patch.set_alpha(0)
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.grid(False)
        ax.spines['polar'].set_visible(False)
        ax.patch.set_visible(False)

        for nivel in [0.2, 0.4, 0.6, 0.8, 1.0]:
            ax.plot(angulos, [nivel] * len(angulos), color='gray', linestyle=':', linewidth=0.5)
        for angulo in angulos[:-1]:
            ax.plot([angulo, angulo], [0, 1], color='gray', linestyle=':', linewidth=0.5)

        ax.fill(angulos, valores, color='#0054A6', alpha=0.25)
        ax.plot(angulos, valores, color='#0054A6', linewidth=2)

        cat_quebradas = [textwrap.fill(cat, width=17) for cat in categorias]
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(cat_quebradas, fontsize=11)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=7, color='gray')
        ax.set_ylim(0, 1.1)
        st.pyplot(fig)


# --- ÁREA PRINCIPAL ---
if options:
    # 1. Inicialização do Session State
    if 'df_investido' not in st.session_state:
        st.session_state.df_investido = pd.DataFrame(columns=['INICIATIVA', 'SEBRAE/PR', 'MUNICIPIO', 'TOTAL'])
    if 'df_proposta' not in st.session_state:
        st.session_state.df_proposta = pd.DataFrame(
            columns=['INICIATIVA', 'SOLUCAO', 'SUBSIDIO', 'VALOR_MUNICIPIO', 'VALOR'])

    col_ctrl1, col_ctrl2 = st.columns([3, 1])

    # 1. Inicialização de estados adicionais
    if 'mostrar_upload' not in st.session_state:
        st.session_state.mostrar_upload = False

    # 2. BOTÕES DE CONTROLE LADO A LADO
    col_btn1, col_btn2 = st.columns([1, 1])

    with col_btn1:
        if st.button('Continuar proposta salva', use_container_width=True):
            st.session_state.mostrar_upload = not st.session_state.mostrar_upload

    with col_btn2:
        if st.button('Redefinir', use_container_width=True):
            # Em vez de DataFrame(), recriamos com a estrutura original
            st.session_state.df_investido = pd.DataFrame(columns=['INICIATIVA', 'SEBRAE/PR', 'MUNICIPIO', 'TOTAL'])
            st.session_state.df_proposta = pd.DataFrame(columns=['INICIATIVA', 'SOLUCAO', 'SUBSIDIO', 'VALOR_MUNICIPIO', 'VALOR'])
            st.session_state.mostrar_upload = False
            st.rerun()

    # 3. ÁREA DE UPLOAD CONDICIONAL
    if st.session_state.mostrar_upload:
        st.info("Selecione o arquivo .csv exportado anteriormente (nomedomunicipio_proposta_salva.csv)")
        arquivo_csv = st.file_uploader("Escolha o arquivo", type="csv", label_visibility='collapsed')

        if arquivo_csv:
            df_temp = pd.read_csv(arquivo_csv)
            if st.button("Carregar dados do arquivo", use_container_width=True):
                # Filtra e limpa colunas extras para cada tabela
                df_at_limpo = df_temp[df_temp['TIPO'] == 'ATUAL'].dropna(axis=1, how='all')
                st.session_state.df_investido = df_at_limpo.drop(columns=['TIPO'], errors='ignore').reset_index(
                    drop=True)

                df_pr_limpo = df_temp[df_temp['TIPO'] == 'PROPOSTA'].dropna(axis=1, how='all')
                st.session_state.df_proposta = df_pr_limpo.drop(columns=['TIPO'], errors='ignore').reset_index(
                    drop=True)

                st.session_state.mostrar_upload = False  # Fecha a área após carregar
                st.rerun()
    # --- 1. SEÇÃO: MONTANTE INVESTIDO ATUALMENTE ---
    st.subheader('Montante Investido Atualmente')
    with st.expander("➕ Lançar Investimento Atual", expanded=st.session_state.df_investido.empty):
        col_at_inic, col_at_val = st.columns([2, 1])
        with col_at_inic:
            inic_at_sel = st.selectbox('Iniciativa', options=sorted(list(ref_atual.keys())), index=None,
                                       placeholder='Selecione a iniciativa')
        if inic_at_sel:
            val_ref = ref_atual[inic_at_sel]
            with col_at_val:
                if val_ref == 'Digite o valor':
                    v_total_at = st.number_input('Valor Total', value=None, min_value=0.0, format='%.2f',
                                                 placeholder='Digite o valor')
                    v_sub_at = st.number_input('Valor Subsídio (Sebrae)', value=None, min_value=0.0, format='%.2f',
                                               placeholder='Digite o valor')
                else:
                    v_total_at = v_sub_at = val_ref
                    st.info(f"**Total: R\$ {formata_reais(v_total_at)}** (Subsídio 100%)")
            if st.button('Adicionar ao Investido Atualmente', use_container_width=True):
                vt, vs = (v_total_at or 0.0), (v_sub_at or 0.0)
                nova = {'INICIATIVA': inic_at_sel, 'SEBRAE/PR': vs, 'MUNICIPIO': vt - vs, 'TOTAL': vt}
                st.session_state.df_investido = pd.concat([st.session_state.df_investido, pd.DataFrame([nova])],
                                                          ignore_index=True)
                st.rerun()

    if not st.session_state.df_investido.empty:
        edicao_at = st.data_editor(st.session_state.df_investido, column_config={
            'INICIATIVA': st.column_config.TextColumn('Iniciativa', disabled=True),
            'SEBRAE/PR': st.column_config.NumberColumn('SEBRAE/PR (R$)', format='R$ %.2f'),
            'MUNICIPIO': st.column_config.NumberColumn('Município (R$)', format='R$ %.2f', disabled=True),
            'TOTAL': st.column_config.NumberColumn('Total (R$)', format='R$ %.2f')}, num_rows='dynamic',
                                   hide_index=True, width='stretch', key='grid_at')
        st.session_state.df_investido = edicao_at
        st.markdown(
            f'<div style="display: flex; justify-content: flex-end; gap: 40px; background-color: #f0f2f6; padding: 5px 10px; border-radius: 0 0 10px 10px; margin-top: -20px; margin-bottom: 20px; border: 1px solid #d1d5db;"><span>TOTAL JÁ INVESTIDO:</span><span>Sebrae: <b>R$ {formata_reais(edicao_at["SEBRAE/PR"].sum())}</b></span><span>Município: <b>R$ {formata_reais(edicao_at["MUNICIPIO"].sum())}</b></span><span>Total: <b>R$ {formata_reais(edicao_at["TOTAL"].sum())}</b></span></div>',
            unsafe_allow_html=True)

    # --- 2. SEÇÃO: PROPOSTA DE PARCERIA ---
    st.subheader('Proposta de Parceria')
    with st.expander("➕ Adicionar Item na Proposta", expanded=st.session_state.df_proposta.empty):
        col_pr_inic, col_pr_sol = st.columns(2)
        with col_pr_inic:
            nova_inic_pr = st.selectbox('Iniciativa', options=sorted(df_inic_prop['INICIATIVA'].unique().tolist()),
                                        index=None, placeholder='Selecione a iniciativa')
        if nova_inic_pr:
            sols_filtradas = df_inic_prop[df_inic_prop['INICIATIVA'] == nova_inic_pr]
            lista_sols = sols_filtradas['SOLUCAO'].unique().tolist()
            with col_pr_sol:
                nova_sol_pr = st.selectbox('Solução', options=lista_sols, placeholder='Selecione a solução',
                                           index=None if lista_sols != ['-'] else 0, disabled=lista_sols == ['-'])
            if nova_inic_pr == 'Customizado':
                v_total_pr, v_sub_pr = st.number_input('Valor Total Customizado', value=None, min_value=0.0,
                                                       format='%.2f'), 0.0
            else:
                match = sols_filtradas[sols_filtradas['SOLUCAO'] == nova_sol_pr]
                v_total_pr = match['VALOR'].iloc[0] if not match.empty else 0.0
                v_sub_pr = match['SUBSIDIO'].iloc[0] if not match.empty else 0.0
                if not match.empty: st.info(
                    f"**Total: R\$ {formata_reais(v_total_pr)}** | **Subsídio: R\$ {formata_reais(v_sub_pr)}**")
            if st.button('Adicionar à Proposta', use_container_width=True):
                vt_p, vs_p = (v_total_pr or 0.0), (v_sub_pr or 0.0)
                nova_p = {'INICIATIVA': nova_inic_pr, 'SOLUCAO': nova_sol_pr, 'SUBSIDIO': vs_p,
                          'VALOR_MUNICIPIO': vt_p - vs_p, 'VALOR': vt_p}
                st.session_state.df_proposta = pd.concat([st.session_state.df_proposta, pd.DataFrame([nova_p])],
                                                         ignore_index=True)
                st.rerun()

    if not st.session_state.df_proposta.empty:
        edicao_pr = st.data_editor(st.session_state.df_proposta, column_config={
            'INICIATIVA': st.column_config.TextColumn('Iniciativa', disabled=True),
            'SOLUCAO': st.column_config.TextColumn('Solução', disabled=True),
            'SUBSIDIO': st.column_config.NumberColumn('SEBRAE/PR (R$)', format='R$ %.2f'),
            'VALOR_MUNICIPIO': st.column_config.NumberColumn('Município (R$)', format='R$ %.2f', disabled=True),
            'VALOR': st.column_config.NumberColumn('Total (R$)', format='R$ %.2f')}, num_rows='dynamic',
                                   hide_index=True, width='stretch', key='grid_pr')
        st.session_state.df_proposta = edicao_pr
        st.markdown(
            f'<div style="display: flex; justify-content: flex-end; gap: 40px; background-color: #f0f2f6; padding: 5px 10px; border-radius: 0 0 10px 10px; margin-top: -20px; margin-bottom: 20px; border: 1px solid #d1d5db;"><span>TOTAL PROPOSTA:</span><span>Sebrae: <b>R$ {formata_reais(edicao_pr["SUBSIDIO"].sum())}</b></span><span>Município: <b>R$ {formata_reais(edicao_pr["VALOR_MUNICIPIO"].sum())}</b></span><span>Total: <b>R$ {formata_reais(edicao_pr["VALOR"].sum())}</b></span></div>',
            unsafe_allow_html=True)

    # --- RODA-PÉ: TOTALIZADORES GERAIS ---
    st.divider()
    df1_f, df2_f = st.session_state.df_investido.fillna(0), st.session_state.df_proposta.fillna(0)
    tot_g, tot_s, tot_m = df1_f['TOTAL'].sum() + df2_f['VALOR'].sum(), df1_f['SEBRAE/PR'].sum() + df2_f[
        'SUBSIDIO'].sum(), df1_f['MUNICIPIO'].sum() + df2_f['VALOR_MUNICIPIO'].sum()

    st.markdown(f'''
    <style>
        .footer-container {{ display: flex; justify-content: space-between; gap: 10px; margin-top: 20px; padding-bottom: 40px; }}
        .skew-card {{ flex: 1; height: 100px; transform: skewX(-27deg); display: flex; align-items: center; justify-content: center; box-shadow: 4px 4px 10px rgba(0,0,0,0.1); }}
        .card-content {{ transform: skewX(27deg); text-align: center; color: white; }}
        .card-title {{ font-size: 0.5rem; font-weight: bold; margin: 0; text-transform: uppercase; }}
        .card-value {{ font-size: 2rem; margin: 0; font-weight: 800; }}
        .bg-total {{ background-color: #003d7a; }}
        .bg-sebrae {{ background-color: #0054A6; }}
        .bg-municipio {{ background-color: #0054A6; }}
    </style>
    <div class="footer-container">
        <div class="skew-card bg-total"><div class="card-content"><p class="card-title">Total</p><h2 class="card-value">R$ {formata_reais(tot_g)}</h2></div></div>
        <div class="skew-card bg-sebrae"><div class="card-content"><p class="card-title">Sebrae/PR</p><h2 class="card-value">R$ {formata_reais(tot_s)}</h2></div></div>
        <div class="skew-card bg-municipio"><div class="card-content"><p class="card-title">Município</p><h2 class="card-value">R$ {formata_reais(tot_m)}</h2></div></div>
    </div>
    ''', unsafe_allow_html=True)

    # --- EXPORTAÇÃO EXCEL E CSV ---
    st.divider()
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            workbook = writer.book
            fmt_moeda = workbook.add_format({'num_format': 'R$ #,##0.00'})
            fmt_header = workbook.add_format({'bold': True, 'font_color': '#0054A6', 'font_size': 12})
            sheet_name = 'Resumo_Proposta'

            st.session_state.df_investido.to_excel(writer, sheet_name=sheet_name, startrow=2, index=False)
            row_prop = len(st.session_state.df_investido) + 5
            st.session_state.df_proposta.to_excel(writer, sheet_name=sheet_name, startrow=row_prop, index=False)

            ws = writer.sheets[sheet_name]
            ws.set_column(1, 4, 18, fmt_moeda)
            ws.write(0, 0, f"SIMULADOR DE AÇÕES MUNICIPAIS: {options}", fmt_header)
            ws.write(1, 0, "JÁ INVESTIDO NO MUNICÍPIO", fmt_header)
            ws.write(row_prop - 1, 0, "PROPOSTA DE PARCERIA", fmt_header)

            row_total = row_prop + len(st.session_state.df_proposta) + 3
            ws.write(row_total, 0, "CONSOLIDADO FINAL", fmt_header)
            ws.write(row_total + 1, 0, "Investimento Total:");
            ws.write(row_total + 1, 1, tot_g, fmt_moeda)
            ws.write(row_total + 2, 0, "Subsídio Sebrae/PR:");
            ws.write(row_total + 2, 1, tot_s, fmt_moeda)
            ws.write(row_total + 3, 0, "Aporte Município:");
            ws.write(row_total + 3, 1, tot_m, fmt_moeda)
        st.download_button("Exportar para Excel (.xlsx) 📥", data=buffer.getvalue(),
                           file_name=f"proposta_acoes_{options}.xlsx", use_container_width=True)

    with col_ex2:
        df_csv = pd.concat(
            [st.session_state.df_investido.assign(TIPO='ATUAL'), st.session_state.df_proposta.assign(TIPO='PROPOSTA')],
            ignore_index=True)
        st.download_button("Salvar proposta (.csv) 💾", data=df_csv.to_csv(index=False).encode('utf-8-sig'),
                           file_name=f"{options}_proposta_salva.csv", mime="text/csv", use_container_width=True)