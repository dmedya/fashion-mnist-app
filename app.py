from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)

# Sınıf isimleri
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Modeli yükle ve eğit
try:
    # Fashion MNIST veri setini yükle
    (train_images, train_labels), _ = tf.keras.datasets.fashion_mnist.load_data()
    train_images = train_images / 255.0

    # Model oluştur
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                 loss='sparse_categorical_crossentropy',
                 metrics=['accuracy'])

    # Modeli eğit
    model.fit(train_images, train_labels, epochs=10)
    print("Model başarıyla eğitildi!")

except Exception as e:
    print("Model eğitme hatası:", e)
    raise

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'Dosya yüklenmedi'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Dosya seçilmedi'})
        
        try:
            # Resmi oku ve işle
            image = Image.open(file.stream).convert('L')  # Gri tonlamaya çevir
            image = image.resize((28, 28))
            
            # Görüntüyü numpy dizisine çevir ve ön işleme
            image_array = np.array(image)
            image_array = 255 - image_array  # Renkleri tersine çevir (beyaz arka plan -> siyah arka plan)
            image_array = image_array / 255.0  # Normalize et
            
            # Görüntüyü kontrol et
            print("Görüntü şekli:", image_array.shape)
            print("Görüntü değer aralığı:", image_array.min(), "-", image_array.max())
            
            # Tahmin yap
            prediction = model.predict(image_array.reshape(1, 28, 28))
            predicted_class = class_names[np.argmax(prediction)]
            confidence = float(np.max(prediction))
            
            return jsonify({
                'prediction': predicted_class,
                'confidence': confidence
            })
            
        except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
