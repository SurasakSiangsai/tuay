import cv2 as cv #อิมพอตopencv-python
import requests #อิมพอตrequests 

camera = cv.VideoCapture(0) #Cameraของเรา
url = 'https://notify-api.line.me/api/notify'#ลิ้งไลน์เรา
token = 'hGiaE2lAQ5N8aO3L5FAPhSnj5jN28JLnSvTUBCPS7iM'#Tokenไลน์เรา
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer ' + token #เพื่อระบุว่า token คืออะไร
}
#awdawgio9h9aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
#awdawgio9h9aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
#awdawgio9h9aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
#awdawgio9h9aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
#awdawgio9h9aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
#awdawgio9h9aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

msg = 'ตรวจพบความเคลื่อนไหวของกล้องPoom'#ข้อความเเสดงเเจ้งเตือนในไลน์

first_frame = None

while camera.isOpened():
    retry, frame = camera.read()
    
    if not retry:
        break

    if first_frame is None: # กำหนด first_frame ด้วยเฟรมแรกที่ถ่าย
        first_frame = frame
        continue
    
    difference = cv.absdiff(first_frame, frame)#หาความแตกต่างระหว่างภาพแรกกับเฟรมปัจจุบัน
    gray = cv.cvtColor(difference, cv.COLOR_BGR2GRAY)#แปลงเป็นภาพขาวดำ
    blur = cv.GaussianBlur(gray, (5, 5), 0)# ทำการแบลอภาพ
    _, threshold = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)#หาค่าสะพริบ
    dilation = cv.dilate(threshold, None, iterations=5)#ขยายพื้นที่ขาวในรูปภาพ
    contours, _ = cv.findContours(dilation, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)# หาขอบ
    #cv.drawContours(screen1, contours, -1, (0, 255, 0),2)

    for movement in contours:
        if cv.contourArea(movement) < 8000:
            continue
        x, y, w, h = cv.boundingRect(movement)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)#วาดกรอบรอบวัตถุที่มีการเคลื่อนไหว

        notify = requests.post(url, headers=headers, data={'message': msg}) #ส่งการแจ้งเตือนผ่านHTTP POST

    cv.imshow('pyCCTV ของPoomys', frame)#แสดงเฟรมในหน้าต่างรูปภาพ

    if cv.waitKey(10) == ord('q'):
        break#หยุดการทำงานหากผู้ใช้กดปุ่ม 'q' บนคีย์บอร์ด

camera.release() #ปิดการเชื่อมต่อกล้อง
cv.destroyAllWindows()#ปิดหน้าต่างรูปภาพ