import glob
import cv2
import math
import numpy as np

#list_images_names = glob.glob("images//*.jpeg")

#list_images = [cv2.imread(i) for i in list_images_names]

def arrange(list_images,n_rows = 4, out_width = 600, out_height = 700):

    #n_rows = 4
    n = len(list_images)
    
    #out_width = 600
    #out_height = 700
    
    heightPerRow = out_height//n_rows
    
    list_aspects = [i.shape[1]/i.shape[0] for i in list_images]
    
    list_widths = [math.ceil(heightPerRow*i) for i in list_aspects]
    
    list_images_resize = [cv2.resize(list_images[i],(list_widths[i],heightPerRow)) for i in range(n)]
    
    total_area = sum([i.shape[0]*i.shape[1] for i in list_images_resize])
    
    if (sum(list_widths) > out_width*n_rows):
        
        print(" The images won't fit, try more rows or bigger out_width ")
        return None, None
        
    elif (out_height - n_rows*heightPerRow < 0): 
        
        print(" output_height is too small ")
        return None, None
    
    else :
        
        out_image = np.zeros((out_height,out_width,3),dtype = 'uint8')
        
        rowVise = []
        
        ind = 0
        
        for i in range(n_rows):
            
            if (ind >= n) : break
            
            curr = list_widths[ind]
            img = list_images_resize[ind] 
            ind+=1
            
            while (ind<n and curr+list_widths[ind] <= out_width):
                
                img = cv2.hconcat([img,list_images_resize[ind]])
                curr+=list_widths[ind]
                ind+=1
            
            rowVise.append(img)
        
        output_image = np.zeros((0,out_width,3),dtype = 'uint8')
        
        for i in range(len(rowVise)):
            
            temp = rowVise[i]
            
            temp_h, temp_w = temp.shape[0], temp.shape[1]
            
            extra = np.zeros((temp_h,out_width-temp_w,3),dtype = 'uint8')
            
            output_image = cv2.vconcat([output_image,cv2.hconcat([temp,extra])])
        
        extra = np.zeros((out_height - len(rowVise)*heightPerRow,out_width,3),dtype = 'uint8')
        output_image = cv2.vconcat([output_image,extra])
        
        print(" success")
        return output_image, total_area
        #cv2.imwrite("Output//output.jpeg",output_image)