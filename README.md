# Spirograph

Spirograph figures in Python... just for fun! :-)

https://github.com/user-attachments/assets/b7e96521-15b9-48dd-9c11-5f2f554e724d

This π symbol is drawn by 2302 rotating circles.

## How it Works

The project uses Fast Fourier Transform (FFT) to decompose 2D paths into their frequency components, where each
component represents a rotating circle (epicycle) that contributes to recreating the original shape.
