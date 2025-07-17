# Spirograph

Spirograph figures in Python... just for fun! :-)

![pi](https://github.com/user-attachments/assets/c0206fdd-d276-4d6f-9ab2-757a71d66e60)


This π symbol is drawn by 2302 rotating circles.

![einsteingif](https://github.com/user-attachments/assets/ca8c5b11-cb62-439b-b260-065ae1403944)

This person you might recognize was drawn with just 3509 rotating circles.

## How it Works

The project uses Fast Fourier Transform (FFT) to decompose 2D paths into their frequency components, where each
component represents a rotating circle (epicycle) that contributes to recreating the original shape.
