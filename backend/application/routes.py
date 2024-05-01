from flask import request, jsonify
from flask import current_app as app
from application.models import Sample, Post, Section
from application.utils import transliterate_sentence, lang_dict, ak, emo2id
from application.database import db
from datetime import datetime
import json, os
import pandas as pd

@app.route('/')
def index():
    samples = Sample.query.all()
    print(samples)
    return 'Hello, World!'

@app.route('/api/samples', methods=['GET', 'POST'])  # Allow both GET and POST requests
def upload():
    if request.method == 'POST':
        files = request.files
        data = request.form
        audio_files = []
        train_metadata = []
        test_metadata = []

        for name, file in files.items():
            if name == 'trainMetadata':
                file.seek(0)  
                for line in file:
                    train_metadata.append(json.loads(line.decode('utf-8')))
            elif name == 'testMetadata':
                file.seek(0) 
                for line in file:
                    test_metadata.append(json.loads(line.decode('utf-8')))
            elif "audio" == name.split(' ')[0]:
                audio_files.append(file)

        train_df = pd.DataFrame(train_metadata)
        test_df = pd.DataFrame(test_metadata)
        train_df['filename'] = train_df['audio_filepath'].apply(lambda x: x.split('/')[-1].split('.')[0])
        test_df['filename'] = test_df['audio_filepath'].apply(lambda x: x.split('/')[-1].split('.')[0])
        secs = list(set(train_df['emotion']))

        post = Post(title=data['modelName'], description=data['modelDescription'], author=data['uploaderName'])
        db.session.add(post)
        db.session.commit()
        print("Successfully added post")
        sections = {}

        audio_dir = f'/home/sherry/Code/Audio-sample-webpage/test-folder/{post.post_id}'

        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        static_audio_dir = os.path.join(app.root_path, f'static/audios/{post.post_id}')

        if not os.path.exists(static_audio_dir):
            os.makedirs(static_audio_dir)

        train_df['emotion'] = train_df['emotion'].apply(lambda x: emo2id[x])
        test_df['emotion'] = test_df['emotion'].apply(lambda x: emo2id[x])

        train_df['speaker'] = train_df['filename'].apply(lambda x: x.split('_')[1])
        test_df['speaker'] = test_df['filename'].apply(lambda x: x.split('_')[1])

        train_df.to_csv(f'{audio_dir}/train_metadata.csv', index=False)
        os.symlink(f'{audio_dir}/train_metadata.csv', f'{static_audio_dir}/train_metadata.csv')
        test_df.to_csv(f'{audio_dir}/test_metadata.csv', index=False)
        os.symlink(f'{audio_dir}/test_metadata.csv', f'{static_audio_dir}/test_metadata.csv')

        for value in audio_files:
            lang_iso, gender, cat = value.filename.split('_')[:3]
            cat = "NEUTRAL" if (cat == 'INDIC' or cat == 'WIKI') else cat
            lang, gender = lang_dict[lang_iso.lower()], "Female" if gender.lower() == 'f' else "Male"
            id_name = str(cat) + '_' + str(lang) + '_' + str(gender)

            if id_name not in sections:
                section = Section(post_id=post.post_id, section_name=data['modelName'], description=data['modelDescription'], language=lang, gender=gender, category=cat)
                db.session.add(section)
                db.session.commit()
                sections[id_name] = section.section_id
            
            value.save(os.path.join(audio_dir, value.filename))
            os.symlink(os.path.join(audio_dir, value.filename), os.path.join(static_audio_dir, value.filename))

            transcript = test_df[test_df['filename'] == value.filename.split('.')[0]].iloc[0]['text']
            transliteration = transliterate_sentence(transcript, ak[lang_iso.lower()][0], 'ISO')
            sample = Sample(section_id=sections[id_name], sample_dir=value.filename, transcript=transcript, transliteration=transliteration)
            db.session.add(sample)
            db.session.commit()
        return 'Success', 200
    else:
        return 'Method Not Allowed', 405 

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return jsonify({'error': 'Post not found'}), 404

    train_df = pd.read_csv(f'{app.root_path}/static/audios/{post_id}/train_metadata.csv')
    test_df = pd.read_csv(f'{app.root_path}/static/audios/{post_id}/test_metadata.csv')

    sections = Section.query.filter_by(post_id=post_id).all()
    section_data = []
    for section in sections:
        section_duration = train_df[(train_df['emotion'].apply(lambda x: x.lower()) == section.category.lower()) & (train_df['speaker'].apply(lambda x: x.lower()) == section.gender[0].lower())]['duration'].sum()
        # convert section duration to hours
        section_duration = section_duration / 3600
        print(section_duration)
        samples = Sample.query.filter_by(section_id=section.section_id).all()
        sample_data = [{'id': sample.sample_id,'sample_dir': sample.sample_dir, 'transcript': sample.transcript, 'transliteration': sample.transliteration} for sample in samples]
        section_data.append({
            'id': section.section_id,
            'section_name': section.section_name,
            'description': section.description,
            'language': section.language,
            'gender': section.gender,
            'category': section.category,
            'samples': sample_data,
            'duration': round(section_duration, 2)
        })

    post_data = {
        'id': post.post_id,
        'title': post.title,
        'description': post.description,
        'author': post.author,
        'sections': section_data
    }

    return jsonify(post_data)


@app.route('/api/posts/recent', methods=['GET'])
def get_recent_posts():
    # Get the optional query parameters for language, gender, and category
    language = request.args.get('language', default=None)
    gender = request.args.get('gender', default=None)
    category = request.args.get('category', default=None)

    print(language, gender, category)

    recent_posts = Post.query.order_by(Post.date.desc()).all()  # Get the most recent posts

    for post in recent_posts:
        sections = Section.query.filter_by(post_id=post.post_id).all()
        state = False
        for section in sections:
            if language is "" and gender is "" and category is "":
                state = True
                break
            if language is not "" and section.language.lower() == language.lower():
                print(category.lower(), section.category.lower())
                if gender is "" and category is "":
                    state = True
                    break
                if gender is not "" and section.gender[0].lower() == gender[0].lower():
                    state = True
                    break
                if category is not "" and section.category.lower() == category.lower():
                    state = True
                    break


        if not state:
            recent_posts.remove(post)

    print(len(recent_posts))

    recent_posts_data = []

    for post in recent_posts:
        sections = Section.query.filter_by(post_id=post.post_id).all()
        sample_count = 0  # Initialize sample count for the post
        for section in sections:
            samples = Sample.query.filter_by(section_id=section.section_id).all()
            sample_count += len(samples)  # Increment the sample count by the number of samples in each section
        
        post_data = {
            'id': post.post_id,
            'title': post.title,
            'author': post.author,
            'date': post.date.strftime("%Y-%m-%d %H:%M:%S"),
            'description': post.description,
            'sample_count': sample_count  # Add the sample count to the post data
        }
        recent_posts_data.append(post_data)

    return jsonify(recent_posts_data)