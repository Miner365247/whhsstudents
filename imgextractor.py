from pypdf import PdfReader
import json,string
with open('students.json') as file:
    studentsdata=json.load(file)
for grade in range(7,13):
    listofstudents=[]
    for student in studentsdata:
        if student['grade']==grade:
            listofstudents.append(f'{student["firstName"]} {student["lastName"]}')
    reader = PdfReader(f"./pdfs/grade{grade}.pdf")

    for page_index, page in enumerate(reader.pages):
      for count, image_file_object in enumerate(page.images):
        # Define an output filename
        if image_file_object.name[4] in string.digits:
            index=image_file_object.name[2:5]
        elif image_file_object.name[3] in string.digits:
            index=image_file_object.name[2:4]
        elif image_file_object.name[2] in string.digits:
            index=image_file_object.name[2]
        filename = f"./jpgs/grade{grade}/{listofstudents[int(index)-1]}.jpg"

        # Write the image bytes to disk
        with open(filename, "wb") as fp:
          fp.write(image_file_object.data)

        print(f"Saved: {filename}")
