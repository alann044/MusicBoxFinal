import mysql.connector
import urllib.parse

db_config = {'user': 'root', 'password': 'toor', 'host': 'localhost', 'database': 'prueba'}

def fix_db():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor(dictionary=True)
    
    # 1. Update the first 4 products with tracklist and sizes
    updates = [
        # 1. Thriller - CD
        "UPDATE products SET tracklist='1. Wanna Be Startin Somethin\n2. Baby Be Mine\n3. The Girl Is Mine\n4. Thriller\n5. Beat It\n6. Billie Jean\n7. Human Nature\n8. P.Y.T. (Pretty Young Thing)\n9. The Lady in My Life' WHERE id=1",
        
        # 2. Daft Punk - Vinyl
        "UPDATE products SET tracklist='1. Give Life Back to Music\n2. The Game of Love\n3. Giorgio by Moroder\n4. Within\n5. Instant Crush\n6. Lose Yourself to Dance\n7. Touch\n8. Get Lucky\n9. Beyond\n10. Motherboard\n11. Fragments of Time\n12. Doin It Right\n13. Contact' WHERE id=2",
        
        # 3. Abbey Road - CD
        "UPDATE products SET tracklist='1. Come Together\n2. Something\n3. Maxwells Silver Hammer\n4. Oh! Darling\n5. Octopus Garden\n6. I Want You (Shes So Heavy)\n7. Here Comes the Sun\n8. Because' WHERE id=3",
        
        # 4. Playera Nirvana - Merch
        "UPDATE products SET sizes='S, M, L, XL' WHERE id=4"
    ]
    
    for q in updates:
        cursor.execute(q)
    
    # 2. Fix images for ALL products
    # We will use placehold.co to generate clean, stylized images based on the title
    cursor.execute("SELECT id, title, category FROM products")
    products = cursor.fetchall()
    
    for p in products:
        # Create a URL safe string for the placeholder text
        text = urllib.parse.quote_plus(p['title'])
        if p['category'] == 'merch':
            # Use unsplash random shirt images for merch or placeholder
            img_url = f"https://placehold.co/500x500/111111/FFEA20?text={text}"
        else:
            # Use placeholder for albums to guarantee loading
            img_url = f"https://placehold.co/500x500/111111/FFEA20?text={text}"
            
        cursor.execute("UPDATE products SET image_url=%s WHERE id=%s", (img_url, p['id']))
        
    cnx.commit()
    cursor.close()
    cnx.close()
    print("Base de datos corregida correctamente.")

if __name__ == '__main__':
    fix_db()
