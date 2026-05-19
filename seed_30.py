import mysql.connector

db_config = {'user': 'root', 'password': 'toor', 'host': 'localhost', 'database': 'prueba'}

def seed():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE cart")
    cursor.execute("TRUNCATE TABLE order_items")
    cursor.execute("TRUNCATE TABLE orders")
    cursor.execute("TRUNCATE TABLE products")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    
    cursor.execute("SELECT id FROM users WHERE role='seller' LIMIT 1")
    seller = cursor.fetchone()
    if not seller:
        cursor.execute("INSERT INTO users (fname, lastname, email, password, role) VALUES ('Admin', 'Seller', 'admin_seller@test.com', 'hash', 'seller')")
        cnx.commit()
        seller_id = cursor.lastrowid
    else:
        seller_id = seller[0]

    productos_ejemplo = [
        ("Thriller - Michael Jackson", "Thriller es el sexto album de estudio.", 250.00, "https://cdn-images.dzcdn.net/images/cover/92a024220a9532489c75c9d994835697/500x500-000000-80-0-0.jpg", "cd", None, "1. Wanna Be Startin Somethin\n2. Baby Be Mine\n3. The Girl Is Mine\n4. Thriller\n5. Beat It\n6. Billie Jean\n7. Human Nature\n8. P.Y.T.\n9. The Lady in My Life"),
        ("Daft Punk - Random Access Memories", "Album vinilo doble", 800.00, "https://cdn-images.dzcdn.net/images/cover/311bba0fc112d15f72c8b5a65f0456c1/500x500-000000-80-0-0.jpg", "vinyl", None, "1. Give Life Back to Music\n2. The Game of Love\n3. Giorgio by Moroder\n4. Within\n5. Instant Crush\n6. Lose Yourself to Dance\n7. Touch\n8. Get Lucky\n9. Beyond\n10. Motherboard\n11. Fragments of Time\n12. Doin It Right\n13. Contact"),
        ("The Beatles - Abbey Road", "CD original remasterizado", 450.00, "https://cdn-images.dzcdn.net/images/cover/aa94ab293730bb7845d2aa8c672b2c29/500x500-000000-80-0-0.jpg", "cd", None, "1. Come Together\n2. Something\n3. Maxwells Silver Hammer\n4. Oh! Darling\n5. Octopus Garden\n6. I Want You (Shes So Heavy)\n7. Here Comes the Sun\n8. Because"),
        ("Playera Nirvana", "Playera negra con logo clasico.", 300.00, "https://cdn-images.dzcdn.net/images/cover/f0282817b697279e56df13909962a54a/500x500-000000-80-0-0.jpg", "merch", "S, M, L, XL", None),
        ("Playera Nirvana Nevermind", "Playera 100% algodon.", 350.00, "https://cdn-images.dzcdn.net/images/cover/f0282817b697279e56df13909962a54a/500x500-000000-80-0-0.jpg", "merch", "S, M, L, XL", None),
        ("Sudadera Arctic Monkeys", "Sudadera oficial AM.", 600.00, "https://cdn-images.dzcdn.net/images/cover/64e54e307bd5e2bdb27ffeb662fd910d/500x500-000000-80-0-0.jpg", "merch", "M, L", None),
        ("Taza The Beatles", "Taza de ceramica Abbey Road.", 150.00, "https://cdn-images.dzcdn.net/images/cover/aa94ab293730bb7845d2aa8c672b2c29/500x500-000000-80-0-0.jpg", "merch", "Unitalla", None),
        ("Gorra Red Hot Chili Peppers", "Gorra bordada con logo.", 250.00, "https://cdn-images.dzcdn.net/images/cover/5e61e8290a4d1d64ca58920656c9602d/500x500-000000-80-0-0.jpg", "merch", "Unitalla", None),
        ("Playera Pink Floyd", "Playera Dark Side of the Moon.", 300.00, "https://cdn-images.dzcdn.net/images/cover/2bea643b92a8fc6b19a23756f718cbd4/500x500-000000-80-0-0.jpg", "merch", "S, M, XL", None),
        ("Póster Metallica", "Poster Ride the Lightning 60x90cm.", 120.00, "https://cdn-images.dzcdn.net/images/cover/4f2093c9d25852c8f1937ae5a47b99a6/500x500-000000-80-0-0.jpg", "merch", "Unitalla", None),
        ("Llavero Queen", "Llavero de metal con logo clasico.", 80.00, "https://cdn-images.dzcdn.net/images/cover/6706f1154083f461a348508c28030a30/500x500-000000-80-0-0.jpg", "merch", "Unitalla", None),
        ("Mochila Gorillaz", "Mochila Demon Days.", 700.00, "https://cdn-images.dzcdn.net/images/cover/3dc29a565149240729afc08e1f251b46/500x500-000000-80-0-0.jpg", "merch", "Unitalla", None),
        ("Playera The Strokes", "Is This It merch.", 300.00, "https://cdn-images.dzcdn.net/images/cover/f8a0a2e1ec12c1026cd03208237cd934/500x500-000000-80-0-0.jpg", "merch", "M, L, XL", None),
        ("Calcetines David Bowie", "Calcetines Aladdin Sane.", 100.00, "https://cdn-images.dzcdn.net/images/cover/e16455433a84c7e19025403ae3eec52d/500x500-000000-80-0-0.jpg", "merch", "Unitalla", None),
        ("Pink Floyd - The Dark Side of the Moon", "Vinilo de 180g remasterizado.", 900.00, "https://cdn-images.dzcdn.net/images/cover/e635a8510c1a74bc089b3566ebbb9cb8/500x500-000000-80-0-0.jpg", "vinyl", None, "1. Speak to Me\n2. Breathe\n3. On the Run\n4. Time\n5. The Great Gig in the Sky\n6. Money\n7. Us and Them\n8. Any Colour You Like\n9. Brain Damage\n10. Eclipse"),
        ("Nirvana - Nevermind", "Vinilo clásico del grunge.", 850.00, "https://cdn-images.dzcdn.net/images/cover/f0282817b697279e56df13909962a54a/500x500-000000-80-0-0.jpg", "vinyl", None, "1. Smells Like Teen Spirit\n2. In Bloom\n3. Come as You Are\n4. Breed"),
        ("Michael Jackson - Bad", "Edicion especial en vinilo.", 950.00, "https://cdn-images.dzcdn.net/images/cover/fb0a49a91ab8137ec9d028c4dbb04021/500x500-000000-80-0-0.jpg", "vinyl", None, "1. Bad\n2. The Way You Make Me Feel\n3. Speed Demon\n4. Liberian Girl\n5. Just Good Friends\n6. Another Part of Me"),
        ("Kendrick Lamar - To Pimp a Butterfly", "Doble LP vinilo.", 1100.00, "https://cdn-images.dzcdn.net/images/cover/00dd0da365a94b1829302d6b7fec70e6/500x500-000000-80-0-0.jpg", "vinyl", None, "1. Wesley's Theory\n2. For Free?\n3. King Kunta\n4. Institutionalized"),
        ("Radiohead - OK Computer", "Vinilo doble.", 1000.00, "https://cdn-images.dzcdn.net/images/cover/05a186e0a859a36f9cd51cdae2158fe1/500x500-000000-80-0-0.jpg", "vinyl", None, "1. Airbag\n2. Paranoid Android\n3. Subterranean Homesick Alien\n4. Exit Music (For a Film)\n5. Let Down"),
        ("Fleetwood Mac - Rumours", "Vinilo estándar.", 800.00, "https://cdn-images.dzcdn.net/images/cover/9732751ce91d786dcf30069853697078/500x500-000000-80-0-0.jpg", "vinyl", None, "1. Second Hand News\n2. Dreams\n3. Never Going Back Again\n4. Don't Stop"),
        ("Arctic Monkeys - AM", "Vinilo importado.", 900.00, "https://cdn-images.dzcdn.net/images/cover/64e54e307bd5e2bdb27ffeb662fd910d/500x500-000000-80-0-0.jpg", "vinyl", None, "1. Do I Wanna Know?\n2. R U Mine?\n3. One for the Road\n4. Arabella\n5. I Want It All"),
        ("Rosalía - MOTOMAMI", "Vinilo rojo translúcido.", 1200.00, "https://cdn-images.dzcdn.net/images/cover/66ae12120936d9660d3e30a7db7627b8/500x500-000000-80-0-0.jpg", "vinyl", None, "1. SAOKO\n2. CANDY\n3. LA FAMA\n4. BULERÍAS"),
        ("Dua Lipa - Future Nostalgia", "CD Digipack.", 400.00, "https://cdn-images.dzcdn.net/images/cover/f8364f090ba04f1b19b381ec0390f3e4/500x500-000000-80-0-0.jpg", "cd", None, "1. Future Nostalgia\n2. Don't Start Now\n3. Cool\n4. Physical\n5. Levitating\n6. Pretty Please"),
        ("The Weeknd - After Hours", "CD Estándar.", 450.00, "https://cdn-images.dzcdn.net/images/cover/fd00ebd6d30d7253f813dba3bb1c66a9/500x500-000000-80-0-0.jpg", "cd", None, "1. Alone Again\n2. Too Late\n3. Hardest To Love\n4. Scared To Live\n5. Snowchild\n6. Escape From LA"),
        ("Harry Styles - Harry's House", "CD edición normal.", 450.00, "https://cdn-images.dzcdn.net/images/cover/b0e936124f59e669ddba02ebe5893f95/500x500-000000-80-0-0.jpg", "cd", None, "1. Music for a Sushi Restaurant\n2. Late Night Talking\n3. Grapejuice\n4. As It Was\n5. Daylight"),
        ("Bad Bunny - Un Verano Sin Ti", "CD Digipack especial.", 500.00, "https://cdn-images.dzcdn.net/images/cover/b29d1070377b784384c2456093f96a66/500x500-000000-80-0-0.jpg", "cd", None, "1. Moscow Mule\n2. Después de la Playa\n3. Me Porto Bonito\n4. Tití Me Preguntó\n5. Un Ratito"),
        ("Taylor Swift - 1989 (Taylor's Version)", "CD original.", 450.00, "https://cdn-images.dzcdn.net/images/cover/60c1f1896b2f6b4a4a29ca45d314d4bf/500x500-000000-80-0-0.jpg", "cd", None, "1. Welcome to New York\n2. Blank Space\n3. Style\n4. Out of the Woods\n5. All You Had to Do Was Stay"),
        ("Coldplay - Parachutes", "CD Joya clasico.", 300.00, "https://cdn-images.dzcdn.net/images/cover/970dce98eeea6729244c0ae71707a83d/500x500-000000-80-0-0.jpg", "cd", None, "1. Don't Panic\n2. Shiver\n3. Spies\n4. Sparks\n5. Yellow\n6. Trouble"),
        ("Adele - 21", "CD estándar.", 350.00, "https://cdn-images.dzcdn.net/images/cover/dc1ce848d830ecc93521be5a78350364/500x500-000000-80-0-0.jpg", "cd", None, "1. Rolling in the Deep\n2. Rumour Has It\n3. Turning Tables\n4. Don't You Remember\n5. Set Fire to the Rain"),
        ("Guardians of the Galaxy - Awesome Mix Vol. 1", "Cassette retro.", 600.00, "https://cdn-images.dzcdn.net/images/cover/09d72e7b1162403dc2c1b43f891fb167/500x500-000000-80-0-0.jpg", "cassette", None, "1. Hooked on a Feeling\n2. Go All the Way\n3. Spirit in the Sky\n4. Moonage Daydream\n5. Fooled Around and Fell in Love"),
        ("Stranger Things - Soundtrack", "Cassette rojo.", 550.00, "https://cdn-images.dzcdn.net/images/cover/a3996622e0d55c887255c45a3c1291bd/500x500-000000-80-0-0.jpg", "cassette", None, "1. Stranger Things\n2. Kids\n3. Nancy and Barb\n4. This Isn't You\n5. Lay-Z-Boy"),
        ("Depeche Mode - Violator", "Cassette vintage.", 400.00, "https://cdn-images.dzcdn.net/images/cover/2632e326fac7c48c2fbef198f295995a/500x500-000000-80-0-0.jpg", "cassette", None, "1. World in My Eyes\n2. Sweetest Perfection\n3. Personal Jesus\n4. Halo\n5. Waiting for the Night\n6. Enjoy the Silence"),
        ("The Smiths - The Queen Is Dead", "Cassette clásico.", 450.00, "https://cdn-images.dzcdn.net/images/cover/7ca9c4c9988765720bf3b722e101d2c3/500x500-000000-80-0-0.jpg", "cassette", None, "1. The Queen Is Dead\n2. Frankly, Mr. Shankly\n3. I Know It's Over\n4. Never Had No One Ever\n5. Cemetry Gates"),
        ("Joy Division - Unknown Pleasures", "Cassette edición limitada.", 500.00, "https://cdn-images.dzcdn.net/images/cover/013c601da70bf83a0fea61bd9c526449/500x500-000000-80-0-0.jpg", "cassette", None, "1. Disorder\n2. Day of the Lords\n3. Candidate\n4. Insight\n5. New Dawn Fades")
    ]

    for p in productos_ejemplo:
        title, desc, price, img, category, sizes, *tracklist = p
        track = tracklist[0] if tracklist else None
        
        query = "INSERT INTO products (seller_id, title, description, price, image_url, category, stock, sizes, tracklist) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (seller_id, title, desc, price, img, category, 20, sizes, track))

    cnx.commit()
    cursor.close()
    cnx.close()
    print(f"Restaurados {len(productos_ejemplo)} productos con imágenes originales.")

if __name__ == '__main__':
    seed()
