from image_segmentation_aicore.utils import ImageSegmentation, get_image, run_visualization

model = ImageSegmentation('model.tar.gz')
category = 'cat'
img_url = ''
img = get_image(category=category)
img = img or img_url
run_visualization(model, img)