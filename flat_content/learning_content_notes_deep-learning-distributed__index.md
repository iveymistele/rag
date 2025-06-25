Deep Learning (DL) is a powerful tool transforming scientific workflows. Because DL training is computationally intensive, it is well suited to HPC systems. Effective use of UVA HPC resources can greatly accelerate your DL workflows. In this tutorial, we will discuss:
* When is it appropriate to use a GPU?
* How to optimize single-GPU code?
* How to convert single-GPU code to Multi-GPU code in different frameworks and run it on UVA HPC?

The following outline presents topics that will be discussed as well as when code will be provided:
* Overview of Deep Learning
    * Example: Convolutional Neural Network
* Introduction to GPUs and GPU Computing
* Tensorflow/Keras
    * Single-GPU Code Example
* PyTorch
    * Single-GPU Code Example
* Distributed Training
    * TF Multi-GPU Code Example
    * PT Multi-GPU Code Example
    * PT Lightning Multi-GPU Code Example
* Effective Use/Remarks

Prior experience with the Python programming language and some familiarity with machine learning concepts are helpful for this tutorial. 

If you have not already done so, please download the example code here:

{{< file-download file="/notes/deep-learning-distributed/code/distributed_dl.zip" text="distributed_dl.zip" >}}
