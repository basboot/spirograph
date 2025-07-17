# Spirograph

Spirograph figures in Python... just for fun! :-)

![pi](https://github.com/user-attachments/assets/c0206fdd-d276-4d6f-9ab2-757a71d66e60)


This π symbol is drawn by 2302 rotating circles.

But we can reduce frequency (at the the cost of losing some accuracy).

![einstein](https://github.com/user-attachments/assets/7ad5f205-6b65-43b9-9a79-9025dc12fcea)

This person you might recognize was drawn with just 780 rotating circles.

## How it Works

The project uses Fast Fourier Transform (FFT) to decompose 2D paths into their frequency components, where each
component represents a rotating circle (epicycle) that contributes to recreating the original shape.
