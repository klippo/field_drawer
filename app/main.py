from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from field_drawer import FieldDrawer
from forms import DrawForm
import simplejson as json
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = '€%€%#dfvdgeryj4wi5t4543&342b'
app.config['TEMPLATES_AUTO_RELOAD'] = True
Bootstrap(app)
csrf = CSRFProtect(app)
csrf.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = DrawForm()
    return render_template('draw.html', form=form)


@app.route('/draw', methods=['POST'])
def draw():
    if request.method == 'POST':
        print(request.form)
        parse_anchors = 'parse_anchors' in request.form
        include_markers = 'include_markers' in request.form
        generate_markers = 'generate_markers' in request.form
        include_all_polylines = 'include_all_polylines' in request.form

        draw_tools_export = request.form['draw_tools_export']
        polyline_color = request.form['polyline_color']
        marker_color = request.form['marker_color']

        anchor1 = request.form['anchor1']
        anchor2 = request.form['anchor2']

        if anchor1 == '' or anchor2 == '' or parse_anchors:
            for portal in json.loads(draw_tools_export):
                if portal["type"] == "polyline":
                    anchor1 = '{},{}'.format(portal["latLngs"][0]['lat'], portal["latLngs"][0]['lng'])
                    anchor2 = '{},{}'.format(portal["latLngs"][1]['lat'], portal["latLngs"][1]['lng'])
                    break
            parse_anchors = True
        print('made it')
        field = FieldDrawer(anchor1, anchor2, draw_tools_export, include_markers, generate_markers, include_all_polylines, polyline_color, marker_color).generate()
        print(field)
        return jsonify(result=field, anchor1=anchor1, anchor2=anchor2, parse_anchors=parse_anchors)


@app.route('/contact')
def faq():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8080,
            use_reloader = True,
            threaded=True)
