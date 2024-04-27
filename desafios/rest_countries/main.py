from flask import Flask, render_template, request, send_file
import services.country_data


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pais', methods=['GET'])
def pesquisar_paises():
    data = request.args.get('q', '')
    try:
        my_data = services.country_data.get_data(data)
    except:
        my_data = []
    return render_template('search_results.html', details = my_data, country_searched = data)
    
@app.route('/pais/<name>', methods=['GET']) 
def get_country_data(name):
    country_details = services.country_data.get_data(name)
    return render_template('country_data.html', nome = name, details = country_details[0])

@app.route('/pais/<name>/download/<format>/', methods=['GET'])
def baixar_dados(name, format):
    if format == 'xml':
        download = services.country_data.criar_xml(name)
        return send_file(download, as_attachment=True)
    elif format == 'xls':
        download = services.country_data.criar_excel(name)
        return send_file(download, as_attachment=True)
    elif format == 'csv':
        download = services.country_data.criar_csv(name)
        return send_file(download, as_attachment=True)
    else:
        return render_template('index.html')
    

if __name__== "__main__":
    app.run(debug=True,port=5001)