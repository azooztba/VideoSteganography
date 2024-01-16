"""The code is provided for educational purposes only. It is intended to help individuals learn about coding, programming, and related concepts.
 The use of this code for any malicious or unauthorized activities is strictly prohibited.
 The author is not responsible for any misuse or damage caused by this code. 
 Use it responsibly and within the bounds of ethical and legal guidelines."""

import argparse
import cv2
import numpy as np
from skimage import metrics
from stegano import lsb
from os.path import isfile,join                                                              
import math
import os
import shutil
from subprocess import call,STDOUT



def extract_frames(video_path,tmp_path="./tmp"):
    # Extract frames from the video.
    
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    temp_folder=tmp_path
    print(tmp_path," directory is created")

    vidcap = cv2.VideoCapture(video_path)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    count = 0
    print("Frames = ",frame_count)
    print("Extracting frames . . .")
    for i in range(frame_count):
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(i)), image)
    print("Extracting frames: DONE.")

def split_message(s_str,count=10):
    # Split the message to chunks

    per_c=math.ceil(len(s_str)/count)
    c_cout=0
    out_str=''
    split_list=[]
    for s in s_str:
        out_str+=s
        c_cout+=1
        if c_cout == per_c:
            split_list.append(out_str)
            out_str=''
            c_cout=0
    if c_cout!=0:
        split_list.append(out_str)
    return split_list

def embed_message(input_string,root="./tmp/"):
    # Embed message inside the extracted frames
     
    for i in range(0,len(input_string)):
        f_name="{}{}.png".format(root,i)
        secret_enc=lsb.hide(f_name,input_string[i])
        secret_enc.save(f_name)
        print("[INFO] frame {} holds {}".format(f_name,input_string[i]))

def clean_tmp(path="./tmp"):
    # Remove the temporary directory

    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"[INFO] {path} files are cleaned up")

def extract_message(video_path):
    # Extract message from video

    print("Starting the extraction . . .")
    extract_frames(video_path)
    secret=[]
    root="./tmp/"
    for i in range(len(os.listdir(root))):
        f_name="{}{}.png".format(root,i)
        try:
            
            secret_dec=lsb.reveal(f_name)
            secret.append(secret_dec)
            print("frame ",f_name, "contains: ",secret_dec )
        except:
            break
    print("secret message= ",''.join([i for i in secret]))
    clean_tmp()

def compare_video_quality(original_video_path, stego_video_path):
    # Compare video quality between two videos using SSIM metric

    print("Starting the comparison. . .")
    extract_frames(original_video_path,tmp_path="./tmp1")
    extract_frames(stego_video_path,tmp_path='./tmp2')

    ssim_scores=[]
    all_files1 = os.listdir("./tmp1")
    files1 = [filename for filename in all_files1 if os.path.isfile(os.path.join("./tmp1", filename))]
    all_files2 = os.listdir("./tmp2")
    files2 = [filename for filename in all_files2 if os.path.isfile(os.path.join("./tmp2", filename))]
    sorted_files1 = sorted(files1)
    sorted_files2 = sorted(files2)

    counter=1
    for file_tmp1, file_tmp2 in zip(sorted_files1, sorted_files2):
        full_path_tmp1 = os.path.join("./tmp1", file_tmp1)
        full_path_tmp2 = os.path.join("./tmp2", file_tmp2)
        # Read images using OpenCV
        img1 = cv2.imread(full_path_tmp1, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(full_path_tmp2, cv2.IMREAD_GRAYSCALE)
        ssim_score = metrics.structural_similarity(img1, img2, full=True)
        ssim_scores.append(ssim_score[0])
        if counter%10==0:
            print("Completed ",counter," SSIM comparisons.")
        counter+=1
    
    ssim_scores=np.array(ssim_scores)
    print(f"SSIM Score: ", np.mean(ssim_scores))
    clean_tmp(path="./tmp1")
    clean_tmp(path="./tmp2")


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="LSB Video Steganography Tool")
    parser.add_argument("mode", choices=["embed", "extract","compare"], help="Select 'embed' to embed a message or 'extract' to extract a message or 'compare' to compare the quality of the original file and the stego file.")
    parser.add_argument("video_path", help="Input Video file path(Mp4 format)")
    parser.add_argument("--stego_path", help="Stego Video file path")
    parser.add_argument("--message", help="Message to embed")
    args = parser.parse_args()

    #check arguments
    if args.mode == "embed":
        if not args.video_path:
            parser.error("Input video is required for embedding.")
            exit()
        if not args.message:
            parser.error("Message is required for embedding.")
            exit()

        extract_frames(args.video_path)
        message_chunks = split_message(args.message)
        # extract audio
        call(["ffmpeg", "-i",args.video_path, "-q:a", "0", "-map", "a", "tmp/audio.wav", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        # Embed message to the frames
        stego_video_path = "stego_video.avi"
        embed_message(message_chunks)
        # frames back into video and add the audio
        call(["ffmpeg", "-i", "tmp/%d.png", "-i", "tmp/audio.wav", "-c:v", "ffv1", "-c:a", "copy", stego_video_path, "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        clean_tmp()

    elif args.mode == "extract":
        if not args.video_path:
            parser.error("Stego video is required for extracting.")
            exit()
        
        # Extract the message
        extract_message(args.video_path)
    
    elif args.mode == 'compare':
        if not args.stego_path:
            parser.error("Stego video is required for comparing.")
            exit()
        if not args.video_path:
            parser.error("original video is required for comparing.")
            exit()

        compare_video_quality(args.video_path,args.stego_path)