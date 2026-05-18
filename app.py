import streamlit as st
import pandas as pd
import os
from PIL import Image
from datetime import datetime

# --- 1. ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="ระบบลงทะเบียนและวินัยจราจร - วก.ชัยภูมิ", page_icon="🛵", layout="centered")

# --- 2. การจัดการไฟล์ข้อมูล ---
DATA_FILE = "regist_data_chaiyaphum.xlsx"  
INCIDENT_FILE = "incident_data_chaiyaphum.xlsx" # ไฟล์เก็บประวัติทำผิดกฎ
IMG_FOLDER = "images_student_moto"
INCIDENT_IMG_FOLDER = "images_incidents" # โฟลเดอร์เก็บรูปทำผิดกฎ

for folder in [IMG_FOLDER, INCIDENT_IMG_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# ฟังก์ชันโหลดข้อมูลทะเบียนรถ
def load_data():
    if os.path.exists(DATA_FILE):
        try: return pd.read_excel(DATA_FILE)
        except: return pd.DataFrame()
    else:
        return pd.DataFrame(columns=[
            "Timestamp", "Sticker_No", "Student_ID", "Name", "Level", "Department", "Phone",
            "Parent_Name", "Relation", "Parent_Phone", "Brand", "Model", "Plate_No", "Color",
            "Student_Img", "Moto_Img", "Agreement"
        ])

# ฟังก์ชันโหลดข้อมูลการทำผิดกฎ
def load_incident_data():
    if os.path.exists(INCIDENT_FILE):
        try: return pd.read_excel(INCIDENT_FILE)
        except: return pd.DataFrame()
    else:
        return pd.DataFrame(columns=["Timestamp", "Sticker_No", "Violation_Type", "Details", "Img_Sticker", "Img_Overview"])

# ฟังก์ชันบันทึกข้อมูลทะเบียน
def save_data(data_dict):
    df = load_data()
    new_df = pd.DataFrame([data_dict])
    pd.concat([df, new_df], ignore_index=True).to_excel(DATA_FILE, index=False)

# ฟังก์ชันบันทึกข้อมูลผิดกฎ
def save_incident(data_dict):
    df = load_incident_data()
    new_df = pd.DataFrame([data_dict])
    pd.concat([df, new_df], ignore_index=True).to_excel(INCIDENT_FILE, index=False)

# ฟังก์ชันไฮไลต์สีแดงสำหรับคนที่ทำผิดตั้งแต่ 3 ครั้งขึ้นไป
def highlight_violations(val):
    color = '#ffcccc' if val >= 3 else ''
    return f'background-color: {color}; font-weight: bold;'

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
                path1 = f"{IMG_FOLDER}/{std_id}_STD_{ts_str}.{img_student.name.split('.')[-1]}"
                with open(path1, "wb") as f: f.write(img_student.getbuffer())
                path2 = f"{IMG_FOLDER}/{std_id}_MOTO_{ts_str}.{img_moto.name.split('.')[-1]}"
                with open(path2, "wb") as f: f.write(img_moto.getbuffer())

                data = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Sticker_No": "รออนุมัติ", 
                    "Student_ID": std_id, "Name": std_name, "Level": level, "Department": dept, "Phone": std_phone,
                    "Parent_Name": parent_name, "Relation": relation, "Parent_Phone": parent_phone,
                    "Brand": brand, "Model": model, "Plate_No": plate_no, "Color": color,
                    "Student_Img": path1, "Moto_Img": path2, "Agreement": "ยอมรับแล้ว"
                }
                save_data(data)
                st.success("🎉 บันทึกข้อมูลสำเร็จ! กรุณาติดต่อห้องปกครองเพื่อรับสติ๊กเกอร์")
                st.balloons()
            else:
                st.error("กรุณากรอกข้อมูลให้ครบถ้วน")

# ==========================================
# TAB 2: สำหรับงานปกครอง (Admin)
# ==========================================
with tab2:
    st.header("👮 ระบบจัดการข้อมูลงานปกครอง")
    pwd = st.text_input("รหัสผ่านเจ้าหน้าที่", type="password")
    
    if pwd == "admin1234": 
        df = load_data()
        df_inc = load_incident_data()
        
        st.metric("จำนวนรถที่ลงทะเบียนทั้งหมด", f"{len(df)} คัน")
        
        # --- ตารางที่ 1: ตารางทะเบียนรถทั้งหมด ---
        st.subheader("📋 ตารางข้อมูลการลงทะเบียนสติ๊กเกอร์รถ")
        search = st.text_input("🔍 ค้นหาในตาราง (ชื่อ, ทะเบียน, รหัสสติ๊กเกอร์)")
        if search:
            mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
            display_df = df[mask]
        else: display_df = df
        st.dataframe(display_df)

        # --- ตารางที่ 2: สรุปคนผิดกฎ + ไฮไลต์สีแดง (ใหม่ล่าสุด!) ---
        st.markdown("---")
        st.subheader("📊 ตารางสรุปรายชื่อผู้กระทำผิดกฎระเบียบจราจร")
        if df_inc.empty:
            st.info("ยังไม่มีประวัติการทำผิดกฎระเบียบในระบบ")
        else:
            # คำนวณจำนวนครั้งที่ผิดสะสมของแต่ละสติ๊กเกอร์
            violation_counts = df_inc["Sticker_No"].value_counts().reset_index()
            violation_counts.columns = ["Sticker_No", "จำนวนครั้งที่ทำผิดสะสม"]
            
            # นำไปเชื่อมกับตารางข้อมูลนักเรียนเพื่อเอาชื่อ-ระดับชั้นมาโชว์
            df_for_merge = df[["Sticker_No", "Name", "Level", "Department", "Plate_No"]].drop_duplicates()
            summary_violation_df = pd.merge(violation_counts, df_for_merge, on="Sticker_No", how="left")
            
            # จัดเรียงคอลัมน์ให้อ่านง่าย
            summary_violation_df = summary_violation_df[["Sticker_No", "Name", "Level", "Department", "Plate_No", "จำนวนครั้งที่ทำผิดสะสม"]]
            
            st.caption("💡 แถบสีแดงไฮไลต์ = ผู้ทำผิดกฎสะสมวิกฤตตั้งแต่ 3 ครั้งขึ้นไป (ต้องเรียกพบตัดแต้มความประพฤติ)")
            # แสดงตารางพร้อมใส่ Logic ไฮไลต์สีแดง
            st.dataframe(summary_violation_df.style.map(highlight_violations, subset=["จำนวนครั้งที่ทำผิดสะสม"]))

        # --- ส่วนงานอนุมัติออกเลขสติ๊กเกอร์ ---
        if not df.empty:
            st.markdown("---")
            st.subheader("🛠️ ระบบตรวจอนุมัติและออกหมายเลขสติ๊กเกอร์")
            student_list = df.apply(lambda row: f"{row['Student_ID']} - {row['Name']} ({row['Sticker_No']})", axis=1).tolist()
            selected_student = st.selectbox("เลือกนักเรียนที่ต้องการตรวจสอบเพื่ออกหมายเลข", student_list)
            selected_id = selected_student.split(" - ")[0]
            student_row = df[df["Student_ID"].astype(str) == selected_id].iloc[0]
            student_index = df[df["Student_ID"].astype(str) == selected_id].index[0]
            
            st.write(f"**ระดับชั้น:** {student_row['Level']} | **แผนกวิชา:** {student_row['Department']}")
            col_show1, col_show2 = st.columns(2)
            with col_show1:
                if os.path.exists(str(student_row['Student_Img'])): st.image(student_row['Student_Img'], caption="รูปนักเรียน", use_container_width=True)
            with col_show2:
                if os.path.exists(str(student_row['Moto_Img'])): st.image(student_row['Moto_Img'], caption="รูปรถ", use_container_width=True)
            
            current_sticker = student_row['Sticker_No']
            new_sticker_no = st.text_input("ระบุหมายเลขสติ๊กเกอร์ที่ออกให้", value="" if current_sticker == "รออนุมัติ" else current_sticker)
            if st.button("💾 บันทึกการอนุมัติ / อัปเดตข้อมูล"):
                if new_sticker_no.strip() == "": st.error("กรุณากรอกหมายเลขสติ๊กเกอร์")
                else:
                    df.at[student_index, 'Sticker_No'] = new_sticker_no.strip()
                    df.to_excel(DATA_FILE, index=False)
                    st.success(f"อัปเดตหมายเลขสติ๊กเกอร์สำเร็จ!")
                    st.rerun()
        st.markdown("---")
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "rb") as f: st.download_button("📥 ดาวน์โหลดไฟล์ Excel ทะเบียนรถทั้งหมด", f, file_name="Motorcycle_Data_Chaiyaphum.xlsx")
        if os.path.exists(INCIDENT_FILE):
            with open(INCIDENT_FILE, "rb") as f: st.download_button("📥 ดาวน์โหลดไฟล์ Excel ประวัติทำผิดกฎทั้งหมด", f, file_name="Violation_Data.xlsx")
    elif pwd: st.error("รหัสผ่านไม่ถูกต้อง")

# ==========================================
# TAB 3: ระบบรายงานทำผิดกฎและเด้งแจ้งเตือนบนเว็บ
# ==========================================
with tab3:
    st.header("🚨 ศูนย์รายงานการทำผิดกฎระเบียบจราจร")
    st.info("สำหรับคณะครูและงานปกครองใช้ถ่ายรูปรายงานเมื่อพบรถทำผิดกฎ")
    
    df_reg = load_data()
    if df_reg.empty:
        st.warning("⚠️ ยังไม่มีข้อมูลสติ๊กเกอร์ในระบบ ทันทีที่มีการออกสติ๊กเกอร์ ระบบรายงานผลจะเปิดให้ใช้งานครับ")
    else:
        valid_stickers = df_reg[df_reg["Sticker_No"] != "รออนุมัติ"]["Sticker_No"].astype(str).unique().tolist()
        
        if not valid_stickers:
            st.warning("⚠️ ยังไม่มีหมายเลขสติ๊กเกอร์ที่ผ่านการอนุมัติในระบบ (ครูต้องไปกดอนุมัติออกเลขสติ๊กเกอร์ใน TAB 2 ก่อนครับ)")
        else:
            with st.form("incident_form", clear_on_submit=True):
                target_sticker = st.selectbox("🎯 เลือกหมายเลขสติ๊กเกอร์ที่ทำผิดกฎ", valid_stickers)
                violation_type = st.selectbox("⚠️ ข้อหาความผิด", [
                    "จอดรถในพื้นที่ห้ามจอด / จอดไม่เป็นระเบียบ",
                    "ไม่สวมหมวกนิรภัยเข้ามาในวิทยาลัย",
                    "ขับรถเร็วเกินกำหนด / ขับขี่น่าหวาดเสียว",
                    "ดัดแปลงสภาพรถ / ท่อไอเสียเสียงดังเกินเกณฑ์",
                    "อื่นๆ (โปรดระบุในช่องคำอธิบาย)"
                ])
                details = st.text_area("📝 คำอธิบายเพิ่มเติม (เช่น สถานที่เกิดเหตุ, พฤติกรรม)")
                
                col_up1, col_up2 = st.columns(2)
                img_stick = col_up1.file_uploader("📸 1. รูปถ่ายให้เห็นเลขสติ๊กเกอร์ชัดเจน", type=["jpg", "png", "jpeg"])
                img_over = col_up2.file_uploader("📸 2. รูปถ่ายพื้นที่โดยรวม / สภาพแวดล้อม", type=["jpg", "png", "jpeg"])
                
                btn_report = st.form_submit_button("🚨 ส่งรายงานพฤติกรรม")
                
                if btn_report:
                    if img_stick and img_over:
                        ts_now = datetime.now()
                        ts_str = ts_now.strftime("%Y%m%d_%H%M%S")
                        
                        # เซฟรูปเก็บลงเครื่องคอมพิวเตอร์และเซิร์ฟเวอร์
                        p_stick = f"{INCIDENT_IMG_FOLDER}/{target_sticker}_STICKER_{ts_str}.{img_stick.name.split('.')[-1]}"
                        with open(p_stick, "wb") as f: f.write(img_stick.getbuffer())
                        p_over = f"{INCIDENT_IMG_FOLDER}/{target_sticker}_OVERVIEW_{ts_str}.{img_over.name.split('.')[-1]}"
                        with open(p_over, "wb") as f: f.write(img_over.getbuffer())
                        
                        # บันทึกลงตารางผิดกฎ
                        incident_dict = {
                            "Timestamp": ts_now.strftime("%Y-%m-%d %H:%M:%S"),
                            "Sticker_No": target_sticker, "Violation_Type": violation_type,
                            "Details": details, "Img_Sticker": p_stick, "Img_Overview": p_over
                        }
                        save_incident(incident_dict)
                        
                        # ดึงข้อมูลนักเรียนเจ้าของรถมาแสดงผลแมตช์ชื่อเสียงเรียงนาม
                        stud_info = df_reg[df_reg["Sticker_No"].astype(str) == str(target_sticker)].iloc[0]
                        
                        # คำนวณนับยอดรวมความผิดสะสม
                        df_inc = load_incident_data()
                        count_violation = len(df_inc[df_inc["Sticker_No"].astype(str) == str(target_sticker)])
                        
                        st.subheader("📊 ผลการบันทึกข้อมูล")
                        st.write(f"**ชื่อผู้ทำผิด:** {stud_info['Name']} ({stud_info['Level']})")
                        st.write(f"**ทำผิดข้อหา:** {violation_type}")
                        
                        # 🚨 เงื่อนไขการโชว์ป๊อปอัปแจ้งเตือนด่วนบนหน้าเว็บแบบสดๆ (Real-time)
                        if count_violation >= 3:
                            st.error(f"""
                            ### 🚨 🚨 แจ้งเตือนด่วนที่สุด! (ทำผิดสะสมครบเงื่อนไข)
                            - **สติ๊กเกอร์หมายเลข:** {target_sticker} 
                            - **นักศึกษา:** {stud_info['Name']} ชั้น {stud_info['Level']}
                            - **พฤติกรรมล่าสุด:** {violation_type}
                            - **📊 ประวัติทำผิดกฎระเบียบสะสมรวม:** {count_violation} ครั้ง !!
                            
                            **⚠️ ข้อปฏิบัติ:** ระบบทำการบันทึกข้อมูลพฤติกรรมนี้เข้าตารางบัญชีดำ (Blacklist) เรียบร้อยแล้ว ครูที่ปรึกษาหรือฝ่ายปกครองโปรดเรียกตัวพบเพื่อดำเนินการทางวินัยและหักแต้มตามระเบียบวิทยาลัยฯ ทันที!
                            """)
                        else:
                            st.success(f"🎉 บันทึกประวัติพฤติกรรมสำเร็จ! (ทำผิดสะสมครั้งที่ {count_violation}) ข้อมูลถูกส่งเข้าสู่ระบบงานปกครองแล้ว")
                        st.balloons()
                    else:
                        st.error("กรุณาอัปโหลดรูปภาพให้ครบทั้ง 2 รูป (รูปสติ๊กเกอร์ และรูปพื้นที่โดยรวม)")