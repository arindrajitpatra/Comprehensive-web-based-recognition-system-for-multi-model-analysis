from flask import Flask, render_template, Response,jsonify,request,session,redirect,url_for
#FlaskForm--> it is required to receive input from the user
# Whether uploading a video file  to our object detection model
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField,StringField,DecimalRangeField,IntegerRangeField 
from werkzeug.utils import secure_filename 
from wtforms.validators import InputRequired,NumberRange
import os
import cv2

# YOLO_Video is the python file which contains the code for our object detection model
#Video Detection is the Function which performs Object Detection on Input Video
from final_merge import main
from object import obj
from text import text
from url_object import urlobj
from url_text import urltext
from url_color import urlcol
from ipobj import ip_obj
from iptext import ip_text
from ipcol import ip_col
from speech2text import SpeechToText

app = Flask(__name__)

app.config['SECRET_KEY'] = 'group_1'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'files')

#Use FlaskForm to get input video file  from user
class UploadFileForm(FlaskForm):
    #We store the uploaded video file path in the FileField in the variable file
    #We have added validators to make sure the user inputs the video in the valid format  and user does upload the
    #video when prompted to do so
    file = FileField("File",validators=[InputRequired()])
    submit = SubmitField("Run")

app.secret_key = 'souvik_1'

#output generate for url
def generate_url_obj(path_x = ''):
    yolo_output = urlobj(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        
def generate_url_text(path_x = ''):
    yolo_output = urltext(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        
def generate_url_col(path_x = ''):
    yolo_output = urlcol(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')

#output generate for video/webcam
def generate_frames_col(path_x = ''):
    yolo_output = main(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        
def generate_frames_obj(path_x = ''):
    yolo_output = obj(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        
def generate_frames_text(path_x = ''):
    yolo_output = text(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')

#output generate for ip
def generate_ip_obj(path_x = ''):
    yolo_output = ip_obj(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        
def generate_ip_text(path_x = ''):
    yolo_output = ip_text(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        
def generate_ip_col(path_x = ''):
    yolo_output = ip_col(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    session.clear()
    return render_template('indexproject.html')

@app.route("/sptxt", methods=['GET','POST'])
def sptxt():
    session.clear()
    return render_template('sp_text.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        session['speech_video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             filename)
        text_generator=SpeechToText(session.get('speech_video_path', None))
        text_list = list(text_generator)
        result = '\n'.join(text_list)

    return render_template('sp_text.html', filename=filename, result=result)


# Rendering the Webcam Rage
#Now lets make a Webcam page for the application
#Use 'app.route()' method, to render the Webcam page at "/webcam"
@app.route("/webcam", methods=['GET','POST'])
def webcam_col():
    session.clear()
    return render_template('uicol.html')

@app.route("/webobj", methods=['GET','POST'])
def webcam_obj():
    session.clear()
    return render_template('uiobj.html')

@app.route("/webtext", methods=['GET','POST'])
def webcam_text():
    session.clear()
    return render_template('uitext.html')

#for url :
@app.route('/getobjurl', methods=['GET','POST'])
def getobjurl():
    session.clear()
    return render_template('url_obj.html')

@app.route('/gettexturl', methods=['GET','POST'])
def gettexturl():
    session.clear()
    return render_template('url_text.html')

@app.route('/getcolurl', methods=['GET','POST'])
def getcolurl():
    session.clear()
    return render_template('url_col.html')

#for ip :
@app.route('/getipobj', methods=['GET','POST'])
def getipobj():
    session.clear()
    return render_template('ip_obj.html')

@app.route('/getiptext', methods=['GET','POST'])
def getiptext():
    session.clear()
    return render_template('ip_text.html')

@app.route('/getipcol', methods=['GET','POST'])
def getipcol():
    session.clear()
    return render_template('ip_col.html')

#for video upload :
@app.route('/vdocol', methods=['GET','POST'])
def front_col():
    # Upload File Form: Create an instance for the Upload File Form
    form = UploadFileForm()
    if form.validate_on_submit():
        # Our uploaded video file path is saved here
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))  # Then save the file
        # Use session storage to save video file path
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('video_col.html', form=form)


@app.route('/vdotext', methods=['GET','POST'])
def front_text():
    # Upload File Form: Create an instance for the Upload File Form
    form = UploadFileForm()
    if form.validate_on_submit():
        # Our uploaded video file path is saved here
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))  # Then save the file
        # Use session storage to save video file path
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('video_text.html', form=form)


@app.route('/vdoobj', methods=['GET','POST'])
def front_obj():
    # Upload File Form: Create an instance for the Upload File Form
    form = UploadFileForm()
    if form.validate_on_submit():
        # Our uploaded video file path is saved here
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))  # Then save the file
        # Use session storage to save video file path
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('video_obj.html', form=form)

#url collection for youtube
@app.route('/objurl', methods=['GET','POST'])
def objurl():
    video_url = request.form['url']
    session['url']=video_url
    return render_template('url_obj.html',res=video_url)

@app.route('/texturl', methods=['GET','POST'])
def texturl():
    video_url = request.form['url']
    session['url']=video_url
    return render_template('url_text.html',res=video_url)

@app.route('/colurl', methods=['GET','POST'])
def colurl():
    video_url = request.form['url']
    session['url']=video_url
    return render_template('url_col.html',res=video_url)

#url collection for ip
@app.route('/ipobj', methods=['GET','POST'])
def ipobj():
    video_url = request.form['url']
    session['url']=video_url
    return render_template('ip_obj.html',res=video_url)

@app.route('/iptext', methods=['GET','POST'])
def iptext():
    video_url = request.form['url']
    session['url']=video_url
    return render_template('ip_text.html',res=video_url)

@app.route('/ipcol', methods=['GET','POST'])
def ipcol():
    video_url = request.form['url']
    session['url']=video_url
    return render_template('ip_col.html',res=video_url)

#display output for video upload
@app.route('/video_col')
def video_col():
    #return Response(generate_frames_col(path_x='static/files/bikes.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames_col(path_x = session.get('video_path', None)),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_text')
def video_text():
    #return Response(generate_frames_col(path_x='static/files/bikes.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames_text(path_x = session.get('video_path', None)),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_obj')
def video_obj():
    #return Response(generate_frames_col(path_x='static/files/bikes.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames_obj(path_x = session.get('video_path', None)),mimetype='multipart/x-mixed-replace; boundary=frame')

# To display the Output Video on Webcam page
@app.route('/webapp_col')
def webapp_col():
    #return Response(generate_frames_col(path_x = session.get('video_path', None),conf_=round(float(session.get('conf_', None))/100,2)),mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames_col(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webapp_text')
def webapp_text():
    #return Response(generate_frames_col(path_x = session.get('video_path', None),conf_=round(float(session.get('conf_', None))/100,2)),mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames_text(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webapp_obj')
def webapp_obj():
    #return Response(generate_frames_col(path_x = session.get('video_path', None),conf_=round(float(session.get('conf_', None))/100,2)),mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames_obj(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

#detection for url
@app.route('/detectobjurl', methods=['GET','POST'])
def detectobjurl():
    url = session['url']
    return Response(generate_url_obj(url), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detecttexturl', methods=['GET','POST'])
def detecttexturl():
    url = session['url']
    return Response(generate_url_text(url), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detectcolurl', methods=['GET','POST'])
def detectcolurl():
    url = session['url']
    return Response(generate_url_col(url), mimetype='multipart/x-mixed-replace; boundary=frame')

#detection for ip 
@app.route('/detectobjip', methods=['GET','POST'])
def detectobjip():
    url = session['url']
    return Response(generate_ip_obj(url), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detecttextip', methods=['GET','POST'])
def detecttextip():
    url = session['url']
    return Response(generate_ip_text(url), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detectcolip', methods=['GET','POST'])
def detectcolip():
    url = session['url']
    return Response(generate_ip_col(url), mimetype='multipart/x-mixed-replace; boundary=frame')

#for speech to text
'''@app.route('/sp2text')
def sp2text():
    text_generator=SpeechToText(path_x=session.get('speech_video_path', None))
    text_list = list(text_generator)
    result = '\n'.join(text_list)
    # Render the HTML template with the text embedded within a paragraph tag
    return render_template('sp_text.html', text_response=result)'''
    

if __name__ == "__main__":
    app.run(debug=True)