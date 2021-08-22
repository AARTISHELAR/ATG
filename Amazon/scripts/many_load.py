import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load

from Home.models import Product,Rating


def run():
    fhand = open('Home/amazon_product.csv')
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    Rating.objects.all().delete()
    

    
    for col in reader:
        print(col)

        try:
            rate= float(col[5])
        except:
            rate = None
        rating, created = Rating.objects.get_or_create(rate=rate)
        
        try:
            price = float(col[2])
        except:
            price = None
        
        try:
            global_rating = int(col[6][:-2])
            print(global_rating)
        except Exception as e:
            print(e)
            global_rating = None

        

        #site = Site(name=col[0],description=col[1],justification=col[2],year=year,longitude=longitude,latitude=latitude,area_hectares=area_hectares,category=category,state=state,region=region,iso=iso)
        product = Product(product_name = col[1],price = price,discount=col[3],image=col[4],rating=rating,global_rating=global_rating)
        product.save()

        