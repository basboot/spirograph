# Spirograph

Spirograph figures in Python... just for fun! :-)

![pi](https://github.com/user-attachments/assets/c0206fdd-d276-4d6f-9ab2-757a71d66e60)


This π symbol is drawn by 2302 rotating circles.

## How it Works

The project uses Fast Fourier Transform (FFT) to decompose 2D paths into their frequency components, where each
component represents a rotating circle (epicycle) that contributes to recreating the original shape.
