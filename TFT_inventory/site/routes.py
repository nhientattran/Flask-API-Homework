from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from TFT_inventory.forms import ChampionForm
from TFT_inventory.models import Champion, db
from TFT_inventory.helpers import champion_info_generator

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    print('Look at this cool project')
    return render_template('index.html')

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    championform = ChampionForm()

    try:
        if request.method == 'POST' and championform.validate_on_submit():
            name = championform.name.data
            description = championform.description.data
            skill = championform.skill.data
            skill_description = championform.skill_description.data
            cost = championform.cost.data
            traits = championform.traits.data
            series = championform.series.data
            if championform.champion_info.data:
                random_info = championform.champion_info.data
            else:
                random_info = champion_info_generator(name)
            user_token = current_user.token

            champion = Champion(name, description, skill, skill_description, cost, traits, series, random_info, user_token)

            db.session.add(champion)
            db.session.commit()

            return redirect(url_for('site.profile'))
    except:
        raise Exception('Champion not created, please check your form and try again')
    
    user_token = current_user.token
    champions = Champion.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=championform, champions=champions)