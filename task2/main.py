from flask import Flask, render_template, request
from googletrans import Translator

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def translate_text():
    if request.method == 'POST':
        text = request.form['text']
        source_lang = request.form['source_lang']
        target_lang = request.form['target_lang']

        translator = Translator(service_urls=['translate.google.com'])
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        translated_text = translation.text

        return render_template('index.html', translated_text=translated_text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
