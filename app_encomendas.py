import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials

NOME_PLANILHA = "Encomendas Salgados"
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
st.set_page_config(
    page_title="Salgados Oliveira",
    page_icon="🥟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
:root {
    --primary: #FF6B35;
    --secondary: #F7931E;
}
.main {
    background: linear-gradient(135deg, #FFF5F0 0%, #FFE8D6 100%);
}
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border-left: 4px solid var(--primary);
    margin-bottom: 15px;
}
.stButton>button {
    border-radius: 10px;
    border: none;
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    color: white;
    font-weight: 600;
    padding: 12px 24px;
    transition: all 0.3s;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(255,107,53,0.3);
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: white;
    padding: 10px;
    border-radius: 15px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    color: white;
}
h1 {
    color: #2E2E2E;
    font-weight: 700;
}
.login-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 40px;
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)


LOGO_PATH = "logo.png"

SALGADOS = [
    'Coxinha', 'Pastel de frango', 'Pastel doce', 'Pastel de queijo',
    'Pastel misto', 'Pastel de carne', 'Canudos de frango',
    'Canudos de carne', 'Canudos de frango c/ azeitona e maionese',
    'Tortelete de frango', 'Tortelete doce', 'Empada',
    'Salgadinho de queijo assado', 'Salgadinho de queijo frito',
    'Bolinha empanada de azeitona e queijo', 'Bolinha empanada de queijo',
    'Bolinha empanada de charque', 'Mini pizzas', 'Pastel mercado'
]

FORMAS_PAGAMENTO = ['A vista', 'Cartão de crédito', 'Cartão de débito', 'Pix', 'Fiado']

def salvar_dados(df):
    planilha = conectar_planilha()
    planilha.clear()
    planilha.update([df.columns.values.tolist()] + df.values.tolist())

def atualizar_status_automatico(df):
    if df.empty:
        return df
    agora = datetime.now()
    alterou = False
    for idx, row in df.iterrows():
        if row['Status'] not in ['Entregue', 'Cancelada']:
            try:
                data_str = f"{row['Data_Entrega']} {row['Hora_Entrega']}"
                data_entrega = datetime.strptime(data_str, '%d/%m/%Y %H:%M')
                if agora > data_entrega:
                    df.loc[idx, 'Status'] = 'Entregue'
                    alterou = True
            except:
                pass
    if alterou:
        salvar_dados(df)
    return df

@st.cache_resource
def conectar_planilha():
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], SCOPE)
    client = gspread.authorize(creds)
    planilha = client.open(NOME_PLANILHA).sheet1
    return planilha
@st.cache_resource
def carregar_dados():
    planilha = conectar_planilha()
    dados = planilha.get_all_records()
    df = pd.DataFrame(dados)
    if df.empty:
        colunas = ['Data_Pedido', 'Cliente', 'Telefone', 'Produto', 'Quantidade',
                   'Valor', 'Data_Entrega', 'Hora_Entrega', 'Status', 'Observacoes', 'Forma_Pagamento']
        return pd.DataFrame(columns=colunas)
    df = atualizar_status_automatico(df)
    return df
   

def card_metrica(titulo, valor, icone, cor):
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {cor};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <p style="color: #888; font-size: 14px; margin: 0;">{titulo}</p>
                <h2 style="color: #2E2E2E; margin: 5px 0 0 0;">{valor}</h2>
            </div>
            <div style="font-size: 40px;">{icone}</div>
        </div>
    """, unsafe_allow_html=True)

def gerar_html_impressao(df, titulo="Relatório de Encomendas"):
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo} - Salgados Oliveira</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; color: #333; }}
        h1 {{ color: #FF6B35; text-align: center; margin-bottom: 5px; }}
        h2 {{ text-align: center; color: #333; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 11px; }}
        th {{ background-color: #FF6B35; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
     .info {{ text-align: center; margin-bottom: 20px; color: #666; }}
     .rodape {{ text-align: center; margin-top: 30px; font-size: 10px; color: #999; }}
        @media print {{.no-print {{ display: none; }} }}
    </style>
</head>
<body>
    <h1>🥟 Salgados Oliveira</h1>
    <h2>{titulo}</h2>
    <p class="info">Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    <button class="no-print" onclick="window.print()" style="background:#FF6B35;color:white;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;margin-bottom:15px;">🖨️ Imprimir Esta Página</button>
    <table>
        <thead>
            <tr>
"""
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            html += f"<td>{val}</td>"
        html += "</tr>"

    html += """
            </tbody>
        </table>
        <p class="rodape">Sistema de Gestão de Encomendas - Salgados Oliveira</p>
    </body>
    </html>"""
    return html

def calcular_salgados_pendentes(df):
    salgados_pendentes = {}
    df_pendentes = df[df['Status'].isin(['Pendente', 'Em produção', 'Pronto'])]
    for _, row in df_pendentes.iterrows():
        produtos = row['Produto'].split(', ')
        for produto in produtos:
            try:
                partes = produto.split('x ', 1)
                if len(partes) == 2:
                    qtd = int(partes[0])
                    nome = partes[1].strip()
                    salgados_pendentes[nome] = salgados_pendentes.get(nome, 0) + qtd
            except:
                continue
    return salgados_pendentes

def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=150)
        st.markdown('<h1 style="text-align: center; color: #FF6B35;">🥟 Salgados Oliveira</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #888;">Sistema de Gestão de Encomendas</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("login_form"):
            usuario = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
            entrar = st.form_submit_button("Entrar", use_container_width=True)
            if entrar:
                if usuario == "admin" and senha == "admin123":
                    st.session_state['logado'] = True
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos!")
        st.markdown('</div>', unsafe_allow_html=True)

def app_principal():
    if 'produtos' not in st.session_state:
        st.session_state.produtos = []
    if 'editando' not in st.session_state:
        st.session_state.editando = None

    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=80)
    with col2:
        st.markdown('<h1 style="text-align: center; margin: 0;">🥟 Salgados Oliveira</h1>', unsafe_allow_html=True)
    with col3:
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state['logado'] = False
            st.session_state.editando = None
            st.rerun()
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📊 Dashboard", "➕ Nova", "📋 Ver", "✏️ Editar", "✅ Atualizar Status", "🗑️ Excluir", "📊 Relatório", "📦 Salgados Pendentes", "⚙️ Configurações"
    ])

    with tab1:
        df = carregar_dados()
        if df.empty:
            st.info("📭 Nenhuma encomenda cadastrada ainda. Vá em 'Nova' para começar.")
        else:
            df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)
            df['Data_Entrega_dt'] = pd.to_datetime(df['Data_Entrega'], format='%d/%m/%Y', errors='coerce')
            hoje = date.today()
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            fat_hoje = df[(df['Data_Entrega_dt'].dt.date == hoje) & (~df['Status'].isin(['Entregue', 'Cancelada']))]['Valor'].sum()
            fat_semana = df[(df['Data_Entrega_dt'].dt.date >= inicio_semana) & (~df['Status'].isin(['Entregue', 'Cancelada']))]['Valor'].sum()
            fat_total = df[df['Status'] == 'Entregue']['Valor'].sum()
            pedidos_pendentes = len(df[df['Status'].isin(['Pendente', 'Em produção', 'Pronto'])])

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                card_metrica("Hoje", f"R$ {fat_hoje:.2f}", "💰", "#FF6B35")
            with col2:
                card_metrica("Semana", f"R$ {fat_semana:.2f}", "📈", "#F7931E")
            with col3:
                card_metrica("Entregue", f"R$ {fat_total:.2f}", "✅", "#00C851")
            with col4:
                card_metrica("Pendentes", str(pedidos_pendentes), "⏰", "#ff4444")

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns([2,1])
            with col1:
                st.subheader("📊 Faturamento por Data")
                df_grafico = df[(~df['Status'].isin(['Entregue', 'Cancelada']))].copy()
                df_grafico = df_grafico[df_grafico['Data_Entrega'].notna()]
                if not df_grafico.empty:
                    df_chart = df_grafico.groupby('Data_Entrega')['Valor'].sum().reset_index()
                    st.bar_chart(df_chart.set_index('Data_Entrega'))
                else:
                    st.info("Sem dados para exibir ainda.")
            with col2:
                st.subheader("🔔 Próximas Entregas")
                proximas = df[df['Status'].isin(['Pendente', 'Em produção', 'Pronto'])].sort_values('Data_Entrega_dt').head(5)
                if not proximas.empty:
                    for _, row in proximas.iterrows():
                        st.markdown(f"""
                        <div style='background: white; padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 3px solid #FF6B35;'>
                            <strong>{row['Cliente']}</strong><br>
                            <span style='color: #888; font-size: 13px;'>📅 {row['Data_Entrega']} às {row['Hora_Entrega']}</span><br>
                            <span style='color: #FF6B35; font-weight: 600;'>R$ {float(row['Valor']):.2f}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Nenhuma entrega pendente.")

    with tab2:
        st.subheader("➕ Cadastrar Nova Encomenda")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Dados do Cliente**")
            cliente = st.text_input("Nome*", placeholder="Nome completo", key="nome")
            telefone = st.text_input("WhatsApp", placeholder="(87) 99999-9999", key="tel")
        with col2:
            st.markdown("**Detalhes do Pedido**")
            valor = st.number_input("Valor Total R$*", min_value=0.0, step=0.50, format="%.2f", key="val")
            data_entrega = st.date_input("Data de Entrega*", value=date.today(), key="data")
            hora_entrega = st.time_input("Hora de Entrega*", key="hora")

        forma_pagamento = st.selectbox("💳 Forma de Pagamento*", FORMAS_PAGAMENTO, key="forma_pag")

        st.markdown("---")
        st.markdown("**Produtos* (selecione os salgados e a quantidade)**")
        col1, col2, col3 = st.columns([3,2,2])
        with col1:
            salgado_escolhido = st.selectbox("Tipo de salgado", SALGADOS, key="salgado")
        with col2:
            quantidade = st.number_input("Quantidade", min_value=1, step=1, key="qtd")
        with col3:
            st.write("")
            if st.button("➕ Adicionar", use_container_width=True):
                st.session_state.produtos.append({"produto": salgado_escolhido, "quantidade": quantidade})
                st.rerun()

        if st.session_state.produtos:
            st.markdown("**Produtos adicionados:**")
            total_qtd = 0
            for i, p in enumerate(st.session_state.produtos):
                col1, col2 = st.columns([4,1])
                col1.write(f"• {p['quantidade']}x {p['produto']}")
                if col2.button("🗑️", key=f"rem_{i}"):
                    st.session_state.produtos.pop(i)
                    st.rerun()
                total_qtd += p['quantidade']
            st.info(f"Total: {total_qtd} salgados")
        else:
            st.warning("⚠️ Adicione pelo menos 1 produto")

        observacoes = st.text_area("📝 Observações", placeholder="Alguma observação especial?", key="obs")

        if st.button("💾 Salvar Encomenda", use_container_width=True, type="primary"):
            if cliente and st.session_state.produtos and valor > 0:
                df = carregar_dados()
                produtos_texto = ", ".join([f"{p['quantidade']}x {p['produto']}" for p in st.session_state.produtos])
                nova_linha = pd.DataFrame([{
                    'Data_Pedido': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'Cliente': cliente,
                    'Telefone': telefone,
                    'Produto': produtos_texto,
                    'Quantidade': sum([p['quantidade'] for p in st.session_state.produtos]),
                    'Valor': valor,
                    'Data_Entrega': data_entrega.strftime('%d/%m/%Y'),
                    'Hora_Entrega': hora_entrega.strftime('%H:%M'),
                    'Status': 'Pendente',
                    'Observacoes': observacoes,
                    'Forma_Pagamento': forma_pagamento
                }])
                df = pd.concat([df, nova_linha], ignore_index=True)
                salvar_dados(df)
                st.success(f"✅ Encomenda de {cliente} salva com sucesso!")
                st.session_state.produtos = []
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Preencha nome, valor e adicione pelo menos 1 produto")

    with tab3:
        st.subheader("📋 Todas as Encomendas")
        df = carregar_dados()
        if df.empty:
            st.info("📭 Nenhuma encomenda cadastrada ainda.")
        else:
            df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)
            filtro_status = st.multiselect(
                "Filtrar por Status",
                options=['Pendente', 'Em produção', 'Pronto', 'Entregue', 'Cancelada'],
                default=['Pendente', 'Em produção', 'Pronto']
            )
            df_filtrado = df[df['Status'].isin(filtro_status)]
            st.dataframe(df_filtrado, use_container_width=True, hide_index=True, height=400)

            col1, col2 = st.columns(2)
            with col1:
                if not df_filtrado.empty:
                    html_content = gerar_html_impressao(df_filtrado, "Lista de Encomendas")
                    st.download_button(
                        label="🖨️ Baixar Página para Impressão",
                        data=html_content,
                        file_name=f"impressao_encomendas_{date.today()}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                else:
                    st.info("Nada para imprimir.")
            with col2:
                csv = df_filtrado.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                st.markdown(f'<a href="data:file/csv;base64,{b64}" download="encomendas_filtradas.csv">📥 Baixar CSV</a>', unsafe_allow_html=True)

    with tab4:
        st.subheader("✏️ Editar Encomenda")
        df = carregar_dados()
        if df.empty:
            st.info("📭 Nenhuma encomenda para editar.")
        else:
            df['Opcao'] = df.index.astype(str) + " - " + df['Cliente'] + " - " + df['Produto'] + " - " + df['Data_Entrega']
            if st.session_state.editando is None:
                encomenda_selecionada = st.selectbox("Selecione a encomenda para editar", df['Opcao'])
                index = int(encomenda_selecionada.split(" - ")[0])
                if st.button("✏️ Editar Esta Encomenda", use_container_width=True):
                    st.session_state.editando = index
                    st.rerun()
            else:
                index = st.session_state.editando
                row = df.loc[index]
                with st.form("editar_form"):
                    cliente = st.text_input("Cliente", value=row['Cliente'])
                    telefone = st.text_input("Telefone", value=row.get('Telefone', ''))
                    produto = st.text_area("Produto", value=row['Produto'], height=100)
                    quantidade = st.number_input("Quantidade", value=int(row['Quantidade']), min_value=1)
                    valor = st.number_input("Valor", value=float(row['Valor']), min_value=0.0, format="%.2f")
                    data_entrega = st.date_input("Data Entrega", value=datetime.strptime(row['Data_Entrega'], '%d/%m/%Y'))
                    hora_entrega = st.time_input("Hora Entrega", value=datetime.strptime(row['Hora_Entrega'], '%H:%M'))
                    status = st.selectbox("Status", ['Pendente', 'Em produção', 'Pronto', 'Entregue', 'Cancelada'],
                                          index=['Pendente', 'Em produção', 'Pronto', 'Entregue', 'Cancelada'].index(row['Status']))
                    forma_pagamento = st.selectbox("Forma de Pagamento", FORMAS_PAGAMENTO,
                                                   index=FORMAS_PAGAMENTO.index(row.get('Forma_Pagamento', 'A vista')) if row.get('Forma_Pagamento', 'A vista') in FORMAS_PAGAMENTO else 0)
                    observacoes = st.text_area("Observações", value=row.get('Observacoes', ''))

                    col1, col2 = st.columns(2)
                    with col1:
                        salvar = st.form_submit_button("💾 Salvar Alterações", use_container_width=True, type="primary")
                    with col2:
                        cancelar = st.form_submit_button("❌ Cancelar Edição", use_container_width=True)

                    if salvar:
                        df.loc[index, 'Cliente'] = cliente
                        df.loc[index, 'Telefone'] = telefone
                        df.loc[index, 'Produto'] = produto
                        df.loc[index, 'Quantidade'] = quantidade
                        df.loc[index, 'Valor'] = valor
                        df.loc[index, 'Data_Entrega'] = data_entrega.strftime('%d/%m/%Y')
                        df.loc[index, 'Hora_Entrega'] = hora_entrega.strftime('%H:%M')
                        df.loc[index, 'Status'] = status
                        df.loc[index, 'Forma_Pagamento'] = forma_pagamento
                        df.loc[index, 'Observacoes'] = observacoes
                        salvar_dados(df)
                        st.success("✅ Encomenda atualizada com sucesso!")
                        st.session_state.editando = None
                        st.rerun()
                    if cancelar:
                        st.session_state.editando = None
                        st.rerun()

    with tab5:
        st.subheader("✅ Atualizar Status da Encomenda")
        df = carregar_dados()
        df_ativas = df[df['Status'].isin(['Pendente', 'Em produção', 'Pronto'])]
        if df_ativas.empty:
            st.info("📭 Nenhuma encomenda ativa para atualizar.")
        else:
            df_ativas['Opcao'] = df_ativas.index.astype(str) + " - " + df_ativas['Cliente'] + " - " + df_ativas['Data_Entrega'] + " - R$" + df_ativas['Valor'].astype(str)
            encomenda_selecionada = st.selectbox("Selecione a encomenda", df_ativas['Opcao'])
            index = int(encomenda_selecionada.split(" - ")[0])

            col1, col2, col3 = st.columns(3)
            col1.metric("Cliente", df.loc[index, 'Cliente'])
            col2.metric("Valor", f"R$ {float(df.loc[index, 'Valor']):.2f}")
            col3.metric("Status Atual", df.loc[index, 'Status'])

            st.markdown(f"**Produtos:** {df.loc[index, 'Produto']}")
            st.markdown(f"**Entrega:** {df.loc[index, 'Data_Entrega']} às {df.loc[index, 'Hora_Entrega']}")
            st.markdown(f"**Pagamento:** {df.loc[index, 'Forma_Pagamento']}")

            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Marcar como ENTREGUE", use_container_width=True, type="primary"):
                    df.loc[index, 'Status'] = 'Entregue'
                    salvar_dados(df)
                    st.success("✅ Status atualizado para Entregue!")
                    st.rerun()
            with col2:
                if st.button("❌ Marcar como CANCELADA", use_container_width=True):
                    df.loc[index, 'Status'] = 'Cancelada'
                    salvar_dados(df)
                    st.success("❌ Encomenda cancelada!")
                    st.rerun()

    with tab6:
        st.subheader("🗑️ Excluir Encomenda")
        st.warning("⚠️ Atenção: Esta ação não pode ser desfeita!")
        df = carregar_dados()
        if df.empty:
            st.info("📭 Nenhuma encomenda para excluir.")
        else:
            df['Opcao'] = df.index.astype(str) + " - " + df['Cliente'] + " - " + df['Produto'] + " - " + df['Data_Entrega']
            encomenda_selecionada = st.selectbox("Selecione a encomenda para excluir", df['Opcao'])
            index = int(encomenda_selecionada.split(" - ")[0])
            st.markdown("---")
            col1, col2 = st.columns(2)
            col1.write(f"**Cliente:** {df.loc[index, 'Cliente']}")
            col1.write(f"**Produto:** {df.loc[index, 'Produto']}")
            col2.write(f"**Valor:** R$ {float(df.loc[index, 'Valor']):.2f}")
            col2.write(f"**Data:** {df.loc[index, 'Data_Entrega']}")
            st.markdown("---")
            confirmar = st.checkbox("Sim, tenho certeza que quero excluir esta encomenda")
            if st.button("🗑️ Excluir Definitivamente", use_container_width=True, disabled=not confirmar):
                nome_cliente = df.loc[index, 'Cliente']
                df = df.drop(index).reset_index(drop=True)
                salvar_dados(df)
                st.success(f"Encomenda de {nome_cliente} excluída!")
                st.rerun()

    with tab7:
        st.subheader("📊 Relatório de Encomendas")
        df = carregar_dados()
        if df.empty:
            st.info("📭 Nenhuma encomenda cadastrada ainda.")
        else:
            df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)
            st.markdown("**Selecione o período do relatório:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                data_inicio = st.date_input("Data Início", value=date.today() - timedelta(days=30), key="data_inicio_rel")
            with col2:
                data_fim = st.date_input("Data Fim", value=date.today(), key="data_fim_rel")
            with col3:
                status_filtro = st.multiselect("Status", ['Pendente', 'Em produção', 'Pronto', 'Entregue', 'Cancelada'], default=['Entregue'], key="status_rel")

            df['Data_Entrega_dt'] = pd.to_datetime(df['Data_Entrega'], format='%d/%m/%Y', errors='coerce')
            df_relatorio = df[
                (df['Data_Entrega_dt'].dt.date >= data_inicio) &
                (df['Data_Entrega_dt'].dt.date <= data_fim) &
                (df['Status'].isin(status_filtro))
            ]

            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Encomendas", len(df_relatorio))
            col2.metric("Valor Total", f"R$ {df_relatorio['Valor'].sum():.2f}")
            col3.metric("Média por Pedido", f"R$ {df_relatorio['Valor'].mean():.2f}" if len(df_relatorio) > 0 else "R$ 0.00")

            st.dataframe(df_relatorio[['Cliente', 'Produto', 'Quantidade', 'Valor', 'Data_Entrega', 'Status', 'Forma_Pagamento']], use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("📄 Gerar Impressão")
            st.info(f"Relatório filtrado de {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}")

            col1, col2 = st.columns(2)
            with col1:
                if not df_relatorio.empty:
                    html_content = gerar_html_impressao(df_relatorio, f"Relatório {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")
                    st.download_button(
                        label="🖨️ Baixar Página para Impressão (.html)",
                        data=html_content,
                        file_name=f"relatorio_{data_inicio}_{data_fim}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                    st.caption("Clique, abra o arquivo baixado e aperte Ctrl+P para imprimir")
                else:
                    st.info("Nada para imprimir no período selecionado.")
            with col2:
                csv = df_relatorio.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                st.markdown(f'<a href="data:file/csv;base64,{b64}" download="relatorio_{data_inicio}_{data_fim}.csv">📥 Baixar CSV</a>', unsafe_allow_html=True)

    with tab8:
        st.subheader("📦 Relatório de Salgados Pendentes")
        df = carregar_dados()
        if df.empty:
            st.info("📭 Nenhuma encomenda cadastrada ainda.")
        else:
            salgados_pendentes = calcular_salgados_pendentes(df)
            if not salgados_pendentes:
                st.info("📭 Nenhum salgado pendente para fazer.")
            else:
                st.markdown("### **Total de salgados que ainda precisam ser feitos:**")

                col1, col2 = st.columns([2, 1])
                with col1:
                    df_salgados = pd.DataFrame(list(salgados_pendentes.items()), columns=['Salgado', 'Quantidade Total'])
                    df_salgados = df_salgados.sort_values('Quantidade Total', ascending=False)
                    st.dataframe(df_salgados, use_container_width=True, hide_index=True)

                with col2:
                    total_geral = sum(salgados_pendentes.values())
                    st.metric("**Total Geral**", f"{total_geral} unidades")

                st.markdown("---")
                st.subheader("📋 Encomendas Pendentes Detalhadas")
                df_pendentes = df[df['Status'].isin(['Pendente', 'Em produção', 'Pronto'])]
                st.dataframe(df_pendentes[['Cliente', 'Produto', 'Quantidade', 'Data_Entrega', 'Status']], use_container_width=True, hide_index=True)

                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    html_salgados = gerar_html_impressao(df_salgados, "Totais de Salgados Pendentes para Produção")
                    st.download_button(
                        label="🖨️ Imprimir Totais de Salgados",
                        data=html_salgados,
                        file_name=f"totais_salgados_pendentes_{date.today()}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                with col2:
                    html_lista = gerar_html_impressao(df_pendentes[['Cliente', 'Produto', 'Quantidade', 'Data_Entrega', 'Status']], "Lista de Encomendas Pendentes")
                    st.download_button(
                        label="🖨️ Imprimir Lista de Produção",
                        data=html_lista,
                        file_name=f"lista_producao_{date.today()}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                with col3:
                    csv = df_pendentes.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    st.markdown(f'<a href="data:file/csv;base64,{b64}" download="salgados_pendentes.csv">📥 Baixar CSV</a>', unsafe_allow_html=True)

    with tab9:
        st.subheader("⚙️ Configurações do Sistema")

        st.markdown("**1. Logomarca**")
        col1, col2 = st.columns([1,2])
        with col1:
            if os.path.exists(LOGO_PATH):
                st.image(LOGO_PATH, width=150, caption="Logo atual")
        with col2:
            logo_file = st.file_uploader("Faça upload da nova logomarca", type=['png', 'jpg', 'jpeg'])
            if logo_file:
                with open(LOGO_PATH, "wb") as f:
                    f.write(logo_file.read())
                st.success("Logomarca atualizada! Recarregue a página.")
                st.rerun()

        st.markdown("---")
        st.markdown("**2. Backup de Dados**")
        df = carregar_dados()
        if not df.empty:
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            st.markdown(f'<a href="data:file/csv;base64,{b64}" download="backup_encomendas_{date.today()}.csv">📥 Baixar Backup Completo</a>', unsafe_allow_html=True)
        else:
            st.info("Nenhum dado para backup ainda.")

        st.markdown("---")
        st.markdown("**3. Informações**")
        st.info("Sistema Salgados Oliveira v3.2 - Botões separados + Impressão Salgados Pendentes")

if 'logado' not in st.session_state:
    st.session_state['logado'] = False
if st.session_state['logado']:
    app_principal()
else:
    login()
# Migração para Google Sheets concluída
