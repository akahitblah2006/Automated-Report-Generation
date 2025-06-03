import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
import os


data = pd.read_csv('data.csv')


summary = data.groupby('Product')['Sales'].agg(['sum', 'mean', 'max', 'min']).reset_index()

chart_file = 'sales_chart.png'
plt.figure(figsize=(6,4))
data.groupby('Product')['Sales'].sum().plot(kind='bar', color='skyblue')
plt.title('Total Sales by Product')
plt.ylabel('Sales')
plt.tight_layout()
plt.savefig(chart_file)
plt.close()


class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Sales Report', ln=True, align='C')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'Date: {datetime.date.today()}', ln=True, align='C')
        self.ln(10)

    def create_table(self, dataframe):
        self.set_font('Arial', 'B', 12)
        col_width = self.w / 5
        th = 8
        for col in dataframe.columns:
            self.cell(col_width, th, str(col), border=1)
        self.ln(th)
        self.set_font('Arial', '', 12)
        for i in range(len(dataframe)):
            for col in dataframe.columns:
                self.cell(col_width, th, str(round(dataframe[col][i], 2)), border=1)
            self.ln(th)

pdf = PDFReport()
pdf.add_page()


pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Sales Summary by Product', ln=True)
pdf.ln(5)
pdf.create_table(summary)


pdf.ln(10)
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Sales Chart', ln=True)
pdf.image(chart_file, x=25, w=160)


pdf_file = 'sales_report.pdf'
pdf.output(pdf_file)
print(f' Report generated: {pdf_file}')

if os.path.exists(chart_file):
    os.remove(chart_file)
