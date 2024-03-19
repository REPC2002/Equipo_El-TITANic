from jinja2 import Template
import json
import os

with open('book_data.json', 'r') as file:
    books = json.load(file)

# Your HTML template with placeholders for dynamic data
html_template = '''
<!DOCTYPE html>
<html lang="es-mx">
<head>
    <title>Proyecto 1</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Kumar+One+Outline&family=Norican&family=Poly:ital@0;1&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=K2D:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800&family=Kumar+One+Outline&family=Norican&family=Poly:ital@0;1&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Julee&family=K2D:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800&family=Knewave&family=Kumar+One+Outline&family=Norican&family=Poly:ital@0;1&display=swap" rel="stylesheet">
    <style>
        .container {
            width: 89vw;
            min-height: 79vh;
            padding: 5%;
            background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)),
            url("../Images/Background_Books.jpg");
            background-position: left;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        
        .info_container {
            text-align: center;
            max-width: 600px;
            margin-right: 20px; /* Espaciado entre la informacion */
            background-color: rgba(224, 224, 224, 0.8);
        }
        .info_container h3 {
            font-family: "Knewave", system-ui;
            font-weight: 400;
            font-style: normal;
        }
        .author_info {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px; /* Espaciado entre el título del libro y la información del autor */
        }
        .author_info p {text-align: left;}
        
        .author_info img {
            width: 250px; 
            margin-bottom: 10px;
        }
        
        .book_image img {width: 300px;}
        
        h2 {
            margin-bottom: 20px;
            font-style: italic;
            font-size: xx-large;
            font-family: "Norican", cursive;
            font-weight: 400;
            font-style: normal;
        }
        .info_container p {
            font-family: "K2D", sans-serif;
            font-weight: 100;
            font-style: normal;
        }
    </style>
</head>
<body>
    <div class="container">
        <main class="info_container">
            <h2> {{nombre}} </h2>
            <h3> {{autor}} </h3>
            <!-- Información y Imagen del autor -->
            <div class="author_info">
                <img src="{{autor_imagen_url}}">
                <p>
                    {{sinopsis}}
                </p>
                 <p>
                    Categorias: {{categoria}}
                </p>
            </div>
        </main>
        <div class="book_image">
            <!-- Imagen del Libro -->
            <img src="{{imagen_url}}">  
        </div>
    </div>
</body>
</html>
'''
    
    # Directory to save the HTML files
output_directory = "./html/books"

# Create the directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Render the template for each object in the dictionary
for key, book in books.items():
    # Render the template with the object's attributes
    template = Template(html_template)
    rendered_html = template.render(book)

    # Generate the file path for the HTML file
    file_path = os.path.join(output_directory, f"book{key}.html")

    # Write the rendered HTML to the file
    with open(file_path, "w") as file:
        file.write(rendered_html)

    print(f"HTML file generated for {key} at: {file_path}")