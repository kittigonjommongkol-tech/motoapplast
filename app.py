import streamlit as st
import pandas as pd
import os
from PIL import Image
from datetime import datetime

# --- 1. ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="ระบบลงทะเบียนรถ - วก.ชัยภูมิ", page_icon="🛵", layout="centered")

# --- 2. การจัดการไฟล์ข้อมูล ---
DATA_FILE = "regist_data_chaiyaphum.xlsx"  
IMG_FOLDER = "images_student_moto"

if not os.path.exists(IMG_FOLDER):
    os.makedirs(IMG_FOLDER)

# ฟังก์ชันโหลดข้อมูล
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_excel(DATA_FILE)
        except:
            return pd.DataFrame()
    else:
        return pd.DataFrame(columns=[
            "Timestamp", "Sticker_No", "Student_ID", "Name", "Level", "Department", "Phone",
            "Parent_Name", "Relation", "Parent_Phone",
            "Brand", "Model", "Plate_No", "Color",
            "Student_Img", "Moto_Img", "Agreement"
        ])

# ฟังก์ชันบันทึกข้อมูลใหม่
def save_data(data_dict):
    df = load_data()
    new_df = pd.DataFrame([data_dict])
    combined_df = pd.concat([df, new_df], ignore_index=True)
    combined_df.to_excel(DATA_FILE, index=False)

# --- 3. ส่วนแสดงผลหลัก ---
st.image("https://www.vec.go.th/Portals/0/logo_vec.png", width=100) 
st.title("วิทยาลัยเกษตรและเทคโนโลยีชัยภูมิ")
st.subheader("🛵 แบบฟอร์มลงทะเบียนรถจักรยานยนต์")

tab1, tab2 = st.tabs(["📝 สำหรับนักเรียน/บุคลากร", "👮 สำหรับงานปกครอง"])

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
        st.caption("กรุณาถ่ายรูปให้ชัดเจน")
        col_img1, col_img2 = st.columns(2)
        img_student = col_img1.file_uploader("1. รูปถ่ายนักเรียน (หน้าตรง)", type=["jpg", "png", "jpeg"])
        img_moto = col_img2.file_uploader("2. รูปถ่ายรถจักรยานยนต์ (เห็นป้าย/สภาพรถ)", type=["jpg", "png", "jpeg"])

        st.warning("ส่วนที่ 5: ข้อตกลงและรับทราบกฎระเบียบ")
        st.markdown("""
        **ข้าพเจ้าและผู้ปกครอง รับทราบและจะปฏิบัติตามกฎระเบียบที่วิทยาลัยกำหนด ดังนี้:**
        1. ✅ **สวมหมวกนิรภัย** ทุกครั้งที่ขับขี่มาโรงเรียน
        2. ✅ **จอดรถ** ในบริเวณที่วิทยาลัยกำหนดเท่านั้น
        3. ✅ **มีใบขับขี่** และเอกสารรถถูกต้องตามกฎหมาย
        """)
        
        agreement = st.checkbox("ข้าพเจ้าขอรับรองว่าข้อมูลเป็นความจริง และยินยอมปฏิบัติตามกฎระเบียบทุกประการ")

        submitted = st.form_submit_button("✅ ส่งข้อมูลลงทะเบียน")

        if submitted:
            if std_name and std_id and parent_phone and brand and img_student and img_moto and agreement:
                ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # บันทึกรูปนักเรียน
                ext1 = img_student.name.split('.')[-1]
                path1 = f"{IMG_FOLDER}/{std_id}_STD_{ts_str}.{ext1}"
                with open(path1, "wb") as f:
                    f.write(img_student.getbuffer())
                
                # บันทึกรูปรถ
                ext2 = img_moto.name.split('.')[-1]
                path2 = f"{IMG_FOLDER}/{std_id}_MOTO_{ts_str}.{ext2}"
                with open(path2, "wb") as f:
                    f.write(img_moto.getbuffer())

                data = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Sticker_No": "รออนุมัติ", 
                    "Student_ID": std_id,
                    "Name": std_name,
                    "Level": level,
                    "Department": dept,
                    "Phone": std_phone,
                    "Parent_Name": parent_name,
                    "Relation": relation,
                    "Parent_Phone": parent_phone,
                    "Brand": brand,
                    "Model": model,
                    "Plate_No": plate_no,
                    "Color": color,
                    "Student_Img": path1,
                    "Moto_Img": path2,
                    "Agreement": "ยอมรับแล้ว"
                }

                save_data(data)
                st.success("🎉 บันทึกข้อมูลสำเร็จ! กรุณาติดต่อห้องปกครองเพื่อรับสติ๊กเกอร์")
                st.balloons()
            else:
                st.error("กรุณากรอกข้อมูลให้ครบ, อัปโหลดรูปภาพทั้ง 2 รูป และติ๊กยอมรับเงื่อนไข")

# ==========================================
# TAB 2: สำหรับงานปกครอง (Admin) 
# ==========================================
with tab2:
    st.header("👮 ระบบจัดการข้อมูลงานปกครอง")
    pwd = st.text_input("รหัสผ่านเจ้าหน้าที่", type="password")
    
    if pwd == "admin1234": 
        df = load_data()
        st.metric("จำนวนรถที่ลงทะเบียนทั้งหมด", f"{len(df)} คัน")
        
        # ค้นหาข้อมูลทั่วไป
        search = st.text_input("🔍 ค้นหาในตาราง (ชื่อ, ทะเบียน, รหัส)")
        if search:
            mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
            display_df = df[mask]
        else:
            display_df = df

        st.dataframe(display_df)

        # ---- ระบบพิจารณาอนุมัติรายบุคคล ----
        if not df.empty:
            st.markdown("---")
            st.subheader("🛠️ ระบบตรวจอนุมัติและออกหมายเลขสติ๊กเกอร์")
            
            # ดึงรายชื่อนักเรียน
            student_list = df.apply(lambda row: f"{row['Student_ID']} - {row['Name']} ({row['Sticker_No']})", axis=1).tolist()
            selected_student = st.selectbox("เลือกนักเรียนที่ต้องการตรวจสอบ", student_list)
            
            # ค้นหาข้อมูลแถวของนักเรียนคนนั้น
            selected_id = selected_student.split(" - ")[0]
            student_row = df[df["Student_ID"].astype(str) == selected_id].iloc[0]
            student_index = df[df["Student_ID"].astype(str) == selected_id].index[0]
            
            st.write(f"**ระดับชั้น:** {student_row['Level']} | **แผนกวิชา:** {student_row['Department']} | **เบอร์โทร:** {student_row['Phone']}")
            st.write(f"**ข้อมูลรถ:** ยี่ห้อ {student_row['Brand']} รุ่น {student_row['Model']} | ทะเบียน {student_row['Plate_No']} สี {student_row['Color']}")
            
            # แสดงรูปถ่าย
            col_show1, col_show2 = st.columns(2)
            with col_show1:
                if os.path.exists(str(student_row['Student_Img'])):
                    st.image(student_row['Student_Img'], caption="รูปถ่ายนักเรียนหน้าตรง", use_container_width=True)
                else:
                    st.warning("ไม่พบไฟล์รูปภาพนักเรียน")
            with col_show2:
                if os.path.exists(str(student_row['Moto_Img'])):
                    st.image(student_row['Moto_Img'], caption="รูปถ่ายรถจักรยานยนต์", use_container_width=True)
                else:
                    st.warning("ไม่พบไฟล์รูปภาพรถ")
            
            # ช่องกรอกเลขสติ๊กเกอร์
            current_sticker = student_row['Sticker_No']
            new_sticker_no = st.text_input("ระบุหมายเลขสติ๊กเกอร์ที่ออกให้ (หรือพิมพ์เปลี่ยนสถานะ)", value="" if current_sticker == "รออนุมัติ" else current_sticker)
            
            btn_approve = st.button("💾 บันทึกการอนุมัติ / อัปเดตข้อมูล")
            if btn_approve:
                if new_sticker_no.strip() == "":
                    st.error("กรุณากรอกหมายเลขสติ๊กเกรก่อนกดบันทึก")
                else:
                    df.at[student_index, 'Sticker_No'] = new_sticker_no.strip()
                    df.to_excel(DATA_FILE, index=False)
                    st.success(f"อัปเดตหมายเลขสติ๊กเกอร์ให้กับ {student_row['Name']} สำเร็จเป็น: {new_sticker_no}")
                    st.rerun()
            
            st.markdown("---")
        
        # ---- ปุ่มดาวน์โหลดไฟล์ Excel ----
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "rb") as f:
                st.download_button("📥 ดาวน์โหลดไฟล์ Excel ข้อมูลทั้งหมด", f, file_name="Motorcycle_Data_Chaiyaphum.xlsx")
        else:
            st.info("💡 ยังไม่มีข้อมูลการลงทะเบียนในระบบ (ปุ่มดาวน์โหลดจะแสดงเมื่อมีนักเรียนลงทะเบียนคนแรกเข้ามาครับ)")
            
    elif pwd:
        st.error("รหัสผ่านไม่ถูกต้อง")