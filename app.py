from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
app.secret_key = 'Plant'

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PLANT_INFO = {
    "Aloevera": {
         "A succulent plant known for its medicinal properties, particularly for soothing burns and skin care."
    },
    "Amla": {
         "Also known as Indian Gooseberry, rich in Vitamin C and widely used in Ayurvedic medicine."
    },
    "Amruta_Balli": {
         "Known as Giloy or Guduchi, it is a medicinal herb used to boost immunity and treat fever."
    },
    "Arali": {
         "Refers to Oleander, a flowering plant often used for ornamental purposes but can be toxic."
    },
    "Ashoka": {
         "A sacred tree in India, valued for its medicinal properties, particularly in treating gynecological disorders."
    },
    "Ashwagandha": {
         "A powerful adaptogen known for reducing stress, boosting energy, and improving overall health."
    },
    "Avacado": {
         "A nutrient-rich fruit high in healthy fats, commonly used in cooking and skincare."
    },
    "Bamboo": {
     "A fast-growing grass species used in construction, crafts, and as a source of food (bamboo shoots)."
    },
    "Basale": {
         "Also known as Malabar Spinach, a leafy vegetable rich in vitamins and iron."
    },
    "Betel": {
         "A vine whose leaves are chewed in many cultures for their stimulant and medicinal properties."
    },
    "Betel_Nut": {
         "Also called Areca Nut, it is chewed as a stimulant but can have harmful effects with excessive use."
    },
    "Brahmi": {
     "A medicinal herb known for enhancing memory, reducing anxiety, and improving brain function."
    },
    "Castor": {
     "A plant whose seeds are used to produce castor oil, known for its medicinal and industrial uses."
    },
    "Curry_Leaf": {
         "A flavorful herb widely used in Indian cuisine and known for its digestive and antioxidant properties."
    },
    "Doddapatre": {
         "Also called Indian Borage, it is used in traditional medicine to treat colds, coughs, and digestive issues."
    },
    "Ekka": {
         "A flowering plant species, often used in traditional medicine for its antimicrobial properties."
    },
    "Ganike": {
         "A local plant used for its medicinal and culinary properties, especially in South India."
    },
    "Gauva": {
         "A tropical fruit rich in Vitamin C and dietary fiber, known for its sweet and tangy flavor."
    },
    "Geranium": {
         "An aromatic plant often used in essential oils and perfumes for its floral fragrance."
    },
    "Henna": {
         "A plant whose leaves are used to create a natural dye for hair and skin decoration."
    },
    "Hibiscus": {
     "A flowering plant known for its vibrant blooms and use in teas and hair care products."
    },
    "Honge": {
         "Also known as Indian Beech, it is used for oil production and in traditional medicine."
    },
    "Insulin": {
         "Refers to Costus Igneus, known as the Insulin Plant, believed to help manage diabetes."
    },
    "Jasmine": {
         "A fragrant flowering plant often used in perfumes and as a decorative plant."
    },
    "Lemon": {
         "A citrus fruit rich in Vitamin C, widely used in cooking, beverages, and cleaning."
    },
    "Lemon_grass": {
         "A fragrant herb used in teas, soups, and traditional medicine for its calming properties."
    },
    "Mango": {
         "A tropical fruit loved for its sweet flavor and high content of vitamins A and C."
    },
    "Mint": {
         "A refreshing herb commonly used in teas, cooking, and as a digestive aid."
    },
    "Nagadali": {
         "A traditional medicinal plant known for its healing properties."
    },
    "Neem": {
         "A tree with strong antibacterial and antifungal properties, widely used in skincare and medicine."
    },
    "Nithyapushpa": {
         "A perennial flowering plant used for ornamental purposes and in traditional medicine."
    },
    "Nooni": {
         "Also known as Noni, it is a fruit-bearing plant used for its purported health benefits."
    },
    "Pappaya": {
         "A tropical fruit rich in enzymes like papain, which aid digestion."
    },
    "Pepper": {
         "A spice derived from the Piper plant, used to add heat and flavor to dishes."
    },
    "Pomegranate": {
         "A fruit with antioxidant-rich seeds, known for its health benefits and sweet-tart taste."
    },
    "Raktachandini": {
     "A medicinal plant known for its use in treating skin disorders and wounds."
    },
    "Rose": {
         "A flowering plant known for its beauty and fragrance, often used in perfumes and cosmetics."
    },
    "Sapota": {
     "Also known as Chikoo, a tropical fruit with a sweet, malty flavor."
    },
    "Tulasi": {
         "Also known as Holy Basil, it is revered for its healing properties and is widely used in Ayurveda."
    },
    "Wood_sorel": {
         "A small plant with tangy leaves, often used in salads and traditional medicine."
    }
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Call the model to detect the disease using the saved file
            result = predict_disease(file_path)
            description=PLANT_INFO.get(result)
            
            return render_template('result.html', result=result,description=description, image_file=filename)
    return render_template('detect.html')

def predict_disease(image_path):
    model = tf.keras.models.load_model('C:/Users/shrav/Downloads/leaf/model/plant_medicinal_model.h5')
    
    # Load image from the file path and preprocess
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Add batch dimension
    img_array /= 255.  # Normalize image

    # Predict using the model
    predictions = model.predict(img_array)

    # Get the predicted class index
    predicted_class = tf.argmax(predictions[0]).numpy()

    # Class names based on your model
    class_names =['Aloevera', 'Amla', 'Amruta_Balli', 'Arali', 'Ashoka', 'Ashwagandha', 'Avacado', 'Bamboo', 'Basale', 'Betel', 'Betel_Nut', 'Brahmi', 'Castor', 'Curry_Leaf', 'Doddapatre', 'Ekka', 'Ganike', 'Gauva', 'Geranium', 'Henna', 'Hibiscus', 'Honge', 'Insulin', 'Jasmine', 'Lemon', 'Lemon_grass', 'Mango', 'Mint', 'Nagadali', 'Neem', 'Nithyapushpa', 'Nooni', 'Pappaya', 'Pepper', 'Pomegranate', 'Raktachandini', 'Rose', 'Sapota', 'Tulasi', 'Wood_sorel']
    return class_names[predicted_class]

if __name__ == '__main__':
    app.run(debug=True)
