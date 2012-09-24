"""
The MIT License

Copyright (c) 2012 William Dollins (bill@geomusings.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
Helper class to assist with calculating dimensions of WeoGeo base image and
thumbnail image using the aspect ratio of user-provided geographic extent
"""

import math

class WeoAspectRatio:
    _right = 0
    _left = 0
    _top = 0
    _bottom = 0
    _thumbnail = 61
    _baseimage = 256

    def __init__(self, right=0, left=0, top=0, bottom=0):
        global _right, _left, _top, _bottom, _thumbnail, _baseimage
        _thumbnail = 61
        _baseimage = 256
        _right = right
        _left = left
        _top = top
        _bottom = bottom

    def showValues(self):
        print _right, _left, _top, _bottom

    def xDim(self):
        return math.fabs(_right - _left)
        
    def yDim(self):
        return math.fabs(_top - _bottom)

    def aspect(self):
        asp = 0
        if self.yDim() != 0 and self.xDim() != 0:
            asp = min(self.xDim(), self.yDim()) / max(self.xDim(), self.yDim())
        return asp

    def thumbDimensions(self):
        return self.getDimensions(_thumbnail)

    def baseDimensions(self):
        return self.getDimensions(_baseimage)

    def pageDimensions(self, pageSize):
        return self.getDimensions(pageSize)

    def getDimensions(self, imgwidth):
        shortDim = imgwidth * self.aspect();
        height = 0
        width = 0
        if self.aspect() == 1:
            height = imgwidth
            width = imgwidth
        elif self.yDim() > self.xDim():
            height = imgwidth
            width = shortDim
        elif self.xDim() > self.yDim():
            height = shortDim
            width = imgwidth
        return height, width
