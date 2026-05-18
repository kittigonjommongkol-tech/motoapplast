import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ตั้งค่าหน้าเว็บแอปที่ 2 ---
st.set_page_config(page_title="ระบบคะแนนความประพฤติ - วก.ชัยภูมิ", page_icon="⚖️", layout="wide")

# --- 2. การจัดการไฟล์ข้อมูล ---
STUDENT_MASTER = "student_conduct_master.xlsx" 
PUNISHMENT_LOG = "conduct_punishment_logs.xlsx" 

def load_student_master():
    if os.path.exists(STUDENT_MASTER):
        try: return pd.read_excel(STUDENT_MASTER)
        except: return pd.DataFrame()
    else:
        return pd.DataFrame(columns=["Student_ID", "Name", "Level", "Department", "Current_Score"])

def load_punishment_logs():
    if os.path.exists(PUNISHMENT_LOG):
        try: return pd.read_excel(PUNISHMENT_LOG)
        except: return pd.DataFrame()
    else:
        return pd.DataFrame(columns=[
            "Log_ID", "Timestamp", "Student_ID", "Violation_Type", 
            "Score_Deducted", "Reporter_Teacher", "Status", "Committee_Summary"
        ])

def save_to_excel(df, filename):
    df.to_excel(filename, index=False)

# 🚨 ฟังก์ชันใส่สีแถบตารางตามเกณฑ์ระเบียบใหม่ของอาจารย์กิตติกร
def color_score_by_rule(row):
    score = row["Current_Score"]
    if score == 100:
        color = '#d4edda' # 🟢 สีเขียว: ปกติ 100 คะแนนเต็ม
    elif score >= 70:
        color = '#fff3cd' # 🟡 สีเหลือง: โดนหักคะแนนแล้ว (ครูที่ปรึกษาต้องเชิญผู้ปกครองพบ)
    else:
        color = '#f8d7da' # 🔴 สีแดง: หักคะแนนเกิน 30 คะแนน (พิจารณาพักการเรียน/ย้ายสถานศึกษา)
    return [f'background-color: {color}; font-weight: bold;' for _ in row]

# --- 3. หน้าตาและการแสดงผลแอป ---
st.title("⚖️ ระบบบริหารจัดการคะแนนความประพฤตินักเรียน")
st.subheader("วิทยาลัยเกษตรและเทคโนโลยีชัยภูมิ")
st.markdown("---")

col_left, col_right = st.columns([2, 1])

# ==========================================
# ฝั่งซ้าย: สำหรับคณะครูและครูที่ปรึกษา
# ==========================================
with col_left:
    st.header("📋 ตรวจสอบพฤติกรรม (สำหรับครูทั่วไป/ครูที่ปรึกษา)")
    
    df_master = load_student_master()
    df_logs = load_punishment_logs()
    
    if df_master.empty:
        st.warning("⚠️ ยังไม่มีข้อมูลนักเรียนในระบบ (หัวหน้างานปกครองต้องลงทะเบียนข้อมูลนักเรียนในระบบก่อนครับ)")
    else:
        search_query = st.text_input("🔍 ค้นหานักเรียน (กรอกรหัสประจำตัว หรือ ชื่อ-สกุล เพื่อตรวจแต้ม)")
        
        if search_query:
            mask = df_master.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            display_df = df_master[mask]
        else:
            display_df = df_master
            
        st.markdown("""
        **📊 เกณฑ์การพิจารณาและแถบสีแจ้งเตือน:**
        - 🟢 **แถบสีเขียว (100 คะแนนเต็ม):** พฤติกรรมปกติ 
        - 🟡 **แถบสีเหลือง (โดนหักแต้ม):** ครูที่ปรึกษาโปรดดึงข้อมูลเพื่อ**ติดต่อเชิญผู้ปกครองมาพบปะพูดคุย**
        - 🔴 **แถบสีแดง (หักคะแนนเกิน 30 คะแนน/เหลือต่ำกว่า 70 แต้ม):** งานปกครองเสนอคณะกรรมการ**พิจารณาพักการเรียน หรือย้ายสถานศึกษา**
        """)
        
        # แสดงตารางแบบไฮไลต์ทั้งแถวตามเกณฑ์ความรุนแรง
        st.dataframe(display_df.style.apply(color_score_by_rule, axis=1), use_container_width=True)
        
        st.markdown("---")
        st.subheader("📜 ประวัติการบันทึกความผิดและการบำเพ็ญประโยชน์โดยละเอียด")
        if df_logs.empty:
            st.info("ยังไม่มีประวัติการทำผิดวินัยในระบบ")
        else:
            st.dataframe(df_logs[["Timestamp", "Student_ID", "Violation_Type", "Score_Deducted", "Reporter_Teacher", "Status", "Committee_Summary"]], use_container_width=True)
        
        st.markdown("---")
        with open(STUDENT_MASTER, "rb") as f:
            st.download_button("📥 ดาวน์โหลดตารางคะแนนความประพฤติรวม (Excel)", f, file_name="Student_Conduct_Scores.xlsx")

# ==========================================
# ฝั่งขวา: สำหรับหัวหน้างานปกครอง (Admin)
# ==========================================
with col_right:
    st.header("🔒 ส่วนของหัวหน้างานปกครอง")
    admin_pwd = st.text_input("กรุณากรอกรหัสผ่านเพื่อจัดการระบบ", type="password")
    
    if admin_pwd == "head1234": 
        st.success("🔓 ยินดีต้อนรับหัวหน้างานปกครอง วก.ชัยภูมิ")
        
        menu = st.radio("เลือกงานที่ต้องการทำ:", ["1. เพิ่มนักเรียนเข้าสู่ระบบ", "2. บันทึกการทำผิดกฎระเบียบ", "3. ปิดเคสบำเพ็ญประโยชน์"])
        
        # ------------------------------------
        # เมนูที่ 1: เพิ่มนักเรียนใหม่
        # ------------------------------------
        if menu == "1. เพิ่มนักเรียนเข้าสู่ระบบ":
            with st.form("add_student_form", clear_on_submit=True):
                new_id = st.text_input("รหัสประจำตัวนักเรียน")
                new_name = st.text_input("ชื่อ - นามสกุล")
                new_level = st.selectbox("ระดับชั้น", ["ปวช.1", "ปวช.2", "ปวช.3", "ปวส.1", "ปวส.2", "ปริญญาตรี"])
                new_dept = st.text_input("แผนกวิชา")
                
                btn_add = st.form_submit_button("➕ ลงทะเบียนฐานคะแนน 100 แต้มเริ่มต้น")
                if btn_add:
                    if new_id and new_name:
                        df_m = load_student_master()
                        if new_id in df_m["Student_ID"].astype(str).values:
                            st.error("รหัสนักเรียนนี้มีในระบบแล้ว")
                        else:
                            new_row = {"Student_ID": new_id, "Name": new_name, "Level": new_level, "Department": new_dept, "Current_Score": 100}
                            df_m = pd.concat([df_m, pd.DataFrame([new_row])], ignore_index=True)
                            save_to_excel(df_m, STUDENT_MASTER)
                            st.success(f"บันทึก {new_name} เข้าฐานคะแนนประพฤติเรียบร้อย")
                            st.rerun()
                            
        # ------------------------------------
        # เมนูที่ 2: บันทึกการทำผิด (หักคะแนนตามเกณฑ์ใหม่)
        # ------------------------------------
        elif menu == "2. บันทึกการทำผิดกฎระเบียบ":
            df_m = load_student_master()
            if df_m.empty:
                st.warning("กรุณาเพิ่มนักเรียนในเมนูที่ 1 ก่อนครับ")
            else:
                student_options = df_m.apply(lambda r: f"{r['Student_ID']} - {r['Name']} (แต้มปัจจุบัน: {r['Current_Score']})", axis=1).tolist()
                selected_student = st.selectbox("เลือกนักเรียนผู้กระทำความผิด", student_options)
                selected_id = selected_student.split(" - ")[0]
                
                # ตัวเลือกกลุ่มคะแนนที่จะหัก
                score_category = st.selectbox("🎯 เลือกระดับการหักคะแนน", ["หัก 5 คะแนน", "หัก 10 คะแนน", "หัก 15 คะแนน", "หัก 20 คะแนน"])
                
                # เปลี่ยนตัวเลือกความผิดไปตามกลุ่มคะแนนที่หัวหน้างานเลือก
                if score_category == "หัก 5 คะแนน":
                    violation_detail = st.selectbox("ระบุฐานความผิด (หมวด 5 คะแนน)", [
                        "ข้อ 1. แต่งกายไม่สุภาพหรือแต่งกายผิดระเบียบ",
                        "ข้อ 2. สูบบุหรี่ในที่เปิดเผย",
                        "ข้อ 3. มีอุปกรณ์ เล่นการพนันไว้ในครอบครอง",
                        "ข้อ 4. หลีกเลี่ยงการเข้าร่วมกิจกรรมที่วิทยาลัยกำหนด",
                        "ข้อ 5. นักเรียนนักศึกษาชายห้ามใส่ต่างหูทุกชนิด",
                        "ข้อ 6. ความผิดอื่นๆ ซึ่งคณะกรรมการฯ เห็นสมควรลงโทษในหมวดนี้"
                    ])
                    deduct_value = 5
                    
                elif score_category == "หัก 10 คะแนน":
                    violation_detail = st.selectbox("ระบุฐานความผิด (หมวด 10 คะแนน)", [
                        "ข้อ 1. แสดงกริยาวาจาไม่สุภาพ",
                        "ข้อ 2. ขัดคำสั่งอันชอบของครู-อาจารย์",
                        "ข้อ 3. เข้าไปในเขตหวงห้ามโดยไม่ได้ได้รับอนุญาต",
                        "ข้อ 4. กระทำผิดระเบียบการใช้โรงอาหาร/หอพัก/ห้องสมุด/รถจักรยานยนต์ในสถานศึกษา",
                        "ข้อ 5. แสดงพฤติกรรมทางชู้สาวที่ไม่เหมาะสมในที่สาธารณะ",
                        "ข้อ 6. ความผิดอื่นๆ ซึ่งคณะกรรมการฯ เห็นสมควรลงโทษในหมวดนี้"
                    ])
                    deduct_value = 10
                    
                elif score_category == "หัก 15 คะแนน":
                    violation_detail = st.selectbox("ระบุฐานความผิด (หมวด 15 คะแนน)", [
                        "ข้อ 1. ก่อความเดือดร้อนแก่ผู้อื่น หรือก่อการทะเลาะวิวาทชกต่อย หรือกระทำให้เกิดความแตกแยกสามัคคี",
                        "ข้อ 2. ยุยง ส่งเสริม ให้เกิดความกระด้างกระเดื่อง เพื่อฝ่าฝืนระเบียบของสถานศึกษา",
                        "ข้อ 3. ดื่มสุรา หรือของมึนเมา หรือเป็นผู้ที่มีส่วนร่วมในการจัดซื้อจัดหาหรือจัดให้มีการดื่ม",
                        "ข้อ 4. ลักทรัพย์ กรรโชกทรัพย์ ข่มขู่หรือบังคับขืนใจ หรือรีดไถบุคคลอื่น",
                        "ข้อ 5. ความผิดอื่นๆ ซึ่งคณะกรรมการฯ เห็นสมควรลงโทษในหมวดนี้"
                    ])
                    deduct_value = 15
                    
                elif score_category == "หัก 20 คะแนน":
                    violation_detail = st.selectbox("ระบุฐานความผิด (หมวด 20 คะแนน)", [
                        "ข้อ 1. ประพฤติตนไม่เหมาะสมกับวัย หรือเข้าไปในบ่อการพนัน/สถานโสเภณี/อาบอบนวด/สถานบริการ",
                        "ข้อ 2. ดื่มสุราหรือของมึนเมาจนครองสติไม่ได้",
                        "ข้อ 3. เสพยาเสพติด เสพสารระเหย หรือมีไว้ครอบครอง",
                        "ข้อ 4. ลบหลู่ ครู-อาจารย์",
                        "ข้อ 5. เล่นการพนันหรือจัดให้มีการเล่นการพนันที่ผิดกฎหมาย",
                        "ข้อ 6. เกี่ยวข้องกับการค้าประเวณี",
                        "ข้อ 7. ความผิดอื่นๆ ซึ่งคณะกรรมการฯ เห็นสมควรลงโทษในหมวดนี้"
                    ])
                    deduct_value = 20

                teacher_name = st.text_input("ชื่อครูผู้ตรวจพบเหตุการณ์ / ผู้ส่งเรื่อง")
                
                if st.button("🚨 ยืนยันการตัดคะแนนความประพฤติ"):
                    idx = df_m[df_m["Student_ID"].astype(str) == str(selected_id)].index[0]
                    old_score = df_m.at[idx, "Current_Score"]
                    new_score = max(0, old_score - deduct_value)
                    df_m.at[idx, "Current_Score"] = new_score
                    save_to_excel(df_m, STUDENT_MASTER)
                    
                    df_l = load_punishment_logs()
                    log_id = f"LOG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    
                    full_violation_text = f"[{score_category}] {violation_detail}"
                    
                    new_log = {
                        "Log_ID": log_id, "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Student_ID": selected_id, "Violation_Type": full_violation_text,
                        "Score_Deducted": deduct_value, "Reporter_Teacher": teacher_name,
                        "Status": "⏳ กำลังดำเนินการบำเพ็ญประโยชน์", "Committee_Summary": "อยู่ระหว่างรอผลพิจารณาและเรียกพบผู้ปกครอง"
                    }
                    df_l = pd.concat([df_l, pd.DataFrame([new_log])], ignore_index=True)
                    save_to_excel(df_l, PUNISHMENT_LOG)
                    
                    st.error(f"⚠️ ตัดคะแนนสำเร็จ! หัก {deduct_value} แต้ม จากนักเรียนรหัส {selected_id}")
                    
                    # แสดงข้อความเตือนนโยบายบนหน้าจอป๊อปอัปทันทีเมื่อตัดคะแนน
                    if new_score < 70:
                        st.error(f"🚨 [วิกฤต] นักเรียนคนนี้ถูกหักคะแนนสะสมเกิน 30 คะแนนแล้ว (เหลือ {new_score} แต้ม) เข้าเกณฑ์พิจารณาพักการเรียนหรือย้ายสถานศึกษา!")
                    else:
                        st.warning(f"📢 [แจ้งเตือน] นักเรียนถูกหักคะแนน (เหลือ {new_score} แต้ม) ครูที่ปรึกษาต้องติดต่อเชิญผู้ปกครองมาพบปะพูดคุย")
                        
                    st.rerun()

        # ------------------------------------
        # เมนูที่ 3: บำเพ็ญประโยชน์เสร็จสิ้น + เขียนมติกรรมการ
        # ------------------------------------
        elif menu == "3. ปิดเคสบำเพ็ญประโยชน์":
            df_l = load_punishment_logs()
            active_logs = df_l[df_l["Status"] == "⏳ กำลังดำเนินการบำเพ็ญประโยชน์"]
            
            if active_logs.empty:
                st.info("ไม่มีเคสความผิดค้างคาในระบบขณะนี้ครับ")
            else:
                log_options = active_logs.apply(lambda r: f"{r['Log_ID']} | รหัส: {r['Student_ID']} | {r['Violation_Type']}", axis=1).tolist()
                selected_log = st.selectbox("เลือกรายการความผิดที่นักเรียนได้บำเพ็ญประโยชน์แก้ไขแล้ว", log_options)
                selected_log_id = selected_log.split(" | ")[0]
                
                committee_text = st.text_area("✍️ เขียนอธิบายข้อสรุป/มติของคณะกรรมการพิจารณาโทษ", placeholder="กรอกมติคณะกรรมการ เช่น บำเพ็ญประโยชน์ล้างห้องน้ำและปรับปรุงพฤติกรรมเรียบร้อย คณะกรรมการมีมติเห็นชอบยุติการคาดโทษ")
                
                refund_score = st.checkbox("🔄 คืนคะแนนความประพฤติให้เด็ก (กรณีทำความดีชดเชย)")
                score_to_refund = 0
                if refund_score:
                    score_to_refund = st.number_input("จำนวนแต้มที่จะบวกคืนให้เด็ก", min_value=1, max_value=20, value=5)
                
                if st.button("✅ บันทึกเครื่องหมายเสร็จสิ้นและปิดเคส"):
                    log_idx = df_l[df_l["Log_ID"] == selected_log_id].index[0]
                    df_l.at[log_idx, "Status"] = "✅ ดำเนินการเสร็จสิ้น"
                    df_l.at[log_idx, "Committee_Summary"] = committee_text if committee_text else "บำเพ็ญประโยชน์เรียบร้อย"
                    save_to_excel(df_l, PUNISHMENT_LOG)
                    
                    if score_to_refund > 0:
                        df_m = load_student_master()
                        target_sid = df_l.at[log_idx, "Student_ID"]
                        m_idx = df_m[df_m["Student_ID"].astype(str) == str(target_sid)].index[0]
                        df_m.at[m_idx, "Current_Score"] = min(100, df_m.at[m_idx, "Current_Score"] + score_to_refund)
                        save_to_excel(df_m, STUDENT_MASTER)
                    
                    st.success("บันทึกปิดเคสและสรุปมติคณะกรรมการเรียบร้อยแล้ว!")
                    st.rerun()
                    
    elif admin_pwd:
        st.error("รหัสผ่านไม่ถูกต้อง (สิทธิ์เฉพาะหัวหน้างานปกครองเท่านั้น)")