# Optimizations in Compression Techniques


## Abstract
Data is becoming the cornerstone of machine learning. As it grows in size, so do the problems it presents. Compression techniques are a way to mitigate some of the problems of hardware storage, transmission time and bandwidth for large files by allowing data to be compressed and stored in a smaller format. This paper takes a look at three different lossless compression methods--Huffman compression, Wavelet compression and Fractal compression-- and compares their runtime and compression factor. Optimizations such as multi-threading on each channel for all three methods are implemented. The Huffman encoder is optimized by multi-threading on each channel and increasing memory to decrease runtime.The Fractal encoder is optimized by a known-index transformation and the implementation of a Encoder class. This allows for a higher compression factor and faster runtime when writing out to a csv file. The wavelet transformation is the most efficient of the three methods. Through multithreading and using the optimized encoder the wavelet transform has the best trade off between runtime and compression ratio. The optimization techniques presented in this paper will show that they should be considered in future compression methods.

## Introduction
As data continues to grow, it has presented many issues in storage and transmission. Big data requires large storage systems and consumes a lot of bandwidth during data transmission.  Through mathematical developments, there have been many ways to compress and reconstruct data in memory efficient manners. Compression is very beneficial in decreasing transmission time and increasing bandwidth when sharing data. When data is compressed, it is much easier to transport between different users and systems. 
Most compression techniques achieve their goal of storing data such as files or images in a smaller format; however, these techniques don’t aim to compress data in the fastest time possible. Through optimization tricks such as multi-threading and use of pre-defined variables, the following three compression techniques will be optimized in both memory used and time to execute: Huffman compression, Fractal compression, and Wavelet compression. 
All the compression techniques implemented will be lossless -- no data will be discarded. This will ensure that compression time is not reliant on a loss of quality when the image is reconstructed. This paper will not address the process of decompression -- only the process of compression and storage of data. Images will be used to compare compression techniques since this would allow for a 2D visualization in all three techniques.

## Previous Works
The three compression techniques (Huffman compression, Fractal compression, and Wavelet compression) are not new in their developments. The most naive of these techniques is Huffman compression. Huffman compression encodes each RGB value as a binary value and writes the whole image out to a binary file. Fractal compression is the most difficult of the three techniques to implement. This method of encoding iterates through the image looking for similar blocks and uses a mapping function to store this relation. The wavelet compression is the most efficient of all three methods to compress an image. It puts an image through the wavelet transformations and allows the implementation to retain as little or as much of the information from the data. 

### Huffman Encoding
Huffman encoding is a lossless encoding technique in which pixel values are replaced by bitwise representation based on the frequency of a color occurring in the image. An example is shown below of the proposed implementation. This format of encoding is a variable-length Huffman encoding.  
A 4 by 4 image has the given pixel colors.
Figure 1: Image with 3 different pixel colors.
    
Figure 2: Color Dictionary   



In a fixed length Huffman encoding, each pixel value is represented by the same number of bits. This is an expensive operation when writing out to a binary file and consumes more memory than a variable length encoding. A variable length encoding is more complicated to implement because it involves building a Huffman tree. 
The first step to variable length encoding is to create a dictionary with each color and the frequency it occurs at. This dictionary is then converted into a Huffman tree where each pixel value is encoded by its popularity. The most frequently occurring color receives the lowest bit encoding. The dictionary would be encoded as follows where red (the most frequent color) is encoded with the least number of bits. (Huffman coding - base of JPEG image compression)
Figure 3: Variable length Huffman tree encoding of the color dictionary
						
	The proposed implementation would build three variable length Huffman trees, as opposed to one which is the common format. One tree for each color channel. While this increases the memory by a slight bit--storing 3 codebooks vs. 1, this approach would allow for an implementation that decreases runtime with multi-threading. The codebook is then to be used in the decompression process to reconstruct the original image. 

### Fractal Compression
Fractal compression is the idea of storing pixel values as collections of transformations. It is very heavy in its time and amount of data that is written out. The first step in this process is to partition the image into range and domain blocks. For each of the range blocks of size s x s, find a domain block of size 2s x 2s that is “similar to it”. Mathematically this means to apply the transformations to the domain blocks and find the error between the transformed domain block and the original range block it is considered to represent. The transformation with the minimal error is chosen to represent that domain block and compared to the transformation values of the other domain blocks in the partition. The position of the range block, its appropriate transformation and the position of the domain block are then written out in another expensive time operation. This approach is called partitioned iterated function system. (Menassel, Rafik)
Partitioned iterated function system is a very time expensive method because it requires iterating over the image at least twice to find matching range and domain blocks. There are some currently existing proposals for optimization of this algorithm. The biggest time saver would be to reduce the time to find a close-enough matching domain block for each range block. Currently this is a brute force algorithm however, this can be done via dynamic programming to significantly increase the time efficiency (Texas Instruments). Another proposed solution would be to take advantage of multi-threading in ways of partitioning the image. The bottleneck issue here becomes if there are race conditions in the process and this requires a very long and complicated implementation of a multi-threading class. 

### Wavelet Compression
Wavelet compression is performed in three phases for lossy compression. The main concept is to apply a wavelet transformation, quantize the transformed image, and encode it. The wavelet transformation will generate n x m coefficients where n and m are the rows and columns of the pixels in the image. These coefficients can then be compressed because the information “is statistically concentrated in just a few coefficients” (Wavelet transform). In the proposed implementation, the most preserved information will be in Low-Low pass filtered image--usually stored at index 0. The coefficients are then put through a quantizer in the case of a lossy compression. Since the proposed implementation is lossless, the quantizer step is skipped and we proceed to the encoding step (Wikimedia Foundation). 
To decompress the image, the process is reversed. The compressed image is put into a decoder, followed by a de-quantizer (if the compression is lossy). Finally an inverse wavelet transformation is applied to recover the original image.	
Proposed Approach
The approach for each one of the compression algorithms is different. What remains the same is the method of comparison across all three. The two main comparison methods are time and compression. 

### Time Comparisons
The first metric measured will be the execution time. It is said that memory is cheap, time is expensive. For this reason, along with the fact that compression techniques already reduce memory used, run time will have a slightly higher importance than memory. The execution time of any of the three compression techniques consists of three steps: 
Time to read in image
Time to encode (compression operations occur here) 
Time to write out
All three of these steps are slightly different in each of the three compression methods. The time to read in an image is relatively constant throughout all three (fractal encoding reads in a .gif as opposed to a .jpeg). 
The time to encode will differ significantly among all three. Fractal encoding should present the highest time to encode since it performs the most extensive computations on pixel values. Huffman encoding should take the least amount of time to encode since it is at most iterating over every pixel in an image and placing them in a tree. Wavelet compression should take slightly more time to encode since it calls Huffman as its last step. 
The time to write out is the time needed to write the recorded information out to a file. For Huffman encoding and Wavelet compression this is writing out the final binary values of the original or modified image to a bin file. These two compression methods will take the same amount of time to write out since Wavelet compression calls Huffman encoding as its last step. Fractal encoding should take more time to write out as it is writing out in a csv format.

### Compression Comparisons
Memory will be measured by the compression factor which is defined as the total size of the output file divided by the size of the original image. In all three optimization techniques, the output file contains enough information along with some stored variables to reconstruct the original image. 

#### Huffman Optimization
	The Huffman implementation is extended from the 1-D data implementation written by GeeksForGeeks (Huffman Coding: Greedy Algo-3). The standard for image Huffman compression is to compress the image by pixel values and not by channels. The proposed implementation builds out three Huffman encoding trees--one for each channel. This provides time benefits when running each channel’s encoding with a single thread. Three threads will run simultaneously and build out three Huffman trees -- one per R,G,B. 
Huffman encoding will return an encoded .bin (binary) file of the image and a codebook. The codebook is a dictionary of the intensity value (between 0 and 255) and the binary encoding of that intensity value. The codebook and encoded file can then be used to recreate the original image. While the three channel tree building increases the memory by allowing the same intensity value to be encoded more than once and producing three code books to store, the time saved is worth the memory gained. 
	Note that the .bin file written out will contain the binary codes written as strings which are 8 bytes each. Therefore the final compressed file size must be divided by 8 to get the true file size.  

#### Fractal Optimization
Pierre Vigier has developed a very naive implementation of a fractal compressor and decompressor (Pvigier). Premier's implementation uses randomly ordered transformations when matching domain blocks for each range block in order to minimize the distance metric. The proposed implementation saves memory by ordering these transformations in a list in the following order: 
 0: original
 1: original, 90 degree rotation
 2: original, 180 degree rotation
 3: original, 270 degree rotation
 4: flipped (left to right)
 5: flipped, 90 degree rotation
 6: flipped, 180 degree rotation
 7: flipped, 270 degree rotation
This will allow a faster write time and higher compression rate because the output file need only contain the index of the transform performed as opposed to the direction and degree of transform. In addition, a known index implementation will not have a negative effect on the speed of decoding the image.
Another time optimization proposed is the use of an Encoder Class Object. This Encoder Class will perform operations of size calculation and reductions without the need of repeated calls. Further time optimization is proposed by encoding each channel with a single thread much like the Huffman implementation. Multi-threading can then be used to calculate the transforms of each channel which will be written out to a csv file. 

### Wavelet Optimization
	Since the implementation of all three methods are lossless, the wavelet compression implementation will not consist of having a quantizer. The proposed approach is to use three individual threads to run a wavelet transform on each one of the color channels. From the approximation coefficients, keep only the Low Pass-Low Pass coefficients and normalize them by dividing them by the max. Finally run the newly generated image through the optimized huffman encoder to get the compressed binary file. 
	The wavelet transform will be computed with three different wavelet families: Haar, Daubechies and Biorthogonal. Biorthogonal wavelet is the best for image reconstruction since it exhibits linear phase. 

Helper Classes
	Python does not support threads returning values from their target functions. For this reason, the ThreadWithReturnValue is sourced from StackOverflow. It is used in Fractal encoding and Wavelet Encoding. It allows the return values to be captured after a thread has started to run and completed its target function.

Data
The classic image in Signals and Image processing was used for all comparisons. Lenna is shown below:

Figure 4: Lenna 
The results of the three compression experiments are shown below.

Table 1: Image Read time


Huffman
Fractal
Wavelet
Read Time
0.00669
0.02175s
0.01299


Table 2: Encoding Runtime


Huffman
Fractal
Wavelet
Unoptimized
0.303s
4.448s
Haar: 0.150s
Daubechies: 0.133s
Bi-othogonal: 0.151s
Optimized
0.284s
4.405s
Haar: 0.133s
Daubechies: 0.128s
Bi-othogonal: 0.132s


Table 3: Image Write Time


Huffman
Fractal
Wavelet
Unoptimized
0.006312
0.010712s
Haar: 0.0081s
Daubechies: 0.00671s
Bi-othogonal: 0.0056s
Optimized
0.005162
0.008719s
Haar: 0.01174s
Daubechies:0.00738s
Bi-othogonal: 0.0103s




It is important to note that all times measured are averaged across 10 runs. This is done because CPU usage on any machine can have an effect on runtimes of a script. There was a fluctuation <0.01s between all the measurements of the runs, therefore averaging allowed this to be factored out. 

Table 4: Compression Factors
Huffman
Fractal
Wavelet
4.82



Unknown-Index Compression Factor: 7.528

Known-Index Compression Factor: 10.839
Haar: 19.280
Daubechies: 19.280
Bi-othogonal: 18.982


Comparison & Discussion
Runtime
	Before beginning an analysis on each of the compression techniques, it is worth noting that from here on out, the results will be discussing multi-threaded compressions. Multi-threading was more efficient in all encoding phases. While one may think that this should be expected, multithreading can have a bottleneck effect that can result in the same runtime as a non-multithreaded implementation. This case could be seen if some code block A is being run for each channel R,G,B on three different threads -- one for each channel. If code block B is reliant on all three threads finishing code block A, there will be a wait time if all three threads don’t finish at the same time. Hypothetically one of the threads could take the same amount of time to finish as it would take a non-threaded implementation. This was not the case seen in this experiment but is worth noting. 
The best encoding time is seen in the multi-threaded Wavelet transforms. The first reason for this is that the other two methods of compression are cumbersome in computation. Fractal encoding iterates through the image finding transformations that match domain to range blocks. This is rather expensive in time. Huffman encoding time relies on the size of the image and range of intensities it is given. Although Huffman encoding is used as a part of the Wavelet transform, it is fed a much smaller image to encode after generating a smaller image from the wavelet coefficients. 

	The difference between the Huffman encoding runtimes for a normal image and a wavelet transformed image can be seen in the figures below. Figure 5 shows the pixel intensities in the original image. Figure 6 shows the pixel intensities after the original image has been put through a wavelet transformer and normalized. The intensity values are concentrated at the lower end -- the Lowpass Lowpass choice. Since there are fewer intensity values to represent, Huffman encoder can have a higher compression ratio and a faster runtime. 


The Wavelet compressor is faster than the fractal compressor because a wavelet transformer has a time complexity of O(N log N). Since the Huffman encoding occurs after a new image has been generated with the Wavelet coefficients, the combined runtime of Wavelet encoding is O(N log N) + O(N log N). 

Fractal encoding has the slowest encoding time, nearly 30 times slower than Wavelet transforms. In images where patterns or repeated textures are not present, fractal encoder is not optimal. This is best understood by examining the procedure of a fractal encoder. The encoding time is heavily reliant on size s which determines the range block. The larger the range block, the harder it is to find a domain block of size 2s x 2s that can represent the range block via some transformation. This is already a delaying factor -- it is heavily reliant on an optimal size s. In the proposed implementation s is stored as factor=8. A size too small is bound to be more reliable but faces a computation penalty. In addition for every range block in the image, when finding a proper domain block, 8 transformations are computed on the domain block. This is the second delaying factor. If s is relatively large, each transformation is bound to take more time. If s is relatively small, these 8 transformations will have to be computed more times than at a larger s. The worst case runtime of a fractal encoder is O(N *N * 8 * 2s *2s). The first N is from the range blocks that are iterated over. The second N is the domain blocks iterated over. The 8 is the number of transformations conducted and final 2s * 2s are the run time for performing rotations and flips on a given domain block. 

Compression Factor 
The Huffman Encoder has the lowest compression factor of all three compression methods. This is because this encoder performs well in compression when images have relatively the same intensity values at each pixel. This can be seen in the analysis of Figures 5 and 6. Traditionally images are encoded as a whole such that R,G,B intensity values are represented in one single tree. The implementation put forth here, has built out 3 individual trees for time optimization. The worst case memory by the given implementation is M(N *8 * 255 * 3) where 8 is the max number of bits needed to represent 255 intensities across 3 color channels in an image of size n x m = N. 
The fractal encoder has a compression factor around 7 to 10. This can be further reduced by having the format of the output file be something other than a csv. If there was a huffman encoder for numeric values, the csv could have been encoded as a binary file. In the unknown transformation index it was necessary to write out the flip and rotation degree performed on the domain range. The known index method only required a single index number to be written out. In the decoding process, this index can be used to look up in O(1) time since the flip and transformations are already stored.
The wavelet encoding method is the most efficient of all three. This can be seen irrespective of what wavelet family is used in the encoding process. The high compression rate relies on the principle of transform coding. When the initial wavelet transform is done, coefficients are generated for every pixel in the image, however most of the information in the image is concentrated in just a few coefficients. These coefficients are seen when they are divided by the max. The concentration of coefficients can be seen in Figure 6. 
Conclusion
Optimization should be used to decrease runtime and increase compression factors. In a method such as Wavelet transform this can be done by using multi-threading on each channel transform. The biorthogonal family of wavelets is best for image reconstruction since it exhibits linear phase, but it is slower and has a slightly lower compression rate than the Haar and Daubechies family. For a lossy compression, the compression ratio can be lowered even further by adding a quantizer before encoding. Huffman encoding is the naivest starting point but should be used in conjunction with other compression techniques such as a wavelet transformer. A wavelet compression can have an even lower compression ratio by using other encoders with better ratios. Multithreading should be used in the encoding process to speed up runtime. The bottleneck effect may be present with multi-threading but it will never perform worse than an unthreaded implementation. 
Fractal encoding can be efficient in memory when similar textures and patterns are present in an image. This would make it easier to find a domain block that matches the range block. In addition, the size of the range block s has a significant role in the runtime of this encoder. A gradient walk implementation should be considered for finding an optimal size s. Further time optimization can occur by adding two features to the encoding process. The first should be a dynamic programming optimization to match range and domain blocks. The second should use multi-threading to perform the 8 transformation on the domain block to find which is best. For the proposed implementation of a known-index transformation, multi-threading could create race conditions that would not have been optimal when used in conjunction with the multi-threaded domain blocks. For memory optimization, a known-index transformation method should be implemented such as the one described in this paper. 

















Bibliography
“Huffman Coding: Greedy Algo-3.” GeeksforGeeks, 24 Nov. 2021, https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/#:~:text=Huffman%20coding%20is%20a%20lossless,character%20gets%20the%20largest%20code. 
Huffman coding - base of JPEG image compression. Universal Document Converter. (2013, December 27). Retrieved October 15, 2021, from https://www.print-driver.com/stories/huffman-coding-jpeg. 
Menassel, Rafik. “Optimization of Fractal Image Compression.” IntechOpen, IntechOpen, 28 July 2020, https://www.intechopen.com/chapters/72917. 
NamitS27. “Namits27/Image-Compression-Dwt at 616f72cecd893ddd266f5fa32e1e91536231a0cb.” GitHub, https://github.com/NamitS27/Image-Compression-DWT/tree/616f72cecd893ddd266f5fa32e1e91536231a0cb. 
Pvigier. “Pvigier/Fractal-Image-Compression: A Very Simple Implementation of Fractal Image Compression.” GitHub, https://github.com/pvigier/fractal-image-compression. 
Texas Instruments. (n.d.). An introduction to fractal image compression. Retrieved October 15, 2021, from https://www.ti.com/lit/an/bpra065/bpra065.pdf. 
Wavelets and image compression. Image Compression. (n.d.). Retrieved October 15, 2021, from https://rafat.github.io/sites/wavebook/app/comp.html. 
Wikimedia Foundation. (2020, October 15). Wavelet transform. Wikipedia. Retrieved October 16, 2021, from https://en.wikipedia.org/wiki/Wavelet_transform. 


