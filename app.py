from flask import Flask , request , url_for , render_template , redirect
from flask_sqlalchemy import SQLAlchemy
import pyodbc
from sqlalchemy import func
import random

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://DESKTOP-LTKETDU/learnsql?driver=ODBC+Driver+17+for+SQL+Server?trusted_connection=yes"
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False
 
class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column('question_id' , db.Integer , primary_key=True)
    question_text = db.Column('question_text' , db.Unicode , nullable=False)
    answers = db.relationship('Answer', backref='question', lazy='subquery', cascade="save-update, merge, delete")
 
class Answer(db.Model):
    __tablename__ = 'answers'
    answer_id = db.Column('answer_id' , db.Integer , primary_key=True)
    question_id = db.Column('question_id', db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
    question_answer = db.Column('question_answer' , db.Unicode , nullable=False)
    is_correct = db.Column('is_correct' , db.Integer , nullable=False)

@app.route('/', methods = ['POST', 'GET'])
def index():
	correct = 0
	incorrect = 0
	questions = Question.query.all()
	for question in questions:
		random.shuffle(question.answers)
	answers = db.session.query(Answer.question_answer).filter(Answer.is_correct==1)
	if request.method == 'POST':
		for question, answer in zip(questions, answers):
			user_answer = request.form[question.question_text]
			if user_answer in answer:
				correct += 1
			else:
				incorrect += 1
		return render_template('results.html',correct=correct, incorrect=incorrect, question_answers = zip(questions, answers))
	else:
		return render_template('index.html', questions = questions)

@app.route('/question', methods = ['POST', 'GET'])
def question():
	if request.method == 'POST':
		if 'add_question_button' in request.form:
			new_question = request.form['question']
			answer_1 = request.form['answer_1']
			answer_2 = request.form['answer_2']
			answer_3 = request.form['answer_3']
			answer_true = request.form['answer_true']
			add_question = Question(question_text=new_question)
			add_answer_1 = Answer(question=add_question, question_answer=answer_1,is_correct=0)
			add_answer_2 = Answer(question=add_question, question_answer=answer_2,is_correct=0)
			add_answer_3 = Answer(question=add_question, question_answer=answer_3,is_correct=0)
			add_answer_true = Answer(question=add_question, question_answer=answer_true,is_correct=1)

			try:
				db.session.add_all([add_question, add_answer_true, add_answer_1, add_answer_2, add_answer_3])
				db.session.commit()
				return render_template('question.html')

			except:
				return 'There was an issue adding your task'

	else:
		return render_template('question.html')

@app.route('/test')
def test():
	questions = Question.query.all()
	for question in questions:
		random.shuffle(question.answers)
	# answers_list = []
	# x = 4
	# counter = 0
	# question = db.session.query(Question.question_text, Answer.question_answer).join(Answer, Question.answers)
	# q = db.session.query(Question.question_text, Answer.question_answer).join(Answer, Question.answers).filter(Question.question_id == 1)
	# q = db.session.query(Question.question_text, Answer.question_answer).join(Answer, Question.answers)
	# answers = db.session.query(Answer.question_answer).filter(Answer.is_correct==1)
	# questions = db.session.query(Question.question_id)
	# question_number = questions.count()
	# for i in range(question_number+1):
	# 	answer = db.session.query(Answer.question_answer).join(Question, Answer.question_id == Question.question_id).filter(Question.question_id == i)
	# 	for i in answer:
	# 		if len(answers_list) < x:
	# 			answers_list.append(i)

	# random.shuffle(answers_list)
	# questions = Question.query.all()
	# for question in questions:
	# 	for answer in question.answers:
	# 		answers_list.append(answer.question_answer)
	# random.shuffle(answers_list)
	return render_template('test.html', questions=questions)

@app.route('/delete')
def delete():
	questions = db.session.query(Question.question_text, Question.question_id)
	return render_template('delete.html', questions=questions)

@app.route('/delete/<int:id>')
def delete_question(id):
	task_to_delete = Question.query.get_or_404(id)

	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/delete')
	except:
		return 'There was an issue removing your task'

	




if __name__ == '__main__':
	app.run(debug=True)