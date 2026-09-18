"""
Seed script to populate the PostgreSQL database with all DROPP catalog products and customer reviews.
"""

from database.settings import SessionLocal, engine
from models.setup import Base, Product, Review


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    women_products = [
        {
            "itemname": "Everyday Straight Leg Pants",
            "description": "High-waisted straight-leg pants designed for everyday comfort with a relaxed fit and adjustable tie waist.",
            "images": [
                "https://i.pinimg.com/736x/4f/bd/7b/4fbd7ba14b539887330811573b0af239.jpg",
                "https://i.pinimg.com/736x/bc/79/d6/bc79d6b971d1f3c47e0f00db33f8a392.jpg",
            ],
            "price": "Rs. 6,500",
            "ratings": 4.8,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL"],
            "details_and_care": [
                "100% Cotton Twill",
                "High-waisted with relaxed straight cut",
                "Machine wash cold, hang dry",
            ],
            "shipping_and_return": [
                "Free shipping on orders over Rs. 5,000",
                "30-day effortless returns",
            ],
        },
        {
            "itemname": "Oversized Essential Hoodie",
            "description": "A premium oversized hoodie made for effortless everyday styling with a soft brushed interior.",
            "images": [
                "https://images.unsplash.com/photo-1556821840-3a63f95609a7",
                "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633",
            ],
            "price": "Rs. 7,500",
            "ratings": 4.7,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
            "details_and_care": [
                "450gsm Heavyweight French Terry",
                "Ribbed cuffs and hem",
                "Machine wash cold",
            ],
            "shipping_and_return": ["Free standard shipping", "Free exchange"],
        },
        {
            "itemname": "Classic Cropped Jacket",
            "description": "A structured cropped jacket with a modern silhouette, perfect for layering during cooler days.",
            "images": [
                "https://images.unsplash.com/photo-1544022613-e87ca75a784a",
                "https://images.unsplash.com/photo-1591047139829-d91aecb6caea",
            ],
            "price": "Rs. 11,000",
            "ratings": 4.9,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["XS", "S", "M", "L", "XL"],
            "details_and_care": ["Structured wool-blend fabric", "Dry clean only"],
            "shipping_and_return": ["Dispatched in 24 hours", "30-day returns"],
        },
        {
            "itemname": "Relaxed Cotton T-Shirt",
            "description": "Soft heavyweight cotton T-shirt with a relaxed silhouette and clean minimal finish.",
            "images": [
                "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab",
                "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c",
            ],
            "price": "Rs. 3,500",
            "ratings": 4.6,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["XXS", "XS", "S", "M", "L", "XL", "XXL"],
            "details_and_care": ["100% Combed ring-spun cotton", "Machine wash cold"],
            "shipping_and_return": ["Complimentary returns within 30 days"],
        },
        {
            "itemname": "Wide Leg Cargo Pants",
            "description": "Utility-inspired wide-leg cargo pants featuring multiple pockets and a comfortable high-rise waist.",
            "images": [
                "https://i.pinimg.com/736x/a6/0c/de/a60cde89d460f680ffa5ce2fb61dd8fc.jpg",
                "https://i.pinimg.com/736x/a6/0c/de/a60cde89d460f680ffa5ce2fb61dd8fc.jpg",
            ],
            "price": "Rs. 8,500",
            "ratings": 4.7,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
            "details_and_care": ["Ripstop cotton blend", "Machine wash cold"],
            "shipping_and_return": ["Free shipping over Rs. 5,000"],
        },
        {
            "itemname": "Minimal Ribbed Tank Top",
            "description": "A versatile ribbed tank top with a fitted silhouette that works effortlessly on its own or layered.",
            "images": [
                "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3",
                "https://images.unsplash.com/photo-1564859228273-274232fdb516",
            ],
            "price": "Rs. 2,900",
            "ratings": 4.5,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["XXS", "XS", "S", "M", "L", "XL"],
            "details_and_care": ["95% Organic cotton, 5% elastane"],
            "shipping_and_return": ["Hassle-free 30-day returns"],
        },
        {
            "itemname": "Relaxed Denim Jeans",
            "description": "Classic relaxed-fit denim jeans featuring a comfortable high-rise waist and timeless washed finish.",
            "images": [
                "https://images.unsplash.com/photo-1541099649105-f69ad21f3246",
                "https://images.unsplash.com/photo-1582418702059-97ebafb35d09",
            ],
            "price": "Rs. 8,900",
            "ratings": 4.8,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["24", "26", "28", "30", "32", "34"],
            "details_and_care": ["13oz Rigid denim", "Wash inside out"],
            "shipping_and_return": ["Fast delivery in 2-4 business days"],
        },
        {
            "itemname": "Satin Slip Dress",
            "description": "Elegant satin slip dress with a flowing silhouette designed for effortless evening styling.",
            "images": [
                "https://images.unsplash.com/photo-1566174053879-31528523f8ae",
                "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446",
            ],
            "price": "Rs. 9,500",
            "ratings": 4.9,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["XS", "S", "M", "L", "XL"],
            "details_and_care": [
                "Liquid drape satin finish",
                "Hand wash or gentle cycle",
            ],
            "shipping_and_return": ["30-day return guarantee"],
        },
        {
            "itemname": "Classic Knit Cardigan",
            "description": "Soft textured cardigan with a relaxed fit and timeless button-front design.",
            "images": [
                "https://images.unsplash.com/photo-1434389677669-e08b4cac3105",
                "https://images.unsplash.com/photo-1576566588028-4147f3842f27",
            ],
            "price": "Rs. 7,900",
            "ratings": 4.6,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
            "details_and_care": ["Chunky rib knit texture", "Dry clean recommended"],
            "shipping_and_return": ["Complimentary shipping over Rs. 5,000"],
        },
        {
            "itemname": "Tailored Blazer",
            "description": "Modern tailored blazer with a clean structured silhouette suitable for both casual and formal looks.",
            "images": [
                "https://images.unsplash.com/photo-1551028719-00167b16eac5",
                "https://images.unsplash.com/photo-1591369822096-ffd140ec948f",
            ],
            "price": "Rs. 12,500",
            "ratings": 4.8,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["XS", "S", "M", "L", "XL"],
            "details_and_care": ["Double-breasted front with horn buttons"],
            "shipping_and_return": ["Express delivery option available"],
        },
        {
            "itemname": "Everyday Mini Skirt",
            "description": "Minimal everyday mini skirt featuring a flattering silhouette and easy-to-style design.",
            "images": [
                "https://i.pinimg.com/1200x/49/d9/36/49d936da425e0bd29033190bf2e99e91.jpg",
                "https://i.pinimg.com/1200x/49/d9/36/49d936da425e0bd29033190bf2e99e91.jpg",
            ],
            "price": "Rs. 5,500",
            "ratings": 4.5,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["XXS", "XS", "S", "M", "L", "XL"],
            "details_and_care": ["A-line silhouette", "Machine wash cold"],
            "shipping_and_return": ["Free returns within 30 days"],
        },
        {
            "itemname": "Premium Oversized Shirt",
            "description": "Relaxed oversized shirt crafted for a clean contemporary look with a lightweight comfortable feel.",
            "images": [
                "https://images.unsplash.com/photo-1596755389378-c31d21fd1273",
                "https://images.unsplash.com/photo-1605763240000-7e93b172d754",
            ],
            "price": "Rs. 6,900",
            "ratings": 4.7,
            "gender": "female",
            "availability": "In Stock",
            "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
            "details_and_care": ["Crisp cotton poplin weave", "Wash warm, line dry"],
            "shipping_and_return": ["Fast fulfillment"],
        },
    ]

    men_products = [
        {
            "itemname": "Essential Oversized Hoodie (Men)",
            "description": "Heavyweight oversized hoodie designed with a relaxed fit and soft brushed interior for everyday comfort.",
            "images": [
                "https://images.unsplash.com/photo-1556821840-3a63f95609a7",
                "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633",
            ],
            "price": "Rs. 7,900",
            "ratings": 4.8,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["S", "M", "L", "XL", "XXL", "XXXL"],
            "details_and_care": ["Heavyweight 450gsm fleece", "Kangaroo pocket"],
            "shipping_and_return": ["Free shipping over Rs. 5,000"],
        },
        {
            "itemname": "Classic Straight Jeans (Men)",
            "description": "Timeless straight-fit denim jeans featuring a durable cotton construction and versatile washed finish.",
            "images": [
                "https://images.unsplash.com/photo-1542272604-787c3835535d",
                "https://images.unsplash.com/photo-1604176354204-9268737828e4",
            ],
            "price": "Rs. 8,900",
            "ratings": 4.7,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["28", "30", "32", "34", "36", "38"],
            "details_and_care": ["100% Selvedge cotton denim", "Button fly"],
            "shipping_and_return": ["30-day exchange guarantee"],
        },
        {
            "itemname": "Heavyweight Graphic T-Shirt",
            "description": "Premium heavyweight cotton T-shirt featuring a relaxed silhouette and understated graphic detail.",
            "images": [
                "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab",
                "https://images.unsplash.com/photo-1503341504253-dff4815485f1",
            ],
            "price": "Rs. 4,200",
            "ratings": 4.6,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["S", "M", "L", "XL", "XXL"],
            "details_and_care": ["280gsm Heavy jersey", "Screen printed detail"],
            "shipping_and_return": ["Free returns within 30 days"],
        },
        {
            "itemname": "Relaxed Cargo Pants (Men)",
            "description": "Modern cargo pants with a relaxed fit, utility pockets and adjustable waist details.",
            "images": [
                "https://images.unsplash.com/photo-1516826957135-700dedea698c",
                "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80",
            ],
            "price": "Rs. 8,500",
            "ratings": 4.8,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["S", "M", "L", "XL", "XXL"],
            "details_and_care": ["Twill weave with reinforced seams"],
            "shipping_and_return": ["Fast dispatch"],
        },
        {
            "itemname": "Classic Oxford Shirt (Men)",
            "description": "Clean Oxford shirt designed with a regular fit and versatile styling for everyday and smart occasions.",
            "images": [
                "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf",
                "https://images.unsplash.com/photo-1598033129183-c4f50c736f10",
            ],
            "price": "Rs. 6,500",
            "ratings": 4.7,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["S", "M", "L", "XL", "XXL"],
            "details_and_care": ["100% Oxford cotton weave"],
            "shipping_and_return": ["30-day returns"],
        },
        {
            "itemname": "Minimal Bomber Jacket",
            "description": "Contemporary bomber jacket with a clean silhouette, ribbed cuffs and lightweight insulated construction.",
            "images": [
                "https://images.unsplash.com/photo-1551028719-00167b16eac5",
                "https://images.unsplash.com/photo-1548883354-94bcfe321cbb",
            ],
            "price": "Rs. 11,900",
            "ratings": 4.9,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["S", "M", "L", "XL", "XXL"],
            "details_and_care": ["Satin nylon shell, thermal polyfill"],
            "shipping_and_return": ["Complimentary shipping"],
        },
        {
            "itemname": "Relaxed Linen Shirt",
            "description": "Breathable linen shirt with a relaxed fit, ideal for warm days and effortless summer outfits.",
            "images": [
                "https://images.unsplash.com/photo-1603252109303-2751441dd157",
                "https://images.unsplash.com/photo-1596755389378-c31d21fd1273",
            ],
            "price": "Rs. 7,200",
            "ratings": 4.6,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["S", "M", "L", "XL", "XXL"],
            "details_and_care": ["100% French flax linen"],
            "shipping_and_return": ["Free 30-day exchange"],
        },
        {
            "itemname": "Everyday Chino Pants",
            "description": "Versatile tapered chino pants made from comfortable stretch cotton for everyday wear.",
            "images": [
                "https://images.unsplash.com/photo-1473966968600-fa801b869a1a",
                "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80",
            ],
            "price": "Rs. 6,900",
            "ratings": 4.7,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["28", "30", "32", "34", "36", "38"],
            "details_and_care": ["98% Cotton, 2% spandex"],
            "shipping_and_return": ["Dispatched within 24h"],
        },
        {
            "itemname": "Premium Knit Polo",
            "description": "Modern knitted polo featuring a refined collar and relaxed silhouette for elevated everyday dressing.",
            "images": [
                "https://i.pinimg.com/736x/e2/19/0b/e2190badb9301678860c13d5ace0187a.jpg",
                "https://i.pinimg.com/736x/e2/19/0b/e2190badb9301678860c13d5ace0187a.jpg",
            ],
            "price": "Rs. 7,500",
            "ratings": 4.8,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["S", "M", "L", "XL", "XXL"],
            "details_and_care": ["Fine gauge cotton knit"],
            "shipping_and_return": ["Free shipping over Rs. 5,000"],
        },
        {
            "itemname": "Utility Overshirt",
            "description": "Versatile heavyweight overshirt with functional pockets and a relaxed fit for easy layering.",
            "images": [
                "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3",
                "https://images.unsplash.com/photo-1598033129183-c4f50c736f10",
            ],
            "price": "Rs. 9,500",
            "ratings": 4.7,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["S", "M", "L", "XL", "XXL"],
            "details_and_care": ["Heavyweight moleskin cotton"],
            "shipping_and_return": ["30-day return policy"],
        },
        {
            "itemname": "Relaxed Sweatpants (Men)",
            "description": "Comfort-focused sweatpants with a relaxed silhouette, elastic waistband and soft fleece interior.",
            "images": [
                "https://images.unsplash.com/photo-1552902865-b72c031ac5ea",
                "https://images.unsplash.com/photo-1580906855281-6e0c2b0b1a2e",
            ],
            "price": "Rs. 6,200",
            "ratings": 4.6,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["S", "M", "L", "XL", "XXL", "XXXL"],
            "details_and_care": ["Soft brushed fleece, custom metal aglets"],
            "shipping_and_return": ["Free shipping over Rs. 5,000"],
        },
        {
            "itemname": "Structured Wool Coat",
            "description": "Premium structured wool coat featuring a clean tailored silhouette designed for colder seasons.",
            "images": [
                "https://images.unsplash.com/photo-1539533113208-f6df8cc8b543",
                "https://images.unsplash.com/photo-1544923246-77307dd628b9",
            ],
            "price": "Rs. 14,900",
            "ratings": 4.9,
            "gender": "male",
            "availability": "In Stock",
            "available_sizes": ["S", "M", "L", "XL", "XXL"],
            "details_and_care": ["70% Melange wool, 30% recycled poly"],
            "shipping_and_return": ["Complimentary tracked delivery"],
        },
    ]

    all_products = women_products + men_products

    print("Checking existing products in database...")
    created_product_ids = {}

    for prod_data in all_products:
        existing = (
            db.query(Product).filter(Product.itemname == prod_data["itemname"]).first()
        )
        if not existing:
            new_p = Product(**prod_data)
            db.add(new_p)
            db.commit()
            db.refresh(new_p)
            print(f"Created product: {new_p.itemname} (id={new_p.id})")
            created_product_ids[new_p.itemname] = new_p.id
        else:
            # Update price and shipping text to Nepali Rupees
            existing.price = prod_data["price"]
            existing.shipping_and_return = prod_data["shipping_and_return"]
            db.commit()
            created_product_ids[existing.itemname] = existing.id

    # Seed Customer Reviews
    sample_reviews = [
        {
            "customer_name": "Sophia Martin",
            "customer_rating": 5,
            "customer_review": "Absolutely love the fit and quality. The fabric feels premium and the pants look exactly like the pictures.",
        },
        {
            "customer_name": "Daniel Carter",
            "customer_rating": 5,
            "customer_review": "The hoodie is incredibly comfortable and the oversized fit is perfect. Definitely ordering another one.",
        },
        {
            "customer_name": "Emma Wilson",
            "customer_rating": 4,
            "customer_review": "Really nice jacket with a great silhouette. Shipping was quick and the packaging was also very neat.",
        },
        {
            "customer_name": "Oliver James",
            "customer_rating": 5,
            "customer_review": "The quality exceeded my expectations. The material feels heavy and durable without being uncomfortable.",
        },
        {
            "customer_name": "Mia Anderson",
            "customer_rating": 4,
            "customer_review": "The cargo pants have a really good fit and plenty of pocket space. The sizing was accurate for me.",
        },
        {
            "customer_name": "James Wilson",
            "customer_rating": 5,
            "customer_review": "Simple, clean and comfortable. Exactly what I was looking for in an everyday wardrobe piece.",
        },
        {
            "customer_name": "Ava Thompson",
            "customer_rating": 5,
            "customer_review": "The jeans fit beautifully and the washed finish looks even better in person. Highly recommended.",
        },
        {
            "customer_name": "Lucas Brown",
            "customer_rating": 4,
            "customer_review": "Very comfortable and well made. I especially liked the attention to detail around the stitching.",
        },
        {
            "customer_name": "Isabella Taylor",
            "customer_rating": 5,
            "customer_review": "Beautiful dress with a really elegant shape. It feels lightweight and comfortable while still looking premium.",
        },
        {
            "customer_name": "Noah Williams",
            "customer_rating": 5,
            "customer_review": "The blazer has a very clean structure and fits perfectly. It works really well with both casual and formal outfits.",
        },
        {
            "customer_name": "Grace Davis",
            "customer_rating": 4,
            "customer_review": "Really versatile skirt and easy to style. The material is comfortable and the fit is flattering.",
        },
        {
            "customer_name": "Ethan Miller",
            "customer_rating": 5,
            "customer_review": "The shirt has a great oversized fit without looking messy. Fabric is lightweight and perfect for layering.",
        },
    ]

    first_product_id = (
        list(created_product_ids.values())[0] if created_product_ids else 1
    )

    for idx, r in enumerate(sample_reviews):
        existing_rev = (
            db.query(Review).filter(Review.customer_name == r["customer_name"]).first()
        )
        if not existing_rev:
            p_id = (
                list(created_product_ids.values())[idx % len(created_product_ids)]
                if created_product_ids
                else first_product_id
            )
            rev = Review(
                product=p_id,
                customer_name=r["customer_name"],
                customer_rating=r["customer_rating"],
                customer_review=r["customer_review"],
            )
            db.add(rev)
            db.commit()
            print(f"Created review from {r['customer_name']}")

    total_products = db.query(Product).count()
    total_reviews = db.query(Review).count()
    print(
        f"\nDatabase seeding complete! Total Products: {total_products}, Total Reviews: {total_reviews}"
    )
    db.close()


if __name__ == "__main__":
    seed()
