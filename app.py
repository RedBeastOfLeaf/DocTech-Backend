#!/usr/bin/env python
# coding: utf-8
from flask import Flask
from create_table_fpdf2 import PDF

import spacy
import en_core_med7_lg

app = Flask(__name__)
pdf = PDF()

med7 = en_core_med7_lg.load()

# create distinct colours for labels
col_dict = {}
seven_colours = ['#e6194B', '#3cb44b', '#ffe119', '#ffd8b1', '#f58231', '#f032e6', '#42d4f4']
for label, colour in zip(med7.pipe_labels['ner'], seven_colours):
    col_dict[label] = colour

options = {'ents': med7.pipe_labels['ner'], 'colors':col_dict}

text = 'Hello Shriyansh, I have diagnosed your child and i have found that he has extreme fever, I will give you a few medicines please be aware and provide them to the child at the earliest, Syrup Atarax for cold, take it 2 times a day for 15 days, Syrup Meftal P for fever, take it 3 times a day for 20 days.'
doc = med7(text)

spacy.displacy.render(doc, style='ent', jupyter=False, options=options)

l = [(ent.text, ent.label_) for ent in doc.ents]

li = dict()

for ent in doc.ents:
  if ent.label_ not in li.keys():
    li[ent.label_] = [ent.text]
  else:
    li[ent.label_].append(ent.text)



@app.route("/")
def home():
    pdf.add_page()
    pdf.set_font("Times", size=10)
    pdf.create_table(table_data=li, title="DOCTECH", cell_width="even")
    pdf.output("sample.pdf")
    print(li)
    return "hello lauda"

if __name__ == "__main__":
    app.run(debug=True)