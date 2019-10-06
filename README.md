# sisr-app
Drag and drop app to increase resolution of images with Single Image, Super Resolution model.

## Inna's to-do list:
- [x] create a single page
- [x] add drag and drop space/button. check if file has .jpg format. if not, display "we support jpg format only"
- [ ] display image that was dragged into drag-and-drop space
- [ ] display loading and then new image, next to the original image. new image can be any image, hardcoded for now.
- [ ] call python code from javascript like this: https://stackoverflow.com/questions/13175510/call-python-function-from-javascript-code

## Rose's to-do list:
- [x] push Python scrit to the repo
- [ ] add video input support?
- [] check the accuracy and improvement
## Mock-up 
![Mock-up v1.0](IMG_20190830_125427747.jpg?raw=true "Mock-up v1.0")

## How to Use Python Script
`python3 increase_resolution.py -i <image> -m <model>.xml`

Example:

`python3 increase_resolution.py -i one.jpg -m 1032/FP16/single-image-super-resolution-1032.xml`

