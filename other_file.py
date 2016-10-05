import googlemaps


gmaps = googlemaps.Client(key='api_key_here')

b = 0
while True:
    a = gmaps.geocode('address here')

    print('latitude: '.__add__(a[0]['geometry']['location']['lat'].__str__()),
          '\nlength: '.__add__(a[0]['geometry']['location']['lng'].__str__()),
          '\n'.__add__(a[0]['formatted_address']))
    b += 1
    print(b)



from PIL import Image


image = Image.open('path_here')
new_image = image.rotate(0)
new_image = new_image.resize((960, 640))
new_image.save('image.jpg')

crop_image = new_image.crop((59, 260, 285, 435))

crop_image.save('crop_image.jpg')
