# LSB-Video-Steganography

This is a project i did for the CY461-INTRODUCTION TO STEGANOGRAPHY course at JUST university.

This is a python code that implements LSB steganography in the raw sapatial domain of the cover video.
Please check the documentation PDF to learn more about the tool.

### Main functions
* Embedding.
  * Takes any video as input and the message you want to embed, and produces a wav file (stego video). 
* Extraction.
  * Takes the stego video as input, and returns the extracted secret message.
* SSIM.
  * Takes two videos as input, and returns the average SSIM score between every 2 frames of the video. It is used to check the quality difference between the two videos. 

### Notes
*  You need to use a video player that supports ffv1 like VLC media player, to play the stego video.
*  You can change the Video codec only to other lossless video codecs, like the ones mentiond in https://en.wikipedia.org/wiki/List_of_codecs#Lossless_video_compression .

### TODO
* Add embedding in the Audio stream of the file.
  * i think this can be done by using lossless audio codecs.


### Disclaimer
*  The code is provided for educational purposes only. It is intended to help individuals learn about coding, programming, and related concepts. The use of this code for any malicious or unauthorized activities is strictly prohibited. The author is not responsible for any misuse or damage caused by this code. Use it responsibly and within the bounds of ethical and legal guidelines.
*  Do not share my work without my permission.
*  If you want permission, please email me on mailto:azooztbaishat@gmail.com
