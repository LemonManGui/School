from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BibleStudyGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Group {self.name}>'

@app.route('/')
def home():
    groups = BibleStudyGroup.query.order_by(BibleStudyGroup.date.asc()).all()
    return render_template('index.html', groups=groups)

@app.route('/add', methods=['POST'])
def add_group():
    name = request.form.get('name')
    topic = request.form.get('topic')
    date = request.form.get('date')
    description = request.form.get('description', '')

    if name and topic and date:
        new_group = BibleStudyGroup(name=name, topic=topic, date=date, description=description)
        db.session.add(new_group)
        db.session.commit()

    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_group(id):
    group = BibleStudyGroup.query.get_or_404(id)

    if request.method == 'POST':
        group.name = request.form['name']
        group.topic = request.form['topic']
        group.date = request.form['date']
        group.description = request.form.get('description', '')
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template('edit.html', group=group)

@app.route('/delete/<int:id>')
def delete_group(id):
    group = BibleStudyGroup.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
