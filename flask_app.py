from flask import Flask,redirect,url_for,render_template,request
from datetime import datetime
from fpdf import FPDF
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    branch = db.Column(db.String(100))
    review = db.Column(db.String(500))
    date_posted = db.Column(db.DateTime, default = datetime.now)

items_per_page = 10
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        return render_template('index.html')
         
    page = request.args.get('page',1,type=int)
    reviews = Review.query.paginate(page=page,per_page=items_per_page)
    
    return render_template('index.html', reviews = reviews)

def most_frequent(List):
    
    if len(List) == 0:
        return 0
    
    else:
        counter = 0
        num = List[0]
        
        for element in List:
            current_frequency = List.count(element)
            if(current_frequency > counter):
                counter = current_frequency
                num = element
        
        return num

@app.route('/search',methods=['GET','POST'])
def search():
    num_reviews = 0
    branches = []
    dates = []
    
    Jan = 0
    Feb = 0
    Mar = 0
    Apr = 0
    May = 0
    Jun = 0
    Jul = 0
    Aug = 0
    Sep = 0
    Oct = 0
    Nov = 0
    Dec = 0
    
    if request.method=='POST':
        business = request.form['business']
        
        if business == "" or business == " ":
            business = "Unkown"
            
        else:            
            reviews = Review.query.filter_by(name=business.lower()).all()
            year = datetime.today().strftime('%Y')
            for review in reviews:
                dates.append(review.date_posted.strftime('%d-%m-%Y'))
                branches.append(review.branch)
             
            for date in dates:
                dt = datetime.strptime(date, '%d-%m-%Y')
                #the algorithm should check the year to make sure the report is for the current year
                if year == str(dt.year):
                    if dt.month == 1 :
                        Jan += 1
                    elif dt.month == 2:
                        Feb += 1
                    elif dt.month == 3:
                        Mar += 1
                    elif dt.month == 4:
                        Apr += 1
                    elif dt.month == 5:
                        May += 1
                    elif dt.month == 6:
                        Jun += 1
                    elif dt.month == 7:
                        Jul += 1
                    elif dt.month == 8:
                        Aug += 1
                    elif dt.month == 9:
                        Sep += 1
                    elif dt.month == 10:
                        Oct += 1
                    elif dt.month == 11:
                        Nov += 1
                    elif dt.month == 12:
                        Dec +=1
                
                else:
                    Jan = 0
                    Feb = 0
                    Mar = 0
                    Apr = 0
                    May = 0
                    Jun = 0
                    Jul = 0
                    Aug = 0
                    Sep = 0
                    Oct = 0
                    Nov = 0
                    Dec = 0
                
            num_reviews = Review.query.filter_by(name=business.lower()).count()
            date = datetime.today().strftime('%d-%m-%Y')
            pdf=FPDF(format='letter', unit='in')
            
            pdf.add_page()
            pdf.set_font('Times','',10.0) 
            
            epw = pdf.w - 2*pdf.l_margin
            col_width = epw/4
            
            data = [['Month','Number of Reviews'],
            ['January',Jan],
            ['February',Feb],
            ['March',Mar],
            ['April',Apr],
            ['May',May],
            ['June',Jun],
            ['July',Jul],
            ['August',Aug],
            ['September',Sep],
            ['October',Oct],
            ['November',Nov],
            ['December',Dec],

            ]

            data2 = [['Total Number of Reviews:',num_reviews],
                    ['Most Reviewed Date:',most_frequent(dates)],
                    ['Most Reviewed Branch:',most_frequent(branches)]]
            
            # Document title centered, 'B'old, 14 pt
            pdf.set_font('Times','B',14.0) 
            pdf.cell(epw, 0.0, upper(business), align='C')
            pdf.set_font('Times','',10.0) 
            pdf.ln(0.5)

            th = pdf.font_size
            
            for row in data:
                for datum in row:
                    pdf.cell(col_width, 2*th, str(datum), border=1)
            
                pdf.ln(2*th)
                
            pdf.set_font('Times','B',10.0) 
            for row in data2:
                for item in row:
                    pdf.cell(col_width, 2*th, str(item))
                pdf.ln(2*th)
            
            pdf.set_font('Times','I',10.0)
            pdf.cell(col_width,4*th,f'generated by rant on {date}')
            pdf.ln(2*th)
            pdf.cell(col_width,4*th,'contact developer: gumbimelusi2@gmail.com')
            pdf.output('report.pdf','F')
            
        return render_template('search.html', business = business, num_reviews = num_reviews, reviews = reviews)
    return render_template('search.html',business="NONE")

@app.route('/post_review')
def post_review():
    
    if request.method=='POST':    
        return render_template('post.html')
    
    else:
        return render_template('post.html')

@app.route('/create_post', methods=['GET','POST'])
def create_post():
    
    if request.method=='POST':
        business_name = request.form['name']
        business_branch = request.form['branch']
        details = request.form['details']
        date = datetime.today().strftime('%d-%m-%Y')
        created_review = Review(name = business_name.lower(), branch = business_branch, review = details)
        
        db.session.add(created_review)
        db.session.commit()
        
        return redirect(url_for('home'))
    return "<h1>error while loading page please contact the developer: gumbimelusi@gmail.com</h1>"

@app.route("/download_report")
def download_report():
    #TODO should implement the download report functionality
    return redirect(url_for('home'))

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)