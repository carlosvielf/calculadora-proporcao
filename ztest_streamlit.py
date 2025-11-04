import streamlit as st
import math
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Calculadora Z-test para Proporção",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📊 Calculadora de Z-test para Proporção")
st.markdown("---")

# Layout em colunas
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Entrada de Dados")
    
    # Inputs
    p_hat = st.number_input(
        "Proporção Observada (p̂):",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.01,
        format="%.4f",
        help="Proporção observada na amostra (entre 0 e 1)"
    )
    
    p_0 = st.number_input(
        "Proporção Esperada (p₀):",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.01,
        format="%.4f",
        help="Proporção esperada sob a hipótese nula (entre 0 e 1)"
    )
    
    n = st.number_input(
        "Tamanho da Amostra (n):",
        min_value=1,
        value=100,
        step=1,
        help="Número de observações na amostra"
    )
    
    alpha = st.number_input(
        "Nível de Significância (α):",
        min_value=0.001,
        max_value=0.999,
        value=0.05,
        step=0.01,
        format="%.3f",
        help="Nível de significância para o teste (ex: 0.05 para 5%)"
    )
    
    test_type = st.selectbox(
        "Tipo de Teste:",
        ["Bicaudal", "Unicaudal (direita)", "Unicaudal (esquerda)"],
        help="Escolha o tipo de teste de hipótese"
    )
    
    calcular = st.button("🔢 Calcular", type="primary", use_container_width=True)

with col2:
    st.header("📈 Resultados")
    
    if calcular:
        try:
            # Validações
            if not (0 <= p_hat <= 1) or not (0 <= p_0 <= 1):
                st.error("❌ As proporções devem estar entre 0 e 1")
            elif n <= 0:
                st.error("❌ O tamanho da amostra deve ser positivo")
            elif not (0 < alpha < 1):
                st.error("❌ O nível de significância deve estar entre 0 e 1")
            else:
                # Calcular valor z
                numerador = p_hat - p_0
                denominador = math.sqrt((p_0 * (1 - p_0)) / n)
                z_value = numerador / denominador
                
                # Calcular p-valor
                if test_type == 'Bicaudal':
                    p_value = 2 * (1 - stats.norm.cdf(abs(z_value)))
                elif test_type == 'Unicaudal (direita)':
                    p_value = 1 - stats.norm.cdf(z_value)
                else:  # Unicaudal (esquerda)
                    p_value = stats.norm.cdf(z_value)
                
                # Determinar significância
                significativo = p_value < alpha
                
                # Exibir resultados em cards
                metric_col1, metric_col2 = st.columns(2)
                
                with metric_col1:
                    st.metric("Valor Z", f"{z_value}")
                    st.metric("P-valor", f"{p_value}")
                
                with metric_col2:
                    st.metric("Nível α", f"{alpha}")
                    st.metric("Tipo de Teste", test_type)
                
                # Resultado da significância
                if significativo:
                    st.success("✅ **Estatisticamente SIGNIFICATIVO**")
                    st.info(f"**Conclusão:** Rejeita-se a hipótese nula (H₀: p = {p_0})")
                else:
                    st.warning("⚠️ **NÃO estatisticamente significativo**")
                    st.info(f"**Conclusão:** Não se rejeita a hipótese nula (H₀: p = {p_0})")
                
                # Interpretação adicional
                with st.expander("📖 Interpretação dos Resultados"):
                    st.write(f"""
                    - **Valor z = {z_value}**: Medida de quantos desvios-padrão a proporção observada está da proporção esperada.
                    - **P-valor = {p_value}**: Probabilidade de observar um resultado tão extremo quanto o obtido, assumindo que H₀ é verdadeira.
                    - **Critério de decisão**: Como p-valor {'<' if significativo else '≥'} α ({alpha}), {'rejeita-se' if significativo else 'não se rejeita'} H₀.
                    """)
                
        except Exception as e:
            st.error(f"❌ Erro ao calcular: {str(e)}")

# Seção do gráfico (largura completa)
st.markdown("---")
st.header("📊 Visualização da Distribuição Normal Padrão")

if calcular:
    try:
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(12, 5))
        
        # Gerar distribuição normal padrão
        x = np.linspace(-4, 4, 1000)
        y = stats.norm.pdf(x, 0, 1)
        
        # Plotar curva normal
        ax.plot(x, y, 'b-', linewidth=2.5, label='Distribuição Normal Padrão')
        
        # Determinar região crítica
        if test_type == 'Bicaudal':
            z_crit = stats.norm.ppf(1 - alpha/2)
            # Região crítica esquerda
            x_left = x[x <= -z_crit]
            ax.fill_between(x_left, stats.norm.pdf(x_left, 0, 1), alpha=0.4, color='red', label='Região Crítica')
            # Região crítica direita
            x_right = x[x >= z_crit]
            ax.fill_between(x_right, stats.norm.pdf(x_right, 0, 1), alpha=0.4, color='red')
            ax.axvline(-z_crit, color='red', linestyle='--', linewidth=2, label=f'z crítico = ±{z_crit:.2f}')
            ax.axvline(z_crit, color='red', linestyle='--', linewidth=2)
        elif test_type == 'Unicaudal (direita)':
            z_crit = stats.norm.ppf(1 - alpha)
            x_right = x[x >= z_crit]
            ax.fill_between(x_right, stats.norm.pdf(x_right, 0, 1), alpha=0.4, color='red', label='Região Crítica')
            ax.axvline(z_crit, color='red', linestyle='--', linewidth=2, label=f'z crítico = {z_crit:.2f}')
        else:  # Unicaudal (esquerda)
            z_crit = stats.norm.ppf(alpha)
            x_left = x[x <= z_crit]
            ax.fill_between(x_left, stats.norm.pdf(x_left, 0, 1), alpha=0.4, color='red', label='Região Crítica')
            ax.axvline(z_crit, color='red', linestyle='--', linewidth=2, label=f'z crítico = {z_crit:.2f}')
        
        # Plotar valor z obtido
        ax.axvline(z_value, color='green', linestyle='-', linewidth=3, label=f'Valor z obtido = {z_value:.2f}')
        
        # Configurações do gráfico
        ax.set_xlabel('Valor z', fontsize=12, fontweight='bold')
        ax.set_ylabel('Densidade de Probabilidade', fontsize=12, fontweight='bold')
        ax.set_title('Distribuição Normal Padrão com Região Crítica', fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=11, loc='upper right')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlim(-4, 4)
        
        # Adicionar linha zero
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5, alpha=0.3)
        
        st.pyplot(fig)
        plt.close()
        
        # Legenda explicativa
        st.info("""
        **Como interpretar o gráfico:**
        - A **curva azul** representa a distribuição normal padrão.
        - A **área vermelha** indica a região crítica (região de rejeição de H₀).
        - A **linha verde** mostra o valor z calculado a partir dos seus dados.
        - Se a linha verde estiver na região vermelha, rejeita-se H₀.
        """)
        
    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {str(e)}")

# Rodapé com informações
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p><b>Fórmula do Z-test para proporção:</b></p>
    <p>z = (p̂ - p₀) / √[p₀(1-p₀)/n]</p>
    <p>Desenvolvido com Python, Streamlit e SciPy</p>
</div>
""", unsafe_allow_html=True)