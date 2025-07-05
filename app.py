from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

def find_translation(word, source_lang, target_lang, file_path='translations.csv'):
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row.get(source_lang) and row[source_lang].lower() == word.lower():
                return {
                    'original_word': word,
                    'original_lang': source_lang,
                    'translated_word': row[target_lang],
                    'translated_lang': target_lang
                }
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    translation_data = None
    error = None
    if request.method == 'POST':
        word_to_translate = request.form.get('word')
        if word_to_translate:
            # Essayer de traduire de l'anglais vers le français
            translation_data = find_translation(word_to_translate, 'english', 'french')
            # Si ce n'est pas trouvé, essayer du français vers l'anglais
            if not translation_data:
                translation_data = find_translation(word_to_translate, 'french', 'english')
            
            if not translation_data:
                error = f'Le mot "{word_to_translate}" n\'a pas été trouvé dans le dictionnaire.'

    return render_template('index.html', translation=translation_data, error=error)

def get_suggestions(prefix, file_path='translations.csv'):
    suggestions = set()
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row.get('english') and row['english'].lower().startswith(prefix.lower()):
                suggestions.add(row['english'])
            if row.get('french') and row['french'].lower().startswith(prefix.lower()):
                suggestions.add(row['french'])
    return list(suggestions)

@app.route('/suggest')
def suggest():
    query = request.args.get('q', '')
    if len(query) >= 3:
        suggestions = get_suggestions(query)
        return jsonify(suggestions)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)