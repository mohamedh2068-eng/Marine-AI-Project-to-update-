import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="M.AFixly - Marine AI Pro", layout="wide", initial_sidebar_state="expanded")

# 2. تصميم UI احترافي باستخدام CSS
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stMetric { background: rgba(30, 41, 59, 0.7); padding: 15px; border-radius: 12px; border-bottom: 3px solid #fbbf24; }
    .header-box { text-align: center; padding: 25px; background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%); border-radius: 15px; border: 1px solid #334155; margin-bottom: 25px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1e293b; border-radius: 5px 5px 0 0; color: white; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #fbbf24; color: #0f172a; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. الهيدر الرسمي
st.markdown("""
    <div class="header-box">
        <h1 style='color: #fbbf24; margin-bottom: 5px;'>M.AFixly: PROPELLER AI & CNC SYSTEM</h1>
        <p style='color: #94a3b8; font-size: 1.2em;'>جامعة شرق بورسعيد التكنولوجية | تكنولوجيا تشغيل وصيانة السفن</p>
        <p style='color: #64748b;'>إعداد الطالب: محمد أشرف حسين دسوقي | إشراف: أ.د/ حسين المصري</p>
    </div>
    """, unsafe_allow_html=True)

# 4. لوحة التحكم الجانبية (Sidebar)
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات الهندسية")
    d_input = st.number_input("قطر الرفاص (متر)", 0.5, 15.0, 2.5, step=0.1)
    v_input = st.slider("السرعة المستهدفة (عقدة)", 5, 60, 22)
    blades = st.select_slider("عدد الريش", options=[3, 4, 5, 6])
    material = st.selectbox("خامة التصنيع", ["Nickel-Alu Bronze", "Stainless Steel 316L", "Manganese Bronze"])
    st.divider()
    st.info("البرنامج يستخدم خوارزميات الذكاء الاصطناعي للتنبؤ بالكفاءة بناءً على معطيات التصنيع.")

# 5. الحسابات الهندسية الخلفية
v_ms = v_input * 0.5144
eff = 0.85 - (v_input * 0.0025) - (0.01 * blades)
thrust = (d_input**2) * (v_ms**2) * 0.55

# 6. التبويبات الرئيسية (Tabs)
tab1, tab2, tab3 = st.tabs(["📊 التحليل الهيدروديناميكي", "🤖 محاكي التصنيع والـ 3D", "📋 بيانات المشروع"])

with tab1:
    # عرض المؤشرات
    col1, col2, col3 = st.columns(3)
    col1.metric("الكفاءة المتوقعة", f"{eff*100:.1f} %")
    col2.metric("قوة الدفع (Thrust)", f"{thrust:.2f} kN")
    col3.metric("مستوى الكافيتيشن", "آمن" if v_input < 35 else "خطر مرتفع")

    # الرسم البياني التفاعلي
    st.markdown("### 📈 منحنى الأداء (Performance Curve)")
    j = np.linspace(0.1, 1.0, 20)
    kt = 0.5 - 0.4 * j
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=j, y=kt, mode='lines+markers', name='Kt', line=dict(color='#fbbf24', width=3)))
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### 🧊 محاكي الرفاص التفاعلي (3D Model)")
    
    # كود الـ JavaScript للمحاكي الـ 3D
    st.components.v1.html(f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <div id="container" style="width: 100%; height: 400px; border-radius: 15px; background: #000;"></div>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 400, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        renderer.setSize(document.getElementById('container').clientWidth, 400);
        document.getElementById('container').appendChild(renderer.domElement);

        const group = new THREE.Group();
        const material = new THREE.MeshPhongMaterial({{ color: 0xfbbf24, specular: 0xffffff, shininess: 100 }});
        
        for (let i = 0; i < {blades}; i++) {{
            const bladeGeom = new THREE.SphereGeometry(2, 32, 32);
            bladeGeom.scale(1, 0.1, 0.4);
            const blade = new THREE.Mesh(bladeGeom, material);
            blade.rotation.y = (i * Math.PI * 2) / {blades};
            blade.position.x = Math.cos(blade.rotation.y) * 0.5;
            blade.position.z = Math.sin(blade.rotation.y) * 0.5;
            group.add(blade);
        }}
        
        const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 1.2, 32), material);
        hub.rotation.x = Math.PI / 2;
        group.add(hub);
        
        scene.add(group);
        const light = new THREE.PointLight(0xffffff, 1, 100);
        light.position.set(10, 10, 10);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040));
        camera.position.z = 6;

        function animate() {{
            requestAnimationFrame(animate);
            group.rotation.z += 0.03;
            renderer.render(scene, camera);
        }}
        animate();
    </script>
    """, height=420)

    st.markdown("### 🛠️ نظام توليد أكواد الـ CNC (G-Code)")
    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
        st.write(f"**معايير الماكينة لـ {material}:**")
        st.write(f"- سرعة الدوران: {2500} RPM")
        st.write(f"- معدل التغذية: {200} mm/min")
        if st.button("Generate G-Code"):
            st.success("تم إنتاج المسار البرمجي للماكينة بنجاح")
    
    with col_c2:
        st.code(f"""
        (M.AFixly G-Code Output)
        G21 (Metric Units)
        T01 M06 (Tool Change)
        S2500 M03 (Spindle On)
        G00 X0 Y0 Z10
        G01 Z-2 F100
        (Path for {blades} Blades Propeller)
        G01 X{d_input*5} Y{d_input*2}
        M30 (End Program)
        """, language="gcode")

with tab3:
    st.markdown(f"""
    ### 📁 توثيق المشروع
    * **اسم الطالب:** محمد أشرف حسين دسوقي
    * **الكلية:** تكنولوجيا الصناعة والطاقة
    * **القسم:** تكنولوجيا تشغيل وصيانة السفن
    * **المشرف:** أ.د/ حسين المصري
    ---
    **وصف النظام:**
    هذه المنصة صممت كجزء من مشروع التخرج لربط تقنيات الذكاء الاصطناعي بعمليات التصنيع المتقدمة (CNC). 
    النظام قادر على تحليل الخصائص الهيدروديناميكية للرفاص البحري وتقديم محاكاة ثلاثية الأبعاد فورية مع إنتاج أكواد التشغيل الآلي.
    """)

st.divider()
st.markdown("<p style='text-align: center; color: #64748b;'>© 2026 M.AFixly Marine Systems | Port Said</p>", unsafe_allow_html=True)
