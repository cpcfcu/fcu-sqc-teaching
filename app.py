import streamlit as st
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# 頁面配置
st.set_page_config(
    page_title="品質管制與工程教學平台 (FCU IESM)",
    page_icon="📊",
    layout="wide"
)

# 自訂 CSS 樣式，打造簡潔現代的介面風格
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 側邊欄導覽
st.sidebar.title("🎓 課程導覽與模組")
st.sidebar.markdown("---")
app_mode = st.sidebar.selectbox("選擇學習/模擬模組", [
    "1. 基礎敘述統計與常態分佈",
    "2. 計量值管制圖 (Xbar-R Chart)",
    "3. 製程能力分析 (Cp / Cpk)",
    "4. 計數值管制圖 (p Chart)"
])

st.sidebar.markdown("---")
st.sidebar.info("📌 **逢甲大學 工業工程與系統管理學系**\n\n授課教師：鍾健平 教授\n參考書目：Montgomery, *Statistical Quality Control*")

# ==========================================
# 模組 1：基礎敘述統計與常態分佈
# ==========================================
if app_mode == "1. 基礎敘述統計與常態分佈":
    st.markdown('<p class="main-header">📊 模組一：基礎敘述統計與常態分佈 (第 3 章)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">模擬與分析製程數據的中心趨勢、變異數、以及常態機率分佈特性。</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### ⚙️ 參數設定")
        sample_size = st.slider("樣本數 (n)", 30, 500, 100, 10)
        true_mean = st.number_input("母體平均數 (μ)", value=50.0, step=1.0)
        true_std = st.number_input("母體標準差 (σ)", value=2.0, min_value=0.1, step=0.1)
        
        # 產生模擬數據
        np.random.seed(42)
        data = np.random.normal(true_mean, true_std, sample_size)
        
        st.markdown("---")
        st.markdown("### 📈 統計量摘要")
        st.write(f"• **樣本平均數 ($\\bar{x}$):** {np.mean(data):.3f}")
        st.write(f"• **樣本標準差 ($s$):** {np.std(data, ddof=1):.3f}")
        st.write(f"• **中位數 (Median):** {np.median(data):.3f}")
        st.write(f"• **四分位距 (IQR):** {stats.iqr(data):.3f}")

    with col2:
        st.markdown("### 📉 數據直方圖與常態配適")
        fig, ax = plt.subplots(figsize=(8, 5))
        count, bins, ignored = ax.hist(data, bins=15, density=True, alpha=0.6, color='#3B82F6', edgecolor='black')
        
        # 繪製理論常態曲線
        xmin, xmax = ax.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, np.mean(data), np.std(data, ddof=1))
        ax.plot(x, p, 'r-', linewidth=2, label='Fitted Normal PDF')
        
        ax.set_title("Process Data Histogram & Normal Fit", fontsize=12, fontweight='bold')
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        ax.legend()
        st.pyplot(fig)

# ==========================================
# 模組 2：計量值管制圖 (Xbar-R Chart)
# ==========================================
elif app_mode == "2. 計量值管制圖 (Xbar-R Chart)":
    st.markdown('<p class="main-header">📈 模組二：計量值管制圖 ($\bar{X}-R$ Chart) (第 5-6 章)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">監控製程水準與變異是否處於統計管制狀態 (Statistical Control)。</p>', unsafe_allow_html=True)

    num_subgroups = st.slider("組數 (m)", 15, 50, 25, 5)
    n_size = st.slider("每組樣本大小 (n)", 2, 10, 5, 1)

    # 產生模擬組別數據 (假設第 12 組刻意給予異常偏移以展示失控)
    np.random.seed(100)
    subgroups = []
    for i in range(num_subgroups):
        if i == 11:
            sg = np.random.normal(52.5, 1.2, n_size)
        else:
            sg = np.random.normal(50.0, 1.0, n_size)
        subgroups.append(sg)

    subgroups = np.array(subgroups)
    x_bars = np.mean(subgroups, axis=1)
    ranges = np.ptp(subgroups, axis=1)

    grand_x_bar = np.mean(x_bars)
    average_range = np.mean(ranges)

    # 查表係數 (A2, D3, D4)
    constants_A2 = {2: 1.880, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483, 7: 0.419, 8: 0.373, 9: 0.337, 10: 0.308}
    constants_D3 = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.076, 8: 0.136, 9: 0.184, 10: 0.223}
    constants_D4 = {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924, 8: 1.864, 9: 1.816, 10: 1.777}

    A2 = constants_A2.get(n_size, 0.577)
    D3 = constants_D3.get(n_size, 0)
    D4 = constants_D4.get(n_size, 2.114)

    x_ucl = grand_x_bar + A2 * average_range
    x_lcl = grand_x_bar - A2 * average_range
    r_ucl = D4 * average_range
    r_lcl = D3 * average_range

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Xbar Chart
    ax1.plot(range(1, num_subgroups + 1), x_bars, marker='o', color='#2563EB', linestyle='-', label='Xbar')
    ax1.axhline(grand_x_bar, color='green', linestyle='-', label=f'CL = {grand_x_bar:.2f}')
    ax1.axhline(x_ucl, color='red', linestyle='--', label=f'UCL = {x_ucl:.2f}')
    ax1.axhline(x_lcl, color='red', linestyle='--', label=f'LCL = {x_lcl:.2f}')
    
    out_of_control_x = [i+1 for i, val in enumerate(x_bars) if val > x_ucl or val < x_lcl]
    if out_of_control_x:
        ax1.plot(out_of_control_x, [x_bars[i-1] for i in out_of_control_x], marker='s', color='red', markersize=8, linestyle='None', label='Out of Control')

    ax1.set_title(f"$\\bar{X}$ Control Chart (n={n_size})", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Subgroup Mean")
    ax1.legend(loc='upper right')
    ax1.grid(True, linestyle=':', alpha=0.6)

    # R Chart
    ax2.plot(range(1, num_subgroups + 1), ranges, marker='o', color='#D97706', linestyle='-', label='Range')
    ax2.axhline(average_range, color='green', linestyle='-', label=f'CL = {average_range:.2f}')
    ax2.axhline(r_ucl, color='red', linestyle='--', label=f'UCL = {r_ucl:.2f}')
    ax2.axhline(r_lcl, color='red', linestyle='--', label=f'LCL = {r_lcl:.2f}')
    
    ax2.set_title("R Control Chart", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Subgroup Number")
    ax2.set_ylabel("Subgroup Range")
    ax2.legend(loc='upper right')
    ax2.grid(True, linestyle=':', alpha=0.6)

    st.pyplot(fig)
    
    if out_of_control_x:
        st.warning(f"⚠️ 偵測到失控點！群組編號 {out_of_control_x} 超出 3-sigma 管制界線，請進行特殊原因分析。")
    else:
        st.success("✅ 製程目前處於統計管制狀態 (In Control)。")

# ==========================================
# 模組 3：製程能力分析 (Cp / Cpk)
# ==========================================
elif app_mode == "3. 製程能力分析 (Cp / Cpk)":
    st.markdown('<p class="main-header">🎯 模組三：製程能力分析 (Process Capability Analysis) (第 8 章)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">評估製程變異相對於規格界線 (USL / LSL) 的符合程度。</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### ⚙️ 規格與製程參數")
        usl = st.number_input("上規格限 (USL)", value=55.0)
        lsl = st.number_input("下規格限 (LSL)", value=45.0)
        process_mean = st.number_input("製程平均數 (μ)", value=50.0)
        process_std = st.number_input("製程標準差 (σ)", value=1.5, min_value=0.1)

        cp = (usl - lsl) / (6 * process_std)
        cpu = (usl - process_mean) / (3 * process_std)
        cpl = (process_mean - lsl) / (3 * process_std)
        cpk = min(cpu, cpl)

        st.markdown("---")
        st.markdown("### 📊 製程能力指數結果")
        st.write(f"• **$C_p$ (潛在製程能力):** {cp:.3f}")
        st.write(f"• **$C_{{pk}}$ (實際製程能力):** {cpk:.3f}")
        
        if cpk >= 1.33:
            st.success("✨ 製程能力優秀 ($C_{pk} \\ge 1.33$)，符合六標準協定要求。")
        elif cpk >= 1.00:
            st.warning("⚠️ 製程能力勉強合格 ($1.00 \\le C_{pk} < 1.33$)，需注意偏移。")
        else:
            st.error("❌ 製程能力不足 ($C_{pk} < 1.00$)，不良率偏高。")

    with col2:
        st.markdown("### 📉 製程常態分佈與規格圖")
        fig, ax = plt.subplots(figsize=(8, 5))
        
        x_min = min(lsl - 3*process_std, process_mean - 4*process_std)
        x_max = max(usl + 3*process_std, process_mean + 4*process_std)
        x = np.linspace(x_min, x_max, 200)
        y = stats.norm.pdf(x, process_mean, process_std)
        
        ax.plot(x, y, 'b-', linewidth=2, label='Process Distribution')
        ax.axvline(usl, color='red', linestyle='--', linewidth=2, label=f'USL ({usl})')
        ax.axvline(lsl, color='red', linestyle='--', linewidth=2, label=f'LSL ({lsl})')
        ax.axvline(process_mean, color='green', linestyle='-', linewidth=2, label=f'Mean ({process_mean})')
        
        x_fill_left = np.linspace(x_min, lsl, 100)
        ax.fill_between(x_fill_left, stats.norm.pdf(x_fill_left, process_mean, process_std), color='red', alpha=0.3)
        
        x_fill_right = np.linspace(usl, x_max, 100)
        ax.fill_between(x_fill_right, stats.norm.pdf(x_fill_right, process_mean, process_std), color='red', alpha=0.3)

        ax.set_title("Process Capability vs Specifications", fontsize=12, fontweight='bold')
        ax.set_xlabel("Characteristic Value")
        ax.set_ylabel("Density")
        ax.legend(loc='upper right')
        ax.grid(True, linestyle=':', alpha=0.6)
        
        st.pyplot(fig)

# ==========================================
# 模組 4：計數值管制圖 (p Chart)
# ==========================================
elif app_mode == "4. 計數值管制圖 (p Chart)":
    st.markdown('<p class="main-header">📋 模組四：計數值管制圖 ($p$ Chart) (第 7 章)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">適用於不良率 (Fraction Nonconforming) 的製程監控與品質改善。</p>', unsafe_allow_html=True)

    num_lots = st.slider("抽樣批數 (k)", 10, 40, 20, 5)
    sample_n = st.number_input("每批樣本大小 (n)", value=100, min_value=20, step=10)
    avg_p = st.slider("平均不良率 (p̄)", 0.01, 0.15, 0.05, 0.01)

    np.random.seed(42)
    defect_counts = np.random.binomial(sample_n, avg_p, num_lots)
    p_hats = defect_counts / sample_n

    p_bar = np.mean(p_hats)
    p_ucl = p_bar + 3 * np.sqrt((p_bar * (1 - p_bar)) / sample_n)
    p_lcl = max(0, p_bar - 3 * np.sqrt((p_bar * (1 - p_bar)) / sample_n))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(range(1, num_lots + 1), p_hats, marker='o', color='#8B5CF6', linestyle='-', label='Sample Proportion (p̂)')
    ax.axhline(p_bar, color='green', linestyle='-', label=f'CL = {p_bar:.3f}')
    ax.axhline(p_ucl, color='red', linestyle='--', label=f'UCL = {p_ucl:.3f}')
    ax.axhline(p_lcl, color='red', linestyle='--', label=f'LCL = {p_lcl:.3f}')

    ax.set_title(f"$p$ Control Chart for Fraction Nonconforming (n={sample_n})", fontsize=12, fontweight='bold')
    ax.set_xlabel("Lot / Sample Number")
    ax.set_ylabel("Fraction Defective")
    ax.legend(loc='upper right')
    ax.grid(True, linestyle=':', alpha=0.6)

    st.pyplot(fig)
    st.info("💡 **提示**：$p$ 管制圖適用於評估服務業錯誤率、行政單據瑕疵、或製造業批量不良率的波動情況。")

# 頁尾
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2026 Feng Chia University | Department of Industrial Engineering and Systems Management</p>", unsafe_allow_html=True)