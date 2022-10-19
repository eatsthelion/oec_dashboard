import os

fontDict = {
    'Montserrat':{
        'directory' : r'O:\pythonprograms\Fonts\Montserrat\static',
        'family' : [
            'Montserrat-Black.ttf',
            'Montserrat-BlackItalic.ttf',
            'Montserrat-Bold.ttf',
            'Montserrat-BoldItalic.ttf',
            'Montserrat-ExtraBold.ttf',
            'Montserrat-ExtraBoldItalic.ttf',
            'Montserrat-ExtraLight.ttf',
            'Montserrat-ExtraLightItalic.ttf',
            'Montserrat-Italic.ttf',
            'Montserrat-Light.ttf',
            'Montserrat-LightItalic.ttf',
            'Montserrat-Medium.ttf',
            'Montserrat-MediumItalic.ttf',
            'Montserrat-Regular.ttf',
            'Montserrat-SemiBold.ttf',
            'Montserrat-SemiBoldItalic.ttf',
            'Montserrat-Thin.ttf',
            'Montserrat-ThinItalic.ttf',
            ]
        },
}
try:
    import pyglet
    for fontfamily in fontDict:
        for font in fontDict[fontfamily]['family']: 
            pyglet.font.add_file(os.path.join(fontDict[fontfamily]['directory'],font))
except: pass