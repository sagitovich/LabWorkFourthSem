import datetime as dt
from schema import factory, User, Story, Category
from web_data import StoryForm
from forms import RegistrationForm, EditUserForm
from flask import Flask, request, render_template, redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890qwertyuiop'  # добавьте секретный ключ для CSRF


@app.errorhandler(404)
def router_not_found(e):
    return render_template('page-not-found.html')


@app.route('/')
@app.route('/index')
def show_all_news():
    result = session.query(Story)
    return render_template('all-news-page.html', stories=result)


@app.route('/add-story', methods=["GET", "POST"])
def add_new_story():
    all_users = session.query(User)
    all_categories = session.query(Category)

    story_form = StoryForm()

    story_form.story_author.choices = [
        (u.id, f'{u.first_name} {u.last_name} ({u.username})') for u in all_users
    ]

    story_form.story_topics.choices = [(c.id, c.name) for c in all_categories]

    if request.method == "GET":
        story_form.creation_date.data = dt.datetime.now()
        return render_template('add-story-page.html', f=story_form)

    if request.method == "POST":
        story_form.process(request.form)

        if not story_form.validate():
            return render_template('add-story-page.html', f=story_form)

        new_story = Story()
        new_story.title = story_form.story_title.data
        new_story.content = story_form.story_content.data
        new_story.author_id = story_form.story_author.data

        if story_form.scope.data == 'public':
            new_story.is_private = False

        if story_form.creation_date.data is not None:
            new_story.created_on = story_form.creation_date.data

        print(story_form.story_topics.data)

        for category_id in story_form.story_topics.data:
            c = session.get(Category, category_id)
            new_story.categories.append(c)

        try:
            session.add(new_story)
            session.commit()
            return redirect('/index')
        except Exception as e:
            session.rollback()
            return f"Что-то пошло не так. Ошибка: {e}"


@app.route('/edit-story/<int:story_id>', methods=["GET", "POST"])
def edit_existing_story(story_id):
    story = session.get(Story, story_id)
    if story is None:
        return f"Истории с идентификатором {story_id} не существует."

    all_users = session.query(User)
    all_categories = session.query(Category)

    story_form = StoryForm()

    story_form.story_author.choices = [
        (u.id, f'{u.first_name} {u.last_name} ({u.username})') for u in all_users
    ]

    story_form.story_topics.choices = [(c.id, c.name) for c in all_categories]

    if request.method == "GET":
        story_form.story_title.data = story.title
        story_form.story_content.data = story.content
        story_form.story_author.data = story.author_id

        if story.is_private:
            story_form.scope.data = "private"
        else:
            story_form.scope.data = "public"

        story_form.story_topics.data = [c.id for c in story.categories]
        story_form.creation_date.data = story.created_on
        story_form.responsibility.data = True

        return render_template("edit-story-page.html", story_id=story.id, f=story_form)

    if request.method == "POST":
        story_form.process(request.form)

        if not story_form.validate():
            return render_template("edit-story-page.html", story_id=story.id, f=story_form)

        story.title = story_form.story_title.data
        story.content = story_form.story_content.data

        story.author_id = story_form.story_author.data

        if story_form.scope.data == 'public':
            story.is_private = False

        story.created_on = story_form.creation_date.data

        # print(story_form.story_topics.data)

        story.categories.clear()
        for category_id in story_form.story_topics.data:
            c = session.get(Category, category_id)
            story.categories.append(c)

        try:
            session.commit()
            return redirect('/index')
        except Exception as e:
            session.rollback()
            return f"Что-то пошло не так. Ошибка: {e}"


@app.route('/delete-story/<int:story_id>')
def delete_existing_story(story_id):
    story = session.get(Story, story_id)
    if story is None:
        return f"Истории с идентификатором {story_id} не существует."

    try:
        session.delete(story)
        session.commit()
        return redirect('/index')
    except Exception as e:
        session.rollback()
        return f"Что-то пошло не так. Ошибка: {e}"


@app.route('/register', methods=["GET", "POST"])
def register_user():
    form = RegistrationForm()

    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User(
                username=form.username.data,
                first_name='',  # можно добавить форму для ввода имени
                last_name='',  # можно добавить форму для ввода фамилии
                created_on=dt.datetime.now()
            )
            new_user.set_password(form.password.data)  # хэшируем пароль перед сохранением
            try:
                session.add(new_user)
                session.commit()
                return redirect('/index')
            except Exception as e:
                session.rollback()
                return f"Что-то пошло не так. Ошибка: {e}"

    return render_template('register.html', form=form)


@app.route('/edit-user/<int:user_id>', methods=["GET", "POST"])
def edit_user(user_id):
    user = session.get(User, user_id)
    if user is None:
        return f"Пользователь с идентификатором {user_id} не существует."

    form = EditUserForm()

    if request.method == "GET":
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        return render_template('edit-user.html', form=form, user_id=user.id)

    if request.method == "POST":
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data

            if form.password.data:
                user.set_password(form.password.data)

            try:
                session.commit()
                return redirect('/index')
            except Exception as e:
                session.rollback()
                return f"Что-то пошло не так. Ошибка: {e}"

    return render_template('edit-user.html', form=form, user_id=user.id)

if __name__ == "__main__":
    session = factory()
    app.run(host="127.0.0.1", port=4321)
