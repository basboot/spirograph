# Spirograph

Spirograph figures in Python... just for fun! :-)

<video width="660" controls autoplay muted loop>
  <source src="assets/pi.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

This π symbol is drawn by 2302 rotating circles.

## How it Works

The project uses Fast Fourier Transform (FFT) to decompose 2D paths into their frequency components, where each
component represents a rotating circle (epicycle) that contributes to recreating the original shape.
