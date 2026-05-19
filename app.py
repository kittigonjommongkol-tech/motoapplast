import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="ระบบลงทะเบียนและวินัยจราจร - วก.ชัยภูมิ", page_icon="🛵", layout="centered")

# --- 2. ตั้งชื่อไฟล์ Excel สำหรับบันทึกข้อมูลถาวรภายในแอป ---
REGISTRATION_FILE = "Database_Registration_Chaiyaphum.xlsx"
INCIDENT_FILE     = "Database_Incident_Chaiyaphum.xlsx"

# โครงสร้างตารางมาตรฐานกรณีที่ยังไม่มีการกรอกข้อมูลใดๆ
REG_COLUMNS = [
    "Timestamp", "Sticker_No", "Student_ID", "Name", "Level", "Department", "Phone",
    "Parent_Name", "Relation", "Parent_Phone", "Brand", "Model", "Plate_No", "Color",
    "Student_Img", "Moto_Img", "Agreement"
]
INC_COLUMNS = ["Timestamp", "Sticker_No", "Violation_Type", "Details", "Reporter_Name", "Img_Sticker", "Img_Overview"]

def load_data():
    """ฟังก์ชันโหลดข้อมูลจากไฟล์ Excel บนตัวแอป"""
    if os.path.exists(REGISTRATION_FILE):
        try:
            return pd.read_excel(REGISTRATION_FILE)
        except:
            return pd.DataFrame(columns=REG_COLUMNS)
    else:
        return pd.DataFrame(columns=REG_COLUMNS)

def load_incident_data():
    """ฟังก์ชันโหลดข้อมูลแจ้งเหตุจากไฟล์ Excel บนตัวแอป"""
    if os.path.exists(INCIDENT_FILE):
        try:
            return pd.read_excel(INCIDENT_FILE)
        except:
            return pd.DataFrame(columns=INC_COLUMNS)
    else:
        return pd.DataFrame(columns=INC_COLUMNS)

def save_data(data_dict):
    """ฟังก์ชันบันทึกข้อมูลลงไฟล์ Excel และอัปเดตระบบจำลอง"""
    df = load_data()
    new_df = pd.DataFrame([data_dict])
    updated_df = pd.concat([df, new_df], ignore_index=True)
    
    # สั่งเซฟลงไฟล์ Excel ในตัวแอปถาวร
    updated_df.to_excel(REGISTRATION_FILE, index=False)
    # ล้างแรมหน้าเว็บให้จำค่าใหม่ทันที
    st.session_state["cached_df"] = updated_df

def save_incident(data_dict):
    """ฟังก์ชันบันทึกข้อมูลแจ้งเหตุลงไฟล์ Excel และอัปเดตระบบจำลอง"""
    df = load_incident_data()
    new_df = pd.DataFrame([data_dict])
    updated_df = pd.concat([df, new_df], ignore_index=True)
    
    # สั่งเซฟลงไฟล์ Excel ในตัวแอปถาวร
    updated_df.to_excel(INCIDENT_FILE, index=False)
    # ล้างแรมหน้าเว็บให้จำค่าใหม่ทันที
    st.session_state["cached_incident_df"] = updated_df

def highlight_violations(val):
    color = '#ffcccc' if val >= 3 else ''
    return f'background-color: {color}; font-weight: bold;'

# สร้างโฟลเดอร์สำหรับเก็บภาพภายในแอป
for folder in ["images_student_moto", "images_incidents"]:
    if not os.path.exists(folder): 
        os.makedirs(folder)

# --- 3. ส่วนแสดงผลหลัก ---
st.image("https://www.vec.go.th/Portals/0/logo_vec.png", width=100) 
st.title("วิทยาลัยเกษตรและเทคโนโลยีชัยภูมิ")
st.subheader("🛵 ระบบบริหารจัดการรถจักรยานยนต์และวินัยจราจร")

tab1, tab2, tab3 = st.tabs(["📝 สำหรับนักเรียน/บุคลากร", "👮 สำหรับงานปกครอง", "🚨 รายงานผิดกฎระเบียบ"])

# ==========================================
# TAB 1: แบบฟอร์มลงทะเบียน (ฝั่งนักเรียน)
# ==========================================
with tab1:
    with st.form("registration_form", clear_on_submit=True):
        st.info("ส่วนที่ 1: ข้อมูลนักเรียน (เจ้าของรถ)")
        c1, c2 = st.columns(2)
        std_name = c1.text_input("ชื่อ - นามสกุล")
        std_id = c2.text_input("รหัสประจำตัวนักเรียน")
        
        c3, c4 = st.columns(2)
        level = c3.selectbox("ระดับชั้น", ["ปวช.1", "ปวช.2", "ปวช.3", "ปวส.1", "ปวส.2", "ปริญญาตรี"])
        dept = c4.text_input("แผนกวิชา") 
        std_phone = st.text_input("เบอร์โทรศัพท์ที่ติดต่อได้")

        st.info("ส่วนที่ 2: ข้อมูลผู้ปกครอง")
        c5, c6 = st.columns(2)
        parent_name = c5.text_input("ชื่อ - นามสกุล ผู้ปกครอง")
        relation = c6.text_input("ความเกี่ยวข้อง (เช่น บิดา/มารดา)")
        parent_phone = st.text_input("เบอร์โทรศัพท์ผู้ปกครอง (กรณีฉุกเฉิน)")

        st.info("ส่วนที่ 3: ข้อมูลรถจักรยานยนต์")
        c7, c8 = st.columns(2)
        brand = c7.selectbox("ยี่ห้อ", ["Honda", "Yamaha", "Suzuki", "Kawasaki", "Vespa", "GPX", "อื่นๆ"])
        model = c8.text_input("รุ่น (เช่น Wave 110i)")
        c9, c10 = st.columns(2)
        plate_no = c9.text_input("เลขทะเบียน (ถ้ามี)")
        color = c10.text_input("สีรถ")

        st.info("ส่วนที่ 4: อัปโหลดรูปภาพ")
        col_img1, col_img2 = st.columns(2)
        img_student = col_img1.file_uploader("1. รูปถ่ายนักเรียน (หน้าตรง)", type=["jpg", "png", "jpeg"])
        img_moto = col_img2.file_uploader("2. รูปถ่ายรถจักรยานยนต์ (เห็นป้าย/สภาพรถ)", type=["jpg", "png", "jpeg"])

        st.warning("ส่วนที่ 5: ข้อตกลงและรับทราบกฎระเบียบ")
        st.markdown("1. ✅ **สวมหมวกนิรภัย** ทุกครั้ง | 2. ✅ **จอดรถ** ในบริเวณที่กำหนด | 3. ✅ **มีใบขับขี่**")
        agreement = st.checkbox("ข้าพเจ้าขอรับรองว่าข้อมูลเป็นความจริง และยินยอมปฏิบัติตามกฎระเบียบทุกประการ")

        submitted = st.form_submit_button("✅ ส่งข้อมูลลงทะเบียน")
        if submitted:
            if std_name and std_id and parent_phone and brand and img_student and img_moto and agreement:
                ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                path1 = f"images_student_moto/{std_id}_STD_{ts_str}.{img_student.name.split('.')[-1]}"
                with open(path1, "wb") as f: f.write(img_student.getbuffer())
                path2 = f"images_student_moto/{std_id}_MOTO_{ts_str}.{img_moto.name.split('.')[-1]}"
                with open(path2, "wb") as f: f.write(img_moto.getbuffer())

                data = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Sticker_No": "รออนุมัติ", 
                    "Student_ID": std_id, "Name": std_name, "Level": level, "Department": dept, "Phone": std_phone,
                    "Parent_Name": parent_name, "Relation": relation, "Parent_Phone": parent_phone,
                    "Brand": brand, "Model": model, "Plate_No": plate_no, "Color": color,
                    "Student_Img": path1, "Moto_Img": path2, "Agreement": "ยอมรับแล้ว"
                }
                save_data(data)
                st.success("🎉 บันทึกข้อมูลลงฐานข้อมูลในระบบสำเร็จถาวรแล้ว!")
                st.balloons()
            else:
                st.error("กรุณากรอกข้อมูลและอัปโหลดรูปภาพให้ครบถ้วน")

# ==========================================
# TAB 2: สำหรับงานปกครอง (Admin)
# ==========================================
with tab2:
    st.header("👮 ระบบจัดการข้อมูลงานปกครอง")
    pwd = st.text_input("รหัสผ่านเจ้าหน้าที่", type="password")
    
    if pwd == "admin1234": 
        if "cached_df" in st.session_state:
            df = st.session_state["cached_df"]
        else:
            df = load_data()

        if "cached_incident_df" in st.session_state:
            df_inc = st.session_state["cached_incident_df"]
        else:
            df_inc = load_incident_data()
        
        st.metric("จำนวนรถที่ลงทะเบียนทั้งหมด (Realtime)", f"{len(df)} คัน")
        
        st.subheader("📋 ตารางข้อมูลการลงทะเบียนสติ๊กเกอร์รถ")
        search = st.text_input("🔍 ค้นหาในตาราง (ชื่อ, ทะเบียน, รหัสสติ๊กเกอร์)")
        if not df.empty:
            if search:
                mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
                display_df = df[mask]
            else: 
                display_df = df
            st.dataframe(display_df)
            
            # 📥 ปุ่มดาวน์โหลดไฟล์ข้อมูลลงทะเบียนแบบ Excel
            try:
                with open(REGISTRATION_FILE, "rb") as file:
                    st.download_button(
                        label="📥 ดาวน์โหลดไฟล์ข้อมูลลงทะเบียนทั้งหมด (Excel)",
                        data=file,
                        file_name=f"ข้อมูลลงทะเบียนรถ_วก_ชัยภูมิ_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="btn_download_reg"
                    )
            except:
                pass
        else:
            st.info("ยังไม่มีข้อมูลนักเรียนลงทะเบียนในระบบ")

        st.markdown("---")
        st.subheader("📊 ตารางสรุปรายชื่อผู้กระทำผิดกฎระเบียบจราจร")
        if df_inc.empty:
            st.info("ยังไม่มีประวัติการทำผิดกฎระเบียบในระบบ")
        else:
            violation_counts = df_inc["Sticker_No"].value_counts().reset_index()
            violation_counts.columns = ["Sticker_No", "จำนวนครั้งที่ทำผิดสะสม"]
            
            df_for_merge = df[["Sticker_No", "Name", "Level", "Department", "Plate_No"]].drop_duplicates()
            summary_violation_df = pd.merge(violation_counts, df_for_merge, on="Sticker_No", how="left")
            summary_violation_df = summary_violation_df[["Sticker_No", "Name", "Level", "Department", "Plate_No", "จำนวนครั้งที่ทำผิดสะสม"]]
            
            st.caption("💡 แถบสีแดงไฮไลต์ = ผู้ทำผิดกฎสะสมวิกฤตตั้งแต่ 3 ครั้งขึ้นไป")
            st.dataframe(summary_violation_df.style.map(highlight_violations, subset=["จำนวนครั้งที่ทำผิดสะสม"]))

            st.subheader("📜 ประ