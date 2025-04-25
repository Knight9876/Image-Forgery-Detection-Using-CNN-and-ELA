import numpy as np
from keras.models import load_model
from ela import convert_to_ela_image, highlight_forged_areas, convert_to_ela_image_gray


def prepare_image(fname):
    image_size = (128, 128)
    return (
        np.array(convert_to_ela_image(fname[0], 90).resize(image_size)).flatten()
        / 255.0
    )  # return ela_image as a numpy array


def predict_result(fname):
    model = load_model("trained_model.h5")  # load the trained model
    class_names = ["Forged", "Authentic"]  # classification outputs
    test_image = prepare_image(fname)
    test_image = test_image.reshape(-1, 128, 128, 3)

    y_pred = model.predict(test_image)
    y_pred_class = round(y_pred[0][0])

    prediction = class_names[y_pred_class]
    if y_pred <= 0.5:
        confidence = f"{(1-(y_pred[0][0])) * 100:0.2f}"
    else:
        confidence = f"{(y_pred[0][0]) * 100:0.2f}"

    if prediction == "Forged":
        # Highlight forged areas if prediction is forged
        original_image, ela_image_gray = convert_to_ela_image_gray(fname[0], 90)
        highlighted_image_path = highlight_forged_areas(original_image, ela_image_gray)
        print(f"Forged areas highlighted in {highlighted_image_path}")
    
    return (prediction, confidence)
