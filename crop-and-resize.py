    @classmethod
    def make_images(cls, img, **kwargs):
        """
        The class method for create a lot image objects with different resolutions and formats.
        Return the needed resolutions and formats without waiting creation of others objects.
        :param img: the original img base64 object
        :param kwargs: the kwargs which have resolutions and formats
        :return: the queryset of new only needed objects
        """
        cls.create_images(img, **kwargs)
        ImageCreator(img, cls, **kwargs).start()

    @classmethod
    def crop_and_resize_image(cls, img, resolution, crop=True):
        """
        The method for crop image with needed resolutions
        :param img: the original image in base64 format
        :param resolution: the Height x Width parameters in string type
        :param crop: True if need to crop image before return the resized image
        :return: the new cropped image
        """
        try:
            img = PILImage.open(BytesIO(base64.b64decode(img)))
        except TypeError:
            """
            Catch for Image object instead of base64 image in parameters
            """
            pass

        width, height = resolution.split('x')

        if img.size[0] < img.size[1]:
            ratio = int(width) / img.size[0]
            new_height = int(img.size[1] * ratio)
            new_img = img.resize((int(width), new_height), PILImage.ANTIALIAS)

            box = (0, (new_img.size[1] - int(height)) / 2, new_img.size[0], (new_img.size[1] + int(height)) / 2)
        else:
            ratio = int(height) / img.size[1]
            new_width = int(img.size[0] * ratio)
            new_img = img.resize((new_width, int(height)), PILImage.ANTIALIAS)

            box = ((new_img.size[0] - int(width)) / 2, 0, (new_img.size[0] + int(width)) / 2, new_img.size[1])

        if crop:
            new_img = new_img.crop(box)
        return new_img

    @classmethod
    def create_images(cls, img, **kwargs):
        """
        The method for proper create Image objects.
        :param img: the original image
        :param kwargs: dictionary with resolutions and format
        :return: the list of new objects
        """
        img_format = kwargs.get('format', 'JPEG')
        images = []
        resolutions = kwargs.get('resolutions') if kwargs.get('resolutions') else [kwargs.get('resolution')]
        for resolution in resolutions:
            crop_for_max_result = True if resolution is settings.IMAGE_RESOLUTIONS[-1] else False
            cropped_img = cls.crop_and_resize_image(img, resolution, crop=crop_for_max_result)

            # create the double sized image for retina.js/retina displays
            double_sized_resolution = cls.get_double_sized_resolution(resolution)
            doubled_image = cls.crop_and_resize_image(cropped_img, double_sized_resolution, crop=False)
            random_img_name = uuid.uuid4()
            images_with_params = [
                (cropped_img, random_img_name, resolution),
                (doubled_image, str(random_img_name) + "@2x", double_sized_resolution)
            ]

            for image, img_name, size in images_with_params:
                out_img = BytesIO()
                try:
                    image.save(out_img, img_format, subsampling=0, quality=90)
                except OSError:
                    """
                    Needed for catching the exception because some formats cannot be saved without converting to RGB.
                    """
                    image = cropped_img.convert('RGB')
                    image.save(out_img, img_format, subsampling=0, quality=90)

                img_info = {
                    'img': ContentFile(out_img.getvalue(), name="%s.%s" % (img_name, img_format)),
                    'format': img_format,
                    'resolution': size
                }
                images.append(img_info)

        return cls.save_images(images, **kwargs)

    @classmethod
    def save_images(cls, images, **kwargs):
        """
        Save images as django objects from Content files
        :param images: the list of content files
        :param kwargs: kwargs with all options for Image model
        :return: the queryset of new objects
        """
        for image in images:
            new_img = cls.objects.create(
                parent=kwargs.get('imageInstance'),
                resolution=image['resolution'],
                img_format=image['format'],
                image=image['img']
            )
            # new_img.image.save(image['img'].name, image['img'], save=True)

    @classmethod
    def get_double_sized_resolution(cls, resolution):
        """
        The help-method for create the new resolution with doubled sizes
        :param resolution: the needed resolution for double sizing
        :return: the new doubled resolution
        """
        sizes = resolution.split('x')
        double_sized_resolution = "x".join([str(int(x) * 2) for x in sizes])
        return double_sized_resolution


class ImageCreator(threading.Thread):
    """
    The asynchronous class for creating cropped Images.
    """
    def __init__(self, original_img, sender, **kwargs):
        self.img, self.sender = original_img, sender

        for param in kwargs:
            setattr(self, param, kwargs[param])

        super(ImageCreator, self).__init__()

    def run(self):
        for img_format in settings.IMAGE_FORMATS:
            for resolution in settings.IMAGE_RESOLUTIONS:
                skip = resolution in getattr(self, 'resolutions') and img_format == getattr(self, 'format')
                if not skip:
                    self.sender.create_images(
                        img=self.img,
                        format=img_format,
                        resolution=resolution,
                        imageInstance=getattr(self, 'imageInstance')
                    )
