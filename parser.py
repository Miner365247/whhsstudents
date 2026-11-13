from pathlib import Path
import pdfquery,json,string
data=[]
grade_num=None
for child in Path('./pdfs').iterdir():
    if child.is_file():
        print(f"{child.name} found!")
        pdf = pdfquery.PDFQuery('./pdfs/'+child.name)
        pdf.load()
        text_elements = pdf.pq('LTTextBoxHorizontal')
        text = [t.text for t in text_elements]
        if text[0][1] in string.digits:
            grade_num=int(text[0][:2])
        else:
            if text[0][0] in string.digits:
                grade_num=int(text[0][0])
            else:
                grade_num=12
        print(grade_num)
        for stringy in text:
            if 'images' in stringy or stringy=='':
                continue
            splity=stringy.split(',')
            person={'firstName':splity[1].strip(), 'lastName':splity[0],'grade':grade_num}
            data.append(person)
with open('students.json','w') as file:
    json.dump(data,file)
