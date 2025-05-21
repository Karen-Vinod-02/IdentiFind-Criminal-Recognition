# IdentiFind 

**IdentiFind** is a criminal face detection and recognition system designed for identity verification at checkpoints, entrances, or other access-controlled areas.

It uses face detection and recognition models to capture and compare facial data against a mugshot database. Built with **Django**, it uses **RetinaFace** (for detection) and **ArcFace** (for recognition).

---

##  Features

- Real-time face detection using images from webcam
- Face comparison against a criminal mugshot database  
- Instant alert with record details if a match is found  
- Admin interface for managing records via Django  

---

## Tech Stack

- **Backend**: Python, Django  
- **Face Detection**: RetinaFace 
- **Face Recognition**: ArcFace 
- **Frontend**: HTML/CSS 

---

## Dataset & Media

- **Dataset Sources**:
  - **IDOC Dataset** from [Kaggle](https://www.kaggle.com/datasets/davidjfisher/illinois-doc-labeled-faces-dataset)
- **Preloaded Records**:
  - First **20 criminal images** are already placed in the `media/front/` directory for testing purposes.

- **Full Dataset**:
  - Remaining mugshots can be downloaded manually from [Kaggle](https://www.kaggle.com/datasets/davidjfisher/illinois-doc-labeled-faces-dataset) or [Hugging Face](https://huggingface.co/datasets/bitmind/idoc-mugshots).

- **CSV Files**:
  - Already placed in `criminal_rec/data/`. No additional downloads required.

---

##  Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/Karen-Vinod-02/IdentiFind-Criminal-Recognition.git
cd IdentiFind
``` 

### 2. Install Dependencies

``` 
pip install -r requirements.txt
```
### 3. Configure Environment Variables
This project uses a .env file to manage sensitive settings . You would need to create your own Django secret key.
- In the root directory of the project, create a file named `.env`.
- Add the following line to the file:
``` 
DJANGO_SECRET_KEY= #your-secure-secret-key
```

**Note**: If DJANGO_SECRET_KEY is not set in the environment, the app will raise an error when starting. This is handled in settings.py for security.

### 4. Apply Migrations
```
python manage.py migrate

```

### 5. Create a Superuser

To access the Django admin panel, you need to create a superuser:

```
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.
You can now log in at http://127.0.0.1:8000/admin using these credentials. 

## Running the Project
```
python manage.py runserver
```
Then open your browser and visit:
http://127.0.0.1:8000/admin
Use the Django admin panel to manage criminal records, view uploads, and monitor matches.

## Importing Criminal Records from CSV
To bulk import entries into the database:
- Ensure that the mugshots referenced in the CSV exist in media/front/.
- Run the import script:
```
python import_criminals.py
```
This script:
- Loads criminal records from the .csv files
- Inserts them into the Django database(accessible via admin panel)
- Links each entry to its corresponding image (if present)

## Acknowledgements
- IDOC Mugshot Dataset – [Kaggle](https://www.kaggle.com/datasets/davidjfisher/illinois-doc-labeled-faces-dataset)
- Face detection - RetinaFace (Deng et al., CVPR 2020)
- Face recognition - ArcFace (Deng et al., CVPR 2019)
- Background image – [cottonbro studio from Pexels](https://www.pexels.com/photo/man-and-photos-on-brown-corkboard-8369526/)

## Disclaimer
This project is for academic and demonstration purposes only. It is not intended for real-world deployment without proper legal, ethical, and security reviews.

